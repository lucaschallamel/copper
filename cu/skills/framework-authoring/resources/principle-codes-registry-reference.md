---
title: Comprehensive Principle Codes Registry
version: '1.3.1'
last_updated: '2026-10-18'
maintained_by: 'Lucas Challamel'
---

# Comprehensive Principle Codes Registry

**Total Codes**: 73

> **This is the principle-code reference, on-demand.** It holds the compact glossary (code ->
> one-line definition for all 73 codes) and the full per-code Definition / Application / Examples /
> "Used in" maps plus the MECE, collision-detection and statistics analysis. Rule 06
> (`rules/06-principles-registry.rules.md`) is the always-on pointer to it (US-378 moved the
> glossary here; US-338 moved the expansion earlier).

This registry provides a comprehensive, MECE (Mutually Exclusive, Collectively Exhaustive) catalogue
of all principle codes used across the framework. Each code is uniquely defined, categorised, and
mapped to its usage across rules 00-07 (the compact glossary is below; Rule 06 points here).

---

## Compact glossary (moved from Rule 06 by US-378)

The one-line definition of every code, by category; the expanded entries follow. This glossary is
the source `curate_register.py` projects into the SAER core register.

### Category 1: Organisational Values (5 codes)

- **[DAR] Daring**: Bold thinking and the courage to challenge the status quo in data protection
- **[OPN] Openness**: Transparency, collaboration, and an open posture with clients and partners
- **[PER] Perseverance**: Sustained commitment to solving hard problems and seeing them through
- **[PRA] Pragmatism**: Practical, unintrusive solutions that fit real-world constraints
- **[RIG] Rigor**: Precision, quality, and auditability appropriate to regulated sectors

### Category 2: Core Development Principles (6 codes)

- **[SF] Simplicity First**: Always prioritise the simplest viable solution that meets requirements
- **[RP] Readability Priority**: Code must be immediately comprehensible to humans and AI systems
- **[DM] Dependency Minimalism**: Introduce new libraries only with explicit justification
- **[ISA] Industry Standards Adherence**: Follow established conventions (3-letter exception for
  clarity)
- **[SD] Strategic Documentation**: Document complex logic; avoid obvious comments
- **[TDT] Test-Driven Thinking**: Design all code for testability from initial implementation

### Category 3: Quality & Architecture Principles (8 codes)

- **[DRY] Don't Repeat Yourself**: Eliminate code duplication through reuse and extension
- **[CA] Clean Architecture**: Maintain formatted, logically structured code with SOLID principles
- **[REH] Robust Error Handling**: Comprehensive error handling for all edge cases
- **[CSD] Code Smell Detection**: Proactively identify refactoring opportunities
- **[MOD] Modularity Focus**: Prefer modular, reusable components over monolithic implementations
- **[ARC] Architecture Stability**: Avoid major changes unless explicitly requested
- **[IMP] Impact Analysis**: Consider affected methods and areas before changes
- **[PA] Performance Awareness**: Consider computational complexity and resource usage

### Category 4: Workflow & Organisation Principles (8 codes)

- **[ENV] Environment Awareness**: Code functions correctly across dev, test, production
- **[ORG] Organisational Clarity**: Maintain clean, well-organised codebase structure
- **[SCM] Script Management**: Avoid embedding one-time scripts in production files
- **[FOC] Focus on Relevant Code**: Work only on areas relevant to the task
- **[SCP] Scope Protection**: Do not touch code unrelated to the task
- **[TST] Test Coverage**: Write thorough tests for all major functionality
- **[AC] Atomic Changes**: Small, self-contained modifications for traceability
- **[CD] Commit Discipline**: Conventional commits with semantic versioning

### Category 5: Security & Compliance Principles (13 codes)

- **[SFT] Security-First Thinking**: Security-by-design, threat modelling, zero-trust architecture
- **[IV] Input Validation**: All external data must undergo comprehensive validation. Two facets:
  (a) syntactic/schema validation of inbound data (Rule 02); (b) provenance / trust-tier validation
  of untrusted content before it influences an action (Rule 07, Control 3)
- **[RM] Resource Management**: Properly close connections, free system resources
- **[CMV] Constants Over Magic Values**: Use descriptive named constants exclusively
- **[RL] Rate Limiting**: Implement rate limiting on ALL API endpoints
- **[RLS] Row Level Security**: Apply row-level security across all data access patterns
- **[CAP] CAPTCHA Integration**: Mandatory CAPTCHA on authentication routes
- **[WAF] Web Application Firewall**: Enable attack challenge mechanisms on WAF
- **[SPO] Secure Prohibited Operations**: Prior approval required for .env, secrets access
- **[QSR] Quarterly Security Review**: Comprehensive vulnerability assessment of dependencies
- **[PKV] Package Verification**: Prioritise signed or cryptographically verified packages
- **[DEH] Dependency Hygiene**: Remove unused/outdated dependencies promptly
- **[DCH] Dependency Change Documentation**: Document all dependency updates with rationale

### Category 6: AI/Agent Communication Principles (6 codes)

- **[RAT] Rule Application Tracking**: Tagging of rule applications (advisory annotation, not a
  mandatory gate , it aids traceability but is not a compliance signal)
- **[TR] Transparent Reasoning**: Explicit documentation of which rules influenced decisions
- **[EDC] Explanation Depth Control**: Adaptive detail scaling based on complexity
- **[AS] Alternative Suggestions**: Proactive offering of alternative approaches
- **[KBT] Knowledge Boundary Transparency**: Clear communication when exceeding capabilities
- **[CWM] Context Window Management**: Proactive management of AI context limitations

### Category 7: Microservices Patterns (27 codes - See Rule 05)

- **[MON]** Monolithic Architecture | **[MSA]** Microservice Architecture
- **[DBC]** Decompose by Business Capability | **[DSD]** Decompose by Subdomain
- **[RPI]** Remote Procedure Invocation | **[MSG]** Messaging
- **[CBR]** Circuit Breaker | **[SDC]** Service Discovery
- **[DPS]** Database per Service | **[SAG]** Saga
- **[OUT]** Transactional Outbox | **[DOM]** Domain Model
- **[TSF]** Transaction Script | **[AGG]** Aggregate
- **[DME]** Domain Event | **[EVS]** Event Sourcing
- **[APC]** API Composition | **[CQR]** CQRS
- **[APG]** API Gateway | **[BFF]** Backend for Frontend
- **[CDC]** Consumer-Driven Contract | **[SCT]** Service Component Test
- **[SVC]** Service per Container | **[SRL]** Serverless
- **[MSC]** Microservice Chassis | **[SMH]** Service Mesh
- **[STR]** Strangler Fig

---

**Definitions, applications, examples, per-rule "Used in" maps, and the MECE / collision /
statistics analysis for every code above:** the sections below.

## Purpose & Usage

**Format**: All principle codes use the format `**[CODE]**` in documentation and code **Scope**:
Framework-wide standard vocabulary for tagging decisions, requirements, and implementations
**Authority**: This file is the canonical home of the principle-code vocabulary (glossary and full
definitions); Rule 06 is the always-on pointer to it. **Integration**: Referenced by the Rule 06
code index and rules 00-07

---

## Registry Statistics

| Category                                | Code Count | Primary Rules            |
| --------------------------------------- | ---------- | ------------------------ |
| **Organisational Values**               | 5          | All rules                |
| **Core Development Principles**         | 6          | Rules 00, 02, 05         |
| **Quality & Architecture Principles**   | 8          | Rules 00, 01, 02, 04, 05 |
| **Workflow & Organisation Principles**  | 8          | Rules 01, 02, 03, 04, 05 |
| **Security & Compliance Principles**    | 13         | Rules 00, 02, 05         |
| **AI/Agent Communication Principles**   | 6          | Rules 03, 04             |
| **Microservices Architecture Patterns** | 27         | Rule 05                  |
| **TOTAL**                               | **73**     | -                        |

---

## Category 1: Organisational Values (5 codes)

**Purpose**: Core organisational values defining cultural identity and philosophy **Scope**:
Permeate all rules, decisions, and implementations **Origin**: Configured via Rule 00 and `/cu:init`
**Official Order**: Daring → Openness → Perseverance → Pragmatism → Rigor

### [DAR] Daring

**Definition**: Bold thinking and the courage to challenge the status quo in data protection
**Application**: Ambitious solution design, tackling hard regulated-data problems, conviction-led
decisions **Used in**: Rules 00-06 (not 07) **Examples**:

- Pursuing category-defining solutions
- Taking on the hardest data-protection challenges
- Backing technical conviction with action
- Proposing bold but auditable approaches

### [OPN] Openness

**Definition**: Transparency, collaboration, and an open posture with clients and partners
**Application**: Clear communication, open ecosystem collaboration, welcoming fresh perspectives
**Used in**: Rules 00-06 (not 07) **Examples**:

- Honest, transparent communication
- Open collaboration across editors, cloud providers, integrators
- "A fresh eye is an asset" - welcoming new perspectives
- Knowledge sharing within and across teams

### [PER] Perseverance

**Definition**: Sustained commitment to solving hard problems and seeing them through
**Application**: Follow-through from PoC to production, durability, long-horizon delivery **Used
in**: Rules 00, 01, 05, 06 **Examples**:

- Following through from proof-of-concept to production
- Staying the course through complex multi-year engagements
- Building durable, dependable solutions
- Iterative improvement until the problem is genuinely solved

### [PRA] Pragmatism

**Definition**: Practical, unintrusive solutions that fit real-world constraints **Application**:
Solve the actual problem without re-engineering apps/data models, production-first decisions **Used
in**: Rules 00, 04, 05, 06 **Examples**:

- Unintrusive integration (no re-engineering of existing systems)
- Favouring what works in production over theoretical purity
- Respecting business logic and operational reality
- Reusable, configuration-driven protection

### [RIG] Rigor

**Definition**: Precision, quality, and auditability appropriate to regulated sectors
**Application**: Verifiable compliant outcomes, high engineering/security standards, evidence-backed
claims **Used in**: Rules 00, 01, 03, 04, 06 **Examples**:

- Verifiable, auditable, compliant outcomes
- High engineering and security standards (ISO 27001 mindset)
- Substantiating claims with evidence and reports
- Peer review and quality gates

---

## Category 2: Core Development Principles (6 codes)

**Purpose**: Fundamental coding standards and development approach **Scope**: Code implementation,
design decisions, technical choices **Application**: Daily coding activities, architecture decisions

### [SF] Simplicity First

**Definition**: Always prioritise the simplest viable solution that meets requirements
**Application**: Implementation choices, architecture decisions, avoid over-engineering **Used in**:
Rules 00, 02, 05**Examples**:

- Prefer monolith over microservices when appropriate
- Avoid premature optimisation
- Simple configuration over complex frameworks
- Straightforward algorithms over clever code

### [RP] Readability Priority

**Definition**: Code must be immediately comprehensible to humans and AI systems **Application**:
Code style, naming conventions, structure clarity **Used in**: Rules 00, 02, 03, 04 **Examples**:

- Clear variable/function names
- Consistent formatting
- Logical code organisation
- Self-documenting code structure

### [DM] Dependency Minimalism

**Definition**: Introduce new libraries only with explicit justification **Application**: Package
management, dependency decisions, library selection **Used in**: Rules 00, 02, 05**Examples**:

- Dependency hygiene practices
- Quarterly dependency reviews
- Justification for new packages
- Removal of unused dependencies

### [ISA] Industry Standards Adherence

**Definition**: Follow established conventions (3-letter exception for clarity) **Application**:
Standards compliance, best practices, established patterns **Used in**: Rules 00, 02, 04,
05**Examples**:

- Twelve-Factor App methodology
- Conventional commits
- OpenAPI/Swagger specifications
- WCAG 2.1 AA standards

### [SD] Strategic Documentation

**Definition**: Document complex logic; avoid obvious comments **Application**: Documentation
decisions, comment quality, knowledge capture **Used in**: Rules 00, 02, 03, 04 **Examples**:

- Document "why" not "what"
- Complex algorithm explanations
- Architectural decision rationale
- Avoid redundant comments

### [TDT] Test-Driven Thinking

**Definition**: Design all code for testability from initial implementation **Application**: Code
design, test architecture, quality assurance **Used in**: Rules 00, 02, 05 **Examples**:

- Dependency injection for testability
- Mock-friendly interfaces
- Test coverage ≥80% unit, ≥70% integration
- Test-first development approach

---

## Category 3: Quality & Architecture Principles (8 codes)

**Purpose**: Code quality, architectural integrity, system design standards **Scope**: Architecture
decisions, code structure, quality maintenance **Application**: Design reviews, refactoring, quality
gates

### [DRY] Don't Repeat Yourself

**Definition**: Eliminate code duplication through reuse and extension **Application**: Code reuse,
abstraction, modularity **Used in**: Rules 00, 02, 04, 05**Examples**:

- Template reuse (Rule 04)
- Shared configuration patterns
- Common utility functions
- Inheritance and composition

### [CA] Clean Architecture

**Definition**: Maintain formatted, logically structured code with SOLID principles **Application**:
Architecture patterns, code organisation, design principles **Used in**: Rules 00, 02, 04,
05**Examples**:

- SOLID principles
- Separation of concerns
- Dependency inversion
- Clean code standards

### [REH] Robust Error Handling

**Definition**: Comprehensive error handling for all edge cases **Application**: Exception handling,
error propagation, failure recovery **Used in**: Rules 02, 05, 07**Examples**:

- Try-catch blocks for all external calls
- Graceful degradation
- Error logging and monitoring
- Circuit breaker patterns

### [CSD] Code Smell Detection

**Definition**: Proactively identify refactoring opportunities **Application**: Code review, static
analysis, technical debt management **Used in**: Rules 02**Examples**:

- Linting tools (Semgrep, MegaLinter)
- Code complexity analysis
- Duplication detection
- Pattern anti-pattern identification

### [MOD] Modularity Focus

**Definition**: Prefer modular, reusable components over monolithic implementations **Application**:
Component design, service boundaries, module organisation **Used in**: Rules 00, 02, 04,
05**Examples**:

- Microservices decomposition
- Pluggable components
- Module boundaries
- Reusable libraries

### [ARC] Architecture Stability

**Definition**: Avoid major changes unless explicitly requested **Application**: Refactoring
decisions, backward compatibility, change management **Used in**: Rules 02, 05**Examples**:

- Versioned APIs
- Deprecation strategies
- Migration paths
- Breaking change avoidance

### [IMP] Impact Analysis

**Definition**: Consider affected methods and areas before changes **Application**: Change impact
assessment, risk evaluation, dependency analysis **Used in**: Rules 02**Examples**:

- Dependency graph analysis
- Affected component identification
- Blast radius assessment
- Side effect prediction

### [PA] Performance Awareness

**Definition**: Consider computational complexity and resource usage **Application**: Algorithm
selection, resource optimisation, scalability planning **Used in**: Rules 02, 05**Examples**:

- Big-O analysis
- Resource profiling
- Caching strategies
- Horizontal scaling design

---

## Category 4: Workflow & Organisation Principles (8 codes)

**Purpose**: Development workflow, codebase organisation, process discipline **Scope**: Daily
workflows, organisational standards, process adherence **Application**: Git workflows, folder
structure, task management

### [ENV] Environment Awareness

**Definition**: Code functions correctly across dev, test, production **Application**: Environment
configuration, deployment strategies, parity **Used in**: Rules 01, 02, 04, 05 **Examples**:

- Environment-specific configuration
- Dev/prod parity >95%
- Cross-platform compatibility
- Environment variable usage

### [ORG] Organisational Clarity

**Definition**: Maintain clean, well-organised codebase structure **Application**: Folder structure,
file organisation, naming conventions **Used in**: Rules 01, 02, 03, 04, 05 **Examples**:

- Centralised documentation structure
- Protected folder structures
- Clear directory purposes
- Consistent naming patterns

### [SCM] Script Management

**Definition**: Avoid embedding one-time scripts in production files **Application**: Script
organisation, tooling separation, production cleanliness **Used in**: Rules 01, 02, 05 **Examples**:

- Scripts in dedicated /scripts/ folder
- Development tools separation
- Production code purity
- Build vs runtime distinction

### [FOC] Focus on Relevant Code

**Definition**: Work only on areas relevant to the task **Application**: Task scoping, change
isolation, attention management **Used in**: Rules 02, 03, 04 **Examples**:

- Atomic commits
- Task-specific changes only
- Avoid scope creep
- Context-aware modifications

### [SCP] Scope Protection

**Definition**: Do not touch code unrelated to the task **Application**: Change discipline,
unintended modification prevention **Used in**: Rules 02, 04 **Examples**:

- Protected folder enforcement (Rule 04)
- Change review for out-of-scope modifications
- Revert unrelated changes
- Explicit permission for exceptions

### [TST] Test Coverage

**Definition**: Write thorough tests for all major functionality **Application**: Testing standards,
coverage requirements, quality gates **Used in**: Rules 01, 02, 03, 05 **Examples**:

- ≥80% unit test coverage
- ≥70% integration test coverage
- Critical path e2e tests
- Test-first development

### [AC] Atomic Changes

**Definition**: Small, self-contained modifications for traceability **Application**: Commit
strategy, change management, review efficiency **Used in**: Rules 02, 05 **Examples**:

- One logical change per commit
- Reviewable commit sizes
- Revertible changes
- Clear commit boundaries

### [CD] Commit Discipline

**Definition**: Conventional commits with semantic versioning **Application**: Git workflow, version
management, changelog generation **Used in**: Rules 01, 02, 05 **Examples**:

- Conventional commit format
- Semantic versioning (MAJOR.MINOR.PATCH)
- Meaningful commit messages
- Commit message templates

---

## Category 5: Security & Compliance Principles (13 codes)

**Purpose**: Security-by-design, compliance standards, data protection **Scope**: Security
architecture, compliance requirements, risk management **Application**: Threat modelling, security
reviews, compliance audits

### [SFT] Security-First Thinking

**Definition**: Security-by-design, threat modelling, zero-trust architecture **Application**:
Architecture decisions, design reviews, security planning **Used in**: Rules 00, 02, 05,
07**Examples**:

- Zero-trust architecture
- Threat modelling sessions
- Security design reviews
- Defence in depth

### [IV] Input Validation

**Definition**: All external data must undergo comprehensive validation **Application**: API
endpoints, user input, external integrations **Used in**: Rules 00, 02, 05, 07**Examples**:

- Schema validation
- Type checking
- Whitelist validation
- Sanitisation before processing

### [RM] Resource Management

**Definition**: Properly close connections, free system resources **Application**: Database
connections, file handles, memory management **Used in**: Rules 02, 05, 07 **Examples**:

- Connection pooling
- Try-finally resource cleanup
- Memory leak prevention
- File handle closure

### [CMV] Constants Over Magic Values

**Definition**: Use descriptive named constants exclusively **Application**: Code readability,
maintainability, magic number elimination **Used in**: Rules 02, 05 **Examples**:

- Named constants for configuration
- Enum types for states
- Configuration files for values
- No hardcoded numbers/strings

### [RL] Rate Limiting

**Definition**: Implement rate limiting on ALL API endpoints **Application**: API protection, DoS
prevention, resource protection **Used in**: Rules 02, 05**Examples**:

- Request per second limits
- Token bucket algorithms
- User-based throttling
- Endpoint-specific limits

### [RLS] Row Level Security

**Definition**: Apply row-level security across all data access patterns **Application**: Database
security, data isolation, multi-tenancy **Used in**: Rules 00, 02**Examples**:

- PostgreSQL RLS policies
- User-based data filtering
- Tenant isolation
- Data access control

### [CAP] CAPTCHA Integration

**Definition**: Mandatory CAPTCHA on authentication routes **Application**: Bot prevention,
authentication security, abuse prevention **Used in**: Rules 02, 05 **Examples**:

- reCAPTCHA on login
- CAPTCHA on registration
- Rate limiting + CAPTCHA combination
- Invisible CAPTCHA options

### [WAF] Web Application Firewall

**Definition**: Enable attack challenge mechanisms on WAF **Application**: Infrastructure security,
attack prevention, traffic filtering **Used in**: Rules 02, 05 **Examples**:

- Cloudflare WAF
- AWS WAF rules
- OWASP Top 10 protection
- DDoS mitigation

### [SPO] Secure Prohibited Operations

**Definition**: Prior approval required for .env, secrets access **Application**: Secrets
management, sensitive operations, approval workflows **Used in**: Rules 02, 05, 07 **Examples**:

- .env file access restrictions
- Secret rotation workflows
- Approval gates for sensitive changes
- Audit logging for secret access

### [QSR] Quarterly Security Review

**Definition**: Comprehensive vulnerability assessment of dependencies **Application**: Dependency
security, vulnerability management, patch cycles **Used in**: Rules 02 **Examples**:

- Quarterly dependency audits
- Vulnerability scanning (Snyk, Dependabot)
- Security patch application
- CVE monitoring

### [PKV] Package Verification

**Definition**: Prioritise signed or cryptographically verified packages **Application**: Supply
chain security, package integrity, trust verification **Used in**: Rules 02 **Examples**:

- GPG signature verification
- Checksum validation
- Official repository sources only
- Package lock file integrity

### [DEH] Dependency Hygiene

**Definition**: Remove unused/outdated dependencies promptly **Application**: Dependency management,
technical debt reduction, attack surface minimisation **Used in**: Rules 02 **Examples**:

- Unused dependency removal
- Version upgrade cycles
- Deprecation tracking
- Minimal dependency footprint

### [DCH] Dependency Change Documentation

**Definition**: Document all dependency updates with rationale **Application**: Change tracking,
upgrade justification, audit trail **Used in**: Rules 02 **Examples**:

- CHANGELOG entries for dependency updates
- Rationale for version changes
- Breaking change documentation
- Migration guides for major updates

---

## Category 6: AI/Agent Communication Principles (6 codes)

**Purpose**: AI agent behaviour, communication standards, context management **Scope**: Agent
interactions, reasoning transparency, knowledge boundaries **Application**: Agent development,
prompt engineering, context optimisation

### [RAT] Rule Application Tracking

**Definition**: Mandatory tagging of all rule applications **Application**: Traceability, audit
trails, decision documentation **Used in**: Rules 03 **Examples**:

- Tag all decisions with principle codes
- Track which rules influenced choices
- Audit trail for AI decisions
- Compliance verification

### [TR] Transparent Reasoning

**Definition**: Explicit documentation of which rules influenced decisions **Application**: AI
explainability, decision rationale, trust building **Used in**: Rules 03 **Examples**:

- Document reasoning chains
- Cite applicable rules
- Explain decision factors
- Provide alternatives considered

### [EDC] Explanation Depth Control

**Definition**: Adaptive detail scaling based on complexity **Application**: Response formatting,
user experience, clarity optimisation **Used in**: Rules 03 **Examples**:

- Brief explanations for simple tasks
- Detailed breakdowns for complex decisions
- Progressive disclosure
- Context-aware verbosity

### [AS] Alternative Suggestions

**Definition**: Proactive offering of alternative approaches **Application**: Solution diversity,
best practice sharing, option presentation **Used in**: Rules 03 **Examples**:

- Multiple implementation options
- Trade-off analysis
- Best practice alternatives
- Pros/cons of each approach

### [KBT] Knowledge Boundary Transparency

**Definition**: Clear communication when exceeding capabilities **Application**: Honesty, limitation
acknowledgement, escalation triggers **Used in**: Rules 03 **Examples**:

- Acknowledge uncertainty
- Request clarification when needed
- Escalate beyond capabilities
- Avoid hallucination

### [CWM] Context Window Management

**Definition**: Proactive management of AI context limitations **Application**: Token optimisation,
context pruning, memory management **Used in**: Rules 03 **Examples**:

- Memory bank file updates
- Context compression techniques
- Relevant information prioritisation
- Token budget awareness

---

## Category 7: Microservices Architecture Patterns (27 codes)

**Purpose**: Microservices design patterns from Chris Richardson's "Microservices Patterns"
**Scope**: Service architecture, decomposition, communication, data management **Application**:
Architecture decisions, service design, distributed systems **Primary Rule**: Rule 05 - Architecture
Guidelines

### Application Architecture Patterns (2 codes)

#### [MON] Monolithic Architecture

**Definition**: Single-tier, tightly-coupled application architecture **Application**: Small
applications, MVPs, initial development **Used in**: Rule 05 **When to Use**: Simple applications,
team <10 developers, low complexity

#### [MSA] Microservice Architecture

**Definition**: Distributed, loosely-coupled service-oriented architecture **Application**: Large
systems, independent deployment, team autonomy **Used in**: Rule 05 **When to Use**: Complex
applications, multiple teams, high scalability needs

### Service Decomposition Patterns (2 codes)

#### [DBC] Decompose by Business Capability

**Definition**: Service boundaries aligned with business capabilities **Application**:
Business-driven service design, stable boundaries **Used in**: Rule 05 **Examples**: Order
Management Service, Customer Service, Payment Service

#### [DSD] Decompose by Subdomain

**Definition**: Service boundaries aligned with DDD subdomains **Application**: Domain-driven
design, ubiquitous language, bounded contexts **Used in**: Rule 05 **Examples**: Core, Supporting,
Generic subdomains

### Inter-Service Communication Patterns (4 codes)

#### [RPI] Remote Procedure Invocation

**Definition**: Synchronous request/response communication (REST, gRPC) **Application**: Immediate
response required, query operations **Used in**: Rule 05 **Examples**: REST APIs, gRPC calls, HTTP
requests

#### [MSG] Messaging

**Definition**: Asynchronous message-based communication **Application**: Event notification, loose
coupling, eventual consistency **Used in**: Rule 05 **Examples**: Kafka, RabbitMQ, AWS SQS, Azure
Service Bus

#### [CBR] Circuit Breaker

**Definition**: Prevent cascading failures through fault tolerance **Application**: Resilience,
graceful degradation, fault isolation **Used in**: Rule 05 **Quality Standard**: All synchronous
inter-service calls require circuit breakers

#### [SDC] Service Discovery

**Definition**: Dynamic service location and registration **Application**: Load balancing, service
registry, health checks **Used in**: Rule 05 **Examples**: Consul, Eureka, Kubernetes DNS

### Data Management Patterns (3 codes)

#### [DPS] Database per Service

**Definition**: Each microservice owns its database **Application**: Data isolation, independent
schema evolution, autonomy **Used in**: Rule 05 **Quality Standard**: Database per service pattern
mandatory

#### [SAG] Saga

**Definition**: Distributed transaction management across services **Application**: Multi-service
workflows, compensation logic, consistency **Used in**: Rule 05 **Quality Standard**: Distributed
transactions via saga pattern only

#### [OUT] Transactional Outbox

**Definition**: Reliable event publishing with database transactions **Application**: Event
sourcing, guaranteed message delivery, atomicity **Used in**: Rule 05 **Examples**: Outbox table
pattern, change data capture

### Business Logic Patterns (5 codes)

#### [DOM] Domain Model

**Definition**: Object-oriented domain model with business logic **Application**: Complex business
rules, rich domain model, OOP **Used in**: Rule 05 **Examples**: Entities, value objects, domain
services

#### [TSF] Transaction Script

**Definition**: Procedural code organised by transaction **Application**: Simple business logic,
CRUD operations **Used in**: Rule 05 **Examples**: Simple scripts, straightforward workflows

#### [AGG] Aggregate

**Definition**: DDD aggregate pattern for consistency boundaries **Application**: Transactional
consistency, entity clusters, invariant enforcement **Used in**: Rule 05 **Examples**: Order
aggregate, Customer aggregate

#### [DME] Domain Event

**Definition**: Events representing business occurrences **Application**: Event-driven architecture,
loose coupling, audit trail **Used in**: Rule 05 **Examples**: OrderPlaced, PaymentProcessed,
CustomerRegistered

#### [EVS] Event Sourcing

**Definition**: Store state changes as event sequence **Application**: Audit trail, temporal
queries, event replay **Used in**: Rule 05 **Examples**: Event store, event replay, temporal queries

### Query Patterns (2 codes)

#### [APC] API Composition

**Definition**: Combine data from multiple services in API layer **Application**: Query aggregation,
data joining, service orchestration **Used in**: Rule 05 **Examples**: Aggregation gateway,
composite queries

#### [CQR] CQRS (Command Query Responsibility Segregation)

**Definition**: Separate read and write models **Application**: Performance optimisation,
scalability, different consistency models **Used in**: Rule 05 **Examples**: Write model (commands),
Read model (queries)

### External API Patterns (2 codes)

#### [APG] API Gateway

**Definition**: Single entry point for client requests **Application**: Request routing,
authentication, rate limiting, API aggregation **Used in**: Rule 05 **Examples**: Kong, Apigee, AWS
API Gateway, Azure API Management

#### [BFF] Backend for Frontend

**Definition**: Specialised backend per client type **Application**: Client-specific optimisation,
API adaptation **Used in**: Rule 05 **Examples**: Mobile BFF, Web BFF, IoT BFF

### Testing Patterns (2 codes)

#### [CDC] Consumer-Driven Contract

**Definition**: Consumer defines service contract expectations **Application**: Contract testing,
API compatibility, integration testing **Used in**: Rule 05 **Examples**: Pact, Spring Cloud
Contract

#### [SCT] Service Component Test

**Definition**: Test service in isolation with test doubles **Application**: Service-level testing,
mock external dependencies **Used in**: Rule 05 **Examples**: Component tests, contract tests

### Deployment Patterns (4 codes)

#### [SVC] Service per Container

**Definition**: Each service instance in separate container **Application**: Isolation, resource
management, deployment flexibility **Used in**: Rule 05 **Examples**: Docker containers, Kubernetes
pods

#### [SRL] Serverless

**Definition**: Function-as-a-service deployment **Application**: Event-driven, auto-scaling,
pay-per-use **Used in**: Rule 05 **Examples**: AWS Lambda, Azure Functions, Google Cloud Functions

#### [MSC] Microservice Chassis

**Definition**: Reusable framework for common service functionality **Application**: Cross-cutting
concerns, standardisation, scaffolding **Used in**: Rule 05 **Examples**: Spring Boot, Micronaut,
Quarkus

#### [SMH] Service Mesh

**Definition**: Infrastructure layer for service-to-service communication **Application**: Traffic
management, security, observability **Used in**: Rule 05 **Examples**: Istio, Linkerd, Consul
Connect

### Refactoring Patterns (1 code)

#### [STR] Strangler Fig

**Definition**: Incrementally migrate from monolith to microservices **Application**: Legacy
modernisation, gradual migration, risk mitigation **Used in**: Rule 05 **Examples**: Façade-based
migration, incremental extraction

---

## MECE Analysis

### Mutually Exclusive Verification

**Analysis**: Each principle code has a UNIQUE definition and purpose. No overlaps detected.

**Potential Overlaps Addressed**:

1. **[SD] vs [RP]**: Strategic Documentation focuses on _what_ to document, Readability Priority on
   _how_ code reads
2. **[MOD] vs [DRY]**: Modularity is about structure, DRY about duplication elimination
3. **[OPN] vs [SFT]**: Commitment is cultural value, Security-First is technical principle
4. **[ORG] vs [ENV]**: Organisation is structural, Environment is cross-environment functionality
5. **[DPS] vs [DBC]**: Database per Service is data pattern, Decompose by Business Capability is
   decomposition strategy

**Result**: ✅ All 73 codes are mutually exclusive

### Collectively Exhaustive Verification

**Coverage Analysis** across software development lifecycle:

| Lifecycle Phase    | Covered By                              | Gap Analysis |
| ------------------ | --------------------------------------- | ------------ |
| **Planning**       | DAR, OPN, PER, PRA, RIG                 | ✅ Complete  |
| **Design**         | SF, CA, MOD, ARC, IMP, DBC, DSD, DOM    | ✅ Complete  |
| **Implementation** | SF, RP, DM, ISA, SD, TDT, DRY, REH, CSD | ✅ Complete  |
| **Testing**        | TDT, TST, CDC, SCT                      | ✅ Complete  |
| **Security**       | SFT, IV, RM, RL, RLS, CAP, WAF, SPO     | ✅ Complete  |
| **Deployment**     | ENV, CD, SVC, SRL, MSC, SMH, STR        | ✅ Complete  |
| **Operations**     | PA, RM, CBR, SDC, APG                   | ✅ Complete  |
| **Maintenance**    | DEH, DCH, QSR, PKV, FOC, SCP            | ✅ Complete  |
| **Documentation**  | SD, ORG, RAT, TR                        | ✅ Complete  |
| **Collaboration**  | OPN, RIG, AS, KBT                       | ✅ Complete  |

**Result**: ✅ Framework is collectively exhaustive for software development lifecycle

---

## Collision Detection

### No Collision Issues

**Analysis**: All 73 codes use unique 2-4 letter abbreviations with no conflicts.

**Verification Method**: Alphabetical sort shows no duplicates

```
AC, AGG, APC, APG, ARC, AS, BFF, CA, CAP, CBR, CDC, CD, CMV, CQR,
CSD, CWM, DAR, DBC, DCH, DEH, DM, DME, DOM, DPS, DRY, DSD, EDC, ENV,
EVS, FOC, IMP, ISA, IV, KBT, MOD, MON, MSA, MSC, MSG, OPN, ORG, OUT,
PA, PER, PKV, PRA, QSR, RAT, REH, RIG, RL, RLS, RM, RP, RPI, SAG, SCM,
SCP, SCT, SD, SDC, SF, SFT, SMH, SPO, SRL, STR, SVC, TDT, TR, TSF, TST, WAF
```

**Result**: ✅ Zero collisions detected

---

## Usage Patterns Across Rules

### High-Frequency Codes (Used in 4+ Rules)

| Code      | Used In                  | Frequency |
| --------- | ------------------------ | --------- |
| **[DAR]** | Rules 00-06 (not 07)     | Universal |
| **[OPN]** | Rules 00-06 (not 07)     | Universal |
| **[RIG]** | Rules 00, 01, 03, 04, 06 | 5 rules   |
| **[SF]**  | Rules 00, 02, 05         | 3 rules   |
| **[DRY]** | Rules 00, 02, 04, 05     | 4 rules   |
| **[CA]**  | Rules 00, 02, 04, 05     | 4 rules   |
| **[MOD]** | Rules 00, 02, 04, 05     | 4 rules   |
| **[ORG]** | Rules 01, 02, 03, 04, 05 | 5 rules   |
| **[ENV]** | Rules 01, 02, 04, 05     | 4 rules   |

### Rule-Specific Codes (Used in 1 Rule Only)

**Rule 05 (Microservices)**: 28 architecture pattern codes (exclusive to Rule 05) **Rule 03 (Memory
Bank)**: RAT, TR, EDC, AS, KBT, CWM (AI agent communication) **Rule 02 (Code Standards)**: QSR, PKV,
DEH, DCH (dependency management)

---

## Quality Metrics

| Metric                         | Value | Status |
| ------------------------------ | ----- | ------ |
| **Total Unique Codes**         | 73    | ✅     |
| **Duplicate Codes**            | 0     | ✅     |
| **Collision Codes**            | 0     | ✅     |
| **Undefined References**       | 0     | ✅     |
| **Orphaned Codes**             | 0     | ✅     |
| **Category Coverage**          | 7/7   | ✅     |
| **MECE Compliance**            | 100%  | ✅     |
| **Documentation Completeness** | 100%  | ✅     |

---

## Recommendations

### Maintenance

1. **Version Control**: Track principle code changes in CHANGELOG.md
2. **Quarterly Review**: Review code usage and update definitions as needed
3. **New Code Process**: Require MECE analysis before adding new codes
4. **Deprecation**: If codes become obsolete, mark as deprecated before removal

### Best Practices

1. **Always Tag**: Every decision/requirement should have at least one principle code
2. **Multiple Tags**: Use multiple codes when decision spans categories
3. **Consistency**: Use exact code format `**[CODE]**` in all documentation
4. **Justification**: Document _why_ a principle code applies to a decision

### Future Enhancements

1. **Usage Analytics**: Track which codes are most/least used
2. **Decision Mapping**: Create decision trees linking codes to common scenarios
3. **Training Materials**: Develop examples for each principle code application
4. **Automated Validation**: Build tools to verify principle code usage in PRs

---

---

**Registry Status**: Production Ready | MECE Verified | Zero Collisions | Complete Coverage

_This is the expanded, on-demand reference for all principle codes across the COPPER framework; the
compact always-on glossary in Rule 06 is the canonical vocabulary home._
