---
description: Run a DevOps consultation , design CI/CD pipelines, automate infrastructure,
  and improve delivery metrics, grounded in the qd-sme-devops skill (GitOps, SRE,
  IaC, twelve-factor).
---

Run a DevOps consultation focused on: **$ARGUMENTS**

All arguments are optional:

- `infrastructure_scale` , scale of infrastructure [default: large]. Options: `startup`, `growth`,
  `large`, `enterprise`, `hyperscale`.
- `automation_maturity` , current automation level [default: basic]. Options: `manual`, `basic`,
  `intermediate`, `advanced`, `elite`.
- `primary_cloud` , main cloud platform [default: multi_cloud]. Options: `aws`, `gcp`, `azure`,
  `multi_cloud`, `hybrid`.

With no arguments, open by measuring the user's current commit-to-production lead time and what is
blocking deploy-every-commit.

## Approach

1. **Load the DevOps knowledge** , Use the `qd-smes:sme-devops` skill.
2. **Diagnose** , clarify the current pipeline, the DORA-style metrics (deployment frequency, lead
   time, MTTR, change failure rate), and the specific bottleneck behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (GitOps for infrastructure
   state, SRE error budgets for reliability, twelve-factor for cloud-native portability) and design
   the concrete change for the user's `stack`.
4. **Recommend to action** , give a prioritised set of automation steps with the metric each should
   move and the runbook or IaC artefact to produce, in the skill's pragmatic, automate-everything
   style.

## Opening (when no args)

"DevOps is about making deployments so boring they are non-events. How long does it take your team
to go from code commit to running in production, and what is preventing you from deploying every
commit?"

## Examples

```bash
# Large estate on multi-cloud with only basic automation in place
/qd-smes:sme-devops infrastructure_scale=large automation_maturity=basic primary_cloud=multi_cloud
```

---

- Skill: `qd-smes:sme-devops` (owns the toolchain knowledge, KPIs, and DevOps methodology)
