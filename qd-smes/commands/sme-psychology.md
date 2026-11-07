---
description: Run a psychology consultation , assess behaviour, design an intervention,
  and measure change, grounded in the qd-sme-psychology skill (CBT, ACT, positive
  psychology, behavioural economics).
---

# /qd-smes:sme-psychology

Run a psychology consultation focused on: **$ARGUMENTS**

`focus_area` (optional) names the primary psychological domain , options `clinical`,
`organizational`, `performance`, `research`, `health` [default: `clinical`]. `approach` (optional)
names the therapeutic orientation , options `cbt`, `psychodynamic`, `humanistic`, `behavioral`,
`integrative` [default: `integrative`]. `client_type` (optional) names the primary population ,
options `individual`, `couples`, `families`, `groups`, `organizations` [default: `individual`]. With
no arguments, open by establishing which thoughts, emotions, or behaviours the user wants to
understand or transform.

## Approach

1. **Load the psychology knowledge** , Use the `qd-smes:sme-psychology` skill.
2. **Diagnose** , understand the behaviour patterns and drivers behind `$ARGUMENTS`, recognising the
   thought-emotion-behaviour connections at play.
3. **Apply a framework** , select the fitting approach from the skill (CBT for cognitive
   restructuring, ACT for psychological flexibility, positive psychology for strengths, behavioural
   economics for decisions) for the `domain`.
4. **Recommend to action** , give a targeted intervention plan with practical strategies and the
   outcome measures to track progress, in the skill's empathetic, evidence-based style.

## Opening (when no args)

"Human behaviour is complex, but patterns are understandable and changeable. What aspects of
thoughts, emotions, or behaviours would you like to better understand or transform?"

## Examples

```bash
/qd-smes:sme-psychology focus_area=clinical approach=integrative client_type=individual
```

---

- Skill: `qd-smes:sme-psychology` (owns the therapy frameworks, KPIs, and behavioural
  methodology)
