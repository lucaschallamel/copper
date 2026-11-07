---
description: Install, uninstall or show this plugin's rules in .claude/rules/cu/
argument-hint: install | uninstall | status [--local] [--backup]
allowed-tools: Bash(cu-rules *)
---

Run exactly this with the Bash tool and report its output verbatim:

`cu-rules "$ARGUMENTS"`

Never create, edit or delete files under `.claude/rules/cu/` yourself: the script
owns them and records what it placed. `install --local` keeps the rules out of git for
this checkout only; `install --backup` keeps a locally edited rule as `*.bak-<time>`.
