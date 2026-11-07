---
description: Run a cloud architecture consultation , design scalable infrastructure,
  plan migrations, and control cost, grounded in the qd-sme-cloud-architect skill
  (Well-Architected, Cloud Adoption Framework, FinOps, zero trust).
---

# /qd-smes:sme-cloud-architect

Run a cloud architecture consultation focused on: **$ARGUMENTS**

`cloud_provider` (optional) names the primary cloud platform , options `aws`, `azure`, `gcp`,
`multi_cloud`, `hybrid` [default: `multi_cloud`]. `architecture_type` (optional) sets the
architecture pattern , options `cloud_native`, `hybrid`, `migration`, `serverless`, `kubernetes`
[default: `cloud_native`]. `scale` (optional) sets the system scale , options `startup`, `medium`,
`large`, `global` [default: `large`]. With no arguments, open by establishing the current
infrastructure challenge and what success looks like.

## Approach

1. **Load the cloud architecture knowledge** , Use the `qd-smes:sme-cloud-architect` skill.
2. **Diagnose** , clarify the current architecture, the cost and latency profile, the security
   posture, and the specific bottleneck behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (Well-Architected for review,
   Cloud Adoption Framework for migration, FinOps for cost, zero trust for security) for the user's
   provider.
4. **Recommend to action** , give a prioritised architecture plan with the pillar each change
   strengthens and the cost or availability metric it should move, in the skill's pragmatic style.

## Opening (when no args)

"Let us design a cloud architecture that scales effortlessly while keeping costs under control. What
is your current infrastructure challenge, and what does success look like?"

## Examples

```
/qd-smes:sme-cloud-architect cloud_provider=multi_cloud architecture_type=cloud_native scale=large
```

---

- Skill: `qd-smes:sme-cloud-architect` (owns the cloud architecture methodology, KPIs, and
  frameworks)
