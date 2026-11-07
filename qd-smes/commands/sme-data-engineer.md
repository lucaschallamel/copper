---
description: Run a data-engineering consultation , design platforms, build pipelines,
  and optimise cost and speed, grounded in the qd-sme-data-engineer skill (data mesh,
  Lambda/Kappa, DataOps, data quality).
---

# /qd-smes:sme-data-engineer

Run a data-engineering consultation focused on: **$ARGUMENTS**

`platform_type` (optional) sets the type of data platform , `modern_stack`, `streaming`,
`warehouse`, `lakehouse`, or `hybrid` [default: modern_stack]. `scale` (optional) sets data scale
and complexity , `startup`, `medium`, `large`, or `massive` [default: large]. `primary_use_case`
(optional) sets the main platform purpose , `analytics`, `ml_platform`, `real_time`, `reporting`, or
`mixed` [default: analytics]. With no arguments, open by measuring the user's current data volume,
velocity, and variety, and what better infrastructure should enable.

## Approach

1. **Load the data-engineering knowledge** , Use the `qd-smes:sme-data-engineer` skill.
2. **Diagnose** , clarify the current platform, the KPIs (pipeline reliability, data freshness,
   query performance, cost, self-service adoption), and the specific bottleneck behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (data mesh for ownership,
   Lambda/Kappa for batch versus stream, DataOps for delivery, a data-quality framework for
   reliability) and design the concrete change for the user's `stack`.
4. **Recommend to action** , give a prioritised set of steps with the metric each should move and
   the pipeline or architecture artefact to produce, in the skill's pragmatic, user-empathetic
   style.

## Opening (when no args)

"Let's talk about your data challenges. What's your current data volume, velocity, and variety, and
what are you trying to enable with better data infrastructure?"

## Examples

```bash
/qd-smes:sme-data-engineer platform_type=modern_stack scale=large primary_use_case=analytics
```

---

- Skill: `qd-smes:sme-data-engineer` (owns the data-platform methodology, KPIs, and frameworks)
