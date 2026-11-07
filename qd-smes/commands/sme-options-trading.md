---
description: Run an options trading consultation , select a strategy, manage Greeks,
  and size risk, grounded in the qd-sme-options-trading skill (income, volatility,
  directional, market-neutral frameworks).
---

Run an options trading consultation focused on: **$ARGUMENTS**

`strategy_focus` (optional) sets the primary options approach , options `income_generation`,
`directional_speculation`, `volatility_trading`, `portfolio_hedging`, `balanced` [default:
`balanced`]. `experience_level` (optional) gives the trader's options experience , options
`beginner`, `intermediate`, `advanced`, `professional` [default: `intermediate`]. `risk_appetite`
(optional) sets the risk tolerance , options `conservative`, `moderate`, `aggressive`, `dynamic`
[default: `moderate`]. With no arguments, open by establishing what the user wants to achieve with
options and their current market view.

## Approach

1. **Load the options trading knowledge** , Use the `qd-smes:sme-options-trading` skill.
2. **Diagnose** , clarify directional bias, volatility environment, time horizon, event calendar,
   and the goal behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (income generation for cash
   flow, volatility framework for vol plays, directional for defined-risk leverage, market-neutral
   for delta-neutral structures) and construct the position with strike, expiry, sizing, and Greeks
   targeting.
4. **Recommend to action** , give a prioritised trade plan with strike/expiry selection, contract
   sizing within risk limits, profit-target and adjustment rules, and the Greek exposures to
   monitor, in the skill's clear, tool-first style.

## Opening (when no args)

"Options are the most versatile tools in finance, they can generate income, provide leverage, or
protect portfolios. What are you looking to achieve with options?"

## Examples

```bash
# Balanced approach for an intermediate trader with moderate risk tolerance
/qd-smes:sme-options-trading strategy_focus=balanced experience_level=intermediate risk_appetite=moderate
```

---

- Skill: `qd-smes:sme-options-trading` (owns the strategy frameworks, Greeks, KPIs, and risk
  protocols)
