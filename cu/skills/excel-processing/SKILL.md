---
name: excel-processing
depends_on:
- cu-cascade-handler
description: Excel spreadsheet processing skill providing read, write, and CSV output operations for .xlsx and legacy .xls files through a cascading fallback strategy. Declares format-specific handler chains consumed by cu-cascade-handler. Covers the excel MCP server, openpyxl library, and Pandoc CLI with full troubleshooting guidance.
version: 1.0.2
last_updated: '2026-07-11'
maintained_by: Lucas Challamel
---

# cu-excel-processing: Excel Spreadsheet Processing

## Purpose

This skill provides resilient Excel spreadsheet processing for the COPPER framework. It handles
read, write, and CSV output operations for `.xlsx` and legacy `.xls` files through a cascading
fallback strategy defined by `cu:cascade-handler` (ADR-017).

**Dependency**: This skill requires `cu:cascade-handler` to be loaded first. The cascade protocol
(decision rules, low-yield detection, error surfacing) is defined there. This skill declares only
the format-specific handler inventory.

## Operations Overview

| Operation      | Available Layers | Primary Handler    | Fallback Chain                           |
| -------------- | ---------------- | ------------------ | ---------------------------------------- |
| **Read**       | 2, 3, 4          | `excel` MCP server | MCP → openpyxl → Pandoc (xlsx/xls to MD) |
| **Write**      | 2, 3, 4          | `excel` MCP server | MCP → openpyxl → CSV fallback            |
| **CSV Output** | 3                | openpyxl + csv     | Python csv module                        |

> **Note**: Layer 1 (Direct Text Read) is skipped for `.xlsx` and `.xls` files because they are
> binary formats that agents cannot natively parse.

## Read Operation

### Handler Chain (AC2)

The read operation attempts handlers in this order:

#### Layer 1: Direct Text Read

**Applicability**: Skipped for `.xlsx` and `.xls` files (binary formats that agents cannot natively
parse).

**When used**: Only if the agent already has the spreadsheet content in its context window through a
previous tool invocation (e.g., markitdown already converted it).

#### Layer 2: MCP `excel` Server

**Handler**: `excel` MCP server (`excel-mcp-server` via `uvx`) configured in `opencode.jsonc`

**Primary tools**:

- `excel_read_data_from_excel` : Read data from a worksheet with cell metadata
- `excel_get_workbook_metadata` : Get workbook info including sheets, ranges, and dimensions
- `excel_validate_excel_range` : Validate if a range exists and is properly formatted
- `excel_get_merged_cells` : Get merged cell information for a worksheet
- `excel_get_data_validation_info` : Get data validation rules in a worksheet

**Expected output**: Structured cell data with addresses, values, row/column indices, and optional
validation metadata.

**Fall-through triggers**:

- MCP server timeout (>30 seconds)
- MCP server unreachable (connection error)
- Schema mismatch (unexpected response structure)
- Low-yield result (<50 characters after whitespace stripping)

#### Layer 3: `openpyxl` Library

**Handler**: `openpyxl` Python library

**What it does**: Parses the `.xlsx` file (which is a ZIP archive containing XML) and extracts:

- Sheet names and dimensions
- Cell values (strings, numbers, formulas, dates, booleans)
- Cell formatting (number formats, font, fill)
- Merged cell ranges
- Data validation rules
- Named ranges

**Limitations**:

- Does NOT execute formulas (returns the cached formula result, or `None` if not cached)
- Does NOT extract charts, images, or embedded objects
- Does NOT extract VBA macros
- Does NOT support legacy `.xls` format (use Pandoc for `.xls`)

**Fall-through triggers**:

- `ImportError` (openpyxl not installed)
- File corruption (cannot parse XML structure)
- `PermissionError` (file locked or read-only)
- Low-yield result (<50 characters)

#### Layer 4: Pandoc CLI

**Handler**: `pandoc` command-line tool

**Command**: `pandoc input.xlsx -t markdown`

**What it does**: Converts the spreadsheet to Markdown format. Pandoc reads `.xlsx` files and
produces one Markdown table per sheet.

**Advantages**:

- Works with both `.xlsx` and legacy `.xls` files
- Simple conversion without requiring Python dependencies
- Good fallback when openpyxl fails

**Fall-through triggers**:

- Pandoc not installed on the system
- Non-zero exit code
- Empty output file

### Normalised Markdown Output (AC5)

The read operation returns a normalised Markdown representation regardless of which layer produced
it. Each sheet becomes a separate section with one Markdown table:

```markdown
## Sheet 1

| Column A | Column B | Column C |
| -------- | -------- | -------- |
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |

## Sheet 2

| Name  | Value | Change |
| ----- | ----- | ------ |
| Alpha | 100   | +5%    |
| Beta  | 200   | -3%    |
```

**Known limitations of the normalised output**:

- Charts, images, and embedded objects are omitted
- Formula cells show cached values (not the formula itself)
- Merged cells are flattened (the value appears in the top-left cell, others are empty)
- Number formatting (currency, percentages) is lost; raw numeric values are shown
- Conditional formatting and cell styling are not preserved
- VBA macros and ActiveX controls are not extracted

## Write Operation

### Handler Chain (AC3)

The write operation modifies an existing `.xlsx` file or creates a new one. Handlers are attempted
in this order:

#### Layer 2: MCP `excel` Server

**Primary tools**:

- `excel_write_data_to_excel` : Write data to specific cells in a worksheet
- `excel_create_workbook` : Create a new workbook
- `excel_create_worksheet` : Create a new worksheet in an existing workbook
- `excel_apply_formula` : Apply a formula to a cell with verification
- `excel_format_range` : Apply formatting to a range of cells
- `excel_insert_rows` / `excel_insert_columns` : Insert rows or columns
- `excel_delete_sheet_rows` / `excel_delete_sheet_columns` : Delete rows or columns
- `excel_copy_range` : Copy a range of cells

**Advantages**: Full formatting support, formula verification, data validation, merged cells,
auto-fit columns.

**Fall-through triggers**: Same as read operation.

#### Layer 3: `openpyxl` Library

**What it does**: Creates or modifies `.xlsx` files programmatically:

- Create workbooks and worksheets
- Write cell values (strings, numbers, formulas, dates)
- Apply cell formatting (fonts, fills, borders, number formats)
- Merge and unmerge cells
- Set column widths and row heights
- Add data validation rules
- Create named ranges

**Limitations**:

- Complex chart creation requires additional libraries (`openpyxl.chart`)
- Macro-enabled files (`.xlsm`) may lose VBA content on save
- Very large files may be slow (openpyxl loads the entire workbook into memory)

**Fall-through triggers**: Same as read operation.

#### Layer 4: CSV Fallback (Binding D2)

**Handler**: Python `csv` module (standard library)

**What it does**: When both MCP and openpyxl fail for write operations, the data is written to a
`.csv` file as a last resort.

**Process**:

1. Convert the input data to a tabular format (list of lists or list of dicts)
2. Write to a `.csv` file using Python's `csv.writer`
3. One CSV file per sheet (if multiple sheets, append sheet name to filename)

**Advantages**:

- No external dependencies (`csv` is a standard library module)
- Universally readable format
- Simple, reliable output

**Limitations**:

- No formatting, formulas, or multiple sheets in a single file
- No cell styling, merged cells, or data validation
- User must manually convert to `.xlsx` if needed

**Important**: This is a last-resort fallback. The agent should inform the user that the output is
CSV, not `.xlsx`, and explain the limitations.

### Write Input Format (AC6)

The write operation accepts structured data in two formats:

**JSON input (2D array)**:

```json
{
  "sheets": [
    {
      "name": "Revenue",
      "data": [
        ["Quarter", "Revenue", "Costs", "Margin"],
        ["Q1 2026", 1200000, 800000, 400000],
        ["Q2 2026", 1350000, 820000, 530000]
      ]
    },
    {
      "name": "Summary",
      "data": [
        ["Metric", "Value"],
        ["Total Revenue", 2550000],
        ["Average Margin", "20.8%"]
      ]
    }
  ]
}
```

**JSON input (list of dicts)**:

```json
{
  "sheets": [
    {
      "name": "Team",
      "data": [
        { "Name": "Alice", "Role": "Architect", "Rate": 1800 },
        { "Name": "Bob", "Role": "Developer", "Rate": 1500 }
      ]
    }
  ]
}
```

The resulting `.xlsx` file must open without error in both Microsoft Excel and LibreOffice Calc.

## Legacy .xls Coverage (AC7)

### Read-Only Support

Legacy `.xls` files (pre-Office 2007 binary format) are supported for **read operations only**.

**Handler routing**:

- **Layer 1**: Not applicable (binary format)
- **Layer 2**: MCP `excel` server may support `.xls` if the underlying system has appropriate
  converters
- **Layer 3**: `openpyxl` does NOT support `.xls` format. This layer is **SKIPPED** for `.xls` files
  with a clear note in telemetry (`handler: py-openpyxl`, `outcome: fallthrough`,
  `error_class: unsupported_format`)
- **Layer 4**: Pandoc CAN read `.xls` files. This is the primary fallback for legacy `.xls`

**Important**: Write and generate operations are NOT supported for `.xls` format. If a write
operation targets a `.xls` file, the agent should:

1. Reject the operation with a clear error message
2. Suggest converting to `.xlsx` first
3. If the caller insists, attempt the write to a new `.xlsx` file instead

## CSV Output Mode (AC8)

The CSV output mode produces one `.csv` file per sheet from an existing `.xlsx` file.

### Process

1. **Layer 3 (Primary)**: Use `openpyxl` to read each sheet and write to CSV via Python `csv.writer`
2. **Layer 2 (Alternative)**: Use MCP `excel_read_data_from_excel` to extract data, then write to
   CSV via Python `csv.writer`
3. **Layer 4 (Fallback)**: Use Pandoc to convert to Markdown, then extract tables to CSV

### Output Convention

- One CSV file per sheet
- Filename pattern: `[original-name]-[sheet-name].csv`
- UTF-8 encoding with BOM for Excel compatibility
- Standard comma delimiter with proper quoting

### Example

For a workbook `pricing-model.xlsx` with sheets "Rates", "Costs", and "Summary":

```text
pricing-model-Rates.csv
pricing-model-Costs.csv
pricing-model-Summary.csv
```

## Telemetry Emission (AC4)

Every layer attempt emits exactly one fallback-telemetry record to the **canonical `cu:telemetry`
sink** (US-166), via `kits/core/skills/telemetry/scripts/telemetry_emitter.py`. All records for one
user operation share a `trace_id`. The persisted record conforms to the canonical schema
(`cu:telemetry`: `resources/fallback-event.schema.json`), NOT the cascade handler's richer internal
view , in particular it carries **no `filename` or content** (privacy invariant, AC6).

**Format-specific fields**:

| Field     | Value for this skill                                       |
| --------- | ---------------------------------------------------------- |
| `format`  | `xlsx` (legacy `.xls` reads are also recorded with `xlsx`) |
| `handler` | `llm-native`, `mcp-excel`, `py-openpyxl`, `pandoc`         |

**Emit step**: at each attempted layer, call the emitter with the canonical fields:

```python
from telemetry_emitter import TelemetryEmitter, new_trace_id

emitter = TelemetryEmitter()
trace_id = new_trace_id()  # once per user operation

# Layer 2 (MCP excel) under-yields and falls through:
emitter.emit(trace_id=trace_id, fmt="xlsx", operation="read",
             handler="mcp-excel", outcome="fallthrough", latency_ms=1500,
             error_class="low_yield")
# Layer 3 (openpyxl) succeeds:
emitter.emit(trace_id=trace_id, fmt="xlsx", operation="read",
             handler="py-openpyxl", outcome="success", latency_ms=410,
             file_size_bytes=51200)
```

**Example persisted records** (note: no `filename`, no extracted cell data):

```json
[
  {
    "trace_id": "8f1c9e2a-...-d4",
    "timestamp": "2026-06-13T10:30:01+00:00",
    "format": "xlsx",
    "operation": "read",
    "handler": "mcp-excel",
    "outcome": "fallthrough",
    "latency_ms": 1500,
    "error_class": "low_yield"
  },
  {
    "trace_id": "8f1c9e2a-...-d4",
    "timestamp": "2026-06-13T10:30:02+00:00",
    "format": "xlsx",
    "operation": "read",
    "handler": "py-openpyxl",
    "outcome": "success",
    "latency_ms": 410,
    "file_size_bytes": 51200
  }
]
```

**Excel-specific cascade nuance**: Pandoc cannot write or generate `.xlsx` output (Layer 4 of the
write/generate chain falls through to the CSV fallback, Binding D2). When a `pandoc` write/generate
attempt is recorded, it carries `outcome: fallthrough` with `error_class: unsupported_format` rather
than `success`.

```json
[
  {
    "trace_id": "3b7d0f44-...-9c",
    "timestamp": "2026-06-13T10:31:00+00:00",
    "format": "xlsx",
    "operation": "write",
    "handler": "pandoc",
    "outcome": "fallthrough",
    "latency_ms": 0,
    "error_class": "unsupported_format"
  }
]
```

The cascade decision and error-surfacing rules are inherited from `cu:cascade-handler`. This skill
does not re-implement them.

**Definition of Done (telemetry)**: this skill emits one `cu:telemetry` record per attempted cascade
layer, with no user content in the payload (AC6), and is covered by a test or documented manual
check that a record is written on fall-through.

## MCP Excel Server Troubleshooting

### Common Failure Modes

#### 1. Server Not Running

**Symptom**: `Connection refused` or `ECONNREFUSED` errors.

**Cause**: The MCP excel server process is not running or crashed.

**Resolution**:

1. Check if the server process is running: `ps aux | grep excel-mcp`
2. Restart the server through the OpenCode MCP management interface
3. If persistent, check `opencode.jsonc` for correct server configuration
4. Verify `uvx` can resolve `excel-mcp-server`: `uvx excel-mcp-server --help`

#### 2. Server Timeout

**Symptom**: Requests take longer than 30 seconds with no response.

**Cause**: Large spreadsheets (>10,000 rows), complex formulas, or resource exhaustion.

**Resolution**:

1. Retry the operation once (may be transient)
2. If persistent, fall back to Layer 3 (openpyxl) or Layer 4 (Pandoc)
3. For large files, use range-based reads (`excel_read_data_from_excel` with `start_cell` and
   `end_cell` parameters)
4. Report to framework maintainer if timeouts are consistent

#### 3. Schema Mismatch

**Symptom**: Response structure does not match expected format (missing fields, wrong types).

**Cause**: MCP server version mismatch or upstream API change.

**Resolution**:

1. Check the MCP server version: `uvx excel-mcp-server --version`
2. Update the MCP server: `uvx --upgrade excel-mcp-server`
3. Fall back to Layer 3 or 4

#### 4. File Permission Error

**Symptom**: `Permission denied` or `Access denied` errors.

**Cause**: File is locked by another application (Excel, LibreOffice) or has read-only permissions.

**Resolution**:

1. Close the file in any open application
2. Check file permissions: `ls -la filename.xlsx`
3. If on a network share, verify mount and access rights
4. For locked files on macOS: `lsof | grep filename.xlsx`

#### 5. Corrupt File

**Symptom**: `Cannot open file` or `Invalid format` errors.

**Cause**: File corruption, incomplete download, or wrong file extension.

**Resolution**:

1. Verify the file is actually an `.xlsx` file: `file filename.xlsx`
2. Try opening in LibreOffice Calc as a recovery attempt
3. If the file is a `.xls` with `.xlsx` extension, rename and retry with legacy handling
4. If the file is actually a CSV with `.xlsx` extension, treat as CSV

### Escalation Path

1. **First**: Fall back to Layer 3 or Layer 4 automatically
2. **Second**: Check MCP server logs for error details
3. **Third**: Report persistent issues to framework maintainer with telemetry trace_id

## Known Limitations

| Limitation                                  | Impact | Workaround                                               |
| ------------------------------------------- | ------ | -------------------------------------------------------- |
| Formulas not executed (cached values only)  | Medium | Open in Excel to refresh, or use `xlcalc` for evaluation |
| Charts and images not extracted             | Low    | Use Layer 2 (MCP) for metadata about charts              |
| Merged cells flattened in output            | Medium | Use `excel_get_merged_cells` to detect merge ranges      |
| Legacy .xls is read-only                    | Medium | Convert to .xlsx first for write operations              |
| Large files may timeout in MCP              | Medium | Use range-based reads; fall back to openpyxl             |
| VBA macros not extracted                    | Low    | Use `oletools` for macro extraction (out of scope)       |
| Number formatting lost in normalised output | Low    | Access raw cell data via Layer 3 for format info         |
| Pandoc cannot output .xlsx                  | None   | By design; CSV fallback for write Layer 4 (D2 binding)   |

## Installation Requirements

| Component  | Install Command               | Required For                          |
| ---------- | ----------------------------- | ------------------------------------- |
| `openpyxl` | `pip install openpyxl`        | Layer 3 read/write                    |
| Pandoc     | `brew install pandoc` (macOS) | Layer 4 read                          |
| `xlrd`     | `pip install xlrd`            | Optional: legacy .xls read via Python |

## Related Documentation

- **cu-cascade-handler**: Foundational cascade protocol skill (dependency)
- **ADR-017**: Cascading fallback for document processing (architectural decision)
- **ADR-009**: Skill architecture and loading model (MECE rule)
- **US-166**: Centralise fallback telemetry and MCP health observability (telemetry consumer)
- **US-159**: Word document processing skill (sister skill)
- **US-161**: PowerPoint processing skill (sister skill)
- **US-162**: PDF document processing skill (sister skill)
- **US-163**: Word template generation (downstream consumer)
- **US-164**: Reference export with Word and PDF (downstream consumer)
- **CV-generation skill**: an Excel consumer for pricing/team tables (kit-supplied)
