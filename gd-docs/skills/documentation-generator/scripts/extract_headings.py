#!/usr/bin/env python3
"""Extract the heading outline from one or more Markdown files.

Bundled with the gd-documentation-generator skill. Pure
standard-library Python, no third-party dependencies. Use it to capture the
existing structure of documentation before generating or reorganising content,
so new docs map onto the real hierarchy.

Recognises ATX headings (``# Heading`` through ``###### Heading``) and skips
heading-like lines inside fenced code blocks (``` ``` ``` and ``~~~``).

Usage:
    python extract_headings.py README.md docs/guide.md
    python extract_headings.py --json docs/*.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass

ATX_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```+|~~~+)")


@dataclass
class Heading:
    file: str
    line: int
    level: int
    text: str


def extract_from_lines(path: str, lines: list[str]) -> list[Heading]:
    """Return the ATX headings in ``lines``, ignoring fenced code blocks."""
    headings: list[Heading] = []
    in_fence = False
    for number, raw in enumerate(lines, start=1):
        if FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = ATX_HEADING.match(raw)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            if text:
                headings.append(Heading(path, number, level, text))
    return headings


def extract_from_file(path: str) -> list[Heading]:
    with open(path, encoding="utf-8") as handle:
        return extract_from_lines(path, handle.read().splitlines())


def render_table(headings: list[Heading]) -> str:
    if not headings:
        return "(no headings found)"
    lines = []
    for heading in headings:
        indent = "  " * (heading.level - 1)
        lines.append(f"{heading.file}:{heading.line}: {indent}{heading.text}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=next(iter((__doc__ or "").splitlines()), None)
    )
    parser.add_argument("files", nargs="+", help="Markdown files to scan")
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit the outline as JSON instead of a table",
    )
    args = parser.parse_args(argv)

    all_headings: list[Heading] = []
    exit_code = 0
    for path in args.files:
        try:
            all_headings.extend(extract_from_file(path))
        except OSError as error:
            print(f"warning: cannot read {path}: {error}", file=sys.stderr)
            exit_code = 1

    if args.json:
        print(json.dumps([asdict(heading) for heading in all_headings], indent=2))
    else:
        print(render_table(all_headings))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
