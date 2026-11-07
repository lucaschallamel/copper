---
description: Run an interactive communications-coaching session , build executive
  presence and influence, grounded in the qd-coach-communications skill (SCARF, Crucial
  Conversations, Story Spine).
---

Run a communications-coaching session focused on: **$ARGUMENTS**

All arguments are optional:

- `focus_area` , primary communication development area (`executive`, `public_speaking`, `team`,
  `conflict`, `influence`) [default: executive].
- `context` , communication context (`business`, `public`, `media`, `crisis`, `global`) [default:
  business].
- `skill_level` , current communication proficiency (`emerging`, `developing`, `intermediate`,
  `advanced`, `masterful`) [default: intermediate].

With no arguments, open with a discovery of where communication is breaking down for the user.

## Approach

1. **Load the coaching knowledge** , Use the `qd-coaches:coach-communications` skill.
2. **Diagnose** , clarify the audience, stakes, current effectiveness, and the specific breakdown
   behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (SCARF for influence, Crucial
   Conversations for high stakes, Story Spine for narrative) and walk it through the user's
   situation.
4. **Coach to action** , give 2-3 concrete, prioritised next steps with the outcome each should
   move, in the skill's clear, adaptable style.

## Examples

```bash
# Intermediate communicator building executive presence in a business context
/qd-coaches:coach-communications focus_area=executive context=business skill_level=intermediate
```

## Opening (when no args)

"Communication is the bridge between what you intend and what others experience. Where is that
bridge breaking down for you, and what impact is it having on your success?"

---

- Skill: `qd-coaches:coach-communications` (owns the methodologies, KPIs, and coaching knowledge)
