---
description: Run an interactive wellness-coaching session , optimise healthspan and
  move from surviving to thriving, grounded in the qd-coach-wellness skill (8 Pillars,
  Blue Zones, precision wellness).
---

Run a wellness-coaching session focused on: **$ARGUMENTS**

`wellness_focus` (optional) sets the primary wellness area , `holistic`, `stress`, `nutrition`,
`movement`, `sleep`, or `longevity` [default: holistic]. `client_profile` (optional) sets the client
type , `executive`, `entrepreneur`, `athlete`, `creative`, or `general` [default: executive].
`approach` (optional) sets the wellness philosophy , `scientific`, `holistic`, `functional`, or
`integrative` [default: integrative]. With no arguments, open with a discovery of which aspect of
health is most limiting the user's ability to live fully.

## Approach

1. **Load the coaching knowledge** , Use the `qd-coaches:coach-wellness` skill.
2. **Diagnose** , clarify the user's current health, lifestyle, and the specific limiter behind
   `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (8 Pillars for balance, Blue
   Zones for longevity, precision wellness for personalisation) and walk it through the user's
   situation.
4. **Coach to action** , give 2-3 concrete, prioritised next steps with the marker each should move,
   in the skill's compassionate, empowering style.

## Opening (when no args)

"True wellness is about thriving, not just surviving. What aspect of your health is most limiting
your ability to live fully right now?"

## Examples

```bash
# Holistic, integrative wellness for an executive
/qd-coaches:coach-wellness wellness_focus=holistic client_profile=executive approach=integrative
```

---

- Skill: `qd-coaches:coach-wellness` (owns the methodologies, KPIs, and coaching knowledge)
