---
todo_id: TODO-{{date:YYYY-MM-DD}}-NNN
title: ''
status: todo
priority: medium
activity_type: ''
okr: ''
assigned_to: Lucas Challamel
delegated_to: ''
created_date: { { date:YYYY-MM-DD } }
due_date: ''
estimated_hours: 0
actual_hours: 0
depends_on: []
blocks: []
completed_date: ''
tags:
  - personal
  - itg-2026
---

> [!note]- Progress Updates **{{date:YYYY-MM-DD}}** - Task created.

# {{title}}

## 📋 Description

[What needs to be done]

## 🎯 Objective

**Success Criteria**:

- [ ] [Criterion 1]
- [ ] [Criterion 2]

## 📊 Context

| Field             | Value                                                                                                             |
| ----------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Activity Type** | `BILLABLE` / `ITG-DEV` / `SE-SUPP` / `STRAT-AM` / `BENCH` / `PEOPLE` / `COMM` / `AI-TRANS` / `ADMIN` / `PERSONAL` |
| **OKR**           | BL-O2 / DL-KR1 / DL-KR2 / DL-KR3 / DL-KR4 / DL-KR5 / DL-KR6 / N/A                                                 |
| **Priority**      | Critical / High / Medium / Low                                                                                    |
| **Estimated**     | X hours                                                                                                           |

## 📅 Timeline

- **Created**: {{date:YYYY-MM-DD}}
- **Due**:
- **Completed**:

## 🔗 Dependencies

**Depends On**:

- **Blocks**:

-

## 📅 Scheduled Time Blocks

<!-- Dataview query to find linked time blocks -->

```dataview
TABLE date as "Date", startTime as "Start", endTime as "End", status as "Status"
FROM "lucas-productivity/weekly-planner"
WHERE contains(todo_ref, this.file.name)
SORT date ASC
```

## ✅ Completion

**Actual Effort**: X hours

**Summary**: [What was accomplished]

**Next Actions**:

- ***

> [!info]- Field Reference
>
> **Status Values:**
>
> | Status        | Kanban Column | Meaning               |
> | ------------- | ------------- | --------------------- |
> | `todo`        | TODO          | Not started           |
> | `in-progress` | DOING         | Working on it         |
> | `done`        | DONE          | Completed             |
> | `blocked`     | CARPARK       | Blocked by dependency |
> | `cancelled`   | CARPARK       | No longer needed      |
> | `deferred`    | CARPARK       | Postponed             |
>
> **Activity Types:**
>
> | Code       | Activity            | OKR Link |
> | ---------- | ------------------- | -------- |
> | `BILLABLE` | Client Delivery     | DL-KR6   |
> | `ITG-DEV`  | IT Governance Dev   | DL-KR1   |
> | `SE-SUPP`  | SE Team Support     | DL-KR2   |
> | `STRAT-AM` | Strategic Accounts  | DL-KR3   |
> | `BENCH`    | Bench-to-Bill       | DL-KR4   |
> | `PEOPLE`   | People & Engagement | DL-KR5   |
> | `COMM`     | Commercial          | DL-KR6   |
> | `AI-TRANS` | AI Transformation   | BL-O2    |
> | `ADMIN`    | Administrative      | N/A      |
> | `PERSONAL` | Personal Dev        | N/A      |
