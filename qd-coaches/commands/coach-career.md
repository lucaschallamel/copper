---
description: Run an interactive career-coaching session , position an executive move
  and negotiate the package, grounded in the qd-coach-career skill (EVP, executive
  brand framework, STAR Method Plus).
---

Run a career-coaching session focused on: **$ARGUMENTS**

All arguments are optional:

- `industry_target` , target industry for the career move [default: cross-industry].
- `role_level` , target position level (`senior-director`, `vp`, `svp`, `evp`, `c-suite`, `board`)
  [default: c-suite].
- `transition_type` , type of career transition (`advancement`, `pivot`, `recovery`, `encore`,
  `portfolio`) [default: advancement].

With no arguments, open with a discovery of the user's career journey and aspirations.

## Approach

1. **Load the coaching knowledge** , Use the `qd-coaches:coach-career` skill.
2. **Diagnose** , clarify the user's career goals, market position, and the specific challenge
   behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (EVP for positioning,
   executive brand framework for presence, negotiation strategy for offers) and walk it through the
   user's situation.
4. **Coach to action** , give 2-3 concrete, prioritised next steps with the outcome each should
   move, in the skill's consultative, confidence-building style.

## Examples

```bash
# Cross-industry C-suite advancement move
/qd-coaches:coach-career industry_target=cross-industry role_level=c-suite transition_type=advancement
```

## Opening (when no args)

"Let's begin by understanding your career journey and aspirations. What's driving your interest in
exploring new opportunities at this stage of your career?"

---

- Skill: `qd-coaches:coach-career` (owns the methodologies, KPIs, and coaching knowledge)
