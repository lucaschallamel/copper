---
description: Adapt prose dialogue into a comic script , balloons within the word budget,
  captions that add value, EN or FR sound effects and placement notes, grounded in
  the qd-master-bd-lettering skill.
---

# /qd-masters:master-bd-lettering

Write the text , condense dialogue to the balloon budget, add captions only where they earn their
space, and specify sound effects and placement.

Load the `qd-masters:master-bd-lettering` skill and apply it to the supplied material.

## Arguments

- `scene` , the prose scene carrying the original dialogue (required)
- `panel_breakdown` , the output of `/qd-masters:master-bd-panel-layout` (required)
- `composition_guide` , the output of `/qd-masters:master-bd-visual-language`, so placement avoids faces and
  key action (optional but recommended , without it, placement notes are provisional)
- `sfx_language` , optional: `english`, `french` or `mixed`. Defaults to matching the dialogue
  language

## Output

A comic script written to `scripts/`: per panel, captions, attributed speech balloons within the
~25-30 word budget, sound effects with intensity, and placement notes giving tail direction and
reading order. Followed by a script summary, character-voice verification and a text-density check
naming any panel that would read better silent.
