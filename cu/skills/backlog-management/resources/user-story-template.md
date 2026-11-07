---
story_id: US-NNN # EP-NNN, US-NNN, BUG-NNN, TD-NNN, SEC-NNN, SP-NNN, CI-NNN, RA-NNN
story_type: user_story # epic, user_story, bug, technical_debt, security, spike, continuous_improvement, risk_action
title: '[Brief descriptive title]'
epic: '[Related epic or initiative]' # optional - for linking US/BUG/TD/SEC/SP to parent EP
priority: Medium
story_points:
status: Draft
assignee: '' # Team member assigned to this story (visible on Kanban board)
author: '' # Story author (the authoring identity, e.g. QUAD)
created: YYYY-MM-DD
last_modified: YYYY-MM-DD
# Type-Specific Fields (uncomment and populate based on story_type)
## For EP (Epic) - uncomment if story_type = epic
# ⚠️ IMPORTANT: When uncommenting fields below, REMOVE all inline comments after values
# Obsidian's YAML parser does not support inline comments in frontmatter
# Move documentation to markdown body using callout blocks (see EP-000-001 example)
# ============================================================================
# EXISTING EP FIELDS (epic enhancement fields)
# ============================================================================
# epic_owner: ""  # strategic owner/sponsor (manual)
# child_stories: []  # [US-001, US-002, BUG-001, TD-005] (manual)
# business_value: medium  # high|medium|low (manual)
# strategic_theme: ""  # e.g., "Digital Transformation", "Security Hardening" (manual)
#
# ============================================================================
# ENHANCEMENT 1: Progress Tracking
# ============================================================================
# progress_percentage: 0  # 0-100, calculated: (completed_stories / total_stories) × 100
# total_stories: 0  # count of child_stories array (calculated)
# completed_stories: 0  # count with status=completed (calculated)
# in_progress_stories: 0  # count with status=in-progress (calculated)
# blocked_stories: 0  # count with status=blocked (calculated)
# not_started_stories: 0  # count with status=not-started (calculated)
#
# ============================================================================
# ENHANCEMENT 2: Sprint Breakdown
# ============================================================================
# sprint_distribution:  # sprint allocation mapping (manual)
#   sprint_001: [US-001-001, US-001-002]  # stories in sprint 1
#   sprint_002: [US-001-003, BUG-001-004]  # stories in sprint 2
#   sprint_003: [TD-001-005]  # stories in sprint 3
#   unallocated: []  # stories not yet assigned (calculated)
#
# sprint_progress:  # sprint-level progress tracking (calculated)
#   sprint_001:
#     total: 2  # count of stories in this sprint
#     completed: 2  # completed stories in this sprint
#     progress_percentage: 100  # sprint completion percentage
#   sprint_002:
#     total: 2
#     completed: 0
#     progress_percentage: 0
#   sprint_003:
#     total: 1
#     completed: 0
#     progress_percentage: 0
#
# ============================================================================
# ENHANCEMENT 3: Story Dependencies
# ============================================================================
# story_dependencies:  # peer dependency mapping (manual)
#   - story: US-001-001
#     depends_on: []  # prerequisite story IDs
#     blocks: [US-001-002, US-001-003]  # downstream story IDs
#     dependency_type: hard  # hard|soft (hard = blocking, soft = informational)
#
#   - story: US-001-002
#     depends_on: [US-001-001]
#     blocks: [BUG-001-004]
#     dependency_type: hard
#
#   - story: US-001-003
#     depends_on: [US-001-001]
#     blocks: []
#     dependency_type: hard
#
#   - story: BUG-001-004
#     depends_on: [US-001-002]
#     blocks: []
#     dependency_type: hard
#
#   - story: TD-001-005
#     depends_on: []
#     blocks: []
#     dependency_type: soft
#
# dependency_metadata:  # dependency analysis (calculated)
#   total_dependencies: 4  # count of hard dependencies
#   critical_path: [US-001-001, US-001-002, BUG-001-004]  # longest dependency chain
#   independent_stories: [TD-001-005]  # stories with no hard dependencies
#   circular_dependencies: []  # circular dependency chains (must be empty)
#
# ============================================================================
# ENHANCEMENT 4: Enhanced Workflow
# ============================================================================
# target_completion: 2025-Q2  # YYYY-QN or YYYY-MM-DD (manual)
# actual_completion: null  # YYYY-MM-DD or null (set when lifecycle_state=completed)
#
# lifecycle_state: planning  # planning|active|review|completed|archived (manual)
# lifecycle_metadata:  # lifecycle timestamps (auto-set on state transition)
#   planning_start: 2025-01-15  # YYYY-MM-DD
#   active_start: null  # YYYY-MM-DD or null
#   review_start: null  # YYYY-MM-DD or null
#   completed_date: null  # YYYY-MM-DD or null
#   archived_date: null  # YYYY-MM-DD or null
#
# success_criteria:  # epic completion criteria (manual)
#   - criterion: "All 5 stories completed with ≥80% test coverage"
#     status: in_progress  # not_started|in_progress|completed|blocked
#     validation_date: null  # YYYY-MM-DD or null
#
#   - criterion: "Security audit passed with zero critical findings"
#     status: not_started
#     validation_date: null
#
#   - criterion: "Documentation complete and peer-reviewed"
#     status: not_started
#     validation_date: null
#
# active_blockers: []  # current blockers (manual)
#   # Example:
#   # - blocker: "Waiting on security team approval"
#   #   severity: high  # low|medium|high|critical
#   #   blocking_since: 2025-01-20  # YYYY-MM-DD
#   #   blocked_stories: [US-001-003]
#   #   mitigation_plan: "Escalated to CTO"
#
# active_risks: []  # risk tracking (manual)
#   # Example:
#   # - risk: "Scope creep due to unclear requirements"
#   #   probability: medium  # low|medium|high
#   #   impact: high  # low|medium|high
#   #   mitigation: "Weekly stakeholder reviews"
#   #   owner: "Product Owner"

## For BUG (Defect) - uncomment if story_type = bug
# severity: medium  # critical|high|medium|low
# affected_version: ""  # version where bug was found
# reproduction_steps: ""  # how to reproduce the bug
# root_cause: ""  # technical root cause analysis
# environment: test  # production|staging|test|dev

## For SEC (Security) - uncomment if story_type = security
# vulnerability_type: ""  # e.g., "SQL Injection", "XSS", "Insecure Deserialisation"
# cvss_score: 0.0  # 0.0-10.0 CVSS score
# compliance_framework: OWASP  # GDPR|ISO27001|OWASP|SOX|HIPAA
# remediation_deadline: YYYY-MM-DD  # compliance or SLA deadline
# cve_id: ""  # CVE-YYYY-NNNNN (if applicable)

## For SP (Spike) - uncomment if story_type = spike
# research_question: ""  # what we need to learn
# time_box: ""  # e.g., "16 hours", "2 days"
# expected_outcome: ""  # what decision/knowledge we expect
# decision_deadline: YYYY-MM-DD  # when decision is needed
# spike_outcome: ""  # actual findings and recommendations (added post-completion)

## For TD (Technical Debt) - uncomment if story_type = technical_debt
# debt_category: code_quality  # code_quality|architecture|testing|documentation|security
# debt_impact: maintainability  # productivity|maintainability|scalability|security
# debt_age_days: 0  # calculated automatically

## For CI (Continuous Improvement) - uncomment if story_type = continuous_improvement
# retrospective_id: RETRO-NNN
# improvement_category: process  # process|tools|team|quality
# source_sprint: NNN

## For RA (Risk Action) - uncomment if story_type = risk_action
# raid_id: R-NNN  # R-NNN|A-NNN|I-NNN|D-NNN
# risk_score: 1  # 1-25 (from 5×5 matrix)
# action_type: mitigation  # mitigation|response|contingency
---

> [!note]- Progress updates
>
> - **YYYY-MM-DD**: Insert here your update. This is very useful for stand-ups, and for incremental
>   reports on progress. (TIP: To insert automatically a date stamp, use the CMD+SHIFT+D shortcut to
>   call the helper from the TEMPLATER plugin).

## Story Overview

[Provide a clear, concise description of what this story aims to achieve and why it's important to
the business and users. Include context about the problem being solved or opportunity being pursued]

**Business Value:**

- [Primary business outcome or benefit]
- [Impact on users or operations]
- [Alignment with strategic objectives]

**Swiss Market Context** (if applicable):

- [Quality expectations and precision requirements]
- [Multilingual considerations (FR/DE/EN)]
- [Regulatory or compliance factors]

---

## User Story Statement

**As a** [type of user/persona] **I want** [goal or functionality] **So that** [business value or
benefit]

**Additional Context:**

- **User Persona**: [Link to persona documentation if available]
- **User Journey**: [Relevant step in user journey this addresses]
- **Frequency of Use**: [How often will this functionality be used?]

---

> [!info] Checkbox Semantics
>
> - `- [ ]` under **Acceptance Criteria** = blocking (story cannot close until verified)
> - `- [ ]` under **Deliverables** = blocking (story cannot close until produced or delegated)
> - `- [ ]` under **Dependencies** = advisory context (informative, not blocking)
> - Plain text = advisory/non-blocking context

> [!warning] Write ACs at the level your statement promises
>
> If the **I want** clause is something an OPERATOR does (`install`, `deploy`, `run`, `publish`),
> then at least one AC must name the thing they actually invoke , a CLI flag, a command, an entry
> point. An AC that says _"the class can X"_ does **not** satisfy a statement that says _"the
> operator can X"_.
>
> **Worked example.** A story once promised _"install a kit from an HTTPS URL... so that I can
> consume published marketplace kits"_. All six of its ACs described what the source CLASS could do;
> none said the CLI used it. Every AC passed and the story closed , then a later test matrix
> measured **zero production consumers**, so the promised outcome had never been reachable. The
> wiring had to be filed as a fresh story.
>
> This is deliberately NOT machine-checked. The obvious lexical gate , an operator verb in the
> statement with no entry point named in the ACs , was built and measured against the corpus: it
> **passed the very story it was designed to catch**, because those ACs cite a MODULE path , which
> is evidence of exactly the unit-level scoping the check was meant to flag , and because a
> `ci:local` line appears in every DoD. A module path and a CLI path are lexically
> indistinguishable, so the judgement is yours at authoring time.

## Acceptance Criteria

### Functional Requirements

- [ ] **AC1**: [Clear, testable acceptance criteria using Given/When/Then format]
- [ ] **AC2**: [Specific measurable outcomes that can be verified]
- [ ] **AC3**: [Edge cases and error handling requirements]

### Non-Functional Requirements

> **Reference**: See
> [05-requirements-traceability.md](../../requirements/05-requirements-traceability.md#functional-domain--nfr-matrix)
> for the complete NFR matrix by functional domain.

#### Performance

- [ ] **NFR-PERF-001**: Page loads in < 3 seconds (First Contentful Paint)
- [ ] **NFR-PERF-002**: API responses in < 500ms (95th percentile)
- [ ] **NFR-PERF-003**: Search results in < 10 seconds (if applicable)

#### Accessibilité (WCAG 2.1 AA) : Engagement contractuel

> **Obligatoire** pour toutes les User Stories avec composants UI. Référence :
> [03-non-functional-requirements.md](../../requirements/03-non-functional-requirements.md#3-accessibility-requirements-wcag-21-aa)

##### Critères WCAG 2.1 AA

- [ ] **NFR-A11Y-001**: Conformité WCAG 2.1 AA vérifiée (axe-core 0 erreurs critiques)
- [ ] **NFR-A11Y-002**: Contraste couleurs ≥ 4.5:1 (texte), ≥ 3:1 (UI/grands textes)
- [ ] **NFR-A11Y-004**: Navigation clavier complète (Tab, Enter, Escape, flèches)
- [ ] **NFR-A11Y-005**: Indicateur de focus visible (outline ≥ 2px)
- [ ] **NFR-A11Y-006**: Compatible lecteurs d'écran (WAI-ARIA 1.0)
- [ ] **NFR-A11Y-007**: Erreurs formulaires associées aux champs (aria-describedby)
- [ ] **NFR-A11Y-008**: Information non transmise uniquement par la couleur
- [ ] **NFR-A11Y-009**: Textes alternatifs pour contenus non-textuels (alt, aria-label)
- [ ] **NFR-A11Y-010**: Texte redimensionnable à 200% sans perte de fonctionnalité

##### Scénarios Gherkin (exemples)

```gherkin
Scenario: Navigation clavier
  Given je navigue avec le clavier uniquement
  When j'accède à [fonctionnalité]
  Then tous les éléments interactifs sont atteignables via Tab
  And l'indicateur de focus est visible (outline ≥ 2px)
  And je peux activer les boutons avec Enter ou Space

Scenario: Lecteur d'écran
  Given j'utilise VoiceOver ou NVDA
  When j'interagis avec [composant]
  Then les labels ARIA sont annoncés correctement
  And les erreurs de formulaire sont vocalisées
  And les changements dynamiques sont annoncés (aria-live)

Scenario: Contraste couleurs
  Given j'affiche l'écran [nom écran]
  Then le contraste texte/fond est ≥ 4.5:1
  And le contraste composants UI est ≥ 3:1
  And les états (erreur, succès) utilisent icône + texte + couleur
```

##### Patterns Angular (CDK a11y)

- [ ] `FocusTrap` pour modales et dialogues
- [ ] `LiveAnnouncer` pour notifications dynamiques
- [ ] `FocusMonitor` pour gestion du focus
- [ ] Bibliothèque de composants : attributs `ariaLabel`, `ariaLabelledBy` configurés si applicables

_Note: Cocher les critères applicables. Pour les stories sans UI, supprimer cette section._

#### Security

- [ ] **TECH-SEC-003**: Access control verified (IAM integration)
- [ ] **TECH-SEC-008**: Input validation on all user inputs
- [ ] **TECH-SEC-005**: Audit logging for sensitive operations

#### Scalability

- [ ] **NFR-SCAL-001**: Supports the target concurrent user volume
- [ ] **NFR-SCAL-003**: Handles the expected data volume (if applicable)

#### Usability

- [ ] **NFR-USAB-005**: Task completable in < 8 clicks
- [ ] **NFR-USAB-007**: All UI text in French

_Note: Check/uncheck applicable NFRs based on the functional domain. Remove non-applicable items._

### Definition of Done

- [ ] Code implemented following project principles [SF, RP, DM, CA]
- [ ] Peer review completed with approval
- [ ] Unit tests written and passing (≥80% coverage) [TST]
- [ ] Integration tests written and passing
- [ ] Security review completed (vulnerability scan, code review) [SFT]
- [ ] Performance benchmarks met (load testing if applicable)
- [ ] API documentation updated in `docs-copper/architecture/apis/` [SD]
- [ ] UI/UX validated against acceptance criteria
- [ ] Deployment to test environment successful
- [ ] UAT sign-off completed with stakeholder approval
- [ ] Memory bank updated (`docs-copper/memory-bank/progress.md`)
- [ ] Dev journal entry created (`docs-copper/dev-journal/`)
- [ ] **Accessibilité** : Tests axe-core passent (0 erreurs critiques)
- [ ] **Accessibilité** : Navigation clavier vérifiée manuellement
- [ ] **Accessibilité** : Test lecteur d'écran effectué (VoiceOver ou NVDA)

---

## Deliverables

> **Convention**: Items here are blocking : the story cannot close until each deliverable is
> produced or explicitly delegated to a child story. Link child stories with `→ US-NNN`.

- [ ] **D1**: [Primary artefact this story produces]
- [ ] **D2**: [Child stories created for follow-on implementation, if any → US-NNN]

---

## Technical Requirements

### Database Changes

**Schema Modifications:**

- [List table creations, alterations, or deletions]
- [Index additions or optimisations]
- [Data migration requirements]

**Migration Artefacts:**

- [Reference to migration files or scripts]
- [Migration strategy and rollback plan]

**Naming Conventions:**

- Tables: `[table_prefix_or_standard]`
- Indexes: `[index_naming_standard]`
- Foreign keys: `[fk_naming_standard]`
- Stored procedures: `[procedure_naming_standard]`
- Views: `[view_naming_standard]`

### API Changes

**New Endpoints:**

- `[METHOD] /api/v1/resource` - [Description]
  - Request: [Body structure or parameters]
  - Response: [Expected response format]
  - Error codes: [HTTP status codes and error messages]

**Modified Endpoints:**

- [Changes to existing endpoints]
- [Backward compatibility considerations]
- [API versioning strategy]

**Documentation:**

- [Update OpenAPI/Swagger specs in `docs-copper/architecture/apis/`]
- [Postman collection updates]

### Frontend Changes

**UI Components:**

- [Components to be created or modified]
- [Design system compliance]
- [Accessibility requirements (ARIA labels, keyboard navigation)]

**User Interaction Flows:**

- [Step-by-step interaction sequences]
- [Error states and user feedback]
- [Loading states and progressive disclosure]

**Responsive Design:**

- [Mobile breakpoints and behaviour]
- [Tablet and desktop layouts]
- [Cross-browser compatibility requirements]

### Integration Points

**External Systems:**

- [Third-party services or APIs affected]
- [Authentication and authorisation flows]
- [Error handling and retry logic]

**Internal Components:**

- [Microservices or modules interacting]
- [Message queues or event streams]
- [Shared data stores or caches]

---

## Dependencies

### Prerequisites

**Must Be Completed First:**

- [Reference to blocking stories: US-XXX]
- [Infrastructure requirements or environment setup]
- [Third-party approvals or external dependencies]

**Technical Dependencies:**

- [Required libraries, frameworks, or tools]
- [Environment configurations]
- [Access permissions or credentials]

### Parallel Work

**Can Be Worked Simultaneously:**

- [Stories that can run in parallel: US-XXX]
- [Shared components requiring coordination]
- [Integration testing dependencies]

### Blocked By

**External Blockers:**

- [Vendor dependencies or procurement]
- [Regulatory approvals or legal reviews]
- [Client decisions or stakeholder sign-offs]

**Decision Points:**

- [Architectural decisions requiring ADR]
- [Design decisions requiring stakeholder input]
- [Technology choices requiring evaluation]

---

## Risk Assessment

### Technical Risks

**Risk 1:** [Description of technical complexity, technology constraints, or unknowns]

- **Probability**: [High/Medium/Low]
- **Impact**: [High/Medium/Low]
- **Mitigation**: [Specific actions to reduce risk]

**Risk 2:** [Integration challenges, performance concerns, security vulnerabilities]

- **Probability**: [High/Medium/Low]
- **Impact**: [High/Medium/Low]
- **Mitigation**: [Proof of concept, spike work, expert consultation]

### Business Risks

**Risk 1:** [User adoption challenges, business value uncertainty, market timing]

- **Probability**: [High/Medium/Low]
- **Impact**: [High/Medium/Low]
- **Mitigation**: [User research, pilot programmes, phased rollout]

### Timeline Risks

**Risk 1:** [Schedule dependencies, resource constraints, external blockers]

- **Probability**: [High/Medium/Low]
- **Impact**: [High/Medium/Low]
- **Mitigation**: [Buffer time, alternative resources, contingency planning]

---

## Testing Strategy

### Unit Testing

**Components Requiring Coverage:**

- [List of classes, functions, or modules]
- [Edge cases and boundary conditions]
- [Error handling scenarios]

**Target Coverage:** ≥80% [TST]

### Integration Testing

**API Endpoints to Test:**

- [List of endpoints and test scenarios]
- [Authentication and authorisation flows]
- [Error responses and status codes]

**Component Interactions:**

- [Service-to-service communication]
- [Database transaction handling]
- [Cache coherence and invalidation]

### User Acceptance Testing

**Test Scenarios:**

- [User workflow 1: step-by-step validation]
- [User workflow 2: alternative paths and error handling]
- [User workflow 3: edge cases and boundary conditions]

**Success Criteria:**

- [Measurable outcomes for UAT approval]
- [Stakeholder sign-off requirements]

### Performance Testing

**Load Testing Requirements:**

- [Concurrent user targets]
- [Transaction throughput requirements]
- [Resource utilisation limits]

**Performance Benchmarks:**

- Response time: ≤ 3s [as per project standards]
- Throughput: [requests per second]
- Uptime: ≥ 99.9% [as per project standards]

---

## Implementation Notes

### Development Approach [SF, CA, MOD]

**Recommended Strategy:**

- [Implementation phases or incremental delivery]
- [Code patterns to follow (design patterns, architectural styles)]
- [Modular design considerations]

**Architectural Considerations:**

- [Alignment with ADRs in `docs-copper/architecture/adr/`]
- [Impact on system architecture or data models]
- [Technical debt considerations and trade-offs]

**Code Principles:**

- [SF] Simplicity First - prefer straightforward solutions
- [RP] Readability Priority - clear, maintainable code
- [DM] Dependency Minimalism - minimal external dependencies
- [DRY] Don't Repeat Yourself - extract reusable components
- [CA] Clean Architecture - separation of concerns

### UI/UX Guidelines

**Design System Compliance:**

- [Reference to design system or style guide]
- [Component library usage]
- [Brand guidelines and visual identity]

**Accessibility Requirements (WCAG 2.1 AA):**

- WCAG 2.1 Level AA compliance where required by project standards
- WAI-ARIA support for dynamic components where applicable
- Screen reader support (NVDA, VoiceOver, JAWS)
- Keyboard navigation patterns (Tab, Enter, Escape, Arrow keys)
- Colour contrast ≥ 4.5:1 (text), ≥ 3:1 (UI components)
- Focus indicators visible (outline ≥ 2px)
- Accessibility patterns and supporting utilities appropriate to the chosen stack

**Responsive Design:**

- [Mobile-first approach or desktop-first]
- [Breakpoint strategy]
- [Touch target sizing and spacing]

### Data Migration

**Migration Scripts:**

- [Migration scripts or schema changes required]
- [Data transformation logic]
- [Validation and testing approach]

**Backward Compatibility:**

- [Support for legacy data formats]
- [API versioning strategy]
- [Deprecation timeline]

**Rollback Procedures:**

- [Rollback scripts and testing]
- [Data recovery strategy]
- [Monitoring and validation post-rollback]

---

## Success Metrics

### Quantitative Metrics

**Performance Improvements:**

- [Response time reduction: X% faster]
- [Throughput increase: Y% more transactions]
- [Error rate reduction: Z% fewer errors]

**Usage Statistics:**

- [Active users: target number]
- [Feature adoption: target percentage]
- [Conversion rates: target percentage]

### Qualitative Metrics

**User Satisfaction:**

- [User feedback scores or NPS targets]
- [Usability testing outcomes]
- [Support ticket reduction]

**Code Quality:**

- [Technical debt reduction]
- [Code complexity metrics (cyclomatic complexity ≤ 10)]
- [Maintainability improvements]

**Team Velocity:**

- [Impact on development speed]
- [Reduced rework or bug fixes]
- [Knowledge transfer effectiveness]

---

## Related Documentation

### Architecture Decision Records

- [ADR-XXX: Related architectural decision in `docs-copper/architecture/adr/`]
- [ADR-YYY: Technology choice or design pattern]

### API Specifications

- [OpenAPI spec: `docs-copper/architecture/apis/openapi/`]
- [Postman collection: `docs-copper/architecture/apis/postman/`]

### Design Assets

- [Wireframes or mockups: link to design tool]
- [User flow diagrams]
- [Prototypes or interactive designs]

### Technical Specifications

- [System architecture diagrams]
- [Database schema documentation]
- [Integration specifications]

### Memory Bank References

- [Active context: `docs-copper/memory-bank/activeContext.md`]
- [Progress tracking: `docs-copper/memory-bank/progress.md`]

---

## Story Breakdown (if applicable)

**When to Break Down:**

- Story exceeds 13 story points
- Implementation spans multiple sprints
- Multiple teams or dependencies involved
- Technical uncertainty requires spike work

### Sub-tasks

1. **TASK-NNN-001**: [Specific technical task - e.g., database schema design]

   - **Owner**: [Team member]
   - **Estimate**: [Hours or story points]
   - **Status**: [Not Started/In Progress/Done]

2. **TASK-NNN-002**: [Specific technical task - e.g., API endpoint implementation]

   - **Owner**: [Team member]
   - **Estimate**: [Hours or story points]
   - **Status**: [Not Started/In Progress/Done]

3. **TASK-NNN-003**: [Specific technical task - e.g., frontend component development]
   - **Owner**: [Team member]
   - **Estimate**: [Hours or story points]
   - **Status**: [Not Started/In Progress/Done]

---

## Quality Assurance Checklist

### Code Review

- [ ] Code follows project conventions and style guide
- [ ] All functions ≤ 30 lines [as per project standards]
- [ ] All files ≤ 300 lines [as per project standards]
- [ ] Nesting depth ≤ 2 levels [as per project standards]
- [ ] No magic values - constants properly defined [CMV]
- [ ] Error handling comprehensive and robust [REH]
- [ ] Logging appropriate and informative

### Security Review

- [ ] Input validation on all user inputs [IV]
- [ ] SQL injection prevention (parameterised queries)
- [ ] XSS prevention (output encoding)
- [ ] CSRF protection implemented
- [ ] Authentication and authorisation verified
- [ ] Sensitive data encrypted (at rest and in transit)
- [ ] Security scanning completed (OWASP ZAP, Snyk, etc.)

### Performance Review

- [ ] Database queries optimised (indexes, query plans)
- [ ] Caching strategy implemented where appropriate
- [ ] Resource cleanup (connections, file handles)
- [ ] No N+1 query problems
- [ ] Load testing completed for high-traffic endpoints

### Documentation Review

- [ ] Code comments clear and meaningful (where necessary)
- [ ] API documentation complete and accurate
- [ ] README updated if applicable
- [ ] Memory bank updated with key decisions
- [ ] Dev journal entry created

---

_[[user-story-template]] maintained by [Project Team] | Version 1.3.0 | Last updated: 2026-02-04_

---

> [!tip]- TEMPLATE USAGE GUIDELINES **To be excluded from the generated user story.** **STORY ID
> CONVENTION**:
>
> - Story Type Prefixes: EP-NNN, US-NNN, BUG-NNN, TD-NNN, SEC-NNN, SP-NNN, CI-NNN, RA-NNN
> - Example: US-001-01 (EPIC-001, Story 01)
> - NO sprint numbers in story IDs - sprint tracking via Kanban board
>
> **STORY TYPE SYSTEM** (8 Types - see story-types/README.md):
>
> - **EP (Epic)**: Strategic initiatives spanning multiple stories/sprints
> - **US (User Story)**: Standard feature delivery with business value
> - **BUG (Defect)**: Production issues requiring remediation
> - **TD (Technical Debt)**: Code quality, architecture, testing improvements
> - **SEC (Security)**: Vulnerabilities, compliance, security hardening
> - **SP (Spike)**: Time-boxed research to reduce uncertainty
> - **CI (Continuous Improvement)**: Actions from retrospectives
> - **RA (Risk Action)**: RAID registry mitigation actions
> - **Type-Specific Guidance**: See `cu:backlog-management` skill resources at
>   `${CLAUDE_PLUGIN_ROOT}/skills/backlog-management/resources/story-types/[TYPE]-guidance.md`
>
> **WHEN TO USE THIS TEMPLATE**:
>
> - Capturing new features or user-facing functionality (US)
> - Documenting system enhancements or improvements (US, TD, CI)
> - Planning technical debt reduction work (TD)
> - Organising complex initiatives requiring user acceptance (EP, US)
> - Tracking bugs and defects (BUG)
> - Security and compliance work (SEC)
> - Research and investigation (SP)
> - Risk mitigation actions (RA)
>
> **AGENT SUPPORT** (the role; whichever agent an installed kit provides for it):
>
> - the project-management role - Project planning and story refinement
> - the agile-coaching role - Agile methodology and story quality
> - the CTO-coaching / technical-direction role - Strategic guidance and technical direction
>
> **PRINCIPLE TAGS**: Core: [SF], [RP], [DM], [DRY], [CA], [MOD] Quality: [TST], [TDT], [REH], [CSD]
> Security: [SFT], [IV], [CMV] Documentation: [SD], [ORG], [FOC], [SCP] Workflow: [AC], [CD], [IMP]
>
> **QUALITY STANDARDS**:
>
> - Test coverage: ≥80%
> - Response time: ≤3s
> - Uptime: ≥99.9%
> - Code complexity: ≤10 (cyclomatic)
> - Function length: ≤30 lines
> - File length: ≤300 lines
> - Nesting depth: ≤2 levels
>
> **BEFORE YOU START**:
>
> 1. Review ADRs in `docs-copper/architecture/adr/`
> 2. Check memory bank `docs-copper/memory-bank/`
> 3. Consult the project-management or agile-coaching role for refinement
> 4. Ensure INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable)
>
> **DURING DEVELOPMENT**:
>
> 1. Update story status in Kanban board
> 2. Document decisions in `docs-copper/dev-journal/`
> 3. Create ADRs for architectural decisions
> 4. Communicate blockers immediately
>
> **UPON COMPLETION**:
>
> 1. Verify all acceptance criteria met
> 2. Complete Definition of Done checklist
> 3. Update memory bank with outcomes
> 4. Create dev journal entry
>
> **SWISS QUALITY STANDARDS**:
>
> - Precision and attention to detail expected
> - Comprehensive documentation required
> - Long-term maintainability prioritised over speed
> - Multilingual support (FR/DE/EN) where applicable
>
> **TEMPLATE MAINTENANCE**:
>
> - Remove sections not applicable to your story
> - Aim for clarity over completeness
> - Update criteria as understanding evolves
> - Link to documentation rather than duplicating

> [!info]- TEMPLATE DATA (YAML BackMatter) For indexing, search, and validation purposes. **To be
> excluded from the generated user story.**
>
> ```yaml
> template_name: 'User Story Template'
> template_description:
>   'Standardised template for capturing user stories following Agile/Scrum methodology with
>   comprehensive acceptance criteria, technical requirements, and quality assurance'
> template_scope:
>   'Use for all new features, enhancements, and technical debt work requiring user acceptance.
>   Applicable to project stories (US-001+) only; scaffold stories (US-000) are eternal and never
>   modified.'
> template_version: '1.3.0'
> template_last_updated: '2026-02-04'
> template_status: 'active'
> template_category: 'planning'
> template_maintained_by: '[Project Team]'
> principle_codes:
>   # Core Development Principles
>   - SF # Simplicity First
>   - RP # Readability Priority
>   - DM # Dependency Minimalism
>   - DRY # Don't Repeat Yourself
>   - CA # Clean Architecture
>   - MOD # Modularity Focus
>   # Quality & Testing
>   - TST # Test Coverage (≥80%)
>   - TDT # Test-Driven Thinking
>   - REH # Robust Error Handling
>   - CSD # Code Smell Detection
>   # Security
>   - SFT # Security-First Thinking
>   - IV # Input Validation
>   - CMV # Constants Over Magic Values
>   # Documentation & Organisation
>   - SD # Strategic Documentation
>   - ORG # Organisational Clarity
>   - FOC # Focus on Relevant Code
>   - SCP # Scope Protection
>   # Workflow
>   - AC # Atomic Changes
>   - CD # Commit Discipline
>   - IMP # Impact Analysis
>   # Organisational Values
>   - COM # Commitment
>   - RSP # Respect
>   - SHR # Sharing
>   - TSP # Team Spirit
> cross_references:
>   - 'Memory Bank: docs-copper/memory-bank/'
>   - 'Dev Journal: docs-copper/dev-journal/'
>   - 'Architecture ADRs: docs-copper/architecture/adr/'
>   - 'Rule Template: rule-template.md'
> applies_to:
>   - 'All project team members (developers, testers, business analysts)'
>   - 'Feature development, enhancements, technical debt work'
> artifacts:
>   - 'User stories tracked in Kanban board'
>   - 'Task breakdowns (TASK-NNN-XXX)'
>   - 'Acceptance criteria checklists'
>   - 'Dev journal entries documenting implementation'
>   - 'ADRs for significant architectural decisions'
> tools:
>   - 'the project-management role - Project planning and story refinement'
>   - 'the agile-coaching role - Agile methodology and story quality'
>   - 'the CTO-coaching / technical-direction role - Strategic guidance and technical direction'
> quality_metrics:
>   test_coverage: '≥80%'
>   response_time: '≤3s'
>   uptime: '≥99.9%'
>   code_complexity: '≤10 (cyclomatic complexity)'
>   function_length: '≤30 lines'
>   file_length: '≤300 lines'
>   nesting_depth: '≤2 levels'
> naming_conventions:
>   scaffold_stories: 'US-000 (永久 eternal - never modify)'
>   project_stories: 'US-001, US-002, US-003... (active development)'
>   tasks: 'TASK-NNN-XXX'
>   note: 'NO sprint numbers in story IDs - sprint tracking via Kanban board'
> changelog:
>   - version: '1.3.0'
>     date: '2026-02-04'
>     changes: 'Accessibility section enriched with reusable project-agnostic criteria and examples'
>   - version: '1.2.0'
>     date: '2026-02-04'
>     changes: 'Version initiale avec structure complète'
> ```
