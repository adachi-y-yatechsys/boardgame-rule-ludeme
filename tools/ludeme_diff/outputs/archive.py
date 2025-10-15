"""Archive helpers for diff verification outputs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Mapping, Any


@dataclass
class ArchiveRecord:
    """Metadata describing a stored diff verification archive."""

    path: Path
    timestamp: str
    label: str | None

    def write(
        self,
        payload: Mapping[str, Any],
        slack_payload: Mapping[str, Any],
        inputs: Mapping[str, str] | None = None,
    ) -> None:
        """Persist payloads and metadata into the archive directory."""

        self.path.mkdir(parents=True, exist_ok=True)

        (self.path / "diff_verify_results.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        (self.path / "slack_payload.json").write_text(
            json.dumps(slack_payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        metadata = {
            "created_at": self.timestamp,
            "label": self.label,
            "status_counts": payload.get("status_counts"),
            "conclusion": payload.get("conclusion"),
            "inputs": dict(inputs or {}),
            "files": {
                "diff_verify_results": "diff_verify_results.json",
                "slack_payload": "slack_payload.json",
            },
        }

        (self.path / "metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def prepare_archive(archive_dir: Path, *, label: str | None = None) -> ArchiveRecord:
    """Prepare an archive directory for the current run."""

    sanitized_label = _sanitize_label(label)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    archive_name = timestamp if not sanitized_label else f"{timestamp}-{sanitized_label}"
    archive_path = archive_dir / archive_name
    archive_path.mkdir(parents=True, exist_ok=False)
    return ArchiveRecord(path=archive_path, timestamp=timestamp, label=sanitized_label or None)


def _sanitize_label(label: str | None) -> str:
    if not label:
        return ""
    normalized = label.strip().lower().replace(" ", "-")
    safe_chars = [c if c.isalnum() or c in {"-", "_"} else "-" for c in normalized]
    collapsed = "".join(safe_chars)
    # Remove duplicate separators
    while "--" in collapsed:
        collapsed = collapsed.replace("--", "-")
    return collapsed.strip("-_")


__all__ = ["ArchiveRecord", "prepare_archive"]
