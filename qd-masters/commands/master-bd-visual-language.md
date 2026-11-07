---
description: Turn a panel breakdown into executable art direction , shot type, camera
  angle, expression, environment, lighting and palette per panel, grounded in the
  qd-master-bd-visual-language skill.
---

# /qd-masters:master-bd-visual-language

Compose each panel , framing, expression, environment, lighting, palette and focal hierarchy.

Load the `qd-masters:master-bd-visual-language` skill and apply it to the supplied breakdown.

## Arguments

- `panel_breakdown` , the output of `/qd-masters:master-bd-panel-layout` (required)
- `character_profiles` , the canon profiles (required). **They must carry physical descriptions** ,
  composition specifies appearance, and the skill reports a missing description rather than
  inventing one
- `visual_style` , optional: one of ligne-claire, realist, atmospheric-noir, franco-fantastic.
  Defaults to asking before assuming

## Output

A composition guide written to `art-direction/`: per panel, shot composition (type, vertical and
horizontal angle, framing), character details (position, pose, expression, clothing and props),
environmental setting with depth layers, lighting and atmosphere (source, scheme, shadow, time,
weather, palette) and visual focus. Page-level notes cover lighting and colour continuity.
