---
title: 'Rules Reference , Framework Map and Cross-References'
version: '1.0.1'
last_updated: '2026-10-18'
maintained_by: 'Lucas Challamel'
---

# Rules Reference , Framework Map and Cross-References

On-demand reference for authors of framework files, moved out of the always-on rules by US-378
(ADR-054): the harness hierarchy, the rule dependency map and each rule's integration notes.

## Framework Hierarchy & Architecture

```
<harness-root>/                      # Harness root: .opencode/ (OpenCode), .claude/ (Claude Code), or your host's equivalent
├── instructions.md                  # Parent framework instructions (always-on)
├── agents/                           # 2 core agents (more via installed kits)
├── skills/                           # 17 core skills (more via installed kits)
├── commands/                         # 19 core commands (more via installed kits)
├── tools/                           # Custom tools (host tool extensions)
│   ├── pipeline_validator.py        # Pipeline evidence verification engine (OpenCode wraps it)
│   └── format_transcript.py         # Standalone transcript formatting CLI
└── rules/                           # 8 anchors (always-on) + 8 scoped files (ADR-054)
    ├── 00-the-user.rules.md
    ├── 01-project-organisation.rules.md
    ├── 02-core-coding-principles.rules.md
    ├── 03-memory-bank.rules.md
    ├── 04-project-documentation.rules.md
    ├── 05-architecture-guidelines.rules.md
    ├── 06-principles-registry.rules.md
    ├── 07-agent-execution-security.rules.md
    └── 02a, 02b, 02c, 03a, 04a, 04b, 04c, 05a  # scoped: load with a matching file (`paths`)
```

**Harness Auto-Discovery** (host-dependent , OpenCode auto-discovers these paths; Claude Code loads
them natively from `.claude/rules/cu/`, scoped files by their `paths`; other hosts via their own
mechanism):

- **Agents**: `agents/*.md`
- **Skills**: `skills/*/SKILL.md` provide reusable capabilities
- **Commands**: `commands/*.md` become `/command-name` slash commands (workflows are implemented as
  commands)

**Core Principles**:

- **Instructions = Foundation**: `instructions.md` provides the framework context
- **Rules = Standalone**: Each rule is self-sufficient within its domain
- **No Redundancy**: Shared content has one home; other files point to it
- **Clear Hierarchy**: Instructions -> Rules -> Implementation

---

## Rules Cross-Reference Map

**Purpose**: Understand rule dependencies and integration points. Each rule builds upon and
references others in this framework.

```
Rule 00 (User Profile & Professional Context)
  |--> Rule 01: Structure alignment, values integration, governance context
  |--> Rule 02: Coding standards, professional expectations, quality mindset
  |--> Rule 03: AI agent integration, OpenCode workflows, tool usage
  |--> Rule 04: Documentation standards, British English, template usage
  |--> Rule 05: Environment preferences, containerisation (as configured in Rule 00)
  +--> Rule 05: Architectural mindset, microservices thinking, DDD approach

Rule 01 (Project Structure & Governance)
  |--> Rule 00: Organisation context, professional standards, cultural values
  |--> Rule 02: Implementation standards, principle tagging, quality gates
  |--> Rule 03: Memory bank location (/memory-bank/)
  |--> Rule 04: Documentation location, templates, folder structure
  |--> Rule 05: Configuration management, dev/prod parity, 12-factor compliance
  +--> Rule 05: Service boundaries, microservices structure, API-first design

Rule 02 (Code Implementation Standards)
  |--> Rule 00: Professional standards, organisational values, technical environment
  |--> Rule 01: Quality frameworks, testing requirements, governance processes
  |--> Rule 04: Documentation principles, strategic documentation
  |--> Rule 05: Configuration principles, environment awareness, stateless design
  +--> Rule 05: Architecture patterns, service communication, data management

Rule 03 (Memory Bank for AI Agents)
  |--> Rule 00: AI agent workflows, OpenCode integration, tool ecosystem
  |--> Rule 01: Memory bank location, project structure, documentation standards
  +--> Rule 04: Documentation standards, templates, knowledge management

Rule 04 (Business & Project Documentation)
  |--> Rule 01: Project structure, folder organisation
  |--> Rule 03: Memory bank location /memory-bank/
  +--> Rule 05: API documentation, architectural decisions

Rule 05 (Architecture Guidelines)
  |--> Rule 00: Environment setup, architectural thinking, DDD approach
  |--> Rule 01: Service structure, deployment infrastructure, API documentation
  +--> Rule 02: Implementation patterns, service communication, data management

Rule 07 (Agent-Execution-Security and Governance)
  |--> Rule 00: User authority + the safety rules Control 4 (effect-tiers) enforces
  |--> Rule 02: [SFT]/[SPO] and Security & Compliance codes realised at runtime
  |--> Rule 05: System-level security architecture (defence in depth, zero-trust)
  +--> Rule 06: Principle-codes registry ([SFT]/[SPO]/[IV]/[RM]/[REH] , no new codes added)
```

---

## Integration with Other Rules (Rule 02)

**Cross-References**:

- **Rule 00**: User preferences (language, containerisation, development environment)
- **Rule 01**: Code organisation within directory structure
- **Rule 03**: Memory bank updates for coding decisions and patterns
- **Rule 04**: Code documentation standards
- **Rule 05**: System-level architecture decisions and patterns

**Memory Bank Integration** **[RAT]**:

- Document coding patterns in `memory-bank/systemPatterns.md`
- Track technology decisions in `memory-bank/techContext.md`
- Log completed features in `memory-bank/progress.md`
- Note active work in `memory-bank/activeContext.md`

---

## Example: Good activeContext.md (Rule 03)

A worked `activeContext.md` example (current state, next steps, decisions, patterns, blockers,
learnings , demonstrating [SD]/[TR]/[RP]/[CWM]) is on-demand at the framework-authoring skill
resource `skills/framework-authoring/resources/activecontext-example.md`.

---

## Integration with Other Rules (Rule 05)

**Cross-References**:

- **Rule 00**: User preferences (development environment, containerisation, technology preferences)
- **Rule 01**: Architecture documentation location and organisation
- **Rule 02**: Code-level implementation of architectural patterns
- **Rule 03**: Memory bank updates for architectural decisions
- **Rule 04**: ADR templates and documentation standards

**Memory Bank Integration** **[RAT]**:

- Document architectural patterns in `memory-bank/systemPatterns.md`
- Track architecture decisions in `memory-bank/progress.md`
- Note system design in `memory-bank/activeContext.md`
- Reference ADRs in `memory-bank/techContext.md`
