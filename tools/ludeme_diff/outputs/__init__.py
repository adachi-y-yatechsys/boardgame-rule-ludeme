"""Output helpers for diff verification."""

from .summary import build_result_payload, render_table_summary
from .slack import build_slack_payload
from .archive import (
    ArchiveRecord,
    ArchiveMetadata,
    prepare_archive,
    load_archive_metadata,
    list_archives,
    find_archive_by_run_id,
)

__all__ = [
    "build_result_payload",
    "render_table_summary",
    "build_slack_payload",
    "ArchiveRecord",
    "ArchiveMetadata",
    "prepare_archive",
    "load_archive_metadata",
    "list_archives",
    "find_archive_by_run_id",
]
