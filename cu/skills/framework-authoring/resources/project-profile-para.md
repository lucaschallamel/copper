# Project Profile , PARA (knowledge / second-brain)

**Purpose**: The folder skeleton and placement rules for a **knowledge** project , a second-brain
vault, a documentation or research workspace, a personal/organisational knowledge base. This is one
of the two on-demand profiles core Rule 01 dispatches to (the other is the Software profile). Load
it when scaffolding or organising knowledge work.

**Provenance**: authored under US-340 when Rule 01 was slimmed to a generic principle + a profile
selector. Applies the PARA method (Projects, Areas, Resources, Archives).

---

## Top-level structure

```
/vault-root/
├── 01-projects/      # Active efforts with a goal and an end date
├── 02-areas/         # Ongoing responsibilities with no end date (durable)
├── 03-resources/     # Topic/reference material, useful across projects and areas
├── 04-archives/      # Inactive items from the other three (never deleted)
└── README.md         # Vault overview and conventions
```

## Placement rules

- **Actionability determines placement.** The more actionable an item, the higher it sits:
  `01-projects/` (acting now, has an end) > `02-areas/` (maintaining, no end) > `03-resources/`
  (reference) > `04-archives/` (inactive).
- **Projects are disposable; areas are durable.** A project ends and **graduates** to
  `04-archives/`; an area persists. Never delete , archive.
- **One item, one tier.** An item lives in exactly one of the four folders at a time; move it when
  its actionability changes (a finished project graduates to archives; a revived one comes back to
  `01-projects/`).
- **Resources are cross-cutting.** Reference material that serves multiple projects/areas lives in
  `03-resources/`, not duplicated inside each project.

## Naming conventions (inside `01-projects/`)

- ISO date prefix for chronological sorting: `[YYYYMMDD]-[short-name]` (e.g.
  `20260709-quarterly-review`).
- kebab-case, lowercase, hyphens for spaces; no spaces, accents, or special characters.
- Version suffixes where a document iterates: `-v1`, `-v2`.

## Security floor

The generic secrets floor (`.env`, `secrets/`, `credentials/` never committed) is stated in core
Rule 01 and applies to every profile , do not restate it here.

## Cross-references

- **Core Rule 01**: the generic project-organisation principle + profile selector this profile
  instantiates.
- **Rule 04**: documentation standards, naming, and templates (do not restate , link).
- **Rule 03**: if the vault hosts an AI agent, the memory-bank structure is Rule 03's contract.
