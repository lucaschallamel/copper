---
entry_date: YYYY-MM-DD
author: ''
focus_area: ''
status: draft
session_duration: ''
tags: []
version: '1.1.0'
last_updated: '2026-09-10'
maintained_by: 'Lucas Challamel'
---

## Why (High-Level Context)

[What prompted this session? What problem, feature, or goal?]

**Session Objectives**:

- [Primary objective or goal for this session]
- [Secondary objectives if applicable]

**Related Work**:

- User Story: [US-XXX if applicable]
- ADR: [ADR-XXX if applicable]
- Sprint: [sprint-XXX if applicable]

---

## How (The Journey)

### The Initial Problem

[Describe the challenge, bug, or feature to be addressed]

**Context**:

- [Background information]
- [Why this matters]
- [Initial assumptions]

**Constraints**:

- [Technical constraints]
- [Time constraints]
- [Resource constraints]

### The Investigation

[How did you approach the problem? What did you research or try?]

**Research Activities**:

- [Documentation reviewed]
- [Code explored]
- [Experiments conducted]

**Key Findings**:

- [Discovery 1]
- [Discovery 2]
- [Discovery 3]

**Dead Ends** (optional):

- [Approaches that didn't work and why - valuable learning]

### The Breakthrough

[What key insight or solution unlocked progress?]

**The "Aha!" Moment**:

- [Description of the breakthrough insight]
- [Why this solution works]
- [How it differs from previous attempts]

**Decision Rationale**:

- [Why this approach was chosen]
- [Trade-offs considered]
- [Alternatives rejected and why]

### Implementation and Refinements

[Summarise the steps taken, code changes, and any refactoring]

**Changes Made**:

- [File/component 1]: [Description of changes]
- [File/component 2]: [Description of changes]
- [File/component 3]: [Description of changes]

**Code Quality**:

- [Refactoring applied]
- [Principle codes followed: [SF], [RP], [DRY], etc.]
- [Technical debt addressed or created]

**Collaboration**:

- [Code reviews]
- [Pair programming sessions]
- [Team discussions]

### Validation and Documentation

[How did you test/validate? What docs or changelogs were updated?]

**Testing Performed**:

- [ ] Unit tests written/updated
- [ ] Integration tests run
- [ ] Manual testing completed
- [ ] Edge cases verified

**Documentation Updated**:

- [ ] Code comments added
- [ ] README.md updated
- [ ] ADR created/updated
- [ ] API documentation updated
- [ ] CHANGELOG.md updated

**Artefacts Created**:

- [Links to commits, PRs, documentation]

---

## Final State & Next Steps

**Current State**:

- [What's the state of the codebase now?]
- [What works?]
- [What's still incomplete?]

**Immediate Next Steps**:

- [ ] [Next action item 1]
- [ ] [Next action item 2]
- [ ] [Next action item 3]

**Future Considerations**:

- [Technical debt to address later]
- [Potential improvements or optimisations]
- [Follow-up questions or uncertainties]

**Knowledge Captured**:

- [Key learnings to remember]
- [Gotchas or pitfalls to avoid]
- [Useful resources or references]

---

## Reflection (Optional)

**What Went Well**:

- [Successes or positive outcomes]

**What Could Be Improved**:

- [Challenges or areas for improvement]

**Skills Developed**:

- [New techniques learned]
- [Tools mastered]
- [Domain knowledge acquired]

---

**Session Summary**: [One-sentence summary of the session outcome]

**Estimated Impact**: [Low | Medium | High]

---

> [!tip]- TEMPLATE USAGE GUIDELINES **To be excluded from the generated journal entry.**
>
> **INSTRUCTIONS FOR COMPLETING THIS TEMPLATE**:
>
> 1. Copy this template for each development session (daily, weekly, or per-feature)
> 2. Replace all [placeholder text] with actual content
> 3. Fill in YAML frontmatter with session date, author, focus area
> 4. Remove optional sections (Dead Ends, Reflection) if not needed
> 5. Keep sections even if brief - consistency aids later review
> 6. Tag relevant user stories, ADRs, or sprint work for traceability
> 7. Be honest about dead ends and failures - valuable learning
> 8. Delete this entire callout section before finalising
>
> **FRONTMATTER FIELD GUIDANCE**:
>
> - `entry_date`: YYYY-MM-DD format (e.g., 2025-10-26)
> - `author`: Resolve from live session context first. Use the active user explicitly identified in
>   the conversation or session context. If that is unavailable, fall back to configured framework
>   context such as `00-the-user.rules.md` or `AGENTS.md`. Only use a placeholder if no active user
>   can be resolved.
> - `focus_area`: Brief description (e.g., "API development", "Bug fix", "Refactoring")
> - `status`: draft | in-progress | completed
> - `session_duration`: Optional (e.g., "2 hours", "full day")
> - `tags`: Array of relevant tags (e.g., [backend, api, security])
> - `version`: Start at `1.0.0` for a new entry
> - `last_updated`: Date of the latest meaningful revision in YYYY-MM-DD format
> - do NOT add a `changelog:` key: US-339 externalised change history to the per-kit `CHANGELOG.md`,
>   Rule 04 forbids an inline `changelog:` frontmatter key, and the markdown-governance gate rejects
>   one (TD-178)
> - `maintained_by`: Framework maintainer value, currently `Lucas Challamel`
>
> **WHEN TO USE THIS TEMPLATE**:
>
> - End of significant development sessions
> - When solving complex problems worth documenting
> - Before context switching to capture current state
> - Weekly summaries of sprint progress
> - Milestone achievements or major breakthroughs
>
> **BENEFITS**:
>
> - Ensures clarity and traceability for team
> - Captures institutional knowledge
> - Aids onboarding of new team members
> - Supports sprint retrospectives and reviews
> - Documents decision rationale for future reference

> [!info]- TEMPLATE DATA (YAML BackMatter) For indexing, search, and validation purposes. **To be
> excluded from the generated journal entry.**
>
> ```yaml
> template_name: 'Dev Journal Template'
> template_description:
>   'Structured template for development journal entries capturing the why, how, and outcomes of
>   development sessions'
> template_scope:
>   'Use for daily/weekly development logs, problem-solving sessions, feature development, and
>   knowledge capture'
> template_version: '1.0.0'
> template_last_updated: '2025-10-26'
> template_status: 'active'
> template_category: 'documentation'
> template_maintained_by: '[Project Team]'
>
> principle_codes_emphasized:
>   - SD # Strategic Documentation
>   - RP # Readability Priority
>   - ORG # Organisational Clarity
>   - ISA # Industry Standards Adherence
>   - TR # Transparent Reasoning (from CLAUDE.md principle codes)
>
> cross_references:
>   - 'User Story Template: user-story-template.md'
>   - 'ADR Template: (to be created)'
>   - 'Sprint Planning Template: (to be created)'
>   - 'Memory Bank: docs-copper/memory-bank/'
>   - 'Dev Journal Directory: docs-copper/dev-journal/'
>
> applies_to:
>   - 'All developers documenting work sessions'
>   - 'Team leads capturing architectural decisions'
>   - 'Engineers solving complex problems'
>   - 'Contributors needing to preserve context'
>
> usage_pattern:
>   when_to_create:
>     - 'End of significant development sessions'
>     - 'After solving complex technical problems'
>     - 'Before context switching to new work'
>     - 'Weekly sprint progress summaries'
>     - 'Major milestone or breakthrough achievements'
>   naming_convention:
>     daily: 'YYYY-MM-DD.md'
>     weekly: 'YYYY-WXX.md (week number)'
>     feature: 'YYYY-MM-DD-feature-name.md'
>   storage_location: 'docs-copper/dev-journal/YYYY/MM/'
>
> related_workflows:
>   - 'Update memory-bank/project-context/progress.md with milestones'
>   - 'Reference in sprint retrospectives'
>   - 'Link from user stories when documenting implementation'
>   - 'Extract ADRs from significant decisions'
>   - 'Share in team knowledge base or wiki'
> ```
