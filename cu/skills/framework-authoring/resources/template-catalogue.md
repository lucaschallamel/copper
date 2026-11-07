---
title: 'Template Catalogue , Required Templates and Their Sections'
version: '1.1.0'
last_updated: '2026-10-19'
maintained_by: 'Lucas Challamel'
---

# Template Catalogue , Required Templates and Their Sections

Per-template detail moved out of Rule 04 by US-378 (ADR-054). Rule 04 keeps the obligation and the
list of template names; this catalogue holds each template's usage, storage and required sections.

### Mandatory Template Types

#### Architecture Decision Records (ADRs)

**Owning Skill Resource**: `skills/architecture-documentation/resources/adr-template.md`

**Future Ownership**: `cu:architecture-documentation` skill resource under `US-112`

**Usage**: ALL architecture decisions MUST use ADR template

- Numbering: Sequential (ADR-001, ADR-002, etc.)
- Storage: `/architecture/ADR/`
- Review: Peer review and stakeholder sign-off required

**Required Sections**:

- Title and ID
- Status (proposed, accepted, deprecated, superseded)
- Context and problem statement
- Decision drivers
- Considered options
- Decision outcome
- Consequences (positive and negative)
- Related decisions

#### Sprint Planning Documents

**Current Baseline Templates**:

- `skills/sprint-delivery/resources/sprint-planning-template.md`
- `skills/sprint-delivery/resources/sprint-retrospective-template.md`
- `skills/kanban-board-management/resources/kanban-board-template.md`

**Future Ownership**: `cu:sprint-delivery` skill resources under `US-111`

**Usage**: Sprint planning, retrospectives, reviews

- Storage: `/roadmap/sprint-XXX/`
- Frequency: Every sprint cycle

**Required Components**:

- Sprint goals and objectives
- User stories and acceptance criteria
- Team capacity and velocity
- Sprint backlog
- Definition of done
- Retrospective notes (post-sprint)

#### Technical Design Specifications

**Owning Skill Resource**:
`skills/architecture-documentation/resources/technical-design-template.md`

**Future Ownership**: `cu:architecture-documentation` skill resource under `US-112`

**Usage**: Feature designs, system designs, integration designs

- Storage: `/application/` or `/architecture/`
- Review: Technical lead or architect approval

**Required Sections**:

- Design overview and objectives
- System context and constraints
- Technical approach and patterns
- Data models and schemas
- API contracts and interfaces
- Security considerations
- Performance implications
- Testing strategy

#### User Stories

**Owning Skill Resource**: `skills/backlog-management/resources/user-story-template.md`

**Supporting Transitional Guidance**:

- `skills/backlog-management/resources/story-types/`
- `skills/backlog-management/scripts/`

**Future Ownership**: `cu:backlog-management` skill resources under `US-110` and `US-116`

**Usage**: Product requirements, feature requests

- Storage: `/roadmap/` or sprint-specific folders
- Format: Standard user story format with acceptance criteria

**Required Elements**:

- User story statement (As a... I want... So that...)
- Acceptance criteria
- Priority and story points
- Dependencies and blockers
- Technical notes

#### API Documentation

**Owning Skill Resource**: `skills/architecture-documentation/resources/api-endpoint-template.md`

**Future Ownership**: `cu:architecture-documentation` skill resource under `US-112`

**Usage**: API endpoint documentation, OpenAPI specifications

- Storage: `/architecture/apis/`
- Format: OpenAPI 3.0+ specification

**Required Components**:

- Endpoint path and method
- Request parameters and body schema
- Response codes and schemas
- Authentication requirements
- Example requests and responses
- Error handling documentation

#### Meeting Minutes

**Owning Skill Resource**: `skills/framework-authoring/resources/meeting-minutes-template.md`

**Future Ownership**: To be classified during the framework-authoring and skill migration pass under
`EP-101`

**Usage**: ALL client and internal meetings requiring formal documentation

- Storage: `/proposals/[proposal-folder]/minutes/` or `/projects/[project-folder]/minutes/`
- Naming: `YYYYMMDD-[Client]-[MeetingType]-Minutes-[Language].md`

**Required Sections**:

- YAML frontmatter (meeting_id, date, client, project, meeting_type, status)
- Attendees with roles and attendance status
- Meeting objectives
- Discussion summary
- Key decisions with owners
- Action items with owners and deadlines
- Next steps
- Distribution and confidentiality

**Meeting Types**:

- `discovery`: Initial client meeting, requirements gathering
- `workshop`: Collaborative working session
- `steering`: Governance/steering committee meeting
- `review`: Project review, sprint review, QBR
- `kickoff`: Project or phase kickoff
- `retrospective`: Lessons learned, improvement discussion

## Documentation Examples

Moved from Rule 04a by US-378 S7 (on demand rather than loaded with every Markdown file).

### Naming Examples

Rule 04 states the naming rules; these are its examples.

**Good**:

```
architecture-decision-record-001-microservices-adoption.md
api-authentication-endpoints-v2.md
sprint-042-planning-user-authentication.md
feature-payment-integration-technical-design.md
```

**Bad** (avoid):

```
doc1.md                  # Not descriptive
My New Feature.md        # Spaces, unclear
temp_notes_2025.md       # Vague purpose
final_FINAL_v2.md        # Poor version control
```

### CHANGELOG Format

Where a CHANGELOG exists or the user asks for one (Rule 04a):

**[ISA]**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- New feature descriptions

### Changed

- Changes to existing functionality

### Deprecated

- Soon-to-be removed features

### Removed

- Removed features

### Fixed

- Bug fixes

### Security

- Security patches
```
