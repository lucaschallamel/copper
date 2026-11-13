---
description: Run a code review , find bugs, security issues, and quality problems
  with constructive, severity- scored feedback, grounded in the gd-code-reviewer skill
  (OWASP, clean code, SOLID, review pyramid).
---

Run a code review for: **$ARGUMENTS**

All arguments are optional. `review_scope` (default `comprehensive`; options: `security`,
`performance`, `architecture`, `quality`, `comprehensive`) sets what to emphasise; `severity_filter`
(default `medium`; options: `critical`, `high`, `medium`, `low`, `all`) sets the minimum severity
reported; `review_depth` (default `thorough`; options: `quick`, `standard`, `thorough`,
`exhaustive`); `language` (default `auto-detect`; options: `javascript`, `python`, `java`, `csharp`,
`go`, `rust`, `typescript`, `php`, `ruby`, `cpp`); `project_context` (default `general`; options:
`microservice`, `monolith`, `library`, `framework`, `mobile`, `cloud-native`). With no arguments,
ask for the code path or diff and the primary concern.

## Approach

1. **Load the code-review knowledge** , Use the `gd-development:code-reviewer` skill.
2. **Scope** , confirm the target behind `$ARGUMENTS` (file, diff, module), the `review_scope`, and
   the `language` and `project_context`.
3. **Review** , work the review pyramid (architecture, design, implementation, security) at the
   requested `review_depth`, grounding each finding in the code; the security layer applies the core
   `cu:security-audit` skill (Use the `cu:security-audit` skill.) and runs no target code without the
   sandbox controls it lists.
4. **Report** , emit findings at or above `severity_filter`, each with a severity level, the
   reasoning, and a concrete fix; flag any hardcoded secrets or critical issues lacking a
   remediation plan.

## Examples

```text
# Security-focused review for a Python microservice with OWASP compliance
/gd-development:code-reviewer review_scope=security language=python project_context=microservice severity_filter=high

# Comprehensive review of a cloud-native TypeScript service
/gd-development:code-reviewer review_scope=comprehensive language=typescript project_context=cloud-native

# Performance review of a mobile Java application, exhaustive depth
/gd-development:code-reviewer review_scope=performance language=java project_context=mobile review_depth=exhaustive
```

## Opening (when no args)

"Let's review your code. Point me at a file, diff, or module, and tell me what matters most ,
security, performance, architecture, or overall quality , and I'll return severity-scored findings
with fixes."

---

- Skill: `gd-development:code-reviewer` (owns the methodologies, the review pyramid, and the safety
  rules)
- Related agent: the proactive `gd-development:code-reviewer` agent loads the same skill autonomously.
