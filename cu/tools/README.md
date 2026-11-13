# Core Tools

Host-invocable tooling shipped with `kits/core/`, compiled unchanged into every host tree
(`${CLAUDE_PLUGIN_ROOT}/tools/`, `${CLAUDE_PLUGIN_ROOT}/tools/`).

## Contents

On OpenCode 2 the model reaches `pipeline_validator.py` through the `cu-pipeline-validator` plugin
(`kits/core/plugins/cu-pipeline-validator/`, TD-207); the V1 `pipeline-validator.ts` wrapper was
removed because OpenCode 2 does not load `${CLAUDE_PLUGIN_ROOT}/tools/` custom tools. The plugin carries the
SHA-256 of `pipeline_validator.py`, `security_review.py` and `status-vocabulary.json`, baked in at
deploy: edit any of them, then re-run the deploy.

These files are **source**. The copies in each generated host tree are compiler output and are
overwritten by `deploy.regenerate` , edit here, then regenerate, never the other way round.

| File                      | Purpose                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pipeline_validator.py`   | The `/cu:pipe` evidence gate , `verify` (per-stage), `status` (also the status-only state a fresh S7 reviewer reads instead of the YAML, US-395), `audit` (corpus-wide); `verify S10_MERGE` also requires the `merge_approval` record and `pr_url`, recorded not proven (US-399). JSON to stdout; exit 0 pass / 1 validation failure / 2 runtime error. **Discovers the documentation root** (TD-178) rather than assuming `docs-copper/` |
| `security_review.py`      | The S5 security-review evidence check `pipeline_validator.py` runs (US-393): findings JSON and coverage ledger through the vendored `cu:security-audit` validators, or the trust-boundary line against `trust-boundary-paths.json`. Fails closed; an absent path list is a warning                                                                                                                                                           |
| `status-vocabulary.json`  | **The** canonical status vocabularies , `story_status` (TD-171) and `quality_gate_status` (BUG-004). One definition point, consumed by both the pipeline validator and `user-story-validator.py`                                                                                                                                                                                                                                          |
| `push_guard.py`           | The push tripwire (TD-206): judges a `git push` command text and exits 2 when it would update `main`, `master` or the remote's default branch, or cannot be resolved. Run by the `cu` plugin's PreToolUse hook and by the OpenCode 2 plugin in `../plugins/cu-push-guard/`. Standard library, no environment off-switch                                                                                                                   |
| `guard_install.py`        | The primary control (TD-206): `install`, `uninstall`, `status` of the git `pre-push` hook that refuses those pushes for every route (every remote's default branch counts); never overwrites a hook or a hook manager's `core.hooksPath`. Run by the core `guard` command (`/cu:guard`, `/cu:guard`)                                                                                                                                      |
| `format_transcript.py`    | Standalone transcript formatting CLI                                                                                                                                                                                                                                                                                                                                                                                                      |
| `universal-commands.json` | Host command-name registry (active / reserved)                                                                                                                                                                                                                                                                                                                                                                                            |

## Two invariants worth knowing before editing

**The vocabulary file is a trust boundary.** Both validators read their enums from
`status-vocabulary.json` and **fail closed** (`sys.exit(2)`) rather than guessing when it is missing
or malformed. Adding a spelling to silence a red gate defeats the purpose , the file carries an
in-file `$comment` saying so, for both keys.

**`quality_gate_status` classifies rather than equates** (BUG-004). A gate has three outcomes ,
passed, did not apply, did not pass , and anything unrecognised **fails closed**. `pending` counts
as a failure because it means the stage never ran.

**The documentation root is discovered, not assumed** (TD-178). `pipeline_validator.py` resolves it
in three layers , `COPPER_DOCS_ROOT` if set, else the first of `docs-copper/` or `docs/` that
actually **contains** the expected subtree (containment, not mere existence), else the historical
default , so a project keeping its documentation elsewhere is not silently unvalidated. It was
changed LAST of the seven targets, after the six guard scripts had proved the contract: this is the
pipeline's own instrument, and `--root` remains the explicit override.

## Related

- [[../../../tests/unit/README.md]] , unit suites covering these scripts
- [[../skills/backlog-management/scripts/]] , the story/epic validators sharing the vocabulary
- `../plugins/cu-push-guard/index.js` , the OpenCode 2 plugin that runs `push_guard.py`, emitted for
  OpenCode only (no README in `plugins/`: everything there ships to the host's plugin folder)
