---
name: powerpoint-processing
depends_on:
- cu-cascade-handler
description: PowerPoint document processing skill providing read, write, and generate operations for .pptx files through a cascading fallback strategy. Declares format-specific handler chains consumed by cu-cascade-handler. Covers the powerpoint MCP server, python-pptx library, and Pandoc CLI with full troubleshooting guidance.
version: 1.0.2
last_updated: '2026-07-11'
maintained_by: Lucas Challamel
---

# cu-powerpoint-processing: PowerPoint Document Processing

## Purpose

This skill provides resilient PowerPoint document processing for the COPPER framework. It handles
read, write, and generate operations for `.pptx` files through a cascading fallback strategy defined
by `cu:cascade-handler` (ADR-017).

**Dependency**: This skill requires `cu:cascade-handler` to be loaded first. The cascade protocol
(decision rules, low-yield detection, error surfacing) is defined there. This skill declares only
the format-specific handler inventory.

## Operations Overview

| Operation    | Available Layers | Primary Handler         | Fallback Chain             |
| ------------ | ---------------- | ----------------------- | -------------------------- |
| **Read**     | 1, 2, 3, 4       | `powerpoint` MCP server | MCP → python-pptx → Pandoc |
| **Write**    | 2, 3             | `powerpoint` MCP server | MCP → python-pptx          |
| **Generate** | 2, 3             | `powerpoint` MCP server | MCP → python-pptx          |

## Read Operation

### Handler Chain (AC2)

The read operation attempts handlers in this order:

#### Layer 1: Direct Text Read

**Applicability**: Skipped for `.pptx` files (binary format that agents cannot natively parse).

**When used**: Only if the agent already has the PowerPoint file content in its context window
through a previous tool invocation (e.g., markitdown already converted it).

#### Layer 2: MCP `powerpoint` Server

**Handler**: `powerpoint` MCP server configured in `opencode.jsonc`

**Primary tools**:

- `powerpoint_extract_presentation_text` : Extract all text content from all slides
- `powerpoint_get_presentation_info` : Get presentation metadata (slide count, dimensions)
- `powerpoint_get_slide_info` : Get information about a specific slide
- `powerpoint_extract_slide_text` : Extract text from a specific slide
- `powerpoint_list_presentations` : List currently loaded presentations

**Expected output**: Full presentation text as a structured string, including slide numbers, titles,
bullet points, speaker notes, and table content.

**Fall-through triggers**:

- MCP server timeout (>30 seconds)
- MCP server unreachable (connection error)
- Schema mismatch (unexpected response structure)
- Low-yield result (<50 characters after whitespace stripping)

#### Layer 3: `python-pptx` Library

**Handler**: `python-pptx` Python library

**What it does**: Parses the `.pptx` file (which is a ZIP archive containing XML) and extracts:

- Slide text (titles, body text, bullet points)
- Tables with cell content
- Slide metadata (layout, slide number)
- Speaker notes
- Presentation metadata (author, title, dimensions)

**Limitations**:

- Does NOT extract images, charts, or embedded objects as text
- Does NOT extract slide master or layout details
- Does NOT handle animations, transitions, or media
- Grouped shapes may yield incomplete text

**Fall-through triggers**:

- `ImportError` (python-pptx not installed)
- File corruption (cannot parse XML structure)
- `PermissionError` (file locked or read-only)
- Low-yield result (<50 characters)

#### Layer 4: Pandoc CLI

**Handler**: `pandoc` command-line tool

**Command**: `pandoc input.pptx -t markdown`

**What it does**: Converts the PowerPoint presentation to Markdown format. Handles:

- Slide titles (converted to headings)
- Body text and bullet points
- Tables (converted to Markdown pipe tables)
- Basic formatting (bold, italic, links)

**Advantages**:

- Broadest text extraction coverage for edge cases
- Handles some complex slide structures
- No additional Python dependencies required

**Limitations**:

- **Write and generate NOT supported** for `.pptx` via Pandoc
- Speaker notes may be incomplete
- Slide layout information is lost
- Grouped shapes may not extract correctly

**Fall-through triggers**:

- Pandoc not installed on the system
- Non-zero exit code
- Empty output file

### Normalised Markdown Output (AC5)

The read operation returns a normalised Markdown representation regardless of which layer produced
it. The output structure:

```markdown
# Slide 1: Presentation Title

- Bullet point 1
- Bullet point 2

## Subtitle Content

Paragraph content...

# Slide 2: Key Findings

| Metric  | Value | Change |
| ------- | ----- | ------ |
| Revenue | $1.2M | +15%   |
| Costs   | $800K | -5%    |
```

**Known limitations of the normalised output**:

- Images are represented as `![alt text](path)` or omitted entirely
- Animations and transitions are not represented
- Slide master content is not included
- Complex tables (merged cells) may lose structure
- Speaker notes may be incomplete or omitted
- Charts and SmartArt are not converted to text

## Write Operation

### Handler Chain (AC3)

The write operation modifies an existing `.pptx` file. Handlers are attempted in this order:

#### Layer 2: MCP `powerpoint` Server

**Primary tools**:

- `powerpoint_add_slide` : Add a new slide
- `powerpoint_add_bullet_points` : Add bullet points to a placeholder
- `powerpoint_populate_placeholder` : Fill a placeholder with text
- `powerpoint_manage_text` : Add or format text on a slide
- `powerpoint_manage_image` : Add or manipulate images
- `powerpoint_add_table` : Add a table to a slide
- `powerpoint_add_chart` : Add a chart to a slide
- `powerpoint_format_table_cell` : Format a specific table cell

**Advantages**: Rich formatting support, preserves existing slide layouts, handles master templates
and complex layouts.

**Fall-through triggers**: Same as read operation.

#### Layer 3: `python-pptx` Library

**What it does**: Creates or modifies `.pptx` files programmatically:

- Add/modify slides with specific layouts
- Add text boxes, shapes, and images
- Create and populate tables and charts
- Set slide dimensions and properties
- Apply basic text formatting (bold, italic, font, size, colour)

**Limitations**:

- Cannot modify existing complex animations or transitions
- Limited support for embedded media (video, audio)
- Chart creation requires manual XML manipulation for advanced chart types

**Fall-through triggers**: Same as read operation.

**Layer 4**: Not applicable for write operations (Pandoc cannot write `.pptx`).

### Write Input Format (AC6)

The write operation accepts structured data in JSON format:

```json
{
  "slides": [
    {
      "layout_index": 1,
      "title": "Quarterly Results",
      "placeholders": {
        "1": "Q4 2025 Performance Summary",
        "2": "Revenue exceeded targets by 15%"
      }
    },
    {
      "layout_index": 6,
      "title": "Key Metrics",
      "table": {
        "headers": ["Metric", "Value", "Change"],
        "rows": [
          ["Revenue", "$1.2M", "+15%"],
          ["Costs", "$800K", "-5%"]
        ]
      }
    }
  ]
}
```

The resulting `.pptx` file must open without error in both Microsoft PowerPoint and LibreOffice
Impress.

## Generate Operation

### Handler Chain

Same as write operation (Layers 2, 3). The generate operation creates a new `.pptx` file from
structured input rather than modifying an existing one.

**Typical workflow**:

1. Agent receives structured data (JSON or Markdown outline)
2. Layer 2: Use `powerpoint_create_presentation` followed by `powerpoint_add_slide`,
   `powerpoint_add_bullet_points`, `powerpoint_add_table` to build the deck
3. Fall back to Layer 3: Use `python-pptx` to create and populate a new presentation
4. Layer 4: Not applicable (Pandoc cannot generate `.pptx`)

## Telemetry Emission (AC4)

Every layer attempt emits exactly one fallback-telemetry record to the **canonical `cu:telemetry`
sink** (US-166), via `kits/core/skills/telemetry/scripts/telemetry_emitter.py`. All records for one
user operation share a `trace_id`. The persisted record conforms to the canonical schema
(`cu:telemetry`: `resources/fallback-event.schema.json`), NOT the cascade handler's richer internal
view , in particular it carries **no `filename` or content** (privacy invariant, AC6).

**Format-specific fields**:

| Field     | Value for this skill                                       |
| --------- | ---------------------------------------------------------- |
| `format`  | `pptx`                                                     |
| `handler` | `llm-native`, `mcp-powerpoint`, `py-python-pptx`, `pandoc` |

**Emit step**: at each attempted layer, call the emitter with the canonical fields:

```python
from telemetry_emitter import TelemetryEmitter, new_trace_id

emitter = TelemetryEmitter()
trace_id = new_trace_id()  # once per user operation

# Layer 2 (MCP powerpoint) under-yields and falls through:
emitter.emit(trace_id=trace_id, fmt="pptx", operation="read",
             handler="mcp-powerpoint", outcome="fallthrough", latency_ms=1100,
             error_class="low_yield")
# Layer 3 (python-pptx) succeeds:
emitter.emit(trace_id=trace_id, fmt="pptx", operation="read",
             handler="py-python-pptx", outcome="success", latency_ms=410,
             file_size_bytes=51200)
```

For write and generate operations, Pandoc is not a valid handler: it cannot write or generate
`.pptx`. When the cascade reaches Layer 4 for those operations, record the fall-through explicitly:

```python
# Write/generate cascade exhausts MCP + python-pptx; Pandoc cannot produce .pptx:
emitter.emit(trace_id=trace_id, fmt="pptx", operation="generate",
             handler="pandoc", outcome="fallthrough", latency_ms=0,
             error_class="unsupported_operation")
```

**Example persisted records** (note: no `filename`, no extracted text):

```json
[
  {
    "trace_id": "8f1c9e2a-...-d4",
    "timestamp": "2026-06-13T10:30:01+00:00",
    "format": "pptx",
    "operation": "read",
    "handler": "mcp-powerpoint",
    "outcome": "fallthrough",
    "latency_ms": 1100,
    "error_class": "low_yield"
  },
  {
    "trace_id": "8f1c9e2a-...-d4",
    "timestamp": "2026-06-13T10:30:02+00:00",
    "format": "pptx",
    "operation": "read",
    "handler": "py-python-pptx",
    "outcome": "success",
    "latency_ms": 410,
    "file_size_bytes": 51200
  }
]
```

The cascade decision and error-surfacing rules are inherited from `cu:cascade-handler`. This skill
does not re-implement them.

**Definition of Done (telemetry)**: this skill emits one `cu:telemetry` record per attempted cascade
layer, with no user content in the payload (AC6), and is covered by a test or documented manual
check that a record is written on fall-through.

## MCP PowerPoint Server Troubleshooting (AC8)

### Common Failure Modes

#### 1. Server Not Running

**Symptom**: `Connection refused` or `ECONNREFUSED` errors.

**Cause**: The MCP powerpoint server process is not running or crashed.

**Resolution**:

1. Check if the server process is running: `ps aux | grep powerpoint`
2. Restart the server through the OpenCode MCP management interface
3. If persistent, check `opencode.jsonc` for correct server configuration
4. Verify the server binary path is correct and the binary exists

#### 2. Server Timeout

**Symptom**: Requests take longer than 30 seconds with no response.

**Cause**: Large or complex presentations, server resource exhaustion, or deadlocks.

**Resolution**:

1. Retry the operation once (may be transient)
2. If persistent, fall back to Layer 3 (python-pptx) or Layer 4 (Pandoc, read only)
3. Report to framework maintainer if timeouts are consistent

#### 3. Schema Mismatch

**Symptom**: Response structure does not match expected format (missing fields, wrong types).

**Cause**: MCP server version mismatch or upstream API change.

**Resolution**:

1. Check the MCP server version against expected version
2. Update the MCP server if a newer version is available
3. Fall back to Layer 3 or 4

#### 4. File Permission Error

**Symptom**: `Permission denied` or `Access denied` errors.

**Cause**: File is locked by another application (PowerPoint, Keynote, LibreOffice) or has read-only
permissions.

**Resolution**:

1. Close the file in any open application
2. Check file permissions: `ls -la filename.pptx`
3. If on a network share, verify mount and access rights
4. For locked files on macOS: `lsof | grep filename.pptx`

#### 5. Corrupt File

**Symptom**: `Cannot open file` or `Invalid format` errors.

**Cause**: File corruption, incomplete download, or wrong file extension.

**Resolution**:

1. Verify the file is actually a `.pptx` file: `file filename.pptx`
2. Try opening in LibreOffice Impress as a recovery attempt
3. If the file is a `.ppt` (legacy) with `.pptx` extension, rename and retry

### Escalation Path

1. **First**: Fall back to Layer 3 or Layer 4 automatically
2. **Second**: Check MCP server logs for error details
3. **Third**: Report persistent issues to framework maintainer with telemetry trace_id

## Known Limitations

| Limitation                             | Impact | Workaround                                        |
| -------------------------------------- | ------ | ------------------------------------------------- |
| Images not extracted as text           | Medium | Use Layer 2 (MCP) for image metadata              |
| Animations/transitions not represented | Low    | Accept as expected behaviour for text extraction  |
| Charts not converted to text           | Medium | Use Layer 2 (MCP) chart tools for data extraction |
| Speaker notes may be incomplete        | Low    | Use Layer 3 (python-pptx) for best notes support  |
| Pandoc write/generate not supported    | Medium | Use Layer 2 or 3 for all write operations         |
| Grouped shapes yield incomplete text   | Low    | Ungroup shapes before processing if possible      |
| SmartArt not converted to text         | Low    | Accept as expected behaviour                      |
| Legacy .ppt not supported              | Medium | Convert to .pptx first using LibreOffice          |

## Related Documentation

- **cu-cascade-handler**: Foundational cascade protocol skill (dependency)
- **ADR-017**: Cascading fallback for document processing (architectural decision)
- **ADR-009**: Skill architecture and loading model (MECE rule)
- **US-166**: Centralise fallback telemetry and MCP health observability (telemetry consumer)
- **US-159**: Word processing skill (sister skill)
- **US-160**: Excel spreadsheet processing skill (sister skill)
- **US-162**: PDF document processing skill (sister skill)
