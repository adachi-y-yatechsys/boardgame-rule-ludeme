"""Glossary loader for diff verification."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable


@dataclass(slots=True)
class GlossaryTerm:
    term_key: str
    canonical_ja: str
    canonical_en: str
    notes: str


class GlossaryLoadError(RuntimeError):
    """Raised when the glossary CSV cannot be parsed."""


def load_glossary(path: str | Path) -> Dict[str, GlossaryTerm]:
    """Load glossary terms keyed by ``term_key``."""

    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Glossary CSV not found: {csv_path}")

    rows = _read_rows(csv_path)
    glossary: Dict[str, GlossaryTerm] = {}
    for raw in rows:
        term_key = (raw.get("term_key") or "").strip()
        canonical_ja = (raw.get("canonical_ja") or "").strip()
        if not term_key or not canonical_ja:
            raise GlossaryLoadError("Glossary row missing term_key or canonical_ja")
        glossary[term_key] = GlossaryTerm(
            term_key=term_key,
            canonical_ja=canonical_ja,
            canonical_en=(raw.get("canonical_en") or "").strip(),
            notes=(raw.get("notes") or "").strip(),
        )
    return glossary


def _read_rows(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader)
