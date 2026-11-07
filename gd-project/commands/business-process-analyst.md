---
description: Run a business-process analysis session , map current and future-state
  workflows, find inefficiencies, and design compliant, automated processes, grounded
  in the gd-business-process-analyst skill.
---

Analyse and optimise the business process for: **$ARGUMENTS**

All arguments are optional. `process_type` (default `back-office`; options: `customer-facing`,
`back-office`, `compliance`, `supply-chain`, `financial`, `operational`); `optimization_scope`
(default `analysis`; options: `discovery`, `analysis`, `redesign`, `automation`, `monitoring`);
`industry_context` (default `general`; options: `financial`, `healthcare`, `manufacturing`,
`technology`, `government`); `compliance_level` (default `standard`; options: `basic`, `standard`,
`strict`, `enterprise`); `automation_level` (default `moderate`; options: `minimal`, `moderate`,
`advanced`, `full-automation`). With no arguments, open by mapping the current-state process and
surfacing where time, cost, and risk actually accumulate.

## Approach

1. **Load the business-process knowledge** , Use the `gd-project:business-process-analyst` skill.
2. **Discover the current state** , clarify the actual versus documented workflow behind `$ARGUMENTS`,
   the actors, the hand-offs, and the compliance controls that must be preserved.
3. **Analyse and redesign** , apply the fitting models from the skill (Value Stream Mapping, DMAIC,
   SIPOC, BPMN 2.0) to the chosen `process_type` and `optimization_scope`, quantifying bottlenecks
   and the expected gains.
4. **Validate the future state** , at the requested `compliance_level` and `automation_level`,
   verify the future-state design against the real current-state process, keep every required audit
   trail, and deliver a quantified recommendation with its assumptions.

## Opening (when no args)

"Let's optimise a process you can measure. Which workflow are we mapping, who owns each step, and
where do delays, errors, or compliance risk pile up today?"

## Examples

```bash
# Customer-facing onboarding redesign in financial services
/gd-project:business-process-analyst process_type=customer-facing optimization_scope=redesign industry_context=financial

# Back-office process automation
/gd-project:business-process-analyst process_type=back-office optimization_scope=automation
```

---

- Skill: `gd-project:business-process-analyst` (owns the methodologies, patterns, and process
  knowledge)
- Related agent: the proactive `gd-project:business-process-analyst` agent loads the same skill
  autonomously.
