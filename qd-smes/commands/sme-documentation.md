---
description: Run an information-systems consultation , design architecture, enforce
  documentation governance, and systematise projects, grounded in the qd-sme-documentation
  skill (3-digit hierarchy, PRINCE2/PMI, AI-friendly taxonomy, living documentation).
---

Run an information-systems consultation focused on: **$ARGUMENTS**

All arguments are optional:

- `organization_stage` , current company maturity level [default: growth]. Options: `startup`,
  `growth`, `scale`, `enterprise`.
- `primary_need` , the most pressing documentation challenge [default: structure]. Options:
  `structure`, `compliance`, `scaling`, `automation`, `integration`.
- `industry_type` , industry-specific requirements [default: tech]. Options: `tech`, `saas`,
  `professional_services`, `healthcare`, `finance`.

With no arguments, open by understanding the current state, growth trajectory, and the biggest
documentation or organisational pain point.

## Approach

1. **Load the information-systems knowledge** , Use the `qd-smes:sme-documentation` skill.
2. **Diagnose** , clarify the current structure, the KPIs (documentation coverage, retrieval speed,
   compliance rate, scalability, AI compatibility), and the specific gap behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (the 3-digit hierarchical
   system for structure, AI-friendly taxonomy for naming, living documentation for governance,
   PRINCE2/PMI for projects) and shape the concrete design for the user's `stage`.
4. **Recommend to action** , give a prioritised set of steps with the metric each should move and
   the folder structure, template, or governance rule to produce, in the skill's systematic,
   pragmatic style.

## Opening (when no args)

"Let's transform your information chaos into a scalable system. I'll need to understand your current
state, growth trajectory, and pain points. What's your biggest documentation or organisational
challenge right now?"

## Examples

```bash
# Growth-stage tech company that needs a foundational information structure
/qd-smes:sme-documentation organization_stage=growth primary_need=structure industry_type=tech
```

---

- Skill: `qd-smes:sme-documentation` (owns the information-architecture methodology, KPIs, and
  frameworks)
