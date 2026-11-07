---
name: master-bd-visual-language
description: Visual composition for bande dessinée , turning a panel breakdown into executable art direction. Covers shot types and camera angles, facial expression and body language, environment, lighting schemes, colour palettes and composition rules. Use when specifying how a panel looks, choosing a shot or angle, designing lighting for mood, or diagnosing compositions that read as visually flat or repetitive.
version: 1.0.0
last_updated: '2026-09-10'
maintained_by: Lucas Challamel
---

# Master BD Visual Language (qd-master-bd-visual-language)

The second stage of the prose-to-page pipeline: it decides **what each panel looks like**. It takes
a panel breakdown as input and produces a composition an artist can execute without ambiguity.

## Goal

Direct the reader's visual experience , what they see, in what order, with what emotional impact. A
composition should make the reader feel the story before they read a word.

## When to Use

- Turning a panel breakdown into per-panel art direction
- Choosing a shot type or camera angle for a specific narrative effect
- Designing lighting and palette for a scene's mood
- Diagnosing pages that read as visually monotonous or confusing

## Setup

Reference material lives in
[`resources/bd-visual-language-reference.md`](resources/bd-visual-language-reference.md) , the shot
and angle vocabularies, emotion mapping, blocking, environment and depth, lighting schemes, palette
approaches, focal hierarchy, composition rules, and the output contract. Load it for any composition
pass.

Output destinations are the pipeline's shared contract, defined in
`qd-master-bd-panel-layout/resources/bd-output-structure.md` , this stage writes to
`art-direction/`. The contract lives with the first stage because it is that pipeline's hand-off;
all three stages read it.

**Canon precondition , and it is a data prerequisite, not a formality**: character profiles must
carry **physical descriptions** before this skill can run. Composition specifies appearance, and
appearance that contradicts canon is the defect this stage is most prone to. Where a profile has no
physical description, report it rather than inventing one.

## Steps

1. **Establish the style register.** Which tradition is this album in , clear-line, realist,
   atmospheric/noir, franco-fantastic (the reference gives each one's practitioners and signatures)?
   **If it is not specified, ask. Do not infer one from the prose.** The register governs every
   later choice in this pass, and it is also what `qd-masters:master-bd-panel-layout` consumes for its
   panel-size consequences, so an assumed register propagates silently.
2. **Establish visual canon.** Read the character profiles for physical description and the world
   sources for location, architecture and period. Note what is fixed and what is open.
3. **Select shot and angle per panel.** Apply the selection criteria , narrative purpose, visual
   variety across consecutive panels, character power dynamics, and pacing support.
4. **Choreograph the characters.** Specify facial expression using the emotion mapping, then
   posture, gesture, weight distribution, spatial relationship and movement direction. Apply the
   blocking principles so silhouettes stay readable.
5. **Design the environment.** Architecture, interior or exterior detail, depth layers, scale
   indicators.
6. **Light the panel.** Choose a source and direction, then a lighting scheme, then a shadow
   pattern. Keep sources and shadows coherent across the page , this is the most common continuity
   failure.
7. **Set the palette.** Dominant hue, accents, and any symbolic colour carried by a character.
8. **Establish focal hierarchy.** Primary, secondary and background, with a detail level for each.
9. **Apply composition rules** with creative flexibility, then review the page for shot variety.

## Constraints

Owns what happens WITHIN a panel: framing, expression, environment, lighting, palette, focal
hierarchy. Does not own how many panels or the page grid (`qd-masters:master-bd-panel-layout`), nor the text
(`qd-masters:master-bd-lettering`). Physical-appearance continuity against canon is checked here as a
precondition; a full continuity audit belongs to `qd-masters:master-canon-verification`.

Never contradicts a character's physical description; never composes without a light source; never
overcrowds a panel; never repeats an identical shot across consecutive panels unless the repetition
is the point.

## Safety Notes

Reads a panel breakdown and canon documents; writes composition guides to the project's BD output
folders. No destructive operation. Reports a missing physical description rather than inventing an
appearance.
