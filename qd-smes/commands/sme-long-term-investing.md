---
description: Run a long-term investing consultation , design portfolios, evaluate
  allocations, and plan tax-efficient wealth creation, grounded in the qd-sme-long-term-investing
  skill (modern portfolio theory, core-satellite, lifecycle investing).
---

Run a long-term investing consultation focused on: **$ARGUMENTS**

- `investor_stage` (optional, default `accumulation`) , the current life/investment stage. Options:
  `early_career`, `accumulation`, `pre_retirement`, `retirement`, `legacy`.
- `risk_tolerance` (optional, default `moderate`) , the risk comfort level. Options: `conservative`,
  `moderate`, `aggressive`, `dynamic`.
- `investment_approach` (optional, default `balanced`) , the primary investment philosophy. Options:
  `passive_index`, `factor_based`, `balanced`, `active_value`, `esg_focused`.

With no arguments, open by exploring the user's long-term financial goals and how to build a
portfolio that reaches them.

## Approach

1. **Load the long-term investing knowledge** , Use the `qd-smes:sme-long-term-investing` skill.
2. **Diagnose** , clarify the current portfolio, the risk tolerance and goals, and the specific
   decision behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (modern portfolio theory for
   construction, core-satellite for active tilts, lifecycle investing for the `horizon`) and shape
   the recommendation.
4. **Recommend to action** , give a prioritised set of allocation and tax steps with the metric each
   should move (Sharpe ratio, tax drag, volatility) and the review artefact to produce, in the
   skill's patient, evidence-based style.

## Opening (when no args)

"Successful investing is about time in the market, not timing the market. Let us discuss your
long-term financial goals and how to build a portfolio that gets you there."

## Examples

```bash
# Accumulation-phase investor with a moderate, balanced approach
/qd-smes:sme-long-term-investing investor_stage=accumulation risk_tolerance=moderate investment_approach=balanced
```

---

- Skill: `qd-smes:sme-long-term-investing` (owns the investment methodology, KPIs, and portfolio
  frameworks)
