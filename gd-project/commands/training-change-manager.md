---
description: Run a training and change-management session , design adult-learning
  programmes, change strategy, and user-adoption plans for a system rollout, grounded
  in the gd-training-change-manager skill.
---

Design training and change management for: **$ARGUMENTS**

All arguments are optional. `training_scope` (default `comprehensive`; extent of the training
programme needed, options: `quick-start`, `standard`, `comprehensive`, `certification`);
`change_complexity` (default `moderate`; level of organisational change, options: `minimal`,
`moderate`, `significant`, `transformational`); `delivery_mode` (default `blended`; primary training
delivery method, options: `self-paced`, `instructor-led`, `blended`, `microlearning`);
`validation_level` (default `standard`; validation strictness, options: `basic`, `standard`,
`strict`, `enterprise`). With no arguments, open by drawing out the system or change, the affected
users, and the sources of resistance.

## Approach

1. **Load the training knowledge** , Use the `gd-project:training-change-manager` skill.
2. **Frame the change** , clarify the system or change behind `$ARGUMENTS`, the affected users and
   their tech-comfort range, and the `change_complexity` to navigate.
3. **Design the programme** , apply the fitting frameworks from the skill (ADKAR, Kotter's 8-step,
   Bloom's taxonomy, 70-20-10) to build a learning architecture at the chosen `training_scope` and
   `delivery_mode`.
4. **Drive and measure** , at the requested `validation_level`, plan the rollout with a feedback
   channel, address resistance directly, verify training accuracy against the real system, and
   deliver adoption metrics.

## Opening (when no args)

"Let's turn this rollout into enthusiastic adoption. What system or change are we introducing, who
is affected, and where do you expect the resistance to come from?"

## Examples

```bash
# Comprehensive blended programme for significant change
/gd-project:training-change-manager training_scope=comprehensive change_complexity=significant delivery_mode=blended

# Certification programme with enterprise-grade validation
/gd-project:training-change-manager training_scope=certification validation_level=enterprise

# Transformational change delivered through microlearning
/gd-project:training-change-manager change_complexity=transformational delivery_mode=microlearning
```

---

- Skill: `gd-project:training-change-manager` (owns the methodologies, frameworks, and KPIs)
- Related agent: the proactive `gd-project:training-change-manager` agent loads the same skill autonomously.
