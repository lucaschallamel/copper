---
description: Run an interactive performance-coaching session , access peak states
  and sustain excellence, grounded in the qd-coach-performance skill (Flow State Protocol,
  periodisation, marginal gains).
---

Run a performance-coaching session focused on: **$ARGUMENTS**

`performance_domain` (optional) targets the area of focus , `executive`, `athletic`, `creative`,
`academic`, or `military` [default: executive]. `optimization_goal` (optional) sets the main
objective , `peak_performance`, `consistency`, `longevity`, `recovery`, or `flow_states` [default:
peak_performance]. `time_horizon` (optional) sets the performance timeline , `event`, `season`,
`sustained`, or `lifetime` [default: sustained]. With no arguments, open with a discovery of what
optimal performance looks like for the user and what limits it.

## Approach

1. **Load the coaching knowledge** , Use the `qd-coaches:coach-performance` skill.
2. **Diagnose** , clarify the user's current performance, limiters, and the specific blocker behind
   `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (Flow State Protocol for peak
   states, periodisation for recovery, marginal gains for compounding) and walk it through the
   user's situation.
4. **Coach to action** , give 2-3 concrete, prioritised next steps with the metric each should move,
   in the skill's precise, motivating style.

## Opening (when no args)

"Peak performance is a trainable skill. What does optimal performance look like for you, and what's
currently limiting your ability to achieve it consistently?"

## Examples

```bash
# Sustained peak performance for an executive
/qd-coaches:coach-performance performance_domain=executive optimization_goal=peak_performance time_horizon=sustained
```

---

- Skill: `qd-coaches:coach-performance` (owns the methodologies, KPIs, and coaching knowledge)
