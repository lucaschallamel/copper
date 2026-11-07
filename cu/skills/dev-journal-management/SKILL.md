---
name: dev-journal-management
description: Create and manage development journal entries capturing session work, decisions, and learnings. Provides the journal template as a skill resource and documents the authoring method for interactive and command-driven workflows. Use when generating dev-journal entries, understanding journal structure, or guiding session-capture workflows.
version: 1.3.0
last_updated: '2026-09-10'
maintained_by: Lucas Challamel
applies_to: 'Primary: /cu:dev-journal command | Secondary: any agent capturing session context'
---

# Skill: Dev-Journal Management

## Purpose

This skill provides the reusable capability for creating development journal entries. It owns the
journal template, defines the authoring method, and documents the boundary with related skills.

## Capability Contract

**What this skill provides**:

- A structured journal template (`resources/dev-journal-template.md`) for session capture
- Authoring method: frontmatter conventions, section structure, quality standards
- Guidance for both interactive and command-driven journal creation

**What this skill does NOT provide**:

- Task or Kanban management (see `cu:productivity-system-management`)
- Sprint retrospective templates (see `cu:sprint-delivery` after migration)
- Memory bank update logic (see memory bank rules and `/cu:memory-update`)

---

## Authoring Method

### When to Create a Journal Entry

- End of significant development sessions
- After solving complex technical problems worth documenting
- Before context switching to capture current state
- Weekly sprint progress summaries
- Major milestone or breakthrough achievements

### File Path Convention

```
docs-copper/dev-journal/YYYY/MM/YYYY-MM-DD-topic-slug.md
```

- Create year and month folders if they do not exist
- Use a short, hyphenated slug describing the focus area

### Template

`resources/dev-journal-template.md` is the **prescribed structure for new entries**, not a loose
starting point (Rule 04: template compliance is mandatory). A new journal MUST carry the template's
top-level sections verbatim , `## Why (High-Level Context)`, `## How (The Journey)`,
`## Final State & Next Steps` , and SHOULD use the `### How` subsections (Initial Problem /
Investigation / Breakthrough / Implementation and Refinements / Validation and Documentation). Map
your content into these sections; do not substitute your own headings.

1. **YAML Frontmatter**: entry date, author, focus area, status, tags, version, last updated,
   maintained by. **No `changelog:` key** (US-339, TD-178): Rule 04 forbids it, git holds the
   history
2. **Why Section**: high-level context, session objectives, related work
3. **How Section**: the journey (problem, investigation, breakthrough, implementation)
4. **Final State & Next Steps**: current state, immediate actions, future considerations
5. **Reflection** (optional): what went well, what could improve, skills developed

Historical entries authored before this guidance are NOT retroactively conformed.

### Self-check (forward-only, ships with the skill)

`scripts/check-journal-conformance.py` validates new entries (dated >= the cutoff) against this
structure. Run it after authoring a journal:

```bash
uv run python ${CLAUDE_PLUGIN_ROOT}/skills/dev-journal-management/scripts/check-journal-conformance.py .
```

It skips historical (pre-cutoff) entries by design. This is the skill's self-contained quality suite
, it travels with the skill to every deployed harness.

### Frontmatter Resolution

The `author` field should be resolved using this order of precedence:

1. Explicit live session context (user identity stated in conversation)
2. Active configured user in `00-the-user.rules.md`
3. Active configured user in `AGENTS.md`
4. If exactly one real user is resolvable from context, use that user
5. If multiple plausible users exist and the active user cannot be resolved confidently, ask
6. Only use `'[TO BE CONFIGURED]'` if no active user can be resolved from any source

### Quality Standards

- Write in past tense for completed work, present tense for current state
- Be specific: reference file paths, tool names, principle codes
- Keep the session summary to one sentence
- Remove the template usage guidelines callout from generated entries
- Do not include emojis unless the user explicitly requests them
- Keep lifecycle history in YAML frontmatter only; do not duplicate it in the body
- Never hardcode a personal name in automation; always resolve from context

---

## Operating Model

### Current State (Post-US-115)

- `/cu:dev-journal` command invokes this skill for template loading and authoring guidance
- The legacy `_templates/dev-journal-template.md` reference has been removed from the command;
  physical deletion completed under US-117
- All journal creation logic flows through this skill

### Interactive Use

Agents or users may load this skill directly when:

- Understanding journal structure conventions
- Generating entries outside the `/cu:dev-journal` command flow
- Reviewing or auditing existing journal entries for quality

---

## Boundary with Related Skills

### productivity-system-management

**Overlap zone**: Both skills touch session-level capture.

**Boundary**:

- `cu:dev-journal-management` owns the **journal entry template and authoring method**
- `cu:productivity-system-management` owns the **Kanban board, calendar, and OKR workflows**
- Journal entries may reference Kanban cards or OKR items, but this skill does not manage them

### Memory Bank (Rule 03)

**Overlap zone**: Both capture session knowledge.

**Boundary**:

- `cu:dev-journal-management` captures **narrative session context** (why, how, what happened)
- Memory bank captures **persistent project context** (current state, patterns, tech stack)
- Journal entries may trigger memory bank updates, but this skill does not own the memory bank

---

## Resources

| Resource             | Location                            | Purpose                                 |
| -------------------- | ----------------------------------- | --------------------------------------- |
| Dev-journal template | `resources/dev-journal-template.md` | Structural baseline for journal entries |

---

## Architecture Alignment

- **ADR-009**: Follows the three-tier skill content model (stable guidance in SKILL.md, reusable
  template in resources/, no volatile external content)
- **ADR-010**: This skill is the target owner for the dev-journal template migration from
  `${CLAUDE_PLUGIN_ROOT}/skills/dev-journal-management/resources/` (migrated from `docs-copper/_templates/`
  under EP-101)
- **ADR-005**: Journal entries contribute to memory continuity alongside the memory bank

---

## Cross-References

- **Command**: `/cu:dev-journal` (current command surface, to be refactored under US-115)
- **Storage**: `docs-copper/dev-journal/YYYY/MM/`
- **Memory Bank**: `docs-copper/memory-bank/` (update after significant entries)
- **Rule**: `04-project-documentation.rules.md` (documentation standards)
- **Related Skill**: `cu:productivity-system-management` (Kanban, calendar, OKR workflows)
