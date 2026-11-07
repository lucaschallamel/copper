---
description: Run a customer success consultation , reduce churn, drive expansion,
  and build health models, grounded in the qd-sme-customer-success skill (health score
  model, success journey mapping, value realisation).
---

# /qd-smes:sme-customer-success

Run a customer success consultation focused on: **$ARGUMENTS**

`company_stage` (optional) sets the current company maturity , `startup`, `growth`, `scale`, or
`enterprise` [default: growth]. `cs_maturity` (optional) sets the current CS sophistication ,
`reactive`, `developing`, `proactive`, or `strategic` [default: developing]. `primary_challenge`
(optional) names the main CS challenge , `retention`, `expansion`, `scaling`, `adoption`, or
`advocacy` [default: retention]. With no arguments, open by establishing the current retention rate
and what is preventing it from being higher.

## Approach

1. **Load the customer success knowledge** , Use the `qd-smes:sme-customer-success` skill.
2. **Diagnose** , clarify the retention and expansion metrics, the health signals, the segment
   model, and the specific bottleneck behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (health score model for risk,
   success journey mapping for lifecycle, value realisation for time-to-value, segmentation strategy
   for scale) for the user's segment.
4. **Recommend to action** , give a prioritised set of steps with the retention or expansion metric
   each should move and the playbook or success plan to produce, in the skill's consultative style.

## Opening (when no args)

"Customer success is about ensuring customers achieve their desired outcomes while using your
product. What is your current retention rate, and what is preventing it from being higher?"

## Examples

```bash
/qd-smes:sme-customer-success company_stage=growth cs_maturity=developing primary_challenge=retention
```

---

- Skill: `qd-smes:sme-customer-success` (owns the customer success methodology, KPIs, and
  frameworks)
