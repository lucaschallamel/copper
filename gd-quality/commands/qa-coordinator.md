---
description: Run a QA strategy session , design a quality framework, test strategy,
  and quality gates with metrics, grounded in the gd-qa-coordinator skill (ISO/CMMI/TMMi,
  shift-left, risk-based testing).
---

Run a QA strategy session for: **$ARGUMENTS**

All arguments are optional. `quality_focus` (default `balanced`; options: `prevention`, `detection`,
`automation`, `compliance`, `balanced`); `methodology` (default `agile`; options: `agile`,
`waterfall`, `devops`, `hybrid`, `regulated`); `maturity_level` (default `developing`; options:
`initial`, `developing`, `defined`, `managed`, `optimizing`); `validation_level` (default
`standard`; options: `basic`, `standard`, `strict`, `enterprise`). With no arguments, open by
drawing out the project context, the current quality maturity, and the business objectives.

## Approach

1. **Load the QA knowledge** , Use the `gd-quality:qa-coordinator` skill.
2. **Frame the programme** , clarify the project context behind `$ARGUMENTS`, the current quality
   maturity, the compliance constraints, and the team structure.
3. **Design the strategy** , apply the fitting models from the skill (multi-layered test strategy,
   quality gates, shift-left, risk-based testing) to the chosen `quality_focus` and `methodology`,
   and define the KPIs and dashboards.
4. **Validate and roll out** , at the requested `validation_level`, check the gate criteria, the
   metrics coverage, and the enablement plan, then deliver a phased quality-programme roadmap.

## Examples

```bash
# Automation-led QA programme for a DevOps team
/gd-quality:qa-coordinator quality_focus=automation methodology=devops

# Defined-maturity organisation needing enterprise-grade validation
/gd-quality:qa-coordinator maturity_level=defined validation_level=enterprise
```

## Opening (when no args)

"Let's build quality in rather than test it in. What are you delivering, where is the team's quality
maturity today, and what business outcomes does the quality programme need to support?"

---

- Skill: `gd-quality:qa-coordinator` (owns the methodologies, frameworks, and QA knowledge)
- Related agent: the proactive `gd-quality:qa-coordinator` agent loads the same skill autonomously.
