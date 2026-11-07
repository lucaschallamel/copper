---
name: coach-asl
description: Coaching a learner through Advanced Squad Leader , pacing complexity, diagnosing where a player is stuck, sequencing what to learn next, and sustaining motivation through a famously steep learning curve. Use when teaching ASL, returning to it after a lapse, or deciding what to study next.
version: 1.0.0
last_updated: '2026-09-08'
maintained_by: Lucas Challamel
---

# Coach ASL (qd-coach-asl)

Reusable ASL coaching knowledge. This skill is the single source of truth for the capability; the
`qd-coaches:coach-asl` command invokes it for a coaching session.

## Role Overview

ASL's difficulty is not the rules , it is the ORDER in which people meet them. A learner who reads
the rulebook front to back usually stops playing; one who learns three rules per scenario keeps
going. Coaching ASL is almost entirely sequencing.

## Respect the Learner's Stated Constraints

Ask for, and then honour, the learner's own limits , available time per session, appetite for
bookkeeping, whether they want to compete or just play. **These are the learner's to state and the
coach's to work within**; never infer them, and never carry one learner's constraints into advice
for another. A coaching plan that ignores the stated time budget will be abandoned, which is worse
than a slower plan that is followed.

For a genuinely time-limited learner, prefer: smaller scenarios, the defender's side (fewer
simultaneous decisions), and a single new rule per session.

## The Complexity Ladder

Introduce in this order. Each rung assumes the one below is comfortable, not mastered:

1. **Movement, fire, morale** , the IFT and the rout chain. Nothing else matters until these are
   automatic.
2. **Leaders and support weapons** , the first real decisions about resource allocation.
3. **Smoke and concealment** , where the game stops being a shooting match and becomes manoeuvre.
4. **Ordnance and armour** , new to-hit procedures; a genuine step change in bookkeeping.
5. **Advanced terrain and conditions** , night, weather, fortifications. Introduce only when a
   scenario the learner WANTS to play requires them.

**Introduce rules as they arise in play, never as preparation.** A rule met in the situation it
governs is learned in one exposure; the same rule read cold is forgotten by the next session.

## Diagnosing Where a Learner Is Stuck

Five recurring plateaus, each with a different remedy:

- **Setup paralysis** , cannot commit to a defensive layout. Remedy: give a heuristic ("cover the
  objective and one approach"), not a full analysis. Paralysis is a decision-cost problem.
- **Rules anxiety** , stops play to check everything. Remedy: agree to play on and resolve
  afterwards. Momentum matters more than correctness while learning.
- **Fire-only play** , shoots but never moves. Remedy: a scenario with a tight turn limit, where
  standing still loses.
- **Armour avoidance** , leaves tanks unused because the procedures feel heavy. Remedy: one tank, one
  scenario, one procedure at a time.
- **Post-loss discouragement** , attributes losses to dice. Remedy: an after-action review that
  finds the decision, not the roll , see `qd-masters:master-asl-scenario-analysis`.

## Calibrating Opponent Difficulty

When the learner plays against a simulated opponent, the strength it should play at is a COACHING
decision, not the opponent's own , an opponent that tunes itself is grading the learner without
telling them. Set it explicitly:

- **Below the learner** while a new rung of the complexity ladder is being learned , the point is to
  practise the mechanic, not to be tested on it.
- **At the learner** once the rung is comfortable , this is where mistakes become instructive.
- **Above the learner** only on request, and only to demonstrate what a stronger line looks like.

Say which, and say why. `qd-masters:master-asl-play-partner` plays at the level it is given and does not
infer one from how the game is going.

## What Progress Looks Like

Not win rate. Better indicators, roughly in order of appearance: resolving common fire situations
without the rulebook; moving before being told to; setting up a defence without prompting; noticing
a DRM they had been forgetting; asking a question the coach has to look up.

The last one is the goal. Coaching succeeds when the learner outgrows the need for it.

## Quality Standards

- The learner's stated constraints are asked for, honoured, and never assumed
- One new rule per session, introduced in the situation that needs it
- Diagnosis names WHICH plateau, because the remedies differ
- Progress is reported against the indicators above, not win rate
- After-action reviews find the decision, not the die roll

## Boundaries

**References to `qd-master-asl-*` below are NAVIGATIONAL, not functional.** This skill's own method ,
the complexity ladder, the five plateaus, the calibration levels , works standalone; the pointers say
where a NEIGHBOURING capability lives if the reader has it. `qd-coaches` therefore declares no
cross-kit dependency, and should not: requiring `qd-masters` would force 26 unrelated master skills
on anyone who wants one coaching skill.

This skill teaches and paces. What the rules SAY is `qd-masters:master-asl-rules`; how to fight a situation
is `qd-masters:master-asl-doctrine`; preparing or reviewing a specific scenario is
`qd-masters:master-asl-scenario-analysis`; playing alongside the learner is
`qd-masters:master-asl-play-partner`. General coaching method beyond this game belongs to the other
`qd-coach-*` skills.
