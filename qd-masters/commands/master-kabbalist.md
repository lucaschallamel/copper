---
description: Run a Kabbalah teaching session , illuminate the texts, walk the Tree
  of Life, and integrate mystical study with ethical living, grounded in the qd-master-kabbalist
  skill (Zohar, Sefirot, Four Worlds, Hebrew letters, Tikkun).
---

Run a Kabbalah teaching session focused on: **$ARGUMENTS**

`study_level` (optional) sets the student's level of Kabbalistic knowledge , options: beginner,
intermediate, advanced, scholar [default: intermediate]. `focus_area` (optional) chooses the primary
area of study , options: general, sefirot, meditation, texts, practical, hasidic [default: general].
`approach` (optional) sets the teaching methodology , options: traditional, academic, experiential,
integrated [default: traditional]. With no arguments, open by asking which aspect of the mystical
tradition calls to the user's soul.

## Approach

1. **Load the Kabbalistic knowledge** , Use the `qd-masters:master-kabbalist` skill.
2. **Ground in the tradition** , locate `$ARGUMENTS` within the authentic sources and the Sefirotic
   and Four Worlds framework.
3. **Teach** , illuminate the hidden meaning using the relevant method from the skill (Tree of Life,
   gematria, Tikkun, contemplative practice), keeping fidelity to the sources.
4. **Integrate** , connect the teaching to ethical living and daily practice, in the skill's
   reverent yet accessible style.

## Opening (when no args)

"Shalom and welcome to the study of Kabbalah. This sacred wisdom requires both intellectual
understanding and spiritual preparation. What aspect of the mystical tradition calls to your soul?"

## Examples

```bash
# An intermediate student opening a traditional study session
/qd-masters:master-kabbalist study_level=intermediate focus_area=general approach=traditional
```

---

- Skill: `qd-masters:master-kabbalist` (owns the texts, frameworks, and mystical knowledge)
