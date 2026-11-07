---
title: 'Architecture Guidelines Reference'
version: '1.0.1'
last_updated: '2026-10-18'
maintained_by: 'Lucas Challamel'
---

# Architecture Guidelines Reference

Design-time reference moved out of the always-on Rule 05 by US-378 (ADR-054): the Twelve-Factor App,
the microservices pattern catalogue, and the cloud-native, performance and security-architecture
principles. Consult it when designing a service or writing an ADR. It ships in core, so every
install has it.

## Twelve-Factor App Methodology

**[ENV]** All cloud-native applications MUST adhere to the Twelve-Factor App principles for maximum
portability, scalability, and maintainability.

The twelve factors, each with its load-bearing constraint (see the referenced source for full
rationale):

- **I. Codebase** **[ORG] [CD]** , one version-controlled codebase, many deploys (1:N); environment
  config externalised.
- **II. Dependencies** **[DM] [ISA]** , 100% explicitly declared + isolated (manifests, pinned
  versions, vendoring/containers); never rely on system-wide packages.
- **III. Config** **[ENV] [SPO]** , store config in environment variables, never in code; never
  commit secrets; `.env.example` as template, never `.env`.
- **IV. Backing services** **[MOD] [ENV]** , treat databases/queues/caches as attached resources,
  swappable by config with no code change.
- **V. Build, release, run** **[AC] [CD]** , strictly separate the stages; immutable releases with
  unique ids and rollback; no runtime code modification.
- **VI. Processes** **[ARC] [MOD]** , execute as share-nothing stateless processes; persist state in
  backing services / a time-expiring datastore.
- **VII. Port binding** **[ISA] [MOD]** , export self-contained services via port binding; no
  runtime webserver injection.
- **VIII. Concurrency** **[PA] [ARC]** , scale out via the process model (workload-typed,
  horizontally partitionable process instances).
- **IX. Disposability** **[RM] [REH]** , fast startup (<10 seconds) + graceful SIGTERM shutdown
  returning queued jobs; crash-safe, idempotent operations.
- **X. Dev/prod parity** **[ENV] [TST]** , keep dev/staging/production >95% similar (same backing
  services, containerised); deploy within hours; developers deploy their own code.
- **XI. Logs** **[ENV] [ORG]** , treat logs as event streams to stdout (unbuffered); never manage
  logfiles in-app; aggregate centrally.
- **XII. Admin processes** **[SCM] [ENV]** , run admin/one-off tasks (migrations, REPL) in an
  identical environment, idempotent and repeatable.

---

## Microservices Architecture Patterns

**[MSA]** 27 patterns (Chris Richardson, "Microservices Patterns"), grouped below by concern. This
is the **name index** (on-demand, with this reference; the always-on Rule 05 points here); the full
per-pattern definitions, trade-offs, when-to-use, and quality standards live on-demand in the
framework-authoring skill resource `principle-codes-registry-reference.md` (Category 7) , Read it
when designing a service or an ADR.

- **Application architecture**: [MON] Monolithic | [MSA] Microservice
- **Decomposition**: [DBC] by Business Capability | [DSD] by Subdomain
- **Communication**: [RPI] Remote Procedure Invocation | [MSG] Messaging
- **Reliability**: [CBR] Circuit Breaker | [SDC] Service Discovery
- **Data management**: [DPS] Database per Service | [SAG] Saga | [OUT] Transactional Outbox
- **Business logic**: [DOM] Domain Model | [TSF] Transaction Script | [AGG] Aggregate | [DME] Domain
  Event | [EVS] Event Sourcing
- **Query**: [APC] API Composition | [CQR] CQRS
- **External API**: [APG] API Gateway | [BFF] Backend for Frontend
- **Testing**: [CDC] Consumer-Driven Contract | [SCT] Service Component Test
- **Deployment**: [SVC] Service per Container | [SRL] Serverless | [MSC] Microservice Chassis |
  [SMH] Service Mesh
- **Refactoring**: [STR] Strangler Fig

**Load-bearing quality expectations** (the normative bits, retained here): a circuit breaker on ALL
synchronous inter-service calls; database-per-service (access only via the owning service's API);
distributed transactions via saga only; health-check endpoints on all services. The reference has
the per-pattern rationale.

## Cloud-Native Architecture Principles

**[ENV] [PA] [ARC]** Cloud-native architecture combines multiple patterns:

### Scalability Design

**Horizontal Scaling**:

- Scale by adding instances, not vertical resources
- Stateless processes for easy replication
- Load balancing across instances
- Auto-scaling based on metrics

### Resilience Engineering

**Fault Tolerance**:

- Design for failure (all services can fail)
- Circuit breakers, retries, timeouts
- Bulkheads for isolation
- Graceful degradation

**Quality Standard**: Zero single points of failure.

### Observability

**[ORG]** Comprehensive observability for distributed systems:

- Structured logging to stdout
- Metrics (Prometheus, Grafana)
- Distributed tracing (Jaeger, Zipkin)
- Health checks and readiness probes

**Quality Standards**:

- End-to-end trace visibility
- Alert response time <5 minutes
- Log retention ≥30 days

---

## Performance & Resource Management

**[PA] [RM] [OPT]** Performance and resource optimisation requirements:

### Performance Optimisation

- Database query optimisation
- Caching strategies (Redis, Memcached)
- CDN for static assets
- Async processing for long operations

### Resource Efficiency

**[RSP]** Sustainable resource management:

- Right-sizing: No over-provisioned resources
- Resource limits and requests (Kubernetes)
- Efficient algorithms (avoid O(n²) complexity)
- Connection pooling
- Graceful resource cleanup

**Quality Standards**:

- Memory leak detection and prevention
- Connection pool optimisation

---

## Security Architecture

**[SFT] [SPO]** Security considerations at architecture level:

### Defence in Depth

- Multiple security layers
- Authentication at API gateway
- Authorisation at service level
- Network policies and segmentation
- Encryption in transit and at rest

### Zero Trust Architecture

- Never trust, always verify
- Mutual TLS between services
- Service-to-service authentication
- Short-lived credentials
- Principle of least privilege

**Quality Standards**:

- Zero critical vulnerabilities
- Encryption for all data in transit

---
