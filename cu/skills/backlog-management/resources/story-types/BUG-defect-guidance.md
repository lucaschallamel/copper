# BUG - Defect Story Type Guidance

**Story Type**: Defect | **Prefix**: BUG-NNN | **Version**: 1.0.0 | **Last Updated**: 2025-10-29

---

## Definition

**Defect**: Unintended behaviour in production or test environments requiring remediation.
Represents functional defects, performance degradation, or data integrity issues where the system
doesn't meet requirements or user expectations.

---

## When to Use BUG Stories

Use the Defect story type when:

- **Production incidents** requiring immediate attention
- **Functional defects** where system doesn't meet requirements
- **Performance degradation** below acceptable thresholds
- **Data integrity issues** or corruption
- **Regression defects** from recent changes
- **User-reported issues** with existing functionality

---

## Required YAML Fields

```yaml
---
story_id: BUG-042
story_type: bug
title: 'Authentication fails after password reset'
severity: high # critical|high|medium|low
affected_version: '2.5.1' # version where bug was found
reproduction_steps:
  '1. Request password reset 2. Click email link 3. Set new password 4. Attempt login - fails'
root_cause: 'Session cookie not invalidated after password reset'
environment: production # production|staging|test|dev
priority: High
story_points: 5
status: In Progress
created: 2025-01-25
last_modified: 2025-01-26
---
```

### Field Descriptions

- **severity**: Impact classification (Critical > High > Medium > Low)
- **affected_version**: Version where bug was discovered
- **reproduction_steps**: Step-by-step instructions to reproduce
- **root_cause**: Technical analysis of underlying issue
- **environment**: Where bug occurs (production, staging, test, dev)

---

## Bug Template Structure

```markdown
# Bug: [Issue Description]

## Severity: [Critical/High/Medium/Low]

## Environment

Production / Staging / Test / Dev

## Reproduction Steps

1. [Prerequisite state or setup]
2. [Action taken by user]
3. [Observed incorrect behaviour]

## Expected Behaviour

[What should happen according to requirements]

## Actual Behaviour

[What actually happens - the bug]

## Root Cause

[Technical analysis of why this occurred]

- Component/module affected
- Code location (file:line if known)
- Underlying technical issue

## Impact Assessment

- **Users Affected**: [Percentage or number]
- **Business Impact**: [Revenue loss, user experience, reputation]
- **Workaround Available**: [Yes/No - describe if yes]

## Fix Strategy

[Remediation approach and testing plan]

- Proposed technical solution
- Testing approach to verify fix
- Regression testing scope

## Verification Criteria

- [ ] Bug no longer reproducible in fix branch
- [ ] Automated test added to prevent regression
- [ ] Manual QA verification completed
- [ ] No new bugs introduced by fix
```

---

## Severity Guidelines

### Critical (Fix within 24h)

- **System down** or completely unavailable
- **Data loss** or corruption affecting multiple users
- **Security breach** or vulnerability actively exploited
- **Revenue-blocking** issue preventing transactions
- **Legal/compliance** violation requiring immediate fix

**Example**: "Payment processing completely broken - all transactions failing"

### High (Fix within 3 days)

- **Major functionality broken** for significant user segment
- **Significant user impact** but workaround available
- **Performance degradation** making system barely usable
- **Data integrity issue** affecting subset of users
- **Key business process** disrupted

**Example**: "Login fails for users with special characters in email - affects 15% of users"

### Medium (Fix within 1 week)

- **Minor functionality issue** with workaround
- **Cosmetic issues** affecting user experience
- **Edge case scenarios** rarely encountered
- **Non-critical performance** issues
- **Minor data inconsistencies**

**Example**: "Date picker doesn't highlight current date - users can still select dates"

### Low (Fix in next release)

- **Cosmetic issues** with no functional impact
- **Nice-to-have improvements** to error messages
- **Documentation errors** or unclear help text
- **Minor UI inconsistencies**

**Example**: "Button alignment slightly off in Firefox on Windows 7"

---

## Examples

### Example 1: Critical Production Bug

```markdown
---
story_id: BUG-001
story_type: bug
title: 'Memory leak in payment processing service'
severity: critical
affected_version: '3.1.2'
reproduction_steps:
  'Service runs normally but memory usage grows 10MB/hour. After 72h, service OOM crashes.'
root_cause: 'Database connections not properly closed in error handling path'
environment: production
priority: High
story_points: 8
status: Done
---

# Bug: Memory Leak in Payment Processing Service

## Severity: Critical

## Environment

Production

## Reproduction Steps

1. Deploy payment service v3.1.2 to production
2. Monitor memory usage over 48-72 hours
3. Observe steady memory growth (~10MB/hour)
4. After ~72 hours, service crashes with OutOfMemoryError

## Expected Behaviour

Memory usage should remain stable under normal load (±5% variance)

## Actual Behaviour

Memory grows linearly until service crashes, requiring restart

## Root Cause

Database connection leak in error handling path:

- File: `PaymentProcessor.java:245`
- Issue: Exception thrown before connection.close() in try block
- Connections accumulate in pool, never released
- Eventually exhaust available memory

## Impact Assessment

- **Users Affected**: All payment attempts after crash (100% during downtime)
- **Business Impact**: Service downtime 15min avg, ~$50K revenue loss per incident
- **Workaround Available**: Manual service restart every 48 hours (unsustainable)

## Fix Strategy

1. Move connection.close() to finally block to ensure cleanup
2. Add connection pool monitoring and alerting
3. Implement circuit breaker for payment service
4. Add automated tests for resource cleanup

## Verification Criteria

- [x] 72-hour soak test shows stable memory usage
- [x] Automated test verifies connection cleanup in error scenarios
- [x] Production monitoring shows no memory growth after deployment
- [x] No new issues introduced
```

### Example 2: High Severity Bug (localisation context)

```markdown
---
story_id: BUG-015
story_type: bug
title: 'Currency amounts display incorrectly for values above 1000'
severity: high
affected_version: '1.0.0'
reproduction_steps:
  '1. Open an account with a balance above 1000 2. View the account summary 3. Amount displays
  without the expected thousand separator'
root_cause: 'Locale-specific number formatting is not properly configured'
environment: test
priority: High
story_points: 3
status: Done
---

# Bug: CHF Thousand Separator Missing

## Severity: High

## Environment

Test (pre-production)

## Reproduction Steps

1. Open an account with a value above 1,000
2. View the account summary
3. Check the formatted amount display
4. Amount displays as "1000.00" instead of "1'000.00" (Swiss format)

## Expected Behaviour

- CHF amounts should use Swiss thousand separator (apostrophe: ')
- Format: CHF 1'234'567.89 (not 1,234,567.89)

## Actual Behaviour

- Amounts display with no thousand separator: CHF 1234567.89
- Violates Swiss number formatting conventions
- User confusion during UAT testing

## Root Cause

- File: `currency.pipe.ts:42`
- Issue: Locale set to "en-US" instead of "fr-CH" (Swiss French)
- Swiss thousand separator (' apostrophe) not configured

## Impact Assessment

- **Users Affected**: All users viewing formatted monetary values
- **Business Impact**: Incorrect display of financial amounts
- **Workaround Available**: Users can interpret amounts, but UX degraded

## Fix Strategy

1. Update Angular locale configuration to "fr-CH"
2. Implement proper Swiss number formatting (apostrophe separator)
3. Add locale-specific display tests
4. QA validation with representative business users

## Localisation Context

- Swiss quality expectations demand precision in financial displays
- Swiss franc formatting: CHF 1'000.00 (apostrophe separator)
- Monetary values must be displayed accurately for user trust and reporting precision

## Verification Criteria

- [x] Amounts display with Swiss apostrophe separator
- [x] All account views updated (summary, detail, reports)
- [x] Tested with fr-CH locale
- [x] UAT approval from representative business users
```

---

## Anti-Patterns

### ❌ Bugs Without Reproduction Steps

**Wrong**: "Login sometimes doesn't work" **Right**: Detailed step-by-step reproduction with
environment details

### ❌ Feature Requests Disguised as Bugs

**Wrong**: BUG-100: "System should support dark mode" **Right**: Use US-NNN for new features, even
if users request as "missing functionality"

### ❌ Bugs Without Severity Classification

**Wrong**: No severity set, unclear prioritisation **Right**: Always classify severity using defined
guidelines

### ❌ Fixing Without Root Cause Analysis

**Wrong**: Apply quick patch without understanding underlying issue **Right**: Analyse root cause to
prevent recurrence and similar bugs

---

## Related Story Types

**BUG can reveal**:

- **TD (Technical Debt)**: Systemic issues requiring architectural fix
- **SEC (Security)**: Security vulnerabilities discovered via bug
- **RA (Risk Action)**: Critical bugs triggering risk mitigation

**BUG can be discovered during**:

- **US (User Story)**: Bugs found during feature implementation
- **EP (Epic)**: Defects identified during large initiative

---

## Story Type Transitions

### BUG → TD (Systemic Issue)

```
BUG-025: "User search returns duplicate results"
  → Root cause: Denormalised data model causes consistency issues
  → TD-040: "Normalise user data model to eliminate duplicates" (13 pts)
```

### BUG → SEC (Security Implication)

```
BUG-030: "File upload accepts executable files"
  → Security analysis reveals XSS vulnerability
  → SEC-018: "Implement file type validation and sandboxing" (CVSS 7.5)
```

---

## Project Considerations

### Quality Expectations

- Comprehensive root cause analysis expected (not just symptoms)
- Thorough testing before fix deployment
- Clear communication to affected users and support teams

### Regulatory Context

- Bugs affecting sensitive or regulated data may require audit trail documentation
- Security-related bugs should align with the applicable compliance framework
- Calculation or reporting bugs affecting business decisions require immediate attention

### Common Bug Categories

- **UI/UX Bugs**: Design system, component library, or responsiveness issues
- **API Bugs**: REST endpoint errors, data transformation issues
- **Integration Bugs**: ESB communication, IAM authentication
- **Data Bugs**: Sensitive data display, calculation errors, synchronisation defects

---

## References

- **Bug Template**: `${CLAUDE_PLUGIN_ROOT}/skills/backlog-management/resources/user-story-template.md` (owning
  skill) `cu:backlog-management` skill resource)
- **Related Types**: [TD](TD-technical-debt-guidance.md), [SEC](SEC-security-guidance.md),
  [RA](RA-risk-action-guidance.md)
- **Memory Bank**: `docs-copper/memory-bank/` for project context

---

_BUG-defect-guidance.md | Version 1.1.0 | Last Updated: 2025-01-23 | COPPER Project Documentation_
