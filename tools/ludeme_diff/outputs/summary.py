"""Summary payload builder for CLI outputs."""

from __future__ import annotations

from typing import Dict

from ..rules import Finding, VerificationResult


def build_result_payload(result: VerificationResult) -> Dict:
    """Convert a :class:`VerificationResult` into a JSON-serialisable dict."""

    return {
        "status_counts": result.status_counts,
        "summary": _build_summary_text(result),
        "conclusion": result.conclusion,
        "findings": [
            {
                "entry_id": finding.entry_id,
                "field": finding.field,
                "severity": finding.severity,
                "message": finding.message,
                "action_required": finding.action_required,
                "term_key": finding.term_key,
                "tolerance": _serialize_tolerance(finding),
            }
            for finding in result.findings
        ],
        "glossary_actions": result.glossary_actions,
        "checks_payload": {
            "conclusion": "failure" if result.has_failures() else "success",
            "annotations": [
                {
                    "path": f"reports/ludeme/diff_report.json",
                    "annotation_level": _map_severity(finding.severity),
                    "message": finding.message,
                    "title": f"{finding.field} ({finding.entry_id})",
                    "start_line": 1,
                    "end_line": 1,
                }
                for finding in result.findings
            ],
        },
    }


def render_table_summary(result: VerificationResult) -> str:
    """Render a human readable table using plain text."""

    header = f"{'Entry ID':<15} | {'Field':<10} | {'Severity':<8} | Message"
    separator = "-" * len(header)
    rows = ["Ludeme diff verification summary", separator, header, separator]
    for finding in result.findings:
        rows.append(
            f"{finding.entry_id:<15} | {finding.field:<10} | {finding.severity:<8} | {finding.message}"
        )
    rows.append(separator)
    return "\n".join(rows)


def _build_summary_text(result: VerificationResult) -> str:
    failures = result.status_counts.get("failure", 0)
    warnings = result.status_counts.get("warning", 0)
    infos = result.status_counts.get("info", 0)
    conclusion = "failure" if failures else "success"
    return (
        "Phase 4 diff verification concluded with "
        f"{failures} failure(s), {warnings} warning(s), {infos} info entries. "
        f"Overall conclusion: {conclusion}."
    )


def _map_severity(severity: str) -> str:
    if severity == "failure":
        return "failure"
    if severity == "warning":
        return "warning"
    return "notice"


def _serialize_tolerance(finding: Finding) -> Dict | None:
    if not finding.tolerance:
        return None
    tolerance = finding.tolerance
    return {
        "matches": tolerance.matches,
        "tolerated": tolerance.tolerated,
        "canonical_normalized": tolerance.canonical_normalized,
        "candidate_normalized": tolerance.candidate_normalized,
        "reason": tolerance.reason,
    }
