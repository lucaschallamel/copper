---
description: Run a project-planning session , decompose requirements into a WBS, architect
  a realistic timeline, allocate resources, and produce an executable roadmap, grounded
  in the gd-project-planner skill.
---

Create a project plan and roadmap for: **$ARGUMENTS**

All arguments are optional. `methodology` (default `agile`; the project-management approach;
options: `agile`, `waterfall`, `hybrid`, `lean`, `safe`); `project_size` (default `medium`; the
scale of the project; options: `small`, `medium`, `large`, `enterprise`); `timeline_constraint`
(default `balanced`; the primary time consideration; options: `fixed-deadline`, `flexible`,
`time-boxed`, `continuous`); `validation_level` (default `standard`; the validation strictness;
options: `basic`, `standard`, `strict`, `enterprise`). With no arguments, open by drawing out the
vision, the constraints, and the deliverables the plan must produce.

## Approach

1. **Load the project-planning knowledge** , Use the `gd-project:project-planner` skill.
2. **Decompose the work** , transform `$ARGUMENTS` into a structured WBS with clear deliverables,
   dependencies, and acceptance criteria.
3. **Architect the schedule** , apply the fitting models from the skill (SAFe, Scrum/Kanban hybrid,
   critical-path analysis, Monte Carlo estimation) to the chosen `methodology` and `project_size`,
   building a realistic timeline and resource plan.
4. **Baseline with risk** , at the requested `timeline_constraint` and `validation_level`, surface
   critical-path and resource risks with mitigation options, keep estimates evidence-based, and
   deliver an executable roadmap with success metrics.

## Opening (when no args)

"Let's build a plan you can actually deliver. What's the goal, what constraints , deadline, budget,
team , are fixed, and what deliverables does the roadmap need to produce?"

## Examples

```bash
# Large agile project with a fixed deadline
/gd-project:project-planner methodology=agile project_size=large timeline_constraint=fixed-deadline

# Enterprise hybrid plan with strict validation
/gd-project:project-planner methodology=hybrid project_size=enterprise validation_level=strict

# Medium SAFe project
/gd-project:project-planner methodology=safe project_size=medium
```

---

- Skill: `gd-project:project-planner` (owns the methodologies, estimation models, and KPIs)
- Related agent: the proactive `gd-project:project-planner` agent loads the same skill autonomously.
