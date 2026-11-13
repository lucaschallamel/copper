---
description: Comprehensive code quality and security review for Python projects
---

# /cu:quality-review

Initiate comprehensive code quality and security review for: **$ARGUMENTS**

---

## Overview

This command orchestrates a thorough code quality and security review covering code quality,
security vulnerabilities, test coverage, and performance considerations.

---

## Delegation & Execution Model

**How this command MUST be executed** (US-395). Read
`${CLAUDE_PLUGIN_ROOT}/skills/framework-authoring/resources/fresh-context-review.md` first: it is the single
home of the rule summarised here.

### Fresh reviewer first, then the author

If your prompt names you as the fresh reviewer, do not start another reviewer and skip the author
step: review, and report as the fresh reviewer.

1. **Fresh reviewer**: start a separate subagent for this review, never a fork or other
   context-inheriting mode, with a prompt of paths only (this command, the story file, the diff
   against the merge base or the changed files, the ADRs the story names, the resource above). Never
   pass the build conversation, the plan rationale, the author's self-review or earlier findings.
   Its report opens with an `## Inputs` section listing exactly what it was given.
2. **Author**: the agent that loaded this command then reviews the same scope itself and adds
   findings the fresh reviewer did not raise.
3. **One report**: findings from both in one table with a `Source` column (`fresh`, `author`, or
   `fresh, author`; duplicates merged at the higher severity).

When no fresh reviewer is possible (the host has no subagent tool, the reviewer cannot start, the
host's subagent isolation is not measured, or the reviewer was given anything the exclusions list),
the author reviews alone and the report's Inputs section opens with `Not independent: <reason>`. A
review that is not independent is never presented as independent.

| Use Case                            | Correct `subagent_type`                  | Why                                                                                                                                                    |
| ----------------------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Fresh reviewer (default)            | `general-purpose`                        | General-purpose agent, starts with no conversation (always available on Claude Code); never `fork`, which inherits the conversation                    |
| Specialist perspective (if present) | a specialist agent from an installed kit | Only if the adopter installed a kit that ships a matching SME agent (e.g. quality-testing or enterprise-architecture); otherwise use `general-purpose` |

`Explore` reads excerpts and cannot produce findings; it is not a reviewer.

### Prohibited: Non-Existent Agent Types

**NEVER** use `code-reviewer` as a `subagent_type`. This agent does not exist in the framework. The
string `code-reviewer` appears in some pipeline audit-trail YAMLs (e.g. US-166, US-191) as a
**descriptive reviewer label**, not as an agent type identifier. Do not infer Task `subagent_type`
values from those labels.

> If you are unsure whether an agent type exists, check the available agents list. Attempting to
> spawn a non-existent agent type is a hard error that blocks the pipeline.

---

## Phase 1: Context Discovery

First, identify the review scope:

1. **Target**: File path, directory, module, or "all" for full codebase
2. **Focus**: Specific concerns (e.g., "API security", "data models", "serialisation")
3. **Depth**: "quick" (surface issues), "standard" (balanced), "thorough" (exhaustive)

Read relevant files to understand:

- Current code structure and patterns
- Existing test coverage
- Related ADRs and architectural decisions

---

## Phase 2: Multi-Dimensional Review

### Code Quality & Maintainability

- Clean code principles (SOLID, DRY, KISS)
- Code complexity and cognitive load
- Naming conventions and readability
- Error handling patterns
- Code duplication detection
- Technical debt identification

### Security Vulnerabilities & Compliance

The security method is the core `cu:security-audit` skill in guidance mode
(`${CLAUDE_PLUGIN_ROOT}/skills/security-audit/SKILL.md`, US-393): load it and use the parts that fit the change
(its attack classes and the domain companions the change touches). A finding needs a concrete trust
boundary, an affected principal or resource and a security outcome; a candidate without them is not
a confirmed finding. Guidance mode writes no files; a full audit runs only at `/cu:pipe` S5 for a
security-sensitive story, or on the maintainer's explicit request. This review never runs target
code without the sandbox controls the skill lists; without them, it stays source-only and says so.
Regulatory checks (data-protection law) stay with the project's compliance rules.

### Test Coverage & Quality Assurance

- Unit test coverage gaps
- Integration test opportunities
- Edge case identification
- Test quality assessment
- Missing assertion patterns

### Performance & Efficiency

- Algorithmic complexity issues
- Memory management concerns
- I/O bottlenecks
- Database query optimisation
- Caching opportunities
- Resource leaks

---

## Phase 3: Review Criteria

### A. Code Quality Assessment

```
- [ ] Functions/methods ≤30 lines
- [ ] Files ≤300 lines (excluding tests)
- [ ] Cyclomatic complexity <10
- [ ] No code duplication >5 lines
- [ ] Consistent naming conventions
- [ ] Appropriate abstraction levels
```

### B. Security Assessment

Apply the `cu:security-audit` skill (Phase 2 above) and report each confirmed finding with its trust
boundary, principal, outcome and source path. The report keeps its Security row.

### C. Test Quality Assessment

```
- [ ] Unit test coverage ≥80%
- [ ] Integration test coverage ≥70%
- [ ] Edge cases covered
- [ ] Error paths tested
```

### D. Performance Assessment

```
- [ ] No O(n²) or worse in hot paths
- [ ] Appropriate data structures used
- [ ] Connection pooling configured
- [ ] No memory leaks detected
```

---

## Phase 4: Findings Classification

| Level       | Description                            | Action Required            |
| ----------- | -------------------------------------- | -------------------------- |
| 🔴 Critical | Security vulnerability, data loss risk | Immediate fix before merge |
| 🟠 High     | Significant quality/performance issue  | Fix in current sprint      |
| 🟡 Medium   | Code smell, maintainability concern    | Plan for near-term fix     |
| 🟢 Low      | Minor improvement opportunity          | Nice-to-have               |
| ℹ️ Info     | Observation, no action needed          | For awareness              |

---

## Output Format

```markdown
# Code Quality & Security Review Report

## Inputs

- Reviewer: fresh subagent (`general-purpose`) | Not independent: <reason>
- Review command, story file, diff range or changed files, ADRs, any other prompt text (verbatim)

## Executive Summary

- **Review Scope**: [Target description]
- **Review Date**: [Date]
- **Overall Risk Level**: [Critical/High/Medium/Low]

## Critical Findings (🔴)

1. [Finding with file:line reference]
   - **Issue**: [Description]
   - **Risk**: [Impact]
   - **Fix**: [Recommended action]

## High Priority Findings (🟠)

[List with file:line references]

## Metrics Summary

| Metric                | Current | Target     | Status |
| --------------------- | ------- | ---------- | ------ |
| Unit Test Coverage    | X%      | ≥80%       | ✅/❌  |
| Cyclomatic Complexity | X       | <10        | ✅/❌  |
| Security Issues       | X       | 0 critical | ✅/❌  |

## Recommended Actions

1. [ ] [Action item with priority]
2. [ ] [Action item with priority]
```

---

## Example Usage

```bash
# Review specific file
/cu:quality-review internal-projects/laap-reference-database/src/refdb/core/config.py

# Review entire module
/cu:quality-review internal-projects/laap-reference-database/src/ --depth=thorough

# Review with specific focus
/cu:quality-review internal-projects/laap-reference-database/ --focus="security"

# Full codebase review
/cu:quality-review all --depth=standard
```

---

## Structured Output

**Purpose**: Provide machine-parseable output that cu-pipe and other orchestrators can consume to
determine pass/fail status without interpreting free-form text.

### Required Output Block

At the end of every review, include a structured block in this exact format:

```markdown
## Structured Findings

**Overall Status**: PASS | FAIL **Total Findings**: <count> (Critical: <n>, High: <n>, Medium: <n>,
Low: <n>, Info: <n>)

| #   | Severity  | Source | File             | Issue                    | Recommendation         |
| --- | --------- | ------ | ---------------- | ------------------------ | ---------------------- |
| 1   | 🟠 High   | fresh  | path/to/file:42  | Description of the issue | Recommended fix action |
| 2   | 🟡 Medium | author | path/to/file:108 | Description of the issue | Recommended fix action |

### Exit Guidance

- **On PASS**: No critical or high findings. Review is complete.
- **On FAIL**: One or more critical or high findings exist. These must be resolved before the
  consuming pipeline stage can advance. If the consuming pipeline stage is S4_CODE_REVIEW via
  `/cu:pipe`, cu-pipe will record the FAIL status and require resolution before allowing stage
  advancement.
```

### Pass/Fail Rules

- **PASS**: Zero critical and zero high severity findings
- **FAIL**: One or more critical or high severity findings

### Consumer Contract

Orchestrators (e.g. cu-pipe) consuming this command's output MUST:

1. Scan for the `**Overall Status**:` line to determine pass/fail
2. Extract the findings table for evidence recording
3. On FAIL: present findings to the user and block stage advancement
4. On PASS: record findings as evidence and allow stage advancement

---

## Linting Commands Reference

```bash
# Python linting
cd internal-projects/laap-reference-database
ruff check src/ tests/
black --check src/ tests/
mypy src/

# Full lint with auto-fix
./_scripts/lint.sh --fix
```

---
