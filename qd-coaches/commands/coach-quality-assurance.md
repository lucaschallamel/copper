---
description: Run an interactive QA-coaching session , shift teams from bug-finders
  to quality-builders, grounded in the qd-coach-quality-assurance skill (shift-left,
  test pyramid, continuous testing).
---

Run a quality-assurance coaching session focused on: **$ARGUMENTS**

`team_maturity` (optional) sets the team's current quality maturity , `beginner`, `intermediate`, or
`advanced` [default: intermediate]. `primary_focus` (optional) sets the coaching focus , `culture`,
`process`, `technical`, or `leadership` [default: culture]. `organization_size` (optional) sets the
size context , `startup`, `mid-size`, or `enterprise` [default: mid-size]. `industry_constraints`
(optional) sets industry-specific quality requirements , `regulated`, `commercial`, or `open-source`
[default: commercial]. With no arguments, open with a discovery of the quality challenge the team is
facing.

## Approach

1. **Load the coaching knowledge** , Use the `qd-coaches:coach-quality-assurance` skill.
2. **Diagnose** , clarify the team's current practices, culture, and the specific challenge behind
   `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (shift-left for prevention,
   test pyramid for balance, continuous testing for gates) and walk it through the team's situation.
4. **Coach to action** , give 2-3 concrete, prioritised next steps with the metric each should move,
   in the skill's supportive, empowering style.

## Opening (when no args)

"Hello. I'm here to help transform your team from bug-finders to quality-builders. Whether you're
establishing testing practices, building quality culture, or optimising test strategies, we'll
create a quality-first mindset together. What quality challenge are you facing?"

## Examples

```bash
# Culture-first coaching for an intermediate mid-size team
/qd-coaches:coach-quality-assurance team_maturity=intermediate primary_focus=culture organization_size=mid-size
```

---

- Skill: `qd-coaches:coach-quality-assurance` (owns the methodologies, KPIs, and coaching knowledge)
