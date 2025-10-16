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

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert "Phase 4 diff verification concluded" in payload["summary"]
    glossary_actions = payload["glossary_actions"]
    assert any(
        action["entry_id"] == "qna-002" and action["action_required"] == "confirm_punctuation_diff"
        for action in glossary_actions
    )

    slack_payload = json.loads(slack.read_text(encoding="utf-8"))
    assert slack_payload["text"] == "Ludeme diff verification report"
    glossary_field = next(
        field
        for field in slack_payload["attachments"][0]["fields"]
        if field["title"].lower() == "glossary actions"
    )
    assert "qna-002" in glossary_field["value"]


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
            "--run-id",
            "run-42",
            "--branch",
            "feature/test-branch",
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
    assert metadata["run_id"] == "run-42"
    assert metadata["branch"] == "feature/test-branch"
    assert metadata["status"] == "failure"
    assert metadata["artifact_path"].endswith(archive_path.name)
    assert any(
        action["entry_id"] == "qna-002" and action["action_required"] == "confirm_punctuation_diff"
        for action in metadata["glossary_actions"]
    )
    assert (archive_path / "diff_verify_results.json").exists()
    assert (archive_path / "slack_payload.json").exists()
    slack_payload = json.loads(slack.read_text(encoding="utf-8"))
    archive_field = next(
        field
        for field in slack_payload["attachments"][0]["fields"]
        if field["title"].lower() == "archive"
    )
    assert archive_path.name in archive_field["value"]


def test_archives_list_and_inspect(tmp_path: Path) -> None:
    runner = CliRunner()
    archive_dir = tmp_path / "archive"
    output = tmp_path / "diff_verify_results.json"
    slack = tmp_path / "slack_payload.json"

    verify_result = runner.invoke(
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
            "--run-id",
            "run-77",
            "--branch",
            "feature/demo",
        ],
    )

    assert verify_result.exit_code == 1

    list_result = runner.invoke(
        main,
        [
            "diff:archives",
            "list",
            "--archive-dir",
            str(archive_dir),
            "--latest",
        ],
    )
    assert list_result.exit_code == 0
    listings = json.loads(list_result.output)
    assert len(listings) == 1
    assert listings[0]["run_id"] == "run-77"
    assert listings[0]["branch"] == "feature/demo"
    assert listings[0]["artifact_path"]

    inspect_result = runner.invoke(
        main,
        [
            "diff:archives",
            "inspect",
            "run-77",
            "--archive-dir",
            str(archive_dir),
        ],
    )
    assert inspect_result.exit_code == 0
    inspection = json.loads(inspect_result.output)
    assert inspection["run_id"] == "run-77"
    assert inspection["files_status"]["diff_verify_results"]["exists"] is True
