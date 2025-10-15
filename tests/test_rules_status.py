from pathlib import Path

from tools.ludeme_diff.loaders import load_diff_report, load_glossary, load_mapping_matrix
from tools.ludeme_diff.rules import evaluate_entries


FIXTURE_DIR = Path(__file__).parent / "fixtures"


def test_evaluate_entries_assigns_expected_severities(tmp_path: Path) -> None:
    diff_entries = load_diff_report(FIXTURE_DIR / "diff_report.json")
    glossary = load_glossary(Path("docs/glossary/ludeme_terms.csv"))
    mapping = load_mapping_matrix(FIXTURE_DIR / "matrix.csv")

    result = evaluate_entries(diff_entries, glossary, mapping)

    severities = {(finding.entry_id, finding.field): finding.severity for finding in result.findings}
    assert severities[("qna-001", "qa_text")] == "info"
    assert severities[("qna-002", "qa_text")] == "warning"
    assert severities[("qna-003", "citation")] == "failure"

    assert result.status_counts["failure"] == 1
    assert result.status_counts["warning"] == 1
    assert result.status_counts["info"] >= 2
    assert result.conclusion == "failure"

    assert any(action["term_key"] == "optionalSteal" for action in result.glossary_actions)
