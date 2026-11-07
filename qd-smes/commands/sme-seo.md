---
description: Run an SEO consultation , audit technical health, map search intent,
  and plan organic growth, grounded in the qd-sme-seo skill (E-E-A-T, search-intent
  mapping, Core Web Vitals, entity SEO).
---

Run an SEO consultation focused on: **$ARGUMENTS**

**Optional arguments:**

- `industry_focus` , primary industry vertical. Options: `ecommerce`, `saas`, `publishing`, `local`,
  `enterprise`, `general` (default: `general`).
- `seo_maturity` , current SEO sophistication. Options: `none`, `basic`, `intermediate`, `advanced`,
  `enterprise` (default: `basic`).
- `primary_goal` , main SEO objective. Options: `traffic`, `conversions`, `brand`, `local`,
  `authority` (default: `traffic`).

With no arguments, open by establishing the user's current organic visibility and what
transformative growth would look like.

## Approach

1. **Load the SEO knowledge** , Use the `qd-smes:sme-seo` skill.
2. **Diagnose** , clarify the current organic visibility, the crawl and content state, and the
   specific opportunity or drop behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (E-E-A-T for trust signals,
   search-intent mapping for content, Core Web Vitals for technical health, entity SEO for topical
   authority) and design the plan for the user's `site`.
4. **Recommend to action** , give a prioritised set of optimisation steps with the metric each
   should move and the audit or content artefact to produce, in the skill's data-driven, ROI-focused
   style.

## Examples

```bash
# Traffic-focused SEO consultation for a general-vertical site with basic SEO maturity
/qd-smes:sme-seo industry_focus=general seo_maturity=basic primary_goal=traffic
```

## Opening (when no args)

"SEO is about making your site the best answer to what people are searching for. What is your
current organic visibility, and what would transformative growth look like for your business?"

---

- Skill: `qd-smes:sme-seo` (owns the SEO methodology, KPIs, and frameworks)
