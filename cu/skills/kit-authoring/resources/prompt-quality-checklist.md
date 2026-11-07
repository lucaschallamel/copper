# Prompt-quality reviewer checklist

Companion to the asset quality standard in `kit-authoring/SKILL.md`. **This checklist is not
optional and not a summary of the gates** , it is the only control that covers MECE and relevance at
all. The gates catch form; a human catches meaning.

Run it per ASSET for the first four sections, and per KIT for the MECE section.

---

## Concision , script-checkable, verify the justification

- [ ] `wc -l` recorded. Skill ~130 lines, agent ~70 , **medians measured 2026-09-06; re-run before
      relying on them**: `wc -l kits/*/skills/*/SKILL.md kits/*/agents/*.md` (see
      `size-budget-evidence.md` for the full distribution and why the median rather than the mean).
- [ ] If over budget: **is there a written justification, and is it about THIS asset?** "It is
      complex" is not a justification. "Each of its 8 exemption surfaces was added by a named review
      finding and carries its rationale in place" is.
- [ ] The justification names the alternative that was rejected and **why, on the merits** , a
      scheduling reason ("no time", "mid-story") is not a merits reason.
- [ ] **Where it is recorded**: in the asset itself, at the top of the section that makes it large.
      Not in the PR, not in the CHANGELOG , both are read once; the asset is read every time.

## Precision , declared, not described

- [ ] **Skills: mark N/A** , `kits/SPEC.md:211` forbids `tools`/`permission` on a skill file, and 0
      of 155 shipped skills carry one. A skill constrains nothing at runtime.
- [ ] **Agents**: the grant is declared , `capabilities.needs` for kit/1.0, `tools:`+`permission:`
      for a COMPILED host-native agent (where they are REQUIRED , different layers, not old vs new).
      An agent declaring NEITHER has no contract at all.
- [ ] No prose claims a behavioural constraint that frontmatter does not enforce. A permission table
      in the body and a `tools:` key that disagree is worse than either alone.
- [ ] No prose merely restates frontmatter.

## Currency , dated or removed

- [ ] No model name, sampler setting, pinned version, or live count in an always-loaded body.
- [ ] Any perishable content sits in a resource carrying an explicit review date.
- [ ] Counts that will drift ("17 skills", "134 tracked") are derived or removed, never asserted.

## Relevance , does the weight sit where the work is?

- [ ] **No inverted weight**: the description block is not longer than the body it describes.
- [ ] Nothing in the body is documentation ABOUT the asset that no agent reads at runtime , rosters,
      capability matrices, statistics, changelogs. Those belong in a kit README or the manifest.
- [ ] For each major section, answer: **is this read at runtime, or is it about the file?**

## MECE , per kit, not per asset

> **No shipped kit carries a coverage table yet** , measured across all 24, the count is zero. This
> section is a FORWARD obligation on kits authored or uplifted from here, not a retroactive audit of
> the existing corpus. For a single-skill kit the table is one row and trivially satisfied; the
> requirement bites on multi-skill kits, which is where a partition can actually be wrong.

- [ ] A coverage table exists, mapping every capability the kit's `kit.md` `summary` claims to
      **exactly one** owning skill.
- [ ] **Mutually exclusive**: for each capability, name the single skill that must load. **If two
      answers are defensible, the partition is wrong.** Overlap is a defect, not redundancy.
- [ ] **Collectively exhaustive**: every directive extracted from the source has a recorded
      destination. Report **blocks mapped against blocks found** , a pass must not be able to mean
      "mapped nothing".
- [ ] Boundaries are drawn on WHEN knowledge is needed, not on subject-matter tidiness. Two bodies
      always needed together are ONE skill.

## Agent budget , per kit

- [ ] Does each agent need to independently explore, decide and iterate, holding its own context? If
      it is reference knowledge, checklists, or a fixed report template, it is a SKILL.
- [ ] Every agent has a written justification that a command loading a skill cannot do the job.
- [ ] Compare against the precedent: `qd-*` ships 92 personas with ZERO agents.

## Behavioural parity , when uplifting an existing asset

- [ ] The same real task was run against the original and the uplifted version, and the outputs were
      compared.
- [ ] **Concision that changes behaviour is a regression, not an improvement.** This is what stops
      an uplift becoming unbounded rewriting.

---

## Personal data , the class no detector can see (US-355 A1)

**Only for an asset MIGRATED from a private workspace.** `check-personal-data` catches a NAME on a
seeded denylist, the SHAPE of a private artefact (a filled Rule 00, a home path, a symlink), and a
revealing HEADING. It does not catch , and cannot , special-category prose once the name is removed.

**Measured (US-355 S5 A1)**: "Respect the learner's values (vegan, environmentally conscious)" and
"Family commitments (married, 2 daughters)" under a neutral heading pass the gate **completely clean
, exit 0, not even a flag**. In that story the content had already escaped its Rule 00 into two
migratable agents, and a human reading the file is what found it.

- [ ] Every migrated asset has been **read**, not only scanned. The gate's exit 0 is not a read.
- [ ] No statement about a **specific person's** beliefs, politics, health, diet, family, ethnicity
      or sexuality survives , with or without their name attached. These are GDPR Article 9 classes.
- [ ] Where such a statement encoded a reusable METHOD, the method survives and the person does not.
      "married with 2 daughters" becomes "respect the learner's stated constraints, asked for and
      never inferred".
- [ ] A section whose TITLE names a person or their journey is removed wholesale, not parameterised
      , there is no non-personal version of it.
- [ ] Source files that carry such content are on the `never_migrate` list **by path**, which is the
      only half of the control that survives to CI.

## What this checklist does NOT do

It does not replace the gates (`check-frontmatter`, `check-portability`, `check-em-dash`,
`check-core-references`, `check-personal-data`), which catch form and run in CI. It does not make
MECE or relevance mechanically verifiable , they are not.

**If a reviewer skips this checklist, three things are checked by nothing at all**: MECE, relevance,
and , since US-355 , **special-category personal prose in a migrated asset**. The last is the one
with a legal consequence, and it was added because a story measured the gate failing to see it (S5
A1). A skipped checklist is not a lighter review; on that item it is no review.
