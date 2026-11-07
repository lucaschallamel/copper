---
description: Run a system-architecture design session , produce a scalable, fault-tolerant
  architecture with trade-offs and a roadmap, grounded in the gd-system-architect
  skill (DDD, C4, cloud-native, microservices patterns).
---

Run a system-architecture design session for: **$ARGUMENTS**

All arguments are optional. `architecture_type` (default `microservices`; options: `monolithic`,
`microservices`, `serverless`, `event-driven`, `hybrid`); `scale` (default `medium`; options:
`small`, `medium`, `large`, `enterprise`, `hyperscale`); `complexity` (default `moderate`; options:
`simple`, `moderate`, `complex`, `highly-complex`); `validation_level` (default `standard`; options:
`basic`, `standard`, `strict`, `enterprise`). With no arguments, open by drawing out the business
requirements, the expected load, and the constraints.

## Approach

1. **Load the architecture knowledge** , Use the `gd-architecture:system-architect` skill.
2. **Frame the problem** , clarify the business requirements behind `$ARGUMENTS`, the expected scale,
   the non-functional requirements (availability, latency, compliance), and what already exists.
3. **Design the architecture** , apply the fitting models from the skill (DDD bounded contexts, C4
   levels, the relevant microservices patterns, the Well-Architected pillars) to the chosen
   `architecture_type` and `scale`, and capture the key decisions as ADRs.
4. **Validate and roadmap** , at the requested `validation_level`, check the scalability path, the
   rollback strategy, and the single-points-of-failure, then deliver a phased implementation roadmap
   with explicit consistency / availability / partition-tolerance trade-offs.

## Opening (when no args)

"Let's design an architecture that fits your business requirements today and scales with them. What
are you building, what load do you expect, and what constraints (compliance, latency, budget, team)
must it respect?"

## Examples

```bash
# Enterprise-scale microservices architecture
/gd-architecture:system-architect architecture_type=microservices scale=enterprise

# Complex system with enterprise validation strictness
/gd-architecture:system-architect complexity=complex validation_level=enterprise
```

---

- Skill: `gd-architecture:system-architect` (owns the methodologies, patterns, and architecture
  knowledge)
- Related agent: the proactive `gd-architecture:system-architect` agent loads the same skill autonomously.
