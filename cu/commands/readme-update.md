---
description: Systematically review and update all README.md files in a folder hierarchy
---

# /cu:readme-update

Systematically review and update all README.md files in subfolders of: **$ARGUMENTS**

---

## Overview

This command scans a folder hierarchy, identifies existing and missing README.md files, and updates
them with consistent, concise documentation.

---

## Phase 1: Discovery

- Scan all subfolders recursively from the designated folder
- Identify existing README.md files
- Identify folders lacking README.md files (where appropriate)
- Build a hierarchical map of the folder structure
- **Skip ignored patterns**: `.git/`, `node_modules/`, `build/`, `__pycache__/`, `.venv/`,
  `.obsidian/`

---

## Phase 2: Planning (INTERACTIVE)

Present to user:

- Total folders discovered
- Existing READMEs found
- Folders needing READMEs (if creating new)
- Estimated scope of work

**Request confirmation before proceeding** to Update Phase.

---

## Phase 3: Analysis

For each folder with or needing a README:

- Analyse the folder's contents (files, subfolders)
- Determine the folder's purpose from:
  - File names and extensions
  - Existing documentation
  - Code comments (if applicable)
  - Parent/sibling folder context
- **Preserve custom content**: If README has manual additions beyond template structure, flag for
  review

---

## Phase 4: Update

**Content Guidelines:**

- Keep content **concise and to the point** (prefer <50 lines)
- Focus on **scope and nature** of contents
- Prioritise **readability and explainability**
- Include a **hierarchical view** of subfolders and files (max 2-3 levels deep)
- Use **British English** spelling:
  - `organise` not `organize`
  - `colour` not `color`
  - `centre` not `center`
  - `analyse` not `analyze`

**Show diff preview** before writing changes to each README.

---

## README Structure Template

```markdown
# [Folder Name]

[One-line description of folder purpose]

## Contents

[Brief explanation of what this folder contains and why it exists]

## Structure

folder-name/ ├── subfolder-1/ # Brief description │ ├── file-a.ext # Purpose │ └── file-b.ext #
Purpose ├── subfolder-2/ # Brief description └── file-c.ext # Purpose

## Related

- [[parent-folder]] - [Context]
- [[sibling-folder]] - [Related documentation]
```

**Template Notes:**

- Use Obsidian-style `[[wikilinks]]` for internal documentation references
- Keep structure tree to 2-3 levels maximum (use "..." for deeper nesting)
- Omit "Related" section if no relevant cross-references exist
- For folders with many files (>10), group by type/category rather than listing all

---

## Quality Criteria

- **Length**: Maximum ~100 lines per README (prefer 30-50)
- **Redundancy**: No duplicate information from parent READMEs
- **Hierarchy**: Clear context within folder structure
- **Accuracy**: File/folder descriptions match actual content
- **Consistency**: Uniform formatting across all READMEs
- **Preservation**: Retain important manual content (flag if uncertain)

---

## Example Usage

```bash
# Update READMEs in a source folder
/cu:readme-update src/

# Update READMEs in architecture folder
/cu:readme-update architecture/

# Update with auto-confirm for batch operations
/cu:readme-update docs/ --auto-confirm

# Create READMEs for folders lacking them
/cu:readme-update internal-projects/ --create-missing
```

---

## Output

### Progress Report (per folder)

- Folder path
- Action taken (updated/created/skipped)
- Diff preview (if changed)
- Confirmation prompt (unless `--auto-confirm`)

### Final Summary

- Total folders scanned
- READMEs updated
- READMEs created (if enabled)
- READMEs skipped (with reasons)
- Folders with custom content requiring manual review

---

**Principle Codes**: [SD] Strategic Documentation, [RP] Readability Priority, [SF] Simplicity First
