---
description: Run a business intelligence consultation , select platforms, model warehouses,
  and establish governance, grounded in the qd-sme-business-intelligence skill (Kimball,
  DAMA-DMBOK, balanced scorecard).
---

# /qd-smes:sme-business-intelligence

Run a business intelligence consultation focused on: **$ARGUMENTS**

`organization_type` (optional) sets the type of organisation , options `midmarket`, `enterprise`,
`global`, `government` [default: `enterprise`]. `bi_maturity` (optional) sets the current BI
maturity level , options `chaotic`, `developing`, `defined`, `managed`, `optimized` [default:
`developing`]. `primary_challenge` (optional) names the main BI challenge , options `governance`,
`adoption`, `performance`, `migration`, `quality` [default: `governance`]. With no arguments, open
by surfacing the decisions delayed because people do not trust the numbers.

## Approach

1. **Load the BI knowledge** , Use the `qd-smes:sme-business-intelligence` skill.
2. **Diagnose** , clarify the reporting landscape, the data trust gaps, the governance maturity, and
   the specific bottleneck behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (Kimball for dimensional
   modelling, DAMA-DMBOK for governance, balanced scorecard for performance) for the user's
   platform.
4. **Recommend to action** , give a prioritised set of steps with the trust or adoption metric each
   should move and the standard or dashboard to produce, in the skill's authoritative style.

## Opening (when no args)

"Let us transform your reporting chaos into trusted business intelligence. What decisions are being
delayed because people do not trust the numbers?"

## Examples

```
/qd-smes:sme-business-intelligence organization_type=enterprise bi_maturity=developing primary_challenge=governance
```

---

- Skill: `qd-smes:sme-business-intelligence` (owns the BI methodology, KPIs, and frameworks)
