---
description: Run a test-suite generation session , produce maintainable, well-targeted
  tests with clear coverage goals, grounded in the gd-test-suite-generator skill (test
  pyramid, TDD/BDD, edge-case detection, quality gates).
---

Run a test-suite generation session for: **$ARGUMENTS**

All arguments are optional. `framework` (default `auto-detect`; options: `jest`, `pytest`, `junit`,
`mocha`, `rspec`, `cypress`); `coverage_target` (default `80`; range 50-100); `test_style` (default
`tdd`; options: `tdd`, `bdd`, `exploratory`); `test_focus` (default `comprehensive`; options:
`comprehensive`, `reproduction`, `regression`, `edge_cases`, `performance`); `validation_level`
(default `standard`; options: `basic`, `standard`, `strict`, `enterprise`); `validation` (validation
automation level, default `manual`; options: `manual`, `semi_automated`, `automated`,
`ai_assisted`); `test_types` (comma-separated, default `unit`; options: `unit`, `integration`,
`regression`, `e2e`, `performance`, `security`); `coverage` (coverage focus strategy, default
`standard`; options: `standard`, `fix_focused`, `comprehensive`, `critical_path`). With no
arguments, open by drawing out the code under test, its risk profile, and the existing test setup.

## Approach

1. **Load the test-generation knowledge** , Use the `gd-quality:test-suite-generator` skill.
2. **Frame the target** , read the code under test, the existing tests, and the framework already in
   use; clarify the risk profile and the critical paths behind `$ARGUMENTS`.
3. **Design the suite** , apply the fitting models from the skill (test pyramid, TDD/BDD, property
   and mutation testing) to the chosen `test_types` and `test_style`, focusing on edge cases and
   high-risk areas towards the `coverage_target`.
4. **Validate and harden** , at the requested `validation_level`, check determinism, isolation, and
   flaky-test risk, then deliver the tests with clear intent and quality-gate criteria.

## Examples

```bash
# Unit tests for UserService.js with Jest, targeting 95% coverage
/gd-quality:test-suite-generator framework=jest coverage_target=95 test_types=unit

# BDD integration tests for API endpoints at strict validation
/gd-quality:test-suite-generator test_style=bdd test_types=integration validation_level=strict

# End-to-end tests for the login flow with Cypress
/gd-quality:test-suite-generator framework=cypress test_types=e2e
```

## Opening (when no args)

"Let's build a test suite that catches real bugs without becoming a maintenance burden. What code
are we testing, what does it touch, and what test setup do you already have?"

---

- Skill: `gd-quality:test-suite-generator` (owns the methodologies, frameworks, and testing
  knowledge)
- Related agent: the proactive `gd-quality:test-suite-generator` agent loads the same skill autonomously.
