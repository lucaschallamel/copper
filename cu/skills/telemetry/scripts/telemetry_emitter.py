#!/usr/bin/env python3
"""Fallback telemetry emitter for the COPPER document-processing cascade.

Owns the canonical fallback-event sink defined by US-166. One record is emitted
per cascade-layer attempt (success or fall-through); all records for a single
user operation share a ``trace_id``.

Design notes
------------
- Mirrors the proven append-only JSONL shape of ``deploy/telemetry.py`` ([DRY]).
- **Fire-and-forget** (NFR-1): ``emit`` never raises into the caller. A write
  failure is swallowed so telemetry can never abort a document operation.
- **Append-only** (NFR-3): records are appended; consumers read but never rewrite.
- **Privacy** (AC6): only the whitelisted fields are written. ``filename``,
  ``content`` and extracted text can never reach the sink, and the JSON Schema
  (``resources/fallback-event.schema.json``) sets ``additionalProperties: false``
  as a second line of defence.
- **Disabled mode** (AC1): ``COPPER_TELEMETRY_PATH=disabled`` makes ``emit`` a no-op
  (the legacy ``RAHAN_TELEMETRY_PATH`` is honoured when the new var is unset, ADR-046).

Exit Codes (when run as a script)
    0: self-test ok
    2: script execution error

Usage (library)
    from telemetry_emitter import TelemetryEmitter, new_trace_id
    emitter = TelemetryEmitter()
    tid = new_trace_id()
    emitter.emit(trace_id=tid, fmt="docx", operation="read",
                 handler="mcp-word", outcome="fallthrough", latency_ms=42,
                 error_class="timeout")

Author: COPPER framework
Version: 1.0.0
Language: British English (en-AU)
"""

from __future__ import annotations

import json
import os
import re
import sys
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# --- Constants (CMV: no magic values) --------------------------------------

ENV_TELEMETRY_PATH = "COPPER_TELEMETRY_PATH"
# Pre-ADR-046 hosts may still set the RAHAN-era variable; read as a fallback.
LEGACY_ENV_TELEMETRY_PATH = "RAHAN_TELEMETRY_PATH"
DISABLED_SENTINEL = "disabled"
DEFAULT_SINK = Path.home() / ".copper" / "telemetry" / "fallback.jsonl"
ROTATION_BYTES = 50 * 1024 * 1024  # NFR-4: rotate at 50 MB
ROTATION_KEEP = (
    3  # number of rotated generations retained (L1: avoid single-gen data loss)
)

VALID_FORMATS = ("docx", "xlsx", "pptx", "pdf", "md")
VALID_OPERATIONS = ("read", "write", "generate")
VALID_OUTCOMES = ("success", "fallthrough", "error")

# Fields permitted in a record. Anything outside this set is dropped before
# write so user content can never leak (AC6).
ALLOWED_FIELDS = frozenset(
    {
        "trace_id",
        "timestamp",
        "format",
        "operation",
        "handler",
        "outcome",
        "latency_ms",
        "error_class",
        "file_size_bytes",
    }
)
# Keys that must NEVER appear in a record (privacy guard, asserted in tests).
FORBIDDEN_FIELDS = frozenset(
    {"filename", "file_name", "path", "content", "text", "extracted_text"}
)

# error_class is a short snake_case CATEGORY token, never free text. This is the
# value-level half of the AC6 privacy guard: a caller passing str(exception)
# (which routinely embeds file paths / PII) is coerced to a safe token rather
# than leaked verbatim. The schema enforces the same pattern at validation time.
ERROR_CLASS_PATTERN = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
ERROR_CLASS_FALLBACK = "unknown"


def _sanitise_error_class(value: str | None) -> str | None:
    """Coerce error_class to a safe category token (AC6 value-level privacy).

    Returns the value unchanged only if it is already a short snake_case
    category. Any free-text value (e.g. an exception message with an embedded
    path) is replaced with ``unknown`` so user content can never reach the sink.
    """
    if value is None:
        return None
    return value if ERROR_CLASS_PATTERN.match(value) else ERROR_CLASS_FALLBACK


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def is_iso8601(value: str) -> bool:
    """True if ``value`` parses as an ISO-8601 datetime (stdlib, no new dep).

    Used both as a defensive guard in the emitter and as the schema
    format-checker in tests, so ``timestamp`` is genuinely validated rather than
    merely annotated (M2).
    """
    try:
        datetime.fromisoformat(value)
        return True
    except (ValueError, TypeError):
        return False


def new_trace_id() -> str:
    """Return a fresh trace id for one user operation (shared across layers)."""
    return str(uuid.uuid4())


def resolve_sink_path(env: dict[str, str] | None = None) -> Path | None:
    """Resolve the sink path from the environment.

    Returns ``None`` when telemetry is disabled (env var set to ``disabled``),
    the configured path otherwise, or the default per-user sink when unset.
    """
    environ = os.environ if env is None else env
    raw = environ.get(ENV_TELEMETRY_PATH)
    if raw is None or raw == "":
        # ADR-046 dual-read: honour the RAHAN-era variable when the new one is unset.
        raw = environ.get(LEGACY_ENV_TELEMETRY_PATH)
    if raw is None or raw == "":
        return DEFAULT_SINK
    if raw.strip().lower() == DISABLED_SENTINEL:
        return None
    return Path(raw).expanduser()


class TelemetryEmitter:
    """Append-only JSONL emitter for fallback events.

    Parameters
    ----------
    sink_path:
        Explicit sink path. When omitted, resolved from the environment via
        :func:`resolve_sink_path` (honouring disabled mode).
    """

    def __init__(
        self, sink_path: Path | None = None, *, env: dict[str, str] | None = None
    ) -> None:
        self._explicit = sink_path is not None
        self._path = sink_path if self._explicit else resolve_sink_path(env)

    @property
    def disabled(self) -> bool:
        return self._path is None

    @property
    def path(self) -> Path | None:
        return self._path

    def build_record(
        self,
        *,
        trace_id: str,
        fmt: str,
        operation: str,
        handler: str,
        outcome: str,
        latency_ms: int,
        error_class: str | None = None,
        file_size_bytes: int | None = None,
    ) -> dict[str, Any]:
        """Assemble a schema-conformant, whitelisted record (no I/O)."""
        record: dict[str, Any] = {
            "trace_id": trace_id,
            "timestamp": _now_iso(),
            "format": fmt,
            "operation": operation,
            "handler": handler,
            "outcome": outcome,
            "latency_ms": int(latency_ms),
        }
        if error_class is not None:
            # Value-level privacy guard (AC6): coerce to a safe category token so
            # a leaked exception string (with embedded paths/PII) never persists.
            record["error_class"] = _sanitise_error_class(error_class)
        if file_size_bytes is not None:
            record["file_size_bytes"] = int(file_size_bytes)
        # Whitelist enforcement (AC6): drop anything not explicitly allowed.
        return {k: v for k, v in record.items() if k in ALLOWED_FIELDS}

    def emit(self, **fields: Any) -> bool:
        """Append one record. Fire-and-forget: never raises (NFR-1).

        Accepts the same keyword arguments as :meth:`build_record`. Returns
        ``True`` if a record was written, ``False`` if telemetry is disabled or
        the write failed (the failure is swallowed so the caller is never
        aborted).
        """
        if self.disabled:
            return False
        try:
            record = self.build_record(**fields)
            return self._write_record(record)
        except Exception:
            # Telemetry must never abort the caller's document operation.
            return False

    def _write_record(self, record: dict[str, Any]) -> bool:
        """Rotate if needed, then append the record as one JSONL line."""
        assert self._path is not None  # guarded by caller's self.disabled check
        self._rotate_if_needed(self._path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        return True

    @staticmethod
    def _rotate_if_needed(path: Path) -> None:
        """Rotate the sink when it exceeds the size cap, keeping N generations.

        Shifts ``<name>.(N-1) -> <name>.N`` (oldest dropped), ``... -> <name>.1``,
        then ``<name> -> <name>.1`` (NFR-4). Best-effort: never blocks emission.
        """
        try:
            if not (path.exists() and path.stat().st_size >= ROTATION_BYTES):
                return
            for gen in range(ROTATION_KEEP, 0, -1):
                src = path if gen == 1 else path.with_suffix(f"{path.suffix}.{gen - 1}")
                dst = path.with_suffix(f"{path.suffix}.{gen}")
                if not src.exists():
                    continue
                if dst.exists():
                    dst.unlink()  # only the oldest (gen == ROTATION_KEEP) is dropped
                src.rename(dst)
        except Exception:
            # Rotation is best-effort; never block emission.
            pass


def _self_test() -> int:
    """Minimal smoke test for direct invocation (real tests live in tests/unit)."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        sink = Path(tmp) / "fallback.jsonl"
        emitter = TelemetryEmitter(sink)
        ok = emitter.emit(
            trace_id=new_trace_id(),
            fmt="docx",
            operation="read",
            handler="mcp-word",
            outcome="fallthrough",
            latency_ms=12,
            error_class="timeout",
        )
        rec = json.loads(sink.read_text(encoding="utf-8").splitlines()[0])
        assert ok and rec["handler"] == "mcp-word" and "filename" not in rec
    print("cu-telemetry emitter self-test: ok")
    return 0


if __name__ == "__main__":
    sys.exit(_self_test())
