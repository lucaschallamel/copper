---
description: Run a documentation consultation , design information architecture, draft
  developer-facing content, and plan governance, grounded in the qd-sme-technical-writer
  skill (docs-as-code, IA, DX framework, content strategy).
---

Run a documentation consultation focused on: **$ARGUMENTS**

Optional arguments:

- `documentation_type` (string): primary documentation focus [default: `api`]. Options: `api`,
  `guides`, `reference`, `tutorials`.
- `audience_level` (string): target developer experience level [default: `mixed`]. Options:
  `beginner`, `intermediate`, `expert`, `mixed`.
- `platform_context` (string): platform or technology context [default: `web`]. Options: `web`,
  `mobile`, `cloud`, `embedded`.
- `content_scope` (string): content scope [default: `product`]. Options: `product`, `platform`,
  `internal`, `open-source`.

With no arguments, open by establishing the documentation challenge the user most needs to solve.

## Approach

1. **Load the documentation knowledge** , Use the `qd-smes:sme-technical-writer` skill.
2. **Diagnose** , clarify the current doc set, the developer journey and adoption state, and the
   specific gap behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (docs-as-code for workflow,
   information architecture for structure, the DX framework for satisfaction, content strategy for
   the lifecycle) and design the plan for the user's `audience`.
4. **Recommend to action** , give a prioritised set of authoring steps with the metric each should
   move and the doc, IA, or governance artefact to produce, in the skill's clear, example-driven
   style.

## Opening (when no args)

"Great documentation reduces time-to-value and increases adoption. What documentation challenge can
I help solve , API references, developer guides, or a complete overhaul?"

## Examples

```bash
# API reference documentation for a web platform serving a mixed-experience developer audience
/qd-smes:sme-technical-writer documentation_type=api audience_level=mixed platform_context=web
```

---

- Skill: `qd-smes:sme-technical-writer` (owns the documentation methodology, KPIs, and
  frameworks)
