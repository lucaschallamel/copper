---
description: First-time COPPER framework personalisation (individual, team, or project
  setup)
---

# COPPER Framework Personalisation

You are running the `/cu:init` command. This is a guided, interactive setup to personalise the
COPPER framework for a new user or team.

## Global Instructions

- Follow the steps **sequentially**. Ask questions **one at a time** and wait for the user's answer
  before proceeding.
- After each section, update the relevant files immediately.
- **Show progress** : prefix each question with its number and section (e.g. "Section 2, question
  3/7 :").
- **Skip/defer** : if the user says "skip", "later", or "pass", accept it and write
  `[TO BE CONFIGURED]` as the value in the rules file.
- **Corrections** : if the user says "back", "correction", or "undo", let them revise their previous
  answer and update the file accordingly.
- **All data is stored locally** in Markdown files within the vault. Nothing is transmitted to
  external services.

### Idempotent Mode (existing configuration detected)

**Before asking any question**, check if `rules/00-the-user.rules.md` already contains a value for
that field.

- **If a value exists** : present it to the user : "I found this : **[existing value]**. Keep it?
  (yes / update)" . If the user says "yes", "keep", or "ok", move to the next question without
  modifying the file.
- **If the value is `[TO BE CONFIGURED]`** : flag it and ask the full question : "This was skipped
  previously. Let's fill it in now :"
- **If no value exists** : ask the question normally.

This makes `/cu:init` safe to run multiple times. It works for both first-time setup and
reconfiguration of an existing framework.

---

## Step 0 : Language, Mode & Pre-flight

### 0a : Language Selection

Ask :

> **In which language would you like to conduct this setup?**
>
> - **(A) English**
> - **(B) Français**

Store the answer. **All subsequent questions, responses, and file content must be in the chosen
language.** If French, translate every question below before asking.

### 0b : Setup Mode

Ask :

> **This setup takes approximately 15-20 minutes (full guided) or 5 minutes (quick).**
>
> **How would you like to proceed?**
>
> - **(1) Full guided setup** : step-by-step interview, one question at a time
> - **(2) Quick setup** : provide your key details in a single message
>
> And **what type of setup is this?**
>
> - **(A) Individual** : a single user working alone
> - **(B) Team** : two or more people working together as a functional team
> - **(C) Project** : a team assembled for a specific project with a defined deliverable

If the user chooses **Quick setup**, ask them to provide all key details in one message (name, role,
organisation, location, OS, editor, language preference, agent name) and skip directly to Step 7
(Symlinks) then Step 8 (Verification). Otherwise, proceed step by step.

### 0c : Pre-flight Check

Silently verify :

1. Run `/mcp` and note which servers are Connected vs Failed
2. Confirm `opencode.jsonc` exists at the vault root
3. Confirm `.claude/rules/cu/00-the-user.rules.md` exists
4. Confirm `AGENTS.md` exists at the vault root
5. Note the current default LLM model in `opencode.jsonc`

Report the results to the user. If critical files are missing, stop and advise.

---

## Step 1 : Identity & Organisation

Ask these questions **one at a time** :

**For all modes :**

1. What is your full name? (first name, last name)
2. What organisation do you work for?
3. Where are you located? (city, state/canton, country)
4. _(Auto-inferred)_ Timezone is determined automatically from the city/country provided in
   question 3. Do NOT ask the user for their timezone explicitly.
5. What business line, division, or function do you belong to?
6. What is your professional role/title?
7. Who do you report to? (name and role)
8. What is the primary focus of your daily work?
9. Is your primary work client-facing (billable) or internal?

**If Team or Project mode, for each additional team member :** 10. Team member full name 11. Email
address _(optional, stored locally only)_ 12. Role in the team 13. Key responsibilities 14. Working
hours and timezone 15. On-site vs remote pattern (e.g. Mon-Wed on-site, Thu-Fri remote) (Repeat
10-15 for each member. Ask "Any more team members?" after each.)

**If Project mode, additionally :** 16. What is the project name? 17. Brief description of the
project (2-3 sentences) 18. What is the nature of the team / project type? (e.g. software
development, knowledge base, consulting, sales pursuit , this informs the project-structure profile
applied in Step 7 TR3) 19. What methodology does the team follow? (Scrum, SAFe, PRINCE2, Kanban,
GTD, TOGAF, ad hoc, other)

**Action** : update `rules/00-the-user.rules.md` with a structured "User Overview" or "Team
Overview" section including all collected information. For teams, include a member roster table with
columns: Name, Role, Responsibilities, Timezone, Pattern.

---

## Step 2 : Communication & Cultural Preferences

Ask one at a time :

1. What pronouns should the AI use when referring to you? (he/him, she/her, they/them, other, no
   preference) _(optional)_
2. What is your nationality? _(optional, for cultural context only)_
3. What is your primary working language?
4. Secondary language? (if any)
5. Tertiary language? (if any)
6. What communication perspective best describes your role? (Executive / Leadership / Commercial /
   Technical / Academic, can choose multiple)
7. What level of decision authority do you have? (final decision maker / recommender / contributor)
8. What tone do you prefer for AI interactions? (Professional and formal / Strategic and concise /
   Warm and collaborative / Direct and factual / Academic and thorough, can choose multiple)
9. What formatting do you prefer for outputs? (Markdown / Plain text / Word-ready)

**If Individual mode only :** 10. Are there any personal values or cultural considerations you'd
like the AI to be aware of? _(optional)_ 11. Any other personal preferences for how the AI should
interact with you?

**Action** : update `rules/00-the-user.rules.md` with a "Communication Preferences" section.

---

## Step 3 : Professional Context

Ask one at a time :

1. What industry sectors do you primarily work in? (banking/finance, healthcare, public sector,
   energy, retail, technology, other)
2. Does your work involve any regulated context? (financial-sector regulators, GDPR/privacy law,
   DORA, banking secrecy, healthcare regulations, public procurement, none)
3. What types of documents do you typically produce? (proposals, RFPs/RFIs, architecture docs, code,
   presentations, meeting notes, reports, other)
4. Does your organisation have branded document templates you need to use? (Word templates,
   PowerPoint templates, letterheads, CSS themes)
5. Do you have any data classification constraints? (e.g. confidential data that must not leave the
   machine, regulated data, client NDA restrictions, none)
6. Are you comfortable sending document content to cloud LLMs, or do you require local-only
   processing?

**Action** : update `rules/00-the-user.rules.md` with a "Professional Context" section. If the user
requires local-only processing, note this prominently and flag it for LLM provider configuration in
Step 6.

---

## Step 4 : Technical Environment

Ask one at a time :

1. What operating system do you use? (Windows 10/11, macOS, Linux distro)
2. How much RAM does your machine have? (relevant for local LLM model sizing)
3. What is your primary editor or IDE? (Obsidian / VS Code / JetBrains / Visual Studio / other)
4. What terminal do you use? (PowerShell / zsh / bash / Warp / Windows Terminal / Obsidian
   integrated)
5. What office suite? (Microsoft 365 / Google Workspace / LibreOffice)
6. What diagramming tools? (Draw.io / Excalidraw / Mermaid / Visio / Figma / none)
7. What version control? (Git+GitHub / Git+GitLab / Git+Azure DevOps / SVN / none)
8. Do you use container platforms? (Docker / Podman / none)
9. What CRM or collaboration platform? (Teams / Slack / Jira / Confluence / Notion / Monday / none)
10. What cloud/storage provider? (OneDrive / Google Drive / AWS / Azure / GCP / NAS / custom)
11. What programming languages do you work with? (Python / Java / JavaScript/TypeScript / C# / Go /
    none / other)
12. Are you currently using any AI coding assistants? (GitHub Copilot / Cursor / Windsurf / Cody /
    TabNine / none)
13. Are you behind a corporate proxy or VPN? If so, which services are blocked? (npm, pip, API
    endpoints, none known)
14. How would you describe your appetite for open source? (strong preference / pragmatic / prefer
    commercial)
15. Any other daily tools the AI should know about?

**If Team/Project mode :** 16. Is this a shared/standardised environment, or does each team member
have their own setup?

**Action** : update `rules/00-the-user.rules.md` with a "Technical Environment" section. Also update
the `filesystem` MCP server args in `opencode.jsonc` with the user's Documents folder path and any
code directories mentioned. If proxy/VPN issues are reported, add them to a "Known Constraints"
subsection.

---

## Step 5 : Accessibility & Workflow _(optional section)_

Ask one at a time. Preface with : "These questions are optional but help fine-tune the experience."

1. Do you have any accessibility preferences? (e.g. high-contrast output, screen reader
   compatibility, dyslexia-friendly formatting, none)
2. What are your typical working hours? (e.g. 08:00-17:00, flexible)
3. How often do you produce deliverables? (daily / weekly / sprint-based / milestone-based)
4. Do you have existing knowledge bases or document repositories the framework should connect to?
   (SharePoint sites, Confluence spaces, internal wikis, none)
5. Does your team follow any specific methodology? (Scrum / SAFe / PRINCE2 / Kanban / GTD / TOGAF /
   ad hoc) _(skip if already answered in Step 1 for Project mode)_

**Action** : update `rules/00-the-user.rules.md` with a "Workflow Preferences" section. Mark any
skipped questions as `[TO BE CONFIGURED]`.

---

## Step 6 : AI Agent Identity & Preferences

Ask one at a time :

1. What name do you want your AI agent to go by? (e.g. COPPER, Atlas, Sage)
2. Should the AI always respond in a specific language by default? (e.g. always French / always
   English / match my language)
3. Should the AI ask for confirmation before modifying files? (yes / no / only for destructive
   operations)
4. Any instructions the AI should always follow? (e.g. "never use emojis", "always include sources",
   "keep responses concise")
5. Any instructions the AI should never do? (e.g. "never delete files without asking", "never commit
   to Git automatically")

**Action** :

- Update `AGENTS.md` : set the agent name in the identity section, add global instructions
- Update `rules/00-the-user.rules.md` : add an "AI Preferences" section
- Scan the vault folder structure and update the structure section in `AGENTS.md` to match
- If data sovereignty was flagged in Step 3, ensure `AGENTS.md` includes a directive to never send
  content to cloud LLMs

---

## Step 7 : Shared-Resource Symlinks + Project Structure (TR2 + TR3)

Ask :

> Do you want to set up connections to shared resources now? This creates local symlinks (shortcuts)
> from your vault to OneDrive or network folders.
>
> - **(A) Yes, let's set them up now**
> - **(B) Skip for now** (you can run `/cu:init` again later to add them)

If yes, proceed :

### TR2 : Institutional Data

Ask one at a time :

1. Do you have a shared **CV/resume** folder? If so, what is the full path? (e.g.
   `/Users/XXX/OneDrive - company.com/Shared/CV` or `C:\Users\XXX\OneDrive - company.com\Shared\CV`)
2. Do you have a shared **references** folder? Path?
3. Do you have a shared **templates** folder? (Word models, logos, CSS themes) Path?
4. Do you have a shared **branding** folder? (brand guidelines, logos) Path?
5. Do you have a shared **institutional/company info** folder? (org chart, RSE, certifications)
   Path?
6. Any other shared folders to connect?

For each path provided, **create the symlink automatically** :

```bash
# macOS/Linux
ln -s "[provided_path]" "[vault_root]/_CV" # or _References, _templates, etc.
```

```powershell
# Windows
mklink / D "[vault_root]\_CV" "[provided_path]"
```

Report the result of each symlink creation (success or error).

### TR3 : Project Structure (profile-dispatched)

The concrete top-level structure a vault should adopt depends on the project TYPE, not on a
hardcoded assumption. Rule 01 dispatches to a **project-structure profile** (Rule 01 profile
selector); `/cu:init` applies whichever the adopter's installed profile/kit provides.

Ask :

> What kind of project is this vault for?
>
> - **(A) Software repository** , applies the Software profile (`src/`, `tests/`, `docs/`,
>   `config/`, `scripts/`, `memory-bank/`).
> - **(B) Knowledge / documentation / second-brain** , applies the PARA profile (`01-projects/` ..
>   `04-archives/`).
> - **(C) A specialised structure from an installed kit** , if the adopter has installed a kit that
>   ships its own project-structure profile (for example a consulting-delivery kit whose
>   project-structure skill defines a proposal/tender/client/project hierarchy and its
>   `clients/[name]` shared-folder symlinks), apply that kit's profile instead.

Load the matching project-structure resource and apply its top-level layout + any shared-folder
symlinks it defines. The two core profiles ship as framework-authoring resources
(`project-profile-software.md`, `project-profile-para.md`); a kit-supplied profile lives in that
kit. Core does not hardcode any one project type's scaffolding.

**Action** : record which TR2 shared-resource pointers and which project-structure profile are
active in the vault's own notes or README (the core project-organisation rule no longer stores
per-vault symlink structure , the concrete hierarchy lives in the installed project-structure
profile).

---

## Step 8 : Verification & Smoke Test

After all updates are made :

1. **Show a summary** of all changes made to :

   - `rules/00-the-user.rules.md` (list all sections created)
   - `AGENTS.md` (agent name, instructions)
   - `opencode.jsonc` (if filesystem paths or providers were modified)
   - Symlinks created (list each with status)
   - Items marked `[TO BE CONFIGURED]` (if any questions were skipped)

2. **Run a smoke test** :

   - Greet the user by name in their preferred language and tone
   - Confirm the agent name is set correctly
   - List any MCP servers that failed in the pre-flight check and suggest fixes
   - If symlinks were created, verify at least one is accessible (try to list its contents)

3. **Recommend next steps** based on what was configured :
   - If symlinks were skipped : "Run `/cu:init` again to set up institutional and client symlinks"
   - If proxy issues were flagged : "Investigate npm proxy configuration to enable MCP servers"
   - If local-only processing was requested : "Configure a local LLM provider (Ollama or LM Studio)
     if not already done"
   - If Brave Search API key is missing : "Obtain a Brave Search API key for web search
     capabilities"
   - General : "Try `/cu:status` to verify the full configuration"
   - If questions were skipped : "Run `/cu:review` when ready to complete the `[TO BE CONFIGURED]`
     items"

---

## Quick Setup Mode

If the user chose quick setup in Step 0b, ask them to provide all key information in one message.
Parse their input and populate all files. Then jump to Step 7 (symlinks) and Step 8 (verification).

**Template for quick setup :**

> I am [FULL NAME], [ROLE] at [ORGANISATION] in [CITY, COUNTRY]. I work in [INDUSTRY] on [PRIMARY >
>
> > FOCUS]. I use [OS] with [EDITOR]. My preferred language is [LANGUAGE] and I want a [TONE]
> > communication style. [DATA CONSTRAINTS if any]. Please name the AI agent [NAME].
