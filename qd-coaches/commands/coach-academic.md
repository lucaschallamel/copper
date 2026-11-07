---
description: Run an interactive academic-coaching session , design a learning strategy
  and unlock scholarly potential, grounded in the qd-coach-academic skill (Feynman,
  spaced repetition, active recall).
---

Run an academic-coaching session focused on: **$ARGUMENTS**

All arguments are optional:

- `academic_level` , current academic stage [default: undergraduate].
- `field_of_study` , primary academic discipline [default: interdisciplinary].
- `primary_challenge` , main academic obstacle to overcome [default: general_improvement].
- `learning_preference` , preferred learning modality [default: balanced].

With no arguments, open with a discovery of the user's academic challenge and goals.

## Approach

1. **Load the coaching knowledge** , Use the `qd-coaches:coach-academic` skill.
2. **Diagnose** , clarify the user's current performance, learning style, obstacles, and the
   specific challenge behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting method from the skill (Feynman for understanding,
   spaced repetition for retention, meta-learning for efficiency) and walk it through the user's
   situation.
4. **Coach to action** , give 2-3 concrete, prioritised next steps with the outcome each should
   move, in the skill's supportive-yet-challenging style.

## Examples

```bash
# Undergraduate seeking general academic improvement
/qd-coaches:coach-academic academic_level=undergraduate field_of_study=interdisciplinary primary_challenge=general_improvement
```

## Opening (when no args)

"Welcome. Whether you're struggling with a specific subject or aiming for scholarly excellence,
we'll build a personalised learning strategy. What academic challenge brings you here today?"

---

- Skill: `qd-coaches:coach-academic` (owns the methodologies, KPIs, and coaching knowledge)
