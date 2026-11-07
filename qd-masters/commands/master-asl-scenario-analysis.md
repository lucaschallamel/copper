---
description: Analyse an ASL scenario before play , victory conditions, the ground-to-turns
  budget, order of battle, terrain channels and SSR, grounded in the qd-master-asl-scenario-analysis
  skill.
---

# /qd-masters:master-asl-scenario-analysis

Prepare for a scenario, or diagnose why a plan failed.

## Arguments

- `scenario` , the scenario to analyse (required)
- `side` , optional: which side, or ask which to take
- `mode` , optional: `prepare` or `post-mortem`. Defaults to prepare

## Output

For prepare: victory conditions quoted, the ground-to-turns ratio computed, order-of-battle quality
comparison, terrain channels, and a plan with its stated failure condition. For post-mortem: the
analysis step that actually failed, checked in order before execution is blamed.
