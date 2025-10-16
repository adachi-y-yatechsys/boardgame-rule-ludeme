"""Archive helpers for diff verification outputs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class ArchiveMetadata:
    """Snapshot of the metadata stored for a verification archive."""

    run_id: str
    branch: str | None
    status: str | None
    timestamp: str
    path: Path
    label: str | None
    artifact_path: str
    files: Mapping[str, str]
    inputs: Mapping[str, str]

    def as_dict(self, *, relative_to: Path | None = None) -> dict[str, Any]:
        """Serialise the metadata into a JSON friendly dictionary."""

        base_path = (
            relative_to.resolve()
            if relative_to is not None
            else self.path.parent.resolve()
        )
        archive_path = self.path.resolve()
        artifact_path = Path(self.artifact_path)
        if not artifact_path.is_absolute():
            artifact_display = str(artifact_path)
        else:
            try:
                artifact_display = str(artifact_path.relative_to(base_path))
            except ValueError:
                artifact_display = str(artifact_path)
        try:
            relative_path = str(archive_path.relative_to(base_path))
        except ValueError:
            relative_path = str(archive_path)

        return {
            "run_id": self.run_id,
            "branch": self.branch,
            "status": self.status,
            "timestamp": self.timestamp,
            "path": relative_path,
            "label": self.label,
            "artifact_path": artifact_display,
            "files": dict(self.files),
            "inputs": dict(self.inputs),
        }


@dataclass
class ArchiveRecord:
    """Metadata describing a stored diff verification archive."""

    path: Path
    timestamp: str
    label: str | None
    run_id: str | None = None
    branch: str | None = None

    def write(
        self,
        payload: Mapping[str, Any],
        slack_payload: Mapping[str, Any],
        inputs: Mapping[str, str] | None = None,
        *,
        status: str | None = None,
        branch: str | None = None,
        run_id: str | None = None,
        artifact_path: str | None = None,
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

        resolved_run_id = run_id or self.run_id or self.path.name
        resolved_branch = branch or self.branch
        resolved_status = status or payload.get("conclusion")
        metadata = {
            "created_at": self.timestamp,
            "label": self.label,
            "run_id": resolved_run_id,
            "branch": resolved_branch,
            "status": resolved_status,
            "status_counts": payload.get("status_counts"),
            "conclusion": payload.get("conclusion"),
            "inputs": dict(inputs or {}),
            "artifact_path": artifact_path or str(self.path),
            "files": {
                "diff_verify_results": "diff_verify_results.json",
                "slack_payload": "slack_payload.json",
            },
        }

        (self.path / "metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def prepare_archive(
    archive_dir: Path,
    *,
    label: str | None = None,
    run_id: str | None = None,
    branch: str | None = None,
) -> ArchiveRecord:
    """Prepare an archive directory for the current run."""

    sanitized_label = _sanitize_label(label)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    archive_name = timestamp if not sanitized_label else f"{timestamp}-{sanitized_label}"
    archive_path = archive_dir / archive_name
    archive_path.mkdir(parents=True, exist_ok=False)
    return ArchiveRecord(
        path=archive_path,
        timestamp=timestamp,
        label=sanitized_label or None,
        run_id=run_id,
        branch=branch,
    )


def load_archive_metadata(archive_path: Path) -> ArchiveMetadata:
    """Load a single archive metadata file."""

    metadata_path = archive_path / "metadata.json"
    if not metadata_path.exists():
        raise FileNotFoundError(f"metadata.json missing for archive: {archive_path}")

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    run_id = metadata.get("run_id") or archive_path.name
    branch = metadata.get("branch")
    status = metadata.get("status") or metadata.get("conclusion")
    timestamp = metadata.get("created_at") or metadata.get("timestamp") or ""
    artifact_path = metadata.get("artifact_path") or str(archive_path)
    files = metadata.get("files") or {}
    inputs = metadata.get("inputs") or {}

    return ArchiveMetadata(
        run_id=run_id,
        branch=branch,
        status=status,
        timestamp=timestamp,
        path=archive_path,
        label=metadata.get("label"),
        artifact_path=artifact_path,
        files=files,
        inputs=inputs,
    )


def list_archives(archive_dir: Path, *, latest: int | None = None) -> list[ArchiveMetadata]:
    """Enumerate stored archives sorted by timestamp (descending)."""

    if not archive_dir.exists():
        return []

    metadata_entries: list[ArchiveMetadata] = []
    for path in sorted(archive_dir.iterdir()):
        if not path.is_dir():
            continue
        metadata_path = path / "metadata.json"
        if not metadata_path.exists():
            continue
        try:
            metadata_entries.append(load_archive_metadata(path))
        except (OSError, json.JSONDecodeError):
            continue

    metadata_entries.sort(key=lambda item: item.timestamp, reverse=True)
    if latest is not None and latest >= 0:
        return metadata_entries[:latest]
    return metadata_entries


def find_archive_by_run_id(archive_dir: Path, run_id: str) -> ArchiveMetadata:
    """Locate an archive by run identifier or directory name."""

    for metadata in list_archives(archive_dir):
        if metadata.run_id == run_id or metadata.path.name == run_id:
            return metadata
    raise FileNotFoundError(f"Archive with run-id '{run_id}' not found in {archive_dir}")


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


__all__ = [
    "ArchiveRecord",
    "ArchiveMetadata",
    "prepare_archive",
    "load_archive_metadata",
    "list_archives",
    "find_archive_by_run_id",
]
