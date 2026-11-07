#!/usr/bin/env python3
# ruff: noqa: E501
"""
Pipeline Validator - COPPER Story Delivery Pipeline

Invoked by the OpenCode custom tool pipeline-validator.ts.
Validates evidence, status consistency, and cross-references for the cu-pipe pipeline.

Usage:
    python3 pipeline_validator.py verify  <story_id> <stage> [--root DIR]
    python3 pipeline_validator.py status  <story_id>           [--root DIR]
    python3 pipeline_validator.py audit                        [--root DIR]

Exit codes: 0 = pass, 1 = validation failure, 2 = runtime error
Output: JSON to stdout
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# TD-178: the documentation root is DISCOVERED, not hardcoded. Changed LAST of the
# targets (S2 W4) , this is the pipeline's OWN instrument, so the six guards proved
# the contract before it was applied here. `--root` already existed and remains the
# explicit layer.
DOCS_ROOT_ENV = "COPPER_DOCS_ROOT"
DOCS_ROOT_CANDIDATES = ("docs-copper", "docs")
DOCS_ROOT_MARKERS = ("roadmap", "dev-journal")


def _docs_root_name(root: Path) -> str:
    """NAME of the documentation directory; historical default if none matches."""
    override = os.environ.get(DOCS_ROOT_ENV)
    if override:
        # TD-178 S4 G4: keep the override USABLE. Returning the bare basename
        # discarded its directory, so an override outside the project resolved to
        # `root/<basename>` , which does not exist. Relative to `root` where
        # possible (these callers join it onto `root`), absolute otherwise.
        candidate = Path(override)
        try:
            return str(candidate.relative_to(root))
        except ValueError:
            return str(candidate)
    for name in DOCS_ROOT_CANDIDATES:
        candidate = root / name
        if candidate.is_dir() and any(
            (candidate / m).is_dir() for m in DOCS_ROOT_MARKERS
        ):
            return name
    return DOCS_ROOT_CANDIDATES[0]


_DOCS = DOCS_ROOT_CANDIDATES[0]
PIPELINE_DIR = f"{_DOCS}/roadmap/pipeline-audit-trail"
STORY_DIR = f"{_DOCS}/roadmap/backlog"
ARTIFACTS_DIR = f"{PIPELINE_DIR}/artifacts"
DEV_JOURNAL_DIR = f"{_DOCS}/dev-journal"


def _bind_docs_root(root: Path) -> None:
    """Rebind the module-level path constants to the discovered documentation root."""
    global _DOCS, PIPELINE_DIR, STORY_DIR, ARTIFACTS_DIR, DEV_JOURNAL_DIR
    _DOCS = _docs_root_name(root)
    PIPELINE_DIR = f"{_DOCS}/roadmap/pipeline-audit-trail"
    STORY_DIR = f"{_DOCS}/roadmap/backlog"
    ARTIFACTS_DIR = f"{PIPELINE_DIR}/artifacts"
    DEV_JOURNAL_DIR = f"{_DOCS}/dev-journal"


# Status enums (from cu-pipe.md Phase 3)
PIPELINE_TOP_LEVEL_STATUSES = {"active", "completed", "abandoned"}
STAGE_LEVEL_STATUSES = {
    "pending",
    "in_progress",
    "completed",
    "blocked",
    "bypassed",
    "abandoned",
}

# Records tagged schema_version: 1 are the TD-171 AC1 legacy quarantine ,
# accurate histories of the May-2026 pipeline schema, skipped (and counted)
# by the audit rather than judged against a schema they were never written to.
LEGACY_SCHEMA_VERSION = 1


def _load_quality_gate_vocabulary() -> dict[str, frozenset[str]]:
    """Load the canonical quality-gate status classes (BUG-004).

    Mirrors ``_load_story_statuses`` deliberately: same file, same
    beside-the-script path resolution (valid across the kits/core, .opencode and
    .claude layouts), and the same FAIL-CLOSED contract , exit 2 on a missing or
    malformed vocabulary rather than a guessed enum. A checker that cannot load
    its own vocabulary must not decide that gates passed.

    Returns three lowercase alias sets keyed ``pass`` / ``not_applicable`` /
    ``fail``. A status matching none of them is UNKNOWN and fails at the call
    site , see ``_check_quality_gates_pass``.
    """
    vocab_path = Path(__file__).resolve().parent / "status-vocabulary.json"
    try:
        classes = json.loads(vocab_path.read_text(encoding="utf-8"))[
            "quality_gate_status"
        ]
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print(
            json.dumps(
                {"error": f"Cannot load quality-gate vocabulary at {vocab_path}: {exc}"}
            )
        )
        sys.exit(2)
    if not isinstance(classes, dict) or set(classes) != {
        "pass",
        "not_applicable",
        "fail",
    }:
        print(
            json.dumps(
                {
                    "error": f"Malformed quality_gate_status in {vocab_path}: expected "
                    f"exactly the keys pass/not_applicable/fail"
                }
            )
        )
        sys.exit(2)
    out: dict[str, frozenset[str]] = {}
    for key, values in classes.items():
        if (
            not isinstance(values, list)
            or not values
            or not all(isinstance(v, str) for v in values)
        ):
            print(
                json.dumps(
                    {"error": f"Malformed quality_gate_status.{key} in {vocab_path}"}
                )
            )
            sys.exit(2)
        out[key] = frozenset(v.strip().lower() for v in values)
    return out


def _load_story_statuses() -> frozenset[str]:
    """Load the canonical story-status set from the shared vocabulary (TD-171 AC3).

    One definition point for this validator AND user-story-validator.py ,
    the file sits beside this script in tools/ in every layout. Fail closed:
    exit 2 (runtime error), never a silently guessed enum.
    """
    vocab_path = Path(__file__).resolve().parent / "status-vocabulary.json"
    try:
        values = json.loads(vocab_path.read_text(encoding="utf-8"))["story_status"]
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print(
            json.dumps(
                {
                    "error": f"Cannot load canonical status vocabulary at {vocab_path}: {exc}"
                }
            )
        )
        sys.exit(2)
    if (
        not isinstance(values, list)
        or not values
        or not all(isinstance(v, str) for v in values)
    ):
        print(json.dumps({"error": f"Malformed story_status list in {vocab_path}"}))
        sys.exit(2)
    return frozenset(values)


STORY_FRONTMATTER_STATUSES = _load_story_statuses()

# Required fields per completed stage
COMPLETED_STAGE_REQUIRED_FIELDS = {"status", "completed_at", "evidence"}

# Per-stage evidence verification (from Phase 4.9)
STAGE_EVIDENCE_RULES: dict[str, dict[str, Any]] = {
    "S0_SELECT": {
        "description": "Feature branch exists; YAML state file created; story status is In Progress",
        "checks": ["branch_exists", "yaml_exists", "story_in_progress"],
    },
    "S1_KICKOFF": {
        "description": "Kickoff artifact exists; story file changed since S0; challenge log entries",
        "checks": ["artifact_s1_exists", "story_changed", "evidence_non_empty"],
    },
    "S2_PLAN": {
        "description": "Plan artifact exists with alternatives and risk sections",
        "checks": ["artifact_s2_exists", "evidence_non_empty"],
    },
    "S3_EXECUTE": {
        "description": "Working tree or commits contain deliverables; AC self-review present",
        "checks": ["evidence_non_empty", "has_commits_since_s2"],
    },
    "S4_CODE_REVIEW": {
        "description": "Quality review command output with Overall Status PASS/FAIL",
        "checks": ["evidence_has_pass_fail"],
    },
    "S5_ARCH_SEC_COMP_REVIEW": {
        "description": "Architecture review with findings table, risk register, PASS/FAIL",
        "checks": ["evidence_has_pass_fail"],
    },
    "S6_TEST_QUALITY_VERIFY": {
        "description": "Quality gates all pass; verified_claims non-empty",
        "checks": ["evidence_has_pass_fail", "quality_gates_pass"],
    },
    "S7_CRITICAL_REVIEW": {
        "description": "DoD verification with definitive status for every criterion",
        "checks": ["evidence_has_pass_fail"],
    },
    "S8_CAPTURE": {
        "description": "Dev-journal on disk; memory-bank updated; readme-update executed",
        "checks": ["dev_journal_exists", "evidence_non_empty"],
    },
    # TD-173: S9 asserts the story is still In Progress, NOT Done. A story is Done
    # only when its pipeline is `completed`, which happens at or after the merge ,
    # so demanding Done here contradicted the `audit` rule that refuses Done while
    # the pipeline is active. With S10 pending, no status satisfied both. The
    # check-set now reads as the lifecycle: S0 In Progress -> S9 In Progress ->
    # S10 Done.
    #
    # READING AN OLD RECORD (S5 V4): 168 records carry `S9_CLOSE: completed` from
    # BEFORE this change. They were verified against the previous rule, which
    # asserted the story was `Done`; this one asserts `In Progress`. Their stored
    # evidence is untouched and nothing about them needs correcting , the per-stage
    # checks are point-in-time and the `audit` never invoked them , but the CLAIM
    # implied by "S9 completed" is not the same claim it was when those records were
    # written. Noted here rather than left to be inferred: silently applying today's
    # semantics to yesterday's evidence is its own kind of drift.
    "S9_CLOSE": {
        "description": "Story still In Progress (Done comes at merge); close docs committed",
        "checks": ["story_in_progress", "evidence_non_empty"],
    },
    # TD-173: `story_status_done` moved here from S9 rather than deleted. S10 is
    # marked completed AFTER the merge, which is exactly when Done becomes true.
    # This overlaps `audit_all`'s completed=>Done rule deliberately , that one is
    # corpus-wide and post-hoc, this one reports at the moment the mistake is made.
    # Recorded as redundancy, not claimed as independent coverage.
    "S10_MERGE": {
        "description": "Branch pushed; MR URL valid; user confirmed merge; story Done",
        "checks": ["evidence_non_empty", "story_status_done"],
    },
    # Legacy stage names (pre-S9/S10 split)
    "S5_ARCH_SEC_COMP": {
        "description": "Architecture review (legacy truncated name)",
        "checks": ["evidence_has_pass_fail"],
    },
    "S6_TEST_QUALITY": {
        "description": "Quality verification (legacy truncated name)",
        "checks": ["evidence_has_pass_fail"],
    },
    # v1 legacy names
    "S1_INIT": {
        "description": "Initialisation (v1 legacy)",
        "checks": ["evidence_non_empty"],
    },
    "S2_DESIGN": {
        "description": "Design (v1 legacy)",
        "checks": ["evidence_non_empty"],
    },
    "S3_BUILD": {
        "description": "Build (v1 legacy)",
        "checks": ["evidence_non_empty"],
    },
    "S4_REVIEW_QUALITY": {
        "description": "Quality review (v1 legacy)",
        "checks": ["evidence_has_pass_fail"],
    },
    "S5_REVIEW_SECURITY": {
        "description": "Security review (v1 legacy)",
        "checks": ["evidence_has_pass_fail"],
    },
    "S6_REVIEW_CONSISTENCY": {
        "description": "Consistency review (v1 legacy)",
        "checks": ["evidence_has_pass_fail"],
    },
    "S7_REVIEW_DOCS": {
        "description": "Docs review (v1 legacy)",
        "checks": ["evidence_has_pass_fail"],
    },
    "S8_CLOSE": {
        "description": "Close (v1 legacy)",
        "checks": ["evidence_non_empty"],
    },
    "S9_MERGE": {
        "description": "Merge (v1 legacy)",
        "checks": ["evidence_non_empty"],
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _yaml_safe_load(path: Path) -> dict | None:
    """Load YAML if pyyaml is available, else return None."""
    try:
        import yaml

        with open(path) as f:
            return yaml.safe_load(f)
    except ImportError:
        return None


def _find_yaml(root: Path, story_id: str) -> Path | None:
    """Locate the pipeline YAML for a given story ID."""
    candidates = list((root / PIPELINE_DIR).glob(f"{story_id}.yaml"))
    return candidates[0] if candidates else None


def _find_story(root: Path, story_id: str) -> Path | None:
    """Locate the story markdown file."""
    pattern = f"{story_id}-*.md"
    candidates = list((root / STORY_DIR).glob(pattern))
    return candidates[0] if candidates else None


def _parse_story_frontmatter(path: Path) -> dict[str, Any]:
    """Extract YAML frontmatter from a markdown file."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end < 0:
        return {}
    fm_text = text[3:end].strip()
    try:
        import yaml

        return yaml.safe_load(fm_text) or {}
    except Exception:
        return {}


def _git_branch_exists(branch: str, root: Path) -> bool:
    """Check if a git branch exists."""
    try:
        result = subprocess.run(
            ["git", "branch", "--list", branch],
            capture_output=True,
            text=True,
            cwd=root,
        )
        return bool(result.stdout.strip())
    except Exception:
        return False


def _git_log_oneline(count: int, root: Path) -> list[str]:
    """Get recent git log entries."""
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", f"-{count}"],
            capture_output=True,
            text=True,
            cwd=root,
        )
        return result.stdout.strip().split("\n") if result.stdout.strip() else []
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class CheckResult:
    """Single check result."""

    name: str
    passed: bool
    message: str
    severity: str = "error"  # error | warning | info


@dataclass
class ValidationResult:
    """Aggregated validation result."""

    story_id: str
    action: str
    stage: str | None = None
    passed: bool = True
    checks: list[CheckResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)

    def add(self, name: str, passed: bool, message: str, severity: str = "error"):
        self.checks.append(CheckResult(name, passed, message, severity))
        if not passed:
            self.passed = False
            if severity == "error":
                self.errors.append(f"{name}: {message}")
            elif severity == "warning":
                self.warnings.append(f"{name}: {message}")

    def to_json(self) -> dict:
        return {
            "story_id": self.story_id,
            "action": self.action,
            "stage": self.stage,
            "passed": self.passed,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings,
            "checks": [
                {
                    "name": c.name,
                    "passed": c.passed,
                    "message": c.message,
                    "severity": c.severity,
                }
                for c in self.checks
            ],
            "details": self.details,
        }


# ---------------------------------------------------------------------------
# Core validation actions
# ---------------------------------------------------------------------------


def verify_stage(root: Path, story_id: str, stage: str) -> ValidationResult:
    """Verify evidence for a specific stage of a story."""
    result = ValidationResult(story_id=story_id, action="verify", stage=stage)

    yaml_path = _find_yaml(root, story_id)
    if not yaml_path:
        result.add(
            "yaml_exists",
            False,
            f"Pipeline YAML not found: {PIPELINE_DIR}/{story_id}.yaml",
        )
        return result
    result.add("yaml_exists", True, str(yaml_path))

    data = _yaml_safe_load(yaml_path)
    if not data:
        result.add(
            "yaml_parseable", False, "Could not parse pipeline YAML (install pyyaml?)"
        )
        return result
    result.add("yaml_parseable", True, "OK")

    # Check stage exists
    stages = data.get("stages", {})
    if stage not in stages:
        result.add(
            "stage_exists",
            False,
            f"Stage {stage} not found in YAML. Available: {sorted(stages.keys())}",
        )
        return result
    result.add("stage_exists", True, f"Found {stage}")

    stage_data = stages[stage]
    stage_status = stage_data.get("status", "")

    # Status enum check
    if stage_status not in STAGE_LEVEL_STATUSES:
        result.add(
            "stage_status_enum", False, f"Invalid stage status: {stage_status!r}"
        )
    else:
        result.add("stage_status_enum", True, f"Status: {stage_status}")

    # Required fields check (only for completed stages)
    if stage_status == "completed":
        for field_name in COMPLETED_STAGE_REQUIRED_FIELDS:
            if field_name not in stage_data:
                result.add(
                    f"has_{field_name}", False, f"Missing required field: {field_name}"
                )
            else:
                result.add(f"has_{field_name}", True, f"OK: {field_name}")

    # Evidence checks
    evidence = stage_data.get("evidence", [])
    if not evidence:
        result.add(
            "evidence_non_empty",
            False,
            "No evidence recorded for this stage",
            "warning",
        )
    else:
        result.add("evidence_non_empty", True, f"{len(evidence)} evidence items")

    # Stage-specific checks
    rules = STAGE_EVIDENCE_RULES.get(stage, {})
    for check_name in rules.get("checks", []):
        _run_stage_check(root, story_id, stage, data, stage_data, check_name, result)

    # Cross-reference , BOTH arms, matching `audit_all` exactly.
    #
    # TD-173 S4 T1: this block used to carry only the `completed` arm, so a story
    # marked Done while its pipeline was still `active` PASSED verify and FAILED
    # audit , the same one-condition-two-verdicts defect this story exists to end,
    # relocated rather than removed. Completing the pair here fixes it for EVERY
    # stage rather than patching the one where it happened to surface, so no future
    # stage can disagree with the audit on story-status alignment.
    top_level = data.get("status", "")
    if top_level in {"completed", "active"}:
        story_path = _find_story(root, story_id)
        if story_path:
            fm = _parse_story_frontmatter(story_path)
            fm_status = fm.get("status", "")
            if top_level == "completed" and fm_status != "Done":
                result.add(
                    "crossref_story_done",
                    False,
                    f"Pipeline completed but story frontmatter is {fm_status!r} (expected 'Done')",
                )
            elif top_level == "active" and fm_status == "Done":
                result.add(
                    "crossref_active_vs_done",
                    False,
                    "Pipeline active but story is already Done",
                )
            else:
                result.add(
                    "crossref_story_status", True, "Pipeline and story status agree"
                )

    result.details["stage_status"] = stage_status
    result.details["top_level_status"] = top_level
    result.details["evidence_count"] = len(evidence)

    return result


def show_status(root: Path, story_id: str) -> ValidationResult:
    """Show pipeline status with consistency checks."""
    result = ValidationResult(story_id=story_id, action="status")

    yaml_path = _find_yaml(root, story_id)
    if not yaml_path:
        result.add("yaml_exists", False, f"Pipeline YAML not found for {story_id}")
        return result
    result.add("yaml_exists", True, str(yaml_path))

    data = _yaml_safe_load(yaml_path)
    if not data:
        result.add("yaml_parseable", False, "Could not parse pipeline YAML")
        return result

    # Top-level status
    top_status = data.get("status", "")
    if top_status in PIPELINE_TOP_LEVEL_STATUSES:
        result.add("top_level_status", True, f"Pipeline status: {top_status}")
    else:
        result.add(
            "top_level_status", False, f"Invalid top-level status: {top_status!r}"
        )

    # Current stage
    current = data.get("current_stage", "unknown")
    result.details["current_stage"] = current

    # Stage summary
    stages = data.get("stages", {})
    stage_summary: dict[str, str] = {}
    for k, v in stages.items():
        s = v.get("status", "missing") if isinstance(v, dict) else "malformed"
        stage_summary[k] = s
        if s not in STAGE_LEVEL_STATUSES and s not in ("missing", "malformed"):
            result.add(f"stage_enum_{k}", False, f"Invalid stage status: {k}={s!r}")

    result.details["stages"] = stage_summary
    result.details["schema_version"] = data.get("schema_version", "unknown")
    result.details["story_path"] = data.get("story_path", "missing")
    result.details["feature_branch"] = data.get("feature_branch", "missing")

    # Cross-reference with story frontmatter
    story_path = _find_story(root, story_id)
    if story_path:
        fm = _parse_story_frontmatter(story_path)
        fm_status = fm.get("status", "")
        result.details["story_frontmatter_status"] = fm_status

        if fm_status in STORY_FRONTMATTER_STATUSES:
            result.add("story_status_enum", True, f"Story frontmatter: {fm_status}")
        else:
            result.add(
                "story_status_enum", False, f"Invalid story status: {fm_status!r}"
            )

        # Cross-reference consistency
        if top_status == "completed" and fm_status != "Done":
            result.add(
                "crossref_completed_vs_done",
                False,
                f"Pipeline completed but story is {fm_status!r}, expected 'Done'",
            )
        elif top_status == "active" and fm_status == "Done":
            # TD-173: an ERROR here, matching `audit_all`. This condition used to be
            # a "warning" on this path and a hard error on the audit path , one rule
            # with two verdicts depending which entry point the caller came through,
            # which is how a gate quietly becomes advice.
            result.add(
                "crossref_active_vs_done",
                False,
                "Pipeline active but story is already Done",
            )
        else:
            result.add(
                "crossref_consistency", True, "Pipeline and story status are consistent"
            )
    else:
        result.add(
            "story_file_exists",
            False,
            f"Story file not found for {story_id}",
            "warning",
        )

    return result


def audit_all(root: Path) -> dict[str, Any]:
    """Full consistency audit across all pipeline YAMLs."""
    pipeline_dir = root / PIPELINE_DIR
    if not pipeline_dir.exists():
        return {
            "passed": False,
            "errors": [f"Pipeline directory not found: {PIPELINE_DIR}"],
        }

    # TD-171 D5: glob EVERY record. The previous "US-*.yaml" glob left 35 of 187
    # records (BUG-/SEC-/SP-/TD- prefixes) permanently unaudited, and 4 stale
    # records hid there. A gate that reports "total" over a subset overstates
    # what it verified.
    yaml_files = sorted(pipeline_dir.glob("*.yaml"))
    if not yaml_files:
        return {"passed": False, "errors": ["No pipeline YAML files found"]}

    total = len(yaml_files)
    passed = 0
    failed = 0
    legacy_skipped = 0
    results: list[dict] = []

    for yf in yaml_files:
        story_id = yf.stem
        data = _yaml_safe_load(yf)

        if not data:
            failed += 1
            results.append(
                {
                    "story_id": story_id,
                    "passed": False,
                    "errors": ["Could not parse YAML"],
                }
            )
            continue

        # TD-171 AC1: legacy quarantine , distinct outcome, never a pass or fail.
        # str() coercion: a hand-tagged '1' (string) means the same as 1 (int),
        # and '1' never legitimately means schema v2 , so coercing cannot
        # smuggle a current record past the audit.
        if str(data.get("schema_version", "")).strip() == str(LEGACY_SCHEMA_VERSION):
            legacy_skipped += 1
            results.append(
                {
                    "story_id": story_id,
                    "passed": None,
                    "legacy_skipped": True,
                    "errors": [],
                }
            )
            continue

        errors: list[str] = []

        # Top-level status
        top = data.get("status", "")
        if top not in PIPELINE_TOP_LEVEL_STATUSES:
            errors.append(f"Invalid top-level status: {top!r}")

        # Stage statuses
        stages = data.get("stages", {})
        for sk, sv in stages.items():
            if isinstance(sv, dict):
                ss = sv.get("status", "")
                if ss and ss not in STAGE_LEVEL_STATUSES:
                    errors.append(f"Invalid stage status: {sk}={ss!r}")

        # Cross-reference with story
        story_path = _find_story(root, story_id)
        if story_path:
            fm = _parse_story_frontmatter(story_path)
            fm_status = fm.get("status", "")
            if fm_status not in STORY_FRONTMATTER_STATUSES:
                errors.append(f"Invalid story frontmatter status: {fm_status!r}")
            elif top == "completed" and fm_status != "Done":
                errors.append(f"Pipeline completed but story is {fm_status!r}")
            elif top == "active" and fm_status == "Done":
                errors.append("Pipeline active but story is already Done")
        else:
            errors.append("Story file not found")

        ok = len(errors) == 0
        if ok:
            passed += 1
        else:
            failed += 1

        results.append({"story_id": story_id, "passed": ok, "errors": errors})

    return {
        "passed": failed == 0,
        "total": total,
        "checked": total - legacy_skipped,
        "legacy_skipped": legacy_skipped,
        "passed_count": passed,
        "failed_count": failed,
        "results": results,
    }


# ---------------------------------------------------------------------------
# Stage-specific check implementations
# ---------------------------------------------------------------------------


def _run_stage_check(
    root: Path,
    story_id: str,
    stage: str,
    yaml_data: dict,
    stage_data: dict,
    check_name: str,
    result: ValidationResult,
):
    """Dispatch to a specific check implementation."""
    check_fn = _CHECK_DISPATCH.get(check_name)
    if check_fn:
        check_fn(root, story_id, stage, yaml_data, stage_data, result)
    else:
        result.add(check_name, True, "Check not yet implemented", "info")


def _check_branch_exists(root, story_id, stage, yaml_data, stage_data, result):
    # TD-171 D6: `feature_branch` is canonical; `branch` is tolerated because the
    # cu-pipe Phase 3 template documented it for months and records conforming to
    # the documented template must not fail verification.
    branch = yaml_data.get("feature_branch", "") or yaml_data.get("branch", "")
    if not branch:
        result.add("branch_exists", False, "No feature_branch recorded in YAML")
        return
    if _git_branch_exists(branch, root):
        result.add("branch_exists", True, f"Branch {branch} exists")
    else:
        result.add("branch_exists", False, f"Branch {branch} not found", "warning")


def _check_yaml_exists(root, story_id, stage, yaml_data, stage_data, result):
    result.add("yaml_exists", True, "YAML loaded successfully")


def _check_story_in_progress(root, story_id, stage, yaml_data, stage_data, result):
    story_path = _find_story(root, story_id)
    if not story_path:
        result.add("story_in_progress", False, "Story file not found")
        return
    fm = _parse_story_frontmatter(story_path)
    status = fm.get("status", "")
    if status == "In Progress":
        result.add("story_in_progress", True, "Story status is In Progress")
    else:
        result.add(
            "story_in_progress",
            False,
            f"Story status is {status!r}, expected 'In Progress'",
        )


def _check_artifact_s1_exists(root, story_id, stage, yaml_data, stage_data, result):
    artifacts_dir = root / ARTIFACTS_DIR
    candidates = (
        list(artifacts_dir.glob(f"{story_id}-s1-kickoff*"))
        if artifacts_dir.exists()
        else []
    )
    if candidates:
        result.add("artifact_s1_exists", True, str(candidates[0].relative_to(root)))
    else:
        result.add(
            "artifact_s1_exists",
            False,
            f"No S1 kickoff artifact found in {ARTIFACTS_DIR}/",
        )


def _check_artifact_s2_exists(root, story_id, stage, yaml_data, stage_data, result):
    artifacts_dir = root / ARTIFACTS_DIR
    candidates = (
        list(artifacts_dir.glob(f"{story_id}-s2-plan*"))
        if artifacts_dir.exists()
        else []
    )
    if candidates:
        result.add("artifact_s2_exists", True, str(candidates[0].relative_to(root)))
    else:
        result.add(
            "artifact_s2_exists",
            False,
            f"No S2 plan artifact found in {ARTIFACTS_DIR}/",
        )


def _check_story_changed(root, story_id, stage, yaml_data, stage_data, result):
    result.add(
        "story_changed", True, "Story changed check deferred to cu-pipe runtime", "info"
    )


def _check_evidence_non_empty(root, story_id, stage, yaml_data, stage_data, result):
    evidence = stage_data.get("evidence", [])
    if evidence:
        result.add(
            "evidence_non_empty", True, f"{len(evidence)} evidence items recorded"
        )
    else:
        result.add("evidence_non_empty", False, "No evidence recorded", "warning")


# BUG-004 AC5 , RESOLVED BY MEASUREMENT AS "NOT FIXABLE AT THIS LAYER".
#
# The check below is a SUBSTRING match, and the story asked whether that is worth
# keeping. Two stricter designs were IMPLEMENTED and MEASURED against all 1,914
# completed stages. Both were worse than the permissive form:
#
#   1. WORD-BOUNDARY TOKENS , newly failed 5 stages, including US-121's genuine
#      "271/271 tests passing" (no standalone "pass" token). Stricter, not more
#      correct.
#   2. NON-VERIFICATION PHRASE LIST ("unverified", "did not verify", "could not
#      check") , reddened 15 stages, ALL FALSE POSITIVES: TD-172 describing "
#      signatures that did not verify" (the bug it FIXED), US-349 quoting its own
#      rule that '"could not check" must never share a code with checked-and-
#      clean', SP-105 recording capabilities "honestly declared (unverified), not
#      falsely claimed". Narrowing to first-person ("we/I skipped verifying") cut
#      it to 3 , STILL all false positives.
#
# The last of those three is why this stops here. SEC-004's S9 evidence reads
# "...and I never checked the result. Exactly the self-attestation this pipeline
# exists to prevent." That is a first-person admission of not checking, inside
# evidence that is otherwise exemplary , a RETROSPECTIVE account of a past
# mistake, not a claim about this stage. No lexical rule separates it from the
# target case ("we skipped verifying this stage"): the difference is SEMANTIC, in
# what the sentence refers to, and quote-detection separates only the two quoted
# instances, not this one.
#
# So the permissive form is KEPT DELIBERATELY. Making the check stricter would
# punish precisely the candid self-reporting the pipeline is built to encourage,
# and a fail-CLOSED evidence check would be a worse trade than the narrow
# fail-open it removes. The real fix is STRUCTURED status (a parsed field rather
# than prose), which is a schema change to the evidence contract , recorded here
# so the next reader inherits the measurement rather than repeating it.


def _check_evidence_has_pass_fail(root, story_id, stage, yaml_data, stage_data, result):
    """Evidence must carry a status indicator.

    BUG-004 AC5 asked whether this substring match is worth keeping. It is , and
    that verdict is MEASURED, not assumed: see the block comment above, which
    records the two stricter designs that were implemented, run against all 1,914
    completed stages, and found WORSE than this one. This check's residual
    weakness (evidence that says verification did not happen still contains a
    status word) is real but is not closable by matching prose; it needs a
    structured status field, which is an evidence-schema change.
    """
    evidence = stage_data.get("evidence", [])
    text = " ".join(str(e) for e in evidence).lower()

    if "pass" in text or "fail" in text or "skip" in text:
        result.add("evidence_has_pass_fail", True, "Evidence contains status indicator")
    else:
        result.add(
            "evidence_has_pass_fail",
            False,
            "Evidence does not contain PASS/FAIL/SKIP status",
            "warning",
        )


def _check_has_commits_since_s2(root, story_id, stage, yaml_data, stage_data, result):
    result.add(
        "has_commits_since_s2", True, "Commit check deferred to cu-pipe runtime", "info"
    )


def _check_quality_gates_pass(root, story_id, stage, yaml_data, stage_data, result):
    """S6 gate check , PASS only if every gate passed or did not apply.

    BUG-004: the previous implementation was FAIL-OPEN by vacuous truth. It read
    ``all(g.get("status") == "pass" for g in gates if isinstance(g, dict))`` over
    ``quality_gates``, which is a MAPPING , so ``for g in gates`` yielded KEYS
    (strings), every ``isinstance(g, dict)`` was False, the comprehension was
    empty, and ``all([])`` is True. The check reported "All 6 quality gates pass"
    while never reading a single status, and did so on records that recorded
    ``unit_tests: fail``.

    Statuses are classified into three CLASSES (see ``quality_gate_status`` in
    status-vocabulary.json), because a gate has three meaningful outcomes , not
    two. Anything unrecognised FAILS: fail-closed is the whole lesson of this
    defect, and without it the same vacuity returns via a new spelling.
    """
    gates = yaml_data.get("quality_gates")
    if gates is None or gates == {} or gates == []:
        result.add(
            "quality_gates_pass", True, "No quality_gates field (legacy YAML)", "info"
        )
        return

    # AC2/AC3: the mapping is the only supported shape (180/180 real records use
    # it). An unrecognised shape REFUSES rather than passing , an unreadable gate
    # record is an unverified gate, and silently passing it is this very defect.
    if not isinstance(gates, dict):
        result.add(
            "quality_gates_pass",
            False,
            f"quality_gates must be a mapping of name -> {{status}}, got "
            f"{type(gates).__name__}. Refusing rather than reporting green on a "
            f"shape this check cannot read.",
        )
        return

    vocab = _load_quality_gate_vocabulary()
    passing, not_applicable, failing, unknown = [], [], [], []
    for name, entry in gates.items():
        status = entry.get("status") if isinstance(entry, dict) else entry
        # S4 review finding: a non-string status must be classified as UNKNOWN
        # WITHOUT being used as a set key. An unhashable value (list/dict) raised
        # TypeError here and the caller got NO verdict at all , strictly worse
        # than the fail-open this story removes, since a crash is not a result.
        if not isinstance(status, str):
            unknown.append(f"{name}={status!r}")
            continue
        status_key = status.strip().lower()
        if status_key in vocab["pass"]:
            passing.append(name)
        elif status_key in vocab["not_applicable"]:
            not_applicable.append(name)
        elif status_key in vocab["fail"]:
            failing.append(f"{name}={status!r}")
        else:
            unknown.append(f"{name}={status!r}")

    if failing or unknown:
        parts = []
        if failing:
            parts.append(f"failing: {failing}")
        if unknown:
            parts.append(f"unrecognised status (fail-closed): {unknown}")
        result.add("quality_gates_pass", False, "; ".join(parts))
        return

    detail = f"{len(passing)} pass"
    if not_applicable:
        detail += f", {len(not_applicable)} not-applicable ({not_applicable})"
    result.add(
        "quality_gates_pass", True, f"All {len(gates)} quality gates OK , {detail}"
    )


def _check_dev_journal_exists(root, story_id, stage, yaml_data, stage_data, result):
    closure = yaml_data.get("closure_checks", {})
    dj_raw = closure.get("dev_journal", "")

    # dev_journal can be a string path, or a dict with 'reason' containing the path
    dj_path = ""
    if isinstance(dj_raw, str):
        dj_path = dj_raw
    elif isinstance(dj_raw, dict):
        reason = str(dj_raw.get("reason", ""))
        if reason:
            for token in reason.split():
                if token.startswith("docs-copper/") and token.endswith(".md"):
                    dj_path = token
                    break

    if not dj_path:
        evidence = stage_data.get("evidence", [])
        for e in evidence:
            if "dev-journal" in str(e).lower() or "dev_journal" in str(e).lower():
                dj_path = str(e)
                break

    if dj_path and (root / dj_path).exists():
        result.add("dev_journal_exists", True, f"Dev-journal found: {dj_path}")
    elif dj_path:
        result.add(
            "dev_journal_exists",
            False,
            f"Dev-journal path recorded but file not on disk: {dj_path}",
        )
    else:
        result.add(
            "dev_journal_exists",
            False,
            "No dev-journal path found in closure_checks or evidence",
        )


def _check_story_status_done(root, story_id, stage, yaml_data, stage_data, result):
    story_path = _find_story(root, story_id)
    if not story_path:
        result.add("story_status_done", False, "Story file not found")
        return
    fm = _parse_story_frontmatter(story_path)
    status = fm.get("status", "")
    if status == "Done":
        result.add("story_status_done", True, "Story status is Done")
    else:
        result.add(
            "story_status_done", False, f"Story status is {status!r}, expected 'Done'"
        )


_CHECK_DISPATCH = {
    "branch_exists": _check_branch_exists,
    "yaml_exists": _check_yaml_exists,
    "story_in_progress": _check_story_in_progress,
    "artifact_s1_exists": _check_artifact_s1_exists,
    "artifact_s2_exists": _check_artifact_s2_exists,
    "story_changed": _check_story_changed,
    "evidence_non_empty": _check_evidence_non_empty,
    "evidence_has_pass_fail": _check_evidence_has_pass_fail,
    "has_commits_since_s2": _check_has_commits_since_s2,
    "quality_gates_pass": _check_quality_gates_pass,
    "dev_journal_exists": _check_dev_journal_exists,
    "story_status_done": _check_story_status_done,
}


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main():
    args = sys.argv[1:]
    if not args:
        print(
            json.dumps({"error": "No action specified. Use: verify | status | audit"})
        )
        sys.exit(2)

    action = args[0]

    # Resolve project root
    root_flag = "--root" in args
    if root_flag:
        idx = args.index("--root")
        root = Path(args[idx + 1])
    else:
        root = (
            Path(__file__).resolve().parent.parent.parent
        )  # .opencode/tools -> .opencode -> project root
    _bind_docs_root(root)

    if action == "audit":
        output = audit_all(root)
        print(json.dumps(output, indent=2))
        sys.exit(0 if output.get("passed") else 1)

    if action in ("verify", "status"):
        if len(args) < 2:
            print(
                json.dumps(
                    {"error": f"Usage: {action} <story_id> [stage] [--root DIR]"}
                )
            )
            sys.exit(2)

        story_id = args[1]
        stage = args[2] if len(args) > 2 and not args[2].startswith("--") else None

        if action == "verify":
            if not stage:
                print(
                    json.dumps(
                        {"error": "verify requires a stage argument (e.g. S8_CAPTURE)"}
                    )
                )
                sys.exit(2)
            result = verify_stage(root, story_id, stage)
        else:
            result = show_status(root, story_id)

        print(json.dumps(result.to_json(), indent=2))
        sys.exit(0 if result.passed else 1)

    print(
        json.dumps(
            {"error": f"Unknown action: {action!r}. Use: verify | status | audit"}
        )
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
