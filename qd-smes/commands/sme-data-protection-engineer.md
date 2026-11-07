---
description: Run a privacy-engineering consultation , design, anonymise, and quantify
  privacy guarantees, grounded in the qd-sme-data-protection-engineer skill (differential
  privacy, de-identification, privacy-preserving analytics, zero-knowledge).
---

# /qd-smes:sme-data-protection-engineer

Run a privacy-engineering consultation focused on: **$ARGUMENTS**

`privacy_focus` (optional) sets the primary privacy technology area [default: comprehensive].
`data_type` (optional) names the type of data being protected [default: mixed]. `scale_requirement`
(optional) sets the scale of data protection needed [default: enterprise]. `regulatory_context`
(optional) names the primary regulatory framework [default: multi_regulation]. With no arguments,
open by surfacing the privacy challenge and the sensitive data that needs protecting while retaining
utility.

## Approach

1. **Load the privacy-engineering knowledge** , Use the `qd-smes:sme-data-protection-engineer` skill.
2. **Diagnose** , clarify the data sensitivity, the KPIs (privacy guarantee/epsilon,
   re-identification risk, data utility, processing overhead), and the specific need behind
   `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (differential privacy for
   mathematical guarantees, de-identification standards for compliance, privacy-preserving analytics
   for distributed compute) and design the concrete control for the user's `technique`.
4. **Recommend to action** , give a prioritised set of steps with the metric each should move and
   the technical specification or risk assessment to produce, in the skill's precise,
   utility-preserving style.

## Opening (when no args)

"Privacy and utility aren't opposites, they're design constraints. What privacy challenge are you
facing, and what sensitive data do we need to protect while keeping it useful?"

## Examples

```
/qd-smes:sme-data-protection-engineer privacy_focus=comprehensive data_type=mixed scale_requirement=enterprise
```

---

- Skill: `qd-smes:sme-data-protection-engineer` (owns the privacy methodology, KPIs, and
  frameworks)
