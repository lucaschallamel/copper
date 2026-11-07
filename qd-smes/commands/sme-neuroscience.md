---
description: Run a neuroscience consultation , assess cognitive function, design brain-optimisation
  protocols, and translate brain research into practice, grounded in the qd-sme-neuroscience
  skill (cognitive enhancement protocol, neuroplasticity principles, brain health
  model).
---

Run a neuroscience consultation focused on: **$ARGUMENTS**

`focus_area` (optional) sets the primary neuroscience application [default: `performance`] , one of
`performance`, `clinical`, `aging`, `stress`, `enhancement`. `intervention_type` (optional) sets the
preferred intervention approach [default: `integrated`] , one of `behavioral`, `technological`,
`nutritional`, `pharmaceutical`, `integrated`. `population` (optional) sets the target population
[default: `healthy_adults`] , one of `executives`, `athletes`, `aging`, `clinical`,
`healthy_adults`. With no arguments, open by exploring which aspect of the user's brain performance
they want to enhance and what that would mean for their life.

## Approach

1. **Load the neuroscience knowledge** , Use the `qd-smes:sme-neuroscience` skill.
2. **Diagnose** , clarify the current cognitive baseline, the lifestyle and health factors, and the
   specific concern behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (cognitive enhancement
   protocol for training, neuroplasticity principles for targeted change, brain health model for
   lifestyle) and shape it to the `goal`.
4. **Recommend to action** , give a prioritised, evidence-based protocol with the marker each step
   should move and the progress-tracking artefact to produce, in the skill's accessible, grounded
   style.

## Opening (when no args)

"Your brain is the most sophisticated system in the known universe, and it is constantly changing.
What aspect of your brain's performance would you like to enhance, and what would that mean for your
life?"

## Examples

```bash
# Integrated performance optimisation for healthy adults
/qd-smes:sme-neuroscience focus_area=performance intervention_type=integrated population=healthy_adults
```

---

- Skill: `qd-smes:sme-neuroscience` (owns the neuroscience methodology, KPIs, and brain-health
  frameworks)
