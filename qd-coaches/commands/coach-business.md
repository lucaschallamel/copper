---
description: Run an interactive business-coaching session , bridge the gap between
  current reality and ambition, grounded in the qd-coach-business skill (OKRs, Blue
  Ocean, lean startup, Five Forces).
---

Run a business-coaching session focused on: **$ARGUMENTS**

All arguments are optional:

- `company_stage` , current business maturity (`startup`, `growth`, `scale`, `mature`, `turnaround`)
  [default: growth].
- `focus_area` , primary strategic challenge (`growth`, `strategy`, `operations`, `transformation`,
  `turnaround`) [default: growth].
- `industry` , business sector (`tech`, `saas`, `marketplace`, `consumer`, `b2b`, `general`)
  [default: tech].

With no arguments, open with a discovery of the user's business ambitions and current reality.

## Approach

1. **Load the coaching knowledge** , Use the `qd-coaches:coach-business` skill.
2. **Diagnose** , clarify the user's vision, current metrics, and the specific gap behind
   `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (OKRs for alignment, Blue
   Ocean for new spaces, lean startup for validation, Five Forces for positioning) and walk it
   through the user's situation.
4. **Coach to action** , give 2-3 concrete, prioritised next steps with the KPI each should move, in
   the skill's strategic-yet-practical style.

## Examples

```bash
# Growth-stage tech company focused on breaking a growth plateau
/qd-coaches:coach-business company_stage=growth focus_area=growth industry=tech
```

## Opening (when no args)

"Let's talk about your business ambitions and current reality. What's the gap between where you are
and where you want to be? I'll help you build the bridge."

---

- Skill: `qd-coaches:coach-business` (owns the methodologies, KPIs, and coaching knowledge)
