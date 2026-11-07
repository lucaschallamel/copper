---
description: Run a resource-monitoring and cost-optimisation session , analyse usage,
  surface cost drivers, and produce optimisation recommendations, grounded in the
  gd-resource-monitor skill (USE/RED methods, SRE SLI/SLO, capacity planning).
---

Run a resource-monitoring and cost-optimisation session for: **$ARGUMENTS**

All arguments are optional. `monitoring_focus` (default `comprehensive`; options: `performance`,
`cost`, `availability`, `security`, `comprehensive`); `analysis_period` (default `last-month`;
options: `real-time`, `last-hour`, `last-day`, `last-week`, `last-month`, `last-quarter`);
`alert_strategy` (default `intelligent`; options: `basic`, `intelligent`, `predictive`,
`sla-based`); `optimization_target` (default `efficiency`; options: `cost-reduction`, `performance`,
`availability`, `scalability`, `efficiency`). With no arguments, open by drawing out the system, the
usage data available, and the optimisation goal.

## Approach

1. **Load the monitoring knowledge** , Use the `gd-devops:resource-monitor` skill.
2. **Frame the problem** , clarify the system behind `$ARGUMENTS`, the `analysis_period`, the
   available metrics and cost data, and the optimisation goal.
3. **Analyse usage** , apply the fitting models from the skill (USE and RED methods, SLI/SLO
   framing, time-series and anomaly analysis) over the chosen `monitoring_focus`, measuring before
   recommending.
4. **Recommend and forecast** , at the requested `alert_strategy`, define thresholds and capacity
   forecasts, then deliver a cost-benefit report with prioritised optimisations toward the
   `optimization_target`.

## Examples

```bash
# Real-time performance monitoring with predictive alerting
/gd-devops:resource-monitor monitoring_focus=performance analysis_period=real-time alert_strategy=predictive

# Availability optimisation with SLA-based alerting
/gd-devops:resource-monitor optimization_target=availability alert_strategy=sla-based

# Comprehensive quarterly review targeting efficiency
/gd-devops:resource-monitor monitoring_focus=comprehensive analysis_period=last-quarter optimization_target=efficiency
```

## Opening (when no args)

"Let's find where the resources and cost are going. What system should I analyse, what usage data do
you have, and are you optimising for cost, performance, or efficiency?"

---

- Skill: `gd-devops:resource-monitor` (owns the methodologies, methods, and monitoring knowledge)
- Related agent: the proactive `gd-devops:resource-monitor` agent loads the same skill autonomously.
