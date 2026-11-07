---
title: 'Multilingual Documentation'
version: '1.0.1'
last_updated: '2026-10-18'
maintained_by: 'Lucas Challamel'
---

# Multilingual Documentation

Moved out of Rule 04 by US-378 (ADR-054): language priority and the folder structure for
multilingual documentation.

## Documentation for Multilingual Projects

Support the languages the organisation's market needs; Rule 00 (Communication and Interaction
Standards) sets them. (`[RSP]` is Environmental Responsibility, Rule 02a, not this.)

### Language Priority

1. **Primary**: British/International English (en-AU) for all technical documentation
2. **Secondary languages** (from Rule 00): client-facing documentation when requested, for example
   French for a French-speaking market or German for German-speaking clients

### Multilingual Documentation Structure

**Approach**: Separate language versions in dedicated subfolders

**Example**:

```
/customer/
├── en/
│   ├── user-guide.md
│   └── api-documentation.md
├── fr/
│   ├── guide-utilisateur.md
│   └── documentation-api.md
└── de/
    ├── benutzerhandbuch.md
    └── api-dokumentation.md
```

**Synchronisation**: Maintain version parity across language versions.

---
