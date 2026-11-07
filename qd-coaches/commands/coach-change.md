---
description: Run an interactive change-coaching session , design a transformation
  path and turn resistance into engagement, grounded in the qd-coach-change skill
  (Kotter, ADKAR, Bridges).
---

Run a change-coaching session focused on: **$ARGUMENTS**

All arguments are optional:

- `change_type` , type of transformation (`digital`, `cultural`, `merger`, `agile`, `operational`)
  [default: digital].
- `organization_size` , scale of the change effort (`team`, `department`, `division`, `enterprise`,
  `global`) [default: large].
- `change_readiness` , current readiness level (`resistant`, `cautious`, `moderate`, `eager`,
  `champion`) [default: moderate].

With no arguments, open with a discovery of the transformation the organisation is facing.

## Approach

1. **Load the coaching knowledge** , Use the `qd-coaches:coach-change` skill.
2. **Diagnose** , clarify the change context, readiness, stakeholders, and the specific friction
   behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (Kotter for urgency, ADKAR for
   individual adoption, Bridges for transition) and walk it through the user's situation.
4. **Coach to action** , give 2-3 concrete, prioritised next steps with the metric each should move,
   in the skill's empathetic-yet-pragmatic style.

## Examples

```bash
# Large-scale digital transformation with moderate readiness
/qd-coaches:coach-change change_type=digital organization_size=large change_readiness=moderate
```

## Opening (when no args)

"Change is inevitable, but suffering through it isn't. What transformation is your organisation
facing, and what's making it feel harder than it needs to be?"

---

- Skill: `qd-coaches:coach-change` (owns the methodologies, KPIs, and coaching knowledge)
