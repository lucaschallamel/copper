---
description: Run a UX consultation , define experience strategy, plan research, and
  shape interactions, grounded in the qd-sme-ux skill (Design Thinking, Jobs-to-be-Done,
  Atomic Design, Lean UX).
---

Run a UX consultation focused on: **$ARGUMENTS**

Optional arguments:

- `design_focus` (string): primary design domain [default: `product_design`]. Options:
  `product_design`, `design_systems`, `research`, `service_design`, `strategy`.
- `platform` (string): primary platform focus [default: `multi_platform`]. Options: `web`, `mobile`,
  `desktop`, `multi_platform`, `emerging`.
- `design_maturity` (string): organisation's design maturity [default: `growing`]. Options:
  `nascent`, `growing`, `established`, `leading`, `transforming`.

With no arguments, open by establishing what experience the user is creating and what is preventing
it from delighting their users.

## Approach

1. **Load the UX knowledge** , Use the `qd-smes:sme-ux` skill.
2. **Diagnose** , clarify the current experience, the user research and usability state, and the
   specific friction behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (Design Thinking for the
   process, Jobs-to-be-Done for motivation, Atomic Design for the system, Lean UX for validation)
   and design the plan for the user's `product`.
4. **Recommend to action** , give a prioritised set of design steps with the metric each should move
   and the prototype, journey map, or research artefact to produce, in the skill's storytelling,
   user-centred style.

## Opening (when no args)

"Great design makes the complex feel simple and the mundane feel magical. What experience are you
creating, and what is preventing it from delighting your users?"

## Examples

```bash
# Product design across multiple platforms for an organisation with a growing design practice
/qd-smes:sme-ux design_focus=product_design platform=multi_platform design_maturity=growing
```

---

- Skill: `qd-smes:sme-ux` (owns the UX methodology, KPIs, and frameworks)
