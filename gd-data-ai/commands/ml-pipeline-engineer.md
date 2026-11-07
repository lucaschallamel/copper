---
description: Run an ML-pipeline design session , architect training, inference, feature,
  or end-to-end ML pipelines with MLOps, monitoring, and drift detection, grounded
  in the gd-ml-pipeline-engineer skill.
---

Run an ML-pipeline design session for: **$ARGUMENTS**

All arguments are optional. `pipeline_type` (default `end-to-end`; options: `training`, `inference`,
`feature`, `end-to-end`, `monitoring`); `framework` (default `auto-select`; options: `pytorch`,
`tensorflow`, `sklearn`, `xgboost`, `custom`); `scale` (default `medium`; options: `prototype`,
`small`, `medium`, `large`, `enterprise`); `deployment_target` (default `cloud`; options: `cloud`,
`edge`, `mobile`, `embedded`, `hybrid`). With no arguments, open by drawing out the model type, the
data sources, and the training and serving requirements.

## Approach

1. **Load the ML-pipeline knowledge** , Use the `gd-data-ai:ml-pipeline-engineer` skill.
2. **Frame the problem** , clarify the model type and objective behind `$ARGUMENTS`, the data sources,
   the expected scale, and the non-functional requirements (latency, throughput, cost, governance).
3. **Design the pipeline** , apply the fitting patterns from the skill (orchestration, training and
   feature stores, model serving, and an experiment-tracking setup) to the chosen `pipeline_type`,
   `framework`, `scale`, and `deployment_target`.
4. **Validate and monitor** , add automated validation against a benchmark, drift detection, and a
   rollback to the prior version; version data, code, and artefacts; and track experiments and
   lineage.

## Opening (when no args)

"Let's design an ML pipeline that is reproducible and production-ready. What are you modelling,
where does the data come from, and what training, serving, and governance requirements must it
meet?"

## Examples

```bash
# Large-scale PyTorch training pipeline
/gd-data-ai:ml-pipeline-engineer pipeline_type=training framework=pytorch scale=large

# End-to-end pipeline targeting edge deployment
/gd-data-ai:ml-pipeline-engineer pipeline_type=end-to-end deployment_target=edge

# Enterprise-scale model monitoring pipeline
/gd-data-ai:ml-pipeline-engineer pipeline_type=monitoring scale=enterprise
```

---

- Skill: `gd-data-ai:ml-pipeline-engineer` (owns the methodologies, patterns, and ML-pipeline
  knowledge)
- Related agent: the proactive `gd-data-ai:ml-pipeline-engineer` agent loads the same skill autonomously.
