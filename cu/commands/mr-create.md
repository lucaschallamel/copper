---
description: Create a GitLab merge request or GitHub pull request with safety gates,
  metadata generation, secret scanning, and user confirmation. Auto-detects platform
  from git remote. Supports standalone use and cu-pipe S10 delegation.
---

> **Documentation root (TD-178)**: paths below are written against the default `docs-copper/`. A
> project whose documentation lives elsewhere (for example `docs/`) is discovered automatically by
> the guard scripts, or pinned with `COPPER_DOCS_ROOT`. Read `docs-copper/` here as "the
> documentation root", not as a literal path.

# /cu:mr-create

Create a merge request (GitLab) or pull request (GitHub) for: **$ARGUMENTS**

---

## Overview

This command creates a GitLab merge request or GitHub pull request with safety gates, automatic
metadata generation, a secret/PII scan, and a hard user confirmation gate before submission. It
auto-detects the git platform from the remote URL and uses the appropriate CLI (`glab` for GitLab,
`gh` for GitHub).

**Delegated from**: cu-pipe S9_CLOSE (MR creation step) **Also callable**: standalone for ad-hoc
merge/pull requests outside the pipeline

**This command never merges.** Merging requires the explicit user approval rule in AGENTS.md section
"Git Safety".

---

## Platform Detection (Step 0)

**Run before any gates.** Determine the platform and default branch.

### 0a. Detect Platform from Remote

```bash
REMOTE=$(git remote get-url origin 2> /dev/null || echo "")
```

| Remote Pattern                                                                    | Platform | CLI Required                                                                                                                    |
| --------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Hostname contains `github.com`                                                    | `github` | `gh`                                                                                                                            |
| Hostname contains `gitlab` OR `glab auth status` reports a configured GitLab host | `gitlab` | `glab`                                                                                                                          |
| Neither                                                                           | **FAIL** | Abort: "Cannot detect git platform from remote URL. Set origin to a GitHub or GitLab remote, or check your glab configuration." |

**Detection rules**:

- Match against the hostname component of the URL (not pathname substrings). For SSH URLs
  (`git@host:path`), extract the host. For HTTPS URLs (`https://host/path`), extract the host.
- GitLab detection: match `gitlab` in hostname, OR if `glab` is installed and reports a configured
  GitLab host via `glab config get -g host` (handles self-hosted GitLab on custom domains like
  `code.acme.io`).
- GitHub detection: match `github.com` in hostname. GitHub Enterprise (`github.acme.corp`) is not
  auto-detected in this version; set the remote accordingly or contribute a patch.
- If the URL is ambiguous (matches both), prefer GitLab if `glab` is installed, otherwise GitHub.

Store the detected platform as `$PLATFORM` (either `github` or `gitlab`) for use in subsequent
gates.

### 0b. Detect Default Branch

```bash
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2> /dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")
```

If detection fails (no HEAD ref on origin), fall back to `main`. Use `$DEFAULT_BRANCH` throughout
all subsequent gates and commands instead of hardcoding `main`.

---

## Execution Protocol

Run the gates **in order**. Stop at the first failure. Present clear remediation guidance.

### Gate 1: CLI Availability

**Platform-specific check** based on `$PLATFORM` from Step 0.

#### GitLab (`glab`)

**Check A - Installed**:

```bash
which glab
```

**On failure**: Provide installation instructions:

```bash
# macOS
brew install glab

# Linux (official source)
# See https://gitlab.com/gitlab-org/cli/-/releases for latest
curl -sL https://gitlab.com/gitlab-org/cli/-/releases/v1.52.0/downloads/glab_1.52.0_linux_amd64.tar.gz | tar xz
sudo mv glab /usr/local/bin/
```

**Check B - Authenticated**:

```bash
glab repo view 2>&1
```

If output contains `authentication required`, `401`, `permission denied`, or `not found`:

```bash
glab auth login
```

> **Note**: Authentication failures can also be caused by repository permissions, network issues, or
> expired tokens. If `glab auth login` succeeds but `glab repo view` still fails, check repository
> access and network connectivity.

#### GitHub (`gh`)

**Check A - Installed**:

```bash
which gh
```

**On failure**: Provide installation instructions:

```bash
# macOS
brew install gh

# Linux (Debian/Ubuntu)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh
```

**Check B - Authenticated**:

```bash
gh auth status 2>&1
```

If output contains `not logged in` or `authentication required`:

```bash
gh auth login
```

**Evidence to record**:

```yaml
mr_creation:
  gate_1_cli:
    platform: gitlab | github
    status: pass | fail
    evidence: 'glab X.Y.Z installed and authenticated | gh X.Y.Z installed and authenticated'
```

---

### Gate 2: Working Tree Clean and Safe

```bash
git status --porcelain
```

**What it checks**: All changes are committed. No unstaged or untracked files.

**Additional check - secret file detection**:

```bash
git ls-files --cached --others --exclude-standard | grep -iE '\.env|\.pem|\.key|id_rsa|secrets\.|credentials\.'
```

**On failure (uncommitted files)**:

- List the uncommitted files
- Suggest: `git add -A && git commit -m "chore: pending changes"` or `git stash`
- Re-run Gate 2 after resolution

**On failure (secret files detected)**:

- List the detected files
- Warn: "Potential secret or credential files detected. Review and ensure these are in .gitignore."
- Abort until resolved

**Evidence to record**:

```yaml
mr_creation:
  gate_2_clean_tree:
    status: pass | fail
    evidence: 'git status --porcelain returned empty; no secret files detected'
```

---

### Gate 3: Branch Verification

```bash
CURRENT=$(git branch --show-current)
```

**What it checks**:

1. Not on `main`, `master`, or `$DEFAULT_BRANCH`
2. Not in detached HEAD state (empty output from `git branch --show-current`)

**On failure (default branch)**: Abort with message: "You are on `$DEFAULT_BRANCH`. Switch to a
feature branch first using `git checkout -b feature/<story>-<description>`."

**On failure (detached HEAD)**: Abort with message: "Detached HEAD state detected. Checkout a branch
first using `git checkout <branch-name>`."

**Evidence to record**:

```yaml
mr_creation:
  gate_3_branch:
    status: pass | fail
    evidence: 'Current branch: feature/us-137-cu-mr-create-command'
```

---

### Gate 4: Commit Existence

```bash
git log $DEFAULT_BRANCH..HEAD --oneline
```

**What it checks**: The feature branch has at least one commit not on the default branch.

**On failure**: Abort with message: "No commits on this branch vs `$DEFAULT_BRANCH`. Commit your
changes before creating an MR."

**Evidence to record**:

```yaml
mr_creation:
  gate_4_commits:
    status: pass | fail
    evidence: 'N commits ahead of DEFAULT_BRANCH'
```

---

### Gate 5: Remote Push Status

```bash
git status --branch --porcelain
```

**What it checks**:

1. Look for `ahead` in the branch status line. The feature branch must be fully pushed to the
   remote.
2. Also check that an upstream is configured. If
   `git rev-parse --abbrev-ref --symbolic-full-name @{u}` fails, the branch has no upstream and Gate
   5 fails.

**On failure (ahead of remote)**:

```bash
git push -u origin <branch-name>
```

Re-run Gate 5 after push.

**On failure (no upstream)**:

```bash
git push -u origin <branch-name>
```

Re-run Gate 5 after push.

**Evidence to record**:

```yaml
mr_creation:
  gate_5_push:
    status: pass | fail
    evidence: 'Branch up to date with origin'
```

---

### Gate 6: Idempotency Check

**Check that no open MR/PR already exists for this branch.**

#### GitLab

```bash
glab mr list --source-branch opened < branch-name > --state 2>&1
```

#### GitHub

```bash
gh pr list --head open < branch-name > --state 2>&1
```

**On failure (existing MR/PR found)**: Present the existing MR/PR URL and ask user:

- A) Use the existing MR/PR (abort creation)
- B) Close the existing MR/PR and create a new one
- C) Cancel

**Evidence to record**:

```yaml
mr_creation:
  gate_6_idempotency:
    status: pass | fail
    evidence: 'No open MR/PR found for branch <branch-name>'
```

---

## MR Metadata Generation

### Title Fallback Chain

Generate the MR title using the **first successful source** in this priority order:

| Priority | Source                                    | How                                                                                                                             |
| -------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 1        | `$ARGUMENTS` (if provided and not a flag) | Use directly as title                                                                                                           |
| 2        | Pipeline YAML                             | Read `docs-copper/roadmap/pipeline-audit-trail/<STORY>.yaml` and matching story file frontmatter `title`                        |
| 3        | Story file                                | Read `docs-copper/roadmap/backlog/<STORY>*.md` frontmatter `title`                                                              |
| 4        | Branch name                               | Parse `feature/us-137-cu-mr-create-command` or any prefix (bugfix/, chore/, td-NNN-, ep-NNN-, etc.) into a human-readable title |
| 5        | Error                                     | Fail with "Cannot determine MR title. Provide a title via $ARGUMENTS."                                                          |

**Branch name parsing rules**:

- Extract the story-type prefix and slug: `feature/us-137-cu-mr-create-command` becomes
  `US-137: cu-mr-create-command`
- Support all story-type prefixes: `us-`, `ep-`, `td-`, `ci-`, `sp-`, `bg-`, and generic prefixes
  like `feature/`, `bugfix/`, `chore/`, `release/`
- Capitalise the story-type prefix: `us-` becomes `US-`, `td-` becomes `TD-`

### Description Generation

Generate the MR description and write it to a **temporary file** (`$DESC_FILE`). This avoids shell
injection when passing the description to CLI tools.

#### Content Sources

1. **Story metadata**: Extract `story_id`, `epic`, `story_points` from story file frontmatter. If no
   story file is found, use `N/A` for each field.
2. **Commit log**: `git log $DEFAULT_BRANCH..HEAD --oneline` for the key deliverables list
3. **Change surface**: Read from pipeline YAML `change_surface` section. If absent (standalone use),
   omit the Change Surface section.

#### Template

```markdown
## Summary

[Story title from backlog]

**Story**: [story_id or N/A] | **Epic**: [epic or N/A] | **Points**: [story_points or N/A]

### Change Surface

- Code: [true/false]
- Docs: [true/false]
- Tests: [true/false]
- Architecture: [true/false]

### Key Deliverables

- [commit 1 summary]
- [commit 2 summary]
- [commit N summary]

### Verification

- Commit: [the pushed commit's sha]
- Local battery: [passed] passed, [failed] failed, [skipped] skipped, exit [code]

Exit 0 is the only pass; exit 2 means a gate could not be run.
```

**Verification is not optional.** Fill it from the battery run on the pushed commit (under cu-pipe,
the S10 evidence). If no battery ran, write "Local battery: not run" rather than omitting the
section: an unverified change must not read as a checked one (Rule 07 Control 5). This block is the
merge evidence where no CI runs, and `--body-file` bypasses any repository PR template, so it cannot
be left to one.

Write the rendered description to a temp file:

```bash
DESC_FILE=$(mktemp /tmp/mr-description-XXXXXX.md)
# Write description content to $DESC_FILE
```

### Secret/PII Scan

**Before presenting the description to the user, scan all content for secrets and PII.**

Scan the description file and the commit log for patterns:

| Pattern                                          | Matches                      | Action                               |
| ------------------------------------------------ | ---------------------------- | ------------------------------------ |
| `sk-[a-zA-Z0-9]{20,}`                            | OpenAI/API keys              | **BLOCK**: Redact and abort          |
| `glpat-[a-zA-Z0-9\-]{20,}`                       | GitLab PATs                  | **BLOCK**: Redact and abort          |
| `ghp_[a-zA-Z0-9]{36}`                            | GitHub PATs                  | **BLOCK**: Redact and abort          |
| `gho_[a-zA-Z0-9]{36}`                            | GitHub OAuth tokens          | **BLOCK**: Redact and abort          |
| `AKIA[0-9A-Z]{16}`                               | AWS access keys              | **BLOCK**: Redact and abort          |
| `xox[baprs]-[a-zA-Z0-9\-]{10,}`                  | Slack tokens                 | **BLOCK**: Redact and abort          |
| `-----BEGIN (RSA \|EC \|DSA )?PRIVATE KEY-----`  | Private keys                 | **BLOCK**: Redact and abort          |
| `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}` | Email addresses              | **WARN**: Flag for review            |
| `Closes #\d+` / `Fixes #\d+`                     | GitHub auto-close directives | **WARN**: May close unrelated issues |

**On BLOCK**: Abort MR creation. Display the offending pattern (redacted). Do not publish.

**On WARN**: Include warning in the user confirmation preview. Proceed only after user acknowledges.

**Evidence to record**:

```yaml
mr_creation:
  secret_scan:
    status: pass | block | warn
    evidence: 'No secrets or PII detected in commit log or description'
    warnings: []
```

---

## Summary Report

After all gates pass and before the Hard Gate, display a structured summary:

```text
=== Gate Summary ===

  Gate 1 (CLI Available):        PASS  [platform: gitlab, glab 1.52.0]
  Gate 2 (Clean Tree):           PASS  [no uncommitted changes, no secret files]
  Gate 3 (Branch Check):         PASS  [feature/us-137-cu-mr-create-command]
  Gate 4 (Commits Exist):        PASS  [4 commits ahead of main]
  Gate 5 (Push Status):          PASS  [branch up to date with origin]
  Gate 6 (Idempotency):          PASS  [no open MR for this branch]
  Secret Scan:                   PASS  [no secrets or PII detected]

  Platform:       [GitLab | GitHub]
  Default Branch: [main | master | develop]
  Title:          [generated title]
  Description:    [N lines in temp file]
```

---

## Hard Gate: User Confirmation

**STOP HERE. Do NOT create the MR/PR yet.**

Present the following to the user:

```text
=== MR/PR Creation Summary ===

Platform:       [GitLab | GitHub]
Title:          [generated title]
Branch:         [source] -> [DEFAULT_BRANCH]
Commits:        [N commits]
Draft:          [yes/no]

Secret scan:    [PASS / WARN: N warnings listed below]

Description preview:
---
[description excerpt, first 15 lines]
---

Options:
  A) Create MR/PR now
  B) Edit title or description before creating (provide corrected values inline)
  C) Cancel
```

**Wait for user response**. Only proceed with option A or B.

If option B: accept corrected title and/or description from the user, update the temp file, and
re-present the summary.

---

## MR/PR Creation

Execute only after user confirmation (Hard Gate passed). Use the platform detected in Step 0.

### Critical: Safe Argument Passing

**Both CLIs receive the description from a file to prevent shell injection.**

- **GitHub (`gh`)**: Use `--body-file "$DESC_FILE"` (native file-based input)
- **GitLab (`glab`)**: Use `--description "$(cat "$DESC_FILE")"`. Although this uses shell
  substitution, the content originates from a controlled temp file (not user input), and the
  `$(cat ...)` idiom preserves literal content without further expansion. For maximum safety,
  consider piping: `cat "$DESC_FILE" | glab mr create --description -`

### GitLab (`glab`)

```bash
glab mr create \
  --title "[TITLE]" \
  --description "$(cat "$DESC_FILE")" \
  --target-branch "$DEFAULT_BRANCH" \
  $DRAFT_FLAG \
  --remove-source-branch \
  --no-editor
```

**Important**:

- Do NOT use `--yes` (the hard gate replaces it)
- Do NOT use `--assignee` (known issue with some GitLab configurations)
- Do NOT use `--push` (Gate 5 already verified push status)
- `$DRAFT_FLAG` is either `--draft` or empty string based on user preference
- `--remove-source-branch` deletes the source branch after merge. For regulated engagements
  requiring audit evidence retention, omit this flag or use `--keep-source-branch` if available.

### GitHub (`gh`)

```bash
gh pr create \
  --title "[TITLE]" \
  --body-file "$DESC_FILE" \
  --base "$DEFAULT_BRANCH" \
  $DRAFT_FLAG \
  --no-browser
```

**Important**:

- Do NOT use `--yes` (the hard gate replaces it)
- `--body-file` reads description from the temp file (native file-based input, no injection risk)
- `$DRAFT_FLAG` is either `--draft` or empty string based on user preference
- GitHub does not auto-delete source branches. Manual cleanup after merge may be needed.

### Cleanup

After successful MR/PR creation, remove the temp file:

```bash
rm -f "$DESC_FILE"
```

---

## Post-Creation Verification

After `glab mr create` or `gh pr create` executes:

1. **Check exit code**: Must be 0
2. **Parse URL**: Extract from output (look for `https://` URL)
3. **Parse reference**:
   - GitLab: Look for `!N` merge request reference
   - GitHub: Look for `#N` pull request reference
4. **Present result**:

```text
=== MR/PR Created Successfully ===
  Platform:       [GitLab | GitHub]
  URL:            [URL]
  Reference:      [!N or #N]
  Branch:         [source] -> [DEFAULT_BRANCH]
  Source branch:  [will be deleted on merge | will be retained]
```

**On failure** (non-zero exit code):

- Display the full CLI error output
- Do NOT retry automatically (risk of duplicate MR). Instead, run Gate 6 (idempotency check) first
  to see if an MR was partially created
- Suggest remediation based on error type:
  - Auth error: re-run Gate 1
  - Branch error: re-run Gates 3-5
  - Server error: wait and retry (after Gate 6)
  - Network error: check connectivity, then Gate 6 + retry

**Evidence to record**:

```yaml
mr_creation:
  result:
    status: pass | fail
    mr_url: '[URL]'
    mr_reference: '[!N or #N]'
    exit_code: 0
    platform: '[gitlab | github]'
    target_branch: '[DEFAULT_BRANCH]'
    evidence: 'glab mr create exit_code=0, MR URL: [URL]'
```

---

## Pipeline Integration (cu-pipe S10)

When called from cu-pipe S9_CLOSE:

1. Run `/cu:mr-create` (this command)
2. Record the MR URL and reference in the pipeline YAML `pr_creation` section
3. Record the gate results as `verified_claim` entries
4. The user confirmation hard gate in this command replaces the cu-pipe S10 inline confirmation
5. After MR creation, cu-pipe proceeds to the final merge-readiness summary

**Minimum verified claims after S10**:

```yaml
verified_claims:
  - claim: 'Git platform detected from remote URL'
    command: 'git remote get-url origin'
    expected: 'github.com or gitlab host detected'
    actual: '[detected platform]'
    exit_code: 0
    scope: 'mr_creation'
    category: 'platform_detection'
  - claim: 'Default branch detected dynamically'
    command: 'git symbolic-ref refs/remotes/origin/HEAD'
    expected: 'valid branch name'
    actual: '[DEFAULT_BRANCH]'
    exit_code: 0
    scope: 'mr_creation'
    category: 'branch_detection'
  - claim: 'Platform CLI available and authenticated'
    command: 'glab repo view || gh auth status'
    expected: 'exit_code=0'
    actual: 'exit_code=0'
    exit_code: 0
    scope: 'mr_creation'
    category: 'tool_check'
  - claim: 'No open MR/PR exists for this branch'
    command: 'glab mr list --source-branch X || gh pr list --head X'
    expected: 'no results'
    actual: 'no open MR/PR found'
    exit_code: 0
    scope: 'mr_creation'
    category: 'idempotency'
  - claim: 'Secret/PII scan passed on commit log and description'
    command: 'regex scan of $DESC_FILE and git log output'
    expected: 'no secrets or PII detected'
    actual: 'scan passed'
    exit_code: 0
    scope: 'mr_creation'
    category: 'secret_scan'
  - claim: 'Feature branch has commits vs default branch'
    command: 'git log DEFAULT_BRANCH..HEAD --oneline'
    expected: 'non-empty output'
    actual: 'N commits'
    exit_code: 0
    scope: 'mr_creation'
    category: 'commit_check'
  - claim: 'Merge/pull request created on remote'
    command: 'glab mr create ... || gh pr create ...'
    expected: 'exit_code=0'
    actual: 'exit_code=0, URL: [URL]'
    exit_code: 0
    scope: 'mr_creation'
    category: 'mr_creation'
```

---

## Arguments

| Argument          | Default | Description                                                                                            |
| ----------------- | ------- | ------------------------------------------------------------------------------------------------------ |
| `$ARGUMENTS`      | (none)  | Optional: MR/PR title string (overrides fallback chain). Must not start with `--`.                     |
| `--draft`         |         | Create as draft MR/PR. Adds `--draft` to the glab or gh invocation.                                    |
| `--target-branch` | auto    | Override the detected default branch. Useful for repos integrating into `develop` or release branches. |

> **Note**: The hard gate (user confirmation) serves as the review-before-submit mechanism. There is
> no `--dry-run` flag; the preview is always shown before creation.

> **Multi-instance GitLab/GitHub**: Gate 1 checks authentication against the default CLI instance.
> For GitLab with multiple hosts, ensure the correct instance is set via
> `glab config set -g host <hostname>`. For GitHub with multiple accounts, use `gh auth login` to
> set the active account.

> **Regulatory note**: For regulated, secrecy-bound, or privacy-sensitive projects, review the MR
> description carefully in the Hard Gate preview for client-identifying data. The secret scan
> catches technical secrets but not contextual business information. A future `regulatory_profile`
> configuration option is planned to add enhanced controls.

---

## Example Usage

### Standalone: create MR with auto-detected title

```
/cu:mr-create
```

The command detects the platform, finds the pipeline YAML, generates a title and description from
the story file and commit log, runs all safety gates, and presents a confirmation preview.

### Standalone: create MR with custom title

```
/cu:mr-create US-137: Platform-aware MR/PR creation command
```

Uses the provided title instead of the fallback chain.

### Standalone: create draft PR

```
/cu:mr-create --draft
```

Creates a draft merge request or pull request. Title is still auto-detected via the fallback chain.

### Standalone: target a non-default branch

```
/cu:mr-create --target-branch develop
```

Targets the `develop` branch instead of the auto-detected default branch.

### Via cu-pipe S10

```
/cu:pipe complete
```

The cu-pipe command delegates to `/cu:mr-create` at the S10 stage, passing the story context
automatically.

---

## Related Commands

- `/cu:pipe` S9_CLOSE: delegates MR/PR creation to this command
- `/cu:qa-gate`: quality gates that should pass before MR/PR creation
