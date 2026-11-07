---
description: Run an interface-design session , produce accessible wireframes, user
  flows, and design-system guidance with WCAG compliance, grounded in the gd-interface-designer
  skill (Design Thinking, Atomic Design, WCAG 2.1).
---

Run an interface-design session for: **$ARGUMENTS**

All arguments are optional. `interface_type` (default `web`; options: `web`, `mobile`, `api`,
`desktop`, `cross-platform`); `accessibility_level` (default `wcag-aa`; options: `basic`, `wcag-a`,
`wcag-aa`, `wcag-aaa`, `section-508`); `design_complexity` (default `moderate`; options: `simple`,
`moderate`, `complex`, `enterprise`); `validation_level` (default `standard`; options: `basic`,
`standard`, `strict`, `enterprise`). With no arguments, ask who the users are and what problem the
interface must solve.

## Approach

1. **Load the interface-design knowledge** , Use the `gd-development:interface-designer` skill.
2. **Understand** , clarify the users, their problem, and the constraints behind `$ARGUMENTS`, and the
   target `interface_type`.
3. **Design** , produce user flows and annotated wireframes using progressive disclosure for the
   chosen `design_complexity`, building accessibility in from the start for `accessibility_level`.
4. **Validate** , at the requested `validation_level`, check against WCAG, run usability heuristics
   or testing, and deliver design rationale and accessibility requirements for implementers.

## Examples

```text
# Web interface targeting WCAG AA
/gd-development:interface-designer interface_type=web accessibility_level=wcag-aa

# Enterprise-grade validation of an interface design
/gd-development:interface-designer design_complexity=enterprise validation_level=enterprise
```

## Opening (when no args)

"Let's design an interface that solves a real user problem. Who are the users, what are they trying
to do, and which platform and accessibility level (WCAG AA by default) should it meet?"

---

- Skill: `gd-development:interface-designer` (owns the methodologies, the accessibility standards, and
  the safety rules)
- Related agent: the proactive `gd-development:interface-designer` agent loads the same skill autonomously.
