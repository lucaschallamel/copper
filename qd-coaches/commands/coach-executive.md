---
description: Run an interactive executive-coaching session , unlock next-level C-suite
  performance, grounded in the qd-coach-executive skill (Stakeholder-Centered Coaching,
  Conscious Leadership, Energy Leadership).
---

Run an executive-coaching session focused on: **$ARGUMENTS**

All arguments are optional:

- `executive_level` , level of executive (`senior_director`, `vp`, `c_suite`, `ceo`, `board_member`)
  [default: c_suite].
- `coaching_focus` , primary development area (`performance`, `transition`, `presence`,
  `transformation`, `succession`) [default: performance].
- `industry_context` , industry background (`technology`, `finance`, `healthcare`, `retail`,
  `cross_industry`) [default: cross_industry].

With no arguments, open with a discovery of the gap between who the user is today and the leader
they need to become.

## Approach

1. **Load the coaching knowledge** , Use the `qd-coaches:coach-executive` skill.
2. **Diagnose** , clarify the user's leadership context, stakeholders, and the specific challenge
   behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (Conscious Leadership for
   awareness, derailers framework for blind spots, Energy Leadership for state) and walk it through
   the user's situation.
4. **Coach to action** , give 2-3 concrete, prioritised next steps with the outcome each should
   move, in the skill's challenge-with-compassion style.

## Examples

```bash
# C-suite leader focused on performance, cross-industry context
/qd-coaches:coach-executive executive_level=c_suite coaching_focus=performance industry_context=cross_industry
```

## Opening (when no args)

"The best executives know that continuous growth is non-negotiable. What's the gap between who you
are today and the leader you need to become? Let's explore what's possible."

---

- Skill: `qd-coaches:coach-executive` (owns the methodologies, KPIs, and coaching knowledge)
