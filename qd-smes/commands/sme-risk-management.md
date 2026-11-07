---
description: Run a risk management consultation , assess risk, design controls, and
  align governance, grounded in the qd-sme-risk-management skill (COSO ERM, ISO 31000,
  Three Lines Model, risk appetite).
---

Run a risk management consultation focused on: **$ARGUMENTS**

`industry_focus` (optional) sets the primary industry expertise [default: `cross_industry`]; options
are `financial_services`, `technology`, `healthcare`, `manufacturing`, `cross_industry`.
`risk_priority` (optional) names the primary risk focus area [default: `enterprise`]; options are
`enterprise`, `operational`, `cyber`, `financial`, `compliance`. `organization_size` (optional) sets
the company scale [default: `enterprise`]; options are `startup`, `mid_market`, `enterprise`,
`multinational`, `government`. With no arguments, open by establishing what is keeping the user up
at night from a risk perspective.

## Approach

1. **Load the risk management knowledge** , Use the `qd-smes:sme-risk-management` skill.
2. **Diagnose** , identify and prioritise the risks behind `$ARGUMENTS`, weighing likelihood, impact,
   and risk appetite.
3. **Apply a framework** , select the fitting approach from the skill (COSO ERM for integration, ISO
   31000 for standards, Three Lines Model for assurance, risk appetite for strategy alignment) for
   the `risk-domain`.
4. **Recommend to action** , give a prioritised mitigation plan with controls, KRIs, response
   strategies, and the governance reporting to embed it, in the skill's balanced, business-language
   style.

## Opening (when no args)

"Effective risk management is not about avoiding all risks, it is about taking the right risks for
the right reasons. What is keeping you up at night from a risk perspective?"

## Examples

```bash
# Enterprise-wide risk framework across industries for an enterprise-scale organisation
/qd-smes:sme-risk-management industry_focus=cross_industry risk_priority=enterprise organization_size=enterprise
```

---

- Skill: `qd-smes:sme-risk-management` (owns the ERM frameworks, KPIs, and risk methodology)
