# Example , Task Genius task management

A worked example of Task Genius notation (Rule 02 GTD integration) across an authentication-module
feature, showing the 8 status characters in a realistic multi-phase plan. Relocated from Rule 02
body under US-341 (referenced there by one line; on-demand, not always-on). The normative spec , the
8-symbol table and the Mandatory GTD Compliance list , stays in Rule 02.

**Good Task Management** **[TSP]**:

```markdown
## Feature Development - Authentication Module

### Analysis Phase

- [x] Review security requirements (Completed: 2025-01-20)
- [/] Design JWT token strategy (In progress: 60% complete)
- [?] Clarify token expiry requirements (Question sent to security team)

### Implementation Phase

- [>] Implement token generation (Assigned: @backend-team, Due: 2025-01-26)
- [!] URGENT: Fix rate limiting issue (Deadline: 2025-01-25)
- [<] Security code review (Scheduled: 2025-01-26 14:00)

### Testing Phase

- [ ] Write unit tests for auth service (Target: ≥80% coverage)
- [-] Alternative authentication method (Cancelled: JWT standard adopted)
- [<] Integration testing (Scheduled: 2025-02-01)
```

The example above demonstrates the formatting practices Rule 02 states normatively (specific action
verbs, `[>]` ownership, `[<]` deadlines, `[!]` urgency, status kept current); that one-line guidance
lives in Rule 02 and is not restated here.
