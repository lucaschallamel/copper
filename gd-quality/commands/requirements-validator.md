---
description: Run a requirements-validation session , execute the 8-step validation
  cycle to check completeness, consistency, testability, and compliance, grounded
  in the gd-requirements-validator skill (IEEE 830, ISO/IEC 29148, SMART+, traceability).
---

Run a requirements-validation session for: **$ARGUMENTS**

All arguments are optional. `validation_rigor` (default `comprehensive`; options: `quick-check`,
`standard`, `comprehensive`, `formal-methods`); `domain_standards` (default `general`; options:
`general`, `aerospace`, `medical`, `financial`, `automotive`); `focus_areas` (default `all`;
options: `all`, `safety-critical`, `security`, `performance`, `compliance`); `evidence_mode`
(default `standard`; options: `minimal`, `standard`, `comprehensive`, `forensic`);
`validation_level` (default `standard`; options: `basic`, `standard`, `strict`, `enterprise`). With
no arguments, open by drawing out the requirements set, its domain, and the standards it must meet.

## Approach

1. **Load the validation knowledge** , Use the `gd-quality:requirements-validator` skill.
2. **Frame the set** , read the requirements behind `$ARGUMENTS`, clarify the domain, the applicable
   standards, and the highest-risk areas.
3. **Run the 8-step cycle** , at the requested `validation_rigor`, work through syntax, type
   consistency, quality, security, testability, feasibility, traceability, and integration, applying
   the `domain_standards` and `focus_areas`.
4. **Score and report** , at the requested `evidence_mode`, attach evidence and severity to each
   finding, then deliver a validation report with prioritised, actionable recommendations.

## Examples

```bash
# Safety-critical medical requirements with forensic evidence
/gd-quality:requirements-validator validation_rigor=comprehensive domain_standards=medical focus_areas=safety-critical evidence_mode=forensic

# Formal-methods validation at enterprise strictness
/gd-quality:requirements-validator validation_rigor=formal-methods validation_level=enterprise evidence_mode=comprehensive

# Aerospace compliance focus at strict validation
/gd-quality:requirements-validator domain_standards=aerospace focus_areas=compliance validation_level=strict
```

## Opening (when no args)

"Let's catch the requirement flaws now, before they become expensive rework. Which requirements are
we validating, what domain are they in, and which standards must they satisfy?"

---

- Skill: `gd-quality:requirements-validator` (owns the 8-step cycle, methodologies, and validation
  knowledge)
- Related agent: the proactive `gd-quality:requirements-validator` agent loads the same skill autonomously.
