"""Output helpers for diff verification."""

from .summary import build_result_payload, render_table_summary
from .slack import build_slack_payload
from .archive import prepare_archive, ArchiveRecord

__all__ = [
    "build_result_payload",
    "render_table_summary",
    "build_slack_payload",
    "prepare_archive",
    "ArchiveRecord",
]
