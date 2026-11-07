# EP - Epic Story Type Guidance

**Story Type**: Epic | **Prefix**: EP-NNN | **Version**: 1.2.1 | **Last Updated**: 2026-11-02

---

## Progress Update Block

Epics should include a **collapsible progress update callout** immediately after the YAML
frontmatter and before the epic heading or overview content.

### Recommended Format

```markdown
> [!note]- Progress updates
>
> - **2026-05-07**: Epic retained in the active backlog and prepared for prioritisation.
> - **2026-05-06**: Scope refined and governance alignment clarified.
> - **2026-05-05**: Epic created and initial child-story structure captured.
```

### Usage Guidance

- Use the collapsible callout syntax: `[!note]-`
- Keep entries strategic and portfolio-oriented rather than implementation-granular
- Add the newest dated update as the first bullet in the progress block
- Record major grouping, governance, prioritisation, or review milestones

---

## Definition

**Epic**: Large body of work that can be broken down into multiple user stories, typically spanning
multiple sprints and delivering strategic business value incrementally.

Epics represent strategic initiatives that are too large to be completed in a single sprint and
require coordination across multiple stories, teams, or systems. They provide portfolio-level
visibility and enable roadmap planning.

---

## When to Use EP Stories

Use the Epic story type when:

- **Strategic initiatives** requiring multiple stories (>5 stories or >2 sprints)
- **Large features** too big for single sprint delivery
- **Cross-team coordination** needed for cohesive delivery
- **Incremental value delivery** over time with multiple releases
- **Portfolio-level planning** and roadmap communication required
- **Business value** must be tracked at strategic level

---

## Required YAML Fields

```yaml
---
story_id: EP-001
story_type: epic
title: 'Implement OAuth2 Authentication System'
epic_owner: 'CTO' # strategic owner/sponsor
child_stories: [US-001, US-002, US-003, BUG-005, TD-007] # array of child story IDs
business_value: high # high|medium|low
strategic_theme: 'Security Hardening' # e.g., "Digital Transformation", "GDPR Compliance"
priority: High
story_points: 34 # sum of child story points
status: In Progress
created: 2025-01-15
last_modified: 2025-02-10
---
```

### Field Descriptions

- **epic_owner**: Strategic sponsor or owner (typically executive/director level)
- **child_stories**: Array of child story IDs (US, BUG, TD, SEC, SP stories)
- **business_value**: Strategic business value rating (high/medium/low)
- **strategic_theme**: Alignment with organisational strategy or initiative name
- **story_points**: Aggregate sum of all child story points

---

## Enhancement 1: Progress Tracking Fields

**Purpose**: Show an epic's completion at a glance, from the statuses of its child stories.

### When to Use

The counters are **optional**. They are kept by hand (nothing writes them for you), so state them
only if you will update them on every close. An epic that states none is not recounted; an epic that
states any is checked on each one it states.

### Field Definitions

`epic-validator.py` (run by the battery over every epic) recounts each stated counter from the
`status:` of the cards listed in `child_stories`:

| Field                 | Type            | Counted from the children                                                     |
| --------------------- | --------------- | ----------------------------------------------------------------------------- |
| `total_stories`       | integer (≥0)    | Entries in `child_stories`                                                    |
| `completed_stories`   | integer         | Status `Done` or `Cancelled`                                                  |
| `in_progress_stories` | integer         | Status `In Progress`                                                          |
| `blocked_stories`     | integer         | Status `Blocked`                                                              |
| `not_started_stories` | integer         | Status `Draft` or `Ready`                                                     |
| `progress_percentage` | integer (0-100) | `completed_stories * 100 / total_stories`, rounded down; `0` with no children |

A wrong counter fails with the epic, the field, the stated and the counted value; update it in the
same commit that changes a child's status (for example the post-merge close of a story).

### YAML Example

```yaml
---
story_id: EP-001
child_stories: [US-001-001, US-001-002, US-001-003, BUG-001-004, TD-001-005]

# Progress tracking (optional; recounted by epic-validator.py)
progress_percentage: 40 # 2 of 5 stories Done or Cancelled
total_stories: 5 # entries in child_stories
completed_stories: 2 # US-001-001, US-001-002 Done
in_progress_stories: 2 # US-001-003, BUG-001-004 In Progress
blocked_stories: 0 # none Blocked
not_started_stories: 1 # TD-001-005 Draft
---
```

### Validation Rules

`epic-validator.py` is the authority; these are the rules it applies:

- `child_stories` lists exactly the cards whose own `epic:` names this epic: a card naming the epic
  but not listed, a listed id with no card, a listed card naming another epic, and an id listed
  twice each fail.
- Every child status is one of the canonical statuses (`tools/status-vocabulary.json`); the
  validator exits 2 if it cannot read that file.
- Each stated counter equals its count from the children (table above).
- The epic's own status agrees with its children: it is not `Draft` once a child is past `Draft` or
  `Ready`; it is not `Done` or `Cancelled` while a child is open; and once every child is `Done` or
  `Cancelled` it is `Done` (or `Cancelled`).

---

## Enhancement 2: Sprint Breakdown Fields

**Purpose**: Visualise story distribution across sprints, identify allocation gaps, and enable
sprint-level progress tracking within epic scope.

### When to Use

Use sprint breakdown fields when you need:

- Clear visibility of which stories are in which sprints
- Sprint-level progress tracking within the epic
- Identification of unallocated stories
- Sprint planning and allocation management

### Field Definitions

| Field                                            | Type            | Manual?       | Description                       |
| ------------------------------------------------ | --------------- | ------------- | --------------------------------- |
| `sprint_distribution.sprint_XXX`                 | array[string]   | ✅ Yes        | Story IDs assigned to this sprint |
| `sprint_distribution.unallocated`                | array[string]   | ✅ Calculated | Stories not in any sprint         |
| `sprint_progress.sprint_XXX.total`               | integer         | ✅ Calculated | Story count in this sprint        |
| `sprint_progress.sprint_XXX.completed`           | integer         | ✅ Calculated | Completed stories in this sprint  |
| `sprint_progress.sprint_XXX.progress_percentage` | integer (0-100) | ✅ Calculated | `(completed / total) × 100`       |

**Sprint Key Format**: Use `sprint_001`, `sprint_002`, etc. (zero-padded numbers) or `unallocated`
for unassigned stories.

### YAML Example

```yaml
---
story_id: EP-001
child_stories: [US-001-001, US-001-002, US-001-003, BUG-001-004, TD-001-005]

# Sprint breakdown (manual assignment)
sprint_distribution:
  sprint_001: [US-001-001, US-001-002] # Sprint 1: 2 stories
  sprint_002: [US-001-003, BUG-001-004] # Sprint 2: 2 stories
  sprint_003: [TD-001-005] # Sprint 3: 1 story
  unallocated: [] # All stories allocated

# Sprint-level progress (calculated)
sprint_progress:
  sprint_001:
    total: 2
    completed: 2
    progress_percentage: 100 # Sprint 1 complete
  sprint_002:
    total: 2
    completed: 0
    progress_percentage: 0 # Sprint 2 in progress
  sprint_003:
    total: 1
    completed: 0
    progress_percentage: 0 # Sprint 3 not started
---
```

### Validation Rules

- All story IDs in `sprint_distribution` must exist in `child_stories` array
- No story ID can appear in multiple sprints (except `unallocated`)
- `unallocated` array must contain stories NOT in any `sprint_XXX`
- All stories in `child_stories` must appear exactly once across all sprint keys
- Sprint keys must follow format: `sprint_NNN` (zero-padded) or `unallocated`

---

## Enhancement 3: Story Dependency Fields

**Purpose**: Map dependency chains, identify blocking relationships, visualise critical path, and
prevent circular dependencies.

### When to Use

Use story dependency fields when you need:

- Explicit dependency tracking between child stories
- Critical path identification (longest dependency chain)
- Blocker detection and visualisation
- Dependency validation (circular dependency prevention)
- Hard vs soft dependency distinction

### Field Definitions

| Field                                       | Type          | Manual?       | Description                                 |
| ------------------------------------------- | ------------- | ------------- | ------------------------------------------- |
| `story_dependencies[].story`                | string        | ✅ Yes        | Story ID being described                    |
| `story_dependencies[].depends_on`           | array[string] | ✅ Yes        | Story IDs that must complete first          |
| `story_dependencies[].blocks`               | array[string] | ✅ Yes        | Story IDs blocked by this story             |
| `story_dependencies[].dependency_type`      | enum          | ✅ Yes        | `hard` (blocking) or `soft` (informational) |
| `dependency_metadata.total_dependencies`    | integer       | ✅ Calculated | Count of hard dependencies                  |
| `dependency_metadata.critical_path`         | array[string] | ✅ Calculated | Longest dependency chain                    |
| `dependency_metadata.independent_stories`   | array[string] | ✅ Calculated | Stories with no hard dependencies           |
| `dependency_metadata.circular_dependencies` | array         | ✅ Calculated | Must be empty (validation error if not)     |

**Dependency Types**:

- **Hard**: Blocking dependency - child story cannot start until prerequisite completes
- **Soft**: Informational dependency - preference for order, but not strictly blocking

### YAML Example

```yaml
---
story_id: EP-001
child_stories: [US-001-001, US-001-002, US-001-003, BUG-001-004, TD-001-005]

# Story dependencies (manual)
story_dependencies:
  - story: US-001-001
    depends_on: []
    blocks: [US-001-002, US-001-003]
    dependency_type: hard

  - story: US-001-002
    depends_on: [US-001-001]
    blocks: [BUG-001-004]
    dependency_type: hard

  - story: US-001-003
    depends_on: [US-001-001]
    blocks: []
    dependency_type: hard

  - story: BUG-001-004
    depends_on: [US-001-002]
    blocks: []
    dependency_type: hard

  - story: TD-001-005
    depends_on: []
    blocks: []
    dependency_type: soft

# Dependency metadata (calculated)
dependency_metadata:
  total_dependencies: 4
  critical_path: [US-001-001, US-001-002, BUG-001-004]
  independent_stories: [TD-001-005]
  circular_dependencies: []
---
```

### Validation Rules

- All story IDs in dependencies must exist in `child_stories` array
- No circular dependencies allowed (if A depends on B, B cannot depend on A)
- If story A blocks story B, then story B must have A in `depends_on`
- Reciprocal relationships must be consistent (`blocks` ⇄ `depends_on`)
- `dependency_type` must be `hard` or `soft`
- Hard dependencies must form a valid DAG (Directed Acyclic Graph)
- `circular_dependencies` must be empty array (validation error if not)

---

## Enhancement 4: Enhanced Workflow Fields

**Purpose**: Add lifecycle management, completion criteria tracking, and workflow state tracking
beyond basic status field.

### When to Use

Use enhanced workflow fields when you need:

- Epic lifecycle state tracking (planning → active → review → completed → archived)
- Target completion date and actual completion tracking
- Success criteria definition and validation
- Active blocker and risk management
- Lifecycle timestamp tracking

### Field Definitions

| Field                                | Type          | Manual?     | Description                                             |
| ------------------------------------ | ------------- | ----------- | ------------------------------------------------------- |
| `target_completion`                  | string        | ✅ Yes      | YYYY-QN or YYYY-MM-DD format                            |
| `actual_completion`                  | string\|null  | ✅ Auto-set | YYYY-MM-DD or null (set when lifecycle_state=completed) |
| `lifecycle_state`                    | enum          | ✅ Yes      | planning\|active\|review\|completed\|archived           |
| `lifecycle_metadata.*`               | string\|null  | ✅ Auto-set | Timestamps for each lifecycle state transition          |
| `success_criteria[].criterion`       | string        | ✅ Yes      | Success criterion description                           |
| `success_criteria[].status`          | enum          | ✅ Yes      | not_started\|in_progress\|completed\|blocked            |
| `success_criteria[].validation_date` | string\|null  | ✅ Yes      | YYYY-MM-DD when criterion validated                     |
| `active_blockers[]`                  | array[object] | ✅ Yes      | Current blockers with severity and mitigation           |
| `active_risks[]`                     | array[object] | ✅ Yes      | Active risks with probability and impact                |

**Lifecycle State Progression**: `planning → active → review → completed → archived`

### YAML Example

```yaml
---
story_id: EP-001
status: In Progress

# Enhanced workflow (manual + auto-set)
target_completion: 2025-Q2
actual_completion: null

lifecycle_state: active
lifecycle_metadata:
  planning_start: 2025-01-15
  active_start: 2025-01-22
  review_start: null
  completed_date: null
  archived_date: null

success_criteria:
  - criterion: 'All 5 stories completed with ≥80% test coverage'
    status: in_progress
    validation_date: null

  - criterion: 'Security audit passed with zero critical findings'
    status: not_started
    validation_date: null

  - criterion: 'Documentation complete and peer-reviewed'
    status: not_started
    validation_date: null

active_blockers: []

active_risks:
  - risk: 'Scope creep due to unclear requirements'
    probability: medium
    impact: high
    mitigation: 'Weekly stakeholder reviews'
    owner: 'Product Owner'
---
```

### Validation Rules

- `lifecycle_state` must follow progression: planning → active → review → completed → archived
- `actual_completion` must be null unless `lifecycle_state` = completed or archived
- `lifecycle_metadata` dates must be chronological (planning_start < active_start < review_start <
  completed_date < archived_date)
- All `success_criteria` must have `status=completed` before `lifecycle_state` can be set to
  completed
- Blockers with `severity=critical` should prevent `lifecycle_state=completed`
- If `lifecycle_state=completed`, then `status` must be "Done"

---

## Epic Template Structure

```markdown
# Epic: [Epic Name]

## Business Value

[Strategic importance and expected outcomes]

- Revenue impact, cost savings, risk mitigation
- Market positioning, competitive advantage
- Customer satisfaction, operational efficiency

## Strategic Theme

[Alignment with organisational strategy]

- Which company objective does this support?
- How does this fit into the product roadmap?
- What strategic risk does this address?

## Child Stories

- [ ] US-001: [Story title and brief description]
- [ ] US-002: [Story title and brief description]
- [ ] BUG-005: [Critical bug discovered during implementation]
- [ ] TD-007: [Technical debt accumulated]
- [ ] SEC-012: [Security requirement within epic scope]

## Success Criteria

[How we measure epic completion and value realisation]

- Measurable business outcomes (KPIs, metrics)
- Technical milestones and deliverables
- User adoption or satisfaction targets
- Compliance or regulatory requirements met

## Timeline

**Expected Completion**: Q2 2025 / June 2025 **Sprint Allocation**: Sprints 15-20 (6 sprints)
**Milestones**:

- Sprint 15: Foundation and architecture
- Sprint 17: Core functionality delivery
- Sprint 19: Integration and testing
- Sprint 20: Production deployment

## Dependencies & Risks

**Blockers**:

- External vendor API access (required by Sprint 16)
- Security audit approval (required before production)

**Risks**:

- Scope creep risk (High) - strict change control needed
- Resource availability (Medium) - backup resources identified
```

---

## Examples

### Example 1: Authentication System Epic (High Business Value)

```markdown
---
story_id: EP-001
story_type: epic
title: 'Implement OAuth2 Authentication System'
epic_owner: 'CTO'
child_stories: [US-015, US-016, US-017, SEC-012, TD-008]
business_value: high
strategic_theme: 'Security Hardening'
priority: High
story_points: 34
status: In Progress
---

# Epic: Implement OAuth2 Authentication System

## Business Value

Replace legacy session-based authentication with industry-standard OAuth2, reducing security risks
and enabling API economy strategy. Expected outcomes:

- 80% reduction in authentication-related security incidents
- Enable third-party integrations (strategic partnership requirement)
- Improve user experience with single sign-on capability
- Meet compliance requirements for the relevant sector regulator

## Strategic Theme

**Security Hardening & API Economy**

- Supports company objective: "Secure by Design 2025"
- Enables product roadmap item: "Partner API Platform"
- Addresses strategic risk: "Authentication vulnerabilities" (Risk Register R-042)

## Child Stories

- [x] US-015: OAuth2 authorization server setup (8 pts) - DONE
- [ ] US-016: Client application integration (5 pts) - IN PROGRESS
- [ ] US-017: User consent and permissions UI (5 pts)
- [ ] SEC-012: Security audit and penetration testing (8 pts)
- [ ] TD-008: Legacy session cleanup and migration (8 pts)

**Total**: 34 story points across 5 stories

## Success Criteria

- All applications migrated to OAuth2 (100% coverage)
- Security audit passed with zero high/critical findings
- API partner onboarding time reduced from 2 weeks to 2 days
- User authentication experience improved (NPS +15 points)
- Sector-regulator compliance validation completed

## Timeline

**Expected Completion**: June 2025 (Q2) **Sprint Allocation**: Sprints 15-20 (6 sprints)
```

### Example 2: Microservices Migration Epic (Long-term Initiative)

```markdown
---
story_id: EP-002
story_type: epic
title: 'Migrate to Microservices Architecture'
epic_owner: 'VP Engineering'
child_stories: [US-101, US-102, SP-015, TD-045, TD-046, SEC-018]
business_value: medium
strategic_theme: 'Technical Modernisation'
priority: Medium
story_points: 89
status: Draft
---

# Epic: Migrate to Microservices Architecture

## Business Value

Decompose monolithic application into independently deployable microservices to improve:

- Development velocity (50% faster feature delivery)
- System resilience (99.99% uptime target)
- Team autonomy (6 independent teams vs 1 large team)
- Technology flexibility (polyglot programming)

## Strategic Theme

**Technical Modernisation & Scalability**

- 3-year modernisation roadmap initiative
- Enables cloud-native deployment strategy
- Supports expected 10× user growth by 2027

## Child Stories

- [ ] SP-015: Microservices architecture design spike (16h time-box)
- [ ] US-101: Extract user service from monolith (13 pts)
- [ ] US-102: Extract payment service from monolith (13 pts)
- [ ] TD-045: Refactor shared data access layer (21 pts)
- [ ] TD-046: Implement API gateway and service mesh (13 pts)
- [ ] SEC-018: Inter-service authentication and authorisation (13 pts)
- [ ] (More stories to be added after spike completion)

**Total**: 89 story points (initial estimate)

## Success Criteria

- 2 services successfully extracted and running independently
- No increase in p95 latency for critical user journeys
- Deployment frequency improved to daily (from weekly)
- Team satisfaction scores improved (>4.5/5)
- Architecture Decision Records created for all key decisions

## Timeline

**Expected Completion**: Q4 2025 **Sprint Allocation**: Sprints 20-35 (16 sprints across 6 months)
**Milestones**:

- Q2: Architecture spike + first service extraction
- Q3: Second service + shared infrastructure
- Q4: Production deployment + observability
```

### Example 3: GDPR Compliance Epic (Swiss Banking Context)

```markdown
---
story_id: EP-003
story_type: epic
title: 'GDPR Compliance Implementation'
epic_owner: 'Chief Compliance Officer'
child_stories: [SEC-020, SEC-021, SEC-022, US-120, TD-050]
business_value: high
strategic_theme: 'Regulatory Compliance'
priority: High
story_points: 55
status: In Progress
---

# Epic: GDPR Compliance Implementation

## Business Value

Achieve full GDPR compliance for Swiss banking operations:

- Avoid regulatory fines (up to 4% of global revenue)
- Build customer trust through transparency
- Competitive advantage in a privacy-conscious market
- Enable EU market expansion

## Strategic Theme

**Regulatory Compliance & Data Privacy**

- Mandatory for the applicable regulatory or contractual environment
- Supports "Privacy First" brand positioning
- Addresses Risk R-015: "GDPR non-compliance exposure"

## Child Stories

- [x] SEC-020: Right to access - data export functionality (13 pts) - DONE
- [ ] SEC-021: Right to erasure - data deletion workflow (13 pts) - IN PROGRESS
- [ ] SEC-022: Consent management system (13 pts)
- [ ] US-120: Privacy dashboard for customers (8 pts)
- [ ] TD-050: Data retention policy automation (8 pts)

**Total**: 55 story points across 5 stories

## Success Criteria

- Legal audit passed (external counsel verification)
- Sector-regulator compliance validation completed
- All customer data processing documented
- Consent mechanisms in place for all data collection
- Data breach response procedures tested
- Privacy Impact Assessment (PIA) completed

## Timeline

**Expected Completion**: March 2025 (Q1) **Sprint Allocation**: Sprints 10-15 (6 sprints)
**Regulatory Deadline**: April 2025 (sector-regulator audit)
```

---

## Anti-Patterns (Avoid These)

### ❌ Anti-Pattern 1: Creating Epics for Small Features

**Wrong**:

```yaml
story_id: EP-010
title: 'Add search filter to user list'
child_stories: [US-050]
business_value: low
story_points: 3
```

**Why it's wrong**: This is a single user story, not an epic. Epics should span >5 stories or >2
sprints.

**Correct approach**: Make this US-050 directly, not an epic.

---

### ❌ Anti-Pattern 2: Epics Without Clear Business Value

**Wrong**:

```markdown
# Epic: Refactor Codebase

## Business Value

Make code better and cleaner.
```

**Why it's wrong**: Vague business value, no measurable outcomes, no stakeholder justification.

**Correct approach**:

```markdown
# Epic: Modernise Payment Processing Architecture

## Business Value

- Reduce payment failure rate from 5% to <1% (saving $500K annually)
- Enable new payment methods (strategic partnership requirement)
- Improve PCI-DSS compliance posture (reduce audit risk)
```

---

### ❌ Anti-Pattern 3: Epics Spanning More Than 2 Quarters

**Wrong**:

```yaml
story_id: EP-020
title: 'Complete Digital Transformation'
timeline: 18 months
story_points: 500
```

**Why it's wrong**: Too large, too long, impossible to track meaningfully. Scope will change
dramatically.

**Correct approach**: Break into multiple quarterly epics with clear milestones.

---

### ❌ Anti-Pattern 4: Epics Without Child Story Breakdown

**Wrong**:

```yaml
story_id: EP-030
title: 'Implement AI Recommendation Engine'
child_stories: []
```

**Why it's wrong**: Defeats the purpose of epics - no decomposition, no tracking, no incremental
delivery.

**Correct approach**: Always break epics into child stories before starting implementation.

---

## Related Story Types

### Epic Relationships

**EP contains**:

- **US (User Stories)**: Primary child stories for feature delivery
- **BUG (Defects)**: Bugs discovered during epic implementation
- **TD (Technical Debt)**: Debt accumulated or addressed during epic
- **SEC (Security)**: Security requirements within epic scope
- **SP (Spikes)**: Research needed for epic planning and risk reduction

**EP linked from**:

- **SP (Spikes)**: Spike outcomes often spawn epics
- **RA (Risk Actions)**: Risk mitigation may require epic-level work

---

## Story Type Transitions

### From EP to Other Types

**EP breakdown → US** (Most common):

```
EP-001: "OAuth2 Authentication"
  → US-015: "OAuth2 server setup"
  → US-016: "Client integration"
  → US-017: "User consent UI"
```

**EP discovery → SEC** (Security requirements):

```
EP-002: "Payment Processing"
  → SEC-025: "PCI-DSS compliance gaps identified"
```

**EP technical issues → TD** (Debt accumulation):

```
EP-003: "Microservices Migration"
  → TD-060: "Legacy data access layer refactoring needed"
```

**EP uncertainty → SP** (Research needed):

```
EP-004: "Real-time Analytics Platform"
  → SP-020: "Evaluate stream processing frameworks"
```

---

## Priority & Sizing Guidelines

### Business Value Rating

- **High**: Revenue impact >$500K, strategic imperative, regulatory requirement
- **Medium**: Competitive parity, operational efficiency, technical enabler
- **Low**: Nice-to-have, long-term investment, experimentation

### Story Point Sizing

- **Small Epic**: 20-50 points (3-5 stories, 2-3 sprints)
- **Medium Epic**: 50-100 points (5-10 stories, 4-6 sprints)
- **Large Epic**: 100-200 points (10-20 stories, 6-12 sprints)
- **Too Large**: >200 points (break down into multiple epics)

### Time Horizon

- **Short**: 1-2 quarters (tactical improvements)
- **Medium**: 2-4 quarters (strategic initiatives)
- **Long**: >4 quarters (too long - break down)

---

## Project Considerations

### Quality Expectations

- Comprehensive planning and documentation expected
- Long-term thinking valued over quick wins
- Stakeholder alignment critical before starting
- WCAG 2.1 AA accessibility compliance for all UI work

### Language and Localisation

- Epic titles and descriptions should follow project language conventions
- User-facing deliverables should use the agreed business language(s)
- Technical documentation should remain consistent across the project

### Regulatory Context

- Apply sector, client, and internal governance requirements where relevant
- Document privacy, security, audit, and procurement constraints explicitly
- Link to the governing policies, ADRs, or compliance register when applicable

### Example Strategic Themes

- "Ergonomic Excellence" (user experience improvement)
- "Accessibility Compliance" (WCAG 2.1 AA)
- "Modern Architecture" (modern client, API, or integration patterns)
- "Data Security" (protection of sensitive business data)
- "Operational Efficiency" (reduced clicks, faster workflows)

---

## Checklist for Epic Creation

Before creating an EP story, verify:

- [ ] Work requires >5 stories or >2 sprints
- [ ] Clear strategic business value articulated
- [ ] Epic owner identified (executive/director sponsor)
- [ ] Strategic theme alignment documented
- [ ] Initial child story breakdown created (even if high-level)
- [ ] Success criteria defined and measurable
- [ ] Timeline realistic (not >2 quarters)
- [ ] Dependencies and risks identified
- [ ] Stakeholder buy-in obtained

---

## References

### Internal Documentation

- **User Story Template**: `${CLAUDE_PLUGIN_ROOT}/skills/backlog-management/resources/user-story-template.md`
  (owning skill) owner: `cu:backlog-management` skill resource)
- **Memory Bank**: `docs-copper/memory-bank/` for project context
- **Product Context**: `docs-copper/memory-bank/productContext.md` for personas

### Related Story Types

- **US**: [US-user-story-guidance.md](US-user-story-guidance.md) - Child stories for feature
  delivery
- **SP**: [SP-spike-guidance.md](SP-spike-guidance.md) - Research for epic planning
- **SEC**: [SEC-security-guidance.md](SEC-security-guidance.md) - Security within epics
- **TD**: [TD-technical-debt-guidance.md](TD-technical-debt-guidance.md) - Debt from epics

### External Resources

- Scaled Agile Framework (SAFe) - Epic guidance
- "User Story Mapping" by Jeff Patton
- Atlassian Jira - Epic best practices

---

_EP-epic-guidance.md | Version 1.2.0 | Last Updated: 2026-05-07 | COPPER Project Documentation_
