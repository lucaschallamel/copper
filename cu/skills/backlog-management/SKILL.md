---
name: backlog-management
description: Create, review, and validate backlog items using structured templates and story-type guidance. Provides the user story template, eight story-type guidance files, and three Python validation scripts as skill resources, plus a story-type selection guide for choosing the right backlog item format. Use when authoring user stories, epics, bugs, technical debt items, security items, spikes, CI items, or risk actions.
version: 1.1.2
last_updated: '2026-11-02'
maintained_by: Lucas Challamel
applies_to: 'Primary: any agent or command creating or reviewing backlog items | Secondary: sprint planning, backlog grooming, story kickoffs'
---

# Skill: Backlog Management

## Purpose

This skill provides the reusable capability for creating and managing structured backlog items. It
owns the user story template and all story-type guidance files, defines the authoring method for
each backlog item type, and documents the boundary with related skills.

## Capability Contract

**What this skill provides**:

- A structured user story template (`resources/user-story-template.md`) for backlog item authoring
- Eight story-type guidance files (`resources/story-types/`) covering EP, US, BUG, TD, SEC, SP, CI,
  and RA item types
- A story-type selection guide (see below) for choosing the correct backlog item format
- Three Python validation scripts (`scripts/`) for structural quality enforcement (see Scripts
  section)
- Authoring conventions: frontmatter standards, section structure, quality expectations

**What this skill does NOT provide**:

- Task-level GTD notation (see `cu:gtd-notation`)
- Kanban board management (see `cu:kanban-board-management`)
- Sprint planning or retrospective templates (see `cu:sprint-delivery` after migration)
- Definition of Done criteria (see `cu:framework-authoring` after migration under US-114)
- Validation scripts are owned by this skill (see Scripts section below)

---

## Story-Type Selection Guide

Use the following decision table to select the correct backlog item type:

| If the item...                                                       | Then use                   | Prefix | Guidance File                           |
| -------------------------------------------------------------------- | -------------------------- | ------ | --------------------------------------- |
| Delivers a discrete user-facing or system capability                 | **User Story**             | `US`   | `US-user-story-guidance.md`             |
| Groups related user stories under a shared business objective        | **Epic**                   | `EP`   | `EP-epic-guidance.md`                   |
| Fixes incorrect behaviour in an existing capability                  | **Bug/Defect**             | `BUG`  | `BUG-defect-guidance.md`                |
| Addresses technical debt or code quality improvement                 | **Technical Debt**         | `TD`   | `TD-technical-debt-guidance.md`         |
| Addresses a security vulnerability or compliance gap                 | **Security**               | `SEC`  | `SEC-security-guidance.md`              |
| Requires investigation before committing to implementation           | **Spike**                  | `SP`   | `SP-spike-guidance.md`                  |
| Improves a process, tool, or practice without changing functionality | **Continuous Improvement** | `CI`   | `CI-continuous-improvement-guidance.md` |
| Mitigates an identified risk or tracks a risk response action        | **Risk Action**            | `RA`   | `RA-risk-action-guidance.md`            |

### Selection Heuristics

1. **Start with the outcome**: Is the result a new capability (US), a fix (BUG), or an investigation
   (SP)?
2. **Check scope**: Does the item span multiple stories (EP) or stand alone?
3. **Consider urgency**: Security items (SEC) and risk actions (RA) often have time sensitivity.
4. **Validate against existing items**: Avoid duplicating items already in the backlog.

---

## Authoring Method

### When to Create a Backlog Item

- During backlog grooming or sprint planning sessions
- When a new requirement, bug, or risk is identified
- When technical debt accumulates to the point of needing a plan
- When an investigation is needed before committing to implementation

### File Naming Convention

```
docs-copper/roadmap/backlog/<PREFIX>-<NNN>-<short-description>.md
```

- Use the prefix from the selection guide above (US, EP, BUG, TD, SEC, SP, CI, RA)
- Use sequential numbering within each prefix (US-110, US-111, etc.)
- Use kebab-case for the short description

### Template Usage

For **user stories**, use `resources/user-story-template.md` as the structural baseline. The
template provides:

1. **YAML Frontmatter**: story_id, story_type, title, epic, priority, story_points, status,
   assignee, author, created, last_modified
2. **Progress Updates Callout**: collapsed block for chronological progress tracking
3. **Story Overview**: context and architecture alignment
4. **User Story Statement**: As a... I want... So that...
5. **Acceptance Criteria**: functional and non-functional requirements with checkboxes
6. **Technical Requirements**: implementation artefact paths
7. **Dependencies**: prerequisites with checkboxes

For other item types, follow the guidance in the corresponding story-type file.

### Frontmatter Standards

- `status` values: `Draft`, `Ready`, `In Progress`, `Done`, `Blocked`, `Cancelled` , the canonical
  set defined ONCE in `tools/status-vocabulary.json` and loaded by both `user-story-validator.py`
  and `pipeline_validator.py` (TD-171 AC3); never widen it here without changing the vocabulary file

### The Draft -> Ready bar

A card is **Ready** when all three hold. Until this was written down (2026-09-20) no transition
criteria existed anywhere, so `Draft` did not mean _"not groomed"_ , it meant _"nobody typed
Ready"_. Measured at the time: **45 of 47 Drafts already carried acceptance criteria** and 33 had
every dependency satisfied, while exactly **one** story was actionable. The constraint was a status
field nobody maintained, not grooming capacity.

1. **Dependencies satisfied** , every `depends_on` target is `Done` or `Cancelled`.
2. **A contract exists** , a non-empty `## Acceptance Criteria` section. A card without one cannot
   be finished, only abandoned.
3. **Not parked** , no `PARKED`, `NO-GO` or `DO NOT PULL` marker, and no `unblocks_if:` field.

All three are machine-checkable, and `dependency-resolver.py` computes them: its **Ready now**
section marks each card `ACTIONABLE`, `MEETS THE READY BAR` (promotable with a one-word status
edit), or names the specific condition that fails. Promotion stays a human act , the resolver says
what _could_ be promoted, never what _should_ be.

- `story_type` values: `user_story`, `epic`, `bug`, `technical_debt`, `security`, `spike`,
  `continuous_improvement`, `risk_action`
- Always include `created` and `last_modified` dates in `YYYY-MM-DD` format

### Quality Standards

- Write acceptance criteria that are objectively verifiable
- Reference specific file paths in technical requirements
- Tag decisions with principle codes where applicable
- Keep progress updates in reverse chronological order
- Use collapsed callout format for progress updates

---

## Operating Model

### Current State

- Backlog authoring uses `${CLAUDE_PLUGIN_ROOT}/skills/backlog-management/resources/user-story-template.md`
  directly
- Story-type guidance is accessed from `${CLAUDE_PLUGIN_ROOT}/skills/backlog-management/resources/story-types/`
- All backlog authoring flows through this skill

### Interactive Use

Agents or users may load this skill directly when:

- Creating a new backlog item and needing the right template
- Choosing between story types for a new work item
- Reviewing existing backlog items for structural quality
- Understanding story-type conventions during backlog grooming

---

## Boundary with Related Skills

### gtd-notation

**Overlap zone**: Both skills deal with actionable items.

**Boundary**:

- `cu:backlog-management` owns **structured backlog item creation** with full templates and type
  guidance
- `cu:gtd-notation` owns **task-level status tracking** using the 8-character checkbox notation
- Backlog items contain tasks (using GTD notation), but this skill does not define GTD syntax

### kanban-board-management

**Overlap zone**: Both skills touch backlog visualisation.

**Boundary**:

- `cu:backlog-management` owns **backlog item content and structure**
- `cu:kanban-board-management` owns **board column layout and card-to-column mapping**
- A backlog item appears on a Kanban card, but this skill does not manage board layout

### dev-journal-management

**Overlap zone**: Both skills capture session-level knowledge.

**Boundary**:

- `cu:backlog-management` owns **planned work items** (forward-looking)
- `cu:dev-journal-management` owns **session narratives** (retrospective)
- Journal entries may reference backlog items, but this skill does not generate journal entries

### sprint-delivery (future US-111)

**Overlap zone**: Both skills relate to sprint execution.

**Boundary**:

- `cu:backlog-management` owns **backlog item authoring** (what goes into the backlog)
- `cu:sprint-delivery` will own **sprint planning and retrospective templates** (how sprints are
  managed)

---

## Resources

| Resource                  | Location                                                      | Purpose                                              |
| ------------------------- | ------------------------------------------------------------- | ---------------------------------------------------- |
| User story template       | `resources/user-story-template.md`                            | Structural baseline for user stories                 |
| Story-type guidance (EP)  | `resources/story-types/EP-epic-guidance.md`                   | Epic authoring guidance                              |
| Story-type guidance (US)  | `resources/story-types/US-user-story-guidance.md`             | User story authoring guidance                        |
| Story-type guidance (BUG) | `resources/story-types/BUG-defect-guidance.md`                | Bug/defect authoring guidance                        |
| Story-type guidance (TD)  | `resources/story-types/TD-technical-debt-guidance.md`         | Technical debt authoring guidance                    |
| Story-type guidance (SEC) | `resources/story-types/SEC-security-guidance.md`              | Security item authoring guidance                     |
| Story-type guidance (SP)  | `resources/story-types/SP-spike-guidance.md`                  | Spike authoring guidance                             |
| Story-type guidance (CI)  | `resources/story-types/CI-continuous-improvement-guidance.md` | CI item authoring guidance                           |
| Story-type guidance (RA)  | `resources/story-types/RA-risk-action-guidance.md`            | Risk action authoring guidance                       |
| Story-type index          | `resources/story-types/README.md`                             | Index and conventions for all story types            |
| User story validator      | `scripts/user-story-validator.py`                             | Validates backlog stories against structural rules   |
| Epic validator            | `scripts/epic-validator.py`                                   | Epic structure; counters recounted from the children |
| Progress block autofix    | `scripts/progress-block-autofix.py`                           | Inserts or normalises required progress block        |
| Scripts README            | `scripts/README.md`                                           | Validator usage and exit code documentation          |

---

## Architecture Alignment

- **ADR-009**: Follows the three-tier skill content model (stable guidance in SKILL.md, reusable
  templates in resources/, operational scripts in scripts/, no volatile external content)
- **ADR-010**: This skill is the target owner for user-story-template.md, story-type guidance files,
  and validation scripts migrated from `docs-copper/_templates/` (physical deletion completed under
  US-117)
- **ADR-007**: Pipeline state files (YAML) in `docs-copper/roadmap/pipeline-audit-trail/` are
  managed per the story delivery pipeline

---

## Scripts

This skill owns three Python validation scripts located in `scripts/`. They enforce structural
quality rules on backlog items and are invoked by both the local test suite and the CI pipeline.

### Script Inventory

| Script                      | Purpose                                                                                                         | Invocation                                         |
| --------------------------- | --------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `user-story-validator.py`   | Validates backlog stories (US, TD, CI, SP, SEC, RA) against frontmatter, progress-block, and body-section rules | `python3 scripts/user-story-validator.py <path>`   |
| `epic-validator.py`         | Validates epic structure; recounts stated counters and checks the epic status against its children (TD-202)     | `python3 scripts/epic-validator.py <path>`         |
| `progress-block-autofix.py` | Inserts or normalises the required collapsible progress block in supported story files                          | `python3 scripts/progress-block-autofix.py <path>` |

### Exit Codes

All scripts follow a shared convention:

| Code | Meaning                                       |
| ---- | --------------------------------------------- |
| `0`  | All files pass validation                     |
| `1`  | One or more files failed validation           |
| `2`  | Usage error (missing arguments, invalid path) |

### CI Integration

The `.gitlab-ci.yml` pipeline invokes `user-story-validator.py` on every push to validate all
backlog items in `docs-copper/roadmap/backlog/`.

### Test Integration

The `validators_dir` pytest fixture in `tests/conftest.py` resolves to `scripts/` within this skill,
ensuring unit and functional tests execute the same validator code as CI.

---

## Cross-References

- **Storage**: `docs-copper/roadmap/backlog/`
- **Pipeline**: `docs-copper/roadmap/pipeline-audit-trail/` (per `/cu:pipe`)
- **Related Skill**: `cu:gtd-notation` (task status notation)
- **Related Skill**: `cu:kanban-board-management` (board layout and card mapping)
- **Related Skill**: `cu:dev-journal-management` (session capture)
- **Rule**: `04-project-documentation.rules.md` (documentation standards)
- **Skill Resources**: `${CLAUDE_PLUGIN_ROOT}/skills/backlog-management/resources/` (migrated from
  `docs-copper/_templates/` under EP-101)
