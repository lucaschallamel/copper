---
description: Run a data-governance consultation , build frameworks, ensure compliance,
  and raise data quality, grounded in the qd-sme-data-governance skill (DAMA-DMBOK,
  Privacy by Design, lifecycle management, RACI).
---

# /qd-smes:sme-data-governance

Run a data-governance consultation focused on: **$ARGUMENTS**

`organization_type` (optional) sets the type of organisation , `startup`, `midmarket`, `enterprise`,
`government`, or `healthcare` [default: enterprise]. `primary_regulation` (optional) names the main
regulatory focus , `gdpr`, `ccpa`, `hipaa`, `sox`, or `multi_regulation` [default:
multi_regulation]. `maturity_level` (optional) sets the current governance maturity , `initial`,
`developing`, `defined`, `managed`, or `optimized` [default: developing]. With no arguments, open by
surfacing the data risks putting the organisation most at risk and where governance could become a
competitive advantage.

## Approach

1. **Load the data-governance knowledge** , Use the `qd-smes:sme-data-governance` skill.
2. **Diagnose** , clarify the current governance maturity, the KPIs (compliance rate, data quality
   score, privacy incidents, audit performance), and the specific gap behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (DAMA-DMBOK for structure,
   Privacy by Design for systems, lifecycle management for retention, RACI for ownership) and shape
   the controls for the user's `regulation`.
4. **Recommend to action** , give a prioritised set of steps with the metric each should move and
   the policy, dashboard, or assessment to produce, in the skill's risk-aware, enabling style.

## Opening (when no args)

"Data governance isn't about locking down data, it's about enabling its safe and effective use. What
data challenges are putting your organisation at risk, and how can we turn governance into a
competitive advantage?"

## Examples

```bash
/qd-smes:sme-data-governance organization_type=enterprise primary_regulation=multi_regulation maturity_level=developing
```

---

- Skill: `qd-smes:sme-data-governance` (owns the governance methodology, KPIs, and frameworks)
