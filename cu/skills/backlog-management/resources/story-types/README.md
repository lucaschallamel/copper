# Story Type Guidance

Detailed guidance for each backlog item type used in a COPPER project backlog.

## Story Types

| Prefix  | Type                   | File                                    |
| ------- | ---------------------- | --------------------------------------- |
| **EP**  | Epic                   | `EP-epic-guidance.md`                   |
| **US**  | User Story             | `US-user-story-guidance.md`             |
| **BUG** | Bug/Defect             | `BUG-defect-guidance.md`                |
| **TD**  | Technical Debt         | `TD-technical-debt-guidance.md`         |
| **SEC** | Security               | `SEC-security-guidance.md`              |
| **SP**  | Spike                  | `SP-spike-guidance.md`                  |
| **CI**  | Continuous Improvement | `CI-continuous-improvement-guidance.md` |
| **RA**  | Risk Action            | `RA-risk-action-guidance.md`            |

## Persona Guidance

Use project-specific personas in user stories. Define them in the product context and keep naming
consistent across backlog items.

Example structure:

| Persona         | Role   | Domain            |
| --------------- | ------ | ----------------- |
| **[Persona A]** | [Role] | [Business domain] |
| **[Persona B]** | [Role] | [Business domain] |
| **[Persona C]** | [Role] | [Business domain] |

## Shared Progress Update Convention

- supported backlog artefacts should place a collapsed `Progress updates` callout immediately after
  frontmatter
- use bullet-first entries only, with the newest dated update first
- keep dates plain: `YYYY-MM-DD`
- use the validation scripts under `../../scripts/README.md` and `progress-block-autofix.py` when
  normalising existing files

## Related

- Skill overview: `../../SKILL.md` (backlog-management)
- User-story template: `../user-story-template.md`
- Validation scripts: `../../scripts/` (sibling skill scripts, migrated under US-116)

## Status

This story guidance set has been migrated into the `cu:backlog-management` skill resources under US-110
(EP-101). The original files in `docs-copper/_templates/us-docs/story-types/` have been removed
under US-117 deprecation.

---

_Last Updated: 2026-07-07_
