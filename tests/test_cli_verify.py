import json
from pathlib import Path

from click.testing import CliRunner

from tools.ludeme_diff.cli import main

FIXTURE_DIR = Path(__file__).parent / "fixtures"


def test_verify_cli_outputs_json_and_exit_code(tmp_path: Path) -> None:
    runner = CliRunner()
    output = tmp_path / "diff_verify_results.json"
    slack = tmp_path / "slack_payload.json"

    result = runner.invoke(
        main,
        [
            "verify",
            "--report",
            str(FIXTURE_DIR / "diff_report.json"),
            "--matrix",
            str(FIXTURE_DIR / "matrix.csv"),
            "--glossary",
            str(Path("docs/glossary/ludeme_terms.csv")),
            "--output",
            str(output),
            "--slack-payload",
            str(slack),
        ],
    )

    assert result.exit_code == 1

    payload_text = output.read_text(encoding="utf-8")
    assert "Phase 4 diff verification concluded" in payload_text

    slack_text = slack.read_text(encoding="utf-8")
    assert "Ludeme diff verification report" in slack_text


def test_verify_cli_archives_outputs(tmp_path: Path) -> None:
    runner = CliRunner()
    output = tmp_path / "diff_verify_results.json"
    slack = tmp_path / "slack_payload.json"
    archive_dir = tmp_path / "archive"

    result = runner.invoke(
        main,
        [
            "verify",
            "--report",
            str(FIXTURE_DIR / "diff_report.json"),
            "--matrix",
            str(FIXTURE_DIR / "matrix.csv"),
            "--glossary",
            str(Path("docs/glossary/ludeme_terms.csv")),
            "--output",
            str(output),
            "--slack-payload",
            str(slack),
            "--archive-dir",
            str(archive_dir),
            "--archive-label",
            "CI Run",
        ],
    )

    assert result.exit_code == 1
    archive_entries = list(archive_dir.iterdir())
    assert len(archive_entries) == 1
    archive_path = archive_entries[0]
    assert archive_path.name.endswith("ci-run")

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["archive"]["name"].endswith("ci-run")

    metadata = json.loads((archive_path / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["status_counts"]["failure"] > 0
    assert (archive_path / "diff_verify_results.json").exists()
    assert (archive_path / "slack_payload.json").exists()
    slack_payload = json.loads(slack.read_text(encoding="utf-8"))
    archive_field = next(
        field
        for field in slack_payload["attachments"][0]["fields"]
        if field["title"].lower() == "archive"
    )
    assert archive_path.name in archive_field["value"]
