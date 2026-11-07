---
description: Run a project-orchestration session , decompose an ambiguous vision into
  coordinated tasks, sequence and coordinate specialised agents, and drive adaptive,
  quality-gated delivery, grounded in the gd-project-orchestrator skill.
---

Orchestrate the project delivery for: **$ARGUMENTS**

All arguments are optional. `delivery_timeline` (default `standard`; the timeline constraint;
options: `urgent`, `standard`, `extended`, `flexible`); `quality_gates` (default `standard`; the
quality assurance level; options: `basic`, `standard`, `strict`, `enterprise`); `automation_level`
(default `standard`; the workflow-automation depth; options: `manual`, `semi-automated`,
`automated`, `fully-autonomous`); `validation_level` (default `standard`; the validation strictness;
options: `basic`, `standard`, `strict`, `enterprise`). With no arguments, open by drawing out the
vision, the streams of work, and the dependencies that must be coordinated.

## Approach

1. **Load the orchestration knowledge** , Use the `gd-project:project-orchestrator` skill.
2. **Decompose the vision** , break `$ARGUMENTS` into coordinated tasks with an explicit dependency
   map, and identify the specialised capabilities each task needs.
3. **Sequence and coordinate** , apply the fitting models from the skill (event-driven,
   choreography, and saga patterns; adaptive project management) at the chosen `automation_level`,
   selecting and ordering the agents, and adapting as intermediate results arrive.
4. **Synthesise and gate** , at the requested `delivery_timeline`, `quality_gates`, and
   `validation_level`, integrate outputs into a coherent deliverable with verified hand-offs,
   escalating only critical or low-confidence decisions.

## Opening (when no args)

"Let's turn the vision into coordinated delivery. What's the outcome, what streams of work does it
break into, and which dependencies and quality gates must the orchestration respect?"

## Examples

```bash
# Enterprise project with strict quality gates
/gd-project:project-orchestrator quality_gates=strict validation_level=enterprise

# Complex project under an urgent timeline
/gd-project:project-orchestrator delivery_timeline=urgent quality_gates=strict

# Standard project with automated workflows
/gd-project:project-orchestrator automation_level=automated quality_gates=standard
```

---

- Skill: `gd-project:project-orchestrator` (owns the orchestration patterns, methodologies, and
  KPIs)
- Related agent: the proactive `gd-project:project-orchestrator` agent loads the same skill autonomously.
