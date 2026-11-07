---
description: Run a user-story session , decompose epics into INVEST-compliant, sprint-ready
  stories with Given-When-Then acceptance criteria, grounded in the gd-user-story-generator
  skill.
---

Generate user stories for: **$ARGUMENTS**

All arguments are optional. `story_format` (default `classic`; preferred story-writing format,
options: `classic`, `job-story`, `feature-story`, `technical-story`); `detail_level` (default
`comprehensive`; amount of detail in acceptance criteria, options: `minimal`, `standard`,
`comprehensive`, `exhaustive`); `estimation_type` (default `fibonacci`; story-point estimation
approach, options: `fibonacci`, `t-shirt`, `hours`, `ideal-days`); `validation_level` (default
`standard`; validation strictness, options: `basic`, `standard`, `strict`, `enterprise`). With no
arguments, open by drawing out the epic or feature, the users it serves, and the value it should
deliver.

## Approach

1. **Load the user-story knowledge** , Use the `gd-project:user-story-generator` skill.
2. **Frame the work** , clarify the epic or feature behind `$ARGUMENTS`, the users and personas it
   serves, and the user value to maximise.
3. **Decompose and specify** , apply the fitting frameworks from the skill (INVEST, story mapping,
   BDD/ATDD, jobs-to-be-done) to break the work into right-sized stories in the chosen
   `story_format`, with Given-When-Then acceptance criteria at the chosen `detail_level`.
4. **Size and validate** , at the requested `validation_level`, estimate with the chosen
   `estimation_type`, map dependencies, confirm each story is testable with a clear Definition of
   Done, and deliver a sprint-ready, value-ordered set.

## Opening (when no args)

"Let's turn this into stories your team can pick up and ship. What epic or feature are we working
on, who are the users, and what value should each slice deliver?"

## Examples

```bash
# Comprehensive job-story decomposition
/gd-project:user-story-generator story_format=job-story detail_level=comprehensive

# Enterprise-grade validation
/gd-project:user-story-generator validation_level=enterprise
```

---

- Skill: `gd-project:user-story-generator` (owns the methodologies, frameworks, and KPIs)
- Related agent: the proactive `gd-project:user-story-generator` agent loads the same skill autonomously.
