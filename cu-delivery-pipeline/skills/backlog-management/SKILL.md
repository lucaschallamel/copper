---
name: backlog-management
type: skill
description: 'Create, review, and validate backlog items using structured templates and story-type guidance. Provides the user story template, eight story-type guidance files, and three validation scripts as skill resources, plus a story-type selection guide. Use when authoring user stories, epics, bugs, technical debt items, security items, spikes, CI items, or risk actions.

  '
version: 1.1.0
tags:
- delivery
- governance
- backlog
capabilities:
  needs:
  - file-read
  - file-edit
  optional:
  - shell
  permission:
    file-edit: confirm
    shell: confirm
requires:
  skills:
  - gtd-notation
maintained_by: Lucas Challamel
last_updated: '2026-06-05'
---

# Skill: Backlog Management

## Purpose

This skill provides the reusable capability for creating and managing structured backlog items. It
owns the user story template and all story-type guidance files, defines the authoring method for
each backlog item type, and documents the boundary with related skills.

## Capability Contract

**Provides**: a structured user story template (`resources/user-story-template.md`), eight
story-type guidance files (`resources/story-types/`), a story-type selection guide, and three
validation scripts (`scripts/`).

**Does NOT provide**: task-level GTD notation (see `cu:gtd-notation`), Kanban board management
(see `cu:kanban-board-management`), or sprint planning (see `cu:sprint-delivery`).

## Story-Type Selection Guide

| If the item...                                                | Then use       | Prefix | Guidance File                   |
| ------------------------------------------------------------- | -------------- | ------ | ------------------------------- |
| Delivers a discrete user-facing or system capability          | User Story     | `US`   | `US-user-story-guidance.md`     |
| Groups related user stories under a shared business objective | Epic           | `EP`   | `EP-epic-guidance.md`           |
| Fixes incorrect behaviour in an existing capability           | Bug/Defect     | `BUG`  | `BUG-defect-guidance.md`        |
| Addresses technical debt or code quality                      | Technical Debt | `TD`   | `TD-technical-debt-guidance.md` |

## Authoring Method

1. Select the item type using the guide above.
2. Read the matching guidance file in `resources/story-types/`.
3. Start from `resources/user-story-template.md`.
4. Write the item into `docs-copper/roadmap/backlog/`.
5. Validate with the scripts in `scripts/` before committing.

## Resources

- `resources/user-story-template.md` - the canonical backlog item template
- `resources/story-types/*.md` - per-type authoring guidance
- `scripts/` - structural validation utilities

## Cross-References

- Storage: `docs-copper/roadmap/backlog/`
- Related skills: `cu:gtd-notation`, `cu:sprint-delivery`,
  `cu:kanban-board-management`
