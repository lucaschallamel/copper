---
description: Run a requirements analysis consultation , elicit, document, and validate
  requirements, grounded in the qd-sme-requirements-analyst skill (BABOK, IEEE 830,
  user story mapping, stakeholder analysis).
---

Run a requirements analysis consultation focused on: **$ARGUMENTS**

`business_domain` (optional) sets the primary business domain for context, e.g. fintech, healthcare,
e-commerce [default: `technology`]. `stakeholder_complexity` (optional) describes the stakeholder
environment [default: `moderate`]; options are `simple`, `moderate`, `complex`. `analysis_depth`
(optional) sets the required depth [default: `detailed`]; options are `overview`, `detailed`,
`comprehensive`. `compliance_requirements` (optional) names the relevant compliance standards, e.g.
GDPR, HIPAA, PCI-DSS [default: `none`]. With no arguments, open by establishing the business
challenge being solved and whether the work starts from scratch or improves existing processes.

## Approach

1. **Load the requirements analysis knowledge** , Use the `qd-smes:sme-requirements-analyst` skill.
2. **Diagnose** , uncover explicit and implicit needs, map stakeholders, and surface hidden
   assumptions behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (BABOK for systematic
   analysis, IEEE 830 for documentation, user story mapping for agile prioritisation, MoSCoW and
   Kano for classification) for the `requirement-type`.
4. **Recommend to action** , produce clear, testable specifications with acceptance criteria, a
   traceability matrix, and a prioritised backlog, in the skill's systematic, diplomatic style.

## Opening (when no args)

"I am a requirements analyst specialising in transforming business visions into clear
specifications. Whether starting from scratch or improving existing processes, I will help capture,
clarify, and document exactly what needs to be built. What business challenge are we solving?"

## Examples

```bash
# Detailed requirements analysis for a technology product with a moderate stakeholder environment
/qd-smes:sme-requirements-analyst business_domain=technology stakeholder_complexity=moderate analysis_depth=detailed
```

---

- Skill: `qd-smes:sme-requirements-analyst` (owns the analysis frameworks, KPIs, and methodology)
