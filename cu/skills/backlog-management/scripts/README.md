# Validation Scripts

Skill-owned validator scripts for template-driven backlog checks. This folder is the **permanent
home** for backlog validation; under `EP-101`, `US-109`, `US-116`, and `US-117` the validators were
migrated here from `docs-copper/_templates/us-validation/`.

## Contents

- `user-story-validator.py` , validates backlog stories and shared story rules (frontmatter,
  progress block, body sections).
- `epic-validator.py` , validates epic-specific structure and progress fields (incl. per-epic
  dependency DAG / no-cycles). Each epic's `child_stories` must match the cards whose `epic:` names
  it; stated counters are recounted from the children's `status:` (TD-202); the epic's own status
  must agree with them (not Draft once a child started, Done exactly when every child is closed).
  Exits 2 when `tools/status-vocabulary.json` cannot be read. Children are read from the cards in
  the epic's own folder, so epics live beside their cards.
- `dependency-resolver.py` , resolves the GLOBAL cross-epic dependency tree from every story's
  `depends_on:` frontmatter. Detects dangling deps + cycles, and emits the topological order, the
  unblock-the-most ranking, ready-now / near-ready lists, and a Mermaid overview to a generated
  `DEPENDENCIES.md`. Local only, deterministic , no external tools. Suffix-aware (`SP-103` vs
  `SP-103b` are distinct).
- `progress-block-autofix.py` , inserts or normalises the required collapsible progress block.
- `check-kanban-board.py` , the Kanban-board consistency gate: every live card is on the board, in
  the column its `status:` implies, and no Done or Cancelled card sits in an active column (wired
  into `ci:local` and CI as "kanban board").

## Usage

```bash
python3 user-story-validator.py "$BACKLOG/"
python3 epic-validator.py "$BACKLOG"/EP-*.md

# regenerate the dependency index (writes DEPENDENCIES.md):
python3 dependency-resolver.py "$BACKLOG" --out "$BACKLOG/DEPENDENCIES.md"
# CI gate , fails on dangling deps, cycles, or a stale or missing index:
python3 dependency-resolver.py "$BACKLOG" --check --out "$BACKLOG/DEPENDENCIES.md"
```

(`$BACKLOG` = `docs-copper/roadmap/backlog`)

## Enforced Progress Update Structure

The validators now enforce a **collapsible progress update block** for these backlog artefact types:

- `US` : user stories
- `EP` : epics
- `TD` : technical debt items
- `CI` : continuous improvement items
- `SP` : spikes

### Required Structure

Immediately after YAML frontmatter, supported files must begin with this pattern:

```markdown
> [!note]- Progress updates
>
> - **YYYY-MM-DD**: Earlier progress log entry
> - **YYYY-MM-DD**: Earlier progress log entry
```

### Validator Expectations

- header must be exactly: `> [!note]- Progress updates`
- a blank quoted separator line must exist after the header
- all progress entries must be quoted bullet lines
- dates must be plain, not wrapped in square brackets

### Body-Section Validation (Phase 5)

`user-story-validator.py` Phase 5 checks structural body sections for supported story types:

- an `## Acceptance Criteria` or `## Acceptance` section must be present
- it must carry at least one **labelled** criterion, `- [<glyph>] **ACn**` or `- [<glyph>] **SCn**`.
  Any of Rule 02c's eight Task Genius glyphs counts (` x / - > < ? !`), so a story whose criteria
  are all ticked still passes , BUG-010 fixed a rule that matched only the unchecked `- [ ]` box and
  so warned on every delivered story. The `**ACn**` label is what the check keys on; a bare
  `### AC1:` heading with a plain checkbox under it still warns.
- any `## Deliverables` or `## Follow-on Work` section must not contain unchecked items
- the story title must not reference a topic that has no matching acceptance criterion

### Autofix Support

Use the autofix utility to insert or normalise the required structure in supported story files:

```bash
python3 progress-block-autofix.py < backlog-folder > /
```

### Autofix Behaviour Notes

- the autofix utility is intended for supported story files only: `US`, `EP`, `TD`, `CI`, `SP`
- it removes leading blank lines after frontmatter before evaluating the progress block
- it normalises the header to:
  - `> [!note]- Progress updates`
- it normalises all progress entries to quoted bullet lines with plain dates, for example:
  - `> - **2026-05-05**: ...`
- it should be **idempotent**: re-running it on an already-correct file should not create duplicate
  progress blocks
- recommended usage pattern:
  1. run autofix on the target story or backlog folder
  2. run `user-story-validator.py` to confirm compliance

## Notes

- validators should stay generic unless a project-specific rule is explicitly required
- exit codes follow the shared `0`, `1`, `2` convention
- deeper validator behaviour belongs in script help text or dedicated documentation, not this folder
  README

## Related

- [[../SKILL.md]] - Backlog-management skill overview
- [[../resources/story-types/README.md]] - Story-type guidance
- [[../resources/user-story-template.md]] - User-story template
