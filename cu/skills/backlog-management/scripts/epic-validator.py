#!/usr/bin/env python3
"""
epic-validator.py
Epic Story Type Validator for COPPER Projects

Purpose: Validates EP (Epic) stories with enhanced fields:
  1. YAML structure correctness
  2. Progress tracking field calculations
  3. Sprint breakdown data integrity
  4. Story dependency validation (DAG, no cycles)
  5. Enhanced workflow field completeness
  6. Children recounted by status, and the epic's own status (TD-202)

Project: Generic COPPER documentation validation toolkit
Client: [TO BE CONFIGURED]

Usage:
  python3 epic-validator.py [FILE]
  python3 epic-validator.py docs-copper/roadmap/backlog/EP-001-customer-search.md
  python3 epic-validator.py docs-copper/roadmap/backlog/EP-*.md  # validate all epics

  An epic's children are read from the cards in the epic's own folder, so epics
  live beside their story cards (one backlog folder).

Exit Codes:
  0 - All validations passed
  1 - Validation failures detected
  2 - Usage/syntax error, or tools/status-vocabulary.json unreadable

Author: COPPER framework
Version: 1.2.0 (generic adaptation)
"""

import argparse
import functools
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ModuleNotFoundError:
    yaml = None


def _load_story_statuses() -> list[str]:
    """The canonical story statuses (TD-171 AC3), at the offset user-story-validator.py
    uses: tools/ sits beside skills/ in every layout. Exit 2 if unreadable: a validator
    that cannot know the canon must say it could not check, never guess (TD-201)."""
    vocab = Path(__file__).resolve().parents[3] / "tools" / "status-vocabulary.json"
    try:
        return list(json.loads(vocab.read_text(encoding="utf-8"))["story_status"])
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print(
            f"FATAL: cannot load status vocabulary at {vocab}: {exc}", file=sys.stderr
        )
        sys.exit(2)


STORY_STATUSES = _load_story_statuses()
CLOSED = {"Done", "Cancelled"}
DUPLICATE = "two cards"  # card_index marker for a story_id on more than one card
NOT_STARTED = {"Draft", "Ready"}
COUNTED_AS = {
    "Done": "completed_stories",
    "Cancelled": "completed_stories",
    "In Progress": "in_progress_stories",
    "Blocked": "blocked_stories",
    "Draft": "not_started_stories",
    "Ready": "not_started_stories",
}


# Color codes for terminal output
class Colors:
    """ANSI color codes for terminal output"""

    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"  # No Color


class ValidationResult:
    """Stores validation results and statistics"""

    def __init__(self):
        self.total_checks = 0
        self.passed_checks = 0
        self.failed_checks = 0
        self.warning_checks = 0
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def add_pass(self, message: str, quiet: bool = False):
        """Record a passing check"""
        self.total_checks += 1
        self.passed_checks += 1
        if not quiet:
            print(f"{Colors.GREEN}[PASS]{Colors.NC} {message}", file=sys.stderr)

    def add_fail(self, message: str):
        """Record a failing check"""
        self.total_checks += 1
        self.failed_checks += 1
        self.errors.append(message)
        print(f"{Colors.RED}[FAIL]{Colors.NC} {message}", file=sys.stderr)

    def add_warning(self, message: str):
        """Record a warning"""
        self.total_checks += 1
        self.warning_checks += 1
        self.warnings.append(message)
        print(f"{Colors.YELLOW}[WARN]{Colors.NC} {message}", file=sys.stderr)

    def has_failures(self) -> bool:
        """Check if any validations failed"""
        return self.failed_checks > 0

    def has_warnings(self) -> bool:
        """Check if any warnings were raised"""
        return self.warning_checks > 0


def log_info(message: str, quiet: bool = False):
    """Print info message"""
    if not quiet:
        print(f"{Colors.BLUE}[INFO]{Colors.NC} {message}", file=sys.stderr)


def extract_yaml_frontmatter(file_path: Path) -> dict[str, Any] | None:
    """
    Extract and parse YAML frontmatter from markdown file.

    Args:
        file_path: Path to markdown file

    Returns:
        Parsed YAML as dictionary, or None if parsing fails
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Extract YAML between --- markers
        yaml_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if not yaml_match:
            return None

        yaml_text = yaml_match.group(1)

        # Parse YAML
        if yaml is not None:
            return yaml.safe_load(yaml_text)

        parsed: dict[str, Any] = {}
        current_key = None
        array_mode = False
        array_items: list[str] = []

        for line in yaml_text.split("\n"):
            line = line.rstrip()

            if line.strip().startswith("#") or not line.strip():
                continue

            if line.strip().startswith("- ") and array_mode:
                array_items.append(line.strip()[2:].strip().strip("\"'"))
                continue

            if ":" in line and not line.startswith(" "):
                if array_mode and current_key:
                    parsed[current_key] = array_items
                    array_mode = False
                    array_items = []

                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                current_key = key

                if not value:
                    array_mode = True
                elif value.startswith("[") and value.endswith("]"):
                    inner = value[1:-1].strip()
                    parsed[key] = [
                        item.strip().strip("\"'")
                        for item in inner.split(",")
                        if item.strip()
                    ]
                elif value.lower() in {"true", "false"}:
                    parsed[key] = value.lower() == "true"
                elif value.replace(".", "", 1).isdigit():
                    parsed[key] = float(value) if "." in value else int(value)
                else:
                    parsed[key] = value.strip("\"'")

        if array_mode and current_key:
            parsed[current_key] = array_items

        return parsed

    except Exception as e:
        print(
            f"{Colors.RED}[ERROR]{Colors.NC} Failed to parse YAML: {e}", file=sys.stderr
        )
        return None


def validate_yaml_structure(
    file_path: Path, data: dict[str, Any], result: ValidationResult, quiet: bool = False
) -> bool:
    """
    Validation 1: YAML Structure

    Checks:
    - story_type = "EP"
    - Required fields present
    - Enhancement fields present (warnings if missing)
    """
    log_info("Validation 1: YAML Structure", quiet)

    # Check story_type
    story_type = data.get("story_type")
    if story_type in {"EP", "epic"}:
        result.add_pass(f"story_type = {story_type}", quiet)
    else:
        result.add_fail(f"story_type must be 'EP' or 'epic', found: '{story_type}'")
        return False

    # Check required base fields
    required_fields = ["story_id", "title", "priority", "status", "child_stories"]
    for field in required_fields:
        if field in data and data[field] is not None:
            result.add_pass(f"Required field '{field}' present", quiet)
        else:
            result.add_fail(f"Required field '{field}' missing")

    # Check Enhancement 1 fields (progress tracking)
    progress_fields = [
        "progress_percentage",
        "total_stories",
        "completed_stories",
        "in_progress_stories",
        "blocked_stories",
        "not_started_stories",
    ]
    for field in progress_fields:
        if field in data and data[field] is not None:
            result.add_pass(f"Enhancement 1: '{field}' present", quiet)
        else:
            result.add_warning(
                f"Enhancement 1: '{field}' missing (optional but recommended)"
            )

    # Check Enhancement 2 fields (sprint breakdown)
    if "sprint_distribution" in data:
        result.add_pass("Enhancement 2: 'sprint_distribution' present", quiet)
    else:
        result.add_warning("Enhancement 2: 'sprint_distribution' missing (optional)")

    if "sprint_progress" in data:
        result.add_pass("Enhancement 2: 'sprint_progress' present", quiet)
    else:
        result.add_warning("Enhancement 2: 'sprint_progress' missing (optional)")

    # Check Enhancement 3 fields (dependencies)
    if "story_dependencies" in data:
        result.add_pass("Enhancement 3: 'story_dependencies' present", quiet)
    else:
        result.add_warning("Enhancement 3: 'story_dependencies' missing (optional)")

    if "dependency_metadata" in data:
        result.add_pass("Enhancement 3: 'dependency_metadata' present", quiet)
    else:
        result.add_warning("Enhancement 3: 'dependency_metadata' missing (optional)")

    # Check Enhancement 4 fields (workflow)
    if "lifecycle_state" in data:
        result.add_pass("Enhancement 4: 'lifecycle_state' present", quiet)
    else:
        result.add_warning("Enhancement 4: 'lifecycle_state' missing (optional)")

    return True


def validate_progress_block(
    file_path: Path, result: ValidationResult, quiet: bool = False
) -> bool:
    """
    Validation 6: Collapsible progress block structure

    Checks:
    - First body block after frontmatter is '> [!note]- Progress updates'
    - First entry is formatted as '> - **YYYY-MM-DD**: ...'
    """
    log_info("Validation 6: Progress Block", quiet)

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        result.add_fail(f"Failed to read file for progress block validation: {e}")
        return False

    yaml_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not yaml_match:
        result.add_fail("No YAML frontmatter found for progress block validation")
        return False

    body = content[yaml_match.end() :]
    lines = body.splitlines()

    while lines and not lines[0].strip():
        lines.pop(0)

    if not lines or lines[0].strip() != "> [!note]- Progress updates":
        result.add_fail(
            "Epic must include a collapsible "
            "'> [!note]- Progress updates' block immediately after frontmatter"
        )
        return False

    result.add_pass("Progress block header present", quiet)

    if len(lines) < 3 or lines[1].strip() != ">":
        result.add_fail(
            "Progress block must include a blank quoted separator line after the header"
        )
        return False

    if re.match(r"^> - \*\*\d{4}-\d{2}-\d{2}\*\*: .+", lines[2]):
        result.add_pass("First bullet progress entry present", quiet)
    else:
        result.add_fail(
            "Progress block must include a bullet entry in the format "
            "'> - **YYYY-MM-DD**: ...'"
        )
        return False
    return True


def _front_value(front: str, key: str) -> str | None:
    """A top-level frontmatter value as YAML reads it for a plain scalar: the last
    of repeated keys, a trailing ` # comment` dropped, then the quotes."""
    found = re.findall(rf"^{key}:[ \t]*(.*)$", front, re.M)
    if not found:
        return None
    return re.sub(r"\s+#.*$", "", found[-1]).strip().strip("'\"").strip()


@functools.cache
def card_index(backlog: Path) -> dict[str, tuple[str | None, str | None]]:
    """Every non-epic card in the folder: story_id -> (its EP-<n> epic, its status).

    Read once per folder per run (TD-202): the child-list check, the recount and
    the status rules all use it. A free-text legacy `epic:` maps to None, so it is
    never anyone's child. A story_id on two cards maps to (DUPLICATE, None): no
    other gate catches it, and keeping either card would be a guess (S7).
    """
    index: dict[str, tuple[str | None, str | None]] = {}
    for card in sorted(backlog.glob("*.md")):
        if card.name.startswith("EP-"):
            continue
        try:
            fm = re.match(r"^---\n(.*?)\n---", card.read_text(encoding="utf-8"), re.S)
        except OSError:
            continue
        sid = _front_value(fm.group(1), "story_id") if fm else None
        if sid in index:
            index[sid] = (DUPLICATE, None)
        elif sid:
            epic = _front_value(fm.group(1), "epic") or ""
            ep = re.match(r"EP-\d+$", epic)
            index[sid] = (
                ep.group(0) if ep else None,
                _front_value(fm.group(1), "status"),
            )
    return index


def _child_list_failures(epic_id: str, listed, cards: dict) -> list[str]:
    """`child_stories` against the cards whose own `epic:` names this epic: the list
    checked against its own count was green while 99 cards were missing (2026-09-20,
    BUG-004 class). One line per case (TD-202 AC2), at most 8 names each."""
    if not isinstance(listed, list):
        return [f"{epic_id}: child_stories is not a list"]
    dupes = sorted(s for s in listed if cards.get(s, (None,))[0] == DUPLICATE)
    if dupes:
        return [f"{epic_id}: more than one card has story_id {s}" for s in dupes[:8]]
    declared = set(listed)
    derived = {sid for sid, (epic, _) in cards.items() if epic == epic_id}
    cases = [
        (
            f"not listed in child_stories, though their epic is {epic_id}",
            derived - declared,
        ),
        (
            "child_stories lists ids with no card",
            {s for s in declared - derived if s not in cards},
        ),
        ("child_stories lists twice", {s for s in listed if listed.count(s) > 1}),
    ]
    lines = [
        f"{epic_id}: {case}: {', '.join(sorted(ids)[:8])}" for case, ids in cases if ids
    ]
    elsewhere = {
        s: cards[s][0] or "not an epic id" for s in declared - derived if s in cards
    }
    return lines + [
        f"{epic_id}: child_stories lists {s}, whose epic is {elsewhere[s]}"
        for s in sorted(elsewhere)[:8]
    ]


def validate_progress_tracking(
    data: dict[str, Any],
    result: ValidationResult,
    quiet: bool = False,
    epic_path: Path | None = None,
) -> bool:
    """
    Validation 2: Progress Tracking (Enhancement 1)

    Checks:
    - progress_percentage = (completed_stories / total_stories) × 100
    - total_stories = length(child_stories)
    - Sum of status counts = total_stories
    - All counts non-negative
    """
    log_info("Validation 2: Progress Tracking (Enhancement 1)", quiet)

    # UNCONDITIONAL , runs before the optional-progress-field guard below.
    # Placed here deliberately: the progress fields are "optional but recommended",
    # so a check living after that guard is skipped entirely on any epic that omits
    # them (EP-115 omits all six), which is how a gate becomes vacuously green.
    child_stories_decl = data.get("child_stories", [])
    epic_id = data.get("story_id")
    if epic_path is not None and isinstance(epic_id, str):
        failures = _child_list_failures(
            epic_id, child_stories_decl, card_index(epic_path.parent.resolve())
        )
        for line in failures:
            result.add_fail(line)
        if not failures:
            result.add_pass(
                f"child_stories matches the {len(child_stories_decl)} card(s) "
                f"declaring epic {epic_id}",
                quiet,
            )

    required_progress_fields = [
        "progress_percentage",
        "total_stories",
        "completed_stories",
        "in_progress_stories",
        "blocked_stories",
        "not_started_stories",
    ]

    if not all(field in data for field in required_progress_fields):
        result.add_warning(
            "Progress tracking fields are incomplete or absent; "
            "skipping calculated progress validation"
        )
        return True
    if epic_path is not None:
        return True  # the recount against the children owns them (TD-202 S4 F3)

    # Extract fields
    progress_percentage = data.get("progress_percentage", 0)
    total_stories = data.get("total_stories", 0)
    completed_stories = data.get("completed_stories", 0)
    in_progress_stories = data.get("in_progress_stories", 0)
    blocked_stories = data.get("blocked_stories", 0)
    not_started_stories = data.get("not_started_stories", 0)

    child_stories = data.get("child_stories", [])
    child_count = len(child_stories) if isinstance(child_stories, list) else 0

    # Check total_stories = length(child_stories)
    if total_stories == child_count:
        result.add_pass(
            f"total_stories ({total_stories}) = length(child_stories) ({child_count})",
            quiet,
        )
    else:
        result.add_fail(
            f"total_stories ({total_stories}) ≠ length(child_stories) ({child_count})"
        )

    # Check sum of status counts = total_stories
    sum_statuses = (
        completed_stories + in_progress_stories + blocked_stories + not_started_stories
    )
    if sum_statuses == total_stories:
        result.add_pass(
            f"Sum of status counts ({sum_statuses}) = total_stories ({total_stories})",
            quiet,
        )
    else:
        result.add_fail(
            f"Sum of status counts ({sum_statuses}) ≠ total_stories ({total_stories})"
        )

    # Check progress_percentage calculation
    if total_stories > 0:
        expected_progress = int((completed_stories * 100) / total_stories)
        if progress_percentage == expected_progress:
            result.add_pass(
                f"progress_percentage ({progress_percentage}%) matches calculation",
                quiet,
            )
        else:
            result.add_fail(
                "progress_percentage "
                f"({progress_percentage}%) ≠ calculated ({expected_progress}%)"
            )
    else:
        if progress_percentage == 0:
            result.add_pass("progress_percentage = 0 when total_stories = 0", quiet)
        else:
            result.add_fail("progress_percentage should be 0 when total_stories = 0")

    # Check all counts are non-negative
    if all(
        count >= 0
        for count in [
            completed_stories,
            in_progress_stories,
            blocked_stories,
            not_started_stories,
        ]
    ):
        result.add_pass("All story counts are non-negative", quiet)
    else:
        result.add_fail("Story counts contain negative values")

    return True


def _resolved_children(data: dict[str, Any], epic_path: Path, result) -> tuple:
    """({child: status} for the listed children that can be read, whether all of
    them could). A child with no card, another epic, or listed twice was failed by
    the child-list check; a status outside the vocabulary is failed here, once."""
    epic_id, kids = data.get("story_id"), data.get("child_stories") or []
    if not isinstance(kids, list):
        return {}, False  # failed by the child-list check
    cards = card_index(epic_path.parent.resolve())
    statuses: dict[str, str] = {}
    for sid in kids:
        epic, status = cards.get(sid, (None, None))
        if epic == epic_id and status not in STORY_STATUSES:
            result.add_fail(
                f"{epic_id}: child {sid} has status '{status}', not one "
                f"of {', '.join(STORY_STATUSES)}"
            )
        elif epic == epic_id:
            statuses[sid] = status
    return statuses, len(statuses) == len(kids)


def validate_children(data, result, quiet=False, epic_path=None) -> None:
    """TD-202: the children are read once, then the counters (AC1) and the epic's
    own status (AC3) are judged against them."""
    log_info("Validation 6: Children recounted by status (TD-202)", quiet)
    if epic_path is None or not isinstance(data.get("story_id"), str):
        return
    statuses, complete = _resolved_children(data, epic_path, result)
    if complete:
        _check_counters(data, statuses, result, quiet)
    _check_epic_status(data, statuses, complete, result, quiet)


def _check_counters(data, statuses: dict, result, quiet) -> None:
    """AC1: each counter the epic states against the children's statuses (counters
    are optional, S1; any one stated is checked, S4 F2)."""
    counted = dict.fromkeys(COUNTED_AS.values(), 0)
    for status in statuses.values():
        counted[COUNTED_AS[status]] += 1
    total = counted["total_stories"] = len(statuses)
    done = counted["completed_stories"]
    counted["progress_percentage"] = int(done * 100 / total) if total else 0
    wrong = [f for f, n in counted.items() if f in data and data[f] != n]
    for field in wrong:
        result.add_fail(
            f"{data['story_id']}: {field} states {data[field]}, "
            f"its children count {counted[field]}"
        )
    if not wrong and any(f in data for f in counted):
        result.add_pass("Stated counters match the children's statuses", quiet)


def _check_epic_status(data, statuses: dict, complete: bool, result, quiet) -> None:
    """AC3. Draft and Done are judged on the children that can be read: a missing
    one cannot clear those faults (S4 F1). 'Every child closed' needs them all."""
    epic_id, status = data["story_id"], data.get("status")
    if status not in STORY_STATUSES:
        result.add_fail(
            f"{epic_id}: status '{status}' is not one of {', '.join(STORY_STATUSES)}"
        )
        return
    started = sorted(
        s for s, st in statuses.items() if st not in NOT_STARTED | {"Cancelled"}
    )
    still_open = sorted(s for s, st in statuses.items() if st not in CLOSED)
    if status == "Draft" and started:
        result.add_fail(
            f"{epic_id}: status Draft, but these children have started: "
            f"{', '.join(started[:8])}"
        )
    elif status in CLOSED and still_open:
        result.add_fail(
            f"{epic_id}: status {status}, but these children are still "
            f"open: {', '.join(still_open[:8])}"
        )
    elif complete and statuses and not still_open and status not in CLOSED:
        result.add_fail(
            f"{epic_id}: every child is closed (Done or Cancelled), but "
            f"its status is {status}"
        )
    elif complete:
        result.add_pass(f"Epic status {status} agrees with its children", quiet)


def validate_sprint_breakdown(
    data: dict[str, Any], result: ValidationResult, quiet: bool = False
) -> bool:
    """
    Validation 3: Sprint Breakdown (Enhancement 2)

    Checks:
    - All sprint_distribution stories are in child_stories
    - No duplicate stories across sprints
    - Sprint progress calculations match story distribution
    """
    log_info("Validation 3: Sprint Breakdown (Enhancement 2)", quiet)

    child_stories = set(data.get("child_stories", []))
    sprint_distribution = data.get("sprint_distribution", {})

    if not sprint_distribution:
        result.add_warning("sprint_distribution is empty or missing")
        return True

    # Collect all stories from sprint distribution
    sprint_stories = []
    for sprint, stories in sprint_distribution.items():
        if isinstance(stories, list):
            sprint_stories.extend(stories)

    # Check all sprint stories are in child_stories
    all_valid = True
    for story in sprint_stories:
        if story not in child_stories:
            result.add_fail(f"Sprint story '{story}' not in child_stories")
            all_valid = False

    if all_valid and sprint_stories:
        result.add_pass("All sprint_distribution stories are in child_stories", quiet)

    # Check for duplicate stories across sprints
    if len(sprint_stories) == len(set(sprint_stories)):
        result.add_pass("No duplicate stories across sprints", quiet)
    else:
        duplicates = [s for s in sprint_stories if sprint_stories.count(s) > 1]
        result.add_fail(f"Duplicate stories found across sprints: {set(duplicates)}")

    # Check sprint_progress calculations if present
    sprint_progress = data.get("sprint_progress", {})
    if sprint_progress:
        for sprint, progress_data in sprint_progress.items():
            if not isinstance(progress_data, dict):
                continue

            total = progress_data.get("total", 0)
            completed = progress_data.get("completed", 0)
            progress_pct = progress_data.get("progress_percentage", 0)

            # Verify sprint total matches distribution count
            distribution_count = len(sprint_distribution.get(sprint, []))
            if total == distribution_count:
                result.add_pass(
                    f"{sprint}: total ({total}) matches distribution", quiet
                )
            else:
                result.add_fail(
                    f"{sprint}: total ({total}) ≠ distribution ({distribution_count})"
                )

            # Verify progress percentage calculation
            if total > 0:
                expected_pct = int((completed * 100) / total)
                if progress_pct == expected_pct:
                    result.add_pass(f"{sprint}: progress_percentage correct", quiet)
                else:
                    result.add_fail(
                        f"{sprint}: progress_percentage "
                        f"({progress_pct}%) ≠ calculated ({expected_pct}%)"
                    )

    return True


def validate_dependencies(
    data: dict[str, Any], result: ValidationResult, quiet: bool = False
) -> bool:
    """
    Validation 4: Story Dependencies (Enhancement 3)

    Checks:
    - All dependency story IDs are in child_stories
    - No circular dependencies (DAG validation)
    - Critical path is valid
    - Independent stories have no hard dependencies
    """
    log_info("Validation 4: Story Dependencies (Enhancement 3)", quiet)

    child_stories = set(data.get("child_stories", []))
    story_dependencies = data.get("story_dependencies", [])

    if not story_dependencies:
        result.add_warning("story_dependencies is empty or missing")
        return True

    # Collect all stories mentioned in dependencies
    dependency_stories = set()
    dependency_graph: dict[str, set[str]] = {}  # story -> depends_on stories

    for dep in story_dependencies:
        if not isinstance(dep, dict):
            continue

        story = dep.get("story")
        depends_on = dep.get("depends_on", [])
        blocks = dep.get("blocks", [])

        if story:
            dependency_stories.add(story)
            dependency_graph[story] = (
                set(depends_on) if isinstance(depends_on, list) else set()
            )

        if isinstance(depends_on, list):
            dependency_stories.update(depends_on)
        if isinstance(blocks, list):
            dependency_stories.update(blocks)

    # Check all dependency stories are in child_stories
    invalid_stories = dependency_stories - child_stories
    if not invalid_stories:
        result.add_pass("All dependency stories are in child_stories", quiet)
    else:
        for story in invalid_stories:
            result.add_fail(f"Dependency story '{story}' not in child_stories")

    # Check for circular dependencies using DFS
    def has_cycle(node: str, visited: set[str], rec_stack: set[str]) -> bool:
        """DFS to detect cycles in dependency graph"""
        visited.add(node)
        rec_stack.add(node)

        for neighbor in dependency_graph.get(node, set()):
            if neighbor not in visited:
                if has_cycle(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True

        rec_stack.remove(node)
        return False

    visited: set[str] = set()
    has_circular = False

    for node in dependency_graph:
        if node not in visited:
            if has_cycle(node, visited, set()):
                has_circular = True
                break

    if not has_circular:
        result.add_pass("No circular dependencies detected", quiet)
    else:
        result.add_fail("Circular dependencies detected in dependency graph")

    # Validate dependency_metadata if present
    dep_metadata = data.get("dependency_metadata", {})
    if dep_metadata:
        # Check critical_path stories are valid
        critical_path = dep_metadata.get("critical_path", [])
        if critical_path:
            invalid_path = [s for s in critical_path if s not in child_stories]
            if not invalid_path:
                result.add_pass("Critical path stories are valid", quiet)
            else:
                for story in invalid_path:
                    result.add_fail(
                        f"Critical path story '{story}' not in child_stories"
                    )

        # Check circular_dependencies is empty
        circular_deps = dep_metadata.get("circular_dependencies", [])
        if not circular_deps:
            result.add_pass("circular_dependencies is empty (no cycles)", quiet)
        else:
            result.add_fail(f"circular_dependencies not empty: {circular_deps}")

        # Check independent_stories have no hard dependencies
        independent = dep_metadata.get("independent_stories", [])
        if independent:
            for story in independent:
                deps = next(
                    (d for d in story_dependencies if d.get("story") == story), {}
                )
                depends_on = deps.get("depends_on", [])
                dep_type = deps.get("dependency_type", "soft")

                if not depends_on or dep_type == "soft":
                    result.add_pass(
                        f"Independent story '{story}' has no hard dependencies", quiet
                    )
                else:
                    result.add_fail(
                        f"Independent story '{story}' has hard dependencies: "
                        f"{depends_on}"
                    )

    return True


def validate_workflow(
    data: dict[str, Any], result: ValidationResult, quiet: bool = False
) -> bool:
    """
    Validation 5: Enhanced Workflow (Enhancement 4)

    Checks:
    - lifecycle_state is valid enum
    - Lifecycle metadata dates are chronological
    - Success criteria have valid status values
    - Blocker/risk fields are properly structured
    """
    log_info("Validation 5: Enhanced Workflow (Enhancement 4)", quiet)

    # Check lifecycle_state
    valid_lifecycle_states = {"planning", "active", "review", "completed", "archived"}
    lifecycle_state = data.get("lifecycle_state")

    if lifecycle_state in valid_lifecycle_states:
        result.add_pass(f"lifecycle_state '{lifecycle_state}' is valid", quiet)
    elif lifecycle_state:
        result.add_fail(
            f"lifecycle_state '{lifecycle_state}' is invalid "
            f"(must be: {', '.join(valid_lifecycle_states)})"
        )
    else:
        result.add_warning("lifecycle_state missing")

    # Check success_criteria
    success_criteria = data.get("success_criteria", [])
    if success_criteria:
        result.add_pass("success_criteria field present", quiet)

        valid_statuses = {"not_started", "in_progress", "completed", "blocked"}
        for i, criterion in enumerate(success_criteria):
            if not isinstance(criterion, dict):
                continue

            status = criterion.get("status")
            if status in valid_statuses:
                result.add_pass(
                    f"success_criteria[{i}] status '{status}' is valid", quiet
                )
            elif status:
                result.add_fail(f"success_criteria[{i}] status '{status}' is invalid")
    else:
        result.add_warning("success_criteria missing (optional but recommended)")

    # Check active_blockers
    active_blockers = data.get("active_blockers", [])
    if active_blockers:
        valid_severities = {"low", "medium", "high", "critical"}
        for i, blocker in enumerate(active_blockers):
            if not isinstance(blocker, dict):
                continue

            severity = blocker.get("severity")
            if severity in valid_severities:
                result.add_pass(
                    f"active_blockers[{i}] severity '{severity}' is valid", quiet
                )
            elif severity:
                result.add_fail(
                    f"active_blockers[{i}] severity '{severity}' is invalid"
                )
    else:
        result.add_pass("active_blockers empty (no current blockers)", quiet)

    # Check active_risks
    active_risks = data.get("active_risks", [])
    if active_risks:
        valid_risk_levels = {"low", "medium", "high"}
        for i, risk in enumerate(active_risks):
            if not isinstance(risk, dict):
                continue

            probability = risk.get("probability")
            impact = risk.get("impact")

            if probability in valid_risk_levels:
                result.add_pass(
                    f"active_risks[{i}] probability '{probability}' is valid", quiet
                )
            elif probability:
                result.add_fail(
                    f"active_risks[{i}] probability '{probability}' is invalid"
                )

            if impact in valid_risk_levels:
                result.add_pass(f"active_risks[{i}] impact '{impact}' is valid", quiet)
            elif impact:
                result.add_fail(f"active_risks[{i}] impact '{impact}' is invalid")

    return True


def validate_file(
    file_path: Path, quiet: bool = False, verbose: bool = False
) -> ValidationResult:
    """
    Validate a single EP story file

    Args:
        file_path: Path to EP story markdown file
        quiet: Suppress info messages
        verbose: Show all validation checks

    Returns:
        ValidationResult with all check results
    """
    result = ValidationResult()

    log_info("=" * 60, quiet)
    log_info(f"Validating: {file_path}", quiet)
    log_info("=" * 60, quiet)

    # Check file exists
    if not file_path.exists():
        result.add_fail(f"File not found: {file_path}")
        return result

    # Extract YAML
    data = extract_yaml_frontmatter(file_path)
    if not data:
        result.add_fail(f"No YAML frontmatter found in {file_path}")
        return result

    # Run all validations
    validate_yaml_structure(file_path, data, result, quiet=quiet and not verbose)
    if "child_stories" in data and data["child_stories"] is None:
        data["child_stories"] = []  # a blank key is no children (TD-202 S7 A2)
    validate_progress_tracking(
        data, result, quiet=quiet and not verbose, epic_path=file_path
    )
    validate_children(data, result, quiet and not verbose, file_path)
    validate_sprint_breakdown(data, result, quiet=quiet and not verbose)
    validate_dependencies(data, result, quiet=quiet and not verbose)
    validate_workflow(data, result, quiet=quiet and not verbose)
    validate_progress_block(file_path, result, quiet=quiet and not verbose)

    return result


def print_summary(results: list[ValidationResult], strict: bool = False):
    """Print validation summary"""
    total_checks = sum(r.total_checks for r in results)
    passed_checks = sum(r.passed_checks for r in results)
    failed_checks = sum(r.failed_checks for r in results)
    warning_checks = sum(r.warning_checks for r in results)

    all_errors = [e for r in results for e in r.errors]
    all_warnings = [w for r in results for w in r.warnings]

    print()
    log_info("=" * 60)
    log_info("Validation Summary")
    log_info("=" * 60)
    print(f"Total Checks:  {total_checks}")
    print(f"{Colors.GREEN}Passed:{Colors.NC}        {passed_checks}")
    print(f"{Colors.RED}Failed:{Colors.NC}        {failed_checks}")
    print(f"{Colors.YELLOW}Warnings:{Colors.NC}      {warning_checks}")

    # Show errors
    if all_errors:
        print()
        print(f"{Colors.RED}{'=' * 60}{Colors.NC}")
        print(f"{Colors.RED}Validation Errors:{Colors.NC}")
        print(f"{Colors.RED}{'=' * 60}{Colors.NC}")
        for error in all_errors:
            print(f"  {Colors.RED}•{Colors.NC} {error}")

    # Show warnings
    if all_warnings:
        print()
        print(f"{Colors.YELLOW}{'=' * 60}{Colors.NC}")
        print(f"{Colors.YELLOW}Validation Warnings:{Colors.NC}")
        print(f"{Colors.YELLOW}{'=' * 60}{Colors.NC}")
        for warning in all_warnings:
            print(f"  {Colors.YELLOW}•{Colors.NC} {warning}")

    # Final status
    if failed_checks > 0:
        return 1
    elif strict and warning_checks > 0:
        print()
        print(f"{Colors.RED}Strict mode: Treating warnings as errors{Colors.NC}")
        return 1
    else:
        print()
        print(f"{Colors.GREEN}{'=' * 60}{Colors.NC}")
        print(f"{Colors.GREEN}Validation PASSED{Colors.NC}")
        print(f"{Colors.GREEN}{'=' * 60}{Colors.NC}")
        return 0


def main():
    """Main script execution"""
    parser = argparse.ArgumentParser(
        description="Validate EP stories with SC-004 enhancements",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate single epic (its children are read from the cards beside it)
  python3 epic-validator.py docs-copper/roadmap/backlog/EP-001-customer-search.md

  # Validate all epics
  python3 epic-validator.py docs-copper/roadmap/backlog/EP-*.md

  # Strict validation (warnings = errors)
  python3 epic-validator.py --strict docs-copper/roadmap/backlog/EP-*.md
        """,
    )

    parser.add_argument(
        "files", nargs="+", type=Path, help="EP story files to validate"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Verbose output (show all checks)"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Quiet mode (only show errors)"
    )
    parser.add_argument(
        "--strict", action="store_true", help="Treat warnings as errors"
    )

    args = parser.parse_args()

    # Validate each file
    results = []
    for file_path in args.files:
        result = validate_file(file_path, quiet=args.quiet, verbose=args.verbose)
        results.append(result)

    # Print summary and exit
    exit_code = print_summary(results, strict=args.strict)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
