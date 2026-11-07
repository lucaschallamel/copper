---
description: Show current COPPER framework configuration status and health check
---

# COPPER Configuration Status

You are running the `/cu:status` command. This provides a comprehensive status report of the current
framework configuration.

## Instructions

Read all configuration files silently, then present a single comprehensive report. No interactive
questions needed.

---

## Report Structure

### 1. Framework Version

- Read the frontmatter of `rules/00-the-user.rules.md` for last update date
- Count agents in `<harness-root>/agents/` directory
- Count skills in `<harness-root>/skills/` directory
- Count commands in `<harness-root>/commands/` directory
- Count rules in `<harness-root>/rules/` directory

### 2. Setup Mode

- Read `rules/00-the-user.rules.md` and determine : Individual / Team / Project
- If Team/Project : list the team roster with roles

### 3. User Profile Summary

From `rules/00-the-user.rules.md`, display :

- Name, role, organisation, location
- Primary language, preferred tone
- Agent name (from `AGENTS.md`)

### 4. LLM Configuration

From `opencode.jsonc` :

- Default model
- Small model (if configured)
- Custom providers (list any local models configured)
- Data sovereignty flag (local-only or cloud-allowed)

### 5. MCP Server Health

Run `/mcp` and present results :

| Server       | Status             | Notes            |
| ------------ | ------------------ | ---------------- |
| brave-search | Connected / Failed | API key required |
| excel        | Connected / Failed |                  |
| ...          | ...                | ...              |

### 6. Symlink Status (TR2 + TR3)

Scan the vault root for symlinked directories and report the generic shared-resource pointers plus
any symlinks the installed **project-structure profile** defines (these vary by project type , a
software repo, a knowledge base, or a kit-supplied profile such as a consulting-delivery kit's
`clients/[name]` / institutional-folder hierarchy) :

| Symlink                      | Target | Status                    |
| ---------------------------- | ------ | ------------------------- |
| `_CV/`                       | [path] | Active / Broken / Missing |
| `_References/`               | [path] | Active / Broken / Missing |
| `_templates/`                | [path] | Active / Broken / Missing |
| `_branding/`                 | [path] | Active / Broken / Missing |
| _(profile-defined symlinks)_ | [path] | Active / Broken / Missing |

### 7. Pending Configuration

List any items marked `[TO BE CONFIGURED]` in `00-the-user.rules.md`.

### 8. Recommendations

Based on the status, suggest actions :

- If MCP servers are failing : suggest proxy fixes or npm reinstall
- If symlinks are broken : suggest running `/cu:init` Step 7 again
- If `[TO BE CONFIGURED]` items exist : suggest running `/cu:review`
- If no team members and mode is Team/Project : suggest `/cu:onboard`
- If framework hasn't been updated recently : suggest `git pull`

---

## Output Format

Present the entire report as a single, well-formatted Markdown document. Do not ask any questions;
this is a read-only diagnostic command.
