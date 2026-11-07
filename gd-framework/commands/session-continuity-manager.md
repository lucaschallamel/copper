---
description: Run a session-handoff session , capture state, document achievements
  and risks, and leave a resumption-ready environment, grounded in the gd-session-continuity-manager
  skill (STARS, continuity matrix, Git continuity patterns).
---

Create a session handoff for: **$ARGUMENTS**

All arguments are optional. `handoff_depth` (default `comprehensive`; options: `quick`, `standard`,
`comprehensive`, `archival`); `time_gap` (default `next-day`; options: `same-day`, `next-day`,
`next-week`, `extended`) sets how far ahead to plan resumption; `recipient` (default `same-user`;
options: `same-user`, `team-member`, `new-developer`, `any`); `validation_level` (default
`standard`; options: `basic`, `standard`, `strict`, `enterprise`). With no arguments, open by
capturing what was achieved this session and when work resumes.

## Approach

1. **Load the continuity knowledge** , Use the `gd-framework:session-continuity-manager` skill.
2. **Capture state** , using STARS, document the summary, open tasks, achievements, risks, and the
   environment/Git state behind `$ARGUMENTS`.
3. **Prepare for resumption** , at the chosen `handoff_depth`, tune the handoff for the `time_gap`
   and `recipient`, recording decision rationale and a clean re-entry path.
4. **Validate** , at the requested `validation_level`, confirm the working tree is reproducible and
   the handoff answers every likely resumption question, then deliver it.

## Opening (when no args)

"Let's capture this session so it resumes cleanly. What did you achieve, what is still open, and
when (and by whom) will the work be picked up again?"

## Examples

```bash
# Comprehensive handoff for a teammate picking up the work next week
/gd-framework:session-continuity-manager handoff_depth=comprehensive time_gap=next-week recipient=team-member

# Archival-depth handoff validated to enterprise strictness
/gd-framework:session-continuity-manager handoff_depth=archival validation_level=enterprise
```

---

- Skill: `gd-framework:session-continuity-manager` (owns the methodologies, patterns, and continuity
  knowledge)
- Related agent: the proactive `gd-framework:session-continuity-manager` agent loads the same skill
  autonomously.
