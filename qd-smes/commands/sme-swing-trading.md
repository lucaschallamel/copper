---
description: Run a swing-trading consultation , evaluate setups, size risk, and plan
  exits, grounded in the qd-sme-swing-trading skill (stage analysis, trend following,
  breakout and pullback strategies).
---

Run a swing-trading consultation focused on: **$ARGUMENTS**

Optional arguments:

- `market_phase` (string): current market environment [default: `trending`]. Options: `trending`,
  `ranging`, `volatile`, `transitioning`.
- `strategy_focus` (string): primary swing approach [default: `trend_following`]. Options:
  `trend_following`, `breakout`, `reversal`, `pullback`, `mixed`.
- `holding_period` (string): typical position duration [default: `1_2_weeks`]. Options: `3_5_days`,
  `1_2_weeks`, `2_4_weeks`, `flexible`.

With no arguments, open by establishing the user's current approach to capturing multi-day moves.

## Approach

1. **Load the swing-trading knowledge** , Use the `qd-smes:sme-swing-trading` skill.
2. **Diagnose** , clarify the current approach, the market structure and setup quality, and the
   specific issue behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (stage analysis for the cycle,
   trend following for direction, breakout or pullback strategy for entry, the risk-management
   system for sizing) and design the plan for the user's `market`.
4. **Recommend to action** , give a prioritised set of steps with the metric each should move and
   the scan, setup, or position-management artefact to produce, in the skill's process-over-outcomes
   style.

## Opening (when no args)

"Swing trading sits in the sweet spot between day-trading stress and investing patience. What is
your current approach to capturing multi-day moves?"

## Examples

```bash
# Trend-following swing trades over a one-to-two-week horizon in a trending market
/qd-smes:sme-swing-trading market_phase=trending strategy_focus=trend_following holding_period=1_2_weeks
```

---

- Skill: `qd-smes:sme-swing-trading` (owns the swing-trading methodology, KPIs, and frameworks)
