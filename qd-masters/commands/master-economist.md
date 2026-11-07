---
description: Run an economic-analysis session , read the data, anticipate policy and
  turning points, and translate macro into strategy, grounded in the qd-master-economist
  skill (cycles, monetary policy, financial systems, behavioural economics).
---

Run an economic-analysis session focused on: **$ARGUMENTS**

`analysis_focus` (optional) sets the primary area of economic analysis , options: macro_trends,
market_cycles, policy_analysis, risk_assessment, comprehensive [default: comprehensive].
`time_horizon` (optional) sets the investment timeframe consideration , options: short_term,
medium_term, long_term, multi_cycle [default: medium_term]. `geographic_scope` (optional) sets the
regional focus , options: us_focused, european, asian, emerging_markets, global [default: global].
With no arguments, open by asking which economic puzzle the user is trying to solve.

## Approach

1. **Load the economic knowledge** , Use the `qd-masters:master-economist` skill.
2. **Read the data** , identify the relevant indicators, cross-market signals, and the cycle phase
   bearing on `$ARGUMENTS`.
3. **Apply a framework** , select the fitting model from the skill (business-cycle analysis,
   monetary theory, behavioural economics, global macro) and reason through the policy and market
   implications.
4. **Deliver guidance** , give a scenario-weighted view with probabilities, the systemic risks, and
   the strategic positioning, in the skill's accessible, historically-grounded style.

## Opening (when no args)

"Economics is the study of human behaviour under conditions of scarcity , and right now, clarity
about the future is our scarcest resource. What economic puzzle are you trying to solve?"

## Examples

```bash
# Comprehensive medium-term global macro read
/qd-masters:master-economist analysis_focus=comprehensive time_horizon=medium_term geographic_scope=global
```

---

- Skill: `qd-masters:master-economist` (owns the frameworks, domains, and macroeconomic knowledge)
