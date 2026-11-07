---
description: Run a memory-optimisation session , audit, restructure, and compress
  project knowledge for fast retrieval, grounded in the gd-memory-manager skill (information
  architecture, DIKW, conciseness protocol).
---

Audit and optimise project memory for: **$ARGUMENTS**

All arguments are optional. `optimization_strategy` (default `balanced`; options: `aggressive`,
`balanced`, `conservative`, `archival`); `focus_area` (default `all`; options: `all`, `technical`,
`decisions`, `requirements`, `architecture`); `retention_period` (default `relevant`; options:
`current`, `recent`, `relevant`, `complete`); `validation_level` (default `standard`; options:
`basic`, `standard`, `strict`, `enterprise`). With no arguments, open by surveying the current
memory footprint and what is hard to find.

## Approach

1. **Load the memory knowledge** , Use the `gd-framework:memory-manager` skill.
2. **Audit** , survey the project memory behind `$ARGUMENTS` for redundancy, decay, and gaps, scoped
   by `focus_area` and `retention_period`.
3. **Restructure** , at the chosen `optimization_strategy`, apply the fitting model from the skill
   (DIKW, Zettelkasten, MECE, faceted classification) and the conciseness protocol to compress and
   reorganise.
4. **Validate** , at the requested `validation_level`, confirm all critical information is preserved
   and retrieval is fast, then deliver the optimised architecture.

## Opening (when no args)

"Let's tidy your project memory. How large has it grown, and what is currently hard to find , past
decisions, architecture, requirements, or all of it?"

## Examples

```bash
# Balanced optimisation focused on architecture knowledge
/gd-framework:memory-manager optimization_strategy=balanced focus_area=architecture

# Enterprise-strict validation pass over project memory
/gd-framework:memory-manager validation_level=enterprise
```

---

- Skill: `gd-framework:memory-manager` (owns the methodologies, the conciseness protocol, and the
  memory knowledge)
- Related agent: the proactive `gd-framework:memory-manager` agent loads the same skill autonomously.
