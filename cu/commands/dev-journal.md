---
description: Generate a dev-journal entry for the current or recent working session
---

> **Documentation root (TD-178)**: paths below are written against the default `docs-copper/`. A
> project whose documentation lives elsewhere (for example `docs/`) is discovered automatically by
> the guard scripts, or pinned with `COPPER_DOCS_ROOT`. Read `docs-copper/` here as "the
> documentation root", not as a literal path.

# /cu:dev-journal

Create a development journal entry for: **$ARGUMENTS**

If no arguments provided, generate an entry for the current session based on conversation context.

---

## Phase 1: Gather Context

Before writing the entry, collect information from available sources:

1. **Session Context**:

   - Review the current conversation for work done, decisions made, and problems solved
   - Check `docs-copper/memory-bank/activeContext.md` for current work focus
   - Check `docs-copper/memory-bank/progress.md` for recent milestones

2. **Git Context**:

   - Run `git status` and `git diff --staged --stat` to identify changed files
   - Run `git log --oneline -5` to check recent commits
   - Use file changes to reconstruct what was worked on

3. **Determine Entry Scope**:
   - Single session (daily entry)
   - Multi-session (feature or milestone entry)
   - Weekly summary

---

## Phase 2: Determine File Path

Use the naming convention from the template:

```
docs-copper/dev-journal/YYYY/MM/YYYY-MM-DD-topic-slug.md
```

- Create year and month folders if they do not exist
- Use a short, hyphenated slug describing the focus area
- Examples:
  - `2026-04-30-genericisation-docs-copper.md`
  - `2026-05-02-api-authentication-spike.md`
  - `2026-05-05-bug-fix-currency-formatting.md`

---

## Phase 3: Generate the Entry

Load the `cu:dev-journal-management` skill to obtain the journal template and authoring guidance. The
skill resource at `${CLAUDE_PLUGIN_ROOT}/skills/dev-journal-management/resources/dev-journal-template.md`
provides the structural baseline.

**Skill invocation**: `skill({ name: "dev-journal-management" })`

The skill defines frontmatter conventions, section structure, quality standards, and the boundary
with related skills (productivity-system-management, memory bank).

### Content Guidelines

1. **YAML Frontmatter**:

   - `entry_date`: today's date in YYYY-MM-DD format
   - `author`: resolve from the current active user using this order of precedence:
     1. explicit live session context, including the user identity stated in the conversation or
        otherwise made available during the current session
     2. active configured user in `00-the-user.rules.md`
     3. active configured user in `AGENTS.md`
     4. if exactly one real user is resolvable from available context, use that user
     5. if multiple plausible users exist and the active user cannot be resolved confidently, ask
        the user
     6. only use `'[TO BE CONFIGURED]'` if no active user can be resolved from live or configured
        context
   - `focus_area`: brief description of the session's main focus
   - `status`: `draft`, `in-progress`, or `completed`
   - `session_duration`: estimate if known
   - `tags`: relevant keywords as an array
   - `version`: use `1.0.0` for a new entry, then increment when materially revising the same entry
   - `last_updated`: date of the latest meaningful revision in YYYY-MM-DD format
   - do NOT add a `changelog:` key: US-339 externalised change history to the per-kit
     `CHANGELOG.md`, Rule 04 forbids an inline `changelog:` frontmatter key, and the
     markdown-governance gate rejects one. The skill's template carries none and neither must a
     generated entry (TD-178)
   - `maintained_by`: use `'Lucas Challamel'`

   Minimum generated frontmatter:

   ```yaml
   ---
   entry_date: YYYY-MM-DD
   author: 'Resolved from live session context'
   focus_area: ''
   status: draft
   session_duration: ''
   tags: []
   version: '1.0.0'
   last_updated: 'YYYY-MM-DD'
   maintained_by: 'Lucas Challamel'
   ---
   ```

2. **Why Section**:

   - What prompted this work? What goal or problem?
   - Link to related user stories, ADRs, or sprint items if applicable

3. **How Section**:

   - Describe the journey: problem, investigation, breakthrough, implementation
   - Include dead ends and failed approaches (valuable learning)
   - Reference specific files changed and principle codes applied
   - Be honest about what worked and what did not

4. **Final State & Next Steps**:

   - What is the state of the codebase now?
   - What remains to be done?
   - What knowledge should be preserved?

5. **Reflection** (optional but encouraged):
   - What went well, what could improve, skills developed

### Quality Standards

- Write in past tense for completed work, present tense for current state
- Be specific: reference file paths, line numbers, tool names
- Keep the "Session Summary" to one sentence
- Remove the template usage guidelines callout from the final entry
- Do NOT include emojis unless the user explicitly requests them
- Keep lifecycle history in YAML frontmatter only; do not duplicate it in the body
- Never hardcode a personal name in the command itself; always resolve `author` from live session
  context first, then configured framework context
- Never leave `author` as a placeholder if an active user can be resolved confidently

---

## Phase 4: Post-Creation Actions

After writing the entry:

1. **Stage the file**:

   ```bash
   git add docs-copper/dev-journal/YYYY/MM/YYYY-MM-DD-topic-slug.md
   ```

2. **Offer to update memory bank**:

   - If significant work was captured, suggest running `/cu:memory-update`
   - If `activeContext.md` is stale, offer to refresh it

3. **Report**:
   - Confirm the file path created
   - Show a one-line summary of the entry
   - List any suggested follow-up actions

---

## Example Usage

```bash
# Generate entry from current session context
/cu:dev-journal

# Generate entry with a specific topic
/cu:dev-journal API authentication spike completed

# Generate entry for a specific date
/cu:dev-journal 2026-04-28 sprint planning session

# Generate a weekly summary
/cu:dev-journal weekly summary for sprint 3
```

---

## Cross-References

- **Skill**: `cu:dev-journal-management` (owns template resource and authoring method)
- **Storage**: `docs-copper/dev-journal/YYYY/MM/`
- **Memory Bank**: `docs-copper/memory-bank/` (update after significant entries)
- **Rule**: `04-project-documentation.rules.md` (documentation standards)

---
