---
description: Run a refactoring session , restructure code, reduce technical debt,
  and apply design patterns with behaviour preservation, grounded in the gd-code-refactoring-specialist
  skill (SOLID, Fowler's catalogue, incremental transformation).
---

Run a refactoring session for: **$ARGUMENTS**

All arguments are optional. `refactoring_type` (default `structural`; options: `structural`,
`behavioural`, `performance`, `architectural`) sets the kind of change; `refactoring_focus` (default
`general`) names the primary objective (e.g. readability, debt, patterns, performance);
`risk_tolerance` (default `conservative`; options: `conservative`, `balanced`, `aggressive`);
`scope` (default `targeted`; options: `targeted`, `module`, `service`, `system`); `testing_strategy`
(default `comprehensive`) sets the safety-net approach (characterisation, mutation, regression);
`language` (default `auto-detect`; options: `java`, `python`, `javascript`, `typescript`, `csharp`,
`go`, `rust`); `project_context` (default `general`; options: `greenfield`, `brownfield`, `legacy`,
`microservices`, `monolith`). With no arguments, ask which code needs restructuring and what the
goal is.

## Approach

1. **Load the refactoring knowledge** , Use the `gd-development:code-refactoring-specialist` skill.
2. **Analyse** , identify the smells, anti-patterns, and violations behind `$ARGUMENTS`, and confirm a
   characterisation-test net exists before changing behaviour.
3. **Transform** , apply the fitting patterns at the chosen `refactoring_type` and `scope`, in small
   reversible increments matching `risk_tolerance`, keeping tests green between steps.
4. **Validate and document** , confirm behaviour preservation, remove superseded implementations,
   and deliver a before/after summary with the rationale.

## Examples

```text
# Structural refactoring of a legacy Java codebase
/gd-development:code-refactoring-specialist refactoring_type=structural language=java project_context=legacy

# Performance refactoring of a Python microservice
/gd-development:code-refactoring-specialist refactoring_type=performance language=python project_context=microservices
```

## Opening (when no args)

"Let's improve this code without changing what it does. Which file, module, or service should we
refactor, what is the goal (readability, debt, patterns, performance), and how much test coverage is
in place?"

---

- Skill: `gd-development:code-refactoring-specialist` (owns the methodologies, the patterns, and the
  safety rules)
- Related agent: the proactive `gd-development:code-refactoring-specialist` agent loads the same skill
  autonomously.
