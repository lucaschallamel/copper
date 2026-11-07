---
description: Run an Infrastructure-as-Code automation session , produce modular, tested,
  policy-compliant IaC with GitOps workflows, grounded in the gd-iac-automation-engineer
  skill (Terraform, Ansible, Pulumi, policy as code, drift detection).
---

Run an Infrastructure-as-Code automation session for: **$ARGUMENTS**

All arguments are optional. `iac_framework` (default `terraform`; options: `terraform`,
`cloudformation`, `ansible`, `pulumi`, `cdk`); `cloud_provider` (default `multi-cloud`; options:
`aws`, `azure`, `gcp`, `multi-cloud`, `hybrid`); `complexity` (default `standard`; options:
`simple`, `standard`, `complex`, `enterprise`); `gitops_enabled` (boolean, default `true`) enables
GitOps workflows; `testing_strategy` (default `comprehensive`; options: `basic`, `comprehensive`,
`enterprise`); `compliance_level` (default `standard`; options: `basic`, `standard`, `strict`,
`regulatory`). With no arguments, open by drawing out the infrastructure, the target cloud, and the
automation goals.

## Approach

1. **Load the IaC knowledge** , Use the `gd-devops:iac-automation-engineer` skill.
2. **Frame the problem** , clarify the infrastructure behind `$ARGUMENTS`, the `cloud_provider`, the
   state and environment strategy, and the compliance requirements.
3. **Design the automation** , apply the fitting models from the skill (layered modules, remote
   state, GitOps workflows, policy as code) to the chosen `iac_framework` and `complexity`, and
   define the testing pyramid.
4. **Validate and govern** , at the requested `compliance_level`, add policy checks, drift
   detection, and cost governance, then deliver the IaC modules and a plan-then-apply pipeline.
   Require explicit confirmation before any destructive or production-bound apply.

## Examples

```bash
# Enterprise Terraform on AWS
/gd-devops:iac-automation-engineer iac_framework=terraform cloud_provider=aws complexity=enterprise

# Ansible automation with GitOps workflows enabled
/gd-devops:iac-automation-engineer iac_framework=ansible gitops_enabled=true

# Multi-cloud Pulumi provisioning
/gd-devops:iac-automation-engineer iac_framework=pulumi cloud_provider=multi-cloud
```

## Opening (when no args)

"Let's automate this infrastructure so it stays reproducible and compliant. What are you
provisioning, on which cloud, and what compliance and cost guardrails must it honour?"

---

- Skill: `gd-devops:iac-automation-engineer` (owns the methodologies, patterns, and IaC knowledge)
- Related agent: the proactive `gd-devops:iac-automation-engineer` agent loads the same skill autonomously.
