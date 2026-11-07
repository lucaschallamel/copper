# Core Tools

Host-invocable tooling shipped with `kits/core/`, compiled unchanged into every host tree
(`${CLAUDE_PLUGIN_ROOT}/tools/`, `${CLAUDE_PLUGIN_ROOT}/tools/`).

## Contents

These files are **source**. The copies in each generated host tree are compiler output and are
overwritten by `deploy.regenerate` , edit here, then regenerate, never the other way round.

| File                      | Purpose                                                                                                                                                                                                                                       |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pipeline_validator.py`   | The `/cu:pipe` evidence gate , `verify` (per-stage), `status`, `audit` (corpus-wide). JSON to stdout; exit 0 pass / 1 validation failure / 2 runtime error. **Discovers the documentation root** (TD-178) rather than assuming `docs-copper/` |
| `pipeline-validator.ts`   | Thin host tool wrapper that shells out to `pipeline_validator.py`                                                                                                                                                                             |
| `status-vocabulary.json`  | **The** canonical status vocabularies , `story_status` (TD-171) and `quality_gate_status` (BUG-004). One definition point, consumed by both the pipeline validator and `user-story-validator.py`                                              |
| `format_transcript.py`    | Standalone transcript formatting CLI                                                                                                                                                                                                          |
| `universal-commands.json` | Host command-name registry (active / reserved)                                                                                                                                                                                                |

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
