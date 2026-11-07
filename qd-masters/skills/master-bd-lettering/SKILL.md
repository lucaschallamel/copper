---
name: master-bd-lettering
description: Comic scripting and lettering for bande dessinée , adapting prose dialogue into balloons, captions and sound effects. Covers the balloon taxonomy, the 25-30 word budget, condensation technique, caption discipline, EN/FR onomatopoeia banks and placement. Use when condensing dialogue to fit a balloon, writing captions, choosing sound effects, or diagnosing pages that read as text-heavy.
version: 1.0.0
last_updated: '2026-09-10'
maintained_by: Lucas Challamel
---

# Master BD Lettering (qd-master-bd-lettering)

The third stage of the prose-to-page pipeline: it decides **what each panel says**. It takes the
panel breakdown and the visual composition as input and produces the complete text specification.

## Goal

Translate narrative into the language of comics, where words and images tell what neither could
alone. The craft is knowing when to use words and when to trust the art.

## When to Use

- Adapting prose dialogue into balloon-ready text
- Writing narrative captions, or deciding whether a caption is needed at all
- Choosing or inventing sound effects, in English or French
- Specifying balloon placement and reading order
- Diagnosing a page that reads as text-heavy or whose reading order is ambiguous

## Setup

Reference material lives in
[`resources/bd-lettering-reference.md`](resources/bd-lettering-reference.md) , the balloon taxonomy,
text-volume limits, lettering style, condensation technique, multi-balloon splitting, caption rules,
the EN and FR onomatopoeia banks, placement guidelines and the output contract. Load it for any
scripting pass.

Output destinations are the pipeline's shared contract, defined in
`qd-master-bd-panel-layout/resources/bd-output-structure.md` , this stage writes to `scripts/`. The
contract lives with the first stage because it is that pipeline's hand-off; all three stages read
it.

**Canon precondition**: character profiles inform voice. This skill verifies that each character
sounds like themselves; a full continuity audit belongs to `qd-masters:master-canon-verification`.

## Steps

1. **Analyse the source.** Read the complete prose scene , dialogue, exposition, emotional beats,
   subtext, pacing and tone.
2. **Map text to panels.** Using the breakdown and the compositions, decide which character speaks
   in which panel, which moments need captions rather than dialogue, and which actions need sound.
3. **Condense the dialogue.** Apply the condensation principles to bring each line inside the ~25-30
   word balloon budget while preserving subtext and the character's speech pattern. Where a line
   cannot fit, split at complete thoughts, never mid-thought.
4. **Write captions only where they add value.** A caption that describes what the art already shows
   is a defect, not a belt-and-braces.
5. **Create sound effects.** Select from the EN or FR bank by category, set the intensity, and state
   the language parameter. Invent where nothing in the bank fits the register.
6. **Specify placement.** Balloon type, tail direction, position relative to faces and key action,
   and the resulting reading order.
7. **Check density.** Balloons per panel, captions per panel, and whether any panel would be
   stronger silent.

## Constraints

Owns the TEXT: balloons, captions, sound effects, and their placement. Does not own the page grid
(`qd-masters:master-bd-panel-layout`) or the visual composition (`qd-masters:master-bd-visual-language`), though
placement is coordinated with the latter. Character-voice craft in prose belongs to
`qd-masters:master-voice-craft`; this skill applies voice within the balloon constraint.

Never exceeds the readable balloon length; never places text over faces or critical action; never
uses a caption to state what is visible; never homogenises character voices for brevity.

## Safety Notes

Reads prose, breakdowns, compositions and canon documents; writes scripts to the project's BD output
folders. No destructive operation. Reports a voice inconsistency rather than silently normalising
it.
