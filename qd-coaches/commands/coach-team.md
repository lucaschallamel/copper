---
description: Run an interactive team-coaching session , turn a group into a high-performing
  team, grounded in the qd-coach-team skill (Five Dysfunctions, Tuckman's stages,
  psychological safety).
---

Run a team-coaching session focused on: **$ARGUMENTS**

`team_type` (optional) sets the type of team , `leadership`, `project`, `functional`,
`cross_functional`, or `virtual` [default: leadership]. `team_maturity` (optional) sets the
development stage , `forming`, `storming`, `norming`, `performing`, or `reforming` [default:
forming]. `primary_challenge` (optional) names the main issue , `trust`, `communication`,
`alignment`, `performance`, or `innovation` [default: performance]. With no arguments, open with a
discovery of what is preventing the team from reaching its full potential.

## Approach

1. **Load the coaching knowledge** , Use the `qd-coaches:coach-team` skill.
2. **Diagnose** , clarify the team's health, dynamics, and the specific dysfunction behind
   `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (Five Dysfunctions for trust,
   Tuckman's stages for phase, psychological safety for risk-taking) and walk it through the team's
   situation.
4. **Coach to action** , give 2-3 concrete, prioritised next steps with the metric each should move,
   in the skill's warm-challenger style.

## Opening (when no args)

"Great teams aren't just groups of talented individuals , they're collaborative units that achieve
the impossible together. What's preventing your team from reaching its full potential?"

## Examples

```bash
# Performance focus for a forming leadership team
/qd-coaches:coach-team team_type=leadership team_maturity=forming primary_challenge=performance
```

---

- Skill: `qd-coaches:coach-team` (owns the methodologies, KPIs, and coaching knowledge)
