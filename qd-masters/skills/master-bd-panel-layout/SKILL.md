---
name: master-bd-panel-layout
description: Panel breakdown and page layout for bande dessinée , turning a prose scene into a paced sequence of panels with a page grid. Covers panel budgets, grid systems, gutter and border pacing, and action descriptions that state what happens without pre-empting framing. Use when converting prose to a panel breakdown, diagnosing a page that reads flat or cluttered, or deciding how many panels a scene needs.
version: 1.0.0
last_updated: '2026-09-10'
maintained_by: Lucas Challamel
---

# Master BD Panel Layout (qd-master-bd-panel-layout)

The first stage of the prose-to-page pipeline: it decides **how many panels, at what sizes, in what
page arrangement**, and writes the action description for each. It does not decide what a panel
looks like , that is `qd-masters:master-bd-visual-language` , nor what it says , that is
`qd-masters:master-bd-lettering`.

## Goal

Architect the reader's temporal experience. A breakdown controls how fast the reader moves through a
scene, where they linger, and which moments resonate. Dividing text into boxes is not the craft;
pacing is.

## When to Use

- Converting a drafted prose scene into a panel breakdown and page layout
- Deciding a panel budget when several counts are defensible
- Diagnosing a page that reads as flat, rushed or cluttered
- Positioning a page turn for a cliffhanger

## Setup

Reference material lives in
[`resources/bd-panel-and-grid-reference.md`](resources/bd-panel-and-grid-reference.md) , panel
budgets, pacing through size, grid systems, layout principles, special techniques, beat-selection
criteria, the action-description register, and the output contract. Load it for any breakdown pass.

Output destinations are defined in
[`resources/bd-output-structure.md`](resources/bd-output-structure.md).

**Canon precondition**: the project's canon sources (story bible, character profiles, open-questions
register , whatever the project calls them) must be readable before a breakdown begins. This skill
verifies timeline and event sequence against them; it never invents an answer to a tracked open
question.

## Steps

1. **Verify canon first.** Read the prose scene; identify its narrative purpose, the characters
   present, the chronological sequence of events, and the emotional beats. Cross-reference the
   project's canon sources. Flag contradictions and undefined elements rather than resolving them.
2. **Identify the visual beats.** Break the scene into discrete moments that earn a panel, using the
   beat types and selection criteria in the reference. Reject internal monologue with no visual
   component and shots that do not advance the story.
3. **Determine the panel count.** Choose from the budget ladder against the scene's pacing need.
   Where two counts are defensible, propose both and say what each buys.
4. **Design the page layout.** Select a grid system and panel sizes; apply the layout principles;
   reach for a special technique only where it earns its disruption.
5. **Write the action descriptions.** State WHAT happens , subject, action, essential context. Omit
   angles, lighting, palette and expression detail; those belong to the next stage and pre-empting
   them removes its judgement.
6. **Record canon compliance.** List characters, locations and timeline with verification status,
   and name any open question that remains open.
7. **Hand off.** Deliver the breakdown with 2-3 narrative emphases flagged for visual attention.

## Constraints

Owns the PAGE: how many panels, what size, what arrangement, and what happens in each. Does not own
what a panel looks like (`qd-masters:master-bd-visual-language`) or what it says (`qd-masters:master-bd-lettering`).
Continuity verification against canon belongs to `qd-masters:master-canon-verification` , this skill checks
timeline and event sequence as a precondition of its own work and defers a full continuity audit to
that skill.

Never contradicts canon; never invents answers to tracked open questions; never specifies camera
angle, lighting or artistic style; never writes dialogue or captions; never builds a page denser
than 9 panels.

**Whether a panel carries text at all , and so whether it is silent , is `qd-masters:master-bd-lettering`'s
decision, not this skill's.** A layout leaves room for text; choosing to use that room belongs to
the stage that owns the text. Likewise the style taxonomy (named schools and their practitioners)
belongs to `qd-masters:master-bd-visual-language`; this skill consumes a style register only for its
panel-size consequences.

## Safety Notes

Reads prose and canon documents; writes a breakdown to the project's BD output folders. No
destructive operation. Where a canon source is missing or a question is open, it reports and stops
rather than filling the gap.
