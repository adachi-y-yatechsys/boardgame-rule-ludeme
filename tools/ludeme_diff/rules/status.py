"""Status aggregation logic (P4-BL-01/P4-BL-02)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Sequence

from ..loaders import DiffEntry, GlossaryTerm, MappingIndex
from .tolerance import ToleranceResult, compare_with_tolerance

_FAILING_REFERENCE_STATUSES = {"review", "pending", "n/a", "na", "missing"}
_LUDEME_PATTERN = re.compile(r"Ludeme:\s*(?P<term>[A-Za-z0-9_]+)")


@dataclass(slots=True)
class Finding:
    """Represents a single verification observation."""

    entry_id: str
    field: str
    severity: str
    message: str
    action_required: str | None = None
    term_key: str | None = None
    tolerance: ToleranceResult | None = None


@dataclass(slots=True)
class VerificationResult:
    """Aggregated verification results."""

    findings: List[Finding]
    glossary_actions: List[Dict[str, str]]
    status_counts: Dict[str, int]
    conclusion: str

    def has_failures(self) -> bool:
        return self.status_counts.get("failure", 0) > 0


def evaluate_entries(
    entries: Sequence[DiffEntry],
    glossary: Dict[str, GlossaryTerm],
    mapping: MappingIndex,
) -> VerificationResult:
    findings: List[Finding] = []
    glossary_actions: List[Dict[str, str]] = []
    counts: Dict[str, int] = {"failure": 0, "warning": 0, "info": 0}

    for entry in entries:
        severity = "info"
        action: str | None = None
        term_key: str | None = None
        tolerance: ToleranceResult | None = None
        message = ""

        if entry.field == "qa_text":
            term_key = _resolve_term_key(entry, mapping)
            if not term_key:
                severity = "failure"
                message = "Unable to resolve Ludeme term from diff entry"
                action = "update_mapping"
            else:
                glossary_term = glossary.get(term_key)
                if not glossary_term:
                    severity = "failure"
                    message = f"Glossary term '{term_key}' is not registered"
                    action = "register_glossary_term"
                else:
                    tolerance = compare_with_tolerance(entry.new_value, glossary_term.canonical_ja)
                    if tolerance.matches:
                        severity = "info"
                        message = "Translation matches glossary"
                    elif tolerance.tolerated:
                        severity = "warning"
                        message = "Translation differs only by punctuation"
                        action = "confirm_punctuation_diff"
                    else:
                        severity = "failure"
                        message = "Translation deviates from glossary"
                        action = "update_translation"
            if severity in {"failure", "warning"}:
                glossary_actions.append(
                    {
                        "entry_id": entry.entry_id,
                        "term_key": term_key or "",
                        "action_required": action or "review_entry",
                    }
                )

        elif entry.field in {"citation", "evidence"}:
            normalized_status = entry.status.strip().lower()
            if normalized_status in _FAILING_REFERENCE_STATUSES:
                severity = "failure"
                message = f"{entry.field} status '{entry.status}' requires follow-up"
                action = "update_reference_status"
            else:
                severity = "info"
                message = f"{entry.field} status '{entry.status}' accepted"

        else:
            severity = "info"
            message = "Field not targeted for phase 4 rules"

        counts[severity] = counts.get(severity, 0) + 1
        findings.append(
            Finding(
                entry_id=entry.entry_id,
                field=entry.field,
                severity=severity,
                message=message,
                action_required=action,
                term_key=term_key,
                tolerance=tolerance,
            )
        )

    conclusion = "failure" if counts.get("failure", 0) else "success"
    return VerificationResult(
        findings=findings,
        glossary_actions=glossary_actions,
        status_counts=counts,
        conclusion=conclusion,
    )


def _resolve_term_key(entry: DiffEntry, mapping: MappingIndex) -> str | None:
    if entry.entry_id in mapping:
        return mapping[entry.entry_id].ludeme_term

    match = _LUDEME_PATTERN.search(entry.new_value)
    if match:
        term = match.group("term")
        if term in mapping.by_term:
            return mapping.by_term[term].ludeme_term or term
        return term

    return None
