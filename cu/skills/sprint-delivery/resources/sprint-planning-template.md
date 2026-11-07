---
sprint_id: sprint-NNN
sprint_number: 0
project_code: '[PROJECT-CODE]'
scope: project
start_date: YYYY-MM-DD
end_date: YYYY-MM-DD
duration_weeks: 2
working_days: 10
team_name: ''
scrum_master: ''
product_owner: ''
tech_lead: ''
sprint_type: feature
priority_level: medium
velocity_target: 0
committed_velocity: 0
primary_goal: ''
test_coverage_target: 85
status: planning
health: green
completion_percentage: 0
created_date: YYYY-MM-DD
created_by: ''
version: 1.0
tags: []
---

## Sprint Overview

**Sprint Goal**: [One clear, concise statement of what this sprint achieves]

**Business Value**:

- [Primary business outcome or benefit]
- [Impact on users or operations]
- [Alignment with strategic objectives]

**Success Criteria**:

- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
- [ ] [Measurable criterion 3]

**Sprint Theme**: [Optional thematic description for team alignment]

---

## Team Capacity

### Available Capacity

| Team Member | Role   | Available Hours | Allocation % | Focus Areas    |
| ----------- | ------ | --------------- | ------------ | -------------- |
| [Name]      | [Role] | [40h]           | [100%]       | [Area1, Area2] |
| [Name]      | [Role] | [32h]           | [80%]        | [Area1, Area2] |
| **Total**   |        | **[72h]**       |              |                |

### Capacity Adjustments

**Holidays**: [List any holidays during sprint]

**Planned Absences**: [Vacations, conferences, training]

**Non-Sprint Work**: [Support, meetings, admin - typically 20-30%]

**Net Capacity**: [Total available hours after adjustments]

### Velocity Context

- **Previous Sprint Velocity**: XX points
- **3-Sprint Average**: XX points
- **Target Velocity**: XX points
- **Commitment Strategy**: [Conservative / Realistic / Stretch] - [Rationale]

---

## Selected Backlog Items

### Committed User Stories

#### High Priority (Must Have)

1. **[US-NNN-001] Story Title** - X points

   - **Business Value**: [Why this matters]
   - **Acceptance Criteria**: [Link to US document or brief summary]
   - **Dependencies**: [Any blockers or prerequisites]
   - **Assigned To**: [Team member(s)]
   - **Estimated Hours**: Xh

2. **[US-NNN-002] Story Title** - X points
   - **Business Value**: [Why this matters]
   - **Acceptance Criteria**: [Link or summary]
   - **Dependencies**: [Blockers or prerequisites]
   - **Assigned To**: [Team member(s)]
   - **Estimated Hours**: Xh

#### Medium Priority (Should Have)

[Stories that are committed but could flex if needed]

#### Stretch Goals (Could Have)

[Stories that might be pulled in if capacity allows]

### Technical Debt Items

- **[TECH-001]** [Brief description] - Xh
- **[TECH-002]** [Brief description] - Xh

### Bug Fixes

- **[BUG-001]** [Brief description] - Priority: [High/Medium/Low] - Xh
- **[BUG-002]** [Brief description] - Priority: [High/Medium/Low] - Xh

### Total Commitment Summary

- **Story Points Committed**: XX
- **Estimated Hours**: XXh (vs. XXh capacity)
- **Buffer**: XX% (recommended: 15-20% for unknowns)

---

## Dependencies & Risks

### External Dependencies

| Dependency    | Type               | Owner  | Status   | Impact          | Mitigation        |
| ------------- | ------------------ | ------ | -------- | --------------- | ----------------- |
| [Description] | Technical/Business | [Name] | [Status] | High/Medium/Low | [Mitigation plan] |

### Internal Dependencies

| Item     | Depends On        | Risk Level | Plan                       |
| -------- | ----------------- | ---------- | -------------------------- |
| [US-XXX] | [US-YYY complete] | Medium     | [Sequencing or mitigation] |

### Identified Risks

| Risk               | Probability     | Impact          | Mitigation Strategy   | Owner  |
| ------------------ | --------------- | --------------- | --------------------- | ------ |
| [Risk description] | High/Medium/Low | High/Medium/Low | [Concrete mitigation] | [Name] |

### Assumptions

[List key assumptions that could invalidate sprint plan]

- [Assumption 1]
- [Assumption 2]

---

## Architecture Impact

### ADRs Required or Referenced

- **[ADR-XXX] [Decision Title]**: [Required / Referenced] - [Status and timing]
- **[ADR-YYY] [Decision Title]**: [Required / Referenced] - [Status and timing]

### Technical Spikes

| Spike   | Purpose           | Time-boxed | Owner  | Expected Outcome |
| ------- | ----------------- | ---------- | ------ | ---------------- |
| [Topic] | [Inform decision] | [Xh]       | [Name] | [Deliverable]    |

### Technology Stack Changes

[None planned / List any new dependencies, frameworks, or tools being introduced]

---

## Definition of Done

### Sprint-Level DoD

- [ ] All committed user stories meet acceptance criteria
- [ ] Test coverage ≥ 85% for new code **[TST]**
- [ ] Code reviewed and approved by at least one peer **[CA]**
- [ ] Security scan completed with zero critical issues **[SFT]**
- [ ] Documentation updated (code comments, API docs, README) **[SD]**
- [ ] No known defects (or documented and prioritised for future)
- [ ] Deployed to staging environment successfully
- [ ] Demo prepared for Sprint Review

### Story-Level DoD

- [ ] Acceptance criteria verified by Product Owner
- [ ] Unit tests written and passing **[TST]**
- [ ] Integration tests written and passing **[TST]**
- [ ] Code follows project standards **[CA]**
- [ ] No TODO or FIXME comments without tickets
- [ ] Branch merged to main/develop
- [ ] Related ADRs updated or created **[SD]**

### Client or Delivery Quality Standards

- [ ] Multilingual documentation where required (EN/FR/DE) **[ISA]**
- [ ] Client-facing deliverables reviewed for precision and completeness
- [ ] Long-term maintainability considered in all technical decisions **[CA]**

---

## Sprint Ceremonies

### Daily Standups

- **Time**: [HH:MM timezone]
- **Duration**: 15 minutes
- **Location**: [Physical room / Video link]
- **Format**: Yesterday/Today/Blockers

### Sprint Review

- **Date**: [YYYY-MM-DD]
- **Time**: [HH:MM timezone]
- **Duration**: 1-2 hours
- **Attendees**: Team + Stakeholders + Product Owner
- **Demo Agenda**: [To be populated during sprint]

### Sprint Retrospective

- **Date**: [YYYY-MM-DD] (after Review)
- **Time**: [HH:MM timezone]
- **Duration**: 1-1.5 hours
- **Attendees**: Team + Scrum Master
- **Format**: Start/Stop/Continue or custom

### Stakeholder Communication

| Stakeholder   | Update Frequency | Method          | Owner        |
| ------------- | ---------------- | --------------- | ------------ |
| Product Owner | Daily            | Standup + Slack | Scrum Master |
| [Stakeholder] | [Frequency]      | [Method]        | [Name]       |

---

## Sprint Metrics Dashboard

### Velocity Tracking

- **Committed Points**: XX
- **Completed Points**: XX (updated daily)
- **Velocity %**: XX% (completed/committed)
- **Trend**: [Reference to previous 3 sprints]

### Burndown Chart Data

| Day | Planned Remaining | Actual Remaining | Status   |
| --- | ----------------- | ---------------- | -------- |
| 1   | XX points         | XX points        | ✅/⚠️/❌ |
| 2   | XX points         | XX points        | ✅/⚠️/❌ |
| ... | ...               | ...              | ...      |

### Quality Metrics

- **Test Coverage**: Current XX% / Target 85%
- **Code Review Turnaround**: Avg Xh (target: <24h)
- **Build Success Rate**: XX% (target: >95%)
- **Defect Escape Rate**: X bugs to staging (target: <3)

### Efficiency Metrics

- **Story Cycle Time**: Avg X days (from start to done)
- **Blocked Days**: X days total across all stories
- **Rework %**: X% of time spent on rework (target: <10%)
- **Carry-Over Stories**: X stories not completed (target: 0)

---

## Client or Delivery Quality Standards

### Documentation Precision

- All estimates include confidence intervals (e.g., "8-12h")
- Assumptions explicitly stated and validated
- Dependencies mapped with specific owners and deadlines
- Risk mitigation plans concrete and actionable

### Multilingual Capability

- **Client-Facing Deliverables**: [EN/FR/DE as required]
- **Internal Documentation**: [Typically EN, specify if otherwise]
- **Sprint Review Materials**: [Prepared in client's preferred language]

### Sustainability Planning

- **Technical Debt Budget**: X% of sprint capacity
- **Refactoring Allocation**: Minimum Yh per sprint
- **Knowledge Transfer**: Pair programming hours allocated
- **Documentation Standards**: README, API docs, ADRs maintained

### Maintainability Criteria

- Code must be understandable 6 months from now
- No "quick hacks" without explicit technical debt tickets
- Architecture decisions consider 3-5 year horizon

---

## Related Documentation

**User Stories**: `docs-copper/roadmap/sprint-NNN/user-stories/` **Architecture Decisions**:
`docs-copper/architecture/adr/` **Sprint Review**: `docs-copper/roadmap/sprint-NNN/review.md`
(created at sprint end) **Sprint Retrospective**: `docs-copper/roadmap/sprint-NNN/retrospective.md`
(created at sprint end) **Memory Bank**: `docs-copper/memory-bank/activeContext.md`

---

**Sprint Status**: [planning | active | review | complete | cancelled] **Last Updated**: YYYY-MM-DD

---

> [!tip]- TEMPLATE USAGE GUIDELINES **To be excluded from the generated sprint plan.**
>
> **INSTRUCTIONS FOR COMPLETING THIS TEMPLATE**:
>
> 1. Create sprint plan at: `docs-copper/roadmap/sprint-NNN/sprint-plan.md`
> 2. Naming convention: `sprint-NNN-plan.md` (e.g., `sprint-001-plan.md`)
> 3. Replace all [placeholder text] with actual content
> 4. Update YAML frontmatter with real values
> 5. Delete sections not applicable to your sprint
> 6. Tag all decisions with appropriate principle codes
> 7. Delete this entire callout section before finalising
>
> **WHEN TO USE THIS TEMPLATE**:
>
> - At the START of each sprint during Sprint Planning ceremony
> - Project sprints: `/roadmap/sprint-NNN/` (Sprint 001+ - active development)
>
> **FILLING OUT WORKFLOW**:
>
> **Before Sprint Planning**:
>
> 1. Product Owner prepares prioritised backlog
> 2. Tech Lead reviews upcoming technical decisions (ADRs)
> 3. Scrum Master gathers team availability
>
> **During Sprint Planning (Part 1: What)**:
>
> 1. Product Owner presents sprint goal and high-priority stories
> 2. Team discusses and estimates each story
> 3. Fill "Sprint Overview" and "Selected Backlog Items" sections
>
> **During Sprint Planning (Part 2: How)**:
>
> 1. Team breaks down stories into tasks
> 2. Identify dependencies, risks, technical spikes
> 3. Complete "Dependencies & Risks" and "Architecture Impact"
> 4. Finalise "Team Capacity" and ensure commitment is realistic
>
> **After Sprint Planning**:
>
> 1. Scrum Master publishes sprint plan to team repository
> 2. Create placeholder documents for expected ADRs
> 3. Set up sprint tracking board (Jira, GitHub Projects, etc.)
> 4. Schedule all ceremonies (standups, review, retrospective)
>
> **During the Sprint**:
>
> - **Daily Updates**: Update "Sprint Metrics Dashboard" section
> - **Blockers**: Add to "Dependencies & Risks" as they emerge
> - **Scope Changes**: Document any additions/removals with rationale
> - **ADR Creation**: Link created ADRs in "Architecture Impact"
>
> **At Sprint End**:
>
> - Mark status as "complete" or "cancelled"
> - Update final metrics (velocity, quality, planning accuracy)
> - Create Sprint Review document
> - Create Sprint Retrospective document
> - Archive sprint plan (read-only)
>
> **FRONTMATTER FIELD GUIDANCE**:
>
> - `sprint_id`: Format `sprint-NNN` (e.g., sprint-001, sprint-002)
> - `sprint_number`: Numeric (1+ for project sprints)
> - `project_code`: Project identifier (e.g., [PROJECT-CODE])
> - `scope`: "scaffold" or "project"
> - `start_date` / `end_date`: YYYY-MM-DD format
> - `duration_weeks`: Typically 2 weeks
> - `working_days`: Excluding weekends/holidays
> - `sprint_type`: feature | bug-fix | technical-debt | research
> - `priority_level`: low | medium | high | critical
> - `velocity_target`: Story points or ideal days
> - `committed_velocity`: Actual commitment (should be ≤ target)
> - `status`: planning | active | review | complete | cancelled
> - `health`: green | yellow | red (sprint health indicator)
> - `test_coverage_target`: Percentage (default: 85%)
>
> **INTEGRATION WITH OTHER ARTEFACTS**:
>
> - **User Stories**: Link bidirectionally (sprint → stories, stories → sprint)
> - **ADRs**: Reference sprint that prompted decision
> - **Memory Bank**: Update `activeContext.md` with sprint outcomes
> - **Dev Journal**: Daily entries reference sprint plan for context
> - **Retrospective**: Previous retro action items reviewed in planning
>
> **SWISS MARKET BEST PRACTICES**:
>
> - **Precision**: Estimates include confidence ranges, not single numbers
> - **Quality**: Never compromise DoD for velocity
> - **Communication**: Client visibility level determines update frequency
> - **Long-term**: Always allocate technical debt time, even under pressure
>
> **COMMON PITFALLS TO AVOID**:
>
> 1. **Over-commitment**: Always leave 15-20% buffer for unknowns
> 2. **Vague Goals**: "Make progress" → "JWT implementation complete and tested"
> 3. **Ignoring Velocity**: Don't commit to 40 points if team averages 25
> 4. **Missing Dependencies**: Explicitly map external dependencies with owners
> 5. **No Stretch Goals**: Team finishes early with nothing to pull in
> 6. **Weak DoD**: "Code works" → Specific quality criteria with checkboxes
> 7. **No Risk Mitigation**: Identifying risks without mitigation plans is insufficient
> 8. **Skipping Ceremonies**: All ceremonies are valuable, don't skip retrospectives
>
> **QUALITY CHECKLIST**: Before finalising sprint plan:
>
> - [ ] Sprint goal is SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
> - [ ] Team capacity calculated and realistic (accounts for meetings, overhead)
> - [ ] All selected stories have acceptance criteria
> - [ ] Dependencies identified with owners and deadlines
> - [ ] Risks assessed with mitigation strategies
> - [ ] Expected ADRs listed proactively
> - [ ] Definition of Done explicit and measurable
> - [ ] Ceremonies scheduled with confirmed attendees
> - [ ] Metrics baseline established for tracking
> - [ ] Product Owner and Team have consensus on commitment

> [!info]- TEMPLATE DATA (YAML BackMatter) For indexing, search, and validation purposes. **To be
> excluded from the generated sprint plan.**
>
> ```yaml
> template_name: 'Sprint Planning Template'
> template_description:
>   'Agile sprint planning template with comprehensive capacity planning, risk management, and
>   delivery quality standards'
> template_scope:
>   'Use for planning all sprints (Sprint 0 for scaffold, Sprint 1+ for projects) following
>   Agile/Scrum methodology'
> template_version: '1.0.0'
> template_last_updated: '2025-10-26'
> template_status: 'active'
> template_category: 'planning'
> template_maintained_by: '[Project Team]'
>
> principle_codes_emphasized:
>   - ORG # Organisational Clarity
>   - FOC # Focus on Relevant Code
>   - SCP # Scope Protection
>   - TST # Test Coverage
>   - ARC # Architecture Stability
>   - IMP # Impact Analysis
>   - SF # Simplicity First
>   - SD # Strategic Documentation
>   - ISA # Industry Standards Adherence
>   - ENV # Environment Awareness
>   - CA # Clean Architecture
>   - REH # Robust Error Handling
>   - AC # Atomic Changes
>
> cross_references:
>   - 'User Story Template: user-story-template.md'
>   - 'ADR Template: adr-template.md'
>   - 'Sprint Retrospective Template: (to be created)'
>   - 'Dev Journal Template: dev-journal-template.md'
>   - 'Rule Template: rule-template.md'
>   - 'Memory Bank: docs-copper/memory-bank/'
>   - 'Roadmap: docs-copper/roadmap/'
>
> applies_to:
>   - 'Scrum Masters facilitating sprint planning'
>   - 'Product Owners defining sprint goals and priorities'
>   - 'Development teams committing to sprint work'
>   - 'Tech Leads planning architecture work and spikes'
>   - 'Stakeholders reviewing sprint commitments'
>
> usage_pattern:
>   when_to_create:
>     - 'At start of each sprint during Sprint Planning ceremony'
>     - 'Sprint 1+ for project development (ongoing)'
>     - 'When initiating new development cycle or iteration'
>   naming_convention:
>     project: 'sprint-NNN-plan.md (e.g., sprint-001-plan.md, sprint-002-plan.md)'
>   storage_location:
>     project: 'docs-copper/roadmap/sprint-NNN/'
>
> related_workflows:
>   - 'Create user stories before sprint planning for backlog refinement'
>   - 'Reference ADRs for architectural decisions during planning'
>   - 'Update memory-bank/project-context/activeContext.md with sprint focus'
>   - 'Create Sprint Review document at sprint end'
>   - 'Create Sprint Retrospective document after review'
>   - 'Previous retrospective action items inform next sprint planning'
>   - 'Dev journal entries reference sprint context'
>
> agile_best_practices:
>   - 'Capacity-based planning with explicit buffers (15-20%)'
>   - 'SMART sprint goals (Specific, Measurable, Achievable, Relevant, Time-bound)'
>   - 'Structured dependency and risk tracking'
>   - 'Velocity tracking for continuous improvement'
>   - 'Definition of Done non-negotiable'
>   - 'Proactive ADR planning for architectural decisions'
>   - 'Team capacity respects individual availability'
>   - 'Stretch goals prevent idle time'
>   - 'Daily metrics updates for transparency'
>
> swiss_quality_emphasis:
>   - 'Precision in estimates (confidence intervals, not single numbers)'
>   - 'Long-term sustainability (technical debt budgets, maintainability)'
>   - 'Multilingual capability (EN/FR/DE documentation)'
>   - 'Client visibility and communication standards'
>   - 'Quality gates non-negotiable (test coverage, security, reviews)'
>   - 'Documentation completeness before claiming done'
>   - 'Edge case consideration, not just happy path'
>   - '3-5 year horizon for architecture decisions'
>
> metrics_tracked:
>   velocity:
>     - 'Committed vs. completed story points'
>     - '3-sprint moving average'
>     - 'Velocity trend analysis'
>   quality:
>     - 'Test coverage percentage'
>     - 'Code review turnaround time'
>     - 'Build success rate'
>     - 'Defect escape rate'
>   efficiency:
>     - 'Story cycle time'
>     - 'Blocked days'
>     - 'Rework percentage'
>     - 'Carry-over stories'
>   planning_accuracy:
>     - 'Estimation variance (actual vs. estimated)'
>     - 'Risk materialisation rate'
>     - 'Dependency completion on time'
>
> external_references:
>   - 'Scrum Guide: https://scrumguides.org/'
>   - 'Agile Manifesto: https://agilemanifesto.org/'
>   - 'Sprint Planning (Atlassian): https://www.atlassian.com/agile/scrum/sprint-planning'
>   - 'Client or delivery quality standards: project-specific guidance'
> ```
