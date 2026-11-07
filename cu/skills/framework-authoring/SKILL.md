---
name: framework-authoring
description: Framework-internal authoring skill providing templates and guidance for creating rules, definition-of-done documents, meeting minutes, and other framework-native artefacts. Use when creating, reviewing, or maintaining framework governance documents.
version: 1.9.1
last_updated: '2026-10-31'
maintained_by: Lucas Challamel
applies_to: 'Primary: framework maintainers | Secondary: any agent creating framework governance documents'
---

# Skill: Framework Authoring

## Purpose

This skill provides the reusable capability for authoring framework-native artefacts. It owns the
rule template, definition-of-done template, and meeting minutes template, and defines how framework
governance documents should be structured and maintained.

## Capability Contract

**What this skill provides**:

- Rule template (`resources/rule-template.md`) for creating new framework rules
- Definition-of-done template (`resources/definition-of-done.md`) for story completion criteria
- Meeting minutes template (`resources/meeting-minutes-template.md`) for formal meeting
  documentation
- Principle-codes registry reference (`resources/principle-codes-registry-reference.md`) , the
  expanded 73-code registry (per-code definitions, applications, examples, per-rule usage maps, and
  the MECE / collision / statistics analysis). Loaded on-demand; the always-on compact glossary is
  Rule 06
- Project profile , PARA (`resources/project-profile-para.md`) , the knowledge/second-brain folder
  skeleton core Rule 01 dispatches to for knowledge projects
- Project profile , Software (`resources/project-profile-software.md`) , the `src`/`tests`/`docs`
  folder skeleton core Rule 01 dispatches to for software projects
- Kit-authoring guide (`resources/kit-authoring-guide.md`) , the kit/1.0 rules for HAND-WRITING a
  kit, and the pointer to the asset quality standard that governs whether it is any good
- Authoring methods: frontmatter conventions, section structure, governance standards

**What this skill does NOT provide**:

- Language and formatting standards (see `cu:language-formatting` skill)
- Architecture document templates (see `cu:architecture-documentation` skill)
- User story templates (see `cu:backlog-management` skill)
- Sprint planning templates (see `cu:sprint-delivery` skill)

---

## Authoring Methods

### When to Create Framework Artefacts

**Rules**:

- New governance or development standards for the framework
- Updates to existing rules requiring structural changes
- Security, compliance, or quality mandates

**Definition-of-Done Documents**:

- Story-level completion criteria
- Sprint-level quality gates
- Project-level acceptance standards

**Meeting Minutes**:

- Client meetings (discovery, workshop, steering, review, kickoff, retrospective)
- Internal team meetings requiring formal documentation
- Governance committee meetings

### File Path Conventions

```
# Rules (ADR-054 D2)
rules/NN-name.rules.md            # always-on anchor (Rules 00-07)
rules/NN<letter>-name.rules.md    # paths-scoped file beside its anchor (02a, 03a, ...)

# Definition of Done (per story)
docs-copper/roadmap/backlog/definition-of-done.md
  OR embedded in story files

# Meeting Minutes
docs-copper/meeting-minutes/YYYYMMDD-[Client]-[MeetingType]-Minutes-[Language].md
  OR within project/proposal folders
```

### Classifying Rule Content (ADR-054 D1)

Every new or changed rule section is classified before it is written, applying these tests in order;
the first that matches decides:

1. **Always-on (anchor)**: T1 or T2 content, or behaviour needed before any tool call (identity,
   safety, communication, user authority).
2. **Always-on (anchor)**: guidance needed to CREATE or first-edit a file correctly (naming, file
   format, template use, the core coding principles, the required document fields, the Task Genius
   obligation). A scoped rule loads only AFTER the Edit or Write that triggers it (SP-126 M2/M3), so
   creation-time guidance can never be scoped.
3. **`paths`-scoped file**: guidance that refines later edits of matching files, with its glob
   (quoted, so Prettier does not turn it into emphasis). Never T1 or T2: `check-precedence.py`
   refuses a T1/T2 file that declares `paths`.
4. **Skill resource**: reference consulted on demand. It must be a core skill when the rule is core
   (white-label invariant).
5. **Command**: a triggered procedure; the rule keeps a pointer.
6. **Pointer**: content duplicated elsewhere; one line naming the single home.

A moved block leaves a pointer that names its destination BY PATH (`rules/02a-code.rules.md`,
`skills/<skill>/resources/<file>.md`, `skills/<skill>/SKILL.md`, `commands/<name>.md`), so the
compression-honesty gate can follow it. Glob reach: `**/*.md` and `**/memory-bank/**` match nested
and vendored paths too, so in a monorepo a scoped rule loads on any sub-project's matching file,
which costs tokens, never safety.

### Template Usage

Each template in `resources/` provides:

1. **YAML Frontmatter**: Standard metadata fields (ID, status, author, dates, tags)
2. **Structured Sections**: Purpose-built sections for the document type
3. **Placeholder Guidance**: Instructions for filling in each section
4. **Governance Notes**: Standards for maintaining framework consistency

**Important**: Remove the template usage guidelines callout from generated documents.

### Quality Standards

- Follow principle code tagging: all decisions tagged with `**[CODE]**` format
- Maintain consistency with existing framework artefacts
- Cross-reference related rules, ADRs, and stories
- Keep lifecycle history in YAML frontmatter only
- Write in British English (see `cu:language-formatting` skill)

---

## Portability Invariant , ship agnostic & stateless (TD-158)

Shipped `kits/core/` assets MUST be **agnostic and stateless**: they carry no machine-specific
state, no load-time side effects, and no reliance on a host-specific interpreter name. The
`check-portability.py` guard enforces this in CI (validate job + `ci:local`), following the US-178
"guard not a grep" model. It fails the build on:

- **Hardcoded home paths** , `/Users/<name>`, `/home/<name>`, `C:\Users\<name>`. Use a generic
  placeholder instead (`XXX`, `<user>`, `$HOME`, `~`, or a `...` ellipsis), never a real username.
- **Claude load-time blocks** , a line-leading command-expansion directive (a bang immediately
  followed by a back-quoted shell command) in `commands/*.md`. It executes at command-load time, so
  even a documentation example can fire. Make it an agent instruction run via Bash.
- **Bare `python`** , `python `/`python -m ` assumes a `python` on PATH (absent or Python 2 on many
  hosts). Use one of the two allowed forms, chosen by **who runs the call**:

  | Caller context                                                                       | Allowed form                                                 |
  | ------------------------------------------------------------------------------------ | ------------------------------------------------------------ |
  | Framework-internal verification (the harness invoking pytest/validators/`deploy`)    | `uv run python` / `uv run pytest` (the canonical invocation) |
  | User-facing standalone tools (a human running a shipped utility, e.g. usage strings) | `python3`                                                    |

  Also allowed: explicit interpreter paths (`.venv/bin/python`) and non-invocation substrings
  (`python3`, `python_requires`, prose like "a Python utility").

---

## Personal-Data Boundary , no person's identity in a shipped kit (US-352)

The sibling of the no-client-literal invariant, for PERSONAL rather than client identity.
`check-personal-data.py` scans `kits/` **and** `docs-copper/` (the egress boundary is the public git
remote, not one directory) and runs in `deploy/kit/publish_gate.py`, `ci:local` and the CI validate
job. `sign_tree` also runs it before minting, so a signature is never created over an uncleared
corpus.

**Two detectors, deliberately different severities.** REFUSE (fatal): an absolute home path (POSIX
and Windows forms), a FILLED Rule 00 inside kit content, a salted-denylist hit, a `never-migrate`
path reference, a symlink, an unreadable in-scope asset. FLAG (counted, never fatal): a
values/personal heading, an authorship key naming an individual. The split is borrowed from
`publish_gate.py` , heuristic suspicion is for humans to judge, and a permanently red gate only
trains click-through.

**It makes no semantic claim.** "Political affiliation" and "religious belief" are OPEN classes: a
regex for belief either misses (fail-open) or over-fires (unusable). The gate detects the SHAPE of a
private-workspace artefact plus a curated denylist, and its output ends "never a clean bill of
health". A gate that claimed semantic detection and quietly missed would convert an unknown risk
into a FALSE ASSURANCE , worse than no gate.

- **Add a token**: `check-personal-data.py hash "<literal>"`, as for SEC-001. Plaintext never enters
  the repo. **The denylist ships EMPTY** , the literals are only knowable per migration, so the gate
  prints an explicit `WARNING ... INERT` while it is, and each EP-108 migration story seeds it.
- **Zero files scanned is a FAILURE (exit 2)**, as SEC-001 now does too (it returned 0 with "nothing
  to scan" until TD-201). A gate that passes while scanning nothing is the defect this control
  exists to prevent , and it was found live in a sibling gate (`check-count-drift.py` printing
  "PASS: All counts match on-disk reality: {'agents': 0, ...}").
- **The rule matrix**, including all eight exemption surfaces and why each is a distinction rather
  than a hole, is in the script's own docstring. `kits/SPEC.md` s.9.4 states the enforced scope and
  the residuals.

---

## No-Client-Literal Invariant , no client secret in a shipped kit (SEC-001)

Shipped `kits/` assets MUST carry no client-confidential literal (a project codename, a client name,
a named individual). The `check-no-client-literals.py` guard (ADR-028) enforces this in CI (validate
job + `ci:local`), the confidentiality precondition US-217's marketplace publish must pass. It is
the client-secret analogue of `check-white-label-core.py` (which denylists the org's own brand),
with one critical difference: because this repo is publishable, the denylist itself cannot hold
plaintext , the literal set is stored as **salted SHA-256 hashes** in `client-literals.json`.

- **Add a literal** (living data): `check-no-client-literals.py hash "<literal>"` prints a config
  entry; paste it into `client-literals.json`, then `deploy.regenerate` and commit (the determinism
  manifest must be updated, or CI blocks). Plaintext never enters the repo.
- **Matching** is token-based + case-insensitive: `word` literals at token boundaries, `ngram`
  literals over N adjacent tokens. Generic tokens that collide with ordinary words/tools (a
  fictional "Sun"/"Cube") must be seeded as ngram-with-context, not bare words.
- **Fail-closed**: any literal match, an unreadable in-scope asset, or a malformed config blocks the
  build. Governance (owner + quarterly review cadence) and the accepted residuals (brute-force from
  the in-tree salt; deliberate obfuscation; non-text assets) are documented in ADR-028.

---

## Operating Model

### Current State (Post-US-115)

- Framework commands invoke this skill for template loading and authoring guidance
- The legacy `_templates/` references have been removed from commands; physical deletion completed
  under US-117
- All framework authoring logic flows through this skill

### Interactive Use

Agents or users may load this skill directly when:

- Creating new framework rules
- Defining completion criteria for stories or sprints
- Documenting formal meeting outcomes
- Reviewing framework governance documents for quality

---

## Boundary with Related Skills

### language-formatting

**Overlap zone**: Both skills touch content formatting.

**Boundary**:

- `cu:framework-authoring` owns the **framework governance document templates** (rules,
  definition-of-done, meeting minutes)
- `cu:language-formatting` owns the **general formatting standards** (British English, Markdown
  conventions, Mermaid diagrams, LaTeX formulas)
- `cu:framework-authoring` tells you HOW to structure a rule document
- `cu:language-formatting` tells you HOW to format the content within that rule
- An agent creating a rule would load both skills: authoring for structure, formatting for style

### architecture-documentation

**Overlap zone**: Both skills provide document templates.

**Boundary**:

- `cu:framework-authoring` owns **framework governance templates** (rules, meeting minutes, DoD)
- `cu:architecture-documentation` owns **architecture document templates** (ADRs, technical designs,
  API specs)
- Rules may reference ADRs; meeting minutes may record architecture decisions; neither skill manages
  the other

### backlog-management

**Overlap zone**: Both skills support story and sprint workflows.

**Boundary**:

- `cu:framework-authoring` owns **definition-of-done templates** and meeting minute templates
- `cu:backlog-management` owns **user story templates** and story-type guidance
- DoD is used at story completion; stories are created with backlog-management templates

---

## Resources

| Resource                     | Location                                          | Purpose                                                    |
| ---------------------------- | ------------------------------------------------- | ---------------------------------------------------------- |
| Rule template                | `resources/rule-template.md`                      | Framework rule creation                                    |
| Rules reference              | `resources/rules-reference.md`                    | Harness map, rule dependency map (moved from the rules)    |
| Template catalogue           | `resources/template-catalogue.md`                 | Required templates and their sections (moved from Rule 04) |
| Onboarding guide             | `resources/onboarding-guide.md`                   | Human developers and team leads (moved from instructions)  |
| Definition-of-done template  | `resources/definition-of-done.md`                 | Story/sprint completion criteria                           |
| Meeting minutes template     | `resources/meeting-minutes-template.md`           | Formal meeting documentation                               |
| Principle-codes registry ref | `resources/principle-codes-registry-reference.md` | Expanded 73-code registry (on-demand; glossary is Rule 06) |
| Project profile , PARA       | `resources/project-profile-para.md`               | Knowledge/second-brain folder skeleton (Rule 01 profile)   |
| Project profile , Software   | `resources/project-profile-software.md`           | Software repo folder skeleton (Rule 01 profile)            |
| Kit-authoring guide          | `resources/kit-authoring-guide.md`                | Hand-writing a kit/1.0 kit; points at the quality standard |

---

## Command-to-Skill Mapping

This section documents which commands invoke which operational skills for template resources. This
mapping is maintained here because `cu:framework-authoring` governs the framework artefact taxonomy.

| Command           | Template Resource (Legacy `_templates/`) | Target Skill             | Skill Resource                      | Status                           |
| ----------------- | ---------------------------------------- | ------------------------ | ----------------------------------- | -------------------------------- |
| `/cu:dev-journal` | `dev-journal-template.md`                | `cu:dev-journal-management` | `resources/dev-journal-template.md` | Migrated (US-115)                |
| `/cu:pipe`        | `definition-of-done.md`                  | `cu:framework-authoring`    | `resources/definition-of-done.md`   | Migrated (US-115)                |
| `/cu:status`      | `_templates/` symlink diagnostic         | N/A (health check)       | N/A                                 | US-117: diagnostic scope updated |

### How Commands Invoke Skills

Commands invoke skills using the standard skill-loading mechanism:

1. The command specifies the target skill name in its Phase instructions
2. The agent loads the skill via `skill({ name: "skill-name" })`
3. The skill provides the template resource path and authoring guidance
4. The agent uses the skill resource as the structural baseline

### Adding New Mappings

When migrating a new template into a skill:

1. Add the template to the skill's `resources/` directory
2. Update the command to reference the skill instead of `_templates/` (completed under US-115)
3. Add the mapping to this table
4. Update the command version and changelog

---

## Canonical Frontmatter Contract

This section defines the mandatory YAML frontmatter schema for framework artefacts. All commands and
agents MUST conform to this contract. The `check-frontmatter.py` validator enforces it at CI time.

### Commands (`<harness-root>/commands/*.md`)

**Required keys** (every command file MUST include these):

| Key             | Type   | Description                        |
| --------------- | ------ | ---------------------------------- |
| `description`   | string | One-line command purpose           |
| `version`       | string | Semantic version (e.g. `'1.0.0'`)  |
| `last_updated`  | string | ISO date of last meaningful change |
| `maintained_by` | string | Maintainer name                    |

**Optional keys**:

| Key         | Type   | Description                                        |
| ----------- | ------ | -------------------------------------------------- |
| `agent`     | string | Default agent the command delegates to             |
| `changelog` | list   | Version history entries (in frontmatter, not body) |

**Unknown keys are rejected** by the validator.

### Agents (`<harness-root>/agents/*.md`)

**Required keys** (every agent file MUST include these):

| Key             | Type   | Description                         |
| --------------- | ------ | ----------------------------------- |
| `description`   | string | Agent role and capabilities summary |
| `mode`          | string | OpenCode mode (`primary`, etc.)     |
| `temperature`   | float  | LLM temperature (0.0-1.0)           |
| `color`         | string | Brand colour hex code               |
| `tools`         | map    | Tool permissions map                |
| `permission`    | map    | Permission levels map               |
| `version`       | string | Semantic version                    |
| `last_updated`  | string | ISO date of last meaningful change  |
| `maintained_by` | string | Maintainer name                     |

**Optional keys**:

| Key         | Type | Description                                        |
| ----------- | ---- | -------------------------------------------------- |
| `changelog` | list | Version history entries (in frontmatter, not body) |

**Unknown keys are rejected** by the validator.

### Rationale

- The contract codifies what is already universal across all files
- No backfill was needed; all 43 files already conform
- Future files (created by `cu:agent-creator` or manually) will be validated at CI time
- See US-153 for the audit data: 3 command shapes and 2 agent shapes reduced to a single canonical
  schema each

---

## Architecture Alignment

- **ADR-009**: Follows the three-tier skill content model (stable guidance in SKILL.md, reusable
  templates in resources/, no volatile external content)
- **ADR-010**: This skill is the target owner for rule-template.md, definition-of-done.md, and
  meeting-minutes-template.md migrated from `docs-copper/_templates/` (physical deletion completed
  under US-117)
- **Rule 04**: All templates comply with project documentation standards

---

## Cross-References

- **Commands**: `/cu:init` (first-time setup), `/cu:review` (config updates)
- **Storage**: `.claude/rules/cu/`, `docs-copper/roadmap/backlog/`
- **Memory Bank**: `docs-copper/memory-bank/` (update after governance changes)
- **Rule**: `04-project-documentation.rules.md` (documentation standards)
- **Related Skill**: `cu:language-formatting` (general formatting standards)
- **Related Skill**: `cu:architecture-documentation` (architecture document templates)
- **Related Skill**: `cu:backlog-management` (user story templates)
