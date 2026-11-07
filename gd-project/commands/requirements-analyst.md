---
description: Run a requirements-analysis session , elicit, specify, validate, and
  trace requirements from ambiguous business vision to development-ready specification,
  grounded in the gd-requirements-analyst skill.
---

Elicit and analyse requirements for: **$ARGUMENTS**

All arguments are optional. `stakeholder_count` (default `5`; number of stakeholders involved, range
1-50); `domain_complexity` (default `medium`; options: `low`, `medium`, `high`, `expert`);
`compliance_requirements` (default `none`; regulatory compliance needs, options: `gdpr`, `hipaa`,
`sox`, `pci`, `iso27001`, `none`); `validation_level` (default `standard`; validation strictness,
options: `basic`, `standard`, `strict`, `enterprise`); `timeline_constraint` (default `normal`;
project timeline pressure, options: `tight`, `normal`, `flexible`). With no arguments, open by
drawing out the stakeholders, the business goal, and the ambiguities behind the request.

## Approach

1. **Load the requirements knowledge** , Use the `gd-project:requirements-analyst` skill.
2. **Frame the problem** , clarify the stakeholders behind `$ARGUMENTS`, the business vision, the
   domain constraints, and what already exists.
3. **Elicit and specify** , apply the fitting techniques from the skill (interviews, workshops,
   jobs-to-be-done, impact mapping) at the chosen `domain_complexity`, and capture layered
   requirements with bi-directional traceability.
4. **Validate and document** , at the requested `validation_level`, verify each requirement is
   complete, consistent, feasible, and testable; map any `compliance_requirements`; and deliver a
   specification with acceptance criteria and a traceability matrix.

## Opening (when no args)

"Let's turn this vision into requirements your developers will trust and your testers can verify.
Who are the stakeholders, what business outcome are we after, and where is the request still
ambiguous or in tension?"

## Examples

```bash
# Comprehensive analysis for a web app with many stakeholders
/gd-project:requirements-analyst domain_complexity=high stakeholder_count=12 validation_level=standard

# Mobile app requiring enterprise-grade validation
/gd-project:requirements-analyst domain_complexity=medium validation_level=enterprise

# Enterprise transformation under tight timeline pressure
/gd-project:requirements-analyst domain_complexity=expert validation_level=enterprise timeline_constraint=tight
```

---

- Skill: `gd-project:requirements-analyst` (owns the methodologies, frameworks, and KPIs)
- Related agent: the proactive `gd-project:requirements-analyst` agent loads the same skill autonomously.
