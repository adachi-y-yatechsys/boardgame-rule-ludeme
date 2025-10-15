"""Mapping matrix loader."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List


@dataclass(slots=True)
class MappingRow:
    model_id: str
    fact_tag: str
    current_text: str
    ludeme_category: str
    ludeme_term: str
    mapping_type: str
    evidence_source_id: str
    page: str
    notes: str
    entry_id: str | None = None


class MappingIndex(Dict[str, MappingRow]):
    """Helper dictionary mapping entry IDs to mapping rows."""

    by_term: Dict[str, MappingRow]

    def __init__(self) -> None:  # pragma: no cover - thin wrapper
        super().__init__()
        self.by_term = {}

    def add(self, row: MappingRow) -> None:
        if row.entry_id:
            self[row.entry_id] = row
        if row.ludeme_term:
            self.by_term[row.ludeme_term] = row


def load_mapping_matrix(path: str | Path) -> MappingIndex:
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Mapping matrix not found: {csv_path}")

    rows = _read_rows(csv_path)
    index = MappingIndex()
    for raw in rows:
        row = MappingRow(
            model_id=raw.get("model_id", ""),
            fact_tag=raw.get("fact_tag", ""),
            current_text=raw.get("current_text", ""),
            ludeme_category=raw.get("proposed_ludeme.category", ""),
            ludeme_term=raw.get("proposed_ludeme.term", ""),
            mapping_type=raw.get("mapping_type", ""),
            evidence_source_id=raw.get("evidence_source_id", ""),
            page=raw.get("page", ""),
            notes=raw.get("notes", ""),
            entry_id=raw.get("entry_id") or None,
        )
        index.add(row)
    return index


def _read_rows(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader)
