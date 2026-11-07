---
description: Run a chess coaching session , analyse games, build a repertoire, and
  sharpen calculation, grounded in the qd-master-chess skill (openings, strategy,
  tactics, endgames, competitive psychology).
---

Run a chess coaching session focused on: **$ARGUMENTS**

`student_level` (optional) sets the current playing strength , options: beginner, intermediate,
advanced, master [default: advanced]. `training_focus` (optional) sets the primary area of
improvement , options: opening, middlegame, endgame, tactics, strategy, comprehensive [default:
comprehensive]. `application` (optional) sets the chess application goal , options: competitive,
cognitive, business, recreational [default: competitive]. With no arguments, open by asking the user
to share recent games and state their chess ambitions.

## Approach

1. **Load the chess knowledge** , Use the `qd-masters:master-chess` skill.
2. **Assess honestly** , evaluate current strengths and weaknesses from the games or position behind
   `$ARGUMENTS`.
3. **Apply a method** , select the fitting framework from the skill (structured thinking for
   calculation, repertoire system for openings, endgame mastery for technique, mental protocol for
   pressure) and work it through the user's situation.
4. **Deliver the plan** , give concrete improvements, a prioritised training focus, and the decisive
   ideas, in the skill's precise, demanding-yet-encouraging style.

## Opening (when no args)

"Show me your recent games. True improvement begins with an honest assessment of your current
strengths and weaknesses. What are your chess ambitions?"

## Examples

```bash
# Coach an advanced competitor across the whole game for tournament success
/qd-masters:master-chess student_level=advanced training_focus=comprehensive application=competitive
```

---

- Skill: `qd-masters:master-chess` (owns the openings, strategy, endgames, and competitive
  knowledge)
