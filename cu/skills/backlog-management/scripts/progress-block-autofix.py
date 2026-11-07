#!/usr/bin/env python3
"""
progress-block-autofix.py

Insert or normalise the required collapsible progress update block
for supported backlog artefacts.

Supported story types:
  - epic
  - user_story
  - technical_debt
  - continuous_improvement
  - spike

Usage:
  python3 progress-block-autofix.py <file_or_directory>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SUPPORTED_TYPES = {
    "epic",
    "user_story",
    "technical_debt",
    "continuous_improvement",
    "spike",
}

FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
HEADER_PATTERN = re.compile(r"^> \[!note\]- Progress updates.*$")
DATE_TOKEN_PATTERN = r"(?:\d{4}-\d{2}-\d{2}|YYYY-MM-DD)"
DATED_BULLET_PATTERN = re.compile(rf"^> - \*\*({DATE_TOKEN_PATTERN})\*\*: (.+)$")
DATED_SUMMARY_PATTERN = re.compile(rf"^> \*\*\[({DATE_TOKEN_PATTERN})\]\*\*: (.+)$")


def parse_frontmatter(text: str) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in text.splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data


def build_default_block(created_date: str) -> list[str]:
    summary = created_date or "YYYY-MM-DD"
    return [
        "> [!note]- Progress updates",
        ">",
        f"> - **{summary}**: Story created and added to the backlog.",
        "> - Initial scope, business value, and acceptance criteria captured",
        "> - Story linked to the active framework backlog for future prioritisation",
        "> - Next step: refine during sprint planning or implementation kickoff",
    ]


def normalise_progress_block(
    lines: list[str], created_date: str
) -> tuple[list[str], bool]:
    changed = False

    while lines and not lines[0].strip():
        lines = lines[1:]
        changed = True

    if not lines or not HEADER_PATTERN.match(lines[0]):
        return build_default_block(created_date) + [""] + lines, True

    new_lines = ["> [!note]- Progress updates", ">"]
    body_lines = lines[1:]

    while body_lines and body_lines[0].strip() == ">":
        body_lines = body_lines[1:]

    summary_added = False
    rest: list[str] = []

    if body_lines:
        first = body_lines[0]
        bullet_match = DATED_BULLET_PATTERN.match(first)
        summary_match = DATED_SUMMARY_PATTERN.match(first)

        if summary_match:
            summary_lines = [summary_match.group(2)]
            summary_date = summary_match.group(1)
            summary_added = True
            body_lines = body_lines[1:]

            while body_lines:
                current = body_lines[0]
                stripped = current.strip()

                if stripped == ">":
                    body_lines = body_lines[1:]
                    changed = True
                    continue

                if stripped.startswith("> -") or HEADER_PATTERN.match(current):
                    break

                if current.startswith("> "):
                    summary_lines.append(current[2:].strip())
                    body_lines = body_lines[1:]
                    changed = True
                    continue

                break

            summary_text = " ".join(part for part in summary_lines if part).strip()
            new_lines.append(f"> - **{summary_date}**: {summary_text}")
            changed = True
        elif bullet_match:
            new_lines.append(first)
            summary_added = True
            body_lines = body_lines[1:]

    if not summary_added:
        summary = created_date or "YYYY-MM-DD"
        new_lines.append(f"> - **{summary}**: Story created and added to the backlog.")
        changed = True

    for line in body_lines:
        if HEADER_PATTERN.match(line):
            changed = True
            continue
        rest.append(line)

    return new_lines + rest, changed or new_lines != lines


def process_file(file_path: Path) -> bool:
    content = file_path.read_text(encoding="utf-8")
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return False

    frontmatter = match.group(1)
    body = content[match.end() :]
    metadata = parse_frontmatter(frontmatter)
    if metadata.get("story_type") not in SUPPORTED_TYPES:
        return False

    body_lines = body.splitlines()
    normalised_lines, changed = normalise_progress_block(
        body_lines, metadata.get("created", "")
    )
    new_content = f"---\n{frontmatter}\n---\n" + "\n".join(normalised_lines)
    if not new_content.endswith("\n"):
        new_content += "\n"

    if not changed and new_content == content:
        return False

    if new_content == content:
        return False

    file_path.write_text(new_content, encoding="utf-8")
    return True


def iter_markdown_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    return sorted(path for path in target.rglob("*.md") if path.is_file())


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 progress-block-autofix.py <file_or_directory>")
        return 2

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"Error: {target} does not exist")
        return 2

    changed_files = 0
    for path in iter_markdown_files(target):
        try:
            if process_file(path):
                changed_files += 1
                print(f"Updated: {path}")
        except Exception as exc:
            print(f"Error processing {path}: {exc}", file=sys.stderr)
            return 2

    print(f"Autofix complete. Files updated: {changed_files}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
