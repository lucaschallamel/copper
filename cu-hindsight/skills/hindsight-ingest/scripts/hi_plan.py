"""What a run would send, redact and skip, decided locally before any network call (AC5,
AC8)."""

from __future__ import annotations

import os
from collections import Counter
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

import hi_detectors
import hi_gate
from hi_state import State, digest
from hi_walk import doc_id

SOURCE = "hindsight-ingest"  # marks documents this tool sent (Q27), whatever the folder
RULES_VERSION = 2  # bump when hi_detectors or hi_gate change what is sent


def rules_fingerprint(cfg, gitleaks: str) -> str:
    """What decides outgoing text besides the note: detectors, limits, rules, and the
    gitleaks version, so an upgrade re-scans every sent note once (BUG-018 AC5)."""
    basis = f"{RULES_VERSION}|{sorted(cfg.detectors)}|{cfg.max_chars}|{gitleaks}"
    return digest(basis)[:16]


@dataclass
class Note:
    note: str
    path: Path
    text: str
    mtime: float
    sha256: str
    rules: str = ""


@dataclass
class Plan:
    send: list[Note] = field(default_factory=list)
    secret: list[tuple[str, str]] = field(default_factory=list)
    other: list[tuple[str, str]] = field(default_factory=list)
    redacted: list[tuple[str, str]] = field(default_factory=list)
    unchanged: int = 0
    rules: str = ""


def outgoing(path: Path, cfg) -> tuple[str | None, str, dict]:
    """(redacted text or None, skip reason, redaction counts) for one note."""
    return screen(_read(path), cfg)


def _read(path: Path) -> bytes | OSError:
    try:
        return path.read_bytes()
    except OSError as exc:
        return exc


def screen(raw: bytes | OSError, cfg) -> tuple[str | None, str, dict]:
    """`outgoing` for bytes already read: the text gitleaks scanned is the text sent."""
    if isinstance(raw, OSError):
        return None, f"unreadable:{type(raw).__name__}", {}
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, "unreadable:UnicodeDecodeError", {}
    if not text.strip():
        return None, "empty", {}
    if len(text) > cfg.max_chars:
        return None, f"too-large:{len(text)}", {}
    text, counts = hi_detectors.redact(text, cfg.detectors)
    reason = hi_gate.secret_reason(text)
    return (None, f"secret:{reason}", counts) if reason else (text, "", counts)


def _stat(path: Path) -> os.stat_result | None:
    try:
        return path.stat()
    except OSError:
        return None


def plan_files(
    vault: Path,
    cfg,
    state: State,
    files: list[Path],
    flagged=hi_gate.gitleaks_flagged,
    version=hi_gate.gitleaks_identity,
) -> Plan:
    """Decide every note's fate; the mtime fast path holds only under the same rules.

    Each candidate is read once, after its mtime (BUG-018 AC1): gitleaks scans those
    bytes and the same bytes are sent, so a save during the run cannot slip through,
    and a save after the stat leaves a newer mtime for the next run to pick up."""
    plan = Plan(rules=rules_fingerprint(cfg, version()))
    ids = [doc_id(vault, path) for path in files]
    twins = {n for n, count in Counter(ids).items() if count > 1}
    candidates = []
    for note, path in zip(ids, files, strict=True):
        entry, st = state.get(note), _stat(path)
        if note in twins:  # two spellings of one id: gitleaks could judge only one
            plan.other.append((note, "duplicate-id"))
        elif st is None:
            plan.other.append((note, "unreadable:gone"))
        elif entry.get("mtime") == st.st_mtime and entry.get("rules") == plan.rules:
            plan.unchanged += 1
        elif st.st_size > 4 * cfg.max_chars:  # over max_chars in any UTF-8: not read
            plan.other.append((note, f"too-large:{st.st_size}"))
        else:
            candidates.append((note, path, st.st_mtime, _read(path)))
    leaks = flagged({n: raw for n, _, _, raw in candidates if isinstance(raw, bytes)})
    for note, path, mtime, raw in candidates:
        _classify(plan, cfg, state, note, path, mtime, raw, leaks)
    return plan


def _classify(
    plan: Plan, cfg, state: State, note: str, path: Path, mtime, raw, leaks: dict
) -> None:
    if note in leaks:
        plan.secret.append((note, "gitleaks:" + ",".join(sorted(leaks[note]))))
        return
    text, reason, counts = screen(raw, cfg)
    if text is None:
        (plan.secret if reason.startswith("secret:") else plan.other).append(
            (note, reason)
        )
        return
    sha = digest(text)
    if state.get(note).get("sha256") == sha:
        state.record(note, mtime, sha, plan.rules)  # touched, same outgoing text
        plan.unchanged += 1
        return
    if counts:
        plan.redacted.append(
            (note, ", ".join(f"{n} {k}" for k, n in sorted(counts.items())))
        )
    plan.send.append(Note(note, path, text, mtime, sha, plan.rules))


def tags_for(note: str, cfg) -> list[str]:
    parts = note.split("/")
    folder = parts[0] if len(parts) > 1 else "_root"
    return [f"folder:{folder}", "type:markdown", *cfg.tags]


def item(n: Note, cfg, chunk: str) -> dict:
    return {
        "content": n.text,
        "context": f"File: {n.note}",
        "document_id": n.note,
        "timestamp": datetime.fromtimestamp(n.mtime, UTC).isoformat(),
        "metadata": {"source": SOURCE, "path": n.note, "chunk": chunk},
        "tags": tags_for(n.note, cfg),
    }
