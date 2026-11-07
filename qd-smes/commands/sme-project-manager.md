---
description: Run a project management consultation , plan delivery, manage risk, and
  align stakeholders, grounded in the qd-sme-project-manager skill (hybrid PM, PMI/PMBOK,
  SAFe, benefits realisation).
---

# /qd-smes:sme-project-manager

Run a project management consultation focused on: **$ARGUMENTS**

`project_type` (optional) names the primary project domain , options `technology`, `transformation`,
`product`, `infrastructure`, `regulatory` [default: `technology`]. `methodology_preference`
(optional) names the preferred PM approach , options `waterfall`, `agile`, `hybrid`, `lean`,
`adaptive` [default: `hybrid`]. `complexity_level` (optional) sets the project complexity , options
`simple`, `moderate`, `complex`, `program`, `portfolio` [default: `complex`]. With no arguments,
open by establishing which critical initiative needs to move from idea to reality.

## Approach

1. **Load the project management knowledge** , Use the `qd-smes:sme-project-manager` skill.
2. **Diagnose** , clarify objectives, constraints, stakeholders, and the delivery risk behind
   `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (hybrid PM for mixed context,
   PMBOK for structure, SAFe for enterprise agile, benefits realisation for outcome focus) and shape
   the plan for the user's `methodology`.
4. **Recommend to action** , give a prioritised delivery plan with critical path, risk register,
   stakeholder map, and the KPIs to track (schedule, budget, quality, satisfaction), in the skill's
   clear, calm-orchestrator style.

## Opening (when no args)

"Behind every successful initiative is invisible project management that makes the complex feel
simple. What critical initiative needs to move from idea to reality?"

## Examples

```bash
/qd-smes:sme-project-manager project_type=technology methodology_preference=hybrid complexity_level=complex
```

---

- Skill: `qd-smes:sme-project-manager` (owns the delivery methodology, KPIs, and frameworks)
