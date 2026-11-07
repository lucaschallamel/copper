---
name: gtd-notation
description: Complete Task Genius notation reference for task management and GTD integration. Use when generating actionable items, creating project plans, tracking progress on proposals/projects/tenders, delegating tasks, or managing complex workflows with Task Genius notation (8 status characters).
version: 1.1.1
last_updated: '2026-07-11'
maintained_by: Lucas Challamel
applies_to: All 12 agents (universal)
---

# GTD Notation - Complete Task Genius Reference

Complete reference for Task Genius notation and GTD integration for business consulting agents.

**When to use this Skill**:

- Generating actionable items, next steps, or deliverables
- Creating project plans, proposal timelines, or work breakdowns
- Tracking progress on proposals, projects, tenders, or recruitment
- Delegating tasks to other agents or team members
- Managing complex multi-phase workflows

---

## 📋 Complete Task Genius Notation Standard

### Status Characters - Full Definitions

| Syntax             | Status                  | Description                                      | Use Case                                    | Example                                                                    |
| ------------------ | ----------------------- | ------------------------------------------------ | ------------------------------------------- | -------------------------------------------------------------------------- |
| `- [ ]`            | **Todo/Not Started**    | Task identified but not yet begun                | New tasks, backlog items, planned work      | `- [ ] Write executive summary (Target: 2-3 pages)`                        |
| `- [x]` or `- [X]` | **Completed**           | Task successfully finished                       | Finished work, completed deliverables       | `- [x] Conduct RFI analysis (Completed: 2025-01-20, 42 requirements)`      |
| `- [/]`            | **In Progress**         | Task currently being worked on                   | Active tasks, work in progress              | `- [/] Design solution architecture (In progress: 60% complete)`           |
| `- [-]`            | **Cancelled/Abandoned** | Task no longer relevant or deprioritized         | Obsolete tasks, changed requirements        | `- [-] Alternative pricing model (Cancelled: Client requires fixed-price)` |
| `- [>]`            | **Forwarded/Delegated** | Task assigned to another person or team          | Delegated work, handoffs, escalations       | `- [>] Design cloud architecture (Assigned: @your-architect)`              |
| `- [<]`            | **Scheduled**           | Task scheduled for future execution              | Planned tasks with specific dates           | `- [<] Red Team review (Scheduled: 2025-02-02 14:00)`                      |
| `- [?]`            | **Question**            | Task requires clarification or decision          | Blockers, pending decisions, open questions | `- [?] Clarify data residency requirements (Question sent to client)`      |
| `- [!]`            | **Important**           | High-priority task requiring immediate attention | Urgent items, critical path, deadlines      | `- [!] URGENT: Bid/no-bid decision required (Deadline: 2025-01-30)`        |

---

## 🔧 Detailed Usage Guidelines

### When to Use Task Notation (Comprehensive)

Task-Genius notation applies across many work domains. Use it wherever you generate actionable
items, whatever the domain:

- **Analysis and intake**: extract requirements, map compliance, assess feasibility, gather inputs
- **Design and planning**: architecture milestones, work breakdowns, technology evaluation, roadmaps
- **Delivery and tracking**: milestones, acceptance criteria, sign-offs, status reporting, issue
  resolution
- **Review and approval gates**: peer review, technical validation, sign-off checkpoints
- **Delegation and handoffs**: assign to a specialist with
  `[>] ... (Assigned: @your-architect, Due: <date>)`
- **Open questions and blockers**: flag with `[?]` when a decision or clarification is pending

For domain-specific delegation, name the relevant specialist role (for example `@your-architect`,
`@your-analyst`, or `a delegate`) rather than a fixed agent. The teaching is the notation, not the
roster of roles.

> Domain-specific worked-examples (for example consulting/commercial roles , pre-sales, tenders, and
> SME specialists) ship on-demand in the relevant delivery kit's proposal/commercial skill
> resources, not in this vendor-neutral core skill.

**Agent Creation** (@cu:agent-creator):

- Gap analysis validation (capability mapping, MECE validation)
- Agent design tasks (scope definition, architecture, prompt writing)
- Configuration development (opencode.jsonc, custom commands)
- Testing and validation (typical scenarios, company facts, organisational values)
- Ecosystem integration (instructions.md updates, agent count)

---

## 📐 Task Formatting Best Practices (Detailed)

### 1. Be Specific and Actionable

**Principle**: Task descriptions must be concrete, measurable, and actionable. Avoid vague language.

**Bad Examples** ❌:

```markdown
- [ ] Work on proposal
- [ ] Fix issues
- [ ] Talk to client
- [ ] Do architecture
- [ ] Handle security
```

**Good Examples** ✅:

```markdown
- [ ] Write design overview for the payment service (2-3 pages, emphasise idempotency)
- [ ] Address review feedback on security architecture (3 items: encryption, access control,
      monitoring)
- [ ] Schedule clarification call with the platform team (30 min, by Friday 17:00 CET)
- [ ] Design service architecture using C4 model (Context, Container, Component diagrams)
- [ ] Validate compliance requirements (regulations, data residency, audit trail)
```

**Key Elements**:

- **Action verb**: Write, Address, Schedule, Design, Validate
- **Deliverable**: Design overview, feedback response, call, architecture, compliance validation
- **Specificity**: Page count, item count, duration, model type, requirements
- **Context**: the payment service, review feedback, platform team, C4 model, regulator

---

### 2. Assign Ownership When Delegating

**Principle**: Delegated tasks must clearly identify the responsible party and due date.

**Format**: `[>] Task description (Assigned: Name/Role, Due: Date)`

**Examples**:

```markdown
- [>] Design service integration architecture (Assigned: @your-architect, Due: 2025-01-26)
- [>] Validate compliance requirements (Assigned: @your-security-analyst, Due: 2025-01-27)
- [>] Review pricing model for margin validation (Assigned: [User Name], Due: 2025-01-25)
- [>] Conduct technical interview with candidate (Assigned: Hiring Manager, Due: 2025-01-28 10:00)
- [>] Develop consortium agreement (Assigned: Legal Team, Due: 2025-02-01)
```

**Best Practices**:

- Use `@agent-name` for agent delegation
- Use full name or role for human delegation
- Always include due date or deadline
- Add context if needed (e.g., "3 items", "30 min call")

---

### 3. Include Deadlines for Scheduled Tasks

**Principle**: Scheduled tasks must include specific date and time when possible.

**Format**: `[<] Task description (Scheduled: Date Time)`

**Examples**:

```markdown
- [<] Submit release candidate (Scheduled: 2025-02-15 17:00 CET)
- [<] Architecture review meeting (Scheduled: 2025-02-10 14:00, 90 min, 5 attendees)
- [<] Final design walkthrough (Scheduled: 2025-02-08 10:00, in-person, the main office)
- [<] Quarterly agent ecosystem review (Scheduled: 2025-04-01, full day workshop)
- [<] Steering committee presentation (Scheduled: 2025-01-30 15:00, 60 min, 8 stakeholders)
```

**Best Practices**:

- Use ISO date format (YYYY-MM-DD) for clarity
- Include time with timezone (CET for Switzerland)
- Add duration if relevant (90 min, 60 min)
- Add location if relevant (in-person, the main office, video call)
- Add attendee count if relevant (5 attendees, 8 stakeholders)

---

### 4. Prioritise Urgent Tasks

**Principle**: High-priority tasks must be flagged with urgency indicator and deadline.

**Format**: `[!] URGENT: Task description (Deadline: Date, Reason)`

**Examples**:

```markdown
- [!] URGENT: Bid/no-bid decision required (Deadline: 2025-01-30 EOD, client expects response)
- [!] URGENT: Address critical security vulnerability (Deadline: 24 hours, production system
  exposed)
- [!] URGENT: Client escalation response (Deadline: Today 17:00, CEO involved)
- [!] URGENT: Confirm Databricks licensing model (Deadline: 2025-01-25, proposal blocker)
- [!] URGENT: Resource allocation for data engineer (Deadline: This week, project at risk)
```

**Best Practices**:

- Reserve `[!]` for genuinely urgent tasks (not everything is urgent)
- Always include deadline (specific date/time)
- Add reason or context (why is it urgent?)
- Use "URGENT:" prefix for visibility
- Consider impact (client relationship, project risk, security)

---

### 5. Track Progress with Status Updates

**Principle**: Update task status as work progresses to maintain visibility.

**Workflow**: `[ ]` → `[/]` → `[x]`

**Example Progression**:

```markdown
## Feature Development - Payment Service

### Initial State (Backlog)

- [ ] Design cloud migration strategy

### Work Begins (In Progress)

- [/] Design cloud migration strategy (Started: 2025-01-20, 30% complete)

### Blocked/Question (Needs Clarification)

- [?] Design cloud migration strategy (Blocked: Waiting for data centre specs)

### Delegated (Assigned to Specialist)

- [>] Design cloud migration strategy (Assigned: @your-architect, Due: 2025-01-26)

### Scheduled (Planned Execution)

- [<] Design cloud migration strategy (Scheduled: 2025-02-01 - 2025-02-05, 5-day sprint)

### Urgent (Critical Path)

- [!] URGENT: Design cloud migration strategy (Deadline: 2025-01-25, client escalation)

### Completed (Finished)

- [x] Design cloud migration strategy (Completed: 2025-01-23, deliverable: 15-page document)

### Cancelled (Obsolete)

- [-] Design cloud migration strategy (Cancelled: Client decided on SaaS solution instead)
```

**Best Practices**:

- Update status regularly (daily for active tasks)
- Add completion percentage for in-progress tasks (30%, 60%, 90%)
- Document completion date and deliverable
- Explain cancellation reason (changed requirements, obsolete)

---

## 🎭 Multi-Phase Worked Example

A role-neutral worked example showing the full status vocabulary across phases:

```markdown
## Feature Delivery - Governance Framework

### Phase 1: Initial Assessment

- [x] Receive requirements document (Received: 2025-01-18, 87 pages)
- [/] Conduct feasibility assessment (Currently: 65%)
- [?] Clarify data residency requirements (Question sent)
- [!] URGENT: Go/no-go decision (Deadline: 2025-01-21 EOD)

### Phase 2: Solution Design

- [>] Validate compliance (Assigned: @your-security-analyst, Due: 2025-01-24)
- [<] Solution workshop (Scheduled: 2025-01-26 09:00-12:00)
```

_Domain-specific worked examples (pre-sales, tenders, SME roles) ship on-demand in the relevant
delivery kit's proposal/commercial skill resources, not in this vendor-neutral core skill._

---

## 🔗 Integration with Obsidian Vault (Complete)

### Dual MCP Server Setup

**1. Task Genius MCP Server** (`quad-damage-tasks`):

- Task management with GTD workflows
- Create, query, update tasks
- Batch operations

**2. Obsidian Vault MCP Server** (`obsidian-vault`):

- Knowledge management
- Read/write vault files
- Search and templates

**Benefits**:

- ✅ Unified workflow (tasks + knowledge)
- ✅ Context preservation
- ✅ Reference access
- ✅ Complete GTD support

---

## 📖 Quick Reference Card

| Symbol | Status      | Example                                           |
| ------ | ----------- | ------------------------------------------------- |
| `[ ]`  | Todo        | `- [ ] Write summary (2-3 pages)`                 |
| `[x]`  | Done        | `- [x] RFI analysis (Completed: 2025-01-20)`      |
| `[/]`  | In Progress | `- [/] Architecture (60% complete)`               |
| `[-]`  | Cancelled   | `- [-] Alt pricing (Client requires fixed-price)` |
| `[>]`  | Delegated   | `- [>] Design (Assigned: @your-architect)`        |
| `[<]`  | Scheduled   | `- [<] Review (Scheduled: 2025-02-02 14:00)`      |
| `[?]`  | Question    | `- [?] Clarify data residency`                    |
| `[!]`  | Urgent      | `- [!] URGENT: Decision (Deadline: 2025-01-30)`   |

---

## ✅ Compliance Checklist

- [ ] Use Task Genius notation for ALL actionable items
- [ ] Be specific (action verb + deliverable + context)
- [ ] Assign ownership when delegating (`[>]`)
- [ ] Include deadlines for scheduled tasks (`[<]`)
- [ ] Prioritise urgent tasks (`[!]`)
- [ ] Track progress with status updates
- [ ] Flag questions requiring clarification (`[?]`)
- [ ] Cancel obsolete tasks explicitly (`[-]`)

---
