# Kit Authoring Guide

How to author a COPPER `kit.md`, with one reference exemplar per entity type. The frozen format is
defined in `kits/SPEC.md` and validated by `kits/kit-1.0.schema.json` (US-177).

## Start from a reference exemplar

Copy the exemplar that matches your kit's primary entity type, then adapt it:

| Your kit is mainly a... | Copy from                            |
| ----------------------- | ------------------------------------ |
| Agent persona           | `kits/_reference/agent-kit/kit.md`   |
| Skill / capability      | `kits/_reference/skill-kit/kit.md`   |
| Command (slash command) | `kits/_reference/command-kit/kit.md` |

These live under `kits/_reference/` and are authoring templates only , not installable products. For
a worked real kit, see `kits/document-processing/kit.md` (which also shows a kit-to-kit dependency
on `kits/cascade-handler/`).

## The rules that matter

> **Quality bar (US-357)**: the rules below govern whether a kit is VALID. Whether it is GOOD ,
> concision, MECE, relevance, precision, currency, and the size budgets , is the **asset quality
> standard** in `kits/core/skills/kit-authoring/SKILL.md`, with a reviewer checklist at
> `kit-authoring/resources/prompt-quality-checklist.md`. It applies to hand-written kits exactly as
> it does to drafted ones. **Read it before writing an asset** , it lives in the drafting skill, so
> hand-authors do not meet it by default (S5 G1).

- **Frontmatter**: required keys `schema: kit/1.0`, `slug`, `title`, `summary`, `version`. COPPER
  kits also set `namespace` (registry code: `cm`/`ra`/`gd`/`qd`/`st`) and usually `tier` and
  `targets`.
- **Prefix-free slugs**: names in `slug`, `includes`, and `dependencies.kits[].slug` are NEUTRAL ,
  no `ra-`/`ta-` prefix. The adapter applies the per-target prefix at compile time (ADR-018). The
  on-disk OpenCode assets are prefixed (`ra-*`); the kit.md references their neutral names.
- **Six body sections**: Goal, When to Use, Setup, Steps, Constraints, Safety Notes , see
  `kits/SPEC.md` 4 for the per-entity-type meaning of each. Safety Notes must be workflow-specific,
  not generic advice.
- **Dependencies**: a `dependencies.kits[]` entry references another KIT (by neutral slug + pinned
  version + `compositionHint`), not a skill. If your kit needs another kit's capability, that kit
  must exist as its own `kit.md`.

## Validate before you commit

Every `kits/**/cu:kit.md` is validated against the schema by `tests/unit/test_kit_md_schema_valid.py`
(runs in CI). Run it locally:

```bash
uv run python -m pytest tests/unit/test_kit_md_schema_valid.py -q
```

## Standard compatibility (ADR-021)

COPPER skills ARE Agent Skills (`SKILL.md`, the Anthropic-originated open standard). Keep them
standard-compatible: required frontmatter is `name` + `description`; COPPER extensions (e.g.
`depends_on:`) must be ADDITIVE so a vanilla Agent-Skills parser still reads the file. Kits build a
bundle/dependency/white-label layer ABOVE the standard; the `/cu:kit` installer (US-179) delegates
per-skill placement to the Agent Skills rail. So a kit's skills install across 70+ agents via
standard tooling, and company kits ship 100% standard-compatible.

**Where kits come from (dual-source):** `/cu:kit` installs from BOTH public sources (e.g. JourneyKits
browse, public git) and **private/local** sources (a private git repo, GitLab, any git URL, a local
path, or a OneDrive/synced folder). Proprietary company kits (an organisation's IP) live in a
private/local source and are **never published to the public `skills.sh` directory**.

## References

- `kits/SPEC.md` , the frozen kit specification (sections 2-4 cover frontmatter, entities, body)
- `kits/kit-1.0.schema.json` , the machine-checkable frontmatter schema
- ADR-018 (asset prefix is compile-time output), ADR-019 (tiers), ADR-020 (kit format), ADR-021
  (build on the Agent Skills rail)
- Agent Skills standard: <https://agentskills.io/home> | install rail:
  <https://github.com/vercel-labs/skills>, <https://www.skills.sh/> | kit grounding:
  <https://www.journeykits.ai/>
