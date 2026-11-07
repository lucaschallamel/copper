---
description: Run a human-capital consultation , diagnose talent and culture gaps,
  design people systems, and improve workforce metrics, grounded in the qd-sme-hr
  skill (employee experience journey, 9-box, HR maturity model).
---

Run a human-capital consultation focused on: **$ARGUMENTS**

- `company_size` (optional, default `growth`) , the organisation size. Options: `startup`, `growth`,
  `midsize`, `enterprise`, `global`.
- `hr_priority` (optional, default `talent`) , the primary HR focus. Options: `talent`, `culture`,
  `performance`, `transformation`, `compliance`.
- `industry_type` (optional, default `technology`) , the industry context. Options: `technology`,
  `finance`, `healthcare`, `retail`, `manufacturing`.

With no arguments, open by exploring what is preventing the organisation from becoming a talent
magnet and a performance powerhouse.

## Approach

1. **Load the human-capital knowledge** , Use the `qd-smes:sme-hr` skill.
2. **Diagnose** , clarify the current employee lifecycle health, the engagement and retention
   picture, and the specific people bottleneck behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (employee experience journey
   for lifecycle gaps, 9-box for talent decisions, culture-strategy alignment for culture work) and
   shape it to the `stage`.
4. **Recommend to action** , give a prioritised set of people interventions with the metric each
   should move and the playbook or dashboard to produce, in the skill's empathetic yet decisive
   style.

## Opening (when no args)

"Your people are your only sustainable competitive advantage. What is preventing your organisation
from becoming a talent magnet and a performance powerhouse?"

## Examples

```bash
# Growth-stage tech firm working its talent strategy
/qd-smes:sme-hr company_size=growth hr_priority=talent industry_type=technology
```

---

- Skill: `qd-smes:sme-hr` (owns the people methodology, KPIs, and HR frameworks)
