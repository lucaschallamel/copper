---
name: telemetry
description: Fallback telemetry and MCP health-observability skill. Owns the canonical fallback-event record contract for the document-processing cascade (cu-cascade-handler and the word/excel/powerpoint/ pdf-processing and CV-generation consumer skills). Defines the JSONL log sink, the record schema, the privacy invariant, rotation policy, and the summary/health CLIs that aggregate per-handler success and fall-through rates. Use when emitting fallback telemetry, querying handler reliability, or wiring a consumer skill to record cascade-layer attempts.
version: 1.0.1
last_updated: '2026-07-11'
maintained_by: Lucas Challamel
depends_on:
- cu-cascade-handler
---

# cu-telemetry , Fallback Telemetry & MCP Health Observability

This skill is the operational counterpart to `cu:cascade-handler` (US-167). The cascade defines
_how_ a document operation falls through its handler layers; this skill defines _how each attempt is
recorded_ so that MCP-server regressions are detected early, cascade-layer priorities are justified
with data, and graceful degradation is measurable rather than aspirational.

## Log Sink (AC1)

- **Default location**: `~/.copper/telemetry/fallback.jsonl` (newline-delimited JSON).
- **Override**: set `COPPER_TELEMETRY_PATH` to an absolute or `~`-relative path.
- **Disable**: set `COPPER_TELEMETRY_PATH=disabled` , emission becomes a no-op (zero records
  written).
- **Append-only** (NFR-3): records are appended; consumer commands read but never rewrite.
- **Rotation** (NFR-4): the sink rotates once it reaches 50 MB, retaining **3 generations**
  (`fallback.jsonl.1` … `.3`); only the oldest is dropped, so history is not lost on each rotation.

## Record Schema (AC2)

The canonical record is defined in `resources/fallback-event.schema.json` (JSON Schema Draft
2020-12). One record is emitted **per attempted handler** (success or fall-through), so a single
user operation can yield several records sharing one `trace_id` (AC3).

| Field             | Type    | Required | Notes                                                  |
| ----------------- | ------- | -------- | ------------------------------------------------------ |
| `trace_id`        | string  | yes      | UUID shared across all layer attempts of one operation |
| `timestamp`       | string  | yes      | ISO 8601, UTC                                          |
| `format`          | enum    | yes      | `docx`, `xlsx`, `pptx`, `pdf`, `md`                    |
| `operation`       | enum    | yes      | `read`, `write`, `generate`                            |
| `handler`         | string  | yes      | `llm-native`, `pandoc`, `mcp-<name>`, or `py-<lib>`    |
| `outcome`         | enum    | yes      | `success`, `fallthrough`, `error`                      |
| `latency_ms`      | integer | yes      | Wall-clock duration of the attempt                     |
| `error_class`     | string  | no       | snake_case category token only (see Privacy)           |
| `file_size_bytes` | integer | no       | The only size/identity signal permitted                |

> **`error_class` is a category token, not free text.** It is constrained to
> `^[a-z][a-z0-9_]{0,63}$` (e.g. `timeout`, `low_yield`, `unreachable`, `non_zero_exit`). The
> emitter coerces any non-conforming value (such as a raw exception string with an embedded path) to
> `unknown` before write, and the schema rejects free text at validation time. This is the
> value-level half of the AC6 privacy guard , a caller doing `error_class=str(exception)` cannot
> leak a path or PII.
>
> **`timestamp` is genuinely validated, not just annotated.** The schema marks `timestamp` as
> `format: date-time`; the skill provides a stdlib format-checker (`is_iso8601`, backed by
> `datetime.fromisoformat`) so a malformed timestamp is rejected at validation time , with **no
> extra dependency** (**[DM]**). The emitter is the sole producer and always writes ISO-8601 UTC.

### Relationship to the cu-cascade-handler contract

`cu:cascade-handler` SKILL.md documents a richer _internal_ emitter view (`handler_class`, `layer`,
`char_count`, `duration_ms`, an extended status enum). That view maps **down** to this record at
emit time. **Where the two conflict, this schema is authoritative.** In particular, the cascade
handler's documented `filename` field is **dropped** here , see Privacy.

## Privacy Invariant (AC6)

The telemetry payload **never** contains user content: no source-document filenames, no extracted
text. Only `file_size_bytes` is captured. This is enforced two ways:

1. The emitter whitelists fields , anything outside the allowed set is dropped before write.
2. The JSON Schema sets `additionalProperties: false`, so a record carrying `filename`, `content`,
   or extracted text cannot validate.

A unit test asserts no forbidden key (`filename`, `content`, `text`, ...) appears in any emitted
record.

### Privacy Classification (nDSG / GDPR)

- **Data class**: operational metrics only. By construction (AC6) the sink contains **no personal
  data and no user content** , no filenames, no document text, no candidate PII. The only
  size/identity signal is `file_size_bytes`. Under Swiss nDSG / EU-GDPR this stream is therefore
  **not personal data**, so data-subject obligations (access, erasure) do not attach to it.
- **Locality**: the default sink is a **per-user local file**
  (`~/.copper/telemetry/fallback.jsonl`), never a shared or networked store. No third-party
  processor is involved.
- **Opt-out**: set `COPPER_TELEMETRY_PATH=disabled` for a complete no-op (zero records written).
- **Retention**: size-based rotation at 50 MB keeping 3 generations (NFR-4); no time-based retention
  is required because the payload holds no personal data.

## Emitting Telemetry (consumers)

Consumer skills emit one record per cascade-layer attempt. In a code context:

```python
from telemetry_emitter import TelemetryEmitter, new_trace_id

emitter = TelemetryEmitter()          # resolves sink from env (honours disabled)
trace_id = new_trace_id()             # once per user operation

# ... attempt Layer 2 (MCP) ...
emitter.emit(
    trace_id=trace_id, fmt="docx", operation="read",
    handler="mcp-word", outcome="fallthrough", latency_ms=42,
    error_class="timeout",
)
# ... then Layer 3 (Python library) succeeds ...
emitter.emit(
    trace_id=trace_id, fmt="docx", operation="read",
    handler="py-python-docx", outcome="success", latency_ms=15,
    file_size_bytes=20480,
)
```

Emission is **fire-and-forget** (NFR-1): `emit` never raises into the caller. A write failure
returns `False` and is swallowed, so telemetry can never abort a document operation.

## Consumer CLIs

```bash
# Per-handler success/fall-through rates, mean latency, error distribution (AC4)
uv run python ${CLAUDE_PLUGIN_ROOT}/skills/telemetry/scripts/telemetry_cli.py summary --days 30

# Flag handlers over the fall-through threshold; exits non-zero when flagged (AC5, CI-usable)
uv run python ${CLAUDE_PLUGIN_ROOT}/skills/telemetry/scripts/telemetry_cli.py health --days 7 --threshold 0.25
```

`health` exits `1` when any handler is flagged and `0` otherwise, making it suitable as a CI gate.

## Resources

- `resources/fallback-event.schema.json` , canonical record schema (D4)
- `scripts/telemetry_emitter.py` , emitter utility (D2)
- `scripts/telemetry_cli.py` , `summary` and `health` commands (D3)

## Definition of Done for consumers

A consuming skill that performs cascade fallback emits one cu-telemetry record per attempted
handler, with no user content in the payload, and is exercised by at least one test or documented
manual check that a record is written on fall-through.
