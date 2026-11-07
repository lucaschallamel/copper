---
description: Run a cybersecurity consultation , assess risk, design controls, and
  plan incident response, grounded in the qd-sme-security skill (NIST CSF, MITRE ATT&CK,
  Zero Trust, DevSecOps).
---

Run a cybersecurity consultation focused on: **$ARGUMENTS**

`organization_type` (optional) sets the organisational context [default: `enterprise`]; options are
`startup`, `smb`, `enterprise`, `government`, `critical_infrastructure`. `security_focus` (optional)
names the primary security concern [default: `comprehensive`]; options are `cloud`, `application`,
`infrastructure`, `compliance`, `comprehensive`. `maturity_level` (optional) records the current
security maturity [default: `developing`]; options are `initial`, `developing`, `defined`,
`managed`, `optimized`. With no arguments, open by mapping the user's critical assets and the
threats that most concern them.

## Approach

1. **Load the security knowledge** , Use the `qd-smes:sme-security` skill.
2. **Diagnose** , clarify the current posture, the critical assets, and the specific risk or
   exposure behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (NIST CSF for programme
   structure, MITRE ATT&CK for threat coverage, Zero Trust for access, DevSecOps for the pipeline)
   and design controls for the user's `scope`.
4. **Recommend to action** , give a prioritised, risk-based set of mitigations with the metric each
   should move and the artefact to produce, in the skill's pragmatic, business-aligned style.

## Opening (when no args)

"Security is about enabling business while managing risk. What are your critical assets, and what
keeps you worried about their protection?"

## Examples

```bash
# Build a comprehensive security programme for an enterprise still developing its maturity
/qd-smes:sme-security organization_type=enterprise security_focus=comprehensive maturity_level=developing
```

---

- Skill: `qd-smes:sme-security` (owns the security methodology, KPIs, and frameworks)
