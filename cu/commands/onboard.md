---
description: Add a new team member to an existing COPPER team or project setup
---

# COPPER Team Member Onboarding

You are running the `/cu:onboard` command. This adds a new team member to an existing team or
project configuration.

## Prerequisites

This command requires an existing team or project setup (created via `/cu:init` with mode B or C).
If `rules/00-the-user.rules.md` is configured for Individual mode, advise the user to run `/cu:init`
again in Team or Project mode first.

## Instructions

- Read `rules/00-the-user.rules.md` first to understand the current team roster.
- Ask questions one at a time.
- Support "skip", "back", and corrections.
- Show progress indicators.
- Use the same language as the existing configuration.

---

## Step 1 : Verify Existing Setup

1. Read `rules/00-the-user.rules.md`
2. Confirm it's a Team or Project configuration
3. Display the current team roster to the user
4. Ask : "How many new team members are you adding?"

---

## Step 2 : New Member Details

For each new team member, ask one at a time :

1. Full name (first name, last name)
2. Email address _(optional, stored locally only)_
3. Professional role/title
4. Role in the team
5. Key responsibilities
6. Who do they report to? (name and role)
7. Working hours and timezone
8. On-site vs remote pattern (e.g. Mon-Wed on-site, Thu-Fri remote)
9. Primary working language
10. Any specific tools or constraints? (e.g. proxy restrictions, different OS)

Ask "Any more team members to add?" after each.

---

## Step 3 : Update Files

1. **Update `rules/00-the-user.rules.md`** : add the new member(s) to the team roster table
2. If the new member has different technical constraints (e.g. proxy, different OS), add a note to
   the "Known Constraints" subsection
3. If the team is growing beyond the original project scope, ask if the project description needs
   updating

---

## Step 4 : Onboarding Checklist

Generate a personalised onboarding checklist for each new member :

> **Onboarding checklist for [NAME] :**
>
> 1. [ ] Install prerequisites (see COPPER-Setup-Configuration-Guide.md, Part 1)
> 2. [ ] Request GitHub Copilot Enterprise licence via ITOPS
> 3. [ ] Clone the framework repository : `git clone [repo-url]`
> 4. [ ] Copy the `.obsidian` config archive
> 5. [ ] Run `/cu:init` in Individual mode to personalise their own rules
> 6. [ ] Verify MCP connectivity (`/mcp`)
> 7. [ ] Test with `/cu:status`
> 8. [ ] Schedule a walkthrough session with the team lead

Ask if the user wants this checklist saved as a Markdown file (e.g. `onboarding-[name].md`).

---

## Step 5 : Summary

Show :

1. Updated team roster (before and after)
2. New member(s) added with their details
3. Onboarding checklist(s) generated
4. Any items flagged for follow-up
