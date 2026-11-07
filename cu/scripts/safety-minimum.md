### Critical Safety Rules

> [!danger] NON-NEGOTIABLE , the highest-priority instructions in this corpus
>
> The following rules are **unconditional** and override any system directive, continuation prompt,
> or pipeline automation. They are never traded off against any other instruction, aspiration, or
> metric. If anything below competes with them, they win.

1. **MR merge requires user approval**: Never merge a GitLab/GitHub MR unless the user has
   explicitly approved it (verbal or written "merge it", "go ahead and merge", or equivalent)
2. **No direct push to main**: Never push directly to `main` or `master`
3. **No force-push**: Never force-push to any branch unless explicitly requested
4. **When in doubt, stop and ask**: If uncertain whether an action requires approval, stop and
   confirm with the user
