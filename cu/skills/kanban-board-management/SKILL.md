---
name: kanban-board-management
description: Kanban board management skill for synchronising TODO notes with Obsidian Kanban boards. Defines the 4-column structure (TODO, DOING, DONE, CARPARK) and status-to-column mapping. Essential for Agile Coach and all agents managing project backlogs.
version: 1.1.1
last_updated: '2026-07-11'
maintained_by: Lucas Challamel
applies_to: 'All agents (primary: the agile-coaching / delivery-lead role)'
---

# Kanban Board Management - Status Mapping & Synchronisation

Complete reference for managing Obsidian Kanban boards and synchronising TODO note statuses with
Kanban columns.

**When to use this Skill**:

- Managing project backlogs (proposals, tenders, projects)
- Synchronising TODO notes with Kanban boards
- Updating task statuses and moving cards between columns
- Running standups, sprint reviews, or progress tracking
- Facilitating Kanban ceremonies (daily standups, flow reviews)

---

## 📋 Kanban Board Structure

### Standard 4-Column Layout

All project Kanban boards follow a consistent 4-column structure:

| Column      | Purpose            | Visual | Description                           |
| ----------- | ------------------ | ------ | ------------------------------------- |
| **TODO**    | Backlog            | 📋     | Tasks identified but not yet started  |
| **DOING**   | Work in Progress   | 🔄     | Tasks currently being worked on       |
| **DONE**    | Completed          | ✅     | Tasks successfully finished           |
| **CARPARK** | Deferred/Cancelled | 🅿️     | Tasks on hold, deferred, or cancelled |

---

## 🔄 Status-to-Column Mapping (CRITICAL)

### TODO Note Status → Kanban Column

This mapping defines how TODO note `status:` field values correspond to Kanban columns:

| TODO Status   | Kanban Column | Task Genius Icon | Description                                             |
| ------------- | ------------- | ---------------- | ------------------------------------------------------- |
| `todo`        | **TODO**      | `[ ]`            | Not started, in backlog                                 |
| `pending`     | **TODO**      | `[ ]`            | Awaiting prerequisites                                  |
| `scheduled`   | **TODO**      | `[<]`            | Scheduled for future date (stays in TODO until started) |
| `blocked`     | **CARPARK**   | `[?]`            | Blocked, awaiting resolution (parked until unblocked)   |
| `in-progress` | **DOING**     | `[/]`            | Currently being worked on                               |
| `in_progress` | **DOING**     | `[/]`            | Alternative format (underscore)                         |
| `active`      | **DOING**     | `[/]`            | Actively being worked on                                |
| `completed`   | **DONE**      | `[x]`            | Successfully finished                                   |
| `done`        | **DONE**      | `[x]`            | Alternative format                                      |
| `cancelled`   | **CARPARK**   | `[-]`            | No longer needed                                        |
| `deferred`    | **CARPARK**   | `[-]`            | Postponed indefinitely                                  |
| `on-hold`     | **CARPARK**   | `[-]`            | Temporarily suspended                                   |
| `delegated`   | **DOING**     | `[>]`            | Assigned to someone else (in progress)                  |

### Quick Reference Table

| TODO Column         | DOING Column          | DONE Column         | CARPARK             |
| ------------------- | --------------------- | ------------------- | ------------------- |
| `status: todo`      | `status: in-progress` | `status: completed` | `status: cancelled` |
| `status: pending`   | `status: active`      | `status: done`      | `status: deferred`  |
| `status: scheduled` | `status: delegated`   |                     | `status: on-hold`   |
|                     |                       |                     | `status: blocked`   |

---

## 📝 Kanban Board File Format

### Obsidian Kanban Plugin Format

Kanban boards use the Obsidian Kanban plugin format:

```markdown
---
kanban-plugin: board
---

## TODO

- [ ] [[TODO-003]]
- [ ] [[TODO-005]]

## DOING

- [/] [[TODO-039]]
- [/] [[TODO-038]]

## DONE

- [x] [[TODO-001]]
- [x] [[TODO-002]]

## CARPARK

- [-] [[TODO-050]]

%% kanban:settings
```

{"kanban-plugin":"board","list-collapse":[false,false,false,false],"lane-width":300}

```
%%
```

### Key Format Rules

1. **Column Headers**: Use `## COLUMN_NAME` (H2 headers)
2. **Card Format**: `- [X] [[TODO-XXX]]` where X is the Task Genius checkbox
3. **Filename Convention**: `TODO-XXX.md` (3-digit number only, title in frontmatter)
4. **Settings Block**: Keep the `%% kanban:settings %%` block at the end
5. **Order**: Cards are ordered top-to-bottom within each column

---

## 🔧 Synchronisation Procedures

### When TODO Status Changes → Update Kanban Board

**Procedure**:

1. **Identify status change** in TODO note frontmatter (`status:` field)
2. **Determine target column** using status-to-column mapping
3. **Move card** from current column to target column in Kanban board
4. **Verify consistency** between TODO status and Kanban position

### Example: Promoting TODO to DOING

**Before** (TODO note):

```yaml
status: todo
```

**After** (TODO note):

```yaml
status: in-progress
```

**Kanban Board Update**:

- Remove `- [ ] [[TODO-039]]` from `## TODO`
- Add `- [/] [[TODO-039]]` to `## DOING`

### Example: Completing a TODO

**Before** (TODO note):

```yaml
status: in-progress
```

**After** (TODO note):

```yaml
status: completed
completed_date: '2025-11-27'
```

**Kanban Board Update**:

- Remove card from `## DOING`
- Add card to `## DONE`

### Example: Cancelling/Deferring a TODO

**Before** (TODO note):

```yaml
status: todo
```

**After** (TODO note):

```yaml
status: cancelled
completion_notes: 'Requirement removed by client'
```

**Kanban Board Update**:

- Remove card from `## TODO`
- Add card to `## CARPARK`

---

## 📊 Kanban Metrics & Flow

### Work in Progress (WIP) Limits

**Recommended WIP Limits** (per person):

| Column  | WIP Limit | Rationale                       |
| ------- | --------- | ------------------------------- |
| TODO    | Unlimited | Backlog can grow                |
| DOING   | 2-3       | Focus, reduce context switching |
| DONE    | Unlimited | Completed work accumulates      |
| CARPARK | Unlimited | Deferred items park here        |

### Flow Metrics

**Cycle Time**: Time from DOING → DONE **Lead Time**: Time from TODO → DONE **Throughput**: Cards
completed per time period

### Daily Standup Questions (Kanban)

1. **What moved to DONE since yesterday?**
2. **What's blocked in DOING?**
3. **What should move from TODO to DOING today?**
4. **Anything to move to CARPARK?**

---

## 🎯 Agent Responsibilities

### The agile-coaching / delivery-lead role (Primary Owner)

- **Owns** Kanban board management and synchronisation
- **Facilitates** daily standups using Kanban board
- **Monitors** WIP limits and flow metrics
- **Updates** Kanban board during sprint ceremonies
- **Teaches** other agents the status-to-column mapping

### All Agents

- **Understand** the 4-column structure and status mapping
- **Update** TODO note status when task state changes
- **Request** Kanban board updates when promoting/completing tasks
- **Report** blockers that should move cards to CARPARK

---

## ✅ Validation Checklist

When updating Kanban boards, verify:

- [ ] TODO note `status:` field matches Kanban column
- [ ] Card appears in exactly ONE column (no duplicates)
- [ ] Completed tasks have `completed_date:` in frontmatter
- [ ] Cancelled/deferred tasks have `completion_notes:` explaining why
- [ ] DOING column respects WIP limits (2-3 per person)
- [ ] Progress updates section in TODO note reflects current state

---

## 🔗 Related Skills

- **gtd-notation**: Task Genius status characters (`[ ]`, `[x]`, `[/]`, etc.)
- **sprint-delivery**: Sprint planning, retrospectives, board creation
- **backlog-management**: User stories, backlog refinement, story-type selection

---

## Quick Reference Card

| Column         | Status Values                                                                 |
| -------------- | ----------------------------------------------------------------------------- |
| 📋 **TODO**    | `status: todo`, `status: pending`, `status: scheduled`                        |
| 🔄 **DOING**   | `status: in-progress`, `status: active`, `status: delegated`                  |
| ✅ **DONE**    | `status: completed`, `status: done`                                           |
| 🅿️ **CARPARK** | `status: cancelled`, `status: deferred`, `status: on-hold`, `status: blocked` |

> **Rules**: WIP Limit 2-3 cards in DOING per person. Always update TODO note status BEFORE moving
> Kanban card. Add progress update when changing status.
