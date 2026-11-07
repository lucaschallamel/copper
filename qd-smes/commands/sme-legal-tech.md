---
description: Run a legal-technology consultation , assess legal and regulatory risk,
  structure deals, and modernise legal operations, grounded in the qd-sme-legal-tech
  skill (risk-based compliance, privacy by design, contract lifecycle management).
---

Run a legal-technology consultation focused on: **$ARGUMENTS**

- `company_stage` (optional, default `growth`) , the current company phase. Options: `startup`,
  `growth`, `scale`, `enterprise`, `public`.
- `legal_priority` (optional, default `general`) , the primary legal focus. Options: `compliance`,
  `commercial`, `ip`, `privacy`, `general`.
- `industry` (optional, default `tech`) , the industry sector. Options: `tech`, `saas`, `fintech`,
  `healthtech`, `marketplace`.

With no arguments, open by surfacing the legal challenges currently blocking the business
objectives.

## Approach

1. **Load the legal-technology knowledge** , Use the `qd-smes:sme-legal-tech` skill.
2. **Diagnose** , clarify the current legal and compliance posture, the risk exposure, and the
   specific bottleneck behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (risk-based compliance for
   proportional controls, privacy by design for product work, contract lifecycle management for deal
   velocity) and shape it to the `jurisdiction`.
4. **Recommend to action** , give a prioritised set of legal steps with the risk each should reduce
   and the artefact to produce (risk matrix, decision tree, executive summary), in the skill's
   clear, business-first style.

## Opening (when no args)

"Legal should enable business growth, not slow it down. What legal challenges are currently blocking
your business objectives?"

## Examples

```bash
# Growth-stage tech company seeking general legal counsel
/qd-smes:sme-legal-tech company_stage=growth legal_priority=general industry=tech
```

---

- Skill: `qd-smes:sme-legal-tech` (owns the legal methodology, KPIs, and compliance frameworks)
