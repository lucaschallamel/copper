# Example , a good `activeContext.md`

A worked example of the memory-bank `activeContext.md` file (Rule 03), showing the current-state
structure a next session needs to resume work. Relocated from Rule 03 body under US-341 (referenced
there by one line; on-demand, not always-on).

```markdown
# Active Context

**Last Updated**: 2025-01-20 **Current Sprint**: Sprint 002 (API Development) **Phase**:
Implementation

## Current Work

**Active Item**: Implementing user authentication API endpoint

- Started: 2025-01-19
- Expected completion: 2025-01-21
- Files involved: `/src/api/auth/`, `/src/api/routes/auth.ts`
- Pattern: Using JWT tokens, bcrypt for passwords ([SFT] security-first)

## Recent Changes (Last 3 Sessions)

**2025-01-20**:

- Completed database schema for users table
- Applied [RLS] Row Level Security on users table
- Created migration: `db/migrations/V002__create_users_table.sql`

**2025-01-19**:

- Set up project structure following Rule 01
- Configured dev environment with containerisation (per Rule 00 preference)

**2025-01-18**:

- Initialised project from framework scaffold
- Created memory bank structure

## Next Steps

1. Finish auth endpoint implementation (today)
2. Write unit tests for auth service (≥80% coverage per Rule 02)
3. Create ADR for JWT strategy (Rule 01 requirement)
4. Update progress.md when auth complete

## Active Decisions

**JWT Token Expiry**: Considering 15min access + 7day refresh vs 1hour access only

- Need to decide by: 2025-01-21
- Stakeholders: Security team, product owner
- Leaning toward: 15min+refresh for better security ([SFT])

## Patterns Being Applied

- **Repository Pattern**: Data access layer in `/src/api/repositories/`
- **JWT Authentication**: Standard bearer token approach
- **Input Validation**: Joi schemas for all API inputs ([IV])

## Blockers

None currently. Auth endpoint on track.

## Session Learnings

- Container runtime may require `--network=host` for database connectivity in dev
- Joi validation works better with TypeScript if using `@types/joi`
- Remember to update OpenAPI spec when adding new endpoints
```

**Why this works**:

- **[SD]** Clear current state, next steps, decisions
- **[TR]** Transparent reasoning with principle codes
- **[RP]** Easy to scan, structured sections
- **[CWM]** Contains exactly what next session needs to continue work
