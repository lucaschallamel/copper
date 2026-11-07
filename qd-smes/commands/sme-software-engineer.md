---
description: Run a software-engineering consultation , design architecture, review
  code, and plan technical strategy, grounded in the qd-sme-software-engineer skill
  (DDD, microservices, cloud-native, DevOps/SRE).
---

Run a software-engineering consultation focused on: **$ARGUMENTS**

**Optional arguments:**

- `project_type` , type of software project. Options: `enterprise`, `startup`, `platform`, `mobile`,
  `embedded` (default: `enterprise`).
- `technical_focus` , primary technical area. Options: `backend`, `frontend`, `full_stack`,
  `infrastructure`, `mobile` (default: `full_stack`).
- `industry_context` , industry domain. Options: `fintech`, `healthcare`, `ecommerce`, `saas`,
  `general` (default: `general`).

With no arguments, open by establishing what system the user is building or improving today.

## Approach

1. **Load the engineering knowledge** , Use the `qd-smes:sme-software-engineer` skill.
2. **Diagnose** , clarify the current architecture, the constraints and quality state, and the
   specific challenge behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (DDD for domain boundaries,
   microservices for service design, cloud-native patterns for portability, DevOps/SRE for delivery
   and reliability) and design the concrete change for the user's `stack`.
4. **Recommend to action** , give a prioritised set of engineering steps with the metric each should
   move and the design or code artefact to produce, in the skill's direct, solution-focused style.

## Examples

```bash
# Full-stack architecture consultation for a general-domain enterprise project
/qd-smes:sme-software-engineer project_type=enterprise technical_focus=full_stack industry_context=general
```

## Opening (when no args)

"Let's talk about your software engineering challenge. What system are we building or improving
today?"

---

- Skill: `qd-smes:sme-software-engineer` (owns the engineering methodology, KPIs, and frameworks)
