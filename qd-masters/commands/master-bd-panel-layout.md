---
description: Break a prose scene into a paced panel sequence and page layout , panel
  budget, grid system, sizes and action descriptions, grounded in the qd-master-bd-panel-layout
  skill.
---

# /qd-masters:master-bd-panel-layout

Turn a prose scene into a panel breakdown and page layout, verifying canon before pacing.

Load the `qd-masters:master-bd-panel-layout` skill and apply it to the supplied scene.

## Arguments

- `scene` , the prose scene to break down (required)
- `canon_sources` , the project's canon documents and their authority tier (required , the skill
  verifies timeline and event sequence against them and will not invent answers to open questions)
- `panel_budget` , optional: a target panel count per page, **which must be in the range 1-9** (the
  European album ceiling , above 9 a page reads as cluttered, and the skill refuses it). Omit to
  have the budget proposed from the scene's pacing, with alternatives where two counts are
  defensible

## Output

A panel breakdown written to `panels/`: panel sequence with size, action and pacing per panel, then
layout notes (grid, reading flow, gutters, special techniques), canon-compliance notes with
verification status, and 2-3 narrative emphases flagged for the visual-language pass. Open questions
are reported as open, never resolved.
