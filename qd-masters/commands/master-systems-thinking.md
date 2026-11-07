---
description: Run a systems-analysis session , map the system, reframe symptoms to
  root causes, and find high-leverage interventions, grounded in the qd-master-systems-thinking
  skill (causal loops, archetypes, Cynefin, Meadows' leverage points).
---

Run a systems-analysis session focused on: **$ARGUMENTS**

- **`system_type`** (optional): type of system being analysed , options: `organizational`, `social`,
  `environmental`, `economic`, `technical` [default: organizational]
- **`complexity_level`** (optional): system complexity , options: `complicated`, `complex`,
  `chaotic`, `emergent` [default: complex]
- **`intervention_scope`** (optional): scale of desired change , options: `incremental`,
  `substantial`, `transformational`, `paradigm` [default: transformational]

With no arguments, open by asking which patterns keep repeating despite the user's efforts.

## Approach

1. **Load the systems knowledge** , Use the `qd-masters:master-systems-thinking` skill.
2. **Map the system** , define boundaries, stakeholders, feedback loops, and the archetype at work
   in `$ARGUMENTS`.
3. **Apply a framework** , select the fitting tool from the skill (causal-loop diagrams, system
   archetypes, Cynefin, Meadows' leverage points) and reframe from symptoms to root causes.
4. **Design the intervention** , identify the high-leverage change points, anticipate unintended
   consequences, and propose an adaptive approach, in the skill's accessible, questioning style.

## Opening (when no args)

"Every problem exists within a system of interconnected elements. Let's explore the system you're
trying to understand or change. What patterns keep repeating despite your efforts?"

## Examples

```bash
# Map an organisational system and design a transformational intervention
/qd-masters:master-systems-thinking system_type=organizational complexity_level=complex intervention_scope=transformational
```

---

- Skill: `qd-masters:master-systems-thinking` (owns the frameworks, archetypes, and systems
  knowledge)
