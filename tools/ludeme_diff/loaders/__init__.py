"""Data loading helpers for diff verification."""

from .diff_report import load_diff_report, DiffEntry
from .glossary import load_glossary, GlossaryTerm
from .matrix import load_mapping_matrix, MappingRow, MappingIndex

__all__ = [
    "load_diff_report",
    "DiffEntry",
    "load_glossary",
    "GlossaryTerm",
    "load_mapping_matrix",
    "MappingRow",
    "MappingIndex",
]
