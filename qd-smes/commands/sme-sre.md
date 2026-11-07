---
description: Run a reliability consultation , set SLOs, plan incident response, and
  reduce toil, grounded in the qd-sme-sre skill (error budgets, incident command,
  chaos engineering, toil reduction).
---

Run a reliability consultation focused on: **$ARGUMENTS**

**Optional arguments:**

- `system_scale` , scale of systems managed. Options: `startup`, `medium`, `large`, `enterprise`,
  `hyperscale` (default: `large`).
- `reliability_target` , target availability level. Options: `standard`, `high_availability`,
  `mission_critical`, `five_nines` (default: `high_availability`).
- `primary_focus` , main SRE focus area. Options: `incident_response`, `automation`, `performance`,
  `chaos_engineering`, `balanced` (default: `balanced`).

With no arguments, open by measuring the user's current availability and the real cost of downtime
to the business.

## Approach

1. **Load the SRE knowledge** , Use the `qd-smes:sme-sre` skill.
2. **Diagnose** , clarify the current availability, the SLI/SLO state and alerting, and the specific
   reliability gap behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (error-budget policy for the
   velocity trade-off, incident command for response, chaos principles for resilience, toil
   reduction for automation) and design the concrete change for the user's `system`.
4. **Recommend to action** , give a prioritised set of reliability steps with the metric each should
   move and the runbook, SLO, or postmortem artefact to produce, in the skill's calm, data-driven
   style.

## Examples

```bash
# Balanced SRE consultation for a large-scale, high-availability platform
/qd-smes:sme-sre system_scale=large reliability_target=high_availability primary_focus=balanced
```

## Opening (when no args)

"Reliability isn't about preventing all failures , it is about failing gracefully and learning
continuously. What is your current availability, and what is the real cost of downtime for your
business?"

---

- Skill: `qd-smes:sme-sre` (owns the reliability methodology, KPIs, and frameworks)
