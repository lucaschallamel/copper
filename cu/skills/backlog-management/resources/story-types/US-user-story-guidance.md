# US - User Story Type Guidance

**Story Type**: User Story | **Prefix**: US-NNN | **Version**: 1.3.0 | **Last Updated**: 2026-05-07

---

## Definition

**User Story**: Standard delivery unit for features and enhancements that provide direct business
value to users. Follows the classic "As a [user], I want [goal], so that [benefit]" format and
represents a deliverable increment of functionality.

User stories are the primary mechanism for delivering value in Agile development. They focus on user
outcomes rather than technical implementation, enabling flexibility in how requirements are met.

---

## When to Use US Stories

Use the User Story type when:

- **Feature delivery** with direct user-facing value
- **System enhancements** improving existing functionality
- **User experience** improvements with clear user benefit
- **Business logic** implementation requested by stakeholders
- **Integration** with external systems serving user needs
- **Workflow** automation benefiting end users

**Default story type** for most development work.

---

## Purpose

Deliver business value through new features or enhancements that users can directly experience and
benefit from.

---

## Characteristics

- Provides **direct business value** to users or stakeholders
- Has **clear user persona** and benefit statement
- Represents **deliverable increment** of functionality
- Can be completed within **single sprint** (typically 1-13 points)
- Includes **acceptance criteria** that can be tested
- Follows **INVEST principles** (Independent, Negotiable, Valuable, Estimable, Small, Testable)

---

## Required YAML Fields

```yaml
---
story_id: US-042
story_type: user_story
title: 'Export customer reports to CSV format'
epic: 'Reporting Enhancement Initiative' # optional - link to parent EP if part of epic
priority: Medium
story_points: 5
status: Draft
assignee: '' # Team member assigned (visible on Kanban)
created: 2025-01-20
last_modified: 2025-01-25
---
```

### Field Descriptions

- **story_id**: Unique identifier with US prefix (US-001, US-002, etc.)
- **story_type**: Must be `user_story`
- **title**: Clear, concise description of what is being delivered
- **epic**: Optional - link to parent EP story if part of larger initiative
- **priority**: Business priority (High/Medium/Low)
- **story_points**: Effort estimate (Fibonacci: 1, 2, 3, 5, 8, 13)
- **assignee**: Team member assigned to this story (displayed on Kanban board)

---

## Progress Update Block

User stories should include a **collapsible progress update callout** immediately after the YAML
frontmatter and before the story heading or overview content.

### Recommended Format

```markdown
> [!note]- Progress updates
>
> - **2026-05-07**: Story moved to in-progress and implementation started.
> - **2026-05-06**: Scope and architecture alignment confirmed.
> - **2026-05-05**: Initial command structure and state model identified as the next implementation
>   slice.
```

### Why This Matters

- Gives a lightweight running log at the top of the story
- Supports stand-ups and incremental reporting
- Makes active work visible without scanning the full document
- Keeps progress context close to the story metadata and status

### Usage Guidance

- Use the callout in collapsed form: `[!note]-`
- Add the newest dated update at the top of the progress block
- Keep updates concise and action-oriented
- Align the note with frontmatter status changes such as `Draft`, `Ready`, `in-progress`, or
  `completed`

---

## User Story Statement Format

The core of every user story follows this structure:

```markdown
## User Story Statement

**As a** [type of user/persona] **I want** [goal or functionality] **So that** [business value or
benefit]
```

### Components Explained

- **As a**: WHO - Specific user persona or role (not generic "user")
- **I want**: WHAT - Specific capability or feature needed
- **So that**: WHY - Clear business value or user benefit

### Examples of Good Story Statements

**Good Example 1** (Specific persona, clear goal):

```markdown
**As a** sales manager **I want** to export quarterly revenue reports to CSV format **So that** I
can analyse trends in Excel and share with executives
```

**Good Example 2** (Clear value proposition):

```markdown
**As a** mobile app user **I want** to receive push notifications for order status changes **So
that** I stay informed without constantly checking the app
```

**Good Example 3** (project persona context):

```markdown
**As a** collections specialist **I want** to view all overdue accounts for a customer in a single
screen **So that** I can quickly assess collection status and create an appropriate action plan
```

---

## Examples

### Example 1: Simple Feature (5 points)

```markdown
---
story_id: US-042
story_type: user_story
title: 'Export customer reports to CSV format'
priority: Medium
story_points: 5
status: Done
assignee: '[TO BE ASSIGNED]'
---

> [!note]- Progress updates
>
> - **2025-01-25**: Story completed and ready for validation.
> - **2025-01-24**: CSV export implemented.
> - **2025-01-23**: Acceptance criteria reviewed with stakeholders ahead of sign-off.

# User Story: Export Customer Reports to CSV

## User Story Statement

**As a** sales manager **I want** to export customer reports to CSV format **So that** I can analyse
data in Excel and share with my team

## Acceptance Criteria

- [ ] **AC1**: Export button available on customer report page
- [ ] **AC2**: CSV file generated with all visible columns
- [ ] **AC3**: File naming convention: `customers_YYYY-MM-DD_HHMMSS.csv`
- [ ] **AC4**: Export completes within 3 seconds for up to 1000 records
- [ ] **AC5**: Special characters properly escaped in CSV format

## Success Metrics

- 80% of sales managers use export feature monthly
- Average time savings: 15 minutes per report
```

### Example 2: User Experience Improvement (3 points)

```markdown
---
story_id: US-075
story_type: user_story
title: 'Add loading indicators for API calls'
priority: High
story_points: 3
status: In Progress
assignee: '[TO BE ASSIGNED]'
---

> [!note]- Progress updates
>
> - **2025-01-25**: Implementation in progress.
> - **2025-01-24**: Loading states added to primary API actions.
> - **2025-01-23**: Accessibility announcement behaviour identified for follow-up review.

# User Story: Add Loading Indicators for API Calls

## User Story Statement

**As a** web application user **I want** to see loading indicators during API calls **So that** I
know the system is processing my request and hasn't frozen

## Acceptance Criteria

- [ ] **AC1**: Spinner displayed within 100ms of API call initiation
- [ ] **AC2**: Loading state disables action buttons to prevent duplicate submissions
- [ ] **AC3**: Loading indicator removes when response received
- [ ] **AC4**: Error state displayed if API call fails after 30 seconds
- [ ] **AC5**: Accessibility: screen reader announces loading state

## Swiss Market Context

- Multilingual loading messages (FR: "Chargement...", DE: "Laden...", EN: "Loading...")
- Precision expected: exact progress indication where possible

## Success Metrics

- User confusion reports reduced by 60%
- Duplicate submission errors reduced by 90%
```

### Example 3: Integration Feature (8 points)

```markdown
---
story_id: US-101
story_type: user_story
title: 'Integrate with payment gateway for credit card processing'
epic: 'Payment Processing Modernisation'
priority: High
story_points: 8
status: Draft
assignee: '[TO BE ASSIGNED]'
---

> [!note]- Progress updates
>
> - **2025-01-25**: Story drafted and awaiting implementation kickoff.
> - **2025-01-24**: External dependency review captured.
> - **2025-01-23**: Compliance considerations identified for technical design.

# User Story: Payment Gateway Integration

## User Story Statement

**As an** e-commerce customer **I want** to pay with credit card through a secure payment gateway
**So that** I can complete purchases safely without entering card details directly

## Acceptance Criteria

- [ ] **AC1**: Payment form captures card details with client-side validation
- [ ] **AC2**: Card details tokenised before transmission (PCI-DSS compliance)
- [ ] **AC3**: Payment gateway API integration handles authorisation and capture
- [ ] **AC4**: Success/failure states handled with clear user feedback
- [ ] **AC5**: Transaction records stored with gateway transaction IDs
- [ ] **AC6**: Refund capability through gateway API

## Swiss Market Context

- Support Swiss Franc (CHF) currency
- Integration with PostFinance and Twint (Swiss payment methods)
- Sector-regulator compliance for financial transactions

## Dependencies

- Payment gateway account provisioned (external dependency)
- PCI-DSS compliance review completed
- SSL certificate installed on production

## Risks

- **Risk 1**: Payment gateway API changes (Medium probability, High impact)
  - Mitigation: Use versioned API, subscribe to gateway notifications

## Success Metrics

- Payment success rate ≥98%
- Average payment processing time <5 seconds
- Zero PCI-DSS compliance violations
```

---

## Anti-Patterns (Avoid These)

### ❌ Anti-Pattern 1: Technical Implementation Instead of User Value

**Wrong**:

```markdown
**As a** developer **I want** to refactor the authentication module **So that** the code is cleaner
```

**Why it's wrong**: No user value, technical focus. This is TD (Technical Debt), not US.

**Correct approach**: Use TD-NNN for technical work without direct user value.

---

### ❌ Anti-Pattern 2: Missing "So That" (No Clear Benefit)

**Wrong**:

```markdown
**As a** user **I want** to search by date range
```

**Why it's wrong**: Missing business value - WHY does the user need this?

**Correct approach**:

```markdown
**As a** compliance officer **I want** to search audit logs by date range **So that** I can quickly
find relevant records during regulatory audits
```

---

### ❌ Anti-Pattern 3: Generic "User" Persona

**Wrong**:

```markdown
**As a** user **I want** better performance
```

**Why it's wrong**: Too vague - which user? What performance? What threshold?

**Correct approach**:

```markdown
**As a** mobile app user on 3G connection **I want** dashboard to load within 3 seconds **So that**
I can quickly check my account status on the go
```

---

### ❌ Anti-Pattern 4: Story Too Large (>13 Points)

**Wrong**:

```yaml
story_id: US-200
title: 'Complete customer portal redesign'
story_points: 34
```

**Why it's wrong**: Cannot complete in single sprint. This should be an EP (Epic) with child US
stories.

**Correct approach**: Break into multiple US stories or create EP-NNN epic.

---

## Related Story Types

### User Story Relationships

**US can be child of**:

- **EP (Epic)**: US stories are primary children of epics for feature delivery

**US can spawn**:

- **BUG**: Defects discovered during US implementation
- **TD**: Technical debt accumulated during rushed US delivery
- **SEC**: Security concerns identified during US development

**US can be preceded by**:

- **SP (Spike)**: Research reducing uncertainty before US implementation

**US can trigger**:

- **RA (Risk Action)**: Issues discovered during US requiring mitigation

---

## Story Type Transitions

### From SP to US (Research → Implementation)

**Spike outcome spawns user stories**:

```
SP-015: "Evaluate search engine options (Elasticsearch vs Solr)"
  → Decision: Use Elasticsearch
  → US-120: "Implement Elasticsearch for product search"
  → US-121: "Migrate existing search data to Elasticsearch"
```

### From US to BUG (Feature → Defect)

**User story implementation reveals bugs**:

```
US-075: "Add multi-currency support"
  → Deployed to production
  → BUG-042: "Currency conversion rounding errors in reports"
```

### From US to TD (Feature → Technical Debt)

**Quick delivery accumulates debt**:

```
US-080: "Urgent: Black Friday promotion banner" (3 points, rushed)
  → Delivered with hardcoded values
  → TD-055: "Refactor promotion system for configurability" (8 points)
```

---

## Priority Guidelines

### High Priority

- Critical business functionality blocking revenue
- Regulatory or compliance requirements with deadlines
- Customer-facing issues affecting user experience
- Strategic initiative dependencies

### Medium Priority

- Standard feature requests from product roadmap
- Operational improvements with clear business value
- Enhancements to existing functionality
- Customer requests from multiple sources

### Low Priority

- Nice-to-have features
- Long-term improvements without urgency
- Experimental features
- Minor UI/UX enhancements

---

## Sizing Guidelines (Story Points)

### Fibonacci Sequence

- **1 point**: Trivial change (e.g., text label update, simple configuration)
- **2 points**: Small feature (e.g., add validation rule, simple UI change)
- **3 points**: Standard feature (e.g., new form field with validation, simple API endpoint)
- **5 points**: Moderate complexity (e.g., integration with external API, complex business logic)
- **8 points**: Complex feature (e.g., multi-step workflow, sophisticated algorithm)
- **13 points**: Very complex (e.g., major integration, complex data transformation) - consider
  breaking down

### If Story >13 Points

Either:

1. Break down into smaller US stories
2. Convert to EP (Epic) with child US stories
3. Create SP (Spike) to reduce uncertainty, then re-estimate

---

## Acceptance Criteria Best Practices

### Clear and Testable

**Good**:

```markdown
- [ ] **AC1**: Login form validates email format (RFC 5322 standard)
- [ ] **AC2**: Password must be minimum 12 characters with uppercase, lowercase, number, symbol
- [ ] **AC3**: "Remember me" checkbox persists session for 30 days
```

**Bad**:

```markdown
- [ ] Login works properly
- [ ] Password is secure
- [ ] User can stay logged in
```

### Given/When/Then Format (BDD Style)

```markdown
- [ ] **AC1**: **Given** user is on login page **When** user enters valid credentials **Then** user
      is redirected to dashboard within 2 seconds

- [ ] **AC2**: **Given** user enters invalid email format **When** user clicks submit **Then**
      inline error message displayed: "Please enter a valid email address"
```

### Include Non-Functional Requirements

```markdown
### Non-Functional Requirements

- [ ] **Performance**: Page load time ≤3 seconds
- [ ] **Security**: All user inputs validated and sanitised [SFT]
- [ ] **Accessibility**: WCAG 2.1 Level AA compliance
- [ ] **Usability**: Mobile responsive design (320px-1920px)
- [ ] **Compatibility**: Works in Chrome, Firefox, Safari, Edge (last 2 versions)
```

### Title-AC Alignment Test

Read the story title aloud, then read the ACs. If the title promises more than the ACs cover,
either:

1. **Add missing ACs** to cover the full title scope, or
2. **Narrow the title** to match what the ACs actually deliver

**Example of misalignment** (hypothetical):

- Title: "Rationalise **and enforce** vendor-prefixed namespace"
- ACs: All about review and classification (no "enforce" action)
- Fix: Either add ACs for enforcement, or change title to "Rationalise command estate"

**Example of correct alignment**:

- Title: "Create backlog-management skill"
- ACs: Skill file exists, SKILL.md follows template, commands reference it, validator passes
- Alignment: Title scope matches AC coverage

### Deliverables Section

If a story produces artefacts or spawns follow-on child stories, declare them in a `## Deliverables`
section (placed between Definition of Done and Technical Requirements in the story template).

```markdown
## Deliverables

- [ ] **D1**: Primary analysis document
- [ ] **D2**: Child stories created for follow-on implementation → US-NNN
```

Convention: Items in `## Deliverables` are **blocking** : the story cannot close until each is
produced or explicitly delegated to a child story.

---

## Project Considerations

### Quality Expectations

- Comprehensive acceptance criteria expected
- Edge cases and error handling must be thorough
- Long-term maintainability valued over speed
- WCAG 2.1 AA accessibility compliance mandatory

### User Interface Standards

- Use the project's approved design system and component library
- Apply localisation rules appropriate to the target user base
- Maintain keyboard navigation for all interactive elements
- Document any branding, theming, or responsive design constraints

### Regulatory Context

- Apply the relevant security, privacy, and sector regulations
- Reflect any client-specific governance directives
- Document confidentiality and retention requirements for sensitive data
- Align with project-level compliance obligations from the brief or ADRs

### Personas

- Define personas in the product context before writing stories at scale
- Use stable persona names and role labels across the backlog
- Prefer business-role personas over generic labels such as "user"

---

## Checklist for US Story Creation

Before creating a US story, verify:

- [ ] Clear user persona identified (not generic "user")
- [ ] Business value articulated in "so that" statement
- [ ] Story can be completed within single sprint (1-13 points)
- [ ] Acceptance criteria are specific and testable
- [ ] Non-functional requirements considered
- [ ] Dependencies identified and manageable
- [ ] Story is independent of other stories (or dependencies documented)
- [ ] Story follows INVEST principles
- [ ] Project, market, or regulatory context addressed if applicable
- [ ] Assignee identified (for Kanban board visibility)

---

## References

### Internal Documentation

- **User Story Template**: `${CLAUDE_PLUGIN_ROOT}/skills/backlog-management/resources/user-story-template.md`
  (owning skill) owner: `cu:backlog-management` skill resource)
- **Kanban Board**: Filter by `story_type = "user_story"`
- **Memory Bank**: `docs-copper/memory-bank/` for project context

### Related Story Types

- **EP**: [EP-epic-guidance.md](EP-epic-guidance.md) - Parent epics containing US stories
- **BUG**: [BUG-defect-guidance.md](BUG-defect-guidance.md) - Defects discovered during US
- **TD**: [TD-technical-debt-guidance.md](TD-technical-debt-guidance.md) - Debt from rushed US
- **SP**: [SP-spike-guidance.md](SP-spike-guidance.md) - Research before US implementation

### External Resources

- "User Stories Applied" by Mike Cohn
- Atlassian Agile Coach - Writing User Stories
- INVEST Principles for User Stories
- Behaviour-Driven Development (BDD) - Given/When/Then format

---

_US-user-story-guidance.md | Version 1.3.0 | Last Updated: 2026-05-07 | COPPER Project
Documentation_
