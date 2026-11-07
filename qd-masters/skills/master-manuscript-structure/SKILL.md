---
name: master-manuscript-structure
description: Folder and document structure for long-form writing projects , the canon/working/research/archive authority separation, scene and chapter file conventions, and naming that survives a series. Use when setting up a new writing project, reorganising one that has sprawled, or deciding where a document belongs.
version: 1.0.0
last_updated: '2026-09-07'
maintained_by: Lucas Challamel
---

# Master Manuscript Structure (qd-master-manuscript-structure)

Reusable project-structure knowledge for long-form writing. This skill is the single source of truth
for the capability; the `qd-masters:master-manuscript-structure` command applies it to a project.

## Role Overview

A long writing project fails at the filesystem before it fails on the page. The recurring symptom is
not disorder , it is **ambiguous authority**: three documents describe the protagonist's age and
nothing says which one is true. Structure exists to make authority unambiguous.

## The Authority Separation

Four levels, and the whole scheme rests on them. A document's LOCATION declares its authority:

1. **Canon** , absolute authority. The story bible, character profiles, world rules, timeline.
   Change-controlled: edited deliberately, never in passing while drafting.
2. **Working documents** , proposals, not decisions. Outlines, drafts of ideas, "what if" notes.
   May contradict canon; that contradiction is a question, not a fact.
3. **Research** , supporting material. Sources, references, inspiration. Informs canon; is never
   itself canon.
4. **Archive** , historical record. Superseded versions, cut scenes, abandoned arcs. Kept for
   provenance and never consulted as current.

**The rule that makes it work**: when two documents disagree, the higher level wins, and the lower
one is corrected or archived. Same-level disagreement is an open question for the author , resolving
it silently is how a draft becomes an accidental source of truth.

## Recommended Layout

```
canon/          # Level 1 , story bible, characters, world rules, timeline
working/        # Level 2 , outlines, planning notes, open questions
research/       # Level 3 , sources and references
manuscript/     # the draft itself, organised by the project's own shape
archive/        # Level 4 , superseded material, dated
```

**Recommended, not mandated.** A kit advises; the project's shape is the author's. What is NOT
optional is that the four authority levels are separable , whatever they are called, a reader must
be able to tell canon from a working note without opening the file.

## Naming Conventions

- **Scenes** , zero-padded sequence plus a short slug (`03-the-harbour-meeting.md`). Padding keeps
  sort order honest past nine; the slug makes a file list readable without opening anything.
- **Chapters and parts** , the same pattern one level up. Nest only as deep as the work needs; a
  three-level hierarchy for a standalone novel is overhead.
- **Series** , a book folder at the top, and canon shared ACROSS books rather than duplicated into
  each. Duplicated canon is the single most reliable source of continuity error.
- **Canon documents** , named for the thing, not the document type (`magic-system.md`, not
  `worldbuilding-notes-2.md`).
- **Archives** , dated on archiving (`2026-09-07-cut-prologue.md`), so provenance survives.

## Quality Standards

- Every document sits at exactly one authority level, inferable from its location
- Canon is never edited as a side effect of drafting
- Same-level contradictions are raised as questions, not silently resolved
- Series canon lives once and is referenced, never copied per book
- Archived material is dated and never cited as current

## Boundaries

This skill governs WHERE things live and which document wins. Verifying a manuscript against canon
is `qd-masters:master-canon-verification`; designing the world's rules is `qd-masters:master-worldbuilding`. When a
structural problem is really a canon-authority dispute , two documents both claiming to be the story
bible , that is this skill's, and the answer is to designate one and archive the other.
