"""Command line interface for Ludeme diff verification."""

from __future__ import annotations

import json
from pathlib import Path
import os

import click

from .loaders import (
    load_diff_report,
    load_glossary,
    load_mapping_matrix,
)
from .outputs import (
    ArchiveRecord,
    build_result_payload,
    build_slack_payload,
    find_archive_by_run_id,
    list_archives,
    prepare_archive,
    render_table_summary,
)
from .rules import evaluate_entries


@click.group()
def main() -> None:
    """Ludeme diff verification CLI entry point."""


@main.command()
@click.option("--report", "report_path", type=click.Path(path_type=Path), required=True)
@click.option("--matrix", "matrix_path", type=click.Path(path_type=Path), required=True)
@click.option("--glossary", "glossary_path", type=click.Path(path_type=Path), required=True)
@click.option("--output", "output_path", type=click.Path(path_type=Path), required=True)
@click.option(
    "--slack-payload",
    "slack_payload_path",
    type=click.Path(path_type=Path),
    default=Path("reports/ludeme/slack_payload.json"),
    show_default=True,
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "table"], case_sensitive=False),
    default="json",
)
@click.option(
    "--archive-dir",
    "archive_dir",
    type=click.Path(path_type=Path),
    default=None,
    help="Directory to store timestamped archives of verification outputs.",
)
@click.option(
    "--archive-label",
    "archive_label",
    type=str,
    default=None,
    help="Optional label appended to the archive directory name.",
)
@click.option(
    "--run-id",
    "run_id",
    type=str,
    default=None,
    help="Identifier of the CI run or execution triggering the archive.",
)
@click.option(
    "--branch",
    "branch_name",
    type=str,
    default=None,
    help="Source branch associated with the verification run.",
)
def verify(
    report_path: Path,
    matrix_path: Path,
    glossary_path: Path,
    output_path: Path,
    slack_payload_path: Path,
    output_format: str,
    archive_dir: Path | None,
    archive_label: str | None,
    run_id: str | None,
    branch_name: str | None,
) -> None:
    """Verify diff report entries against glossary and tolerance rules."""

    entries = load_diff_report(report_path)
    mapping = load_mapping_matrix(matrix_path)
    glossary = load_glossary(glossary_path)

    result = evaluate_entries(entries, glossary, mapping)
    payload = build_result_payload(result)
    slack_payload = build_slack_payload(result)
    archive: ArchiveRecord | None = None

    archive_run_url: str | None = None
    if run_id:
        repo = os.environ.get("GITHUB_REPOSITORY")
        server = os.environ.get("GITHUB_SERVER_URL", "https://github.com").rstrip("/")
        if repo:
            archive_run_url = f"{server}/{repo}/actions/runs/{run_id}"

    if archive_dir is not None:
        archive = prepare_archive(
            archive_dir,
            label=archive_label,
            run_id=run_id,
            branch=branch_name,
        )
        payload["archive"] = {
            "path": str(archive.path),
            "name": archive.path.name,
            "timestamp": archive.timestamp,
            "label": archive.label,
            "run_id": run_id,
            "branch": branch_name,
            "artifact_path": archive_run_url or str(archive.path),
        }
        attachments = slack_payload.setdefault("attachments", [])
        if attachments:
            attachments[0].setdefault("fields", []).append(
                {
                    "title": "Archive",
                    "value": str(archive.path),
                    "short": False,
                }
            )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)

    slack_payload_path.parent.mkdir(parents=True, exist_ok=True)
    with slack_payload_path.open("w", encoding="utf-8") as handle:
        json.dump(slack_payload, handle, ensure_ascii=False, indent=2)

    if archive is not None:
        archive.write(
            payload,
            slack_payload,
            inputs={
                "report": str(report_path),
                "matrix": str(matrix_path),
                "glossary": str(glossary_path),
                "output": str(output_path),
                "slack_payload": str(slack_payload_path),
            },
            status=payload.get("conclusion"),
            branch=branch_name,
            run_id=run_id,
            artifact_path=archive_run_url or str(archive.path),
        )
        click.echo(f"Archive stored at {archive.path}", err=True)

    if output_format == "table":
        click.echo(render_table_summary(result))
    else:
        click.echo(json.dumps(payload, ensure_ascii=False, indent=2))

    if result.has_failures():
        raise click.exceptions.Exit(1)


@main.group(name="diff:archives")
def archives() -> None:
    """Archive utilities for diff verification runs."""


@archives.command(name="list")
@click.option(
    "--archive-dir",
    "archive_dir",
    type=click.Path(path_type=Path),
    default=Path("reports/ludeme/archive"),
    show_default=True,
    help="Directory containing stored diff verification archives.",
)
@click.option(
    "--latest",
    "latest_only",
    is_flag=True,
    default=False,
    help="Limit output to the latest archives (see --count).",
)
@click.option(
    "--count",
    "count",
    type=int,
    default=5,
    show_default=True,
    help="Number of archives to display when --latest is supplied.",
)
@click.option(
    "--output",
    "output_path",
    type=click.Path(path_type=Path),
    default=None,
    help="Optional path to write the JSON summary.",
)
def list_archives_cmd(
    archive_dir: Path,
    latest_only: bool,
    count: int,
    output_path: Path | None,
) -> None:
    """List stored archives along with summary metadata."""

    latest = count if latest_only else None
    archives = list_archives(archive_dir, latest=latest)
    data = [metadata.as_dict(relative_to=archive_dir) for metadata in archives]

    payload = json.dumps(data, ensure_ascii=False, indent=2)
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload, encoding="utf-8")

    click.echo(payload)


@archives.command(name="inspect")
@click.argument("run_id")
@click.option(
    "--archive-dir",
    "archive_dir",
    type=click.Path(path_type=Path),
    default=Path("reports/ludeme/archive"),
    show_default=True,
    help="Directory containing stored diff verification archives.",
)
@click.option(
    "--output",
    "output_path",
    type=click.Path(path_type=Path),
    default=None,
    help="Optional path to write the metadata JSON.",
)
def inspect_archive_cmd(
    run_id: str,
    archive_dir: Path,
    output_path: Path | None,
) -> None:
    """Inspect metadata for a specific archive run."""

    metadata = find_archive_by_run_id(archive_dir, run_id)
    details = metadata.as_dict(relative_to=archive_dir)
    files_status = {
        name: {
            "path": str(Path(details["path"]) / relative_path),
            "exists": (metadata.path / relative_path).exists(),
        }
        for name, relative_path in metadata.files.items()
    }
    details["files_status"] = files_status

    payload = json.dumps(details, ensure_ascii=False, indent=2)
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload, encoding="utf-8")

    click.echo(payload)


if __name__ == "__main__":  # pragma: no cover
    main()
