---
description: Run a risk-management session , identify, quantify, model, and mitigate
  project and security risks with contingency planning and continuous monitoring,
  grounded in the gd-risk-manager skill.
---

Assess and manage risk for: **$ARGUMENTS**

All arguments are optional. `risk_focus` (default `comprehensive`; primary risk domain emphasis,
options: `technical`, `security`, `financial`, `regulatory`, `operational`, `comprehensive`);
`assessment_depth` (default `standard`; level of risk-analysis detail, options: `quick`, `standard`,
`detailed`, `forensic`, `threat_modeling`); `risk_appetite` (default `moderate`; the organisation's
risk-tolerance level, options: `conservative`, `moderate`, `aggressive`, `adaptive`,
`quantitative`); `validation_level` (default `standard`; validation strictness, options: `basic`,
`standard`, `strict`, `enterprise`, `owasp_compliant`); `triage` (default `manual`; bug-triage
automation level, options: `manual`, `assisted`, `automated`, `ai_powered`); `severity_assessment`
(default `standard`; severity assessment methodology, options: `standard`, `impact_based`,
`risk_matrix`, `quantitative`); `root_cause` (default `standard`; root-cause-analysis depth,
options: `basic`, `standard`, `comprehensive`, `forensic`). With no arguments, open by drawing out
the scope, the assets at stake, and the constraints the assessment must respect.

## Approach

1. **Load the risk knowledge** , Use the `gd-project:risk-manager` skill.
2. **Frame the problem** , clarify the scope behind `$ARGUMENTS`, the assets and stakeholders at
   stake, the `risk_focus`, and the organisation's `risk_appetite`.
3. **Identify and quantify** , apply the fitting models from the skill (threat modelling at
   `assessment_depth`, Monte Carlo and probabilistic quantification, OWASP-compliant security
   audits) and capture likelihood, impact, and confidence per risk.
4. **Mitigate and monitor** , at the requested `validation_level`, design defence-in-depth
   mitigation and contingency with owners and triggers, set the `severity_assessment` and
   `root_cause` approach, and deliver a risk register with key risk indicators and a monitoring
   plan.

## Opening (when no args)

"Let's turn this uncertainty into a manageable plan. What is the scope, which assets and
stakeholders are at stake, and how much risk is the organisation prepared to carry?"

## Examples

```bash
# Security-focused threat-modelling assessment under OWASP compliance
/gd-project:risk-manager risk_focus=security assessment_depth=threat_modeling validation_level=owasp_compliant

# Forensic technical assessment with quantitative risk appetite
/gd-project:risk-manager risk_focus=technical assessment_depth=forensic risk_appetite=quantitative validation_level=enterprise
```

---

- Skill: `gd-project:risk-manager` (owns the methodologies, frameworks, and KPIs)
- Related agent: the proactive `gd-project:risk-manager` agent loads the same skill autonomously.
