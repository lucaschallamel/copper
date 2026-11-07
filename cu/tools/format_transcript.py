#!/usr/bin/env python3
"""
Transcript Formatting Utility

Breaks raw voice-memo transcripts (often a single long line) into readable
paragraphs by splitting on sentence boundaries.  Preserves speaker-label
lines and blank lines between speaker turns.

Usage:
    python3 <host-tools-dir>/format_transcript.py <input.md> [--sentences N] [--force]
    (host-tools-dir: .opencode/tools on OpenCode, .claude/tools on Claude Code)

Arguments:
    input.md        Path to raw transcript file
    --sentences N   Sentences per paragraph (default: 5)
    --force         Overwrite existing _formatted.md

Behaviour:
    1. Read input file (UTF-8).
    2. If <input>_formatted.md already exists and --force is not set,
       print a message and exit 0 (idempotent by default).
    3. Identify speaker-label lines matching the pattern:
       ^[A-Z][A-Za-z\\s]+?\\s*:\\s*\\d{1,2}:\\d{2}
    4. Split remaining text on sentence boundaries: (?<=[.!?])\\s+
    5. Group sentences into paragraphs of N sentences each.
    6. Preserve speaker-label lines and inter-turn blank lines as-is.
    7. Write <input>_formatted.md adjacent to the input file.
    8. Exit 0.

Constraints:
    - No external dependencies (stdlib only).
    - UTF-8 encoding throughout.
    - Deterministic and idempotent (NFR-001).
    - Repo-relative paths only (NFR-002).
    - Handles long single-line transcripts >10,000 chars (NFR-004).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_SENTENCES = 5
ENCODING = "utf-8"

# Speaker-label pattern: "Firstname Lastname  :  HH:MM"
SPEAKER_LABEL_RE = re.compile(r"^[A-Z][A-Za-z\s]+?\s*:\s*\d{1,2}:\d{2}")

# Sentence-boundary pattern: split after . ! or ? followed by whitespace
SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[.!?])\s+")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Format raw voice-memo transcripts into readable paragraphs."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=None,
        help="Path to raw transcript Markdown file",
    )
    parser.add_argument(
        "--sentences",
        type=int,
        default=DEFAULT_SENTENCES,
        help=f"Sentences per paragraph (default: {DEFAULT_SENTENCES})",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing _formatted.md output file",
    )
    return parser.parse_args(argv)


def read_input(path: Path) -> str:
    """Read the entire input file as a string."""
    return path.read_text(encoding=ENCODING)


def output_path(input_path: Path) -> Path:
    """Derive the output path: <stem>_formatted.md next to the input."""
    return input_path.with_name(f"{input_path.stem}_formatted.md")


def is_speaker_label(line: str) -> bool:
    """Return True if *line* looks like a speaker turn label."""
    return bool(SPEAKER_LABEL_RE.match(line))


def format_transcript(text: str, sentences_per_paragraph: int) -> str:
    """Break *text* into paragraphs while preserving speaker labels."""
    lines = text.split("\n")
    formatted_lines: list[str] = []

    for line in lines:
        stripped = line.strip()

        # Preserve blank lines as-is
        if stripped == "":
            formatted_lines.append("")
            continue

        # Preserve speaker-label lines as-is
        if is_speaker_label(stripped):
            formatted_lines.append(stripped)
            continue

        # Split on sentence boundaries and group into paragraphs
        sentences = SENTENCE_BOUNDARY_RE.split(stripped)
        sentences = [s for s in sentences if s]  # drop empties

        for i in range(0, len(sentences), sentences_per_paragraph):
            paragraph = " ".join(sentences[i : i + sentences_per_paragraph])
            formatted_lines.append(paragraph)
            # Add blank line after each paragraph (except the last group)
            if i + sentences_per_paragraph < len(sentences):
                formatted_lines.append("")

    return "\n".join(formatted_lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    # Fail soft: a no-input invocation (e.g. an accidental load-time call) prints
    # a one-line usage hint and exits cleanly instead of an argparse traceback.
    if args.input is None:
        print(
            "usage: format_transcript.py <input.md> [--sentences N] [--force]",
            file=sys.stderr,
        )
        return 0

    input_path = Path(args.input).resolve()

    if not input_path.is_file():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        return 1

    out_path = output_path(input_path)

    # Idempotent: skip if output already exists (unless --force)
    if out_path.exists() and not args.force:
        print(f"Output already exists: {out_path}  (use --force to overwrite)")
        return 0

    text = read_input(input_path)
    formatted = format_transcript(text, args.sentences)
    out_path.write_text(formatted, encoding=ENCODING)

    print(f"Formatted transcript written to: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
