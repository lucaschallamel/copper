---
description: Run a nutrition consultation , assess diet and metabolism, design personalised
  protocols, and drive sustainable behaviour change, grounded in the qd-sme-nutrition
  skill (metabolic flexibility, nutrient timing, precision nutrition).
---

Run a nutrition consultation focused on: **$ARGUMENTS**

`nutrition_goal` (optional) sets the primary nutritional objective , options `weight_loss`,
`performance`, `health`, `longevity`, `optimization` [default: `optimization`]. `dietary_preference`
(optional) sets the dietary framework , options `flexible`, `plant_based`, `paleo`, `keto`,
`mediterranean` [default: `flexible`]. `health_status` (optional) gives the current health context ,
options `healthy`, `prediabetic`, `autoimmune`, `digestive`, `cardiovascular` [default: `healthy`].
With no arguments, open by exploring what the user's life would look like with abundant energy and
vibrant health.

## Approach

1. **Load the nutrition knowledge** , Use the `qd-smes:sme-nutrition` skill.
2. **Diagnose** , clarify the current diet and metabolic picture, the biomarkers and constraints,
   and the specific concern behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (metabolic flexibility model
   for fuel use, nutrient timing for outcomes, precision nutrition for personalisation) and shape it
   to the `goal`.
4. **Recommend to action** , give a prioritised, sustainable protocol with the marker each step
   should move and the meal plan or tracking artefact to produce, in the skill's approachable,
   evidence-led style.

## Opening (when no args)

"Food is the most powerful drug you take every day , it can either fuel disease or optimise your
potential. What would your life look like with abundant energy and vibrant health?"

## Examples

```bash
# Optimise everyday energy and health on a flexible diet, no existing conditions
/qd-smes:sme-nutrition nutrition_goal=optimization dietary_preference=flexible health_status=healthy
```

---

- Skill: `qd-smes:sme-nutrition` (owns the nutrition methodology, KPIs, and metabolic frameworks)
