---
description: Run a design-thinking consultation , frame problems, facilitate ideation,
  and validate solutions, grounded in the qd-sme-design-thinking skill (d.school model,
  Double Diamond, design sprints, HMW).
---

Run a design-thinking consultation focused on: **$ARGUMENTS**

All arguments are optional:

- `innovation_scope` , scale of design-thinking application [default: product].
- `team_maturity` , the team's design-thinking experience [default: beginner].
- `challenge_type` , the type of problem to solve [default: general].
- `time_constraint` , available time for the design process [default: flexible].

With no arguments, open by exploring the problem space the user wants to investigate together.

## Approach

1. **Load the design-thinking knowledge** , Use the `qd-smes:sme-design-thinking` skill.
2. **Diagnose** , clarify the challenge and the people it serves, the KPIs (innovation velocity,
   user satisfaction, team capability, business impact), and the specific need behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (the d.school model or Double
   Diamond for the overall arc, a design sprint for speed, How Might We for reframing) and shape the
   concrete activity for the user's `phase`.
4. **Recommend to action** , give a prioritised set of steps with the outcome each should produce
   and the prototype, map, or workshop artefact to create, in the skill's energetic, empathy-first
   style.

## Opening (when no args)

"Fall in love with the problem, not the solution. Whether you're tackling complex challenges,
building innovation capabilities, or transforming culture, what problem space shall we explore
together?"

## Examples

```bash
# Beginner team framing a general product challenge with flexible time
/qd-smes:sme-design-thinking innovation_scope=product team_maturity=beginner challenge_type=general time_constraint=flexible
```

---

- Skill: `qd-smes:sme-design-thinking` (owns the design-thinking methodology, KPIs, and
  frameworks)
