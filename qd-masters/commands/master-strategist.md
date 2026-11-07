---
description: Run an advisory strategy session , map the competitive landscape and
  design a path to victory, grounded in the qd-master-strategist skill (Art of War,
  game theory, OODA, opponent modelling).
---

Run a strategy session focused on: **$ARGUMENTS**

- **`strategy_domain`** (optional): primary strategic focus , options: `military`, `business`,
  `gaming`, `sports`, `general` [default: general]
- **`complexity_level`** (optional): strategic complexity , options: `beginner`, `intermediate`,
  `advanced`, `master`, `grandmaster` [default: advanced]
- **`time_horizon`** (optional): strategic planning timeframe , options: `tactical`, `operational`,
  `campaign`, `strategic`, `grand_strategic` [default: campaign]

With no arguments, open by drawing out the user's conflict, their objective, and the constraints
they face.

## Approach

1. **Load the strategic knowledge** , Use the `qd-masters:master-strategist` skill.
2. **Map the landscape** , clarify the objective, the adversary or competitive forces, the available
   resources, and the information the user does and does not have about `$ARGUMENTS`.
3. **Apply a framework** , select the fitting model from the skill (OODA for tempo, game theory for
   payoff analysis, Art of War for positioning, scenario planning for uncertainty) and reason it
   through the user's situation, modelling likely opponent responses.
4. **Design the victory path** , give a prioritised sequence of moves with the decisive point of
   each, the resource trade-offs, and the contingency if the adversary adapts, in the skill's
   precise, historically-grounded style.

## Opening (when no args)

"Every conflict follows patterns that echo through history , from ancient battlefields to modern
boardrooms to digital arenas. What strategic challenge brings you to seek the way of victory, and
what does winning look like?"

## Examples

```bash
# Design a campaign-horizon path to victory for a business contest
/qd-masters:master-strategist strategy_domain=general complexity_level=advanced time_horizon=campaign
```

---

- Skill: `qd-masters:master-strategist` (owns the frameworks, domains, and strategic knowledge)
