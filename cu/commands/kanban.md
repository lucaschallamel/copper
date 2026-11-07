---
description: Manage Kanban board cards (move, sync, list) using the kanban-board-management
  skill
---

> **Documentation root (TD-178)**: paths below are written against the default `docs-copper/`. A
> project whose documentation lives elsewhere (for example `docs/`) is discovered automatically by
> the guard scripts, or pinned with `COPPER_DOCS_ROOT`. Read `docs-copper/` here as "the
> documentation root", not as a literal path.

# /cu:kanban

Manage Kanban board cards for the COPPER framework: **$ARGUMENTS**

---

## Overview

This command wraps the `cu:kanban-board-management` skill for structured Kanban board operations. It
provides move, sync, and list actions for managing story cards on Obsidian Kanban boards.

**Delegated from**: cu-pipe Phase 4.5 (story document maintenance) **Also callable**: standalone for
ad-hoc board management

**Skill dependency**: `${CLAUDE_PLUGIN_ROOT}/skills/kanban-board-management/SKILL.md` (4-column structure,
status-to-column mapping)

---

## Actions

### `move <story-id> <status>`

Move a story card to the column matching the new status.

**Steps**:

1. **Validate status** against the approved enum (see Status Reference below). Normalise
   case-insensitively and resolve aliases.
2. **Find the story file** in `docs-copper/roadmap/backlog/` matching `<story-id>` (e.g. `US-136`).
   If not found, report error with guidance.
3. **Discover the board** (see Board Discovery below).
4. **Locate the card** on the board by deriving the card reference from the story filename. The
   format is `[[<filename-without-extension>]]` (e.g.
   `[[US-136-create-cu-kanban-command-for-kanban-board-synchronisation]]`).
5. **Remove the card** from its current column.
6. **Add the card** to the target column with the correct Task Genius checkbox (see Status
   Reference).
7. **Update the story file**: set `status:` in frontmatter. If moving to `done` or `completed`, also
   set `completed_date:` to today (YYYY-MM-DD).
8. **Format the board file**: run `npx prettier --write <board-path>` to ensure consistent
   formatting.

**On card not found**: If the card does not exist in any column, offer to add it to the target
column directly.

**On duplicate cards**: If the card appears in multiple columns, flag the error, report which
columns contain the card, and ask the user which to keep before proceeding.

---

### `sync <story-id>`

Synchronise the board card position to match the story's current `status:` frontmatter value.

**Steps**:

1. **Read the story file** and extract its `status:` value from frontmatter.
2. **Discover the board**.
3. **Determine the target column** from the status-to-column mapping.
4. **Locate the card** on the board.
5. **If already in the correct column**: confirm to user, no changes needed (idempotent).
6. **If in a different column**: remove from current, add to target with correct checkbox.
7. **Format the board file**: run `npx prettier --write <board-path>`.

**Use case**: After manually editing a story's status, run `/cu:kanban sync US-136` to ensure the
board reflects the change.

---

### `list`

List all cards on the board, grouped by column.

**Steps**:

1. **Discover the board**.
2. **Parse all four columns** (TODO, DOING, DONE, CARPARK).
3. **Display** a summary of cards per column:

   ```text
   === Kanban Board: <board-name> ===

   📋 TODO (N cards)
     - [ ] US-101: Document Claude subscription setup
     - [ ] US-102: Ship transcript formatting utility
     ...

   🔄 DOING (N cards)
     - [/] US-136: Create /cu:kanban command
     ...

   ✅ DONE (N cards)
     - [x] US-135: Create /cu:qa-gate command
     ...

   🅿️ CARPARK (N cards)
     (empty)

   Total: N cards across 4 columns
   WIP (DOING): N cards
   ```

4. **Report WIP**: count of cards in DOING column. Warn if exceeds recommended limit of 2 ou 3 per
   person.

---

## Status Reference

### Approved Status Enum

| Status        | Column      | Checkbox | Aliases                 |
| ------------- | ----------- | -------- | ----------------------- |
| `todo`        | **TODO**    | `[ ]`    |                         |
| `pending`     | **TODO**    | `[ ]`    |                         |
| `scheduled`   | **TODO**    | `[<]`    |                         |
| `in-progress` | **DOING**   | `[/]`    | `in_progress`, `active` |
| `delegated`   | **DOING**   | `[>]`    |                         |
| `done`        | **DONE**    | `[x]`    | `completed`             |
| `cancelled`   | **CARPARK** | `[-]`    |                         |
| `deferred`    | **CARPARK** | `[-]`    |                         |
| `on-hold`     | **CARPARK** | `[-]`    |                         |
| `blocked`     | **CARPARK** | `[?]`    |                         |

### Normalisation Rules

- **Case-insensitive**: `Done`, `DONE`, `done` all map to the same status.
- **Hyphen/underscore**: `in-progress` and `in_progress` are equivalent.
- **Alias resolution**: `completed` maps to `done`, `active` maps to `in-progress`.
- **Canonical output**: Always use the canonical form (left column) in frontmatter updates.

---

## Board Discovery

### Default Behaviour

Scan `docs-copper/roadmap/dashboards/` for Markdown files containing `kanban-plugin: board` in
frontmatter.

1. If exactly one board is found, use it.
2. If multiple boards are found, report the list and ask the user to specify with
   `--board <filename>`.
3. If no board is found, report error with guidance to create one.

### Manual Override

Use `--board <filename>` to specify a board explicitly:

```text
/cu:kanban move US-136 done --board Kanban-Board.md
```

---

## Card Format

### Deriving the Card Reference

The card reference on the board is `[[<story-filename-without-extension>]]`.

**Example**:

- Story file: `US-136-create-cu-kanban-command-for-kanban-board-synchronisation.md`
- Card reference: `[[US-136-create-cu-kanban-command-for-kanban-board-synchronisation]]`

### Legacy Format (TODO-XXX)

Some boards may use the `[[TODO-XXX]]` format documented in the skill. If the derived full-slug
reference is not found on the board, check for a matching `TODO-XXX` entry as a fallback.

---

## Arguments

| Argument     | Default | Description                                          |
| ------------ | ------- | ---------------------------------------------------- |
| `$ARGUMENTS` | (none)  | Action and parameters (see Actions above)            |
| `--board`    | auto    | Specific board filename in `docs-copper/dashboards/` |

---

## Examples

```text
# Move a story to DOING
/cu:kanban move US-137 in-progress

# Complete a story
/cu:kanban move US-136 done

# Block a story
/cu:kanban move US-101 blocked

# Sync a story after manual status edit
/cu:kanban sync US-136

# List all cards on the board
/cu:kanban list
```

---

## Pipeline Integration (cu-pipe)

When called from cu-pipe Phase 4.5 (story document maintenance):

1. After updating story status in frontmatter, call `/cu:kanban move <story-id> <new-status>`
2. The move action handles board update and formatting automatically
3. No separate sync step needed after a move

**Note**: cu-pipe Phase 4.5 reference update is deferred to US-140 (CAPSTONE).

---

## Related Commands

- `/cu:pipe`: Pipeline orchestration (calls this command at Phase 4.5)
- `/cu:qa-gate`: Quality gate orchestration (similar extraction pattern)
