"""Glossary difference tolerance rules (P4-BL-05)."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

_PUNCTUATION_PATTERN = re.compile(r"[\s、。,.、，．・・]+")
_LUDEME_TAG_PATTERN = re.compile(r"[（(]Ludeme:[^)）]+[)）]")


@dataclass(slots=True)
class ToleranceResult:
    """Represents the outcome of a tolerance comparison."""

    matches: bool
    tolerated: bool
    canonical_normalized: str
    candidate_normalized: str
    reason: str = ""

    @property
    def is_success(self) -> bool:
        return self.matches or self.tolerated


def _normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text or "")
    normalized = _LUDEME_TAG_PATTERN.sub("", normalized)
    normalized = normalized.strip()
    return normalized


def compare_with_tolerance(candidate: str, canonical: str) -> ToleranceResult:
    """Compare two strings allowing punctuation-only drift."""

    candidate_norm = _normalize(candidate)
    canonical_norm = _normalize(canonical)

    if candidate_norm == canonical_norm:
        return ToleranceResult(
            matches=True,
            tolerated=False,
            canonical_normalized=canonical_norm,
            candidate_normalized=candidate_norm,
        )

    candidate_reduced = _PUNCTUATION_PATTERN.sub("", candidate_norm)
    canonical_reduced = _PUNCTUATION_PATTERN.sub("", canonical_norm)
    if candidate_reduced == canonical_reduced:
        return ToleranceResult(
            matches=False,
            tolerated=True,
            canonical_normalized=canonical_norm,
            candidate_normalized=candidate_norm,
            reason="Punctuation-only differences",
        )

    return ToleranceResult(
        matches=False,
        tolerated=False,
        canonical_normalized=canonical_norm,
        candidate_normalized=candidate_norm,
        reason="Text differs beyond tolerance",
    )
