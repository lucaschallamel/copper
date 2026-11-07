---
name: master-asl-scenario-analysis
description: Pre-game scenario analysis for Advanced Squad Leader , reading victory conditions, order-of-battle assessment, terrain appraisal, and building a plan before the first turn. Use when preparing to play a scenario, choosing a side, or diagnosing why a plan failed.
version: 1.0.0
last_updated: '2026-09-08'
maintained_by: Lucas Challamel
---

# Master ASL Scenario Analysis (qd-master-asl-scenario-analysis)

Reusable scenario-preparation knowledge. This skill is the single source of truth for the capability;
the `qd-masters:master-asl-scenario-analysis` command invokes it for a pre-game analysis.

## Role Overview

Most scenarios are decided before the first die roll, by whether each side understood what it
actually had to achieve. The commonest loss is not a tactical error , it is fighting the wrong battle
competently.

## The Analysis, in Order

The sequence matters; each step constrains the next.

1. **Victory conditions FIRST, and read them literally.** Control which hexes, by when, held by
   what? "Control" and "occupy" are different, and the turn limit is a resource. Everything else is
   subordinate to this.
2. **The turn count is the real budget.** Divide the ground to be crossed by the turns available.
   That ratio tells you immediately whether this is a methodical advance or a race , and it is the
   single most informative number in the scenario.
3. **Order of battle , compare quality, not counts.** Squad firepower and morale, leader quality and
   count, support weapons, ordnance, armour. A smaller force with two good leaders is often stronger.
4. **Terrain , find the channels.** Where MUST the attacker cross open ground? Which buildings
   dominate the objective? Where can the defender not be? Attacks funnel; find the funnel.
5. **SSR , read them before planning, not during play.** A scenario special rule frequently exists
   to make one specific approach viable or impossible, and planning around the base rules first
   wastes the analysis.
6. **Name the plan and its failure condition.** "Cross the road by turn 3 using the orchard for
   cover; if the road is still swept by turn 4, switch to the left flank." A plan without a stated
   failure condition cannot be abandoned in time.

## Choosing a Side

Balance is a function of skill asymmetry, not just the scenario. The side with the tighter time
budget usually demands more of the player; the side with more units demands more bookkeeping. For a
learner, the defender is usually the gentler introduction , fewer simultaneous decisions per turn.

## Diagnosing a Failed Plan

Work backwards through the analysis order. Most failures are step 1 or 2 , a misread victory
condition, or a time budget that never allowed the plan , and they are frequently misattributed to
step 4 (bad luck in a specific firefight). Check the arithmetic before blaming the dice.

## Quality Standards

- Victory conditions are quoted, not paraphrased
- The ground-to-turns ratio is computed explicitly
- Order-of-battle comparison names quality differences, not just counts
- Every plan states its failure condition and the switch it triggers
- Post-mortems check steps 1 and 2 before blaming execution

## Boundaries

This skill prepares for a scenario and reviews it afterwards. What the rules permit is
`qd-masters:master-asl-rules`; how to fight a situation once play begins is `qd-masters:master-asl-doctrine`;
teaching and pacing a learner is `qd-coaches:coach-asl`. The in-game advisory loop is
`qd-masters:master-asl-play-partner`.
