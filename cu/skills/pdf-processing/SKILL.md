---
name: pdf-processing
depends_on:
- cu-cascade-handler
description: PDF document processing skill providing read and generate operations for .pdf files through a cascading fallback strategy. Declares format-specific handler chains consumed by cu-cascade-handler. Covers the pdf-tools and markitdown MCP servers, pypdf library, Pandoc CLI, and optional weasyprint fallback with full troubleshooting guidance.
version: 1.1.0
last_updated: '2026-06-13'
maintained_by: Lucas Challamel
---

# cu-pdf-processing: PDF Document Processing

## Purpose

This skill provides resilient PDF document processing for the COPPER framework. It handles read and
generate operations for `.pdf` files through a cascading fallback strategy defined by
`cu:cascade-handler` (ADR-017).

**Dependency**: This skill requires `cu:cascade-handler` to be loaded first. The cascade protocol
(decision rules, low-yield detection, error surfacing) is defined there. This skill declares only
the format-specific handler inventory.

## Operations Overview

| Operation    | Available Layers | Primary Handler        | Fallback Chain                    |
| ------------ | ---------------- | ---------------------- | --------------------------------- |
| **Read**     | 2, 3, 4          | `pdf-tools` MCP server | markitdown MCP → pypdf → Pandoc   |
| **Generate** | 4                | Pandoc CLI             | weasyprint (HTML-to-PDF fallback) |

> **Note**: Layer 1 (Direct Text Read) is skipped for PDF files because they are binary formats that
> agents cannot natively parse. There is no Write operation because PDFs are not edited in-place;
> use Read to extract content and Generate to create new PDFs.

## Read Operation

### Handler Chain (AC2)

The read operation attempts handlers in this order:

#### Layer 1: Direct Text Read

**Applicability**: Skipped for `.pdf` files (binary format that agents cannot natively parse).

**When used**: Only if the agent already has the PDF content in its context window through a
previous tool invocation (e.g., markitdown already converted it).

#### Layer 2: MCP `pdf-tools` / `markitdown` Server

**Handlers**: `pdf-tools` or `markitdown` MCP servers configured in `opencode.jsonc`

**Primary tools**:

- `pdf-tools_read_pdf_content` : Extract text content from a PDF file
- `pdf-tools_read_pdf_pages` : Read specific page ranges with structured output
- `pdf-tools_search_pdf_text` : Search for text within a PDF
- `markitdown_convert_to_markdown` : Universal document conversion including PDF

**Expected output**: Full document text as a string, including headings, paragraphs, lists, and
table content where extractable.

**Fall-through triggers**:

- MCP server timeout (>30 seconds)
- MCP server unreachable (connection error)
- Schema mismatch (unexpected response structure)
- Low-yield result (<50 characters after whitespace stripping)

#### Layer 3: `pypdf` Library

**Handler**: `pypdf` Python library

**What it does**: Parses the `.pdf` file and extracts:

- Text content from each page
- Document metadata (title, author, page count)
- Basic structural information (page boundaries)

**Limitations**:

- Does NOT extract images, charts, or embedded objects as text
- Does NOT handle scanned/image-based PDFs (returns empty or low-yield)
- Does NOT preserve formatting, columns, or layout information
- Does NOT extract form field data or annotations

**Fall-through triggers**:

- `ImportError` (pypdf not installed)
- File corruption (cannot parse PDF structure)
- `PermissionError` (file locked or read-only)
- Low-yield result (<50 characters)

#### Layer 4: Pandoc CLI

**Handler**: `pandoc` command-line tool

**Command**: `pandoc input.pdf -t markdown`

**What it does**: Converts the PDF document to Markdown format. Handles:

- Headings, paragraphs, lists (ordered and unordered)
- Tables (converted to Markdown pipe tables)
- Basic formatting (bold, italic, links)
- Metadata (title block)

**Advantages**:

- Broadest format coverage for text-based PDFs
- Handles some complex structures that pypdf misses
- Reliable for well-structured PDF documents

**Fall-through triggers**:

- Pandoc not installed on the system
- Non-zero exit code
- Empty output file

### Normalised Markdown Output (AC5)

The read operation returns a normalised Markdown representation regardless of which layer produced
it. The output structure:

```markdown
# Document Title (if detected)

## Section Heading

Paragraph content extracted from the PDF...

- List item 1
- List item 2

## Another Section

| Column A | Column B | Column C |
| -------- | -------- | -------- |
| Cell 1   | Cell 2   | Cell 3   |
```

**Known limitations of the normalised output**:

- Images are represented as `![alt text](path)` or omitted entirely
- Headers and footers are not consistently included
- Complex tables (merged cells, nested tables) may lose structure
- Multi-column layouts are flattened to single-column
- Annotations, form fields, and comments are not extracted
- Watermarks and background text may appear in the output

### Scanned PDF Handling (AC6)

For scanned or image-based PDFs, the cascade applies the **uniform low-yield rule** defined in
`cu:cascade-handler` (50-character threshold after whitespace stripping):

1. Layer 2 (MCP) attempts extraction → typically returns empty or minimal text
2. Layer 3 (pypdf) attempts extraction → returns empty or minimal text
3. Layer 4 (Pandoc) attempts extraction → returns empty or minimal text
4. All layers exhausted → return clear error with LLM vision recommendation

**Error message for scanned PDFs**:

```
PDF text extraction failed for [filename]. All cascade layers returned low-yield content
(extracted text fewer than 50 characters after whitespace stripping).

This PDF appears to be scanned or image-based. Recommended approaches:
- Use LLM vision/multimodal reading capabilities to process the scanned content
- Pre-process with OCR tools (e.g., Tesseract, Azure Form Recognizer)
- Request a digital/text-based version of the document

Note: Full OCR is out of scope for this skill.
```

## Generate Operation

### Handler Chain (AC3)

The generate operation creates a new PDF file from structured input. Unlike Word/Excel/PowerPoint,
PDF generation starts at Layer 4 because Layers 1-3 do not support PDF creation.

#### Layer 4 (Primary): Pandoc CLI

**Command**: `pandoc input.md -o output.pdf --pdf-engine=xelatex`

**What it does**: Converts Markdown input to a PDF document via LaTeX. Handles:

- Headings with hierarchy (H1-H6)
- Paragraphs, lists, tables
- Code blocks with syntax highlighting
- Math equations (LaTeX notation)
- Cross-references and links

**Requirements**:

- Pandoc must be installed
- A LaTeX engine must be installed (XeLaTeX recommended for Unicode/font support)
- Fonts specified in the template must be available on the system

**Fall-through triggers**:

- Pandoc not installed
- LaTeX engine not installed
- Non-zero exit code (compilation error)
- Empty output file

#### Fallback: `weasyprint` (HTML-to-PDF)

**Handler**: `weasyprint` Python library

**What it does**: Converts HTML (generated from Markdown) to PDF. This is a fallback when LaTeX is
not available on the system, which is common on corporate laptops.

**Process**:

1. Convert Markdown to HTML using Python `markdown` library or Pandoc (`pandoc input.md -t html`)
2. Apply CSS styling with brand colours and typography [TO BE CONFIGURED - the organisation's brand
   kit]
3. Convert HTML+CSS to PDF using weasyprint

**Advantages**:

- Does NOT require LaTeX installation
- CSS-based styling is familiar and flexible
- Good Unicode and font support
- Lighter dependency than full LaTeX

**Limitations**:

- Less precise page layout control than LaTeX
- Complex math equations not supported
- Page break control is less granular
- May produce slightly different output than Pandoc+LaTeX

**Fall-through triggers**:

- `ImportError` (weasyprint not installed)
- CSS rendering error
- Empty output file

### Brand Styling (AC7)

The generate operation applies brand styling [TO BE CONFIGURED - the organisation's brand kit] to
PDF output:

| Element          | Specification | Usage                    |
| ---------------- | ------------- | ------------------------ |
| **Primary Blue** | `#5480BA`     | Headings, section titles |
| **Green**        | `#8F9424`     | Secondary accents        |
| **Pink**         | `#E04580`     | Highlights, callouts     |
| **Purple**       | `#6B367D`     | Accent elements          |
| **Heading Font** | Arvo          | All headings (H1-H6)     |
| **Body Font**    | Inter         | Body text, paragraphs    |
| **Fallback**     | Arial         | System fallback          |

**CSS template for weasyprint**:

```css
@page {
  size: A4;
  margin: 2.5cm;
}

body {
  font-family: 'Inter', Arial, sans-serif;
  font-size: 11pt;
  line-height: 1.5;
  color: #333333;
}

h1,
h2,
h3,
h4,
h5,
h6 {
  font-family: 'Arvo', Arial, sans-serif;
  color: #5480ba;
}

h1 {
  font-size: 24pt;
  border-bottom: 2px solid #5480ba;
  padding-bottom: 8px;
}

h2 {
  font-size: 18pt;
  border-bottom: 1px solid #8f9424;
  padding-bottom: 4px;
}
```

**LaTeX template for Pandoc**:

```latex
\usepackage{fontspec}
\setmainfont{Inter}
\setkomafont{sectioning}{\color[HTML]{5480BA}\bfseries}
\setkomafont{section}{\Large}
```

Brand styling verification is performed via schema-level inspection (e.g., `pikepdf` colour
extraction from the generated PDF's colour streams), not by visual review.

### Generate Input Format

The generate operation accepts Markdown input:

```markdown
# Proposal: Digital Transformation

## Executive Summary

This document outlines the approach...

## Methodology

1. **Design Phase**: Stakeholder workshops
2. **Empower Phase**: Capability building
3. **Implement Phase**: Technology deployment
4. **Innovate Phase**: Continuous improvement
```

## Telemetry Emission (AC4)

Every layer attempt emits exactly one fallback-telemetry record to the **canonical `cu:telemetry`
sink** (US-166), via `kits/core/skills/telemetry/scripts/telemetry_emitter.py`. All records for one
user operation share a `trace_id`. The persisted record conforms to the canonical schema
(`cu:telemetry`: `resources/fallback-event.schema.json`), NOT the cascade handler's richer internal
view , in particular it carries **no `filename` or content** (privacy invariant, AC6).

**Format-specific fields**:

| Field     | Value for this skill                                                  |
| --------- | --------------------------------------------------------------------- |
| `format`  | `pdf`                                                                 |
| `handler` | `llm-native`, `mcp-pdf-tools`, `mcp-markitdown`, `py-pypdf`, `pandoc` |

**Scanned/image PDFs**: when the document is scanned or image-based, each text-extraction layer
typically under-yields and falls through (recorded as `outcome: fallthrough`,
`error_class: low_yield`) until all layers are exhausted, per the uniform low-yield rule in
`cu:cascade-handler`.

**Emit step**: at each attempted layer, call the emitter with the canonical fields:

```python
from telemetry_emitter import TelemetryEmitter, new_trace_id

emitter = TelemetryEmitter()
trace_id = new_trace_id()  # once per user operation

# Layer 2 (MCP pdf-tools) under-yields on a scanned PDF and falls through:
emitter.emit(trace_id=trace_id, fmt="pdf", operation="read",
             handler="mcp-pdf-tools", outcome="fallthrough", latency_ms=1400,
             error_class="low_yield")
# Layer 3 (pypdf) succeeds:
emitter.emit(trace_id=trace_id, fmt="pdf", operation="read",
             handler="py-pypdf", outcome="success", latency_ms=280,
             file_size_bytes=51200)
```

**Example persisted records** (note: no `filename`, no extracted text):

```json
[
  {
    "trace_id": "3b7d1f04-...-9c",
    "timestamp": "2026-06-13T10:30:01+00:00",
    "format": "pdf",
    "operation": "read",
    "handler": "mcp-pdf-tools",
    "outcome": "fallthrough",
    "latency_ms": 1400,
    "error_class": "low_yield"
  },
  {
    "trace_id": "3b7d1f04-...-9c",
    "timestamp": "2026-06-13T10:30:02+00:00",
    "format": "pdf",
    "operation": "read",
    "handler": "py-pypdf",
    "outcome": "success",
    "latency_ms": 280,
    "file_size_bytes": 51200
  }
]
```

The cascade decision and error-surfacing rules are inherited from `cu:cascade-handler`. This skill
does not re-implement them. Errors from individual layers are captured via telemetry but only
surfaced to the caller when ALL layers have failed.

**Definition of Done (telemetry)**: this skill emits one `cu:telemetry` record per attempted cascade
layer, with no user content in the payload (AC6), and is covered by a test or documented manual
check that a record is written on fall-through.

## Error Surfacing

Follows the standard error-surfacing rule from `cu:cascade-handler`. The final error message lists
each layer attempted:

```
PDF processing failed for [filename]. All cascade layers exhausted:
- Layer 1 (Direct text read): Not applicable (binary format)
- Layer 2 (MCP server / pdf-tools): TimeoutError - Server did not respond within 30s
- Layer 3 (Python library / pypdf): Low yield - Extracted 12 characters (<50 threshold)
- Layer 4 (Pandoc CLI): FileNotFoundError - pandoc not found on system
```

## Troubleshooting

### Common Issues

| Issue                              | Cause                          | Resolution                                                           |
| ---------------------------------- | ------------------------------ | -------------------------------------------------------------------- |
| Empty text from PDF                | Scanned/image-based PDF        | Use LLM vision/multimodal reading; request digital version           |
| Pandoc PDF generation fails        | LaTeX not installed            | Install XeLaTeX (`tlmgr install xelatex`) or use weasyprint fallback |
| Font errors in generated PDF       | Inter or Arvo not installed    | Install fonts or rely on Arial fallback                              |
| Low-yield from digital PDF         | Unusual encoding or protection | Try different layer; check if file is password-protected             |
| weasyprint ImportError             | Library not installed          | `pip install weasyprint`; requires system-level deps                 |
| Permission denied on read          | File locked by another process | Close the application using the file; retry                          |
| Chinese/special characters missing | Font lacks Unicode coverage    | Use XeLaTeX with Unicode font; ensure font installed                 |

### MCP Server Issues

| Symptom               | Cause                          | Resolution                                      |
| --------------------- | ------------------------------ | ----------------------------------------------- |
| `pdf-tools` timeout   | Large PDF file (>100 pages)    | Use `read_pdf_pages` with specific page ranges  |
| `markitdown` fails    | Corrupted or protected PDF     | Fall through to pypdf (Layer 3)                 |
| Both MCP servers fail | Network or configuration issue | Check `opencode.jsonc` MCP server configuration |

### Installation Requirements

| Component    | Install Command               | Required For              |
| ------------ | ----------------------------- | ------------------------- |
| `pypdf`      | `pip install pypdf`           | Layer 3 read              |
| `weasyprint` | `pip install weasyprint`      | Generate fallback         |
| Pandoc       | `brew install pandoc` (macOS) | Layer 4 read/generate     |
| XeLaTeX      | `tlmgr install xelatex`       | Pandoc PDF generate       |
| `pikepdf`    | `pip install pikepdf`         | Brand colour verification |
| Inter font   | Download from Google Fonts    | Generate output           |
| Arvo font    | Download from Google Fonts    | Generate output           |
