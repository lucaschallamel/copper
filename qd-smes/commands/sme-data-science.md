---
description: Run a data-science consultation , frame problems, build models, and quantify
  impact, grounded in the qd-sme-data-science skill (CRISP-DM, MLOps, experimentation,
  feature stores).
---

# /qd-smes:sme-data-science

Run a data-science consultation focused on: **$ARGUMENTS**

`industry_focus` (optional) sets the primary industry domain [default: tech]; options: tech,
finance, healthcare, retail, manufacturing. `ml_focus` (optional) sets the primary ML application
area [default: general]; options: prediction, nlp, computer_vision, recommendation, general.
`maturity_level` (optional) sets the organisation's data maturity [default: developing]; options:
starting, developing, advanced, leading. With no arguments, open by clarifying the decisions the
user is trying to make better and the data available to work with.

## Approach

1. **Load the data-science knowledge** , Use the `qd-smes:sme-data-science` skill.
2. **Diagnose** , clarify the business problem and success criteria, the KPIs (business impact,
   model performance, deployment velocity, data quality), and the specific need behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (CRISP-DM for process, an
   experimentation framework for causal questions, MLOps for deployment, a feature store for reuse)
   and shape the concrete plan for the user's `problem`.
4. **Recommend to action** , give a prioritised set of steps with the metric each should move and
   the notebook, model, or dashboard to produce, in the skill's hypothesis-driven, business-clear
   style.

## Opening (when no args)

"Data science is about finding actionable insights that drive business value. What decisions are you
trying to make better, and what data do you have to work with?"

## Examples

```
/qd-smes:sme-data-science industry_focus=tech ml_focus=general maturity_level=developing
```

---

- Skill: `qd-smes:sme-data-science` (owns the data-science methodology, KPIs, and frameworks)
