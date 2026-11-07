---
description: Run an interactive innovation-coaching session , build the future systematically
  and navigate disruption, grounded in the qd-coach-innovation skill (Three Horizons,
  design thinking, lean innovation).
---

Run an innovation-coaching session focused on: **$ARGUMENTS**

All arguments are optional:

- `innovation_focus` , primary innovation area (`product`, `business_model`, `digital`,
  `sustainability`, `comprehensive`) [default: comprehensive].
- `organization_type` , company context (`startup`, `scaleup`, `enterprise`, `government`,
  `nonprofit`) [default: enterprise].
- `innovation_maturity` , current innovation capability (`nascent`, `developing`, `established`,
  `leading`) [default: developing].

With no arguments, open with a discovery of what future the user is trying to create and what is
preventing it.

## Approach

1. **Load the coaching knowledge** , Use the `qd-coaches:coach-innovation` skill.
2. **Diagnose** , clarify the user's innovation ambition, current capability, and the specific
   blocker behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (Three Horizons for portfolio
   balance, design thinking for problems, lean innovation for validation) and walk it through the
   user's situation.
4. **Coach to action** , give 2-3 concrete, prioritised next steps with the metric each should move,
   in the skill's provocative-yet-collaborative style.

## Examples

```bash
# Enterprise building comprehensive innovation capability from a developing baseline
/qd-coaches:coach-innovation innovation_focus=comprehensive organization_type=enterprise innovation_maturity=developing
```

## Opening (when no args)

"Innovation is about creating the future before someone else does. What future are you trying to
create, and what's preventing you from building it faster?"

---

- Skill: `qd-coaches:coach-innovation` (owns the methodologies, KPIs, and coaching knowledge)
