# Security Review Checklist

A reusable, domain-by-domain application-security review checklist bundled with the
`gd-security:security-analyzer` skill. Work through each domain against the target system; record severity,
CVSS score, and business impact for every finding, and pair each finding with developer-friendly
remediation.

## How to Use

1. Scope the target (web app, API, microservice, mobile, cloud infrastructure).
2. Walk each domain below; mark each item pass / fail / not-applicable.
3. For every failure, capture: location, severity, CVSS vector, business impact, remediation.
4. Map findings to the requested compliance framework (OWASP, PCI-DSS, HIPAA, SOX, GDPR, SOC2, ISO
   27001, NIST CSF).

## 1. OWASP Top 10

- [ ] Broken access control , vertical and horizontal privilege escalation, IDOR, forced browsing.
- [ ] Cryptographic failures , data exposed in transit or at rest, weak or missing encryption.
- [ ] Injection , SQL, NoSQL, OS command, LDAP, and ORM injection across all input vectors.
- [ ] Insecure design , missing threat model, unsafe defaults, absent rate limiting.
- [ ] Security misconfiguration , default credentials, verbose errors, unnecessary features enabled.
- [ ] Vulnerable and outdated components , unpatched dependencies, end-of-life libraries.
- [ ] Identification and authentication failures , weak credential, session, and recovery flows.
- [ ] Software and data integrity failures , unsigned updates, insecure deserialisation, CI/CD
      tampering.
- [ ] Security logging and monitoring failures , missing audit trail, no alerting on auth events.
- [ ] Server-side request forgery (SSRF) , unvalidated outbound requests to internal resources.

## 2. Authentication & Session

- [ ] JWT validation , signature verification, algorithm pinning (no `none`), expiry and audience
      checks.
- [ ] OAuth2 / OIDC flows , correct grant type, PKCE for public clients, state parameter.
- [ ] SAML , signature validation, replay protection, audience restriction.
- [ ] Session management , secure cookie flags (HttpOnly, Secure, SameSite), idle and absolute
      timeout, rotation on privilege change.
- [ ] Credential storage , strong adaptive hashing (Argon2/bcrypt/scrypt), no plaintext or
      reversible storage.
- [ ] Multi-factor and account-recovery flows , no privilege escalation via recovery.

## 3. Input Validation & Output Encoding

- [ ] Server-side validation on every input vector (body, query, headers, cookies, files).
- [ ] Parameterised queries / prepared statements , no string-concatenated SQL.
- [ ] XSS mitigation , context-aware output encoding, CSP as defence in depth.
- [ ] Command-injection prevention , no shelling out with unsanitised input.
- [ ] File-upload validation , type, size, and content checks; safe storage location.

## 4. Cryptography

- [ ] Encryption in transit , TLS 1.2+ only, strong cipher suites, valid certificate chain.
- [ ] Encryption at rest , data classification drives encryption; managed keys.
- [ ] Key management , rotation, secure storage (KMS/vault), no keys in source or config.
- [ ] No deprecated algorithms , reject MD5, SHA1, DES, RC4.
- [ ] Timing-attack resistance for comparisons of secrets and tokens.

## 5. Security Headers & CORS

- [ ] `Content-Security-Policy` present and restrictive.
- [ ] `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options` / frame-ancestors.
- [ ] `Referrer-Policy` and `Permissions-Policy` set appropriately.
- [ ] CORS , explicit allow-list of origins, no wildcard with credentials.

## 6. Compliance & Evidence

- [ ] SOC2 control evidence captured with audit trail.
- [ ] ISO 27001 ISMS controls validated.
- [ ] PCI-DSS / HIPAA / GDPR data-handling requirements verified where in scope.
- [ ] Regulatory audit trail generated and retained.

## Finding Record (template)

```
Finding: <short title>
Location: <file / endpoint / component>
Severity: <low | medium | high | critical>
CVSS: <vector string and score>
Business impact: <data exposed / systems affected / regulatory exposure>
Remediation: <concrete, developer-friendly fix with secure code example>
Status: <open | remediated | accepted-risk>
```
