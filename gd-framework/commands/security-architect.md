---
description: Run a security-architecture design session , model threats, design controls,
  and align with a compliance framework, grounded in the gd-security-architect skill
  (zero trust, STRIDE, NIST CSF, compliance frameworks).
---

Design a security architecture for: **$ARGUMENTS**

All arguments are optional. `security_focus` (default `comprehensive`; options: `authentication`,
`data-protection`, `compliance`, `threat-defense`, `comprehensive`); `compliance_framework` (default
`general`; options: `general`, `gdpr`, `hipaa`, `pci-dss`, `sox`, `iso27001`); `threat_level`
(default `moderate`; options: `low`, `moderate`, `high`, `nation-state`, `insider`);
`validation_level` (default `standard`; options: `basic`, `standard`, `strict`, `enterprise`). With
no arguments, open by drawing out the system, its sensitive assets, and the threats and regulations
that apply.

## Approach

1. **Load the security-architecture knowledge** , Use the `gd-framework:security-architect` skill.
2. **Model threats** , for the system behind `$ARGUMENTS`, identify assets, trust boundaries, and
   threats (STRIDE or equivalent) at the chosen `threat_level`.
3. **Design controls** , apply the fitting models from the skill (zero trust, defence in depth,
   identity, data protection) to the `security_focus`, and map every control to the
   `compliance_framework`.
4. **Validate** , at the requested `validation_level`, check for single points of control, document
   residual risk, and deliver the architecture with a threat model and compliance mapping.

## Opening (when no args)

"Let's design security that fits your system and its regulators. What are you protecting, what are
the most sensitive assets, and which threats and compliance frameworks must the design address?"

## Examples

```bash
# Authentication-focused design against a high threat level, PCI-DSS scope
/gd-framework:security-architect security_focus=authentication compliance_framework=pci-dss threat_level=high

# Data-protection design under GDPR with enterprise-strict validation
/gd-framework:security-architect security_focus=data-protection compliance_framework=gdpr validation_level=enterprise
```

---

- Skill: `gd-framework:security-architect` (owns the methodologies, patterns, and
  security-architecture knowledge)
- Related agent: the proactive `gd-framework:security-architect` agent loads the same skill autonomously.
