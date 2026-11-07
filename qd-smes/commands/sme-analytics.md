---
description: Run an analytics consultation , design metric frameworks, build dashboards,
  and turn data into decisions, grounded in the qd-sme-analytics skill (metric hierarchy,
  analytics maturity model, HEART).
---

# /qd-smes:sme-analytics

Run an analytics consultation focused on: **$ARGUMENTS**

`analytics_focus` (optional) names the primary analytics domain [default: general; options:
customer, product, financial, operational, general]; `organization_size` (optional) names the
company scale [default: enterprise; options: startup, midmarket, enterprise, global];
`analytics_maturity` (optional) names the current analytics sophistication [default: developing;
options: basic, developing, advanced, leading]. With no arguments, open by surfacing the decisions
being made by gut feel that should be backed by data.

## Approach

1. **Load the analytics knowledge** , Use the `qd-smes:sme-analytics` skill.
2. **Diagnose** , clarify the business question, the current metrics, the data trust gaps, and the
   specific bottleneck behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (metric hierarchy for KPI
   design, analytics maturity model for staging, HEART for engagement) for the user's domain.
4. **Recommend to action** , give a prioritised set of steps with the decision each insight supports
   and the dashboard or metric to produce, in the skill's business-first, action-oriented style.

## Opening (when no args)

"Analytics should answer your most important business questions. What decisions are you making by
gut feel that you wish were backed by data?"

## Examples

```
/qd-smes:sme-analytics analytics_focus=general organization_size=enterprise analytics_maturity=developing
```

---

- Skill: `qd-smes:sme-analytics` (owns the analytics methodology, KPIs, and frameworks)
