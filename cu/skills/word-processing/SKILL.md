---
name: word-processing
depends_on:
- cu-cascade-handler
description: Word document processing skill providing read, write, and generate operations for .docx and legacy .doc files through a cascading fallback strategy. Declares format-specific handler chains consumed by cu-cascade-handler. Covers the word MCP server, python-docx library, and Pandoc CLI with full troubleshooting guidance.
version: 1.0.2
last_updated: '2026-07-11'
maintained_by: Lucas Challamel
---

# cu-word-processing: Word Document Processing

## Purpose

This skill provides resilient Word document processing for the COPPER framework. It handles read,
write, and generate operations for `.docx` and legacy `.doc` files through a cascading fallback
strategy defined by `cu:cascade-handler` (ADR-017).

**Dependency**: This skill requires `cu:cascade-handler` to be loaded first. The cascade protocol
(decision rules, low-yield detection, error surfacing) is defined there. This skill declares only
the format-specific handler inventory.

## Operations Overview

| Operation    | Available Layers | Primary Handler   | Fallback Chain             |
| ------------ | ---------------- | ----------------- | -------------------------- |
| **Read**     | 1, 2, 3, 4       | `word` MCP server | MCP → python-docx → Pandoc |
| **Write**    | 2, 3, 4          | `word` MCP server | MCP → python-docx → Pandoc |
| **Generate** | 2, 3, 4          | `word` MCP server | MCP → python-docx → Pandoc |

## Read Operation

### Handler Chain (AC2)

The read operation attempts handlers in this order:

#### Layer 1: Direct Text Read

**Applicability**: Skipped for `.docx` and `.doc` files (binary formats that agents cannot natively
parse).

**When used**: Only if the agent already has the Word file content in its context window through a
previous tool invocation (e.g., markitdown already converted it).

#### Layer 2: MCP `word` Server

**Handler**: `word` MCP server configured in `opencode.jsonc`

**Primary tools**:

- `word_get_document_text` : Extract all text content from a Word document
- `word_get_document_info` : Get document metadata (title, author, page count)
- `word_get_document_outline` : Get document structure (headings hierarchy)
- `word_get_paragraph_text_from_document` : Extract text from a specific paragraph
- `word_read_data_from_excel` : Read tables embedded in the document (if any)

**Expected output**: Full document text as a string, including headings, paragraphs, lists, and
table content.

**Fall-through triggers**:

- MCP server timeout (>30 seconds)
- MCP server unreachable (connection error)
- Schema mismatch (unexpected response structure)
- Low-yield result (<50 characters after whitespace stripping)

#### Layer 3: `python-docx` Library

**Handler**: `python-docx` Python library

**What it does**: Parses the `.docx` file (which is a ZIP archive containing XML) and extracts:

- Paragraphs with their styles (heading levels, normal text, lists)
- Tables with cell content
- Document metadata (title, author, core properties)

**Limitations**:

- Does NOT extract images, charts, or embedded objects
- Does NOT extract headers, footers, or page numbers
- Does NOT handle tracked changes or comments
- Does NOT support legacy `.doc` format (use Pandoc for `.doc`)

**Fall-through triggers**:

- `ImportError` (python-docx not installed)
- File corruption (cannot parse XML structure)
- `PermissionError` (file locked or read-only)
- Low-yield result (<50 characters)

#### Layer 4: Pandoc CLI

**Handler**: `pandoc` command-line tool

**Command**: `pandoc input.docx -t markdown`

**What it does**: Converts the Word document to Markdown format. Handles:

- Headings, paragraphs, lists (ordered and unordered)
- Tables (converted to Markdown pipe tables)
- Basic formatting (bold, italic, links)
- Metadata (title block)

**Advantages**:

- Broadest format coverage including edge cases
- Handles some complex structures that python-docx misses
- Works with both `.docx` and legacy `.doc` files

**Fall-through triggers**:

- Pandoc not installed on the system
- Non-zero exit code
- Empty output file

### Normalised Markdown Output (AC5)

The read operation returns a normalised Markdown representation regardless of which layer produced
it. The output structure:

```markdown
# Document Title (if detected)

## Heading 1

Paragraph content...

- List item 1
- List item 2

## Heading 2

| Column A | Column B | Column C |
| -------- | -------- | -------- |
| Cell 1   | Cell 2   | Cell 3   |

### Heading 3

More paragraph content...
```

**Known limitations of the normalised output**:

- Images are represented as `![alt text](path)` or omitted entirely
- Headers and footers are not included
- Tracked changes are not represented
- Complex tables (merged cells, nested tables) may lose structure
- Footnotes and endnotes may be incomplete
- Columns, text boxes, and shapes are not supported

## Write Operation

### Handler Chain (AC3)

The write operation modifies an existing `.docx` file. Handlers are attempted in this order:

#### Layer 2: MCP `word` Server

**Primary tools**:

- `word_search_and_replace` : Find and replace text
- `word_add_paragraph` : Add a new paragraph
- `word_add_heading` : Add a heading
- `word_add_table` : Add a table
- `word_add_page_break` : Insert a page break
- `word_format_text` : Format text within a paragraph
- `word_format_table` : Format a table with borders and shading

**Advantages**: Rich formatting support, preserves existing document structure, handles complex
layouts.

**Fall-through triggers**: Same as read operation.

#### Layer 3: `python-docx` Library

**What it does**: Creates or modifies `.docx` files programmatically:

- Add/modify paragraphs with styles
- Create and populate tables
- Set document properties
- Add headings with specific levels
- Apply basic text formatting (bold, italic, font, size, colour)

**Limitations**:

- Cannot modify existing complex layouts without risking structure loss
- Limited header/footer manipulation
- No support for modifying existing charts or images

**Fall-through triggers**: Same as read operation.

#### Layer 4: Pandoc CLI

**Command**: `pandoc input.md -o output.docx`

**What it does**: Converts Markdown input to a Word document.

**Advantages**: Simple Markdown-to-docx conversion. Good for generating clean documents from
structured text.

**Limitations**:

- Cannot modify existing `.docx` files (creates new files only)
- Limited formatting control compared to MCP/python-docx
- No template application support

**Fall-through triggers**: Same as read operation.

### Write Input Format (AC6)

The write operation accepts structured data in two formats:

**JSON input**:

```json
{
  "title": "Document Title",
  "sections": [
    {
      "heading": "Introduction",
      "level": 1,
      "content": "Paragraph text here."
    },
    {
      "heading": "Key Findings",
      "level": 2,
      "content": "Detailed findings...",
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

**Markdown input**: Standard Markdown with headings, paragraphs, lists, and tables.

The resulting `.docx` file must open without error in both Microsoft Word and LibreOffice.

## Generate Operation

### Handler Chain

Same as write operation (Layers 2, 3, 4). The generate operation creates a new `.docx` file from
structured input rather than modifying an existing one.

**Typical workflow**:

1. Agent receives structured data (JSON or Markdown)
2. Layer 2: Use `word_create_document` followed by `word_add_heading`, `word_add_paragraph`,
   `word_add_table` to build the document
3. Fall back to Layer 3: Use `python-docx` to create and populate a new document
4. Fall back to Layer 4: Use Pandoc to convert Markdown to `.docx`

## Legacy .doc Coverage (AC7)

### Read-Only Support

Legacy `.doc` files (pre-Office 2007 binary format) are supported for **read operations only**.

**Handler routing**:

- **Layer 1**: Not applicable (binary format)
- **Layer 2**: MCP `word` server may support `.doc` if the underlying system has appropriate
  converters
- **Layer 3**: `python-docx` does NOT support `.doc` format. This layer is skipped for `.doc` files
  with a clear note in telemetry (`handler_class: python-docx`, `status: skipped`,
  `error_class: unsupported_format`)
- **Layer 4**: Pandoc CAN read `.doc` files if the system has `libreoffice` or `wvWare` installed.
  This is the primary fallback for legacy `.doc`

**Important**: Write and generate operations are NOT supported for `.doc` format. If a write
operation targets a `.doc` file, the agent should:

1. Reject the operation with a clear error message
2. Suggest converting to `.docx` first
3. If the caller insists, attempt Layer 4 (Pandoc) which may handle some conversions

## Telemetry Emission (AC4)

Every layer attempt emits exactly one fallback-telemetry record to the **canonical `cu:telemetry`
sink** (US-166), via `kits/core/skills/telemetry/scripts/telemetry_emitter.py`. All records for one
user operation share a `trace_id`. The persisted record conforms to the canonical schema
(`cu:telemetry`: `resources/fallback-event.schema.json`), NOT the cascade handler's richer internal
view , in particular it carries **no `filename` or content** (privacy invariant, AC6).

**Format-specific fields**:

| Field     | Value for this skill                                       |
| --------- | ---------------------------------------------------------- |
| `format`  | `docx` (legacy `.doc` reads are also recorded with `docx`) |
| `handler` | `llm-native`, `mcp-word`, `py-python-docx`, `pandoc`       |

**Emit step**: at each attempted layer, call the emitter with the canonical fields:

```python
from telemetry_emitter import TelemetryEmitter, new_trace_id

emitter = TelemetryEmitter()
trace_id = new_trace_id()  # once per user operation

# Layer 2 (MCP word) under-yields and falls through:
emitter.emit(trace_id=trace_id, fmt="docx", operation="read",
             handler="mcp-word", outcome="fallthrough", latency_ms=1200,
             error_class="low_yield")
# Layer 3 (python-docx) succeeds:
emitter.emit(trace_id=trace_id, fmt="docx", operation="read",
             handler="py-python-docx", outcome="success", latency_ms=320,
             file_size_bytes=20480)
```

**Example persisted records** (note: no `filename`, no extracted text):

```json
[
  {
    "trace_id": "8f1c9e2a-...-d4",
    "timestamp": "2026-06-13T10:30:01+00:00",
    "format": "docx",
    "operation": "read",
    "handler": "mcp-word",
    "outcome": "fallthrough",
    "latency_ms": 1200,
    "error_class": "low_yield"
  },
  {
    "trace_id": "8f1c9e2a-...-d4",
    "timestamp": "2026-06-13T10:30:02+00:00",
    "format": "docx",
    "operation": "read",
    "handler": "py-python-docx",
    "outcome": "success",
    "latency_ms": 320,
    "file_size_bytes": 20480
  }
]
```

The cascade decision and error-surfacing rules are inherited from `cu:cascade-handler`. This skill
does not re-implement them.

**Definition of Done (telemetry)**: this skill emits one `cu:telemetry` record per attempted cascade
layer, with no user content in the payload (AC6), and is covered by a test or documented manual
check that a record is written on fall-through.

## MCP Word Server Troubleshooting (AC8)

### Common Failure Modes

#### 1. Server Not Running

**Symptom**: `Connection refused` or `ECONNREFUSED` errors.

**Cause**: The MCP word server process is not running or crashed.

**Resolution**:

1. Check if the server process is running: `ps aux | grep word`
2. Restart the server through the OpenCode MCP management interface
3. If persistent, check `opencode.jsonc` for correct server configuration
4. Verify the server binary path is correct and the binary exists

#### 2. Server Timeout

**Symptom**: Requests take longer than 30 seconds with no response.

**Cause**: Large or complex documents, server resource exhaustion, or deadlocks.

**Resolution**:

1. Retry the operation once (may be transient)
2. If persistent, fall back to Layer 3 (python-docx) or Layer 4 (Pandoc)
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

**Cause**: File is locked by another application (Word, LibreOffice) or has read-only permissions.

**Resolution**:

1. Close the file in any open application
2. Check file permissions: `ls -la filename.docx`
3. If on a network share, verify mount and access rights
4. For locked files on macOS: `lsof | grep filename.docx`

#### 5. Corrupt File

**Symptom**: `Cannot open file` or `Invalid format` errors.

**Cause**: File corruption, incomplete download, or wrong file extension.

**Resolution**:

1. Verify the file is actually a `.docx` file: `file filename.docx`
2. Try opening in LibreOffice as a recovery attempt
3. If the file is a `.doc` with `.docx` extension, rename and retry with legacy handling

### Escalation Path

1. **First**: Fall back to Layer 3 or Layer 4 automatically
2. **Second**: Check MCP server logs for error details
3. **Third**: Report persistent issues to framework maintainer with telemetry trace_id

## Known Limitations

| Limitation                        | Impact | Workaround                                                 |
| --------------------------------- | ------ | ---------------------------------------------------------- |
| Images not extracted in Layer 3   | Medium | Use Layer 2 (MCP) or Layer 4 (Pandoc) for image-heavy docs |
| Headers/footers not extracted     | Low    | Document this as expected behaviour                        |
| Tracked changes not represented   | Low    | Accept tracked changes before processing                   |
| Complex tables may lose structure | Medium | Use Layer 2 (MCP) for best table fidelity                  |
| Legacy .doc is read-only          | Medium | Convert to .docx first for write operations                |
| Footnotes/endnotes incomplete     | Low    | Use Layer 4 (Pandoc) for best footnote support             |
| Columns not supported             | Low    | Reformat document to single-column before processing       |

## Related Documentation

- **cu-cascade-handler**: Foundational cascade protocol skill (dependency)
- **ADR-017**: Cascading fallback for document processing (architectural decision)
- **ADR-009**: Skill architecture and loading model (MECE rule)
- **US-166**: Centralise fallback telemetry and MCP health observability (telemetry consumer)
- **US-160**: Excel spreadsheet processing skill (sister skill)
- **US-161**: PowerPoint processing skill (sister skill)
- **US-162**: PDF document processing skill (sister skill)
- **US-163**: Word template generation (downstream consumer)
- **US-164**: Reference export with Word and PDF (downstream consumer)
