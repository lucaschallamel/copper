---
description: Run an ASL coaching session , diagnose where the learner is stuck, pick
  the next rung of the complexity ladder, and honour their stated constraints, grounded
  in the qd-coach-asl skill.
---

# /qd-coaches:coach-asl

Coach a learner: diagnose the plateau, sequence what comes next.

## Arguments

- `learner_state` , what the learner can currently do and where they are stuck (required)
- `constraints` , the learner's OWN stated limits (time per session, appetite for bookkeeping).
  Asked for, never inferred
- `goal` , optional: competitive play, solo enjoyment, or a specific scenario

## Output

Which plateau the learner is on (the five are named in the skill), the remedy for that specific
plateau, the next rung of the complexity ladder, and progress measured against the stated indicators
rather than win rate.
