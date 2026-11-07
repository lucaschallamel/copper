---
title: 'BD production output structure'
version: '1.0.0'
last_updated: '2026-09-10'
maintained_by: 'Lucas Challamel'
---

# BD production output structure

Where each stage of the prose-to-page pipeline writes its deliverable. This file is the pipeline's
shared hand-off contract, referenced by all three BD skills.

## The four output folders

Relative to the writing project's root:

| Folder           | Written by                     | Contains                                                   |
| ---------------- | ------------------------------ | ---------------------------------------------------------- |
| `panels/`        | `qd-masters:master-bd-panel-layout`    | Panel breakdowns , sequence, sizes, actions, pacing        |
| `art-direction/` | `qd-masters:master-bd-visual-language` | Composition guides , shot, angle, lighting, palette, focus |
| `scripts/`       | `qd-masters:master-bd-lettering`       | Comic scripts , balloons, captions, SFX, placement notes   |
| `pages/`         | the production pass            | Assembled pages , the three stages composited per page     |

## Naming

One file per page or per scene, prefixed so chronological and narrative order agree:

```
panels/bd-page-012-the-observatory.md
art-direction/bd-page-012-the-observatory.md
scripts/bd-page-012-the-observatory.md
pages/bd-page-012-the-observatory.md
```

The same stem across all four folders makes a page's four artefacts trivially greppable and keeps
the hand-off explicit , each stage reads the previous stage's file of the same name.

## These are OUTPUTS, not canon

Do not conflate them with the project's canon sources , the story bible, character profiles and
open-questions register, whatever the project calls them. Those are **inputs** the BD skills read
and must never contradict. The four folders above are **outputs** the BD skills write.

A project that keeps canon under its own conventional paths needs no change here; the BD skills
locate canon by role ("the character profiles"), not by a hardcoded path.

An output with no documented destination writes into the void: the next stage cannot find its input,
and a reader cannot tell whether a deliverable was produced.
