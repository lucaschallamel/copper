---
description: Multi-agent review and implementation planning for user stories or work
  items
---

# /cu:story-kickoff

Initiate comprehensive review for work item: **$ARGUMENTS**

---

## Overview

This command orchestrates a comprehensive review and implementation planning session for a user
story, proposal task, or project work item.

---

## Phase 1: Story Discovery & Context Gathering

First, read and analyse the work item to understand:

1. The item ID and location
2. Current status and completeness
3. Parent initiative and strategic context
4. Related ADRs and technical decisions

---

## Phase 2: Multi-Dimensional Review

Based on the work item's domain, conduct a comprehensive review:

### Requirements Analysis

- Validate requirements completeness
- Assess acceptance criteria quality
- Ensure business value clarity
- Check INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable)

### Technical Feasibility

- System design and integration patterns
- Data models and persistence considerations
- Security requirements and compliance
- Performance targets and optimisation strategies

### Delivery Planning

- Resource and skill requirements
- Dependencies and blockers
- Risk identification and mitigation
- Timeline and milestone planning

---

## Phase 3: Review Criteria

### A. Scope Assessment

```
- [ ] Scope is well-defined and bounded
- [ ] No scope creep risks identified
- [ ] Dependencies are explicit and manageable
- [ ] Complexity is appropriate for single work item
```

### B. Requirements Quality

```
- [ ] Clear statement of what is needed
- [ ] Acceptance criteria are SMART
- [ ] Non-functional requirements explicit
- [ ] Edge cases and error scenarios covered
```

### C. Technical Feasibility

```
- [ ] Technical approach is clear and viable
- [ ] Architecture aligns with existing patterns
- [ ] Integration points are identified
- [ ] Technical risks documented with mitigations
```

### D. Definition of Done Alignment

```
- [ ] DoD criteria are complete and verifiable
- [ ] Test coverage targets are realistic
- [ ] Documentation requirements specified
- [ ] Quality gates are achievable
```

---

## Phase 4: Implementation Plan Generation

Create a **detailed phased implementation plan**:

```markdown
## Implementation Plan for [ITEM_ID]

### Phase 1: Setup & Foundation

- Step 1.1: [Specific action with principle tags]
- Step 1.2: [Specific action]
- Deliverables: [List]
- Validation: [How to verify]

### Phase 2: Core Implementation

- Step 2.1: [Specific action]
- Step 2.2: [Specific action]
- Deliverables: [List]
- Validation: [How to verify]

### Phase 3: Testing & Quality

- Step 3.1: [Specific action]
- Step 3.2: [Specific action]
- Deliverables: [List]
- Validation: [How to verify]

### Phase 4: Documentation & Closure

- Step 4.1: [Specific action]
- Step 4.2: [Specific action]
- Deliverables: [List]
- Validation: [How to verify]

### Risk Mitigation Checkpoints

- Checkpoint 1: [After Phase X, verify Y]
- Checkpoint 2: [After Phase X, verify Y]

### Estimated Effort

- Total: [X days / Y hours]
- Phase breakdown: [Distribution]
```

---

## Phase 5: Output Artefacts

Generate the following:

1. **Enhanced Work Item Document** - Updated with review findings
2. **Implementation Checklist** - Actionable task list with dependencies
3. **Risk Register Entry** - If significant risks identified
4. **ADR Draft** - If architectural decisions required

---

## Challenge Log Output

**Purpose**: Produce a structured challenge log artefact that cu-pipe and other orchestrators can
consume as S1_KICKOFF evidence without interpreting free-form text.

### Required Output Block

At the end of every kickoff, include a challenge log in this exact format:

```markdown
## Challenge Log

**Story**: <story-id> | **Profile**: <lightweight|standard|hardened> | **Entries**: <count>

| #   | Aspect               | Challenge                                                 | Disposition              | Status   |
| --- | -------------------- | --------------------------------------------------------- | ------------------------ | -------- |
| 1   | Scope stress-test    | <question or concern about scope boundaries>              | <resolution or decision> | resolved |
| 2   | AC testability       | <question about how an AC can be objectively verified>    | <resolution or decision> | resolved |
| 3   | Risk surfacing       | <risk not listed in the story that could affect delivery> | <resolution or decision> | resolved |
| 4   | Dependency freshness | <question about prerequisite currency>                    | <resolution or decision> | open     |
| 5   | Open question        | <question the agent cannot answer alone>                  | <surfaced to user>       | open     |
```

### Minimum Entries by Profile

| Profile       | Minimum Challenge Log Entries |
| ------------- | ----------------------------- |
| `lightweight` | 2 entries                     |
| `standard`    | 3 entries                     |
| `hardened`    | 5 entries                     |

### Required Coverage Areas

Every challenge log MUST cover at minimum:

1. **Scope stress-test**: Is the story too broad, too narrow, or overlapping with existing work?
2. **AC testability**: Can each AC be objectively verified with a specified output format?
3. **Risk surfacing**: What risks does the story NOT list that could affect delivery?
4. **Dependency freshness**: Are prerequisites still current and unblocked?

If the review profile is `hardened`, also cover:

5. **Open question**: At least one question the agent cannot answer alone, surfaced to the user.

### Consumer Contract

Orchestrators (e.g. cu-pipe) consuming this command's output MUST:

1. Scan for the `## Challenge Log` section heading
2. Extract the challenge log table for evidence recording in pipeline YAML
3. Verify entry count meets the minimum for the declared profile
4. Surface any `open` status entries to the user before advancing
5. Record the challenge log in the S1_KICKOFF evidence

---

## Example Usage

```bash
# Kickoff a proposal task
/cu:story-kickoff Proposal: [Client] Data Platform - Executive Summary section

# Kickoff a project deliverable
/cu:story-kickoff Project: LAAP Reference Database - API endpoint implementation

# Kickoff with file reference
/cu:story-kickoff @docs/requirements/data-platform-requirements.md
```

---

## Organisation Context

When reviewing work items, consider the organisation's context (supplied by its identity-kit):

- **Product fit**: How does this relate to the organisation's product and its core capabilities?
- **Regulated sectors**: Regulatory considerations for clients (the organisation's applicable
  regulators and privacy law) and auditability/proof-of-compliance.
- **Security-first**: Confidentiality, trust, and security-standard alignment before features.
- **Ecosystem**: Leverage the organisation's partner capabilities where relevant.

---
