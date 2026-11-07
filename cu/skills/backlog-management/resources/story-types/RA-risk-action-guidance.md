# RA - Risk Action Story Type Guidance

**Story Type**: Risk Action | **Prefix**: RA-NNN | **Version**: 1.1.0 | **Last Updated**: 2025-01-23

---

## Definition

**Risk Action**: Actions addressing risks, incidents, issues, or decisions from the RAID (Risks,
Actions, Issues, Decisions) registry. Represents risk mitigation, incident response, or decision
implementation work driven by project risk management.

---

## Purpose

Address actions from RAID registry:

- **Risk mitigation** (reduce probability or impact)
- **Issue resolution** (resolve blocking issues)
- **Decision implementation** (execute agreed decisions)
- **Incident response** (address project incidents)

---

## When to Use RA Stories

- **Risk mitigation actions** from risk register
- **Issue resolution** for project blockers
- **Decision implementation** following governance decisions
- **Incident response** actions from post-mortems
- **Contingency planning** for identified risks

---

## Required YAML Fields

```yaml
---
story_id: RA-004
story_type: risk_action
title: 'Implement database backup strategy (Risk R-012 mitigation)'
raid_id: R-012 # R-NNN|A-NNN|I-NNN|D-NNN
risk_score: 20 # 1-25 (from 5×5 matrix: Probability × Impact)
action_type: mitigation # mitigation|response|contingency
priority: High
story_points: 8
status: Draft
created: 2025-01-20
last_modified: 2025-01-25
---
```

### Field Descriptions

- **raid_id**: Link to RAID registry entry (R/A/I/D prefix + number)
- **risk_score**: Score from 5×5 risk matrix (1-25: Probability 1-5 × Impact 1-5)
- **action_type**: Type of risk action (mitigation/response/contingency)

---

## Risk Scoring (5×5 Matrix)

### Probability (1-5)

- **1 - Very Low**: <10% probability
- **2 - Low**: 10-30% probability
- **3 - Medium**: 30-50% probability
- **4 - High**: 50-70% probability
- **5 - Very High**: >70% probability

### Impact (1-5)

- **1 - Negligible**: <1 day delay, <$5K cost
- **2 - Minor**: 1-5 days delay, $5K-$25K cost
- **3 - Moderate**: 1-2 weeks delay, $25K-$100K cost
- **4 - Major**: 2-4 weeks delay, $100K-$500K cost
- **5 - Severe**: >4 weeks delay, >$500K cost or project failure

### Risk Score = Probability × Impact (1-25)

**Priority Thresholds**:

- **Critical (20-25)**: Immediate action required
- **High (12-19)**: Urgent mitigation needed
- **Medium (6-11)**: Planned mitigation
- **Low (1-5)**: Monitor and review

---

## Action Types

### Mitigation

**Goal**: Reduce probability or impact BEFORE risk occurs

- Implement preventive controls
- Add redundancy or backup systems
- Improve processes to reduce likelihood

### Response

**Goal**: Address ACTIVE issues or incidents

- Resolve blocking issues immediately
- Incident response and recovery
- Damage control and workarounds

### Contingency

**Goal**: Prepare for risk if it DOES occur

- Create fallback plans
- Identify alternative approaches
- Reserve budget/time buffers

---

## Examples

### Example 1: Risk Mitigation (Database Failure Risk)

```markdown
---
story_id: RA-004
story_type: risk_action
title: 'Implement automated database backup strategy'
raid_id: R-012
risk_score: 20 # Probability: 4 (High), Impact: 5 (Severe) = 20
action_type: mitigation
priority: High
story_points: 8
status: Done
---

# Risk Action: Database Backup Implementation

## RAID Entry: R-012 - Database Failure Risk

**Risk Description**:

- Current database has no automated backup
- Manual backups inconsistent (last backup: 2 weeks ago)
- Database failure would result in data loss
- Recovery time unknown (no tested recovery procedure)

**Probability**: 4 (High) - Hardware failure, human error, corruption likely **Impact**: 5
(Severe) - Complete data loss, project failure, regulatory violation **Risk Score**: 20 (CRITICAL)

## Mitigation Strategy

**Objective**: Reduce Impact from 5 (Severe) to 2 (Minor)

- Target Risk Score: 8 (4×2) - 60% risk reduction

**Implementation**:

1. **Automated Backups**:

   - Daily full backups (retained 30 days)
   - Hourly incremental backups (retained 7 days)
   - Backups stored in separate region (disaster recovery)

2. **Backup Monitoring**:

   - Automated backup success/failure alerts
   - Weekly backup integrity verification
   - Monthly recovery testing

3. **Recovery Procedures**:
   - Documented recovery runbook
   - Tested recovery time: <2 hours
   - Automated recovery scripts

## Implementation

- [x] Set up PostgreSQL pg_basebackup automation
- [x] Configure AWS S3 cross-region replication
- [x] Implement backup monitoring and alerting
- [x] Create and test recovery runbook
- [x] Train team on recovery procedures

## Risk Reduction Achieved

**Before**:

- Probability: 4 (High)
- Impact: 5 (Severe)
- Risk Score: 20 (CRITICAL)

**After**:

- Probability: 4 (High) - hardware failure still possible
- Impact: 2 (Minor) - max 1 hour data loss, 2 hour recovery
- Risk Score: 8 (MEDIUM) - 60% risk reduction

**Residual Risk**: Acceptable - database failure no longer project-critical

## Project Context

- Regulated or critical services may require demonstrable data protection and recovery capability
- Recovery objectives should align with business continuity expectations
- Sensitive data protection should be validated through backup and restoration testing
- Risk treatment should align with the project's governance and compliance requirements
```

### Example 2: Issue Resolution (Vendor API Instability)

```markdown
---
story_id: RA-008
story_type: risk_action
title: 'Resolve vendor API instability (Issue I-003)'
raid_id: I-003
risk_score: 16 # Active issue: Probability 4, Impact 4
action_type: response
priority: High
story_points: 13
status: Done
---

# Risk Action: Vendor API Stability Resolution

## RAID Entry: I-003 - Payment Gateway API Instability

**Issue Description**:

- Payment gateway API has 15% failure rate (last 7 days)
- Intermittent timeouts and 503 errors
- Affecting 200+ customer transactions daily
- Vendor SLA: 99.9% uptime (currently 85%)

**Impact**: 4 (Major) - Revenue loss, customer dissatisfaction **Urgency**: ACTIVE ISSUE - requires
immediate response

## Response Strategy

**Immediate Actions** (Day 1-3):

1. Implement retry logic with exponential backoff
2. Add circuit breaker to prevent cascading failures
3. Queue failed transactions for retry
4. Notify affected customers with status updates

**Short-term** (Week 1-2):

1. Escalate to vendor support (SLA breach)
2. Implement fallback payment processor
3. Add comprehensive monitoring and alerting
4. Daily status updates to stakeholders

**Long-term** (Month 1-3):

1. Evaluate alternative payment gateways
2. Implement multi-gateway support (SP-025 spike)
3. Renegotiate SLA with vendor or switch

## Implementation

**Immediate** (Day 1):

- [x] Circuit breaker implemented (Hystrix)
- [x] Retry logic with exponential backoff (3 attempts)
- [x] Transaction queue for failed payments
- [x] Customer notification system active

**Short-term** (Week 1):

- [x] Vendor escalation (ticket #78452 - P1 priority)
- [x] Monitoring dashboard for payment health
- [x] Daily stakeholder updates established

**Long-term** (Ongoing):

- [ ] SP-025: Evaluate alternative payment gateways (16h spike)
- [ ] US-180: Implement secondary payment processor (13 pts)

## Results

**Immediate Impact** (After Day 1):

- Failure rate: 15% → 3% (with retries)
- Customer impact: 200 failures/day → 20 failures/day (-90%)
- Transaction recovery rate: 80% via retry queue

**Vendor Response** (Week 1):

- Root cause identified: database connection pool exhaustion
- Vendor deployed fix (Week 2)
- SLA credits applied: CHF 5,000

**Final Resolution** (Week 3):

- Failure rate: <0.5% (within SLA)
- All mitigation code remains (defence-in-depth)
- Secondary gateway evaluation in backlog (risk mitigation)
```

### Example 3: Decision Implementation (Security Policy)

```markdown
---
story_id: RA-015
story_type: risk_action
title: 'Enforce new security policy for API authentication'
raid_id: D-005
risk_score: 12 # Decision implementation: Medium priority
action_type: mitigation
priority: Medium
story_points: 8
status: Draft
---

# Risk Action: Security Policy Enforcement

## RAID Entry: D-005 - API Authentication Policy Decision

**Decision Context**:

- Architecture Review Board decision (2025-01-20)
- Current API authentication inconsistent (3 different methods)
- Security audit finding: weak authentication in legacy APIs
- Decision: Standardise on OAuth2 + API keys

**Decision Details**:

- **What**: All APIs must use OAuth2 for user context, API keys for service-to-service
- **Why**: Consistent security posture, audit compliance, modern standard
- **When**: Complete migration by 2025-03-31
- **Who**: All development teams

## Implementation Plan

**Phase 1** (Sprint 1-2):

- Audit all existing APIs (identify authentication methods)
- Create migration guide and reference implementation
- Set up OAuth2 authorization server

**Phase 2** (Sprint 3-5):

- Migrate high-priority APIs (customer-facing)
- Deprecate legacy authentication methods
- Add automated security testing

**Phase 3** (Sprint 6):

- Migrate remaining APIs
- Remove legacy authentication code
- Security validation and sign-off

## Implementation

- [ ] API authentication audit completed (inventory: 42 APIs)
- [ ] OAuth2 migration guide published
- [ ] Reference implementation available
- [ ] Training session for all developers
- [ ] 15 APIs migrated (36% complete)
- [ ] Security automated tests in CI/CD
- [ ] Target: 100% by 2025-03-31

## Benefits

**Security**:

- Consistent authentication across all APIs
- Audit trail for all API access
- Token-based (not password) authentication
- Security audit finding resolved

**Developer Experience**:

- Single authentication method to learn
- Better tooling and documentation
- Standard OAuth2 libraries

**Compliance**:

- Sector-regulator security policy compliance
- Audit readiness (single authentication method)
```

---

## Anti-Patterns

### ❌ RA Stories Without RAID Link

**Wrong**: Creating risk actions without RAID registry entry **Right**: All RA stories must link to
R/A/I/D entry

### ❌ Ignoring High-Risk Scores

**Wrong**: Risk score 20 (CRITICAL) but low priority **Right**: Risk score determines priority
(20-25 = immediate action)

### ❌ No Risk Reduction Measurement

**Wrong**: "Implemented mitigation" (no before/after) **Right**: Document risk score before and
after, demonstrate reduction

---

## Related Story Types

**RA can spawn**:

- **US (User Stories)**: Risk mitigation may require features
- **TD (Technical Debt)**: Risk response may reveal technical debt
- **SEC (Security)**: Security risks spawn SEC stories

**RA spawned from**:

- **BUG (Defects)**: Critical bugs trigger risk actions
- **US (User Stories)**: Features may identify new risks
- **EP (Epics)**: Large initiatives create project risks

---

## RAID Registry Integration

### Risk (R-NNN)

Potential future events that could negatively impact project. → **Mitigation** RA stories reduce
probability or impact

### Action (A-NNN)

Planned activities not tied to specific deliverables. → **Implementation** RA stories execute
actions

### Issue (I-NNN)

Current problems blocking progress. → **Response** RA stories resolve issues

### Decision (D-NNN)

Key project decisions requiring implementation. → **Execution** RA stories implement decisions

---

## Project Considerations

### Risk Management Culture

- **Quality focus**: Proactive mitigation is preferable to reactive response
- **Documentation**: Risk decisions should be traceable for governance and auditability
- **Regulatory compliance**: Risk management should be demonstrable where regulation applies

### Common Risk Categories

- **Legacy Integration Risk**: API layer failures, synchronisation issues, brittle dependencies
- **Technology Risk**: Framework compatibility, upgrade path, tooling constraints
- **Resource Risk**: Key person dependency, onboarding, skill availability
- **Schedule Risk**: Timeline compression, release dependencies, external approvals
- **User Adoption Risk**: Change resistance, training effectiveness, rollout readiness

### Common Risks to Monitor

- **R-001**: Legacy backend API instability during migration
- **R-002**: IAM authentication integration complexity
- **R-003**: Data migration accuracy for sensitive or business-critical records
- **R-004**: User acceptance of a new interface or workflow
- **R-005**: Performance degradation for complex search or reporting queries

### Risk Mitigation Strategies

- **Anti-Corruption Layer**: Isolate new frontend from legacy backend changes
- **Phased Rollout**: Gradual deployment to reduce user adoption risk
- **Parallel Running**: Legacy and new systems operate simultaneously during transition
- **User Involvement**: Early user testing and structured feedback incorporation
- **Comprehensive Testing**: Integration tests for API layer, UAT with real users

---

## References

- **Story Type System**: See [story-types/README.md](README.md) for the complete type reference
- **RAID Registry Template**: Use with RA stories for structured risk tracking
- **Related Types**: [US](US-user-story-guidance.md), [BUG](BUG-defect-guidance.md),
  [SEC](SEC-security-guidance.md)
- **Memory Bank**: `docs-copper/memory-bank/` for project context

---

_RA-risk-action-guidance.md | Version 1.1.0 | Last Updated: 2025-01-23 | COPPER Project
Documentation_
