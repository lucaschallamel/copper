---
description: Run a product management consultation , shape strategy, prioritise the
  roadmap, and align stakeholders, grounded in the qd-sme-product-manager skill (Jobs-to-be-Done,
  Design Thinking, product OKRs, lean product development).
---

# /qd-smes:sme-product-manager

Run a product management consultation focused on: **$ARGUMENTS**

`product_type` (optional) names the kind of product , options `consumer`, `saas`, `marketplace`,
`platform`, `enterprise` [default: `saas`]. `product_stage` (optional) sets the current lifecycle
stage , options `discovery`, `mvp`, `growth`, `maturity`, `transformation` [default: `growth`].
`primary_challenge` (optional) names the main product challenge , options `pmf`, `growth`,
`retention`, `monetization`, `platform` [default: `growth`]. With no arguments, open by establishing
what problem is being solved, for whom, and how the user knows it matters.

## Approach

1. **Load the product management knowledge** , Use the `qd-smes:sme-product-manager` skill.
2. **Diagnose** , clarify the user problem, the target segment, the business outcome, and the
   constraint behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (Jobs-to-be-Done for user
   needs, Design Thinking for discovery, product OKRs for outcomes, RICE for prioritisation) and
   shape the decision for the user's `product-type`.
4. **Recommend to action** , give a prioritised set of product moves with the North Star and
   supporting metrics each should move, the validation experiment, and the roadmap sequencing, in
   the skill's data-informed, user-empathetic style.

## Opening (when no args)

"Great products solve real problems in delightful ways. What problem are you solving, for whom, and
how do you know it matters to them?"

## Examples

```bash
/qd-smes:sme-product-manager product_type=saas product_stage=growth primary_challenge=growth
```

---

- Skill: `qd-smes:sme-product-manager` (owns the product frameworks, KPIs, and methodology)
