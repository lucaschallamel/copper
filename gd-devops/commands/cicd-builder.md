---
description: Run a CI/CD pipeline-design session , produce a multi-stage build, test,
  and deploy pipeline with security gates and automated rollback, grounded in the
  gd-cicd-builder skill (GitOps, DevSecOps, container orchestration).
---

Run a CI/CD pipeline-design session for: **$ARGUMENTS**

All arguments are optional. `pipeline_type` (default `build-test-deploy`; options: `build-only`,
`build-test`, `build-test-deploy`, `full-devops`, `compliance-focused`); `platform` (default
`github-actions`; options: `github-actions`, `gitlab-ci`, `jenkins`, `azure-devops`, `circleci`);
`deployment_target` (default `kubernetes`; options: `kubernetes`, `serverless`, `vm`, `containers`,
`hybrid`); `compliance_framework` (default `none`; options: `none`, `soc2`, `pci-dss`, `hipaa`,
`fedramp`); `deployment_strategy` (default `rolling`; options: `blue-green`, `canary`, `rolling`,
`immutable`, `feature-flags`); `security_level` (default `standard`; options: `basic`, `standard`,
`enterprise`, `government`, `financial-services`). With no arguments, open by drawing out the
application, the target environment, and the release expectations.

## Approach

1. **Load the CI/CD knowledge** , Use the `gd-devops:cicd-builder` skill.
2. **Frame the problem** , clarify the application behind `$ARGUMENTS`, the target `platform`, the
   build and test needs, and the security and compliance requirements.
3. **Design the pipeline** , apply the fitting models from the skill (multi-stage stages, parallel
   execution, shift-left security gates, GitOps reconciliation) to the chosen `pipeline_type` and
   `deployment_strategy`.
4. **Harden and validate** , at the requested `security_level`, add SAST/DAST and dependency
   scanning, define quality gates, and wire automated rollback, then deliver the pipeline definition
   with a self-service developer experience.

## Examples

```bash
# Full DevOps pipeline with canary delivery at enterprise security
/gd-devops:cicd-builder pipeline_type=full-devops deployment_strategy=canary security_level=enterprise

# Compliance-focused pipeline with blue-green delivery under SOC2
/gd-devops:cicd-builder pipeline_type=compliance-focused deployment_strategy=blue-green compliance_framework=soc2

# Build-test-deploy pipeline with rolling delivery at standard security
/gd-devops:cicd-builder pipeline_type=build-test-deploy deployment_strategy=rolling security_level=standard
```

## Opening (when no args)

"Let's build a pipeline that ships safely and fast. What are you deploying, where does it run, and
what security and compliance bars must each release clear?"

---

- Skill: `gd-devops:cicd-builder` (owns the methodologies, patterns, and CI/CD knowledge)
- Related agent: the proactive `gd-devops:cicd-builder` agent loads the same skill autonomously.
