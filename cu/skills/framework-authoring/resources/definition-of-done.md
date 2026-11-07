---
title: 'Definition of Done (DoD) Template'
description: 'Comprehensive 4-level Definition of Done framework adaptable to any project context'
version: '1.0.0'
created: '2025-10-30'
last_updated: '2025-10-30'
status: 'active'
category: 'quality-assurance'
applies_to:
  - 'User Stories'
  - 'Sprints'
  - 'Releases'
  - 'Epics'
principle_codes:
  - COM # Commitment to quality
  - TST # Test Coverage
  - SD # Strategic Documentation
  - CA # Clean Architecture
  - CD # Commit Discipline
cross_references:
- '${CLAUDE_PLUGIN_ROOT}/skills/backlog-management/resources/user-story-template.md'
- '${CLAUDE_PLUGIN_ROOT}/skills/sprint-delivery/resources/sprint-planning-template.md'
  - '/.claude/rules/cu/02-core-coding-principles.rules.md'
---

# Definition of Done (DoD) Template

**Purpose**: This template establishes comprehensive quality criteria across four hierarchical
levels (Story, Sprint, Release, Epic) to ensure consistent delivery standards across different
projects and delivery contexts.

**How to Use**:

1. **Copy relevant sections** to user stories, sprint goals, release plans, or epic definitions
2. **Check off criteria** as they are completed
3. **Customise** based on project-specific requirements (mark customisations clearly)
4. **Review** during sprint retrospectives and improve criteria based on learnings

---

## Level 1: Story-Level Definition of Done

**Scope**: Individual user story completion criteria **When to Use**: Every user story, task, or bug
fix **Review Point**: Before marking story as "Done" in sprint board

### Code Quality & Implementation

- [ ] **[CA] Clean Architecture**: Code follows project coding standards and style guides
- [ ] **[SF] Simplicity First**: Implementation uses simplest viable solution
- [ ] **[RP] Readability Priority**: Code is self-documenting with clear naming
- [ ] **[DRY] Don't Repeat Yourself**: No code duplication; reusable components extracted
- [ ] **[REH] Robust Error Handling**: Comprehensive error handling for edge cases
- [ ] **[IV] Input Validation**: All external inputs validated and sanitised
- [ ] **Principle Tagging**: All decisions tagged with relevant principle codes `[XX]`

### Testing Requirements

- [ ] **[TST] Unit Tests**: ≥80% code coverage for new/modified code
- [ ] **Integration Tests**: ≥70% coverage for API endpoints and service interactions
- [ ] **Test Documentation**: Test cases documented with clear assertions
- [ ] **All Tests Pass**: Green build in CI/CD pipeline
- [ ] **Edge Cases Covered**: Boundary conditions and error scenarios tested

### Documentation Standards

- [ ] **[SD] Strategic Documentation**: Complex logic documented (why, not just what)
- [ ] **API Documentation**: OpenAPI/Swagger specs updated (if API changes)
- [ ] **README Updates**: Relevant README.md files updated with new features
- [ ] **Code Comments**: Non-obvious logic explained inline
- [ ] **CHANGELOG**: Entry added to CHANGELOG.md with semantic versioning
- [ ] **Deliverable Completeness**: All declared deliverables produced or explicitly delegated to
      child stories

### Code Review & Quality Gates

- [ ] **Peer Review**: Code reviewed and approved by at least one team member
- [ ] **Linters Pass**: All automated linters pass (Semgrep, MegaLinter, ESLint, etc.)
- [ ] **Security Scan**: No new security vulnerabilities introduced
- [ ] **Performance Check**: No performance regressions detected

### Version Control & Deployment

- [ ] **[CD] Commit Discipline**: Conventional commits with semantic messages
- [ ] **Branch Clean**: Feature branch merged to develop/main and deleted
- [ ] **Deployment Ready**: Code deployed to development/staging environment
- [ ] **Rollback Plan**: Rollback procedure documented if needed

---

## Level 2: Sprint-Level Definition of Done

**Scope**: Sprint goal and collective story completion **When to Use**: End of each sprint
(typically 2-week cycles) **Review Point**: Sprint Review and Retrospective meetings

### Sprint Backlog Completion

- [ ] **Committed Stories**: All committed user stories meet Story-Level DoD
- [ ] **Sprint Goal Achieved**: Sprint goal met or clearly documented why not
- [ ] **Acceptance Criteria**: All acceptance criteria validated by Product Owner
- [ ] **Demo Ready**: Features demonstrated to stakeholders successfully

### Quality Metrics

- [ ] **Test Coverage**: Overall project coverage ≥80% unit, ≥70% integration
- [ ] **Code Quality**: No critical or high-severity code smells introduced
- [ ] **Technical Debt**: New technical debt documented in backlog
- [ ] **Bug Count**: No increase in critical/high-priority bugs

### Documentation & Knowledge Sharing

- [ ] **Sprint Documentation**: Sprint review notes and retrospective captured
- [ ] **Memory Bank Updated**: activeContext.md and progress.md reflect current state
- [ ] **Architecture Decisions**: ADRs created for significant architectural changes
- [ ] **Team Knowledge**: Knowledge shared through pair programming or demos

---

## Level 3: Release-Level Definition of Done

**Scope**: Production-ready release criteria **When to Use**: Before deploying to production
environment **Review Point**: Release planning and Go/No-Go decision meetings

### Functional Completeness

- [ ] **All Features Complete**: All planned features meet Story-Level and Sprint-Level DoD
- [ ] **User Acceptance**: UAT completed and signed off by Product Owner/Stakeholders
- [ ] **Business Value**: Release delivers measurable business value
- [ ] **Feature Flags**: Feature toggles configured for gradual rollout if needed

### Quality Assurance

- [ ] **E2E Testing**: Critical user workflows tested end-to-end
- [ ] **Performance Testing**: Load testing completed (expected + 3x traffic)
- [ ] **Security Audit**: Security review completed, vulnerabilities addressed
- [ ] **Accessibility**: WCAG 2.1 AA compliance verified (if UI changes)
- [ ] **Cross-Browser/Device**: Tested on target browsers and devices

### Documentation & Training

- [ ] **User Documentation**: User guides, help documentation, FAQs updated
- [ ] **Admin Documentation**: Operational runbooks, troubleshooting guides created
- [ ] **API Documentation**: Complete OpenAPI/Swagger specs published
- [ ] **Release Notes**: CHANGELOG.md updated with all changes
- [ ] **Training Materials**: Training provided to support/operations teams if needed

### Compliance & Legal

- [ ] **[RSP] GDPR/Privacy**: Data protection requirements met (GDPR, CCPA, local privacy law)
- [ ] **Licensing**: All dependencies reviewed for license compatibility
- [ ] **Regulatory**: Industry-specific compliance verified (sector regulators, ISO, etc.)
- [ ] **Audit Trail**: All changes logged for compliance auditing

### Deployment & Operations

- [ ] **Deployment Plan**: Deployment procedure documented and tested
- [ ] **Rollback Plan**: Rollback procedure tested and ready
- [ ] **Monitoring**: Production monitoring and alerting configured
- [ ] **Incident Response**: On-call rotation and incident procedures updated
- [ ] **Backup/Recovery**: Backup strategy validated, recovery tested
- [ ] **Production Deploy**: Successfully deployed to production environment
- [ ] **Smoke Tests**: Post-deployment smoke tests pass

---

## Level 4: Epic-Level Definition of Done

**Scope**: Major feature/initiative completion **When to Use**: Completion of multi-sprint epics or
major business initiatives **Review Point**: Epic closure and business value assessment

### Business Value Delivery

- [ ] **[COM] Commitment**: Business objectives achieved and measurable
- [ ] **Success Metrics**: KPIs met or exceeded (defined at epic start)
- [ ] **Stakeholder Satisfaction**: Positive feedback from key stakeholders
- [ ] **ROI Demonstrated**: Return on investment calculated and documented

### Technical Excellence

- [ ] **Architecture Aligned**: Solution aligns with target architecture (ADRs)
- [ ] **Scalability**: Solution scales to expected load (tested)
- [ ] **Maintainability**: Code maintainable with clear patterns and documentation
- [ ] **Technical Debt**: Minimal technical debt; any debt documented and prioritised

### Knowledge Transfer & Documentation

- [ ] **[COL] Collaboration**: Knowledge shared across team through documentation
- [ ] **Architecture Documentation**: System context, C4 diagrams, ADRs complete
- [ ] **Lessons Learned**: Retrospective insights documented for future epics
- [ ] **Onboarding Materials**: New team members can understand feature from docs

---

## Regional or Client-Specific Criteria

**Scope**: Additional quality standards for specific regulatory, linguistic, or client contexts
**When to Apply**: Projects with explicit regional, regulatory, or client-mandated requirements

### Compliance & Standards

- [ ] **ISO 9001**: Quality management standards followed
- [ ] **Regional Privacy Law**: Applicable data protection regulations verified
- [ ] **Industry Regulation**: Sector-specific regulations met (if applicable)
- [ ] **Domain Regulation**: Domain-specific requirements met (if applicable)

### Multilingual Support

- [ ] **Primary Language**: Documentation available in the required primary language
- [ ] **Secondary Language(s)**: Additional required languages available
- [ ] **English**: International English documentation available where required
- [ ] **Localisation**: UI/UX localised for regional conventions where needed

### Quality Standards

- [ ] **[COM] Delivery Quality**: Precision, reliability, and attention to detail demonstrated
- [ ] **Sustainability Alignment**: Environmental sustainability considerations documented where
      relevant
- [ ] **Team Health**: Team sustainability and delivery quality monitored appropriately

---

## Customisation Guidelines

### When to Customise DoD

1. **Project-Specific Requirements**: Add criteria for unique project needs
2. **Technology-Specific**: Add framework/language-specific quality gates
3. **Client Requirements**: Add client-mandated compliance or quality standards
4. **Lessons Learned**: Add criteria based on past project retrospectives

### How to Customise

```markdown
### Custom Section: [Your Category]

- [ ] **[Principle Code] Description**: Specific criterion for your project
- [ ] **Custom Requirement**: Additional project-specific requirement

**Rationale**: Explain why this custom criterion is needed **Owner**: Specify who validates this
criterion
```

### Example Customisations

**For AI/ML Projects**:

- [ ] **Model Performance**: Model accuracy ≥95% on validation set
- [ ] **Bias Detection**: Fairness metrics validated, bias mitigation applied
- [ ] **Explainability**: Model decisions explainable (SHAP, LIME)

**For Mobile Apps**:

- [ ] **App Store Ready**: App meets Apple/Google store guidelines
- [ ] **Offline Mode**: Core functionality works offline
- [ ] **Battery Impact**: Battery consumption within acceptable limits

**For Data Platforms**:

- [ ] **Data Quality**: Data validation rules pass ≥99.9%
- [ ] **Data Lineage**: Data lineage documented in metadata catalogue
- [ ] **SLA Met**: Data freshness and availability SLAs achieved

---

## Quality Gate Enforcement

### Automated Checks (CI/CD)

```yaml
# Example GitHub Actions quality gate
quality_gates:
  - linting: 'All linters must pass'
  - unit_tests: '≥80% coverage required'
  - integration_tests: '≥70% coverage required'
  - security_scan: 'No critical vulnerabilities'
  - build: 'Clean build required'
```

### Manual Reviews

- **Code Review**: At least 1 approver required (2 for critical changes)
- **Architecture Review**: Architect approval for ADR-worthy changes
- **Security Review**: Security team review for authentication/authorisation changes
- **UX Review**: Design team review for user-facing changes

### Escalation Process

**If DoD Not Met**:

1. **Document**: Clearly document which criteria are not met and why
2. **Risk Assessment**: Assess risk of proceeding without meeting criteria
3. **Stakeholder Decision**: Product Owner decides: delay, accept risk, or descope
4. **Technical Debt**: If accepted, create technical debt story in backlog
5. **Retrospective**: Discuss in sprint retrospective to prevent recurrence

---

## Integration with Agile Ceremonies

### Sprint Planning

- Review Story-Level DoD with team
- Ensure all stories have clear acceptance criteria aligned with DoD
- Estimate effort including time to meet DoD

### Daily Standup

- Blockers preventing DoD completion raised immediately
- Team collaborates to unblock DoD-related issues

### Sprint Review

- Demo only features that meet Story-Level DoD
- Validate Sprint-Level DoD criteria with stakeholders

### Sprint Retrospective

- Review DoD effectiveness
- Propose improvements to DoD criteria
- Update DoD template based on learnings

---

## Related Templates

- **User Story Template**: `${CLAUDE_PLUGIN_ROOT}/skills/backlog-management/resources/user-story-template.md`
- **Sprint Planning Template**:
  `${CLAUDE_PLUGIN_ROOT}/skills/sprint-delivery/resources/sprint-planning-template.md`
- **Sprint Retrospective Template**:
  `${CLAUDE_PLUGIN_ROOT}/skills/sprint-delivery/resources/sprint-retrospective-template.md`
- **ADR Template**: `${CLAUDE_PLUGIN_ROOT}/skills/architecture-documentation/resources/adr-template.md`

---

**Template Status**: ✅ Active | Production Ready **Compliance**: Adaptable to project-specific
quality, compliance, and governance standards **Maintenance**: Review quarterly, update based on
retrospective insights

---

_This template supports quality excellence, continuous improvement, and maintainable delivery
practices._
