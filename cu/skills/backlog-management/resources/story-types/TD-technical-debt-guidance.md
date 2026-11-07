# TD - Technical Debt Story Type Guidance

**Story Type**: Technical Debt | **Prefix**: TD-NNN | **Version**: 1.2.0 | **Last Updated**:
2026-05-07

---

## Progress Update Block

Technical debt stories should include a **collapsible progress update callout** immediately after
the YAML frontmatter and before the story heading or overview content.

### Recommended Format

```markdown
> [!note]- Progress updates
>
> - **2026-05-07**: Debt item tracked and ready for remediation planning.
> - **2026-05-06**: Architectural or quality impact clarified.
> - **2026-05-05**: Debt item created and remediation scope recorded.
```

### Usage Guidance

- Use the collapsible callout syntax: `[!note]-`
- Focus on debt identification, impact clarification, remediation planning, and active cleanup
- Keep the wording evidence-based and avoid overstating implementation progress

---

## Definition

**Technical Debt**: Technical improvements, refactoring, or remediation work that doesn't deliver
immediate user-facing value but is critical for long-term system health, maintainability, and
velocity.

---

## Purpose

Address code quality, architecture, testing, or documentation issues that accumulate over time and
create drag on development velocity or increase maintenance burden.

---

## When to Use TD Stories

- **Code quality** issues (complexity, duplication, code smells)
- **Architecture** improvements (modularisation, decoupling)
- **Testing gaps** (missing unit/integration tests, low coverage)
- **Documentation debt** (missing or outdated docs)
- **Security debt** (non-critical vulnerabilities, hardening)
- **Dependency upgrades** (outdated libraries,frameworks)
- **Performance optimisation** (not caused by bugs)

---

## Required YAML Fields

```yaml
---
story_id: TD-055
story_type: technical_debt
title: 'Refactor authentication module for maintainability'
debt_category: code_quality # code_quality|architecture|testing|documentation|security
debt_impact: maintainability # productivity|maintainability|scalability|security
debt_age_days: 45 # calculated automatically or manually set
priority: Medium
story_points: 8
status: Draft
created: 2025-01-10
last_modified: 2025-01-25
---
```

---

## Examples

### Example 1: Code Quality Debt

```markdown
---
story_id: TD-055
story_type: technical_debt
title: 'Refactor authentication module for maintainability'
debt_category: code_quality
debt_impact: maintainability
debt_age_days: 45
priority: Medium
story_points: 8
---

## Technical Debt Description

**Current State**:

- Authentication module is 800-line monolithic file
- Cyclomatic complexity: 28 (target: <10)
- No unit tests (0% coverage)
- Duplicated password hashing logic in 4 places

**Impact**:

- New authentication features take 2× longer to implement
- High bug rate (6 auth bugs in last quarter)
- Difficult to onboard new developers

**Proposed Improvement**:

- Extract password service, token service, session service
- Reduce complexity to <10 per method
- Achieve 80% test coverage
- Eliminate code duplication

**Business Value**:

- 50% faster authentication feature delivery
- 70% reduction in auth-related bugs (projected)
- Improved developer velocity and satisfaction
```

### Example 2: Testing Debt

```markdown
---
story_id: TD-022
story_type: technical_debt
title: 'Add unit tests for payment processing (current coverage 35%)'
debt_category: testing
debt_impact: security
debt_age_days: 120
priority: High
---

## Technical Debt Description

**Current State**:

- Payment module has only 35% unit test coverage
- Critical paths (refunds, chargebacks) untested
- Integration tests flaky and slow (20min execution)

**Impact**:

- Payment bugs frequently reach production
- Developers afraid to refactor payment code
- Regression testing relies on manual QA (bottleneck)

**Proposed Improvement**:

- Increase unit test coverage to 85%
- Add tests for all critical payment paths
- Mock external payment gateway for fast tests
- Implement contract tests for gateway integration

**Business Value**:

- Reduced payment bugs (currently 30% of production incidents)
- Faster, safer payment feature development
- Reduced manual QA burden (3 days → 1 day per release)
```

### Example 3: Architecture Debt (legacy integration context)

```markdown
---
story_id: TD-070
story_type: technical_debt
title: 'Refactor legacy API integration layer for maintainability'
debt_category: architecture
debt_impact: maintainability
debt_age_days: 180
priority: High
---

## Technical Debt Description

**Current State**:

- Anti-Corruption Layer tightly coupled to legacy backend services
- No clear separation between API transformation and business logic
- Direct database queries mixed with REST endpoint handlers
- Difficult to test API layer in isolation

**Impact**:

- New API endpoints take 3× longer to implement
- Changes to legacy backend require API layer modifications
- Cannot easily mock legacy system for testing
- Risk of data inconsistency between new and legacy systems

**Proposed Improvement**:

- Implement clean Anti-Corruption Layer pattern
- Separate API transformation from business logic
- Create repository pattern for legacy data access
- Add comprehensive integration tests with mocked legacy backend

**Project Context**:

- Legacy backend must remain operational during migration
- New web frontend requires clean REST APIs
- Delivery standards emphasise maintainability and testability
- Compliance requirements demand clear data access patterns

**Business Value**:

- 50% faster API endpoint development
- Reduced risk of data inconsistency
- Easier testing and quality assurance
- Foundation for eventual legacy system replacement
```

---

## Debt Categories & Impact

### Debt Categories

- **code_quality**: Complexity, duplication, code smells
- **architecture**: Structural issues, tight coupling, poor modularity
- **testing**: Missing tests, low coverage, flaky tests
- **documentation**: Missing/outdated docs, unclear APIs
- **security**: Non-critical vulnerabilities, hardening gaps

### Debt Impact

- **productivity**: Slows feature delivery, increases development friction
- **maintainability**: Difficult to change, high bug rate, onboarding burden
- **scalability**: Performance bottlenecks, resource inefficiency
- **security**: Vulnerability risk, compliance gaps

---

## Prioritisation Framework

### High Priority TD

- **Productivity blockers** (3× development slowdown)
- **High bug rate** correlation (>5 bugs/quarter in module)
- **Security/compliance** implications
- **Aging debt** (>90 days) affecting critical paths

### Medium Priority TD

- **Moderate productivity impact** (1.5-2× slowdown)
- **Maintainability concerns** (complex, hard to change)
- **Testing gaps** in non-critical areas
- **Documentation** for public APIs

### Low Priority TD

- **Minor code quality** issues
- **Nice-to-have refactoring**
- **Documentation** for internal utilities
- **Non-blocking** dependency upgrades

---

## Anti-Patterns

### ❌ Perfectionism Debt

**Wrong**: TD-100: "Rewrite entire codebase in new framework" **Right**: Incremental improvements
with measurable impact

### ❌ Debt Without Business Justification

**Wrong**: "Code should be cleaner" (vague) **Right**: Quantify impact: "40% slower feature
delivery, 60% higher bug rate"

### ❌ Infinite Debt Accumulation

**Wrong**: Never prioritising TD, always "too busy with features" **Right**: Allocate 15-20% of
sprint capacity to TD reduction

---

## Related Story Types

**TD spawned from**:

- **US**: Rushed delivery accumulates debt
- **BUG**: Root cause reveals systemic debt
- **EP**: Large initiative creates architectural debt

**TD prevents**:

- **BUG**: Better code quality reduces defects
- **SEC**: Addressing security debt prevents vulnerabilities

---

## Project Considerations

### Legacy System Integration

- **Anti-Corruption Layer**: Technical debt often accumulates at the boundary between a new frontend
  and legacy backend services
- **Data Transformation**: Debt in mapping between legacy data models and modern REST APIs
- **Session Management**: IAM integration complexity can create architectural debt

### Technology Stack Debt

- **Frontend Framework**: Keep the primary frontend framework current enough to avoid upgrade debt
- **Component Library**: Ensure shared UI libraries remain compatible with the chosen framework
- **Design System**: Custom theming or token layers can create maintainability debt

### Quality Debt Categories

- **Test Coverage**: Use project quality targets and track debt when coverage drops materially
- **API Documentation**: OpenAPI specs must stay synchronised with implementation
- **Accessibility**: WCAG 2.1 AA compliance debt if not addressed during development

### Debt Prioritisation

- **User-Facing Impact**: Debt affecting critical user journeys takes priority
- **Integration Risk**: Debt at legacy system boundaries is higher risk
- **Compliance Impact**: Debt affecting regulated obligations requires urgent attention

---

## References

- **Story Type System**: See [story-types/README.md](README.md) for the complete type reference
- **Technical Debt Dashboard**: `roadmap/dashboards/technical-debt-registry.md` (create when needed)
- **Related Types**: [US](US-user-story-guidance.md), [BUG](BUG-defect-guidance.md),
  [SEC](SEC-security-guidance.md)
- **Memory Bank**: `docs-copper/memory-bank/` for project context

---

_TD-technical-debt-guidance.md | Version 1.2.0 | Last Updated: 2026-05-07 | COPPER Project
Documentation_
