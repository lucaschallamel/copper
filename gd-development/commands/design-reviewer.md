---
description: Run a design review , validate a system design, find flaws and failure
  modes, quantify risk, and synthesise alternatives, grounded in the gd-design-reviewer
  skill (ATAM, evidence-based review, multi-criteria scoring).
---

Run a design review for: **$ARGUMENTS**

All arguments are optional. `review_depth` (default `comprehensive`; options: `quick-scan`,
`standard`, `comprehensive`, `forensic`, `evidence-based`); `focus_areas` (default `balanced`;
options: `balanced`, `performance`, `security`, `scalability`, `maintainability`, `configuration`,
`quality-gates`); `design_stage` (default `detailed`; options: `conceptual`, `high-level`,
`detailed`, `final`); `validation_level` (default `standard`; options: `basic`, `standard`,
`strict`, `enterprise`); `quality_framework` (default `multi-criteria`; options: `functional`,
`structural`, `performance`, `security`, `multi-criteria`, `evidence-driven`) sets the
quality-assessment approach. With no arguments, ask for the design document or architecture to
review and its stage.

## Approach

1. **Load the design-review knowledge** , Use the `gd-development:design-reviewer` skill.
2. **Scope** , confirm the design behind `$ARGUMENTS`, its `design_stage`, and the `focus_areas` that
   carry the most risk.
3. **Review** , run the validation cycle at the chosen `review_depth`, applying ATAM trade-off
   analysis, anti-pattern recognition, and configuration-vulnerability checks, grounding each
   finding in evidence.
4. **Quantify and synthesise** , at the requested `validation_level`, score risk with a
   multi-criteria matrix, require a rollback strategy and load-testing evidence for scale-bound
   designs, and pair every critical finding with evidence-backed alternatives.

## Examples

```text
# Evidence-based review focused on configuration, multi-criteria scoring
/gd-development:design-reviewer review_depth=evidence-based focus_areas=configuration quality_framework=multi-criteria

# Validation-cycle review of a final design, focused on quality gates
/gd-development:design-reviewer validation_level=strict design_stage=final focus_areas=quality-gates
```

## Opening (when no args)

"Let's validate this design before it becomes a production problem. Share the design document or
architecture, tell me its stage (conceptual to final), and where you are most concerned ,
performance, security, scalability, or configuration."

---

- Skill: `gd-development:design-reviewer` (owns the methodologies, the validation cycle, and the safety
  rules)
- Related agent: the proactive `gd-development:design-reviewer` agent loads the same skill autonomously.
