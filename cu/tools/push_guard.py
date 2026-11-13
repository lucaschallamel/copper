"""PreToolUse push guard: refuse a Bash `git push` to main or master (TD-206).

Core's plugin only, fed by `bin/cu-rules push-guard`; a refusal is exit 2, reason on
stderr. Command text only: a guard, not a guarantee (ADR-053 D14). It refuses what it
cannot resolve (D2), decides an error on the text (D5) and has no off-switch (AC3).
"""

from __future__ import annotations

import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

PROTECTED = ("main", "master")
GIT_TIMEOUT = 5  # seconds per git call; the hook entry allows 15 (D5)
RUN = {"capture_output": True, "text": True, "timeout": GIT_TIMEOUT, "check": False}
SHELL_TOOLS = {"Bash", "Monitor", "PowerShell"}  # host tools that run a command (S5)
PUSHY = re.compile(r"push|send-pack")  # a command without either is never judged
MAY_PUSH = re.compile(r"git\b.*\b(push|send-pack)\b", re.DOTALL)
PUSH_WORD = re.compile(r"\bpush\b|send-pack|\$")  # after git: push, or `$SUB`
QUOTED_HASH = re.compile(r"""['"\\]#""")  # a `#` the shell keeps as text: '#x', \#x
HEREDOC = re.compile(  # `cat <<'EOF'`: the word before `<<`, the delimiter, the body
    r"(\S*)\s*<<-?\s*(['\"]?)(\w+)\2(?![\w'\"])[^\n]*\n(.*?)\n\s*\3[ \t]*(?=\n|$)",
    re.S,
)
HEREDOC_OP = re.compile(r"(?<!<)<<(?!<)")  # every heredoc, read or not (S5 audit)
DASHED = re.compile(r"git-(push|send-pack|http-push)")  # git-core's `git-push`
OPERATOR_CHARS = re.compile(r"[;&|()]+")
OPERATOR = re.compile(r";;|&&|\|\||\|&|[;&|()]")
ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
REDIRECT = re.compile(r"^\d*[<>&]*[<>][<>&|]*$")
SEPARATORS = {";", ";;", "&", "&&", "|", "||", "|&", "(", ")"}
KEYWORDS = {"{", "}", "!", "if", "then", "else", "elif", "fi", "do", "done", "while"}
KEYWORDS |= {"until", "for", "case", "esac", "select", "function"}
WRAPPERS = {"command", "exec", "nice", "nohup", "time", "builtin", "sudo", "env"}
WRAPPER_VALUE = {"-n", "-u", "-g", "--user", "--group"}
CHDIR = {"-C", "--chdir", "-D", "--chdir-dir"}  # env -C, sudo -D: a new directory
GIT_PLACE = ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR")  # anywhere: like git -C
# Allow-list (S5): a segment naming git and push passes only as a judged push, a
# non-push git command, or one of these, which only print, search or file a PR text.
READERS = {"echo", "printf", "grep", "egrep", "fgrep", "ag", "ack", "gh", "cat"}
READERS |= {"head", "tail", "wc", "sort", "uniq", "cut", "tr", "less", "more", "jq"}
EXPANDERS = {"eval", "xargs", "source", "."}  # re-read or extend the git words
ELSEWHERE = re.compile(r"\b(cd|pushd)\b|\s(-C|-D|--git-dir|--work-tree|--chdir)\b")
ARITHMETIC = re.compile(r"\(\([^()]*\)\)")
FUNSUB = re.compile(r"\$\{[\s|]")
UNSEEN = re.compile(r"[${}*?\[]")  # filled in by the shell after the guard looks
OUTSIDE_CONFIG = re.compile(r"GIT_CONFIG|--config-env|include(if)?\.", re.IGNORECASE)
GIT_VALUE = {"-c", "--namespace", "--exec-path", "--config-env", "--attr-source"}
GIT_MOVE = {"-C", "--git-dir", "--work-tree"}
GIT_FLAGS = {"-p", "--paginate", "-P", "--no-pager", "--bare", "--no-replace-objects"}
GIT_FLAGS |= {"--literal-pathspecs", "--glob-pathspecs", "--noglob-pathspecs"}
GIT_FLAGS |= {"--icase-pathspecs", "--no-optional-locks", "--no-advice"}
PLUMBING_PUSH = {"send-pack", "http-push"}  # update remote refs without `push`
REF_PLACES = (">", "git-dir", "GIT_DIR", ".git")  # where a ref file may be written
CREATE_FLAGS = {"-b", "-B", "-c", "-C", "--create", "--force-create", "--orphan"}
REF_WRITERS = {"symbolic-ref", "update-ref"}  # can point a branch name at main
REMOTE_WRITES = {"add", "set-url", "rename", "set-head", "set-branches"}
PUSH_VALUE = {"--push-option", "--receive-pack", "--exec", "--recurse-submodules"}
PUSH_EVERY = {"--all", "--mirror", "--branches"}
PUSH_NONE = {"--help", "-h", "--dry-run", "-n"}  # nothing is pushed
SHORT_VALUE = re.compile(r"-[^-=]*o")  # `-o`, `-fo`: o takes the next word
CONFIG_ROUTES = ("push.", "remote.", "branch.")  # -c keys that reroute a push
ROUTE_KEYS = (*CONFIG_ROUTES, "alias.", "include")  # a `git config` write that does too
# Git commands that keep the branch, upstream and push routing; any other earlier in the
# command makes a later bare or HEAD push unresolvable (S7).
GIT_KEEPS = {"status", "log", "diff", "show", "rev-parse", "ls-files", "grep", "blame"}
GIT_KEEPS |= {"fetch", "pull", "add", "commit", "stash", "tag", "rm", "mv", "restore"}
GIT_KEEPS |= {"merge", "revert", "cherry-pick", "apply", "describe", "reflog", "push"}
UNRESOLVED = "its destination cannot be determined"
MARK = "'git push'"  # left where hidden text named git push, so it still counts
RULE = (
    "Critical Safety Rule 2 and Rule 07 Control 4: never push directly to main or "
    "master. Push a feature branch by name (git push -u origin <branch>) and open a "
    "pull request."
)


class Refused(Exception):
    """The command may push to a protected branch; the message says why."""


def _git(args: list[str], cwd: str | None) -> str | None:
    done = subprocess.run(["git", *args], cwd=cwd, **RUN)
    return done.stdout.strip() if done.returncode == 0 else None


def _heredocs(command: str, count: bool) -> str:
    """Drop a heredoc body fed to a reader; refuse one naming git push fed elsewhere."""

    def drop(m: re.Match) -> str:
        name = re.sub(r"^\W+", "", m.group(1)).rsplit("/", 1)[-1]
        if name not in READERS and MAY_PUSH.search(m.group(4)):
            raise Refused(f"{UNRESOLVED} (a heredoc naming git push feeds `{name}`)")
        opening = m.group(0)[: m.start(4) - m.start(0)].rstrip("\n")
        return opening + (" " + MARK if MAY_PUSH.search(m.group(4)) else "")

    text, read = HEREDOC.subn(drop, command)
    operators = HEREDOC_OP.findall(ARITHMETIC.sub("", command))  # not `$((1<<2))`
    unread = count and read != len(operators)
    if unread and MAY_PUSH.search(command):
        raise Refused(f"{UNRESOLVED} (a heredoc it cannot read)")  # `<<\A` (S5 audit)
    return text


def _lift(command: str) -> tuple[str, list[str]]:
    """The command with each `$(...)` or backtick span as `$SUB`, and the spans."""
    outer, inner, i = [], [], 0
    while i < len(command):
        tick = command[i] == "`"
        if not (tick or command.startswith("$(", i)):
            outer.append(command[i])
            i += 1
            continue
        j, depth = i + (1 if tick else 2), 1
        while j < len(command) and depth:
            if tick:
                depth -= command[j] == "`"
            else:
                depth += {"(": 1, ")": -1}.get(command[j], 0)
            j += 1
        inner.append(command[i + (1 if tick else 2) : j - (0 if depth else 1)])
        outer.append(MARK if MAY_PUSH.search(inner[-1]) else "$SUB")
        i = j
    return "".join(outer), inner


def _operators(token: str) -> list[str]:
    """shlex lexes `);` or `)&&` as one token: split it into the separators."""
    if token in SEPARATORS or not OPERATOR_CHARS.fullmatch(token):
        return [token]
    return OPERATOR.findall(token)


def _fed(words: list[str], raw: list[str], piped: bool, state: dict) -> bool:
    """An expander reads its git words from a pipe, a file, a here-string (S5 audit)."""
    from_file = any(t.startswith("<") for t in raw) or {"-a", "--arg-file"} & set(words)
    return (piped and state["said"]) or (from_file and state["names_push"])


def _renamed(token: str) -> bool:
    """`exec -agit-push git`, `env --argv0=git-push git`: git run as another name."""
    found = DASHED.search(token)
    return found is not None and not DASHED.fullmatch(token.rsplit("/", 1)[-1])


def _segments(command: str) -> list[tuple[list[str], list[str], bool]]:
    """Per simple command: its words, all its tokens and whether a pipe feeds it."""
    text = command.replace("\\\n", "").replace("\n", " ; ")  # continuations first
    lexer = shlex.shlex(text, posix=True, punctuation_chars=True)
    lexer.whitespace_split, lexer.commenters = True, ""  # `fix#12` is a word in bash
    segments, words, raw, comment, piped = [], [], [], False, False
    tokens, i = [p for t in lexer for p in _operators(t)], 0
    while i < len(tokens):
        token = tokens[i]
        if token in SEPARATORS:
            segments.append((words, raw, piped))
            words, raw, comment, piped = [], [], False, token in ("|", "|&")
            i += 1
            continue
        dashed = DASHED.fullmatch(token.rsplit("/", 1)[-1])
        parts = ["git", dashed.group(1)] if dashed else [token]
        raw += parts
        if comment or token.startswith("#"):  # quotes are gone: '#1' looks the same,
            comment = True  # so the allow-list below still sees the hidden words
        elif REDIRECT.match(token):
            if words and words[-1].isdigit():
                words.pop()  # `2>/dev/null` lexes as `2`, `>`: the 2 is no argument
            i += 1  # the target goes with the operator
        else:
            words += parts
        i += 1
    return [s for s in [*segments, (words, raw, piped)] if s[1]]


def _mentions(raw: list[str]) -> bool:
    """`git` (or `$SUB`) then a word naming push, or a spaced string naming both."""
    names = [w.rsplit("/", 1)[-1] for w in raw]
    at = next((i for i, n in enumerate(names) if n == "git" or "$" in n), None)
    if at is not None and PUSH_WORD.search(" ".join(raw[at + 1 :])):
        return True  # a `$SUB push ...` may be git: the shell decides
    return any(" " in t and MAY_PUSH.search(t) for t in raw)


def _is_git(word: str) -> bool:
    return word.rsplit("/", 1)[-1] == "git"


def _unwrap(words: list[str]) -> tuple[list[str], bool]:
    """The command under keywords, assignments and wrappers; True if git moves."""
    moved, i = False, 0
    while i < len(words):
        word = words[i]
        if word in KEYWORDS:
            i += 1
        elif ASSIGNMENT.match(word):
            i += 1
        elif word in WRAPPERS:
            i += 1
            while i < len(words) and words[i].startswith("-"):
                moved = moved or words[i].split("=", 1)[0] in CHDIR
                takes = words[i] in WRAPPER_VALUE or words[i] in CHDIR
                # never take `git` itself as an option's value (`sudo -n git`)
                takes = takes and i + 1 < len(words) and not _is_git(words[i + 1])
                i += 2 if takes else 1
        else:
            break
    return words[i:], moved


def _git_head(words: list[str]) -> tuple[int, dict]:
    """Where the git subcommand is, and where git looks (`-C`, `--git-dir`)."""
    head = {"moved": False, "chdirs": [], "lost": None, "unknown": False}
    i = 1
    while i < len(words) and words[i].startswith("-"):
        name, joined = words[i].split("=")[0], "=" in words[i]
        takes = (name in GIT_VALUE or name in GIT_MOVE) and not joined
        value = words[i + 1] if takes and i + 1 < len(words) else ""
        key = value.lower()
        routes = key.startswith(CONFIG_ROUTES) and "push" in words[i + 2 :]
        if name == "-c" and (routes or key.startswith("alias.")):  # an alias can push
            raise Refused(f"{UNRESOLVED} (a `-c` setting changes where it pushes)")
        if name == "-C" and takes:
            head["chdirs"].append(value)
        elif name in GIT_MOVE:
            head["lost"] = "git is pointed at another repository"
        head["unknown"] |= name not in GIT_VALUE | GIT_MOVE | GIT_FLAGS
        head["moved"] |= name in GIT_MOVE
        i += 2 if takes else 1
    return i, head


def _git_args(words: list[str]) -> tuple[list[str], dict] | None:
    """Arguments after `push`, and where git looks; None if not a push."""
    i, head = _git_head(words)
    sub = words[i] if i < len(words) else ""
    if sub == "push":
        return words[i + 1 :], head
    if sub in PLUMBING_PUSH:
        raise Refused(f"{UNRESOLVED} (`git {sub}` updates remote refs directly)")
    if not sub or UNSEEN.search(sub):  # cut short, or `git $SUB`
        raise Refused(f"{UNRESOLVED} (the git command is not visible)")
    if head["unknown"] and "push" in words[i:]:  # `--attr-source HEAD push` (S5 audit)
        raise Refused(f"{UNRESOLVED} (a git option it does not know)")
    return None


def _long(name: str, options: set[str]) -> bool:
    """`name` is one of `options` or an abbreviation git accepts (`--al`)."""
    return (
        len(name) > 2
        and name.startswith("--")
        and any(o.startswith(name) for o in options)
    )


def _parse_push(args: list[str]) -> list[str] | None:
    """Remote, then refspecs; None for `--help` or `--dry-run` in option position."""
    positionals, i = [], 0
    while i < len(args):
        arg = args[i]
        name = arg.split("=", 1)[0]
        if arg == "--":
            return positionals + args[i + 1 :]
        if _long(name, PUSH_EVERY):
            raise Refused(f"`{arg}` pushes every branch, main included")
        if _long(name, {"--repo"}):
            raise Refused(f"{UNRESOLVED} (`--repo` names the remote)")
        if arg in PUSH_NONE:
            return None
        if (_long(name, PUSH_VALUE) and "=" not in arg) or SHORT_VALUE.fullmatch(arg):
            i += 1  # its value is never an option or a refspec
        elif not arg.startswith("-"):
            positionals.append(arg)
        i += 1
    return positionals


def _remotes(cwd: str | None) -> set[str]:
    return set((_git(["remote"], cwd) or "").split())


def _protected(remote: str | None, cwd: str | None) -> set[str]:
    """Lower-cased: a remote on a case-insensitive filesystem takes `MAIN` as main.
    Every remote's default branch counts, whichever remote or URL is named: two remotes
    can share a URL, and only one may have its HEAD recorded (S5 audit)."""
    names = set(PROTECTED)
    for name in _remotes(cwd):
        prefix = f"refs/remotes/{name}/"  # full name: `--short` misleads (S5 audit)
        default = _git(["symbolic-ref", f"{prefix}HEAD"], cwd)
        if default and default.startswith(prefix):
            names.add(default[len(prefix) :])
    return {n.lower() for n in names}


def _routed(remote: str | None, cwd: str | None) -> str | None:  # push or mirror
    if not remote:
        return None
    # pre-config remotes: `git remote` does not list them, `git push` still reads them
    for legacy in (f"remotes/{remote}", f"branches/{remote}"):
        path = _git(["rev-parse", "--git-path", legacy], cwd)
        if path and Path(cwd or ".", path).exists():
            return f"{legacy} file"
    if remote not in _remotes(cwd):
        return None
    push = _git(["config", "--get-all", f"remote.{remote}.push"], cwd)
    return push or _git(["config", "--get", f"remote.{remote}.mirror"], cwd)


def _strip(name: str) -> str:
    for prefix in ("refs/heads/", "heads/"):  # git reads `heads/main` as the branch
        if name.startswith(prefix):
            return name[len(prefix) :]
    return name


def _source(src: str, cwd: str | None, ctx: dict) -> str:
    """The ref git pushes for a refspec with no destination: what `src` resolves to."""
    if ctx["refs"]:
        raise Refused(f"{UNRESOLVED} (a ref was repointed earlier in the command)")
    full = _git(["rev-parse", "--symbolic-full-name", src], cwd) or ""
    if src in ("HEAD", "@") and (ctx["moved"] or not full.startswith("refs/heads/")):
        raise Refused(f"{UNRESOLVED} (HEAD is not a branch here)")
    if not full:  # not there yet: made by this command, or git refuses it
        if _strip(src) in ctx["created"]:  # `git checkout -b x && git push -u origin x`
            return _strip(src)
        if any(mark in ctx["text"] for mark in REF_PLACES):  # S7 F2
            raise Refused(f"{UNRESOLVED} (`{src}` may be written as a ref first)")
        return _strip(src)
    if full.startswith("refs/tags/"):
        return full  # a tag is no branch
    if not full.startswith("refs/heads/"):
        raise Refused(f"{UNRESOLVED} (`{src}` is not a branch here)")
    return full[len("refs/heads/") :]  # a symbolic ref counts as its target


def _destination(spec: str, cwd: str | None, ctx: dict) -> str:
    dst = spec.lstrip("+")
    if ":" not in dst:
        return _source(dst, cwd, ctx)
    src, dst = dst.split(":", 1)
    if not dst and not src:  # `:` and `+:` push every matching branch
        raise Refused("`:` pushes every matching branch, main included")
    if not dst or dst in ("HEAD", "@"):
        return _source(dst or src, cwd, ctx)
    return _strip(dst)


def _owner(target: str, cwd: str | None) -> str | None:
    """The configured remote whose tracking refs hold `target` (names may hold `/`)."""
    owners = [r for r in _remotes(cwd) if target.startswith(f"refs/remotes/{r}/")]
    return max(owners, key=len) if owners else None


def _judge_bare(remote: str | None, cwd: str | None, moved: bool) -> None:
    if moved:
        raise Refused(f"{UNRESOLVED} (a bare push after a directory change)")
    if _git(["config", "push.default"], cwd) == "matching":
        raise Refused("push.default is `matching`, which pushes main too")
    target = _git(["rev-parse", "--symbolic-full-name", "@{push}"], cwd) or ""
    push_remote = _owner(target, cwd)
    if push_remote is None:
        raise Refused(f"{UNRESOLVED} (no push destination is configured)")
    if remote and remote != push_remote:
        raise Refused(f"{UNRESOLVED} (a bare push to a remote other than its own)")
    if _routed(push_remote, cwd):
        raise Refused(f"{UNRESOLVED} (remote.{push_remote}.push or mirror is set)")
    # Every name git may push to: the tracking ref's, the branch's own, its upstream's;
    # a fetch refspec can rename the tracking ref (S5 audit).
    current = _source("HEAD", cwd, {"refs": False, "moved": False})
    merge = _git(["config", f"branch.{current}.merge"], cwd) or ""
    names = {target[len(f"refs/remotes/{push_remote}/") :], current, _strip(merge)}
    protected = _protected(push_remote, cwd)
    for branch in sorted(n for n in names if n.lower() in protected):
        named = branch if branch.lower() in PROTECTED else "the remote's default branch"
        raise Refused(f"it pushes to {named}")  # never echo a repo's own name


def _judge_push(args: list[str], ctx: dict) -> None:
    positionals = _parse_push(args)
    if positionals is None:
        return
    if any(UNSEEN.search(p) for p in positionals):  # filled in after we look
        raise Refused(f"{UNRESOLVED} (the shell fills in the remote or branch)")
    if ctx["lost"]:
        raise Refused(f"{UNRESOLVED} ({ctx['lost']})")
    remote, specs = (positionals[0], positionals[1:]) if positionals else (None, [])
    if not specs:
        _judge_bare(remote, ctx["dirs"][0], ctx["moved"])
        return
    for cwd in ctx["dirs"]:  # every repository the push may run in (S5 audit)
        if _routed(remote, cwd):
            raise Refused(f"{UNRESOLVED} (remote.{remote}.push or mirror is set)")
        protected = _protected(remote, cwd)
        for spec in specs:
            dst = _destination(spec, cwd, ctx)
            if dst.lower() in protected:
                raise Refused(f"it pushes to {dst}")


def _places(
    dirs: list, targets: list[str], home_set: bool = False
) -> tuple[list, str | None]:
    """The directories `cd` or `git -C` may lead to from each of `dirs`."""
    for target in targets:
        if UNSEEN.search(target) or target == "-":
            return dirs, "a directory the shell fills in"
        if target.startswith("~") and home_set:  # `HOME=x; cd ~` (S7 F4)
            return dirs, "HOME is changed in the command"
        found = {Path(d or Path.cwd()) / Path(target).expanduser() for d in dirs}
        dirs = sorted(str(d) for d in found if d.is_dir())
        if not dirs:
            return dirs, "a directory that does not exist yet"
    return dirs, None


def _track(words: list[str], state: dict) -> None:
    """What a git command changes for the segments after it (S7)."""
    if state["rerouted"]:
        raise Refused(f"{UNRESOLVED} (git config changed push routing earlier)")
    i, _ = _git_head(words)
    sub, rest = (words[i] if i < len(words) else ""), words[i + 1 :]
    if sub == "config" and any(w.lower().startswith(ROUTE_KEYS) for w in rest):
        state["rerouted"] = True  # `git config alias.p push`, `push.default matching`
    elif sub == "remote" and REMOTE_WRITES & set(rest):
        state["rerouted"] = True  # `git remote set-url --push origin ...`
    elif sub not in GIT_KEEPS:
        state["moved"] = True  # `git checkout main && git push`
    state["refs"] |= (
        sub in REF_WRITERS
    )  # `git symbolic-ref refs/heads/x refs/heads/main`
    if sub == "branch":
        state["created"] |= {w for w in rest if not w.startswith("-")}
    for flag, name in zip(rest, rest[1:]):  # checkout -b, switch -c, worktree add -b
        if sub != "branch" and flag in CREATE_FLAGS:
            state["created"].add(name)


def _judge_mention(words: list[str], raw: list[str], start, state) -> None:
    """A non-reader segment naming git and push: allowed only if understood."""
    before = {w.rsplit("/", 1)[-1] for w in words[: start or 0]}
    if start is None or before & EXPANDERS:
        raise Refused(f"{UNRESOLVED} (a command it cannot read names git push)")
    found = _git_args(words[start:])
    if found is None and start == 0:
        return  # a visible git command that is not push: `commit -m "#12 push"`
    if found is None:
        raise Refused(f"{UNRESOLVED} (git behind a command it cannot read)")
    if state["hidden"] and any(w[:1] == "#" for w in raw):
        raise Refused(f"{UNRESOLVED} (a quoted `#` hides part of the push)")
    args, head = found
    dirs, lost = _places(state["dirs"], head["chdirs"])
    moved = state["moved"] or head["moved"] or start > 0
    lost = state["lost"] or head["lost"] or lost
    ctx = {"dirs": dirs, "moved": moved, "lost": lost, "refs": state["refs"]}
    _judge_push(args, {**ctx, "text": state["text"], "created": state["created"]})


def _start(cwd: str | None, outer: str, inherited: dict) -> dict:
    """The state before the first segment."""
    lost = inherited["lost"]
    if any(name in outer for name in GIT_PLACE):  # `export GIT_DIR=` too
        lost = "GIT_DIR or GIT_WORK_TREE points git elsewhere"
    return {
        "dirs": [cwd],
        "moved": inherited["moved"] or lost is not None,
        "lost": lost,
        "hidden": QUOTED_HASH.search(outer) is not None,
        "fed": False,
        "said": False,  # an earlier segment's text names push
        "names_push": re.search(r"\bpush\b|send-pack", outer) is not None,
        "rerouted": False,
        "refs": inherited["refs"],
        "text": outer,
        "created": set(),
    }


def _inherit(outer: str, inherited: dict) -> dict:
    """A `$(...)` may run after any outer segment: what it must assume (S5 audit)."""
    lost = "a push in a command substitution after a directory change"
    return {
        "moved": True,  # no bare or HEAD push: the branch may have changed
        "lost": inherited["lost"] or (lost if ELSEWHERE.search(outer) else None),
        "refs": inherited["refs"] or any(w in outer for w in REF_WRITERS),
    }


def judge_command(command: str, cwd: str | None, inherited: dict | None = None) -> None:
    """Raise Refused unless every segment naming git and push is understood as safe."""
    if OUTSIDE_CONFIG.search(command) and re.search(r"\bgit\b", command):
        raise Refused(f"{UNRESOLVED} (git config set from the environment or a file)")
    if MAY_PUSH.search(command) and ("<(" in command or ">(" in command):
        raise Refused(f"{UNRESOLVED} (a process substitution with git push in it)")
    if MAY_PUSH.search(command) and FUNSUB.search(command):  # bash 5.3 `${ cmd; }`
        raise Refused(f"{UNRESOLVED} (a `${{ ...; }}` runs in this shell: S7 F3)")
    # heredoc bodies are all in the top-level text; a span holds only their openings
    outer, inner = _lift(_heredocs(command, count=inherited is None))
    inherited = inherited or {"moved": False, "lost": None, "refs": False}
    for span in inner:  # `echo "$(git push origin main)"` runs that push too
        judge_command(span, cwd, _inherit(outer, inherited))
    state = _start(cwd, outer, inherited)
    for words, raw, piped in _segments(outer):
        # unwrapped first: `builtin cd`, `if cd x; then`, `{ cd x; }` (S5 audit)
        words, wrapper_moved = _unwrap(words)
        if words and words[0] in ("cd", "pushd"):
            state["moved"] = True
            if "CDPATH" in outer:
                state["lost"] = "CDPATH changes where `cd` goes"
            target = [w for w in words[1:] if not w.startswith("-") or w == "-"]
            home = "HOME=" in outer  # the shell's `~`, not the guard's
            dirs, lost = _places(state["dirs"], target[:1] or ["~"], home)
            state["dirs"] = sorted(
                set(state["dirs"]) | set(dirs)
            )  # a subshell undoes it
            state["lost"] = state["lost"] or lost
            continue
        name = words[0].rsplit("/", 1)[-1] if words else ""
        mentions, carried = _mentions(raw), piped and state["fed"]
        if carried and name not in READERS:
            raise Refused(f"{UNRESOLVED} (text naming git push is piped onward)")
        state["fed"] = (mentions and name in READERS) or carried
        start = next((i for i, w in enumerate(words) if _is_git(w)), None)
        if name in EXPANDERS and start is not None and _fed(words, raw, piped, state):
            raise Refused(f"{UNRESOLVED} (`{name}` runs git with words fed to it)")
        if start is not None and any(_renamed(t) for t in raw):
            raise Refused(f"{UNRESOLVED} (git started under another name)")
        state["said"] |= any(PUSH_WORD.search(t) and "$" not in t for t in raw)
        if mentions and name not in READERS:
            moved = "a wrapper changes the directory" if wrapper_moved else None
            _judge_mention(words, raw, start, {**state, "lost": state["lost"] or moved})
        if start is not None:
            _track(words[start:], state)


def judge(raw: str) -> str | None:
    """The refusal reason for one hook input, or None to let the call run."""
    command = None
    try:
        data = json.loads(raw)
        if not isinstance(data, dict) or data.get("tool_name") not in SHELL_TOOLS:
            return None
        command = (data.get("tool_input") or {}).get("command")
        if not isinstance(command, str) or not PUSHY.search(command):
            return None
        judge_command(command, data.get("cwd") or None)
        return None
    except Refused as refused:
        return str(refused)
    except Exception:  # D5 (a): never let a broken guard wave a push through
        # the command alone once read: a folder named git/push-x must not refuse `ls`
        may_push = MAY_PUSH.search(command if isinstance(command, str) else raw)
        return "the guard could not check this command" if may_push else None


def main() -> int:
    reason = judge(sys.stdin.read())
    if reason is None:
        return 0
    print(f"cu push guard: refused `git push`: {reason}. {RULE}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
