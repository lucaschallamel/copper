---
description: Run a marketing consultation , diagnose growth gaps, design brand and
  demand programmes, and improve marketing metrics, grounded in the qd-sme-marketing
  skill (jobs-to-be-done, brand pyramid, AARRR).
---

Run a marketing consultation focused on: **$ARGUMENTS**

`company_stage` (optional) sets the company lifecycle stage [default: `growth`] , one of `startup`,
`growth`, `scale`, `enterprise`, `transformation`. `marketing_focus` (optional) sets the primary
marketing priority [default: `growth`] , one of `brand`, `growth`, `product`, `content`, `digital`.
`industry` (optional) sets the industry vertical [default: `b2b_saas`] , one of `b2b_saas`, `b2c`,
`ecommerce`, `marketplace`, `enterprise`. With no arguments, open by exploring what is preventing
the marketing function from driving the growth the business deserves.

## Approach

1. **Load the marketing knowledge** , Use the `qd-smes:sme-marketing` skill.
2. **Diagnose** , clarify the current funnel, the AARRR and CAC:LTV picture, and the specific growth
   bottleneck behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (jobs-to-be-done for
   positioning, brand pyramid for identity, AARRR for funnel optimisation) and shape it to the
   `channel` mix.
4. **Recommend to action** , give a prioritised set of campaign and operations steps with the metric
   each should move and the brief or dashboard to produce, in the skill's data-informed creative
   style.

## Opening (when no args)

"Great marketing creates customers who create customers. What is preventing your marketing from
driving the growth your business deserves?"

## Examples

```bash
# Growth-stage B2B SaaS optimising the growth engine
/qd-smes:sme-marketing company_stage=growth marketing_focus=growth industry=b2b_saas
```

---

- Skill: `qd-smes:sme-marketing` (owns the marketing methodology, KPIs, and growth frameworks)
