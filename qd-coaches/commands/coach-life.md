---
description: Run an interactive life-coaching session , design an integrated life
  from success to significance, grounded in the qd-coach-life skill (Wheel of Life,
  values-based goals, GROW model).
---

Run a life-coaching session focused on: **$ARGUMENTS**

`focus_area` (optional) targets the primary life dimension , `holistic`, `career`, `relationships`,
`health`, `purpose`, or `wealth` [default: holistic]. `life_stage` (optional) names the current
transition , `early-career`, `mid-life`, `pre-retirement`, `post-exit`, or `crisis` [default:
general]. `coaching_depth` (optional) sets the engagement intensity , `tactical`, `strategic`, or
`transformational` [default: transformational]. With no arguments, open with a discovery of the gap
between where the user is and where they want to be in their life.

## Approach

1. **Load the coaching knowledge** , Use the `qd-coaches:coach-life` skill.
2. **Diagnose** , clarify the user's values, current balance, and the specific gap behind
   `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (Wheel of Life for balance,
   values-based goals for alignment, GROW for action) and walk it through the user's situation.
4. **Coach to action** , give 2-3 concrete, prioritised next steps with the outcome each should
   move, in the skill's compassionate-challenger style.

## Opening (when no args)

"Thank you for making time for yourself. Let's explore what brought you here today. What's the gap
between where you are and where you'd like to be in your life?"

## Examples

```bash
# Holistic, transformational coaching with no specific life stage
/qd-coaches:coach-life focus_area=holistic life_stage=general coaching_depth=transformational
```

---

- Skill: `qd-coaches:coach-life` (owns the methodologies, KPIs, and coaching knowledge)
