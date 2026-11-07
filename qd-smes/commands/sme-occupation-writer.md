---
description: Run an AI persona-architecture consultation , decompose an occupation,
  craft a precise role definition, and specify agent behaviour, grounded in the qd-sme-occupation-writer
  skill (RACI adaptation, competency mapping, instruction hierarchy).
---

Run an AI persona-architecture consultation focused on: **$ARGUMENTS**

`complexity_level` (optional) sets the depth of role specification needed , options `simple`,
`standard`, `detailed`, `comprehensive` [default: `standard`]. `domain_type` (optional) sets the
professional domain of the role , options `technical`, `creative`, `business`, `service`,
`academic`, `general` [default: `general`]. `output_format` (optional) sets the structure for the
role definition , options `narrative`, `structured`, `bullet_points`, `hybrid` [default:
`structured`]. With no arguments, open by establishing which occupation or persona must be defined
and what the AI agent will need to accomplish in that role.

## Approach

1. **Load the persona-architecture knowledge** , Use the `qd-smes:sme-occupation-writer` skill.
2. **Diagnose** , clarify the target occupation, the intended behaviour and outputs, and the
   specific definition need behind `$ARGUMENTS`.
3. **Apply a framework** , select the fitting approach from the skill (competency mapping for the
   skill set, persona architecture for the profile, instruction hierarchy for the prompt structure)
   and shape it to the `application`.
4. **Recommend to action** , produce a precise, hierarchical role definition with the behaviour
   specified and a validation check for consistency, in the skill's economical, structured style.

## Opening (when no args)

"I will help you create a precise, actionable role definition. What occupation or persona do you
need to define, and what will the AI agent need to accomplish in this role?"

## Examples

```bash
# Standard-depth, general-domain role definition in structured form
/qd-smes:sme-occupation-writer complexity_level=standard domain_type=general output_format=structured
```

---

- Skill: `qd-smes:sme-occupation-writer` (owns the persona methodology, KPIs, and prompt
  frameworks)
