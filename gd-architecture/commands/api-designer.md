---
description: Run an API-design session , produce a consistent, well-documented API
  surface with an OpenAPI specification, versioning, and governance, grounded in the
  gd-api-designer skill.
---

Design an API for: **$ARGUMENTS**

All arguments are optional. `api_category` (default `business-logic`; the API classification
category); `compliance_requirements` (default `basic`; the regulatory and standards compliance
level); `integration_complexity` (default `collaborative`; the ecosystem integration requirements);
`api_type` (default `rest`; options: `rest`, `graphql`, `grpc`, `websocket`, `webhook`,
`event-driven`); `complexity_level` (default `standard`; options: `simple`, `standard`, `complex`,
`enterprise`, `microservices`); `security_level` (default `standard`; options: `basic`, `standard`,
`high`, `enterprise`, `zero-trust`); `performance_tier` (default `standard`; options: `basic`,
`standard`, `high-throughput`, `real-time`, `enterprise-scale`). With no arguments, open by drawing
out the consumers, the resources, and the contracts the API must expose.

## Approach

1. **Load the API-design knowledge** , Use the `gd-architecture:api-designer` skill.
2. **Frame the problem** , clarify the consumers behind `$ARGUMENTS`, the resources and operations,
   the non-functional requirements (latency, throughput, compliance), and what already exists.
3. **Design the contract** , apply the fitting models from the skill (REST/Richardson Level 3,
   OpenAPI-first schemas, the relevant security and versioning patterns) to the chosen `api_type`
   and `complexity_level`, and capture the endpoints, schemas, and error model.
4. **Validate and document** , at the requested `security_level` and `performance_tier`, lint the
   spec, verify backward compatibility and the deprecation path, and deliver an OpenAPI
   specification with examples, governance rules, and a developer-experience plan.

## Opening (when no args)

"Let's design an API your consumers will adopt quickly and you can evolve safely. Who consumes it,
what resources and operations does it expose, and what latency, throughput, and compliance
constraints must it respect?"

## Examples

```bash
# Enterprise API with high security and high throughput
/gd-architecture:api-designer api_category=business-logic compliance_requirements=enterprise-grade integration_complexity=ecosystem-wide api_type=rest security_level=enterprise performance_tier=high-throughput

# Simple integration API
/gd-architecture:api-designer api_category=integration compliance_requirements=basic integration_complexity=collaborative api_type=rest

# Event-driven microservices API
/gd-architecture:api-designer api_category=event-streaming compliance_requirements=gdpr integration_complexity=orchestrating api_type=event-driven complexity_level=microservices
```

---

- Skill: `gd-architecture:api-designer` (owns the methodologies, patterns, and API-design knowledge)
- Related agent: the proactive `gd-architecture:api-designer` agent loads the same skill autonomously.
