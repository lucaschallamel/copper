---
description: Install, surgically uninstall, or author a capability kit on the current
  host. Runtime kit package manager (install + uninstall + list) plus an authoring
  form (author) that drafts a schema-valid kit.md + skill from a dir, the current
  session, a URL or notes , or, with no source, via a guided interview. Dependency-closure
  resolution, additive-only placement, and checksum-gated removal. Tier-2 white-label
  core.
---

# /cu:kit

Runtime kit package manager for: **$ARGUMENTS**

Loads the `cu:kit-management` skill and invokes the `deploy.kit` package. Tier-2 white-label core , no
organisation identity; the per-target asset prefix is applied by the adapter at install time.

## Forms

```text
/cu:kit install <slug>     # resolve closure (prerequisites first), place additively, write records
/cu:kit uninstall <slug>   # surgical, checksum-gated removal using the install-record
/cu:kit list               # installed kits (from the install-records) + available kits in the source
/cu:kit author [<source>]  # draft from a dir / session / URL / notes , OR, with no source, a guided interview
```

## Behaviour

- **install**: resolves the kit and its `dependencies.kits` closure (pinned-only); refuses on any
  conflict, cycle, or unmet pinned dependency BEFORE touching the host (no silent clobber, no
  partial apply); places each emitted file per its `writeMode`; writes one install-record per kit
  with paths + SHA-256 checksums + provenance.
- **uninstall**: reads the kit's install-record; checksum-gates each delete (a user-modified file is
  preserved and flagged, never blind-deleted); reverses recorded config deltas; refuses if another
  installed kit still depends on this one.
- **list**: reports installed kits (from `<workspace>/.copper/kits/*.install.json`; a legacy
  `.rahan/kits/` store is still read as a fallback, ADR-046) and the installable kits available in
  the source (authoring exemplars are excluded).
- **author**: loads the `cu:kit-authoring` skill and drafts a schema-valid `kit.md` plus skill body.
  WITH a source (a local directory, the current session's context, a doc URL, or pasted notes) it
  drafts from that material; with NO source it runs a **guided interview** (US-266) that elicits the
  kit-1.0 decisions and builds a schema-valid skeleton via `deploy.kit.skeleton.build_kit_skeleton`.
  Providing a source skips the interview by construction. Either way the draft is validated against
  `kit-1.0.schema.json` + COPPER-conformance via the shared `deploy.kit.validate.validate_kit_md`
  (fail-closed) BEFORE writing, emitted INTO the source tree (`kits/core/<slug>/` or
  `kits/_reference/<slug>/`, never the generated host trees), and presented for human review ,
  nothing is auto-committed. If `kits/core/` changes, both checksum manifests are regenerated with
  `uv run python -m deploy.gate update-manifest` (once per host). A bare `learn` universal alias is
  deferred to US-330's allowlist policy; this form ships as a `kit` subcommand only.

## Reference implementation

```bash
# install/uninstall logic (testable Python package)
uv run python -m pytest tests/deploy/kit/ -q
```

The algorithms live in `deploy/kit/` (resolver, adapter, install, uninstall, install_record). Per
ADR-021, per-skill placement will later delegate to the Agent Skills rail; the `deploy/kit/adapter`
module is the seam.

## Safety

- No silent clobber: install refuses on conflict rather than overwriting. Shared-config appends are
  additive-namespaced; a same-pointer collision (or a host-owned non-object on the path) is refused.
- No blind delete: uninstall checksum-gates file removal and value-gates config-key removal; a
  user-modified file or config value is preserved, never clobbered. Reversing one kit's config
  touches only that kit's keys, never another kit's or the host's.
- No secrets in the install-record (plaintext local state): config deltas reference credentials
  indirectly, never the literal value.
- Comment loss on config edit: editing a shared JSONC file (e.g. `opencode.jsonc`) preserves
  structure and key order but DOES NOT preserve comments (the file is structurally re-serialised).
  The deploy system applies the same behaviour to its own merges.

## Related

- Skills: `cu:kit-management` (install/uninstall), `cu:kit-authoring` (the `author` form)
- Spec: `kits/SPEC.md` (section 4: body sections + authoring convention; section 5: install-record +
  adapter seam)
- ADRs: ADR-019 (package-manager model), ADR-020 (install-record), ADR-021 (Agent Skills rail seam),
  ADR-038 (propose-then-approve authoring loop , the `author` form is its authoring corner)
