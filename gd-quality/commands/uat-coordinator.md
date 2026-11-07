---
description: Run a UAT coordination session , plan business validation, acceptance
  criteria, and go-live readiness, grounded in the gd-uat-coordinator skill (business-process
  validation, persona-based and risk-weighted UAT, stakeholder orchestration).
---

Run a UAT coordination session for: **$ARGUMENTS**

All arguments are optional. `uat_scope` (default `comprehensive`; options: `focused`, `standard`,
`comprehensive`, `regulatory`); `testing_approach` (default `scenario-based`; options:
`exploratory`, `scenario-based`, `workflow-based`, `risk-based`); `user_involvement` (default
`active`; options: `minimal`, `moderate`, `active`, `intensive`); `validation_level` (default
`standard`; options: `basic`, `standard`, `strict`, `enterprise`). With no arguments, open by
drawing out the system, the critical business processes, and the stakeholders who must sign off.

## Approach

1. **Load the UAT knowledge** , Use the `gd-quality:uat-coordinator` skill.
2. **Frame the validation** , clarify the system and business processes behind `$ARGUMENTS`, the
   stakeholder map, and the go-live constraints.
3. **Design the UAT** , apply the fitting models from the skill (business-process validation,
   persona-based and risk-weighted UAT) to the chosen `uat_scope` and `testing_approach`, and define
   measurable acceptance criteria.
4. **Validate and recommend** , at the requested `validation_level`, run triage and coverage checks,
   then deliver a data-driven go/no-go recommendation with a sign-off plan.

## Examples

```bash
# Comprehensive, workflow-based UAT across business processes
/gd-quality:uat-coordinator uat_scope=comprehensive testing_approach=workflow-based

# Enterprise-grade validation strictness for a regulated go-live
/gd-quality:uat-coordinator validation_level=enterprise
```

## Opening (when no args)

"Let's validate that this system does what the business actually needs before it goes live. What are
we validating, which business processes are critical, and who needs to sign off?"

---

- Skill: `gd-quality:uat-coordinator` (owns the methodologies, frameworks, and UAT knowledge)
- Related agent: the proactive `gd-quality:uat-coordinator` agent loads the same skill autonomously.
