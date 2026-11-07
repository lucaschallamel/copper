---
description: Run an analytics-engineering session , design the data pipelines, semantic
  layer, dashboards, and metrics for a use case, grounded in the gd-data-analytics-engineer
  skill (modern data stack, dbt, BI).
---

Run an analytics-engineering session for: **$ARGUMENTS**

All arguments are optional. `analytics_type` (default `product`; options: `operational`, `product`,
`financial`, `marketing`, `customer`); `stack_type` (default `modern`; options: `modern`,
`traditional`, `cloud-native`, `open-source`); `scale` (default `medium`; options: `small`,
`medium`, `large`, `enterprise`); `real_time` (default `false`; options: `true`, `false`). With no
arguments, open by drawing out the business questions, the data sources, and the freshness and
performance expectations.

## Approach

1. **Load the analytics knowledge** , Use the `gd-data-ai:data-analytics-engineer` skill.
2. **Frame the problem** , clarify the business questions behind `$ARGUMENTS`, the source systems, the
   data volume, and the freshness, performance, and governance requirements.
3. **Design the solution** , apply the fitting patterns from the skill (dimensional modelling, dbt
   semantic layer, orchestration, the BI tool, and a quality framework) to the chosen
   `analytics_type`, `stack_type`, and `scale`, adding streaming where `real_time` is set.
4. **Validate and govern** , add tests, anomaly detection, and lineage; define metric ownership and
   freshness SLAs; and optimise queries for cost and dashboard performance.

## Opening (when no args)

"Let's build analytics your stakeholders can trust. What business questions are you answering, where
does the data come from, and how fresh and fast do the results need to be?"

## Examples

```bash
# Large-scale product analytics on the modern data stack
/gd-data-ai:data-analytics-engineer analytics_type=product stack_type=modern scale=large

# Real-time financial reporting
/gd-data-ai:data-analytics-engineer analytics_type=financial real_time=true

# Operational analytics on an open-source stack
/gd-data-ai:data-analytics-engineer analytics_type=operational stack_type=open-source
```

---

- Skill: `gd-data-ai:data-analytics-engineer` (owns the methodologies, patterns, and analytics
  knowledge)
- Related agent: the proactive `gd-data-ai:data-analytics-engineer` agent loads the same skill autonomously.
