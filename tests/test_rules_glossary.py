from tools.ludeme_diff.loaders.diff_report import DiffEntry
from tools.ludeme_diff.loaders.glossary import GlossaryTerm
from tools.ludeme_diff.loaders.matrix import MappingIndex, MappingRow
from tools.ludeme_diff.rules import evaluate_entries


def _make_entry(entry_id: str, new_value: str) -> DiffEntry:
    return DiffEntry(
        series="test",
        edition="2024",
        entry_id=entry_id,
        field="qa_text",
        change_type="updated",
        previous_value="",
        new_value=new_value,
        status="confirmed",
        notes="",
    )


def _build_mapping() -> MappingIndex:
    index = MappingIndex()
    index.add(
        MappingRow(
            model_id="model-match",
            fact_tag="FT1",
            current_text="",
            ludeme_category="play",
            ludeme_term="term.match",
            mapping_type="derived",
            evidence_source_id="",
            page="",
            notes="",
            entry_id="entry-match",
        )
    )
    index.add(
        MappingRow(
            model_id="model-unreg",
            fact_tag="FT2",
            current_text="",
            ludeme_category="play",
            ludeme_term="term.unregistered",
            mapping_type="derived",
            evidence_source_id="",
            page="",
            notes="",
            entry_id="entry-unreg",
        )
    )
    index.add(
        MappingRow(
            model_id="model-punct",
            fact_tag="FT3",
            current_text="",
            ludeme_category="play",
            ludeme_term="term.punct",
            mapping_type="derived",
            evidence_source_id="",
            page="",
            notes="",
            entry_id="entry-punct",
        )
    )
    index.add(
        MappingRow(
            model_id="model-diff",
            fact_tag="FT4",
            current_text="",
            ludeme_category="play",
            ludeme_term="term.differs",
            mapping_type="derived",
            evidence_source_id="",
            page="",
            notes="",
            entry_id="entry-diff",
        )
    )
    return index


def _build_glossary() -> dict[str, GlossaryTerm]:
    return {
        "term.match": GlossaryTerm(
            term_key="term.match",
            canonical_ja="統一訳そのまま",
            canonical_en="Match",
            notes="",
        ),
        "term.punct": GlossaryTerm(
            term_key="term.punct",
            canonical_ja="句読点のみ許容",
            canonical_en="Punctuation",
            notes="",
        ),
        "term.differs": GlossaryTerm(
            term_key="term.differs",
            canonical_ja="完全一致テキスト",
            canonical_en="Different",
            notes="",
        ),
    }


def test_evaluate_entries_glossary_cases() -> None:
    mapping = _build_mapping()
    glossary = _build_glossary()
    entries = [
        _make_entry("entry-match", "統一訳そのまま"),
        _make_entry("entry-unreg", "未登録語訳"),
        _make_entry("entry-punct", "句読点のみ許容、"),
        _make_entry("entry-diff", "ずれたテキスト"),
    ]

    result = evaluate_entries(entries, glossary, mapping)

    severities = {finding.entry_id: finding.severity for finding in result.findings}
    assert severities["entry-match"] == "info"
    assert severities["entry-unreg"] == "failure"
    assert severities["entry-punct"] == "warning"
    assert severities["entry-diff"] == "failure"

    glossary_actions = {action["entry_id"]: action for action in result.glossary_actions}
    assert glossary_actions["entry-unreg"]["action_required"] == "register_glossary_term"
    assert glossary_actions["entry-punct"]["action_required"] == "confirm_punctuation_diff"
    assert glossary_actions["entry-diff"]["action_required"] == "update_translation"

    tolerance = next(
        finding.tolerance for finding in result.findings if finding.entry_id == "entry-punct"
    )
    assert tolerance is not None and tolerance.tolerated is True

    assert result.conclusion == "failure"
