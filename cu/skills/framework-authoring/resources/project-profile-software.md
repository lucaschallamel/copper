# Project Profile , Software

**Purpose**: The folder skeleton and placement rules for a **software** project , a code repository
with source, tests, and docs. This is one of the two on-demand profiles core Rule 01 dispatches to
(the other is the PARA knowledge profile). Load it when scaffolding or organising a software repo.

**Provenance**: authored under US-340 when Rule 01 was slimmed to a generic principle + a profile
selector.

---

## Top-level structure

```
/repo-root/
├── src/              # Application/library source
├── tests/            # Unit, integration, e2e tests (mirrors src/ layout)
├── docs/             # Project documentation
│   └── adr/          # Architecture Decision Records
├── config/           # Environment-driven configuration (12-factor)
├── scripts/          # One-off and operational scripts (kept out of source)
├── memory-bank/      # AI-agent persistent memory (if the repo hosts an agent)
├── <harness-root>/   # Agentic harness scope (each host's own directory)
├── .gitignore        # Secrets and build artefacts never committed
└── README.md         # Repo overview, setup, usage
```

## Placement rules

- **Source and tests are separate top-level trees.** `tests/` mirrors `src/`'s layout so a reader
  can find the test for any module.
- **Configuration is env-driven, not hard-coded.** `config/` holds templates and defaults; real
  values come from the environment. See the Twelve-Factor section of
  `skills/architecture-documentation/resources/architecture-guidelines-reference.md` (Rule 05 points
  there) for the contract , do not restate it.
- **Scripts stay out of source.** One-off and operational scripts live in `scripts/`, never embedded
  in production modules (`[SCM]`).
- **Docs are versioned with the code.** `docs/` travels in-repo; ADRs live in `docs/adr/`.

## Owned-elsewhere contracts (link, do not restate)

- **`memory-bank/`** , its structure and update workflow are **Rule 03**'s contract. This profile
  only notes that it sits at repo root; Rule 03 owns the rest.
- **ADRs (`docs/adr/`)** , the ADR template and required sections are **Rule 04**'s contract.
- **`config/` + 12-factor** , the configuration and dev/prod-parity contract is Rule 05's, detailed
  in `architecture-guidelines-reference.md`.

## Naming conventions

- Directories and files: kebab-case, lowercase; follow the language's idiomatic conventions inside
  `src/` (e.g. package/module naming per the ecosystem).
- Docs: `[##]-[section-name]-[version].md` where ordering or iteration matters.

## Security floor

The generic secrets floor (`.env`, `secrets/`, `credentials/` never committed) is stated in core
Rule 01 and applies to every profile , do not restate it here. Add build artefacts and dependency
directories to `.gitignore` per the ecosystem.

## Cross-references

- **Core Rule 01**: the generic project-organisation principle + profile selector this profile
  instantiates.
- **Rule 02**: code implementation standards and `[SCM]` script management.
- **Rule 03**: memory-bank structure. **Rule 04**: documentation and ADR templates. **Rule 05**:
  12-factor configuration and architecture.
