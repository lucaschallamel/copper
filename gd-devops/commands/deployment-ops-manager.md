---
description: Run a production-deployment and operations session , plan a zero-downtime
  rollout with monitoring, validation gates, and recovery, grounded in the gd-deployment-ops-manager
  skill (Kubernetes, SRE, observability, incident response).
---

Run a production-deployment and operations session for: **$ARGUMENTS**

All arguments are optional. `deployment_strategy` (default `blue-green`; options: `blue-green`,
`canary`, `rolling`, `recreate`, `shadow`); `environment_type` (default `production`; options:
`production`, `staging`, `dev`, `dr`, `ephemeral`); `monitoring_depth` (default `comprehensive`;
options: `basic`, `standard`, `comprehensive`, `enterprise`); `validation_level` (default
`standard`; options: `basic`, `standard`, `strict`, `enterprise`); `recovery_strategy` (default
`automatic`; options: `manual`, `automatic`, `progressive`, `immediate`). With no arguments, open by
drawing out the application, the target environment, and the reliability expectations.

## Approach

1. **Load the deployment knowledge** , Use the `gd-devops:deployment-ops-manager` skill.
2. **Frame the problem** , clarify the application behind `$ARGUMENTS`, the `environment_type`, the
   current infrastructure, and the SLOs and rollback expectations.
3. **Plan the rollout** , apply the fitting models from the skill (progressive delivery,
   health-check gates, golden-signals monitoring) to the chosen `deployment_strategy` and
   `monitoring_depth`, and define the validation pipeline.
4. **Wire recovery and observability** , at the requested `recovery_strategy`, define automatic
   rollback triggers and alert escalation, then deliver runbooks and a deployment plan. Require
   explicit confirmation before any production-bound or irreversible step.

## Examples

```bash
# Canary rollout to production with default validation and recovery
/gd-devops:deployment-ops-manager deployment_strategy=canary environment_type=production

# Enterprise observability with strict pre-deployment validation
/gd-devops:deployment-ops-manager monitoring_depth=enterprise validation_level=strict
```

## Opening (when no args)

"Let's get this to production without downtime. What are you deploying, into which environment, and
what reliability and rollback bars must the release respect?"

---

- Skill: `gd-devops:deployment-ops-manager` (owns the methodologies, patterns, and operations
  knowledge)
- Related agent: the proactive `gd-devops:deployment-ops-manager` agent loads the same skill autonomously.
