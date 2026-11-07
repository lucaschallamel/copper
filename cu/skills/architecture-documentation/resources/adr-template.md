---
adr_id: ADR-NNN
title: '[Title of ADR]'
version: '1.0.0'
last_updated: 'YYYY-MM-DD'
status: Proposed
date: YYYY-MM-DD
deciders: []
technical_story: ''
tags: []
superseded_by: ''
---

## Context and Problem Statement

[Describe the context and problem that this decision addresses. What are the forces at play? What is
the issue that needs to be resolved?]

**Background**:

- [Relevant background information]
- [Current situation or challenge]
- [Why this decision is needed now]

**Scope**: [Describe the scope of this ADR - which components, layers, or modules are affected]

---

## Decision Drivers

[List the key drivers, requirements, and constraints that influenced the decision.]

**Functional Requirements**:

- [Requirement 1]
- [Requirement 2]

**Non-Functional Requirements**:

- [Performance requirements]
- [Security considerations]
- [Maintainability needs]

**Constraints**:

- [Existing infrastructure limitations]
- [Team skills and capabilities]
- [Project timeline constraints]
- [Budget constraints]

**Project or Organisational Alignment** (if applicable):

- [How this aligns with project principles or delivery philosophy]
- [Client, regulatory, or organisational considerations]
- [Quality and precision requirements]

---

## Considered Options

[List the options that were considered. For each option, provide a brief description.]

### Option 1: [Name of Option 1]

**Description**: [Brief description of this option]

**Implementation Approach**:

- [How this would be implemented]
- [Key technical details]

**Pros**:

- [Benefit 1] **[PRINCIPLE CODE]**
- [Benefit 2] **[PRINCIPLE CODE]**
- [Benefit 3]

**Cons**:

- [Drawback 1] **[PRINCIPLE CODE]**
- [Drawback 2]
- [Drawback 3]

**Estimated Effort**: [High | Medium | Low]

**Risk Level**: [High | Medium | Low]

---

### Option 2: [Name of Option 2]

**Description**: [Brief description of this option]

**Implementation Approach**:

- [How this would be implemented]
- [Key technical details]

**Pros**:

- [Benefit 1] **[PRINCIPLE CODE]**
- [Benefit 2]
- [Benefit 3]

**Cons**:

- [Drawback 1] **[PRINCIPLE CODE]**
- [Drawback 2]
- [Drawback 3]

**Estimated Effort**: [High | Medium | Low]

**Risk Level**: [High | Medium | Low]

---

### Option 3: [Name of Option 3] (if applicable)

**Description**: [Brief description of this option]

**Implementation Approach**:

- [How this would be implemented]

**Pros**:

- [Benefit 1]
- [Benefit 2]

**Cons**:

- [Drawback 1]
- [Drawback 2]

**Estimated Effort**: [High | Medium | Low]

**Risk Level**: [High | Medium | Low]

---

## Decision Outcome

**Chosen option**: **"[Name of Chosen Option]"**

**Rationale**: [Explain why this option was chosen over the others, referencing the decision drivers
and the pros/cons of the options.]

Key reasons:

- [Reason 1 with principle code reference] **[PRINCIPLE CODE]**
- [Reason 2] **[PRINCIPLE CODE]**
- [Reason 3]
- [How it addresses decision drivers]

---

## Consequences

### Positive Consequences

[Describe the positive outcomes or benefits expected from this decision.]

- [Positive outcome 1] **[PRINCIPLE CODE]**
- [Positive outcome 2]
- [Positive outcome 3]
- [Business value delivered]
- [Technical debt avoided or reduced]

### Negative Consequences

[Describe any drawbacks, risks, or trade-offs associated with this decision.]

- [Trade-off 1] **[PRINCIPLE CODE]**
- [Risk 1 and mitigation strategy]
- [Technical debt introduced]
- [Increased complexity in area X]

**Mitigation Strategies**:

- [How to address negative consequence 1]
- [How to address negative consequence 2]

---

## Validation

**Success Criteria**: [How will we know if this decision was successful?]

**Metrics**:

- [Metric 1]: [Target value]
- [Metric 2]: [Target value]
- [Metric 3]: [Target value]

**Review Schedule**:

- **Short-term** (1-3 months): [What to assess]
- **Medium-term** (6 months): [What to assess]
- **Long-term** (1 year): [What to assess]

**Validation Methods**:

- [Testing approach]
- [Performance benchmarks]
- [User feedback mechanism]
- [Code review criteria]

---

## Implementation Plan

**Phase 1**: [Initial implementation phase]

- [Task 1]
- [Task 2]

**Phase 2**: [Follow-up work]

- [Task 1]
- [Task 2]

**Dependencies**:

- [Dependency 1]
- [Dependency 2]

**Timeline**: [Estimated timeline]

**Owner**: [Person or team responsible]

---

## Related Decisions

**Supersedes**:

- [Link to superseded ADR if applicable]

**Related ADRs**:

- `ADR-XXX`: [Brief relationship description in present tense]
- `ADR-YYY`: [Brief relationship description in present tense]

**Influenced By**:

- [External standard or framework]
- [Industry best practice]
- [Team experience or lessons learned]

---

## References

**Technical Documentation**:

- [Link to technical documentation]
- [Link to API documentation]
- [Link to architecture diagrams]

**External Resources**:

- [Link to related articles or papers]
- [Link to vendor documentation]
- [Link to relevant discussions or RFCs]

**Internal Resources**:

- User Stories: [US-XXX](../../roadmap/sprint-XXX/user-stories/US-XXX-name.md)
- Technical Design: [Link if applicable]
- Memory Bank: [../memory-bank/systemPatterns.md](../memory-bank/systemPatterns.md)

---

**ADR Status**: [Proposed | Accepted | Deprecated | Superseded] **Last Reviewed**: YYYY-MM-DD

---

> [!tip]- TEMPLATE USAGE GUIDELINES **To be excluded from the generated ADR.**
>
> **INSTRUCTIONS FOR COMPLETING THIS TEMPLATE**:
>
> 1. Replace `ADR-NNN` with appropriate ID:
>    - Use sequential numbering: `ADR-001`, `ADR-002`, `ADR-003`, etc.
>    - Location: `docs-copper/architecture/adr/`
> 2. Fill in all [placeholder text] with actual content
> 3. Update YAML frontmatter with real values
> 4. Tag all decisions/principles with appropriate codes: [SF], [RP], [DRY], etc.
> 5. Remove sections not applicable to your decision
> 6. Remove options not seriously considered (keep 2-4 meaningful options)
> 7. Update status as ADR progresses through lifecycle
> 8. Link to related user stories, technical designs, or other ADRs
> 9. Delete this entire callout section before finalising
>
> **FRONTMATTER FIELD GUIDANCE**:
>
> - `adr_id`: Format `ADR-NNN` (scaffold: 000+, project: 001+)
> - `title`: Brief, descriptive title of the decision
> - `version`: Semantic version of the ADR document itself
> - `last_updated`: Last content update date (YYYY-MM-DD)
> - `changelog`: Structured amendment history kept in YAML frontmatter
> - Do not duplicate changelog history in the ADR body; YAML frontmatter is the canonical source
> - `status`: Proposed | Accepted | Deprecated | Superseded
> - `date`: Date of ADR creation (YYYY-MM-DD)
> - `deciders`: Array of people involved in decision (["Name1", "Name2"])
> - `technical_story`: Optional link to related user story or epic
> - `tags`: Array of principle codes (["SF", "RP", "CA"])
> - `superseded_by`: Leave empty unless ADR is superseded (then: "ADR-XXX")
>
> **STATUS LIFECYCLE**:
>
> - `Proposed`: ADR drafted, awaiting review and decision
> - `Accepted`: Decision approved and in effect
> - `Deprecated`: Decision no longer recommended but not yet replaced
> - `Superseded`: Decision replaced by newer ADR (reference in superseded_by field)
>
> **ADR LOCATION**:
>
> - All ADRs are stored in `docs-copper/architecture/adr/`
> - Sequential numbering: ADR-001, ADR-002, etc.
> - Examples: Technology stack, API design, database choice, architecture decisions
>
> **MICHAEL NYGARD FORMAT ALIGNMENT**: This template follows Michael Nygard's ADR format with
> enhancements:
>
> - Clear context and problem statement
> - Decision drivers explicitly listed
> - Multiple options considered with pros/cons
> - Decision outcome with rationale
> - Consequences (positive and negative)
> - Additional sections: Validation, Implementation Plan, References
>
> **WHEN TO CREATE AN ADR**:
>
> - Significant architectural decisions affecting system structure
> - Technology choice decisions (frameworks, databases, platforms)
> - Process or workflow decisions with long-term impact
> - Design patterns or principles adoption
> - Security or compliance decisions
> - Integration or interface design decisions
>
> **BEST PRACTICES**:
>
> - Be concise but comprehensive - quality over quantity
> - Focus on "why" more than "what" - rationale is key
> - Document rejected options - learning from alternatives is valuable
> - Use principle codes to track quality attributes
> - Link to related artefacts (user stories, designs, tests)
> - Review and update regularly - ADRs are living documents
> - Involve relevant stakeholders in decision-making process

> [!info]- TEMPLATE DATA (YAML BackMatter) For indexing, search, and validation purposes. **To be
> excluded from the generated ADR.**
>
> ```yaml
> template_name: 'ADR Template'
> template_description:
>   'Architecture Decision Record template following Michael Nygard format with comprehensive option
>   analysis and validation criteria'
> template_scope:
>   'Use for documenting significant architectural, technical, and design decisions across scaffold
>   and project contexts'
> template_version: '1.0.0'
> template_last_updated: '2025-10-26'
> template_status: 'active'
> template_category: 'architecture'
> template_maintained_by: '[Project Team]'
>
> principle_codes_emphasized:
>   - SF # Simplicity First
>   - RP # Readability Priority
>   - CA # Clean Architecture
>   - ARC # Architecture Stability
>   - SD # Strategic Documentation
>   - DM # Dependency Minimalism
>   - MOD # Modularity Focus
>   - ORG # Organisational Clarity
>
> cross_references:
>   - 'User Story Template: user-story-template.md'
>   - 'Rule Template: rule-template.md'
>   - 'Technical Design Template: (to be created)'
>   - 'Memory Bank: docs-copper/memory-bank/'
>   - 'ADR Directory: docs-copper/architecture/adr/'
>
> applies_to:
>   - 'Architects documenting architectural decisions'
>   - 'Technical leads making design choices'
>   - 'Engineers proposing significant technical changes'
>   - 'Team members reviewing and approving decisions'
>
> usage_pattern:
>   when_to_create:
>     - 'Significant architectural decisions affecting system structure'
>     - 'Technology selection (frameworks, databases, cloud platforms)'
>     - 'Design pattern or principle adoption'
>     - 'Security architecture or compliance decisions'
>     - 'Integration strategy or API design choices'
>     - 'Performance or scalability architecture decisions'
>   naming_convention: 'ADR-001, ADR-002, ADR-003, ... (sequential numbering)'
>   storage_location: 'docs-copper/architecture/adr/'
>
> related_workflows:
>   - 'Link from user stories when decision impacts implementation'
>   - 'Reference in technical design documents'
>   - 'Update docs-copper/memory-bank/activeContext.md with key decisions'
>   - 'Review in sprint retrospectives for decision quality'
>   - 'Create follow-up ADRs when decisions need refinement'
>   - 'Supersede outdated ADRs rather than modifying historical decisions'
>
> quality_standards:
>   - 'Clear problem statement and context'
>   - 'At least 2-3 options considered with honest pros/cons'
>   - 'Decision rationale explicitly stated'
>   - 'Consequences (positive and negative) documented'
>   - 'Validation criteria defined'
>   - 'Principle codes tagged throughout'
>   - 'Related ADRs cross-referenced'
>
> external_references:
>   - 'Michael Nygard ADR format:
>     https://github.com/joelparkerhenderson/architecture-decision-record'
>   - 'ADR GitHub repo: https://adr.github.io/'
>   - 'Documenting Architecture Decisions:
>     https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions'
> ```
