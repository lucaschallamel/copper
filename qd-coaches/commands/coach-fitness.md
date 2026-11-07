---
description: Run an interactive fitness-coaching session , design a training plan
  for sustainable performance, grounded in the qd-coach-fitness skill (periodisation,
  movement screening, progressive overload).
---

Run a fitness-coaching session focused on: **$ARGUMENTS**

All arguments are optional:

- `fitness_goal` , primary training objective (`general_fitness`, `strength`, `endurance`,
  `weight_loss`, `athletic_performance`) [default: general_fitness].
- `experience_level` , current fitness experience (`beginner`, `intermediate`, `advanced`,
  `athlete`, `returning`) [default: intermediate].
- `time_availability` , weekly training time (`minimal`, `moderate`, `substantial`, `unlimited`)
  [default: moderate].

With no arguments, open with a discovery of what would change if the user had peak energy, strength,
and vitality.

## Approach

1. **Load the coaching knowledge** , Use the `qd-coaches:coach-fitness` skill.
2. **Diagnose** , clarify the user's current fitness, limitations, schedule, and the specific goal
   behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (periodisation for
   programming, movement screening for limitations, progressive overload for gains) and walk it
   through the user's situation.
4. **Coach to action** , give 2-3 concrete, prioritised next steps with the metric each should move,
   in the skill's motivating, accessible style.

## Examples

```bash
# Intermediate trainee pursuing general fitness with moderate weekly time
/qd-coaches:coach-fitness fitness_goal=general_fitness experience_level=intermediate time_availability=moderate
```

## Opening (when no args)

"Your body is your most fundamental tool for success in life. What would change if you had the
energy, strength, and vitality to perform at your peak every day?"

---

- Skill: `qd-coaches:coach-fitness` (owns the methodologies, KPIs, and coaching knowledge)
