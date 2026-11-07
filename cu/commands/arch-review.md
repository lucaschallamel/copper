---
description: Comprehensive architectural currency and consistency review across ADRs
  and documentation
---

# /cu:arch-review

Initiate comprehensive architectural review for: **$ARGUMENTS**

---

## Overview

This command orchestrates a thorough architectural currency and consistency review analysing all
ADRs, data models, and architectural documentation for consistency, currency, completeness, and
alignment.

**Scope**: Architecture documentation including ADRs, data models, and system patterns.

---

## Phase 1: Architecture Discovery

First, map the architectural landscape:

1. **List all ADRs** with status (Accepted, Draft, Proposed, Deprecated)
2. **Identify cross-references** between ADRs
3. **Map entity relationships** from naming conventions
4. **Catalogue decision domains**: Data, Security, AI, Integration, Cloud

Read key files to establish baseline:

- `/architecture/ADR/README.md`
- `/memory-bank/systemPatterns.md`
- All ADR files in `/architecture/ADR/*.md`

---

## Phase 2: Multi-Dimensional Review

### System Architecture Consistency

- Cross-platform alignment (if applicable)
- Architectural pattern consistency (layers, boundaries, interfaces)
- Integration point coherence (APIs, messaging, data flows)
- Technology stack alignment across ADRs
- Microservices vs monolith boundary clarity

### Design Quality & Decision Coherence

- ADR format compliance and completeness
- Decision rationale clarity and validity
- Option analysis quality (≥2 options considered)
- Consequence documentation completeness
- Principle code tagging consistency
- Status lifecycle adherence (Proposed→Accepted→Deprecated)

### Data Architecture

- Naming convention adherence
- Entity relationship consistency
- Privacy classification completeness
- Schema versioning strategy validation
- Bounded context boundary clarity

### Security Architecture Alignment

- Threat model coverage
- Encryption at rest/transit consistency
- Authentication/authorisation architecture
- Privacy boundary enforcement (Swiss DPA, GDPR)
- Zero-trust principle adherence

---

## Phase 3: Review Criteria Checklist

### A. Currency Assessment

```
- [ ] All ADRs reviewed within last 6 months
- [ ] No "Proposed" status >3 months old
- [ ] Technology versions current (not deprecated)
- [ ] External references still valid (URLs, docs)
- [ ] No superseded ADRs without replacement
```

### B. Consistency Assessment

```
- [ ] No conflicting decisions across ADRs
- [ ] Consistent technology choices
- [ ] Aligned naming conventions throughout
- [ ] Coherent layer boundaries
- [ ] Unified error handling strategy
```

### C. Completeness Assessment

```
- [ ] All bounded contexts have ADR coverage
- [ ] Entity relationships fully documented
- [ ] Integration points have interface definitions
- [ ] Security considerations in all relevant ADRs
```

### D. Alignment Assessment

```
- [ ] ADRs align with memory-bank/systemPatterns.md
- [ ] Security ADRs align with compliance requirements
- [ ] Technology ADRs align with the organisation's strategic technology partnerships
```

---

## Phase 4: Findings Classification

| Level       | Description                          | Action Required          |
| ----------- | ------------------------------------ | ------------------------ |
| 🔴 Critical | Conflicting decisions, security gaps | Immediate resolution ADR |
| 🟠 High     | Outdated decisions, missing coverage | Update in current sprint |
| 🟡 Medium   | Inconsistencies, incomplete docs     | Plan for near-term fix   |
| 🟢 Low      | Minor gaps, style inconsistencies    | Nice-to-have             |
| ℹ️ Info     | Observation, future consideration    | For awareness            |

---

## Output Format

```markdown
# Architectural Currency & Consistency Review Report

## Executive Summary

- **Review Scope**: [Target description]
- **Review Date**: [Date]
- **Overall Health**: [Critical/Warning/Healthy]

## Architecture Inventory

| Category      | Count | Status Distribution |
| ------------- | ----- | ------------------- |
| Core ADRs     | X     | Y Accepted, Z Draft |
| Security ADRs | X     | Y Accepted, Z Draft |
| Data ADRs     | X     | Y Accepted, Z Draft |

## Critical Conflicts (🔴)

[List with ADR references and resolution recommendations]

## Currency Issues (🟠)

[List with staleness indicators and update recommendations]

## Consistency Gaps (🟡)

[List with alignment recommendations]

## Recommended Actions

| Priority | Action   | Owner  | Target Date |
| -------- | -------- | ------ | ----------- |
| 🔴       | [Action] | [Role] | [Date]      |
```

---

## Structured Output

**Purpose**: Provide machine-parseable output that cu-pipe and other orchestrators can consume to
determine pass/fail status without interpreting free-form text.

### Required Output Block

At the end of every review, include a structured block in this exact format:

```markdown
## Structured Findings

**Overall Status**: PASS | FAIL **Total Findings**: <count> (Critical: <n>, High: <n>, Medium: <n>,
Low: <n>, Info: <n>)

| #   | Severity  | Category    | Issue                    | Recommendation         |
| --- | --------- | ----------- | ------------------------ | ---------------------- |
| 1   | 🟠 High   | Consistency | Description of the issue | Recommended fix action |
| 2   | 🟡 Medium | Currency    | Description of the issue | Recommended fix action |

### Risk Register

| Risk ID | Description | Probability  | Impact       | Mitigation        |
| ------- | ----------- | ------------ | ------------ | ----------------- |
| R1      | Description | Low/Med/High | Low/Med/High | Mitigation action |

### Exit Guidance

- **On PASS**: No critical or high findings. Review is complete.
- **On FAIL**: One or more critical or high findings exist. These must be resolved before the
  consuming pipeline stage can advance. If the consuming pipeline stage is S5_ARCH_SEC_COMP_REVIEW
  via `/cu:pipe`, cu-pipe will record the FAIL status and require resolution before allowing stage
  advancement.
```

### Pass/Fail Rules

- **PASS**: Zero critical and zero high severity findings
- **FAIL**: One or more critical or high severity findings

### Consumer Contract

Orchestrators (e.g. cu-pipe) consuming this command's output MUST:

1. Scan for the `**Overall Status**:` line to determine pass/fail
2. Extract the findings table for evidence recording
3. Extract the risk register for S5 formal review protocol (AC16)
4. On FAIL: present findings to the user and block stage advancement
5. On PASS: record findings and risk register as evidence and allow stage advancement

---

## Example Usage

```bash
# Full architecture review
/cu:arch-review all

# Review specific domain
/cu:arch-review --domain=security

# Currency check only
/cu:arch-review --mode=currency
```

---
