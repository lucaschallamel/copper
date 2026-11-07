---
name: productivity-system-management
description: Comprehensive guidance for managing the user's Obsidian-based personal productivity system. Covers Kanban board, Full Calendar integration, OKR tracking, and operational workflows. Use when managing tasks, scheduling time blocks, tracking OKRs, or performing system health checks.
version: 1.4.1
last_updated: '2026-07-11'
maintained_by: Lucas Challamel
applies_to: 'Primary: the executive-assistant role | Secondary: the agile-coaching and CTO-coaching roles'
---

# Skill: Productivity System Management

## Purpose

This skill provides comprehensive guidance for managing the user's Obsidian-based personal
productivity system. It covers the Kanban board, Full Calendar integration, OKR tracking, and all
operational workflows.

---

## System Overview

### Architecture

The user's productivity system integrates three core components:

1. **Kanban Board** (`Kanban-Board.md`): 4-column task management with WIP limits
2. **Full Calendar** (`weekly-planner/`): 4-colour-coded calendars for time allocation
3. **OKR Framework**: 7 objectives (BL-O2 + DL-KR1-6) linked to activities

**Core Philosophy**: TODOs define WHAT to do, Time Blocks define WHEN to do it, both are OKR-linked.

### File Structure

```
user-productivity/
├── AGENTS.md                    # Agent instructions (this system)
├── Kanban-Board.md              # Kanban plugin board
├── backlog/                     # TODO notes
│   └── TODO-XXX.md              # Simplified naming (e.g., TODO-039.md)
├── weekly-planner/              # Full Calendar event sources
│   ├── billable/               # 🟢 Green - Client work
│   ├── okr-ops/               # 🔵 Blue - OKR & management
│   ├── initiatives/            # 🟣 Purple - Projects & misc
│   └── personal/               # 🔴 Red - Personal & family
└── reviews/                    # Weekly/monthly/quarterly reviews
    └── YYYY-MM-DD-*.md
```

---

## Kanban Board Management

### 4-Column Structure

| Column      | Status Values                                 | Purpose               | Card Checkbox |
| ----------- | --------------------------------------------- | --------------------- | ------------- |
| **TODO**    | `todo`, `pending`, `scheduled`                | Backlog, not started  | `[ ]`         |
| **DOING**   | `in-progress`, `active`, `delegated`          | Work in progress      | `[/]`         |
| **DONE**    | `completed`, `done`                           | Successfully finished | `[x]`         |
| **CARPARK** | `blocked`, `cancelled`, `deferred`, `on-hold` | Blocked or deferred   | `[-]`         |

### Status-to-Column Mapping

```
TODO File Status          →  Kanban Column  →  Card Checkbox
─────────────────────────────────────────────────────────────
status: todo              →  TODO           →  - [ ]
status: pending           →  TODO           →  - [ ]
status: scheduled         →  TODO           →  - [ ]
status: in-progress       →  DOING          →  - [/]
status: active            →  DOING          →  - [/]
status: delegated         →  DOING          →  - [/]
status: completed         →  DONE           →  - [x]
status: done              →  DONE           →  - [x]
status: blocked           →  CARPARK        →  - [-]
status: cancelled         →  CARPARK        →  - [-]
status: deferred          →  CARPARK        →  - [-]
status: on-hold           →  CARPARK        →  - [-]
```

### WIP Limit

**Critical Rule**: Maximum 3 tasks in DOING column at any time.

**Enforcement**:

1. Before moving task to DOING, count current DOING tasks
2. If count = 3, cannot add another
3. Must complete or defer existing DOING task first
4. Consider WIP = 2 for focused periods (reduces context switching)

### Card Format

Cards are wikilinks to TODO notes using simplified naming:

```markdown
## TODO

- [ ] [[TODO-001]]
- [ ] [[TODO-002]]

## DOING

- [/] [[TODO-039]]
- [/] [[TODO-038]]

## DONE

- [x] [[TODO-015]]

## CARPARK

- [-] [[TODO-050]]
```

---

## Full Calendar Integration

### 4-Calendar Structure

| Calendar                   | Folder                        | Color     | Hex       | Purpose                                     |
| -------------------------- | ----------------------------- | --------- | --------- | ------------------------------------------- |
| **BILLABLE**               | `weekly-planner/billable/`    | 🟢 Green  | `#22C55E` | Client work - target 40% (10 segments/week) |
| **OKR Operating System**   | `weekly-planner/okr-ops/`     | 🔵 Blue   | `#3B82F6` | Management & OKR activities - 40%           |
| **Initiatives & Projects** | `weekly-planner/initiatives/` | 🟣 Purple | `#8B5CF6` | Projects & miscellaneous - 20%              |
| **PERSONAL**               | `weekly-planner/personal/`    | 🔴 Red    | `#EF4444` | Personal events & family time               |

### Time Block Naming

**Format**: `YYYY-MM-DD HH-mm-title.md`

**Examples**:

- `2026-01-06 07-00 Week Planning.md`
- `2026-01-07 09-00 Client Workshop.md`
- `2026-01-08 14-00 Team 1-on-1.md`

### Time Block Frontmatter

```yaml
---
title: 'Event Title'
date: 2026-01-06
startTime: '09:00'
endTime: '11:00'
type: single
allDay: false
completed: null | true | false
activity_type:
  BILLABLE | ITG-DEV | SE-SUPP | STRAT-AM | COMM | PEOPLE | BENCH | ADMIN | DEV | PERSONAL | BREAK |
  MGMT | AI-TRANS
okr: N/A | BL-O2 | DL-KR1 | DL-KR2 | DL-KR3 | DL-KR4 | DL-KR5 | DL-KR6
todo_ref: '[[TODO-2026-01-06-001-task-name]]'
tags:
  - time-block
  - itg-2026
---
```

### TODO-Time Block Linkage

**Critical**: Every scheduled task should have:

1. A TODO note in `backlog/` with full frontmatter
2. A time block in appropriate calendar folder with `todo_ref` linking to TODO
3. Matching `activity_type` and `okr` values

**When completing work**:

1. Update time block: `completed: true`
2. Update TODO: `actual_hours: <time spent>`
3. When fully done: Update TODO `status: done`, `completed_date: YYYY-MM-DD`

---

## Activity Types

### 14 Activity Types with OKR Linkage

| Code       | OKR Link | Purpose                      | Calendar  |
| ---------- | -------- | ---------------------------- | --------- |
| `BILLABLE` | DL-KR6   | Client work (40% target)     | 🟢 Green  |
| `ITG-DEV`  | DL-KR1   | IT governance development    | 🔵 Blue   |
| `SE-SUPP`  | DL-KR2   | SE team support              | 🔵 Blue   |
| `STRAT-AM` | DL-KR3   | Strategic account management | 🔵 Blue   |
| `COMM`     | DL-KR6   | Commercial performance       | 🔵 Blue   |
| `PEOPLE`   | DL-KR5   | People & engagement          | 🔵 Blue   |
| `AI-TRANS` | BL-O2    | AI transformation            | 🟣 Purple |
| `BENCH`    | DL-KR4   | Bench management             | 🟣 Purple |
| `MGMT`     | N/A      | General management           | 🔵 Blue   |
| `ADMIN`    | N/A      | Administrative tasks         | 🟣 Purple |
| `DEV`      | N/A      | Development work             | 🟣 Purple |
| `PERSONAL` | N/A      | Personal development         | 🟣 Purple |
| `BREAK`    | N/A      | Breaks / personal time       | 🟣 Purple |

### Activity Type Selection Guide

**When to use each type**:

- **BILLABLE**: Any work directly billed to a client (delivery, consulting, workshops)
- **ITG-DEV**: IT governance framework development, maturity models, assessments
- **SE-SUPP**: Supporting SE team members, proposal reviews, technical guidance
- **STRAT-AM**: Strategic account activities, QBRs, relationship building
- **COMM**: Business development, pipeline management, commercial activities
- **PEOPLE**: 1-on-1s, team meetings, HR activities, engagement initiatives
- **AI-TRANS**: AI strategy, GenAI initiatives, AI governance
- **BENCH**: Bench utilisation tracking, resource allocation, staffing
- **MGMT**: General management, manager syncs, leadership activities
- **ADMIN**: System maintenance, documentation, administrative tasks
- **DEV**: Personal development projects, learning, experimentation
- **PERSONAL**: Personal activities during work hours (appointments, etc.)
- **BREAK**: Lunch, coffee breaks, rest periods

---

## OKR Framework

### 7 Objectives

| OKR        | Name                   | Focus                | Target                             |
| ---------- | ---------------------- | -------------------- | ---------------------------------- |
| **BL-O2**  | AI Transformation      | Transverse objective | AI strategy, GenAI adoption        |
| **DL-KR1** | ITG Development        | Maturity model       | Framework development, assessments |
| **DL-KR2** | SE Wins                | Team support         | SE team success, proposal support  |
| **DL-KR3** | Strategic Accounts     | Account management   | QBRs, relationship building        |
| **DL-KR4** | Bench Management       | Utilisation          | Bench-to-bill optimisation         |
| **DL-KR5** | People & Engagement    | Team health          | 1-on-1s, engagement, retention     |
| **DL-KR6** | Commercial Performance | Revenue              | 40% billable, pipeline, wins       |

### Weekly OKR Coverage Rule

**Critical**: All 7 OKRs should be touched weekly.

**Tracking**:

1. At week end, count tasks/time blocks per OKR
2. Flag OKRs with zero touch
3. Recommend tasks to fill gaps
4. Adjust next week's plan accordingly

### OKR Coverage Template

```markdown
## Weekly OKR Coverage - Week N

| OKR    | Tasks | Hours | Status |
| ------ | ----- | ----- | ------ |
| BL-O2  | 2     | 4h    | ✅     |
| DL-KR1 | 3     | 6h    | ✅     |
| DL-KR2 | 1     | 2h    | ✅     |
| DL-KR3 | 0     | 0h    | ⚠️ Gap |
| DL-KR4 | 1     | 1h    | ✅     |
| DL-KR5 | 2     | 3h    | ✅     |
| DL-KR6 | 5     | 20h   | ✅     |

**Coverage**: 6/7 OKRs (86%) **Gap**: DL-KR3 needs attention next week
```

---

## TODO Note Standards

### Naming Convention (UPDATED 2026-01-14)

**Format**: `TODO-XXX.md`

**Components**:

- `TODO-`: Prefix (always)
- `XXX`: 3-digit sequential number (001-999)

**Examples**:

- `TODO-001.md`
- `TODO-039.md`
- `TODO-125.md`

**IMPORTANT**: The title and all metadata are stored in the YAML frontmatter, NOT in the filename.
This keeps filenames short and clean while maintaining full searchability via frontmatter
properties.

### Frontmatter Template

```yaml
---
id: TODO-XXX
title: "Descriptive Task Title Here"
created: YYYY-MM-DD
due: YYYY-MM-DD
priority: high | medium | low
status: todo | in-progress | done | blocked | cancelled | deferred
okr: N/A | BL-O2 | DL-KR1 | DL-KR2 | DL-KR3 | DL-KR4 | DL-KR5 | DL-KR6
tags:
  - tag1
  - tag2
assignee: [User Name]
---

> [!note]- Progress Updates
> **YYYY-MM-DD** - Initial task creation. [Context]
> **YYYY-MM-DD** - [Update description]

# TODO-XXX: Task Title

## Context
[Why this task exists, background information]

## Action Items
- [ ] Action 1
- [ ] Action 2

## Notes
[Additional context]

---

*Created: YYYY-MM-DD | Last Updated: YYYY-MM-DD | OKR: XXX*
```

### Progress Updates Format (CRITICAL)

**Location**: Immediately after YAML frontmatter, BEFORE the H1 title.

**Format**: Obsidian collapsible callout using `> [!note]-` syntax:

```markdown
> [!note]- Progress Updates **2026-01-14** - Manager approved 10 half-days. Impact-driven mode.
> **2026-01-13** - Task created following 1-on-1 meeting.
```

**Rules**:

- Use `> [!note]-` (with minus) to make it collapsible by default
- Each update on a new line starting with `>`
- Date in bold: `**YYYY-MM-DD**`
- Most recent update FIRST (reverse chronological)
- Keep updates concise (1 line per update)
- This format integrates with Obsidian's native callout rendering

### Required Frontmatter Properties

| Property   | Required    | Description                            |
| ---------- | ----------- | -------------------------------------- |
| `id`       | ✅ Yes      | Unique identifier (e.g., `TODO-039`)   |
| `title`    | ✅ Yes      | Human-readable task title              |
| `created`  | ✅ Yes      | Creation date (YYYY-MM-DD)             |
| `due`      | ✅ Yes      | Due date (YYYY-MM-DD)                  |
| `priority` | ✅ Yes      | `high`, `medium`, or `low`             |
| `status`   | ✅ Yes      | Current status (maps to Kanban column) |
| `okr`      | ✅ Yes      | Linked OKR or `N/A`                    |
| `tags`     | ⚪ Optional | List of tags for filtering             |
| `assignee` | ⚪ Optional | Who owns this task                     |

### Priority Levels

| Priority   | Criteria                                           | Examples                                 |
| ---------- | -------------------------------------------------- | ---------------------------------------- |
| **high**   | Urgent + Important, blocking others, client-facing | Client deadlines, blocking dependencies  |
| **medium** | Important but not urgent, scheduled work           | Planned deliverables, OKR activities     |
| **low**    | Nice-to-have, can be deferred                      | Admin tasks, documentation, optimisation |

### Dependencies

**`depends_on`**: Tasks that must complete before this task can start **`blocks`**: Tasks that
cannot start until this task completes

```yaml
depends_on:
  - TODO-001 # This task needs 001 to complete first
blocks:
  - TODO-010 # Task 010 is waiting for this task
```

---

## Weekly Rhythm

### Standard Week Pattern

| Day           | Focus    | Typical Activities                            |
| ------------- | -------- | --------------------------------------------- |
| **Monday**    | Planning | Week planning, manager sync, priority setting |
| **Tuesday**   | Delivery | Billable work, client delivery                |
| **Wednesday** | Delivery | Billable work, client delivery                |
| **Thursday**  | Flex     | Client overflow, internal projects, meetings  |
| **Friday**    | Review   | Week retro, OKR review, admin catch-up        |
| **Weekend**   | Personal | Family time, rest (protected)                 |

### Billable Target

**Target**: 40% of work time = 20 hours/week = 10 segments

**Calculation**:

- 50-hour work week capacity
- 40% billable = 20 hours
- 2-hour segments = 10 segments/week

**Tracking**:

- Count BILLABLE time blocks weekly
- Alert if below 15 hours by Thursday
- Prioritise billable work on Tue/Wed

---

## Status Synchronisation

### The Golden Rule

**TODO file `status:` field is the source of truth.**

When status changes:

1. **Update TODO file first** (change `status:` value)
2. **Then update Kanban card** (change checkbox)
3. **Verify consistency** (file status matches column)

### Common Synchronisation Issues

**Issue 1: Kanban shows DOING, file shows `todo`**

- **Cause**: Kanban checkbox updated, file not updated
- **Fix**: Update file to `status: in-progress`

**Issue 2: Task in wrong column**

- **Cause**: Status value doesn't match column mapping
- **Fix**: Update status to correct value for desired column

**Issue 3: Completed task not in DONE**

- **Cause**: Forgot to update status after completing
- **Fix**: Update `status: done`, `completed_date`, move card

### Synchronisation Check Script

```bash
# Find status mismatches
for file in backlog/TODO-*.md; do
  status=$(grep "^status:" "$file" | cut -d: -f2 | tr -d ' ')
  echo "$file: $status"
done
```

---

## System Health Metrics

### Key Metrics

| Metric               | Target | Warning | Critical |
| -------------------- | ------ | ------- | -------- |
| Billable Hours/Week  | ≥20    | <15     | <10      |
| Overdue Tasks        | 0      | 1-3     | >5       |
| WIP (DOING)          | ≤3     | =3      | >3       |
| OKR Coverage         | 7/7    | 5-6/7   | <5/7     |
| Status Sync Errors   | 0      | 1-2     | >3       |
| TODO-TimeBlock Links | 100%   | 80-99%  | <80%     |

### Health Check Template

```markdown
## 🏥 System Health - YYYY-MM-DD

### Overall Status: 🟢 Healthy | 🟡 Attention | 🔴 Critical

### Metrics

| Metric         | Current | Target | Status   |
| -------------- | ------- | ------ | -------- |
| Billable Hours | X       | ≥20    | 🟢/🟡/🔴 |
| Overdue Tasks  | X       | 0      | 🟢/🟡/🔴 |
| WIP Compliance | X/3     | ≤3     | 🟢/🟡/🔴 |
| OKR Coverage   | X/7     | 7/7    | 🟢/🟡/🔴 |
| Sync Errors    | X       | 0      | 🟢/🟡/🔴 |

### Issues Found

1. [Issue description]
2. [Issue description]

### Recommended Actions

1. [Action with priority]
2. [Action with priority]
```

---

## Common Operations

### Creating a New TODO

1. **Determine next number**: Find highest existing TODO number, increment by 1
2. **Generate filename**: `TODO-XXX.md` (e.g., `TODO-040.md`)
3. **Create file** in `backlog/` with frontmatter template including `title` property
4. **Add to Kanban**: Add card `[[TODO-XXX]]` to TODO column
5. **Schedule if needed**: Create time block with `todo_ref: "[[TODO-XXX]]"`

### Moving Task to DOING

1. **Check WIP limit**: Count current DOING tasks (must be <3)
2. **Update TODO file**: `status: in-progress`
3. **Update Kanban card**: Change `[ ]` to `[/]`
4. **Verify**: Card appears in DOING column

### Completing a Task

1. **Update time block**: `completed: true`
2. **Update TODO file**:
   - `status: done`
   - `completed_date: YYYY-MM-DD`
   - `actual_hours: <time spent>`
3. **Update Kanban card**: Change to `[x]`
4. **Verify**: Card appears in DONE column

### Deferring a Task

1. **Update TODO file**:
   - `status: deferred`
   - Add note explaining reason
   - Update `due_date` if known
2. **Update Kanban card**: Change to `[-]`
3. **Verify**: Card appears in CARPARK column

### Weekly Review Process

1. **Calculate metrics**:
   - Billable hours (sum BILLABLE time blocks)
   - Tasks completed (count DONE this week)
   - OKR coverage (count OKRs with activity)
2. **Identify issues**:
   - Overdue tasks
   - OKR gaps
   - Status sync errors
3. **Plan next week**:
   - Set priorities
   - Schedule billable blocks
   - Fill OKR gaps

---

## Dataview Queries

### Find Overdue Tasks

```dataview
TABLE due_date, priority, activity_type, estimated_hours
FROM "user-productivity/backlog"
WHERE status != "done" AND status != "cancelled" AND due_date < date(today)
SORT due_date ASC
```

### Tasks by OKR

```dataview
TABLE status, priority, due_date, estimated_hours
FROM "user-productivity/backlog"
WHERE okr = "DL-KR6"
SORT priority DESC, due_date ASC
```

### This Week's Time Blocks

```dataview
TABLE date, startTime, endTime, activity_type, completed
FROM "user-productivity/weekly-planner"
WHERE date >= date(today) - dur(7 days) AND date <= date(today)
SORT date ASC, startTime ASC
```

### Billable Hours This Week

```dataview
TABLE date, title, startTime, endTime
FROM "user-productivity/weekly-planner/billable"
WHERE date >= date(today) - dur(7 days)
SORT date ASC
```

---

## Troubleshooting

### Task Not Appearing on Kanban

**Possible causes**:

1. File not in `backlog/` folder
2. Wikilink syntax incorrect
3. Obsidian needs refresh

**Fix**:

1. Verify file location
2. Check wikilink: `[[TODO-XXX]]` (e.g., `[[TODO-039]]`)
3. Reload Obsidian (Cmd+P → "Reload app")

### Time Block Not on Calendar

**Possible causes**:

1. File not in correct calendar folder
2. Frontmatter syntax error
3. Date format incorrect

**Fix**:

1. Verify folder: `weekly-planner/{billable|okr-ops|initiatives|personal}/`
2. Check YAML syntax (proper indentation, quotes)
3. Verify date format: `YYYY-MM-DD`

### Status Not Syncing

**Possible causes**:

1. Status value not in allowed list
2. Extra spaces in status value
3. Kanban plugin needs refresh

**Fix**:

1. Use exact values: `todo`, `in-progress`, `done`, etc.
2. Remove extra spaces: `status: todo` (not `status:  todo`)
3. Refresh Kanban board

---

## Best Practices

### Daily Habits

1. **Morning**: Check today's time blocks, review priorities
2. **During work**: Update `actual_hours` as you work
3. **End of day**: Mark completed blocks, update TODO progress

### Weekly Habits

1. **Monday**: Week planning, set priorities, schedule billable
2. **Wednesday**: Mid-week check, adjust if needed
3. **Friday**: Week review, calculate metrics, plan next week

### Monthly Habits

1. **First week**: Monthly review, OKR progress assessment
2. **Last week**: Prepare next month's priorities

### System Maintenance

1. **Weekly**: Clear completed tasks older than 2 weeks
2. **Monthly**: Archive old reviews, clean up CARPARK
3. **Quarterly**: Full system audit, process improvements

---

## Resources

The following templates are owned by this skill and located in `resources/`:

| Resource                    | Purpose                                              | Origin                                  |
| --------------------------- | ---------------------------------------------------- | --------------------------------------- |
| `personal-todo-template.md` | Obsidian Templater-compatible personal TODO template | Migrated from `docs-copper/_templates/` |
| `time-block-template.md`    | Obsidian Templater-compatible time-block template    | Migrated from `docs-copper/_templates/` |

## Related Skills

- **@\${CLAUDE_PLUGIN_ROOT}/skills/kanban-board-management/SKILL.md**: Detailed Kanban operations
- **@\${CLAUDE_PLUGIN_ROOT}/skills/gtd-notation/SKILL.md**: Task Genius notation
- **Organisation identity-kit**: the organisation's values integration

---

## Related Memories (Serena MCP)

- **productivity-system-v1.1**: Complete system overview
- **kanban-board-management**: Kanban workflows
- **okr-operations**: OKR tracking guidelines
