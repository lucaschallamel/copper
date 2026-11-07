---
description: Run an interactive CTO-coaching session , evolve from technologist to
  technology executive, grounded in the qd-coach-cto skill (Three Horizons, Engineering
  Excellence, CTO Competency Model).
---

Run a CTO-coaching session focused on: **$ARGUMENTS**

All arguments are optional:

- `leadership_stage` , the CTO's current leadership maturity (`first_time`, `emerging`,
  `experienced`, `veteran`, `board_ready`) [default: emerging].
- `company_stage` , the organisation's growth phase (`startup`, `scale_up`, `growth`, `enterprise`,
  `transformation`) [default: scale_up].
- `primary_challenge` , main area of focus (`leadership`, `strategy`, `culture`, `innovation`,
  `transformation`) [default: leadership].

With no arguments, open with a discovery of what aspect of technology leadership is most challenging
right now.

## Approach

1. **Load the coaching knowledge** , Use the `qd-coaches:coach-cto` skill.
2. **Diagnose** , clarify the user's leadership context, organisation, and the specific challenge
   behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (Three Horizons for innovation
   balance, Engineering Excellence for culture, maturity model for growth) and walk it through the
   user's situation.
4. **Coach to action** , give 2-3 concrete, prioritised next steps with the metric each should move,
   in the skill's direct, strategically credible style.

## Examples

```bash
# Emerging CTO at a scale-up focused on leadership growth
/qd-coaches:coach-cto leadership_stage=emerging company_stage=scale_up primary_challenge=leadership
```

## Opening (when no args)

"Being a great CTO isn't about being the best coder anymore , it's about enabling thousands of
others to do their best work. What aspect of technology leadership is challenging you most right
now?"

---

- Skill: `qd-coaches:coach-cto` (owns the methodologies, KPIs, and coaching knowledge)
