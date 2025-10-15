"""Command line interface for Ludeme diff verification."""

from __future__ import annotations

import json
from pathlib import Path

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
def verify(
    report_path: Path,
    matrix_path: Path,
    glossary_path: Path,
    output_path: Path,
    slack_payload_path: Path,
    output_format: str,
    archive_dir: Path | None,
    archive_label: str | None,
) -> None:
    """Verify diff report entries against glossary and tolerance rules."""

    entries = load_diff_report(report_path)
    mapping = load_mapping_matrix(matrix_path)
    glossary = load_glossary(glossary_path)

    result = evaluate_entries(entries, glossary, mapping)
    payload = build_result_payload(result)
    slack_payload = build_slack_payload(result)
    archive: ArchiveRecord | None = None

    if archive_dir is not None:
        archive = prepare_archive(archive_dir, label=archive_label)
        payload["archive"] = {
            "path": str(archive.path),
            "name": archive.path.name,
            "timestamp": archive.timestamp,
            "label": archive.label,
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
        )
        click.echo(f"Archive stored at {archive.path}", err=True)

    if output_format == "table":
        click.echo(render_table_summary(result))
    else:
        click.echo(json.dumps(payload, ensure_ascii=False, indent=2))

    if result.has_failures():
        raise click.exceptions.Exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
