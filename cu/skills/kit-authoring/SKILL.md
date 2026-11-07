---
name: kit-authoring
description: Draft a schema-valid kit.md plus skill source from existing material , a local directory, the current session's context, a doc URL, or pasted notes. Use when authoring a NEW kit without hand-writing the frozen kit/1.0 format, while the draft is still schema-validated and human- reviewed like any hand-written source. **Also carries the asset quality standard** , the size budgets, MECE, relevance, precision and currency rules governing EVERY kit asset, drafted or hand-written, plus the reviewer checklist. Tier-2 white-label core (no organisation identity).
version: 1.6.1
last_updated: '2026-10-28'
maintained_by: Lucas Challamel
---

# Kit Authoring

The authoring capability for kits: an agent drafts a schema-valid `kit.md` plus skill body from
existing material, emitting it INTO the source tree (`kits/core/` or the relevant kit dir) as a
normal committable asset. Generation is a one-time UPSTREAM authoring act , the draft is validated
and reviewed exactly like a hand-written kit, so the deterministic compiler, JSON-schema validation,
and checksum manifests run unchanged.

This is Tier-2 white-label core: it carries no organisation identity. The per-target asset prefix is
applied by the adapter at install time, not embedded in the draft.

## Goal

Let an author create a new kit without hand-writing the frozen `kit/1.0` format. The agent drafts a
`kit.md` (frontmatter + the six SPEC-4 body sections) plus a skill body from a source, validates the
draft against `kit-1.0.schema.json` + COPPER-conformance BEFORE writing, presents it for human
review, and emits it into the source tree , never auto-committing.

## When to Use

When an author runs `/cu:kit author [<source>]` (the fourth form of `/cu:kit`, alongside
install/uninstall/list). Two modes: WITH a source, turn a directory, the current session, a doc URL,
or pasted notes into a new kit; with NO source, run the guided interview (US-266) that elicits the
kit-1.0 decisions and builds a schema-valid skeleton via `build_kit_skeleton`. Distinct from
`cu:kit-management` (install/uninstall of an EXISTING kit).

## Setup

- **Source**: one of , a local directory (read its files), the current session's notes/context (the
  agent's own working transcript , NOT arbitrary past conversations), a doc URL (fetch + read), or
  pasted notes.
- **Target contract**: the draft must satisfy `kits/kit-1.0.schema.json` (frontmatter) and the six
  SPEC-4 body sections (`kits/SPEC.md` section 4).
- **Validator**: `deploy.kit.validate.validate_kit_md(path)` , the single shared validator (also the
  standing CI guard). No forked validation logic.

## Steps

**Two entry modes (US-266).** `/cu:kit author <source>` drafts FROM material (Step 1 below).
`/cu:kit author` with NO source enters the **guided interview** first (Step 0), then joins the same
validate -> emit -> review flow. Providing a source SKIPS the interview by construction , the
interview is an aid, never a gate.

0. **No-source guided interview** (only when no source is given). Ask the schema-anchored questions
   below, collect them into an `answers` dict, then call
   `deploy.kit.skeleton.build_kit_skeleton(answers)` to produce a schema-valid kit.md SKELETON
   (filled frontmatter + empty SPEC-4 headings). Proceed to Step 4 (validate) with the skeleton,
   then fill the body sections. The questions map 1:1 to kit-1.0 keys (an authoring-UX aid , the
   schema + `validate_kit_md` remain the governance):

   | Question (ask the author)                                                                                                     | kit-1.0 key         |
   | ----------------------------------------------------------------------------------------------------------------------------- | ------------------- |
   | "What is the kit's short slug (kebab-case)?"                                                                                  | `slug`              |
   | "Which namespace , cm / rg / ta / gd / qd?"                                                                                   | `namespace`         |
   | "Title and one-line summary?"                                                                                                 | `title` / `summary` |
   | "Starting version (semver, e.g. 0.1.0)?"                                                                                      | `version`           |
   | "Which tier , 1 config / 2 core / 3 identity / 4 capability?"                                                                 | `tier`              |
   | "Does it depend on other kits? For each: slug + pinned version."                                                              | `dependencies`      |
   | "Skill always. Does it ALSO need an agent (real tool grant + proactive value) or a command (invocable session)? , the TRIPLE" | `includes`          |

1. **Read the source** and extract the kit's purpose, the capability it provides, and any tool/MCP
   needs.
2. **Decide the entity type , the TRIPLE decision** (agent-earned; never default to a flat skill):
   - **skill** , always emit a skill body (the reusable capability).
   - **agent** , ONLY when the kit needs a real tool grant AND has proactive standalone value.
   - **command** , when the capability should be an invocable `/`-command for a session.
3. **Draft the `kit.md`**: frontmatter (`schema: kit/1.0`, `slug`, `namespace`, `title`, `summary`,
   `version`, `includes`) + the six body sections mapped per entity type (SPEC section 4 table),
   plus the skill body.
4. **Validate BEFORE writing**: call `validate_kit_md` on the draft. If it returns errors, REPORT
   them and do not emit. If the validator dependencies are unavailable, it fails closed , surface
   that, never emit an unvalidated draft.
5. **Emit into source**: write under `kits/core/<slug>/` (a real kit) or `kits/_reference/<slug>/`
   (an authoring exemplar, excluded from install). NEVER write into the generated `.opencode/` /
   `.claude/` trees (build output, regenerated + gitignored). The importable guard
   `deploy.kit.validate.is_legal_emit_path(path)` encodes this boundary , a mechanical writer calls
   it before writing.
6. **Run the quality checklist** (`resources/prompt-quality-checklist.md`) over the draft. The
   validators in step 4 check FORM , schema, frontmatter, portability. They do not check concision,
   MECE or relevance, and nothing else does either. Skipping this step means those three dimensions
   are checked by nothing at all.
7. **Complete the mechanical tail , adding an asset is never just the asset (US-356 S4).** These are
   consequences of the operation, not story-specific work, and EVERY EP-108 story hit at least one
   of them at a GATE rather than in its plan:
   - **`kit.md capabilities.needs`** must be the UNION of its assets' needs. A new asset that reads
     or writes files widens it. The `sign_kits --check` capability gate REFUSES a kit whose manifest
     understates what its assets do.
   - **`kit.md version`** , MINOR for a new asset, per Rule 04's decision test.
   - **The per-asset `CHANGELOG.md` entry** , named per asset path, not grouped. The TD-175
     asset-versioning gate resolves each path to its own section.
   - **The corpus pin** in `tests/unit/test_register_economics.py` , adding files to `kits/` moves
     it. Bump it WITH provenance (the test's own convention), never silence it.
   - **Both checksum manifests**, if `kits/core/` changed , once per host:
     `uv run python -m deploy.gate update-manifest --core kits/core --target opencode --manifest kits/core/.checksums.json`
     and `... --target claude-code --manifest kits/core/.checksums.claude-code.json`.
   - **Re-sign**, if anything under `kits/` changed , editing a kit invalidates its Ed25519
     signature.
   - **A bidirectional link**, if the new asset requires an existing one , the existing asset must
     name the new one too, or the capability is correct but unfindable (US-356 S4 F1).
8. **Check what the gates CANNOT (US-356 S7).** The battery checks structure, versioning,
   signatures, manifests, determinism, privacy shapes and tests. It reads neither intent nor
   requirements, so **green is not evidence of these two**, and both were missed by four green gates
   and two reviews in one story:

   - **Verify each acceptance criterion against the SHIPPED ARTEFACT**, not against the diff and not
     against your memory of building it. A review scoped to the diff **cannot see an omission** , an
     unbuilt requirement appears in no diff. Where a plan deliberately supersedes an AC's MECHANISM,
     UPDATE THE AC in the same breath: superseding a mechanism is legitimate, silently dropping its
     INTENT is a defect.
   - **Re-read the asset's own warning or disclosure section whenever you widen what the asset
     DOES.** Nothing couples a disclosure to the behaviour it describes, so a warning silently stops
     being true. Grep it for the new data class or capability before committing.

9. **Present for review; do not commit**: show the draft and STOP. The author reviews and commits.

## Asset quality standard (US-352, US-357)

Five dimensions govern every kit asset: **concision, MECE, relevance, precision, currency**. Only
the first is fully mechanically checkable , see "What a script can and cannot check" below, and the
reviewer checklist at `resources/prompt-quality-checklist.md` for the rest.

> **This file exceeds its own budget, with a recorded justification , the standard applied to
> itself.** It is roughly **2x** the ~130-line skill budget , **run `wc -l` on this file rather than
> trusting a number written here.** Two earlier drafts of this blockquote asserted "222" and "231";
> both were stale within one edit. An asserted count in an always-loaded body is exactly what the
> Currency rule below forbids, and this line kept proving it.
>
> **The composition**: ~120 lines pre-date this standard (the authoring guidance in Goal / Steps /
> Constraints); the quality standard is the remainder. Reference material , the measured
> distribution and the worked exceedance , was moved to `resources/` rather than kept inline, which
> is the correct fix and the reason the file is not larger still.
>
> **The rejected alternative, on the merits**: splitting this into two skills (`cu:kit-authoring` and
> `kit-quality-standard`). Rejected because the bar belongs beside the flow it governs , an author
> reading how to build a kit should meet the standard in the same file, not be expected to find a
> second one. Co-location is the point, and the split would trade a real usability property for a
> line count. A reviewer who disagrees with that trade should say so; the argument is on the merits,
> not on story timing.

### Agent budget , the fewest agents that genuinely need agency (US-352)

**A kit ships the fewest agents that genuinely need autonomous multi-step reasoning. Reference
knowledge is carried as SKILLS the agent loads on demand. One agent over ten skills is preferred to
ten agents with none.**

Adding an agent requires a written justification that a command loading a skill cannot do the job.

**The sorting test.** Does the asset need to independently explore, decide, and iterate, holding its
own context across steps? That is an agent. Is it mostly reference knowledge, checklists, or a fixed
report template? That is a skill. Is it a deterministic parametrised transform with defined inputs
and outputs? That is a command.

**Why it matters more for skills than agents.** An agent is SELECTED by the model reasoning over
descriptions, so a near-miss degrades gracefully. Skills are LOADED on demand, so a bad partition
compounds: overlapping skills mean either both load (duplicate tokens, and where they have drifted,
contradictory guidance inside one context window) or the wrong one loads and the needed knowledge
never arrives. A gap is worse , the agent proceeds confidently, unaware anything is missing. Once
the agent is thin, **the skill library IS the capability**, so its partition quality is the kit's
quality. Draw skill boundaries on WHEN knowledge is needed, not on subject-matter tidiness.

**The precedent** , `qd-coaches`, `qd-masters` and `qd-smes` ship their whole persona corpus as
skill+command pairs with **zero agents** (the count is in `resources/size-budget-evidence.md`,
dated, because an asserted count in an always-loaded body is exactly what the Currency rule
forbids). `gd-*` kits keep agents for work that genuinely explores and iterates (code review,
security analysis). Both are in this repo; compare before adding an agent.

**The anti-pattern** , a single agent discharging seven roles at once, most of it reference
knowledge resident in context on every invocation. Bulk is the symptom; the cause is knowledge that
should have been a loadable skill.

### Concision , the size budget

**Skills ~130 lines, agents ~70**, anchored on the measured MEDIAN of the shipped corpus. Exceeding
is permitted with a recorded justification , a review trigger, not a cap.

The full distribution, the measurement command and date, why the median rather than the mean, and a
worked example of a justified exceedance are in
[`resources/size-budget-evidence.md`](resources/size-budget-evidence.md). **Re-measure rather than
trust the figure** , the earlier budget in this file was a survivorship sample that propagated
because nobody re-ran it.

### MECE , the partition IS the capability (US-352)

**The rule is stated once, in the agent-budget section above.** Restating it here would be two
statements of one rule , which is what drifts.

**What a kit ships to prove it**: a coverage table mapping every capability to **exactly one**
owning skill. The test is behavioural , for each capability, name the single skill that must load.
If two answers are defensible, the partition is wrong.

**What "capability" means here**, because `kit.md`'s one-line `summary` does not enumerate them:
derive the list from `includes.skills` plus each skill's `description` , one row per distinct thing
a skill claims to do. A single-skill kit satisfies this in one row; the requirement bites on
multi-skill kits, where a partition can actually be wrong.

**No shipped kit carries such a table yet** (measured across all 24: zero). This is a forward
obligation on kits authored or uplifted from here, not a retroactive audit , stated so a reviewer
does not fail every existing kit and learn to skip the section.

**A worked example** , retrofitted to `gd-quality` (4 skills), including where the table lives and
what a FAILING one looks like , is in
[`resources/size-budget-evidence.md`](resources/size-budget-evidence.md).

### Relevance , does the weight sit where the work is?

An asset's bulk should be the thing it is for. The recurring failure is **inverted weight**: a
66-line agent body behind a 4,000-character description block; rosters, capability matrices and
framework statistics that no agent reads at runtime but that every author must maintain.

Ask: **what in this file is read at runtime, and what is documentation about the file?** The second
belongs in a kit README or the manifest, not in a body loaded into context on every invocation.

### Precision , declared, not described

**Every constraint expressible as frontmatter IS frontmatter.** Rule 07 Control 2 is explicit: a
prose claim that an agent is read-only is a comment, not a control. The declared grant is the
contract.

**Know which dialect you are writing.** The key differs, and naming the wrong one makes this rule
unanswerable:

| target                     | the declaration                                                                                                                                         |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| kit/1.0 agent              | `capabilities.needs` + `capabilities.optional` (`kits/SPEC.md:203-204`)                                                                                 |
| compiled host-native agent | `tools:` + `permission:` , **REQUIRED** by `cu:framework-authoring`'s frontmatter contract and enforced by `check-frontmatter.py`; 20 of 63 shipped agents |
| **skill**                  | **neither** , `kits/SPEC.md:211`: "No tools/permission on the skill file". This dimension is **N/A for skills**; a skill constrains nothing at runtime. |

**These are LAYERS, not a new dialect replacing an old one** (S5 G5 , "legacy" was the wrong word
and actively misleading). `capabilities.needs` is the kit/1.0 **source** declaration; `tools:` and
`permission:` are what the adapter **compiles it into**, and they are REQUIRED on a compiled
host-native agent , stripping them to "modernise" a compiled asset breaks `check-frontmatter.py`.
Which one you write depends on which layer you are authoring, not on which is newer.

Measured 2026-09-07: of 63 shipped agents, 45 declare `capabilities`, 20 use `tools:`. An agent
declaring **neither** has no contract at all , that is the defect this rule is for.

Prose that merely restates frontmatter is removed. A permission table in the body and a `tools:` key
that disagree is worse than either alone, because a reader cannot tell which one binds.

### Currency , perishable content is dated or removed

Model names, sampler settings, pinned versions, live counts ("134 tracked, 29 answered") and
capability claims about a moving target all rot. An asset carrying "Current AI Limitations (2025)"
in an always-loaded body ships staleness to every future reader.

**No perishable claim sits in an always-loaded body.** Either remove it, or isolate it in a resource
carrying an explicit review date, so the next author knows what to re-check rather than assuming it
still holds.

### What a script can and cannot check

Stating this is part of the standard, not a caveat on it. A standard that implies automation it does
not have produces the same false assurance as a gate that claims semantic detection , the reader
stops looking because they believe something else is watching.

| Dimension     | Mechanisable? , **no gate implements any of these today**                                                                           |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Concision** | **Yes** , `wc -l` against the budget, plus a required justification when exceeded                                                   |
| **Precision** | **Partly** , a script sees whether `tools:` exists; not whether prose restates it                                                   |
| **Currency**  | **Partly** , a denylist of model names and version pins is greppable; judgement is not                                              |
| **MECE**      | **No, for the substance** , a script can check a coverage table is complete and single-owner, but not that the partition is CORRECT |
| **Relevance** | **Partly** , the description:body ratio IS computable (inverted weight); whether the weight sits where the work is, is human        |

**No gate implements ANY of this today.** The table says what COULD be mechanised, not what is
watching. The existing gates (`check-frontmatter`, `check-portability`, `check-em-dash`,
`check-core-references`, `check-personal-data`) check other things entirely , none reads a line
count or a coverage table. Claiming otherwise would be the same false assurance this section warns
about in its next paragraph.

**So the gates catch form; the reviewer checklist catches meaning.** That is why
`resources/prompt-quality-checklist.md` exists and is not optional , it is the only control covering
MECE, relevance, and **special-category personal prose in a migrated asset**. The last was added at
US-355, which MEASURED `check-personal-data` passing Article 9 content clean once the name was
removed (exit 0, not even a flag). That item carries a legal consequence, which the other two do
not.

## Constraints

- **Emit into SOURCE only** , `kits/core/` or `kits/_reference/`, never the generated host trees.
- **Validate before write** , a schema-invalid draft is reported, never silently emitted; validation
  fails closed if its dependencies are absent.
- **Never auto-commit** , the schema gate + human review ARE the propose-then-approve approval gate
  (no autonomy is implied). The command never runs `git commit`.
- **Reuse, do not fork** , validation goes through `validate_kit_md`; the round-trip parses through
  the real manifest loader (`LocalKitSource.load`), not a re-implementation. (Full compile via
  `load_kit`/`compile_kit` is exercised by the standing determinism gate over the whole tree, not by
  the per-draft round-trip.)
- **White-label** , the draft and this skill name the ROLE / capability, never a specific
  `ra-`/`ta-` kit agent or organisation identity. The guided interview (US-266) and the `/distill`
  detected- workflow source (US-274) are OUT of this skill's scope.

## Safety Notes

- **Unvalidated emit is the core hazard** , a malformed `kit.md` that reaches `kits/core/` would
  poison the compiler and checksum run for every downstream install. The pre-write `validate_kit_md`
  gate (fail-closed) is the defence; do not bypass it.
- **Wrong emit target is a silent-loss hazard** , a draft written into `.opencode/`/`.claude/` is
  overwritten on the next compile and never committed. Always resolve the write path under `kits/`.
- **No secrets in a draft** , if a kit needs a credential it is referenced indirectly (env-var name,
  secret-manager path) in `hostConfig`, never as a literal value (mirrors the install-record
  no-secrets rule).
- **`hostConfig` targets are allowlisted** , the installer writes only the files on its allowlist
  (today `opencode.jsonc.example`; never `.claude/settings.json`, whose `hooks` run commands, nor
  the live `opencode.jsonc`). Any other `target` fails the build. See `kits/SPEC.md` 5.1.
