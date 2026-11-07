---
description: Run a strategic-finance consultation , align strategy, sharpen planning,
  and optimise capital, grounded in the qd-sme-finance skill (driver-based planning,
  zero-based budgeting, rolling forecasts, value creation).
---

Run a strategic-finance consultation focused on: **$ARGUMENTS**

All arguments are optional:

- `company_stage` , company lifecycle stage [default: growth]. Options: `startup`, `growth`,
  `mature`, `turnaround`, `pe_backed`.
- `industry_focus` , primary industry [default: technology]. Options: `technology`, `manufacturing`,
  `retail`, `services`, `healthcare`.
- `finance_priority` , primary finance focus [default: growth]. Options: `growth`, `profitability`,
  `efficiency`, `transformation`, `compliance`.

With no arguments, open by surfacing the financial challenges preventing the business from reaching
its full potential.

## Approach

1. **Load the finance knowledge** , Use the `qd-smes:sme-finance` skill.
2. **Diagnose** , clarify the current financial posture, the KPIs (forecast accuracy, close
   timeline, working capital, ROIC vs WACC, stakeholder trust), and the specific need behind
   `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (driver-based planning to link
   operations to outcomes, zero-based budgeting to rebuild from need, rolling forecasts for
   continuous planning, the value-creation framework for capital) and shape it to the user's
   `horizon`.
4. **Recommend to action** , give a prioritised set of steps with the metric each should move and
   the model, dashboard, or board deck to produce, in the skill's business-partner style.

## Opening (when no args)

"Great finance leaders don't just report the score, they help win the game. What financial
challenges are preventing your business from reaching its full potential?"

## Examples

```bash
# Growth-stage technology company prioritising growth-finance decisions
/qd-smes:sme-finance company_stage=growth industry_focus=technology finance_priority=growth
```

---

- Skill: `qd-smes:sme-finance` (owns the finance methodology, KPIs, and frameworks)
