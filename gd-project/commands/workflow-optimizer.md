---
description: Run a workflow-optimisation session , mine processes, find bottlenecks,
  and design lean, automated workflows that cut cycle time and cognitive load without
  eroding quality, grounded in the gd-workflow-optimizer skill.
---

Analyse and optimise the workflow for: **$ARGUMENTS**

All arguments are optional. `scope` (default `full`; optimisation scope, options: `task`, `process`,
`team`, `organization`); `priority` (default `efficiency`; optimisation priority, options: `speed`,
`quality`, `efficiency`, `cost`); `methodology` (default `lean`; analysis methodology, options:
`lean`, `agile`, `kanban`, `value-stream`); `automation_level` (default `moderate`; automation
preference, options: `minimal`, `moderate`, `aggressive`, `full`); `validation_level` (default
`standard`; validation strictness, options: `basic`, `standard`, `strict`, `enterprise`). With no
arguments, open by drawing out the workflow under review, where it feels slow, and what "better"
means for this team.

## Approach

1. **Load the optimisation knowledge** , Use the `gd-project:workflow-optimizer` skill.
2. **Frame and baseline** , clarify the workflow behind `$ARGUMENTS` at the chosen `scope`, measure
   the current cycle time and pain points, and agree what to optimise for via `priority`.
3. **Mine and diagnose** , apply the fitting models from the skill (value-stream mapping, theory of
   constraints, the chosen `methodology`) to surface actual-versus-documented flow, bottlenecks, and
   cognitive-load hotspots.
4. **Redesign and validate** , at the requested `validation_level`, propose a leaner workflow with
   automation at the chosen `automation_level`, preserve the quality gates that matter, and deliver
   before/after metrics with a monitoring plan.

This is an analysis-and-recommendation capability: it observes, diagnoses, and proposes without
editing the workflows or code under review.

## Opening (when no args)

"Let's find where this workflow leaks time and energy. Which process are we looking at, where does
it feel slow or heavy, and are we optimising for speed, quality, efficiency, or cost?"

## Examples

```bash
# Team-level optimisation prioritising speed
/gd-project:workflow-optimizer scope=team priority=speed

# Aggressive automation of an existing process
/gd-project:workflow-optimizer automation_level=aggressive

# Enterprise-grade validation of the analysis
/gd-project:workflow-optimizer validation_level=enterprise
```

---

- Skill: `gd-project:workflow-optimizer` (owns the methodologies, frameworks, and KPIs)
- Related agent: the proactive `gd-project:workflow-optimizer` agent loads the same skill autonomously.
