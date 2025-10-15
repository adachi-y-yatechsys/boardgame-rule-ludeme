"""Diff report loader utilities."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass(slots=True)
class DiffEntry:
    """Normalized diff report row."""

    series: str
    edition: str
    entry_id: str
    field: str
    change_type: str
    previous_value: str
    new_value: str
    status: str
    notes: str


class DiffReportFormatError(RuntimeError):
    """Raised when the diff report payload is malformed."""


_SUPPORTED_SUFFIXES = {".json", ".csv"}


def load_diff_report(path: str | Path) -> List[DiffEntry]:
    """Load diff entries from JSON or CSV files.

    Args:
        path: Path to the diff report.

    Returns:
        A list of validated :class:`DiffEntry` objects.
    """

    report_path = Path(path)
    if not report_path.exists():
        raise FileNotFoundError(f"Diff report not found: {report_path}")

    if report_path.suffix.lower() not in _SUPPORTED_SUFFIXES:
        raise DiffReportFormatError(
            f"Unsupported diff report format: {report_path.suffix}. "
            "Expected one of .json, .csv"
        )

    if report_path.suffix.lower() == ".json":
        raw_entries = _load_json(report_path)
    else:
        raw_entries = _load_csv(report_path)

    entries: List[DiffEntry] = []
    for payload in raw_entries:
        entries.append(_normalise_entry(payload))
    return entries


def _load_json(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, list):
        raise DiffReportFormatError("Diff report JSON must be a list of entries")
    return payload


def _load_csv(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


_REQUIRED_FIELDS = {"series", "edition", "entry_id", "field", "change_type", "status"}


def _normalise_entry(raw: dict) -> DiffEntry:
    missing = _REQUIRED_FIELDS.difference(raw)
    if missing:
        raise DiffReportFormatError(f"Diff report entry missing required fields: {sorted(missing)}")

    def _get(key: str) -> str:
        value = raw.get(key, "")
        if value is None:
            return ""
        return str(value)

    return DiffEntry(
        series=_get("series"),
        edition=_get("edition"),
        entry_id=_get("entry_id"),
        field=_get("field"),
        change_type=_get("change_type"),
        previous_value=_get("previous_value"),
        new_value=_get("new_value"),
        status=_get("status"),
        notes=_get("notes"),
    )
