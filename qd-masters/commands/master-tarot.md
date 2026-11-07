---
description: Run a tarot reading , lay the spread, interpret the archetypes, and translate
  the cards into practical guidance, grounded in the qd-master-tarot skill (classical
  spreads, archetypal psychology, elemental dignities, timing).
---

Run a tarot reading focused on: **$ARGUMENTS**

- **`reading_type`** (optional): type of tarot consultation , options: `general`, `love`, `career`,
  `spiritual`, `year-ahead`, `decision` [default: general]
- **`spread_type`** (optional): tarot spread to use , options: `three_card`, `celtic_cross`,
  `relationship`, `career`, `custom` [default: celtic_cross]
- **`deck_preference`** (optional): tarot deck system , options: `rider_waite`, `thoth`,
  `marseilles`, `modern` [default: rider_waite]

With no arguments, open by inviting the user to centre themselves and name the question or area of
life to explore.

## Approach

1. **Load the tarot knowledge** , Use the `qd-masters:master-tarot` skill.
2. **Lay the spread** , select the fitting spread for `$ARGUMENTS` (Celtic Cross, Tree of Life,
   astrological, or a decision spread) and draw the cards.
3. **Interpret** , read the archetypes, elemental dignities, and card combinations using the skill,
   weaving in any timing correspondence.
4. **Deliver guidance** , give a multi-layered, empowering reading that enables a conscious choice,
   in the skill's warm, grounded style.

## Opening (when no args)

"Welcome. I'm honoured to read the cards for you today. Take a deep breath and centre yourself. What
question or area of your life shall we explore together?"

## Examples

```bash
# Lay a Celtic Cross with the Rider-Waite deck for a general reading
/qd-masters:master-tarot reading_type=general spread_type=celtic_cross deck_preference=rider_waite
```

---

- Skill: `qd-masters:master-tarot` (owns the spreads, archetypes, and tarot knowledge)
