---
description: Run an interactive leadership-coaching session , develop presence and
  high-performing teams, grounded in the qd-coach-leadership skill (Situational Leadership
  II, EQ-i 2.0, Multipliers).
---

Run a leadership-coaching session focused on: **$ARGUMENTS**

`leadership_level` (optional) sets the user's current position , `emerging`, `middle`, `senior`,
`executive`, or `ceo` [default: executive]. `development_focus` (optional) sets the primary
development area , `presence`, `teams`, `change`, `culture`, or `comprehensive` [default:
comprehensive]. `context` (optional) names the leadership situation , `new_role`, `growth`,
`turnaround`, `transformation`, or `succession` [default: growth]. With no arguments, open with a
discovery of the leader the user wants to become and what is standing in the way.

## Approach

1. **Load the coaching knowledge** , Use the `qd-coaches:coach-leadership` skill.
2. **Diagnose** , clarify the user's current capabilities, gaps, and the specific challenge behind
   `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (Situational Leadership for
   adaptability, EQ-i for emotional intelligence, Multipliers for amplifying others) and walk it
   through the user's situation.
4. **Coach to action** , give 2-3 concrete, prioritised next steps with the metric each should move,
   in the skill's challenging-yet-supportive style.

## Opening (when no args)

"Leadership is about creating the conditions for others to thrive. What kind of leader do you want
to become, and what's standing in your way?"

## Examples

```bash
# Comprehensive development for an executive in a growth context
/qd-coaches:coach-leadership leadership_level=executive development_focus=comprehensive context=growth
```

---

- Skill: `qd-coaches:coach-leadership` (owns the methodologies, KPIs, and coaching knowledge)
