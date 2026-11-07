---
name: sprint-delivery
version: 1.0.0
last_updated: '2026-05-11'
maintained_by: Lucas Challamel
description: 'Sprint planning, retrospectives, and board creation grouped under one operational skill. Provides templates for sprint artefact generation following a consistent command-driven model.

  '
instructions: 'Use this skill when creating sprint plans, running retrospectives, or setting up Kanban boards

  for sprint delivery. Load the appropriate resource template based on the sprint artefact needed.


  For sprint planning: load resources/sprint-planning-template.md

  For sprint retrospectives: load resources/sprint-retrospective-template.md

  For Kanban boards: invoke kanban-board-management skill (separate concern)


  Sprint authoring (this skill) handles sprint lifecycle documentation.

  Kanban semantics (kanban-board-management skill) handles board column model and status mapping.

  '
applies_to:
- agents
- commands
---

# Sprint Delivery Skill

Sprint planning, retrospectives, and board creation for COPPER framework delivery.

## Purpose

This skill provides a single operational home for sprint artefact generation. Sprint plans,
retrospectives, and board setup follow one consistent command-driven model, ensuring traceability
and quality across the sprint lifecycle.

## Resources

| Resource                           | Purpose                                              | Format                         |
| ---------------------------------- | ---------------------------------------------------- | ------------------------------ |
| `sprint-planning-template.md`      | Sprint plan with goals, capacity, backlog, and risks | Markdown with YAML frontmatter |
| `sprint-retrospective-template.md` | Retrospective with formats, actions, and metrics     | Markdown with YAML frontmatter |

## Usage

### Sprint Planning

1. Load `resources/sprint-planning-template.md`
2. Replace placeholder values in YAML frontmatter (sprint_id, dates, team)
3. Populate sprint goal, user stories, and capacity
4. Define definition of done and risk register
5. Save to `docs-copper/roadmap/sprint-NNN/`

### Sprint Retrospective

1. Load `resources/sprint-retrospective-template.md`
2. Replace placeholder values (sprint_id, date, participants)
3. Choose retrospective format (start-stop-continue, 4Ls, mad-sad-glad, timeline)
4. Capture what went well, what to improve, and action items
5. Save to `docs-copper/roadmap/sprint-NNN/`

### Kanban Board Creation

For Kanban board setup, use the `cu:kanban-board-management` skill, which owns the board template and
4-column model (TODO, DOING, DONE, CARPARK). This skill references it for board creation during
sprint setup but does not duplicate board semantics.

## Sprint Artefact Selection Guide

| Need                 | Use                                | Owned By                |
| -------------------- | ---------------------------------- | ----------------------- |
| Sprint plan          | `sprint-planning-template.md`      | sprint-delivery         |
| Sprint retrospective | `sprint-retrospective-template.md` | sprint-delivery         |
| Kanban board         | `kanban-board-template.md`         | kanban-board-management |
| User story           | `user-story-template.md`           | backlog-management      |
| Story-type guidance  | `resources/story-types/`           | backlog-management      |
| Dev journal          | `dev-journal-template.md`          | dev-journal-management  |

## Boundary: kanban-board-management

**This skill (sprint-delivery)**: Sprint lifecycle documentation - planning, capacity, goals,
retrospectives, action items.

**kanban-board-management skill**: Kanban board semantics - 4-column model (TODO, DOING, DONE,
CARPARK), status-to-column mapping, board synchronisation with TODO notes.

**Relationship**: Sprint-delivery creates the sprint context (goals, stories, timeline).
Kanban-board-management creates the visual board. During sprint setup, both skills cooperate:
sprint-delivery defines what to deliver; kanban-board-management tracks delivery status.

**Template ownership**: `kanban-board-template.md` lives in the kanban-board-management skill as a
resource. Sprint-delivery references it but does not own it.

## Boundary: backlog-management

**sprint-delivery**: Manages the sprint container (plan, retrospective, timeline).

**backlog-management**: Manages individual work items (user stories, bugs, spikes) that go into
sprints.

**Relationship**: backlog-management creates the items; sprint-delivery organises them into sprints.

## Boundary: dev-journal-management

**sprint-delivery**: Formal sprint artefacts (planning, retrospective).

**dev-journal-management**: Session-level development notes capturing work, decisions, and
learnings.

**Relationship**: Sprint retrospectives capture team-level insights. Dev journals capture individual
session notes. Both contribute to continuous improvement but at different granularity.

## Conventions

- Sprint folders: `docs-copper/roadmap/sprint-NNN/`
- Sprint numbering: 3-digit zero-padded (001, 002, etc.)
- Sprint duration: 2 weeks default (configurable in template)
- Retrospective formats: start-stop-continue (default), 4Ls, mad-sad-glad, timeline
- All dates in ISO format (YYYY-MM-DD)

## Related Skills

- `cu:backlog-management`: Work item creation and story-type guidance
- `cu:kanban-board-management`: Kanban board model and board template
- `cu:dev-journal-management`: Session-level development notes
- `cu:gtd-notation`: Task status notation for sprint tracking
