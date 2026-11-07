---
description: Run an interactive digital-marketing session , grow a health or wellness
  practice authentically, grounded in the qd-coach-digital-marketing skill (ATTRACT,
  client-journey mapping, local SEO).
---

Run a digital-marketing session focused on: **$ARGUMENTS**

All arguments are optional:

- `practice_type` , type of health practice (`counseling`, `coaching`, `therapy`, `wellness`,
  `integrated`) [default: counseling].
- `growth_stage` , current practice stage (`startup`, `growth`, `established`, `scaling`) [default:
  growth].
- `marketing_focus` , primary marketing channel (`local-seo`, `content`, `social`, `referral`,
  `comprehensive`) [default: comprehensive].

With no arguments, open with a discovery of the user's ideal client and what makes their approach
unique.

## Approach

1. **Load the coaching knowledge** , Use the `qd-coaches:coach-digital-marketing` skill.
2. **Diagnose** , clarify the user's practice, ideal client, current presence, and the specific
   challenge behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (ATTRACT for the funnel,
   client-journey mapping for stages, content-pillar strategy for calendars) and walk it through the
   user's situation.
4. **Coach to action** , give 2-3 concrete, prioritised next steps with the KPI each should move, in
   the skill's practical, budget-conscious style.

## Examples

```bash
# Growth-stage counselling practice with a comprehensive marketing approach
/qd-coaches:coach-digital-marketing practice_type=counseling growth_stage=growth marketing_focus=comprehensive
```

## Opening (when no args)

"Let's explore how to grow your practice authentically. Tell me about your ideal client and what
makes your approach unique."

---

- Skill: `qd-coaches:coach-digital-marketing` (owns the methodologies, KPIs, and coaching knowledge)
