---
description: Generate a dev-journal entry for the current or recent working session.
---

# /dev-journal

Create a development journal entry for: **$ARGUMENTS**

If no arguments are provided, generate an entry for the current session based on conversation
context.

## Phase 1: Gather Context

1. Review the current conversation for work done, decisions made, and problems solved.
2. Check `docs-copper/memory-bank/activeContext.md` and `docs-copper/memory-bank/progress.md`.
3. Run `git status`, `git diff --staged --stat`, and `git log --oneline -5`.

## Phase 2: Determine File Path

```
docs-copper/dev-journal/YYYY/MM/YYYY-MM-DD-topic-slug.md
```

Create year and month folders if they do not exist. Use a short hyphenated slug.

## Phase 3: Generate the Entry

Use the `cu:dev-journal-management` skill.

The skill defines frontmatter conventions, section structure, and quality standards. Resolve the
`author` from live session context first, then configured framework context.

## Phase 4: Post-Creation Actions

1. Stage the file: `git add docs-copper/dev-journal/YYYY/MM/YYYY-MM-DD-topic-slug.md`
2. If significant work was captured, suggest running /cu:memory-update.
3. Report the created path and a one-line summary.

## Example Usage

```
/cu-delivery-pipeline:dev-journal
/cu-delivery-pipeline:dev-journal API authentication spike completed
```

## Cross-References

- Skill: `cu:dev-journal-management`
- Storage: `docs-copper/dev-journal/YYYY/MM/`
- Related command: /cu:memory-update
