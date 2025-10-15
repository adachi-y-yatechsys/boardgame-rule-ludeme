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
from .outputs import build_result_payload, build_slack_payload, render_table_summary
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
def verify(
    report_path: Path,
    matrix_path: Path,
    glossary_path: Path,
    output_path: Path,
    slack_payload_path: Path,
    output_format: str,
) -> None:
    """Verify diff report entries against glossary and tolerance rules."""

    entries = load_diff_report(report_path)
    mapping = load_mapping_matrix(matrix_path)
    glossary = load_glossary(glossary_path)

    result = evaluate_entries(entries, glossary, mapping)
    payload = build_result_payload(result)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)

    slack_payload_path.parent.mkdir(parents=True, exist_ok=True)
    with slack_payload_path.open("w", encoding="utf-8") as handle:
        json.dump(build_slack_payload(result), handle, ensure_ascii=False, indent=2)

    if output_format == "table":
        click.echo(render_table_summary(result))
    else:
        click.echo(json.dumps(payload, ensure_ascii=False, indent=2))

    if result.has_failures():
        raise click.exceptions.Exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
