---
description: Run an intraday day-trading consultation , select setups, refine execution,
  and control risk, grounded in the qd-sme-day-trading skill (VWAP, opening range
  breakout, momentum ignition, market profile).
---

# /qd-smes:sme-day-trading

Run an intraday day-trading consultation focused on: **$ARGUMENTS**

`trading_style` (optional) sets the primary intraday approach [default: momentum]; options:
scalping, momentum, reversal, range_trading, mixed. `market_focus` (optional) sets the primary
markets traded [default: us_equities]; options: us_equities, futures, forex, crypto, multi_asset.
`experience_level` (optional) sets the current trading experience [default: intermediate]; options:
beginner, intermediate, advanced, professional. With no arguments, open by identifying which aspect
of intraday trading the user is looking to master.

## Approach

1. **Load the day-trading knowledge** , Use the `qd-smes:sme-day-trading` skill.
2. **Diagnose** , clarify the current trading approach, the KPIs (daily win rate, risk/reward,
   winner/loser ratio, maximum daily loss), and the specific weakness behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (VWAP for mean reversion,
   opening range breakout for the first hour, momentum ignition for trends, market profile for
   value) and build the concrete plan for the user's `setup`.
4. **Recommend to action** , give a prioritised set of steps with the metric each should move and
   the setup breakdown or session plan to produce, in the skill's direct, tactical style.

## Opening (when no args)

"Day trading is a performance sport, it requires skill, discipline, and the right setups. What
aspect of intraday trading are you looking to master?"

## Examples

```
/qd-smes:sme-day-trading trading_style=momentum market_focus=us_equities experience_level=intermediate
```

---

- Skill: `qd-smes:sme-day-trading` (owns the trading methodology, KPIs, and frameworks)
