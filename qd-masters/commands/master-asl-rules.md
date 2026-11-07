---
description: Resolve an ASL rules question , locate the chapter, check SSR and errata
  first, quote the rule and explain the mechanism, grounded in the qd-master-asl-rules
  skill.
---

# /qd-masters:master-asl-rules

Answer a rules question with its citation and mechanism.

## Arguments

- `question` , the rules question (required)
- `scenario_ssr` , optional: the scenario's special rules, which override the base rulebook
- `module` , optional: which module is in play

## Output

The rule number and quoted text, SSR and errata checked first, the mechanism explained, and any DRM
stack enumerated item by item. Genuine ambiguity is reported as ambiguity.
