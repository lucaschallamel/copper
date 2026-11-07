---
description: Run an ML engineering consultation , design production ML pipelines,
  optimise serving, and harden reliability, grounded in the qd-sme-ml-engineer skill
  (MLOps maturity model, feature stores, model registry).
---

Run an ML engineering consultation focused on: **$ARGUMENTS**

`deployment_type` (optional) sets the primary deployment environment [default: `cloud`] , one of
`cloud`, `edge`, `on_premise`, `hybrid`, `mobile`. `scale` (optional) sets the system scale
requirements [default: `large`] , one of `prototype`, `medium`, `large`, `massive`. `ml_type`
(optional) sets the primary ML workload [default: `general`] , one of `nlp`, `computer_vision`,
`recommendation`, `tabular`, `general`. With no arguments, open by establishing which models are
being deployed, the scale they must handle, and the latency requirements.

## Approach

1. **Load the ML engineering knowledge** , Use the `qd-smes:sme-ml-engineer` skill.
2. **Diagnose** , clarify the current ML lifecycle, the serving metrics (latency, uptime, cost), and
   the specific bottleneck behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (MLOps maturity model for
   automation gaps, feature store for reuse, model registry for governance) and design the concrete
   change for the user's `stack`.
4. **Recommend to action** , give a prioritised set of platform steps with the metric each should
   move and the architecture or runbook artefact to produce, in the skill's rigorous, pragmatic
   style.

## Opening (when no args)

"Let us make your ML models production-ready. What models are you trying to deploy, what scale do
they need to handle, and what are your latency requirements?"

## Examples

```bash
# Large-scale cloud deployment of a general ML workload
/qd-smes:sme-ml-engineer deployment_type=cloud scale=large ml_type=general
```

---

- Skill: `qd-smes:sme-ml-engineer` (owns the MLOps methodology, KPIs, and serving frameworks)
