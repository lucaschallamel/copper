#!/usr/bin/env python3
"""
User Story Validator for COPPER Projects

This comprehensive validator performs five phases of validation:
1. Story Type Format: File naming, story ID format, numbering conventions
2. YAML Frontmatter: Required fields, type-specific fields, enumeration values
3. Business Rules: Cross-field validation, conditional requirements, project compliance
4. Progress Block: Collapsible progress update callout structure and format
5. Body Sections: Acceptance criteria presence, deliverables
   resolution, title-AC alignment

Validates all 9 story types: EP, US, BUG, TD, SEC, SP, CI, RA, SC

Project: Generic COPPER documentation validation toolkit
Client: [TO BE CONFIGURED]

Exit Codes:
    0: All validations passed
    1: Validation errors found
    2: Script execution error

Usage:
    python3 user-story-validator.py <file_or_directory>
    python3 user-story-validator.py US-001-customer-search.md
    python3 user-story-validator.py ../roadmap/sprint-001/

Author: COPPER framework
Version: 2.2.0 (generic adaptation)
Language: British English (en-AU)
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def _load_story_statuses() -> frozenset[str]:
    """Load the canonical story-status set from the shared vocabulary (TD-171 AC3).

    One definition point for this validator AND pipeline_validator.py. The
    tools/ directory sits beside skills/ under the harness root in every layout
    (kits/core, .opencode, .claude), so the relative offset is invariant.
    Fail closed: a validator that cannot know the canon must not guess one.
    """
    vocab_path = (
        Path(__file__).resolve().parents[3] / "tools" / "status-vocabulary.json"
    )
    try:
        values = json.loads(vocab_path.read_text(encoding="utf-8"))["story_status"]
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print(
            f"FATAL: cannot load canonical status vocabulary at {vocab_path}: {exc}",
            file=sys.stderr,
        )
        sys.exit(2)
    if (
        not isinstance(values, list)
        or not values
        or not all(isinstance(v, str) for v in values)
    ):
        print(f"FATAL: malformed story_status list in {vocab_path}", file=sys.stderr)
        sys.exit(2)
    return frozenset(values)


# =============================================================================
# CONFIGURATION: Story Types & Patterns
# =============================================================================

VALID_STORY_TYPES = {
    "EP": "Epic",
    "US": "User Story",
    "BUG": "Bug/Defect",
    "TD": "Technical Debt",
    "SEC": "Security",
    "SP": "Spike",
    "CI": "Continuous Improvement",
    "RA": "Risk Action",
    "SC": "Scaffold",
}

STORY_ID_PATTERN = re.compile(r"^(EP|US|BUG|TD|SEC|SP|CI|RA|SC)-(\d{3,4}[a-z]?)$")
FILE_NAME_PATTERN = re.compile(
    r"^(EP|US|BUG|TD|SEC|SP|CI|RA|SC)-(\d{3,4}[a-z]?)-(.+)\.md$"
)
FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---", re.DOTALL | re.MULTILINE)
RETRO_ID_PATTERN = re.compile(r"^RETRO-\d{3,4}$")
RAID_ID_PATTERN = re.compile(r"^[RAID]-\d{3,4}$")
PROGRESS_ENTRY_PATTERN = re.compile(r"^> - \*\*\d{4}-\d{2}-\d{2}\*\*: .+")

# BUG-010: an acceptance/success criterion, in ANY of Rule 02c's eight Task Genius
# statuses. The rule previously matched `- [ ] **ACn**` only, so a story whose
# criteria were all `[x]` was reported as having NO checkboxes , the more complete
# the story, the more certainly it was flagged. Measured before the fix: 105
# warnings on this backlog, 103 of them on `Done` stories, and it reached every
# adopter because this script ships in kits/core.
#
# The eight characters are Rule 02's statuses, verified as a SET rather than by eye.
# `-` is escaped so the class is an ALLOWLIST of eight, not a range: `[.]`, `[0]`
# and `[;]` are rejected. `\d` needs no quantifier because `search()` is unanchored,
# so `**AC10**` matches on its first digit (AC10-AC14 exist in this backlog).
AC_CHECKBOX_PATTERN = re.compile(r"- \[[ x/\-><?!]\] \*\*(?:AC|SC)\d")

# Required base fields for ALL story types
BASE_REQUIRED_FIELDS = {
    "story_id": str,
    "story_type": str,
    "title": str,
    "priority": str,
    "story_points": int,
    "status": str,
    "created": str,
    "last_modified": str,
}

# Valid enumeration values
VALID_ENUMS = {
    "story_type": {
        "epic",
        "user_story",
        "bug",
        "technical_debt",
        "security",
        "spike",
        "continuous_improvement",
        "risk_action",
        "scaffold",
    },
    "priority": {"Critical", "High", "Medium", "Low"},
    # TD-171 AC3: loaded from tools/status-vocabulary.json , the previous inline
    # 18-value set admitted 'active'/'done'/'completed' into story frontmatter,
    # which is what made the pipeline audit drift (Group B) expressible.
    "status": _load_story_statuses(),
    "business_value": {"high", "medium", "low"},
    "severity": {"critical", "high", "medium", "low"},
    "environment": {"production", "staging", "test", "dev"},
    "compliance_framework": {
        "GDPR",
        "ISO27001",
        "OWASP",
        "Swiss_DPA",
        "NIST_CSF",
        "PCI_DSS",
        "project_specific",
    },
    "debt_category": {
        "code_quality",
        "architecture",
        "testing",
        "documentation",
        "security",
    },
    "debt_impact": {"productivity", "maintainability", "scalability", "security"},
    "improvement_category": {"process", "tools", "team", "quality"},
    "action_type": {"mitigation", "response", "contingency"},
}

# Type-specific required fields
TYPE_SPECIFIC_FIELDS = {
    "epic": {
        "epic_owner": str,
        "child_stories": list,
        "business_value": str,
        "strategic_theme": str,
    },
    "bug": {
        "severity": str,
        "affected_version": str,
        "reproduction_steps": str,
        "environment": str,
    },
    "security": {
        "cvss_score": float,
        "vulnerability_type": str,
        "compliance_framework": str,
        "remediation_deadline": str,
    },
    "spike": {
        "research_question": str,
        "time_box": str,
        "expected_outcome": str,
        "decision_deadline": str,
    },
    "technical_debt": {"debt_category": str, "debt_impact": str, "debt_age_days": int},
    "continuous_improvement": {
        "retrospective_id": str,
        "improvement_category": str,
        "source_sprint": int,
    },
    "risk_action": {"raid_id": str, "risk_score": int, "action_type": str},
    "scaffold": {},  # Flexible for Sprint 0 stories
}

STORY_TYPE_MAP = {
    "epic": "epic",
    "user_story": "user_story",
    "bug": "bug",
    "technical_debt": "technical_debt",
    "security": "security",
    "spike": "spike",
    "continuous_improvement": "continuous_improvement",
    "risk_action": "risk_action",
    "scaffold": "scaffold",
}

PROGRESS_BLOCK_REQUIRED_TYPES = {
    "epic",
    "user_story",
    "technical_debt",
    "continuous_improvement",
    "spike",
}


def _parse_inline_list(value: str) -> list[str]:
    """Parse simple inline YAML lists such as [US-101, US-102]."""
    inner = value[1:-1].strip()
    if not inner:
        return []
    return [item.strip().strip("\"'") for item in inner.split(",") if item.strip()]


# =============================================================================
# VALIDATION ERROR CLASS
# =============================================================================


class ValidationError:
    """Represents a validation error with context."""

    def __init__(
        self,
        file_path: Path,
        phase: str,
        error_type: str,
        message: str,
        severity: str = "ERROR",
    ):
        self.file_path = file_path
        self.phase = phase
        self.error_type = error_type
        self.message = message
        self.severity = severity

    def __str__(self) -> str:
        return (
            f"[{self.severity}] {self.file_path.name}: [{self.phase}] "
            f"{self.error_type} - {self.message}"
        )


# =============================================================================
# CONSOLIDATED USER STORY VALIDATOR
# =============================================================================


class UserStoryValidator:
    """Comprehensive user story validator with five validation phases."""

    def __init__(self):
        self.errors: list[ValidationError] = []
        self.warnings: list[ValidationError] = []
        self.files_checked = 0
        self.files_passed = 0

    # =========================================================================
    # PHASE 1: STORY TYPE FORMAT VALIDATION
    # =========================================================================

    def validate_format(self, file_path: Path) -> bool:
        """Phase 1: Validate story ID format and file naming conventions."""
        passed = True

        # Validate file name pattern
        if not FILE_NAME_PATTERN.match(file_path.name):
            self.errors.append(
                ValidationError(
                    file_path,
                    "FORMAT",
                    "INVALID_FILE_NAME",
                    "File name "
                    f"'{file_path.name}' does not match required pattern: "
                    "[TYPE]-[NNN or NNNN]-[description].md",
                )
            )
            passed = False
            return passed

        # Extract story ID from frontmatter
        story_id = self._extract_story_id(file_path)
        if not story_id:
            return False

        # Validate story ID format
        if not self._validate_story_id(story_id, file_path):
            passed = False

        return passed

    def _validate_story_id(self, story_id: str, file_path: Path) -> bool:
        """Validate story ID format and numbering."""
        if not story_id:
            self.errors.append(
                ValidationError(
                    file_path,
                    "FORMAT",
                    "MISSING_STORY_ID",
                    "Story ID is empty or missing",
                )
            )
            return False

        match = STORY_ID_PATTERN.match(story_id.strip())

        if not match:
            parts = story_id.split("-") if "-" in story_id else []
            if len(parts) == 2:
                story_type, number = parts
                if story_type not in VALID_STORY_TYPES:
                    valid_types = ", ".join(VALID_STORY_TYPES.keys())
                    self.errors.append(
                        ValidationError(
                            file_path,
                            "FORMAT",
                            "INVALID_TYPE",
                            f"Story type '{story_type}' not recognised. "
                            f"Valid types: {valid_types}",
                        )
                    )
                elif not number.isdigit() or len(number) not in (3, 4):
                    self.errors.append(
                        ValidationError(
                            file_path,
                            "FORMAT",
                            "INVALID_NUMBER",
                            f"Story number '{number}' must be 3 or 4 digits "
                            "(001-999 or 0001-9999)",
                        )
                    )
            else:
                self.errors.append(
                    ValidationError(
                        file_path,
                        "FORMAT",
                        "INVALID_FORMAT",
                        f"Story ID '{story_id}' has incorrect format. "
                        "Expected: [TYPE]-[NNN or NNNN]",
                    )
                )
            return False

        # Valid format - check special cases
        story_type = match.group(1)
        number_raw = match.group(2)
        # Strip optional alpha suffix for numeric checks
        number = re.sub(r"[a-z]$", "", number_raw, flags=re.IGNORECASE)

        # SC-000/SC-0000 is special exception (foundational meta-story)
        if int(number) == 0 and story_id not in ("SC-000", "SC-0000"):
            self.errors.append(
                ValidationError(
                    file_path,
                    "FORMAT",
                    "INVALID_NUMBER",
                    "Story number cannot be 000/0000. Use 001-999 or 0001-9999 "
                    "(except SC-000)",
                )
            )
            return False

        # Validate number range
        num_value = int(number)
        if num_value < 0 or num_value > 9999:
            self.errors.append(
                ValidationError(
                    file_path,
                    "FORMAT",
                    "NUMBER_OUT_OF_RANGE",
                    f"Story number '{number}' out of valid range: 001-999 or 0001-9999",
                )
            )
            return False

        return True

    def _extract_story_id(self, file_path: Path) -> str | None:
        """Extract story_id from YAML frontmatter."""
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            self.errors.append(
                ValidationError(
                    file_path,
                    "FORMAT",
                    "FILE_READ_ERROR",
                    f"Cannot read file: {str(e)}",
                )
            )
            return None

        frontmatter_match = FRONTMATTER_PATTERN.match(content)
        if not frontmatter_match:
            self.errors.append(
                ValidationError(
                    file_path,
                    "FORMAT",
                    "MISSING_FRONTMATTER",
                    "File missing YAML frontmatter "
                    "(should start with --- and end with ---)",
                )
            )
            return None

        frontmatter_text = frontmatter_match.group(1)
        story_id_match = re.search(
            r"^story_id:\s*(.+)$", frontmatter_text, re.MULTILINE
        )

        if not story_id_match:
            self.errors.append(
                ValidationError(
                    file_path,
                    "FORMAT",
                    "MISSING_STORY_ID",
                    "story_id field not found in YAML frontmatter",
                )
            )
            return None

        return story_id_match.group(1).strip().strip("\"'")

    # =========================================================================
    # PHASE 2: YAML FRONTMATTER VALIDATION
    # =========================================================================

    def validate_yaml(self, file_path: Path) -> bool:
        """Phase 2: Validate YAML frontmatter fields and types."""
        passed = True

        yaml_data = self._parse_yaml_frontmatter(file_path)
        if not yaml_data:
            return False

        # Validate base required fields
        for field_name, expected_type in BASE_REQUIRED_FIELDS.items():
            if field_name not in yaml_data:
                self.errors.append(
                    ValidationError(
                        file_path,
                        "YAML",
                        "MISSING_REQUIRED_FIELD",
                        f"Missing required base field: '{field_name}'",
                    )
                )
                passed = False

        # Validate enum values
        for field_name, value in yaml_data.items():
            if field_name in VALID_ENUMS:
                if isinstance(value, str) and value not in VALID_ENUMS[field_name]:
                    allowed = ", ".join(sorted(VALID_ENUMS[field_name]))
                    self.errors.append(
                        ValidationError(
                            file_path,
                            "YAML",
                            "INVALID_ENUM_VALUE",
                            f"Field '{field_name}' has invalid value '{value}'. "
                            f"Allowed: {allowed}",
                        )
                    )
                    passed = False

        # Validate type-specific fields
        story_type = yaml_data.get("story_type")
        if story_type and story_type in STORY_TYPE_MAP:
            type_key = STORY_TYPE_MAP[story_type]
            if type_key in TYPE_SPECIFIC_FIELDS:
                required_fields = TYPE_SPECIFIC_FIELDS[type_key]
                for field_name, expected_type in required_fields.items():
                    if field_name not in yaml_data:
                        self.errors.append(
                            ValidationError(
                                file_path,
                                "YAML",
                                "MISSING_TYPE_SPECIFIC_FIELD",
                                f"Missing required {story_type} field: '{field_name}'",
                            )
                        )
                        passed = False
                    elif expected_type is list and not isinstance(
                        yaml_data.get(field_name), list
                    ):
                        self.errors.append(
                            ValidationError(
                                file_path,
                                "YAML",
                                "INVALID_FIELD_TYPE",
                                f"Field '{field_name}' should be an array/list",
                            )
                        )
                        passed = False

        return passed

    def _parse_yaml_frontmatter(self, file_path: Path) -> dict[str, Any] | None:
        """Parse YAML frontmatter from markdown file."""
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            return None

        frontmatter_match = FRONTMATTER_PATTERN.match(content)
        if not frontmatter_match:
            return None

        frontmatter_text = frontmatter_match.group(1)
        yaml_data = {}
        current_key = None
        array_mode = False
        array_items = []

        for line in frontmatter_text.split("\n"):
            line = line.rstrip()

            if line.strip().startswith("#") or not line.strip():
                continue

            # Array items
            if line.strip().startswith("- "):
                if array_mode:
                    item = line.strip()[2:].strip().strip("\"'")
                    array_items.append(item)
                continue

            # Key-value pairs
            if ":" in line and not line.startswith(" "):
                if array_mode and current_key:
                    yaml_data[current_key] = array_items
                    array_mode = False
                    array_items = []

                parts = line.split(":", 1)
                key = parts[0].strip()
                value = parts[1].strip() if len(parts) > 1 else ""

                current_key = key

                if not value:
                    array_mode = True
                else:
                    value = value.strip("\"'")
                    if value.startswith("[") and value.endswith("]"):
                        yaml_data[key] = _parse_inline_list(value)
                    elif value.lower() in ("true", "false"):
                        yaml_data[key] = value.lower() == "true"
                    elif value.replace(".", "", 1).isdigit():
                        yaml_data[key] = float(value) if "." in value else int(value)
                    else:
                        yaml_data[key] = value

        if array_mode and current_key:
            yaml_data[current_key] = array_items

        return yaml_data

    # =========================================================================
    # PHASE 3: BUSINESS RULES VALIDATION
    # =========================================================================

    def validate_business_rules(self, file_path: Path) -> bool:
        """Phase 3: Validate business rules and cross-field requirements."""
        passed = True

        yaml_data = self._parse_yaml_frontmatter(file_path)
        if not yaml_data:
            return False

        story_type = yaml_data.get("story_type")

        # BUG rules
        if story_type == "bug":
            if not self._validate_bug_rules(yaml_data, file_path):
                passed = False

        # SEC rules
        elif story_type == "security":
            if not self._validate_security_rules(yaml_data, file_path):
                passed = False

        # TD rules
        elif story_type == "technical_debt":
            if not self._validate_technical_debt_rules(yaml_data, file_path):
                passed = False

        # CI rules
        elif story_type == "continuous_improvement":
            if not self._validate_ci_rules(yaml_data, file_path):
                passed = False

        # RA rules
        elif story_type == "risk_action":
            if not self._validate_risk_action_rules(yaml_data, file_path):
                passed = False

        return passed

    def validate_progress_block(self, file_path: Path) -> bool:
        """Validate the required collapsible progress block.

        Applies only to supported story types.
        """
        passed = True

        yaml_data = self._parse_yaml_frontmatter(file_path)
        if not yaml_data:
            return False

        story_type = yaml_data.get("story_type")
        if story_type not in PROGRESS_BLOCK_REQUIRED_TYPES:
            return True

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            self.errors.append(
                ValidationError(
                    file_path,
                    "DOCUMENTATION",
                    "FILE_READ_ERROR",
                    f"Cannot read file for progress block validation: {str(e)}",
                )
            )
            return False

        frontmatter_match = FRONTMATTER_PATTERN.match(content)
        if not frontmatter_match:
            return False

        body = content[frontmatter_match.end() :]
        lines = body.splitlines()

        while lines and not lines[0].strip():
            lines.pop(0)

        if not lines or lines[0].strip() != "> [!note]- Progress updates":
            self.errors.append(
                ValidationError(
                    file_path,
                    "DOCUMENTATION",
                    "MISSING_PROGRESS_BLOCK",
                    (
                        "Supported backlog artefacts must start with a collapsible "
                        "'> [!note]- Progress updates' block immediately after "
                        "frontmatter"
                    ),
                )
            )
            return False

        if len(lines) < 3 or lines[1].strip() != ">":
            self.errors.append(
                ValidationError(
                    file_path,
                    "DOCUMENTATION",
                    "INVALID_PROGRESS_BLOCK_STRUCTURE",
                    (
                        "Progress block must contain a blank quoted separator line "
                        "after the header"
                    ),
                )
            )
            return False

        if not PROGRESS_ENTRY_PATTERN.match(lines[2]):
            self.errors.append(
                ValidationError(
                    file_path,
                    "DOCUMENTATION",
                    "INVALID_PROGRESS_ENTRY",
                    (
                        "Progress block must include a bullet entry in the format "
                        "'> - **YYYY-MM-DD**: ...'"
                    ),
                )
            )
            return False

        return passed

    def _validate_bug_rules(self, yaml_data: dict[str, Any], file_path: Path) -> bool:
        """Validate BUG story business rules."""
        passed = True
        severity = yaml_data.get("severity", "")
        reproduction_steps = yaml_data.get("reproduction_steps", "")

        if severity == "critical" and not reproduction_steps:
            self.errors.append(
                ValidationError(
                    file_path,
                    "BUSINESS_RULES",
                    "MISSING_REPRODUCTION_STEPS",
                    "Critical severity bugs MUST have detailed reproduction_steps "
                    "field",
                )
            )
            passed = False

        return passed

    def _validate_security_rules(
        self, yaml_data: dict[str, Any], file_path: Path
    ) -> bool:
        """Validate SEC story business rules against a generic remediation SLA."""
        passed = True
        cvss_score = yaml_data.get("cvss_score", 0.0)
        remediation_deadline = yaml_data.get("remediation_deadline", "")
        created = yaml_data.get("created", "")

        # High CVSS (>=7.0) requires prompt remediation per framework defaults
        if cvss_score >= 7.0 and remediation_deadline and created:
            try:
                created_date = datetime.strptime(created, "%Y-%m-%d")
                deadline_date = datetime.strptime(remediation_deadline, "%Y-%m-%d")
                days_diff = (deadline_date - created_date).days

                # Framework default: high-severity vulnerabilities should be
                # addressed within 7 days.
                if days_diff > 7:
                    self.errors.append(
                        ValidationError(
                            file_path,
                            "BUSINESS_RULES",
                            "REMEDIATION_DEADLINE_TOO_LATE",
                            "High CVSS vulnerability "
                            f"(score: {cvss_score}) remediation deadline is "
                            f"{days_diff} days after creation. Should be within "
                            "7 days unless a documented exception exists.",
                        )
                    )
                    passed = False
            except ValueError:
                pass  # Date parsing errors handled elsewhere

        return passed

    def _validate_technical_debt_rules(
        self, yaml_data: dict[str, Any], file_path: Path
    ) -> bool:
        """Validate TD story business rules."""
        passed = True
        debt_age_days = yaml_data.get("debt_age_days", 0)
        created = yaml_data.get("created", "")

        if debt_age_days and created:
            try:
                created_date = datetime.strptime(created, "%Y-%m-%d")
                today = datetime.now()
                actual_age = (today - created_date).days

                # Allow 5-day tolerance for manual updates
                if abs(actual_age - debt_age_days) > 5:
                    self.warnings.append(
                        ValidationError(
                            file_path,
                            "BUSINESS_RULES",
                            "DEBT_AGE_MISMATCH",
                            f"debt_age_days ({debt_age_days}) does not match "
                            f"calculated age ({actual_age} days from created "
                            "date). Consider updating",
                            "WARNING",
                        )
                    )
            except ValueError:
                pass

        return passed

    def _validate_ci_rules(self, yaml_data: dict[str, Any], file_path: Path) -> bool:
        """Validate CI story business rules."""
        passed = True
        retrospective_id = yaml_data.get("retrospective_id", "")

        if retrospective_id and not RETRO_ID_PATTERN.match(retrospective_id):
            self.errors.append(
                ValidationError(
                    file_path,
                    "BUSINESS_RULES",
                    "INVALID_RETROSPECTIVE_ID",
                    f"retrospective_id '{retrospective_id}' does not match "
                    "required format: RETRO-NNN or RETRO-NNNN "
                    "(e.g., RETRO-023 or RETRO-0023)",
                )
            )
            passed = False

        return passed

    def _validate_risk_action_rules(
        self, yaml_data: dict[str, Any], file_path: Path
    ) -> bool:
        """Validate RA story business rules."""
        passed = True
        raid_id = yaml_data.get("raid_id", "")

        if raid_id and not RAID_ID_PATTERN.match(raid_id):
            self.errors.append(
                ValidationError(
                    file_path,
                    "BUSINESS_RULES",
                    "INVALID_RAID_ID",
                    f"raid_id '{raid_id}' does not match required format: "
                    "[RAID]-NNN or [RAID]-NNNN (e.g., R-042, A-0015)",
                )
            )
            passed = False

        return passed

    def validate_body_sections(self, file_path: Path) -> bool:
        """Phase 5: Validate body-level structural sections."""
        content = file_path.read_text(encoding="utf-8")
        passed = True

        yaml_data = self._parse_yaml_frontmatter(file_path)
        story_type = yaml_data.get("story_type", "") if yaml_data else ""

        if story_type not in ("user_story", "spike"):
            return True

        # Check for Acceptance Criteria section
        if (
            "## Acceptance Criteria" not in content
            and "## Success Criteria" not in content
        ):
            self.warnings.append(
                ValidationError(
                    file_path,
                    "BODY_SECTIONS",
                    "MISSING_AC_SECTION",
                    f"{story_type} stories should have a '## Acceptance Criteria' or "
                    "'## Success Criteria' section",
                    "WARNING",
                )
            )
            passed = False
        else:
            import re

            ac_match = re.search(
                r"## (?:Acceptance|Success) Criteria.*?(?=\n## |\Z)",
                content,
                re.DOTALL,
            )
            if ac_match:
                ac_text = ac_match.group(0)
                if not AC_CHECKBOX_PATTERN.search(ac_text):
                    self.warnings.append(
                        ValidationError(
                            file_path,
                            "BODY_SECTIONS",
                            "NO_AC_CHECKBOXES",
                            "Acceptance Criteria section exists but contains no "
                            "Task Genius **ACn**/**SCn** checkboxes",
                            "WARNING",
                        )
                    )

        # Check for unresolved Deliverables or Follow-on Work checkboxes
        import re

        for section_pattern, section_name in [
            (r"## Deliverables.*?(?=\n## |\Z)", "Deliverables"),
            (r"### Follow-on Work.*?(?=\n## |\n### |\Z)", "Follow-on Work"),
        ]:
            match = re.search(section_pattern, content, re.DOTALL)
            if match:
                section_text = match.group(0)
                unchecked = re.findall(r"- \[ \] .+", section_text)
                if unchecked:
                    tag = section_name.upper().replace("-", "_").replace(" ", "_")
                    self.warnings.append(
                        ValidationError(
                            file_path,
                            "BODY_SECTIONS",
                            f"UNRESOLVED_{tag}",
                            f"'{section_name}' section has "
                            f"{len(unchecked)} unchecked "
                            f"item(s) — resolve before closing",
                            "WARNING",
                        )
                    )

        return passed

    # =========================================================================
    # FILE PROCESSING
    # =========================================================================

    def validate_file(self, file_path: Path) -> bool:
        """Validate a single user story file through all three phases."""
        if not file_path.suffix == ".md":
            return True  # Skip non-markdown files

        if file_path.name in ["README.md", "CHANGELOG.md", "DEPENDENCIES.md"]:
            return True  # Skip documentation + generated aggregate files

        self.files_checked += 1
        file_passed = True

        # Phase 1: Format validation
        if not self.validate_format(file_path):
            file_passed = False

        # Phase 2: YAML validation
        if not self.validate_yaml(file_path):
            file_passed = False

        # Phase 3: Business rules validation
        if not self.validate_business_rules(file_path):
            file_passed = False

        # Phase 4: Progress block documentation validation
        if not self.validate_progress_block(file_path):
            file_passed = False

        # Phase 5: Body sections structural validation
        if not self.validate_body_sections(file_path):
            file_passed = False

        if file_passed:
            self.files_passed += 1

        return file_passed

    def validate_directory(self, directory: Path) -> None:
        """Validate all user story files in a directory."""
        if not directory.is_dir():
            print(f"Error: {directory} is not a directory")
            sys.exit(2)

        for md_file in sorted(directory.glob("*.md")):
            self.validate_file(md_file)
        if not self.files_checked:
            # Nothing checked is not a pass (TD-201); README.md and the other
            # skipped files do not count (S4).
            print(f"Error: no story files found in {directory}")
            sys.exit(2)

    def print_report(self) -> None:
        """Print comprehensive validation report."""
        print()
        print("=" * 80)
        print("User Story Validation Report (Consolidated)")
        print("=" * 80)
        print()
        print(f"Files checked: {self.files_checked}")
        print(f"Files passed:  {self.files_passed}")
        print(f"Files failed:  {self.files_checked - self.files_passed}")
        print()

        if self.errors:
            print(f"{len(self.errors)} Error(s) Found:")
            print("-" * 80)
            for error in self.errors:
                print(f"  {error}")
            print()

        if self.warnings:
            print(f"{len(self.warnings)} Warning(s):")
            print("-" * 80)
            for warning in self.warnings:
                print(f"  {warning}")
            print()

        if not self.errors and not self.warnings:
            print("✓ All validations passed successfully!")
            print()

        print("=" * 80)

    def get_exit_code(self) -> int:
        """Return appropriate exit code."""
        return 1 if self.errors else 0


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================


def main():
    """Main entry point for user story validation."""
    if len(sys.argv) < 2:
        print("Usage: python3 validation-user-story.py <file_or_directory>")
        print()
        print("Examples:")
        print("  python3 validation-user-story.py US-001-user-search.md")
        print("  python3 validation-user-story.py ../roadmap/sprint-001/")
        print("  python3 validation-user-story.py ../roadmap/sample-stories/")
        sys.exit(2)

    target_path = Path(sys.argv[1])

    if not target_path.exists():
        print(f"Error: {target_path} does not exist")
        sys.exit(2)

    validator = UserStoryValidator()

    try:
        if target_path.is_file():
            validator.validate_file(target_path)
        else:
            validator.validate_directory(target_path)

        validator.print_report()
        sys.exit(validator.get_exit_code())

    except Exception as e:
        print(f"Fatal error during validation: {str(e)}")
        import traceback

        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
