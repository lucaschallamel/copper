---
description: Run a sleep-optimisation consultation , assess patterns, design protocols,
  and align rest with performance, grounded in the qd-sme-sleep skill (Sleep Optimisation
  Protocol, circadian alignment, 3-2-1 system, sleep-pressure model).
---

Run a sleep-optimisation consultation focused on: **$ARGUMENTS**

**Optional arguments:**

- `sleep_challenge` , primary sleep issue. Options: `insomnia`, `schedule`, `quality`,
  `optimization`, `disorders` (default: `optimization`).
- `lifestyle_type` , lifestyle context. Options: `professional`, `shift_work`, `athlete`,
  `traveler`, `parent` (default: `professional`).
- `optimization_goal` , primary outcome focus. Options: `performance`, `health`, `recovery`,
  `longevity`, `energy` (default: `performance`).

With no arguments, open by exploring what is keeping the user from the restorative sleep they need.

## Approach

1. **Load the sleep knowledge** , Use the `qd-smes:sme-sleep` skill.
2. **Diagnose** , clarify the current sleep patterns, the chronotype and environment, and the
   specific issue behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (Sleep Optimisation Protocol
   for structure, circadian alignment for timing, the 3-2-1 system for wind-down, the sleep-pressure
   model for drive) and design the plan for the user's `context`.
4. **Recommend to action** , give a prioritised set of protocol steps with the metric each should
   move and the tracking or environmental artefact to produce, in the skill's scientific, practical
   style.

## Examples

```bash
# Performance-focused optimisation consultation for a professional lifestyle
/qd-smes:sme-sleep sleep_challenge=optimization lifestyle_type=professional optimization_goal=performance
```

## Opening (when no args)

"Sleep is your superpower , it is when your brain cleans itself, your body repairs, and tomorrow's
performance is built. What is keeping you from the restorative sleep you deserve?"

---

- Skill: `qd-smes:sme-sleep` (owns the sleep methodology, KPIs, and frameworks)
