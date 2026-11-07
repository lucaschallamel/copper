---
description: Review and update existing COPPER framework personalisation
---

# COPPER Configuration Review

You are running the `/cu:review` command. This reviews an existing COPPER personalisation and allows
the user to update any section.

## Instructions

- Read the current `rules/00-the-user.rules.md` and `AGENTS.md` files first.
- Present a summary of the current configuration to the user.
- Ask which sections they want to review or update.
- For any updates, follow the same question format as `/cu:init` (one at a time, skip/back
  supported).
- After changes, show a diff summary of what was modified.

---

## Step 1 : Current Configuration Summary

Read and display a summary of the current personalisation :

1. Read `rules/00-the-user.rules.md` and list all configured sections
2. Read `AGENTS.md` and show the agent name and key settings
3. Check `opencode.jsonc` for the current LLM model and filesystem paths
4. List any active symlinks (TR2 + TR3) by scanning the vault for symlinked directories
5. Flag any items marked `[TO BE CONFIGURED]` from a previous `/cu:init` run

Present this as a structured table :

| Section                   | Status                       | Last value |
| ------------------------- | ---------------------------- | ---------- |
| User Overview             | Configured / Missing         | [summary]  |
| Communication Preferences | Configured / Missing         | [summary]  |
| Professional Context      | Configured / Missing         | [summary]  |
| Technical Environment     | Configured / Missing         | [summary]  |
| Workflow Preferences      | Configured / Missing         | [summary]  |
| AI Preferences            | Configured / Missing         | [summary]  |
| Symlinks TR2              | X active / 0                 | [list]     |
| Symlinks TR3              | X active / 0                 | [list]     |
| Pending items             | X items `[TO BE CONFIGURED]` | [list]     |

---

## Step 2 : Selection

Ask :

> Which sections would you like to review or update?
>
> - **(1)** User Overview (identity, organisation, reporting)
> - **(2)** Communication & Cultural Preferences
> - **(3)** Professional Context (industry, regulations, deliverables)
> - **(4)** Technical Environment (OS, tools, constraints)
> - **(5)** Accessibility & Workflow
> - **(6)** AI Agent Preferences (name, language, instructions)
> - **(7)** Symlinks (TR2 institutional + TR3 clients)
> - **(8)** Complete pending `[TO BE CONFIGURED]` items
> - **(A)** Review everything
>
> You can choose multiple (e.g. "2, 4, 7").

---

## Step 3 : Guided Update

For each selected section :

1. Show the current values
2. Ask if the user wants to change each field (show current value as default)
3. If the user says "keep" or "ok", move to the next field
4. If the user provides a new value, update the file immediately
5. Support "skip" and "back" as in `/cu:init`

---

## Step 4 : Summary & Verification

After all updates :

1. Show a diff summary : what changed vs what stayed the same
2. If symlinks were added or modified, verify they are accessible
3. List any remaining `[TO BE CONFIGURED]` items
4. Suggest running `/cu:status` to verify the updated configuration
