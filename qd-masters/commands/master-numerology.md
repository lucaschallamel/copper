---
description: Run a numerology reading , compute the core numbers, optimise a name,
  and map favourable cycles, grounded in the qd-master-numerology skill (Pythagorean,
  Chaldean, gematria, master numbers, personal cycles).
---

Run a numerology reading focused on: **$ARGUMENTS**

`reading_type` (optional) sets the type of numerological analysis [options: life_path,
personal_year, compatibility, business, comprehensive; default: comprehensive]; `system_preference`
(optional) sets the numerological system to use [options: pythagorean, chaldean, kabbalistic, vedic,
integrated; default: integrated]; `depth_level` (optional) sets the analysis depth [options: basic,
standard, detailed, master, esoteric; default: detailed]. With no arguments, open by asking which
patterns in the user's life are calling for deeper understanding, then gather the name and birth
date needed.

## Approach

1. **Load the numerology knowledge** , Use the `qd-masters:master-numerology` skill.
2. **Compute the numbers** , derive the Life Path, Expression, Soul Urge, and any master numbers
   relevant to `$ARGUMENTS`.
3. **Apply a system** , select the fitting method from the skill (Pythagorean, Chaldean, gematria,
   personal-cycle calculation) and read the vibrational signature.
4. **Deliver the reading** , give a chart-grounded interpretation with practical name or timing
   guidance, in the skill's reverent, accessible style.

## Opening (when no args)

"Numbers are the universal language written before time began. Every name, every date, every moment
carries a vibrational signature. What patterns in your life are calling for deeper understanding?"

## Examples

```bash
# Produce a comprehensive, detailed reading using all systems integrated
/qd-masters:master-numerology reading_type=comprehensive system_preference=integrated depth_level=detailed
```

---

- Skill: `qd-masters:master-numerology` (owns the systems, calculations, and numerological
  knowledge)
