---
description: Run a product-strategy session , define vision, build an outcome-driven
  roadmap, prioritise features, and analyse the market, grounded in the gd-product-strategy-advisor
  skill.
---

Develop product strategy for: **$ARGUMENTS**

`product_stage` is required (the current product lifecycle stage; options: `ideation`, `mvp`,
`growth`, `maturity`, `transformation`). The remaining arguments are optional. `market_type`
(default `b2b`; options: `b2b`, `b2c`, `b2b2c`, `developer`, `enterprise`); `strategy_focus`
(default `growth`; options: `growth`, `retention`, `monetization`, `expansion`, `pivot`);
`complexity` (default `standard`; options: `simple`, `standard`, `complex`, `platform`). With no
arguments, open by drawing out the product's stage, target market, and the outcome the strategy must
move.

## Approach

1. **Load the product-strategy knowledge** , Use the `gd-project:product-strategy-advisor` skill.
2. **Frame the strategy** , clarify the `product_stage`, the `market_type`, the customers, and the
   strategic objective behind `$ARGUMENTS`, grounded in evidence of customer value and market need.
3. **Build the plan** , apply the fitting models from the skill (Lean Canvas, Porter's Five Forces,
   TAM/SAM/SOM, RICE/Kano/JTBD prioritisation, North Star and AARRR metrics) to the chosen
   `strategy_focus` and `complexity`, and produce an outcome-driven roadmap.
4. **Prioritise to outcomes** , give a transparently prioritised set of bets with the metric each
   should move and the assumptions behind it.

## Opening (when no args)

"Let's build a strategy your team can rally behind and your market will reward. What stage is the
product at, who is the target market, and what outcome , growth, retention, expansion , are we
playing for?"

## Examples

```bash
# Growth-stage B2B expansion strategy
/gd-project:product-strategy-advisor product_stage=growth market_type=b2b strategy_focus=expansion

# Simple B2C MVP strategy
/gd-project:product-strategy-advisor product_stage=mvp market_type=b2c complexity=simple

# Mature product retention strategy
/gd-project:product-strategy-advisor product_stage=maturity strategy_focus=retention
```

---

- Skill: `gd-project:product-strategy-advisor` (owns the methodologies, frameworks, and KPIs)
- Related agent: the proactive `gd-project:product-strategy-advisor` agent loads the same skill
  autonomously.
