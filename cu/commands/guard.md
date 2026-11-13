---
description: 'Install, remove or check the git pre-push guard: it refuses any direct
  push to main or master'
---

# Pre-push guard

Install, remove or check this repository's git `pre-push` guard (TD-206): the hook git runs before
every push, which refuses a push that would update `main`, `master` or the remote's default branch,
whatever started it. The in-session push guards are early warnings; this hook is the control.

Run this with the shell tool, from the repository root, and report its output verbatim. It finds the
installer in this deployment's tools folder (a project `${CLAUDE_PLUGIN_ROOT}/tools`, a `${CLAUDE_PLUGIN_ROOT}/tools`, or a
global OpenCode install), so do not hardcode one:

```bash
T=${CLAUDE_PLUGIN_ROOT}/tools/guard_install.py
[ -f "$T" ] || T=${CLAUDE_PLUGIN_ROOT}/tools/guard_install.py
[ -f "$T" ] || T="$HOME/.config/opencode/tools/guard_install.py"
python3 "$T" "$ARGUMENTS"
```

Pass the argument only if it is exactly `install`, `uninstall` or `status`; for anything else, or no
argument, run `status` and say so. If `python3` is not found, run the last line with `python`, then
`py -3`.

Never write, edit or delete the hook yourself, and never offer to merge it into another hook: the
script refuses when a hook or a hook manager (husky, lefthook) is already there, and prints what to
add, so the user decides. Report a refusal as it is.
