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
