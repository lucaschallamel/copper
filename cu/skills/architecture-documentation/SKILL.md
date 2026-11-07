---
name: architecture-documentation
description: Architecture document authoring skill providing templates for Architecture Decision Records (ADRs), technical design specifications, and API endpoint documentation. Use when creating, reviewing, or maintaining architecture documentation artefacts.
version: 1.1.1
last_updated: '2026-10-18'
maintained_by: Lucas Challamel
applies_to: 'Primary: the enterprise-architect role | Secondary: the project-management and pre-sales roles, any agent producing architecture documentation'
---

# Skill: Architecture Documentation

## Purpose

This skill provides the reusable capability for authoring architecture documentation. It owns the
ADR template, technical design template, and API endpoint template, and defines the authoring
methods for each document type.

## Capability Contract

**What this skill provides**:

- ADR template (`resources/adr-template.md`) following the Michael Nygard format with enhancements
- Technical design template (`resources/technical-design-template.md`) for feature and system
  designs
- API endpoint template (`resources/api-endpoint-template.md`) for REST API documentation
- Authoring methods: frontmatter conventions, section structure, quality standards
- Guidance for architecture documentation governance (lifecycle, review, cross-referencing)

**What this skill does NOT provide**:

- Conceptual architecture knowledge (an architecture-patterns skill, where a kit provides one)
- Sprint planning or retrospective templates (see `cu:sprint-delivery` skill)
- User story templates (see `cu:backlog-management` skill)
- Proposal document templates (see proposal-specific skills)

---

## Authoring Methods

### When to Create Architecture Documentation

**Architecture Decision Records (ADRs)**:

- Significant architectural decisions affecting system structure
- Technology selection (frameworks, databases, cloud platforms)
- Design pattern or principle adoption
- Security architecture or compliance decisions
- Integration strategy or API design choices
- Performance or scalability architecture decisions

**Technical Design Specifications**:

- Feature-level technical design before implementation
- System-level design for new components or services
- Integration design for cross-system interfaces
- Data model design for new schemas or migrations

**API Endpoint Documentation**:

- REST API endpoint specifications
- OpenAPI/Swagger complementary documentation
- API versioning and lifecycle management
- Authentication and authorisation documentation

### File Path Conventions

```
# ADRs
docs-copper/architecture/adr/ADR-NNN-title-slug.md

# Technical Designs
docs-copper/architecture/technical-designs/TDD-NNN-title-slug.md
  OR
docs-copper/application/TDD-NNN-title-slug.md

# API Documentation
docs-copper/architecture/apis/API-NNN-endpoint-name.md
  OR
docs-copper/application/api-endpoints/API-NNN-endpoint-name.md
```

### Template Usage

Each template in `resources/` provides:

1. **YAML Frontmatter**: Standard metadata fields (ID, status, author, dates, tags)
2. **Structured Sections**: Purpose-built sections for the document type
3. **Placeholder Guidance**: Instructions for filling in each section
4. **Quality Callouts**: Tips for ensuring documentation quality

**Important**: Remove the template usage guidelines callout from generated documents.

### Quality Standards

- Write in present tense for current state, past tense for completed decisions
- Be specific: reference file paths, tool names, principle codes
- Tag all decisions with principle codes using `**[CODE]**` format
- Cross-reference related ADRs, technical designs, and user stories
- Keep lifecycle history in YAML frontmatter only; do not duplicate it in the body
- Never hardcode personal names in templates; always resolve from context

---

## Operating Model

### Current State

- Commands invoke skill-owned resources directly; legacy `_templates/` references removed under
  US-117
- This skill owns the template resources and provides authoring guidance
- All architecture documentation logic flows through this skill

### Interactive Use

Agents or users may load this skill directly when:

- Creating ADRs, technical designs, or API documentation
- Reviewing architecture documentation for quality and completeness
- Understanding documentation governance (lifecycle, review, cross-referencing)
- Generating architecture documentation outside command-driven workflows

---

## Boundary with Related Skills

### A conceptual architecture-patterns skill (kit-provided)

**Overlap zone**: Both skills touch architecture concerns.

**Boundary**:

- `cu:architecture-documentation` owns the **document templates and authoring methods** for ADRs,
  technical designs, and API documentation
- an architecture-patterns skill owns the **conceptual knowledge** of architecture patterns (C4
  model, microservices, data architecture, security patterns, scalability patterns)
- `cu:architecture-documentation` tells you HOW to write an ADR
- an architecture-patterns skill tells you WHAT patterns to consider when making architecture
  decisions
- An agent creating an ADR would load both, where a kit installs the patterns skill: patterns for
  content, documentation for format

### backlog-management

**Overlap zone**: Both skills may reference user stories and technical decisions.

**Boundary**:

- `cu:architecture-documentation` owns **architecture document templates** (ADRs, technical designs,
  API specs)
- `cu:backlog-management` owns **user story templates** and story-type guidance
- ADRs may reference user stories; user stories may reference ADRs; neither skill manages the other

### dev-journal-management

**Overlap zone**: Both capture technical decisions.

**Boundary**:

- `cu:architecture-documentation` captures **formal architecture decisions** with structured templates
  and governance
- `cu:dev-journal-management` captures **narrative session context** (why, how, what happened)
- Journal entries may reference ADRs; ADRs are not journal entries

---

## Resources

| Resource                          | Location                                         | Purpose                                                                                            |
| --------------------------------- | ------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| ADR template                      | `resources/adr-template.md`                      | Architecture Decision Record authoring                                                             |
| Technical design template         | `resources/technical-design-template.md`         | Feature/system technical design authoring                                                          |
| API endpoint template             | `resources/api-endpoint-template.md`             | REST API endpoint documentation                                                                    |
| Architecture guidelines reference | `resources/architecture-guidelines-reference.md` | Twelve-Factor, microservices patterns, cloud-native and security architecture (moved from Rule 05) |

---

## Architecture Alignment

- **ADR-009**: Follows the three-tier skill content model (stable guidance in SKILL.md, reusable
  templates in resources/, no volatile external content)
- **ADR-010**: This skill is the target owner for the ADR, technical design, and API endpoint
  template migrations from `docs-copper/_templates/` (physical deletion completed under US-117)
- **Rule 04**: All templates comply with project documentation standards
- **Rule 05 / 05a**: Architecture documentation supports the ADR governance process (`05a`)

---

## Cross-References

- **Commands**: `/cu:pipe` (pipeline delivery), `/cu:arch-review` (architectural currency review)
- **Storage**: `docs-copper/architecture/adr/`, `docs-copper/architecture/apis/`
- **Memory Bank**: `docs-copper/memory-bank/systemPatterns.md` (architectural decisions)
- **Rule**: `04-project-documentation.rules.md` (documentation standards)
- **Related Skill**: an architecture-patterns skill, where a kit provides one (conceptual knowledge)
- **Related Skill**: `cu:backlog-management` (user story templates)
- **Related Skill**: `cu:dev-journal-management` (session capture)
