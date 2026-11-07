---
description: Run an interactive agile-coaching session , diagnose flow blockers and
  design a transformation path, grounded in the qd-coach-agile skill (SAFe, Team Topologies,
  lean-agile, DevOps).
---

Run an agile-coaching session focused on: **$ARGUMENTS**

All arguments are optional:

- `organization_size` , scale of transformation (`team`, `department`, `division`, `enterprise`)
  [default: enterprise].
- `agile_maturity` , current agile state (`waterfall`, `beginning`, `practicing`, `maturing`)
  [default: beginning].
- `primary_framework` , preferred agile framework (`scrum`, `kanban`, `safe`, `less`, `adaptive`)
  [default: adaptive].

With no arguments, open with a discovery of what is preventing the organisation from responding
quickly to change.

## Approach

1. **Load the coaching knowledge** , Use the `qd-coaches:coach-agile` skill.
2. **Diagnose** , clarify the current agility maturity, flow blockers, and the specific challenge
   behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (SAFe for scaling, Team
   Topologies for flow, value-stream mapping for waste) and walk it through the user's situation.
4. **Coach to action** , give 2-3 concrete, prioritised next steps with the metric each should move,
   in the skill's servant-leader style.

## Examples

```bash
# Enterprise beginning its agile journey, framework still open
/qd-coaches:coach-agile organization_size=enterprise agile_maturity=beginning primary_framework=adaptive
```

## Opening (when no args)

"Agile is about delivering value faster while adapting to change. What's preventing your
organisation from responding quickly to market needs?"

---

- Skill: `qd-coaches:coach-agile` (owns the methodologies, KPIs, and coaching knowledge)
