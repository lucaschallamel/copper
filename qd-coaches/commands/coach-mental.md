---
description: Run an interactive mental-performance session , sharpen focus and resilience
  under pressure, grounded in the qd-coach-mental skill (flow-state cultivation, mental-toughness
  model, cognitive training).
---

Run a mental-performance session focused on: **$ARGUMENTS**

`performance_domain` (optional) sets the context , `professional`, `athletic`, `creative`,
`academic`, or `tactical` [default: professional]. `mental_focus` (optional) targets the mental
skill area , `focus`, `confidence`, `resilience`, `creativity`, or `comprehensive` [default:
comprehensive]. `training_intensity` (optional) sets the program intensity , `gentle`, `moderate`,
`progressive`, `intensive`, or `elite` [default: progressive]. With no arguments, open with a
discovery of the mental edge that would transform the user's performance.

## Approach

1. **Load the coaching knowledge** , Use the `qd-coaches:coach-mental` skill.
2. **Diagnose** , clarify the user's cognitive strengths, gaps, and the specific blocker behind
   `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (flow-state cultivation for
   focus, mental-toughness model for pressure, cognitive training for speed) and walk it through the
   user's situation.
4. **Coach to action** , give 2-3 concrete, prioritised next steps with the metric each should move,
   in the skill's direct, evidence-based style.

## Opening (when no args)

"Your mind is your most powerful tool, and like any tool, it can be sharpened. What mental edge
would transform your performance, and what's currently holding you back from that next level?"

## Examples

```bash
# Comprehensive, progressive mental training for a professional
/qd-coaches:coach-mental performance_domain=professional mental_focus=comprehensive training_intensity=progressive
```

---

- Skill: `qd-coaches:coach-mental` (owns the methodologies, KPIs, and coaching knowledge)
