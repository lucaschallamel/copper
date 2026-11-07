---
description: Run a security audit , detect vulnerabilities, review code for security,
  and validate compliance with scored findings and remediation, grounded in the gd-security-analyzer
  skill and its bundled review checklist.
---

Run a security audit on: **$ARGUMENTS**

All arguments are optional. `severity_filter` (default `medium`; options: `low`, `medium`, `high`,
`critical`) sets the minimum severity reported; `compliance_framework` (default `owasp`; options:
`owasp`, `pci_dss`, `hipaa`, `sox`, `gdpr`, `soc2`, `iso27001`, `nist_csf`) sets the standard to
validate against; `validation_level` (default `standard`; options: `basic`, `standard`, `strict`,
`enterprise`); `output_format` (default `detailed`; options: `summary`, `detailed`, `executive`,
`technical`). With no arguments, ask for the audit target and scope.

## Approach

1. **Load the security knowledge** , Use the `gd-security:security-analyzer` skill.
2. **Scope** , confirm the target behind `$ARGUMENTS` (web app, API, code path, infrastructure) and
   the `compliance_framework` to validate against.
3. **Review** , work the bundled `references/security-review-checklist.md` domain by domain (OWASP
   Top 10, authentication, input validation, cryptography, headers and CORS, compliance) at the
   requested `validation_level`, grounding each finding in evidence.
4. **Report** , emit findings at or above `severity_filter` in the requested `output_format`, each
   with severity, CVSS, business impact, and developer-friendly remediation including secure code
   examples.

## Examples

```bash
# Vulnerability scan of a web application, high-severity findings only
/gd-security:security-analyzer severity_filter=high

# SOC2 compliance audit of API endpoints
/gd-security:security-analyzer compliance_framework=soc2

# Enterprise-grade code review of an authentication module
/gd-security:security-analyzer validation_level=enterprise
```

## Opening (when no args)

"Let's audit your application's security. What is the target , a codebase path, an API, or a running
system , and which compliance framework should I validate against?"

---

- Skill: `gd-security:security-analyzer` (owns the methodologies, the checklist, and the security
  knowledge)
- Related agent: the proactive `gd-security:security-analyzer` agent loads the same skill autonomously.
