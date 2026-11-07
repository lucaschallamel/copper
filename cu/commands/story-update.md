---
description: Maintain story file content (acceptance criteria, status, progress).
  Supports ad-hoc updates and future cu-pipe delegation. Validates inputs against
  story file structure.
---

> **Documentation root (TD-178)**: paths below are written against the default `docs-copper/`. A
> project whose documentation lives elsewhere (for example `docs/`) is discovered automatically by
> the guard scripts, or pinned with `COPPER_DOCS_ROOT`. Read `docs-copper/` here as "the
> documentation root", not as a literal path.

# /cu:story-update

Update story file content for: **$ARGUMENTS**

---

## Overview

This command maintains story file content - acceptance criteria checkboxes, status field, and
progress entries. It provides structured, validated modifications to backlog story files located in
`docs-copper/roadmap/backlog/`.

**Callable**: standalone for ad-hoc story updates **Future**: cu-pipe Phase 4.5 will delegate to
this command (US-140)

**This command never creates or deletes story files.** It only modifies existing ones.

---

## Arguments

Parse `$ARGUMENTS` as: `<action> <story-id> [action-args...]`

### Actions

| Action     | Syntax                                    | Description                             |
| ---------- | ----------------------------------------- | --------------------------------------- |
| `ac`       | `ac <story-id> <number> <check\|uncheck>` | Toggle acceptance criteria checkbox     |
| `progress` | `progress <story-id> <note>`              | Add dated progress entry (newest first) |
| `status`   | `status <story-id> <new-status>`          | Update frontmatter status field         |

### Valid Status Values

`Ready` | `In Progress` | `Done` | `Cancelled`

---

## Step 0: Resolve Story File

Locate the story file using glob pattern matching.

**Procedure**:

1. Glob for `docs-copper/roadmap/backlog/<story-id>-*.md`
2. Count matches:
   - **0 matches**: STOP with error:
     `"No story file found for ID <story-id> in docs-copper/roadmap/backlog/"`
   - **1 match**: Proceed with resolved path
   - **>1 matches**: STOP with error:
     `"Multiple files match <story-id>-*.md: [list files]. Refine the story ID."`
3. Read the file content for modification

**This gate satisfies AC5** (glob safety).

---

## Step 1: Validate Action and Inputs

### Gate 1: Action Validation

Verify `<action>` is one of: `ac`, `progress`, `status`.

- If invalid: STOP with error: `"Unknown action '<action>'. Valid actions: ac, progress, status"`

### Gate 2: Input Validation Per Action

**For `ac`**:

- `<number>` must be a positive integer
- `<check|uncheck>` must be exactly `check` or `uncheck`
- Error: `"Usage: ac <story-id> <number> <check|uncheck>"`

**For `progress`**:

- `<note>` must be non-empty text
- Error: `"Usage: progress <story-id> <note text>"`

**For `status`**:

- `<new-status>` must be in valid enum: `Ready`, `In Progress`, `Done`, `Cancelled`
- Error: `"Invalid status '<new-status>'. Valid values: Ready, In Progress, Done, Cancelled"`

---

## Step 2: Execute Action

### Action: `ac` - Toggle Acceptance Criteria

**Procedure**:

1. Search the story file for a line matching `**AC<number>**` (with any bracket prefix)
2. If no match found: STOP with error: `"AC<number> not found in story file <story-id>"`
3. Determine current state:
   - If line contains `- [x]` and action is `check`: no-op, report `"AC<number> is already checked"`
   - If line contains `- [ ]` and action is `uncheck`: no-op, report
     `"AC<number> is already unchecked"`
4. Toggle the checkbox:
   - `check`: replace `- [ ]` with `- [x]` on the matching line
   - `uncheck`: replace `- [x]` with `- [ ]` on the matching line
5. Update `last_modified` in frontmatter to today's date

### Action: `progress` - Add Progress Entry

**Procedure**:

1. Locate the `> [!note]- Progress updates` callout in the file
2. If no callout exists: create one immediately after the YAML frontmatter closing `---`
3. Determine the insertion point:
   - After the callout opening line(s) (`> [!note]- Progress updates` and the blank `>` line)
   - BEFORE existing progress entries (newest first)
4. Format the new entry:

```markdown
> - **YYYY-MM-DD**: <note text>
```

5. Insert the entry at the determined position
6. Update `last_modified` in frontmatter to today's date

**Format requirement**: Date must be strict `YYYY-MM-DD` format (no parenthetical suffixes). This
aligns with the user-story-validator `INVALID_PROGRESS_ENTRY` check.

### Action: `status` - Update Story Status

**Procedure**:

1. Read the YAML frontmatter (between the opening and closing `---` markers)
2. Locate the `status:` field
3. If current status equals requested status: no-op, report `"Status is already '<status>'"`
4. Replace the status value:

```yaml
# Before
status: In Progress
# After
status: Done
```

5. Update `last_modified` in frontmatter to today's date

---

## Step 3: Preview and Confirm

**Before writing any changes**:

1. Show a diff preview of the proposed changes
2. Ask the user to confirm:
   - **A**: Apply changes
   - **B**: Abort without changes
3. Only write to file on explicit user confirmation

---

## Step 4: Write and Report

**On confirmation**:

1. Write the modified content back to the story file
2. Report the action taken:

```
Story file updated: docs-copper/roadmap/backlog/<story-id>-<slug>.md
Action: <action> <details>
```

---

## Error Handling

| Error               | Message                                | Recovery                                   |
| ------------------- | -------------------------------------- | ------------------------------------------ |
| No story file       | `"No story file found for ID <id>"`    | Check story ID spelling                    |
| Multiple files      | `"Multiple files match: [list]"`       | Use more specific ID                       |
| Invalid action      | `"Unknown action '<action>'"`          | Use ac, progress, or status                |
| Invalid AC number   | `"AC<N> not found in story file"`      | Check AC numbering in file                 |
| Invalid status      | `"Invalid status '<status>'"`          | Use Ready, In Progress, Done, or Cancelled |
| Empty note          | `"Progress note cannot be empty"`      | Provide note text                          |
| Missing frontmatter | `"Story file has no YAML frontmatter"` | Check file format                          |

---

## Example Usage

```
# Check an acceptance criterion
/cu:story-update ac US-138 1 check

# Uncheck an acceptance criterion
/cu:story-update ac US-138 3 uncheck

# Add a progress entry
/cu:story-update progress US-138 S5 review completed, 3 findings addressed

# Update story status
/cu:story-update status US-138 Done
```

---

## Verified Claims

After execution, verify:

- Story file still has valid YAML frontmatter (no corruption)
- Modified field reflects the requested change
- `last_modified` is updated to today's date
- No unintended side effects on other fields
