---
description: Run a progress-tracking session , build evidence-based status analytics,
  velocity metrics, and delivery forecasts with early-warning detection, grounded
  in the gd-progress-tracker skill. Read-only on the tracked work.
---

Track and forecast delivery progress for: **$ARGUMENTS**

All arguments are optional. `tracking_mode` (default `evidence_based`; options: `evidence_based`,
`statistical_analysis`, `predictive_modeling`, `real_time_monitoring`, `comprehensive`);
`complexity_detection` (default `multi_dimensional`; options: `basic`, `pattern_recognition`,
`multi_dimensional`, `predictive_analytics`, `enterprise_scale`); `resource_thresholds` (default
`five_zone`; the monitoring-zone configuration; options: `basic`, `three_zone`, `five_zone`,
`adaptive`, `enterprise`); `validation_framework` (default `eight_step`; the quality-gate
implementation; options: `basic`, `four_step`, `eight_step`, `comprehensive`, `enterprise_grade`).
With no arguments, open by establishing the current status, the velocity baseline, and the forecast
horizon. This capability observes and reports; it does not edit the tracked artefacts.

## Approach

1. **Load the progress-tracking knowledge** , Use the `gd-project:progress-tracker` skill.
2. **Collect the evidence** , gather the velocity, flow, and resource data behind `$ARGUMENTS` and
   detect untracked or hidden work at the chosen `complexity_detection` level.
3. **Analyse and forecast** , apply the fitting models from the skill (flow metrics, Monte Carlo
   forecasting, regression, five-zone resource monitoring) at the chosen `tracking_mode`, scoring
   risk and surfacing early-warning signals.
4. **Report to action** , at the requested `resource_thresholds` and `validation_framework`, deliver
   a stakeholder-specific dashboard with quantified status, confidence intervals, and prioritised
   recommendations.

## Opening (when no args)

"Let's turn status into a forecast you can trust. What are we tracking, what's the velocity
baseline, and how far out do you need the delivery prediction?"

## Examples

```bash
# Predictive enterprise-scale forecasting with five-zone monitoring
/gd-project:progress-tracker tracking_mode=predictive_modeling complexity_detection=enterprise_scale resource_thresholds=five_zone

# Comprehensive statistical analysis with predictive analytics
/gd-project:progress-tracker validation_framework=comprehensive tracking_mode=statistical_analysis complexity_detection=predictive_analytics
```

---

- Skill: `gd-project:progress-tracker` (owns the metrics, forecasting models, and KPIs)
- Related agent: the proactive, read-only `gd-project:progress-tracker` agent loads the same skill
  autonomously.
