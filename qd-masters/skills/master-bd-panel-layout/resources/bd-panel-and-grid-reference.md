---
title: 'BD panel budgets, grid systems and page-layout reference'
version: '1.0.0'
last_updated: '2026-09-10'
maintained_by: 'Lucas Challamel'
---

# BD panel budgets, grid systems and page layout

Enumerated reference for `qd-masters:master-bd-panel-layout`. Consulted during a breakdown pass , these are
the operational values, kept verbatim rather than summarised, because a deleted term is a deleted
capability.

## Page structure , the European standard

- **Page structure**: typically 1-9 panels per page , fewer and larger than manga convention
- **Panel variety**: mixed sizes for rhythm , splash pages for drama, grids for steady pacing
- **Reading flow**: left-to-right, top-to-bottom (European standard)
- **Visual breathing**: negative space and panel borders create natural pauses
- **Narrative density**: balance between visual action and dialogue-heavy panels

## Panel budget per page

- **1-2 panels**: splash page, dramatic moment, establishing shot
- **3-4 panels**: standard pace, balanced storytelling
- **5-6 panels**: dialogue-heavy scene, steady progression
- **7-9 panels**: fast-paced action, quick transitions

Above 9 the page becomes cluttered and reads as dense rather than fast.

## Pacing through panel size

- **Large panels = slow time**: emphasise drama, allow reader contemplation
- **Small panels = quick time**: accelerate action, create urgency
- **Panel repetition**: the same shot with slight changes reads as passage of time
- **Irregular shapes**: dynamic tension, disorientation

## Grid systems

- **2x2 grid**: four equal panels, steady rhythm
- **Tier system**: horizontal strips, widescreen effect
- **Column system**: vertical divisions, parallel action
- **Asymmetric**: mixed sizes for emphasis

## Layout principles

1. **Reading path**: the eye flows left-to-right, top-to-bottom (European standard)
2. **Visual weight**: larger panels read as more important moments
3. **Gutters**: the space between panels controls pacing , wide reads slower
4. **Panel borders**: thick borders emphasise; no border reads dreamlike or as flashback
5. **Bleed panels**: extending to the page edge is immersive

## Special techniques

- **Inset panels**: a small panel within a larger one , detail zoom, simultaneous action
- **Overlapping panels**: breaking the grid for dynamic movement
- **Splash panel**: full-page single image, maximum impact

Whether a panel carries text at all , and so whether it is silent , is decided by
`qd-masters:master-bd-lettering`, not here. A layout leaves room for text or does not; the decision to use
that room belongs to the stage that owns the text.

## How a style register affects LAYOUT

The style taxonomy itself , the named schools, their practitioners and their visual signatures , is
owned by `qd-masters:master-bd-visual-language` and is not duplicated here. What matters for layout is the
panel-size consequence:

- A **clear-line** register favours balanced, regular panels and a legible grid.
- An **action** register favours varied panel sizes and irregular shapes.
- An **atmospheric** register favours landscape panels and generous negative space.

Take the register from the visual-language pass rather than inferring one here.

## Selecting the visual beats

A beat earns a panel when it is one of:

- **Action**: character movement, physical interaction
- **Emotional peak**: expression, reaction, revelation
- **Environmental reveal**: establishing location or atmosphere
- **Object focus**: an important item, clue or symbolic element
- **Temporal transition**: passage of time, flashback

Selection criteria , **essential** (critical to plot), **emotional** (reveals character state),
**visual** (better shown than described), **pacing** (controls narrative rhythm).

Avoid: internal monologue with no visual component; abstract concepts needing extensive narration;
redundant shots that do not advance the story.

## Action-description register

Panel descriptions state WHAT happens; framing, angle and lighting belong to the visual-language
pass and must not be pre-empted here.

Template: `Panel [#]: [primary subject] + [key action] + [essential context]`

- Panel 1: The detective stands at the threshold of the darkened study.
- Panel 2: His hand reaches toward a letter on the desk.
- Panel 3: The detective's face reacts with shock as he reads.
- Panel 4: Exterior view , the mansion at dusk, one lit window.

Include: time of day when establishing, key props, character positioning relative to others, and
spatial relationships critical to the story. Omit camera angles, lighting specifics, colour palettes
and facial-expression detail.

## Panel-breakdown output contract

```markdown
## BD Page [#]: [Scene Title]

**Source Scene**: [file path and scene identifier] **Canon Verified**: [status and date] **Page
Layout**: [e.g. "Asymmetric 5-panel, top tier splash + 4-panel grid"] **Estimated Page Count**:
[number]

### Panel Sequence

**Panel 1** [SIZE: Full-width tier]

- **Action**: [core action description]
- **Purpose**: [establish location / introduce character / reveal information]
- **Pacing**: [Slow | Medium | Fast]

[continue for all panels]

### Layout Notes

**Grid Structure**: [page composition] **Reading Flow**: [eye-movement considerations] **Gutter
Spacing**: [Standard | Wide | Tight] **Special Techniques**: [insets, overlaps, bleeds]

### Canon Compliance Notes

**Characters**: [list with verification status] **Locations**: [confirmed against canon]
**Timeline**: [confirmed chronology] **Open Questions**: [undefined elements needing input]

### Handoff

**Key narrative emphases**: [2-3 moments needing special visual attention]
```

## Quality bar

Non-negotiable , canon compliance (zero contradictions), narrative logic (the sequence flows), a
readable layout (a clear visual path), complete beat coverage (every story beat has a panel).

Excellence , pacing mastery, visual economy (no redundant panels), layout creativity, emotional
architecture, and page-turn positioning for cliffhangers.
