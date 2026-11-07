"""Scheduler files for nightly `sync` (US-380 AC11a, Q18).

The tool only WRITES the files to a staging folder and prints the commands that install
them; it never enables anything. Credentials stay in an env file the user creates (mode
600): the unit names that file and never contains a credential.
"""

from __future__ import annotations

import re
import shlex
import sys
from pathlib import Path

LABEL = "hindsight-ingest"
TIME_RE = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")


def unit_name(bank: str) -> str:
    return f"{LABEL}-{re.sub(r'[^A-Za-z0-9_-]', '-', bank)}"


def _command(script: Path, vault: Path, python: str) -> str:
    return " ".join(
        shlex.quote(str(p)) for p in (python, "-I", script, "--vault", vault, "sync")
    )


def _unit_value(text: str, command: bool = False) -> str:
    """systemd expands `%` specifiers in both settings, and `$VAR` and C escapes (`\\b`)
    in ExecStart=, even inside single quotes; double them so a path is taken literally
    (BUG-018 AC3, checked on systemd 262 with a real unit)."""
    text = text.replace("%", "%%")
    if command:
        text = text.replace("\\", "\\\\").replace("$", "$$")
    return text


def systemd(
    bank: str, script: Path, vault: Path, env_file: Path, at: str, python: str
) -> dict[str, str]:
    for value in (str(script), str(vault), str(env_file), python):
        if "\n" in value or "\r" in value or value.endswith("\\"):
            raise ValueError(
                f"refused: {value!r} cannot be written into a systemd unit "
                "(a line break, or a trailing backslash that joins the next line)"
            )
    name = unit_name(bank)
    exec_start = _unit_value(_command(script, vault, python), command=True)
    service = (
        f"[Unit]\nDescription=Hindsight vault sync ({bank})\n\n"
        "[Service]\nType=oneshot\n"
        f"EnvironmentFile={_unit_value(str(env_file))}\nExecStart={exec_start}\n"
    )
    timer = (
        f"[Unit]\nDescription=Nightly Hindsight vault sync ({bank})\n\n[Timer]\n"
        f"OnCalendar=*-*-* {at}:00\nPersistent=true\n\n"
        "[Install]\nWantedBy=timers.target\n"
    )
    return {f"{name}.service": service, f"{name}.timer": timer}


def launchd(
    bank: str, script: Path, vault: Path, env_file: Path, at: str, python: str
) -> dict[str, str]:
    name = unit_name(bank)
    hour, minute = (int(x) for x in at.split(":"))
    env = shlex.quote(str(env_file))
    shell = f"set -a; . {env}; set +a; exec {_command(script, vault, python)}"
    plist = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<plist version="1.0"><dict>\n'
        f"  <key>Label</key><string>{name}</string>\n"
        "  <key>ProgramArguments</key><array>"
        "<string>/bin/sh</string><string>-c</string>"
        f"<string>{_xml(shell)}</string></array>\n"
        "  <key>StartCalendarInterval</key><dict>"
        f"<key>Hour</key><integer>{hour}</integer>"
        f"<key>Minute</key><integer>{minute}</integer></dict>\n"
        "</dict></plist>\n"
    )
    return {f"{name}.plist": plist}


def _xml(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def install_commands(files: dict[str, str], staging: Path, platform: str) -> list[str]:
    if platform == "darwin":
        (plist,) = files
        target = "~/Library/LaunchAgents/" + plist
        return [
            f"cp {shlex.quote(str(staging / plist))} {target}",
            f"launchctl load {target}",
        ]
    timer = next(f for f in files if f.endswith(".timer"))
    copies = [
        f"cp {shlex.quote(str(staging / f))} ~/.config/systemd/user/"
        for f in sorted(files)
    ]
    return [
        "mkdir -p ~/.config/systemd/user",
        *copies,
        "systemctl --user daemon-reload",
        f"systemctl --user enable --now {timer}",
    ]


def stage(
    bank: str,
    script: Path,
    vault: Path,
    env_file: Path,
    at: str,
    staging: Path,
    platform: str = sys.platform,
    python: str = "python3",
) -> tuple[dict[str, str], list[str]]:
    """Write the scheduler files to `staging`; return them and the install commands."""
    if not TIME_RE.match(at):
        raise ValueError("--at must be HH:MM (24 h)")
    build = launchd if platform == "darwin" else systemd
    files = build(bank, script, vault, env_file, at, python)
    staging.mkdir(parents=True, exist_ok=True)
    for name, body in files.items():
        (staging / name).write_text(body, encoding="utf-8")
    return files, install_commands(files, staging, platform)
