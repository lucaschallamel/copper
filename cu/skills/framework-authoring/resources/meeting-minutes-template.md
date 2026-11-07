---
meeting_id: 'MTG-YYYYMMDD-NNN'
title: '[Meeting Title]'
date: YYYY-MM-DD
time: 'HH:MM - HH:MM'
timezone: 'Europe/Zurich'
location: "[Physical address or 'Remote - Platform Name']"
meeting_type: '[discovery | workshop | steering | review | kickoff | retrospective | other]'
client: '[Client Name]'
project: '[Project Name or Code]'
status: draft
author: '[Minutes Author Name]'
version: '1.0.1'
last_updated: YYYY-MM-DD
tags: []
---

# Meeting Minutes - [Meeting Title]

**Date**: [DD Month YYYY]  
**Time**: [HH:MM - HH:MM] ([Timezone])  
**Location**: [Full address or Remote platform]  
**Subject**: [Brief description of meeting purpose]

---

## Attendees

### Client / External

| Name       | Role         | Organisation | Attendance                    |
| ---------- | ------------ | ------------ | ----------------------------- |
| **[Name]** | [Role/Title] | [Company]    | Present                       |
| ~~[Name]~~ | [Role/Title] | [Company]    | _Invited - Absent_            |
| **[Name]** | [Role/Title] | [Company]    | Present (partial: [duration]) |

### [Your Organisation]

| Name       | Role         | Attendance |
| ---------- | ------------ | ---------- |
| **[Name]** | [Role/Title] | Present    |
| **[Name]** | [Role/Title] | Present    |

---

## Meeting Objectives

1. [Primary objective of the meeting]
2. [Secondary objective]
3. [Additional objectives as needed]

---

## Agenda

| #   | Topic     | Duration | Owner  |
| --- | --------- | -------- | ------ |
| 1   | [Topic 1] | [XX min] | [Name] |
| 2   | [Topic 2] | [XX min] | [Name] |
| 3   | [Topic 3] | [XX min] | [Name] |

---

## Discussion Summary

### [Topic 1 Title]

**Key Points**:

- [Main point discussed]
- [Important information shared]
- [Relevant context or background]

**Decisions Made**:

- [Decision 1]
- [Decision 2]

---

### [Topic 2 Title]

**Key Points**:

- [Main point discussed]
- [Important information shared]

**Open Questions**:

- [Question requiring follow-up]
- [Clarification needed]

---

## Key Decisions

| #   | Decision               | Owner  | Date         |
| --- | ---------------------- | ------ | ------------ |
| D1  | [Decision description] | [Name] | [YYYY-MM-DD] |
| D2  | [Decision description] | [Name] | [YYYY-MM-DD] |

---

## Action Items

| #   | Action               | Owner  | Deadline     | Status  |
| --- | -------------------- | ------ | ------------ | ------- |
| A1  | [Action description] | [Name] | [YYYY-MM-DD] | Pending |
| A2  | [Action description] | [Name] | [YYYY-MM-DD] | Pending |
| A3  | [Action description] | [Name] | [YYYY-MM-DD] | Pending |

**Status Legend**: `Pending` | `In Progress` | `Completed` | `Blocked` | `Cancelled`

---

## Documents & Materials

### Shared During Meeting

- [ ] [Document name] - [Brief description]
- [ ] [Presentation name] - [Brief description]

### To Be Shared Post-Meeting

- [ ] [Document name] - Owner: [Name] - Due: [Date]
- [ ] [Document name] - Owner: [Name] - Due: [Date]

---

## Next Steps

| Action        | Owner               | Deadline |
| ------------- | ------------------- | -------- |
| [Next step 1] | [Name/Organisation] | [Date]   |
| [Next step 2] | [Name/Organisation] | [Date]   |

---

## Next Meeting

**Proposed Date**: [Date or TBD]  
**Proposed Time**: [Time or TBD]  
**Location**: [Location or TBD]  
**Agenda Preview**: [Brief description of expected topics]

---

## Appendix (Optional)

### A. Glossary / Acronyms

| Term      | Definition                        |
| --------- | --------------------------------- |
| [ACRONYM] | [Full term and brief explanation] |

### B. Reference Documents

- [Document 1]: [Link or location]
- [Document 2]: [Link or location]

### C. Meeting Notes (Raw)

[Optional: Include raw notes or additional context not captured above]

---

_Minutes prepared by [Author Name], [Organisation]_  
_Distribution: [List of recipients or "Meeting attendees"]_  
_Confidentiality: [Internal | Client Confidential | Public]_

---

> [!tip]- TEMPLATE USAGE GUIDELINES **To be excluded from the generated minutes.**
>
> **INSTRUCTIONS FOR COMPLETING THIS TEMPLATE**:
>
> 1. Replace all `[placeholder text]` with actual content
> 2. Update YAML frontmatter with meeting-specific values
> 3. Remove sections not applicable to your meeting (e.g., Appendix if not needed)
> 4. Use strikethrough `~~Name~~` for invited but absent attendees
> 5. Note partial attendance with duration in parentheses
> 6. Ensure all action items have clear owners and deadlines
> 7. Delete this callout section before finalising
>
> **FRONTMATTER FIELD GUIDANCE**:
>
> - `meeting_id`: Format `MTG-YYYYMMDD-NNN` (e.g., MTG-20251125-001)
> - `title`: Brief, descriptive title of the meeting
> - `date`: ISO format YYYY-MM-DD
> - `time`: 24-hour format with timezone
> - `meeting_type`: One of: discovery, workshop, steering, review, kickoff, retrospective, other
> - `client`: Client organisation name
> - `project`: Project name or internal code
> - `status`: draft | final | approved
> - `author`: Person who prepared the minutes
> - `tags`: Array of relevant tags for searchability
>
> **MEETING TYPE DEFINITIONS**:
>
> - `discovery`: Initial client meeting, requirements gathering
> - `workshop`: Collaborative working session
> - `steering`: Governance/steering committee meeting
> - `review`: Project review, sprint review, QBR
> - `kickoff`: Project or phase kickoff
> - `retrospective`: Lessons learned, improvement discussion
> - `other`: Any meeting not fitting above categories
>
> **ATTENDANCE NOTATION**:
>
> - **Present**: Bold name, full attendance
> - ~~Absent~~: Strikethrough, note "Invited - Absent"
> - **Partial**: Bold name with "(partial: first 30 min)" or similar
> - **Remote**: Add "(remote)" if hybrid meeting
>
> **ACTION ITEM BEST PRACTICES**:
>
> - Use clear, actionable language (verb + object)
> - Assign single owner (not "Team" or multiple names)
> - Set realistic, specific deadlines
> - Include success criteria where helpful
>
> **FILE NAMING CONVENTION**:
>
> `YYYYMMDD-[Client]-[MeetingType]-Minutes-[Language].md`
>
> Examples:
>
> - `20251125-TotalEnergies-Discovery-Minutes-EN.md`
> - `20251125-Acme-Workshop-Minutes-FR.md`
> - `20251125-Internal-Retrospective-Minutes-EN.md`
>
> **STORAGE LOCATION**:
>
> - Client meetings: `/proposals/[proposal-folder]/minutes/` or
>   `/projects/[project-folder]/minutes/`
> - Internal meetings: `/projects/internal/minutes/` or relevant project folder

> [!info]- TEMPLATE DATA (YAML BackMatter) For indexing, search, and validation purposes. **To be
> excluded from the generated minutes.**
>
> ```yaml
> template_name: 'Meeting Minutes Template'
> template_description:
>   'Standardised template for recording meeting minutes with attendees, decisions, action items,
>   and follow-up tracking'
> template_scope: 'Use for all client and internal meetings requiring formal documentation'
> template_version: '1.0.0'
> template_last_updated: '2025-11-27'
> template_status: 'active'
> template_category: 'documentation'
> template_maintained_by: 'COPPER framework'
>
> principle_codes_emphasized:
>   - SD # Strategic Documentation
>   - ORG # Organisational Clarity
>   - COM # Commitment
>   - COL # Collaboration
>   - TSP # Team Spirit
>
> cross_references:
>   - 'Rule 01: Project Organisation (naming conventions, storage locations)'
>   - 'Rule 04: Project Documentation (documentation standards)'
>   - 'Pre-Sales Todo Template: presales-todo-template.md'
>   - 'Commercial Reference Template: commercial-reference-template.md (for capturing project
>     outcomes as references)'
>   - 'User Story Template: user-story-template.md (for action items becoming stories)'
>
> applies_to:
>   - 'Pre-sales consultants documenting client meetings'
>   - 'Project managers recording steering committees'
>   - 'Technical leads documenting workshops'
>   - 'Account managers tracking client interactions'
>   - 'All team members requiring formal meeting records'
>
> usage_pattern:
>   when_to_use:
>     - 'Client discovery and requirements meetings'
>     - 'Project steering committee meetings'
>     - 'Technical workshops and design sessions'
>     - 'Sprint reviews and retrospectives'
>     - 'Kickoff meetings for new projects or phases'
>     - 'Any meeting with decisions or action items to track'
>   when_not_to_use:
>     - 'Informal internal discussions'
>     - 'Quick sync calls without decisions'
>     - 'Meetings already documented elsewhere (e.g., Jira, Confluence)'
>   naming_convention: 'YYYYMMDD-[Client]-[MeetingType]-Minutes-[Language].md'
>   storage_locations:
>     proposals: '/proposals/[proposal-folder]/minutes/'
>     projects: '/projects/[project-folder]/minutes/'
>     internal: '/projects/internal/minutes/'
>
> quality_standards:
>   - 'All attendees listed with roles and attendance status'
>   - 'Clear distinction between decisions and action items'
>   - 'Every action item has owner and deadline'
>   - 'Meeting objectives stated and addressed'
>   - 'Next steps clearly defined'
>   - 'Distribution list and confidentiality noted'
>
> related_workflows:
>   - 'Create action items in project management tool after finalising'
>   - 'Share minutes within 24-48 hours of meeting'
>   - 'Follow up on action items at next meeting'
>   - 'Archive minutes in appropriate project folder'
>   - 'Link to your CRM / client system for external meetings'
> ```
