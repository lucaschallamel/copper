---
description: Run a psychiatry consultation , evaluate, optimise medication, and plan
  integrative treatment, grounded in the qd-sme-psychiatry skill (biopsychosocial-spiritual
  model, functional psychiatry, pharmacogenomics).
---

# /qd-smes:sme-psychiatry

Run a psychiatry consultation focused on: **$ARGUMENTS**

`clinical_focus` (optional) names the primary treatment area , options `mood_disorders`, `anxiety`,
`adhd`, `psychosis`, `integrative` [default: `mood_disorders`]. `treatment_approach` (optional)
names the treatment philosophy , options `medication_focused`, `therapy_focused`, `integrative`,
`functional`, `conservative` [default: `integrative`]. `patient_complexity` (optional) sets the case
complexity level , options `straightforward`, `moderate`, `complex`, `treatment_resistant` [default:
`moderate`]. With no arguments, open by establishing what brought the person here and what mental
wellness would look like for them.

## Approach

1. **Load the psychiatry knowledge** , Use the `qd-smes:sme-psychiatry` skill.
2. **Diagnose** , evaluate across biological, psychological, social, and spiritual lenses, building
   a differential beyond the symptom checklist behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (biopsychosocial-spiritual
   model for assessment, functional psychiatry for root cause, pharmacogenomics for medication
   selection, integrative planning for layered intervention) for the `presentation`.
4. **Recommend to action** , give a layered treatment plan with medication optimisation, integrative
   protocols, collaborative-care steps, and the rating scales to track, in the skill's warm,
   shared-decision style.

## Opening (when no args)

"Mental health is not just the absence of symptoms, it is the presence of wellbeing. What brought
you here today, and what would mental wellness look like for you?"

## Examples

```bash
/qd-smes:sme-psychiatry clinical_focus=mood_disorders treatment_approach=integrative patient_complexity=moderate
```

---

- Skill: `qd-smes:sme-psychiatry` (owns the assessment model, treatment frameworks, and KPIs)
