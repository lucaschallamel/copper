---
description: Run an agent-design session , analyse the capability gap, specify a new
  agent with tools, boundaries, and behaviour, grounded in the gd-agent-creator skill
  (gap analysis, cognitive architecture, tool integration).
---

Design a new agent for: **$ARGUMENTS**

All arguments are optional. `complexity_level` (default `standard`; options: `simple`, `standard`,
`advanced`, `expert`) sets the sophistication of the agent's capabilities; `ecosystem_integration`
(default `collaborative`; options: `standalone`, `collaborative`, `orchestrating`, `meta-level`)
sets how the new agent integrates with existing agents; `validation_level` (default `standard`;
options: `basic`, `standard`, `strict`, `enterprise`) sets how strictly the specification is
checked; `template_version` (default `2.1`; options: `2.0`, `2.1`) selects the agent-specification
template version. With no arguments, open by drawing out the capability gap and the agent's intended
purpose.

## Approach

1. **Load the agent-design knowledge** , Use the `gd-framework:agent-creator` skill.
2. **Frame the gap** , clarify the missing capability behind `$ARGUMENTS`, the agent's purpose, and
   how it should complement what already exists without overlap.
3. **Specify the agent** , at the chosen `complexity_level`, define the role, responsibilities,
   trigger conditions, required tools, and permission levels, with explicit boundaries.
4. **Validate** , at the requested `validation_level`, check scope isolation, tool-grant fit, and
   specification completeness, then deliver the agent definition with usage examples.

## Opening (when no args)

"Let's design the agent you need. What capability is missing today, what should the agent do, and
how should it sit alongside your existing agents so it complements rather than overlaps them?"

## Examples

```bash
# Expert-level architecture agent that collaborates with existing agents
/gd-framework:agent-creator complexity_level=expert ecosystem_integration=collaborative

# Quality-focused agent validated to enterprise strictness
/gd-framework:agent-creator validation_level=enterprise

# Advanced analysis agent
/gd-framework:agent-creator complexity_level=advanced
```

---

- Skill: `gd-framework:agent-creator` (owns the methodologies, patterns, and agent-design knowledge)
- Related agent: the proactive `gd-framework:agent-creator` agent loads the same skill autonomously.
