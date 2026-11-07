---
description: Run an interactive corporate-coaching session , diagnose culture and
  design a transformation journey, grounded in the qd-coach-corporate skill (Kotter,
  Competing Values, 7S, ADKAR).
---

Run a corporate-transformation session focused on: **$ARGUMENTS**

All arguments are optional:

- `transformation_type` , primary focus of transformation (`cultural`, `digital`, `merger`, `agile`,
  `restructuring`) [default: cultural].
- `organization_size` , size of organisation (`mid-market`, `enterprise`, `multinational`) [default:
  enterprise].
- `urgency_level` , pace of required change (`crisis`, `accelerated`, `strategic`) [default:
  strategic].

With no arguments, open with a discovery of the compelling reason for change and what success looks
like to stakeholders.

## Approach

1. **Load the coaching knowledge** , Use the `qd-coaches:coach-corporate` skill.
2. **Diagnose** , clarify the current culture, change drivers, stakeholders, and the specific
   challenge behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (Competing Values for culture,
   7S for alignment, ADKAR for adoption) and walk it through the user's situation.
4. **Coach to action** , give 2-3 concrete, prioritised next steps with the metric each should move,
   in the skill's authoritative-yet-collaborative style.

## Examples

```bash
# Enterprise cultural transformation at a strategic pace
/qd-coaches:coach-corporate transformation_type=cultural organization_size=enterprise urgency_level=strategic
```

## Opening (when no args)

"Let's explore your organisation's transformation journey. What's the compelling reason for change,
and what does success look like to your stakeholders?"

---

- Skill: `qd-coaches:coach-corporate` (owns the methodologies, KPIs, and coaching knowledge)
