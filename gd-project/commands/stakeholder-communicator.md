---
description: Run a stakeholder-communication session , craft audience-targeted reports,
  presentations, executive summaries, and change or crisis messaging that translate
  technical work into business narrative, grounded in the gd-stakeholder-communicator
  skill.
---

Craft stakeholder communication for: **$ARGUMENTS**

All arguments are optional. `audience_type` (default `mixed`; primary stakeholder group, options:
`executive`, `technical`, `customer`, `investor`, `mixed`); `communication_tone` (default
`informative`; message tone and urgency, options: `informative`, `urgent`, `celebratory`,
`cautionary`, `neutral`); `format_preference` (default `report`; preferred output format, options:
`report`, `presentation`, `dashboard`, `email`, `video-script`, `pr-description`);
`validation_level` (default `standard`; validation strictness, options: `basic`, `standard`,
`strict`, `enterprise`). With no arguments, open by drawing out the audience, the core message, and
the decision or action it should drive.

## Approach

1. **Load the communication knowledge** , Use the `gd-project:stakeholder-communicator` skill.
2. **Frame the message** , clarify the `audience_type` behind `$ARGUMENTS`, what they need to know and
   decide, and the facts and risks to convey honestly.
3. **Architect the narrative** , apply the fitting frameworks from the skill (power/interest grid,
   message architecture, pyramid principle, SCARF) to layer the message for the audience at the
   chosen `communication_tone`.
4. **Produce and check** , at the requested `validation_level`, deliver in the chosen
   `format_preference` with the right depth, verify it represents status accurately, and respect
   confidentiality boundaries.

## Opening (when no args)

"Let's get this message landing with the right people. Who is the audience, what is the one thing
they must take away, and what decision or action should it drive?"

## Examples

```bash
# Urgent executive update
/gd-project:stakeholder-communicator audience_type=executive communication_tone=urgent

# Enterprise-grade presentation
/gd-project:stakeholder-communicator format_preference=presentation validation_level=enterprise
```

---

- Skill: `gd-project:stakeholder-communicator` (owns the methodologies, frameworks, and KPIs)
- Related agent: the proactive `gd-project:stakeholder-communicator` agent loads the same skill
  autonomously.
