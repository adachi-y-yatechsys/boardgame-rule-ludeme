"""Slack payload helper."""

from __future__ import annotations

from typing import Dict

from ..rules import VerificationResult


def build_slack_payload(result: VerificationResult) -> Dict:
    """Return a Slack message payload summarising verification."""

    color = "#2eb886" if not result.has_failures() else "#e01e5a"
    title = "diff:verify success" if not result.has_failures() else "diff:verify requires action"
    summary = (
        f"Failures: {result.status_counts.get('failure', 0)}, "
        f"Warnings: {result.status_counts.get('warning', 0)}, "
        f"Info: {result.status_counts.get('info', 0)}"
    )

    return {
        "text": "Ludeme diff verification report",
        "attachments": [
            {
                "color": color,
                "title": title,
                "text": summary,
                "fields": [
                    {
                        "title": "Glossary actions",
                        "value": "\n".join(
                            f"• {item['entry_id']} → {item['action_required']} ({item['term_key'] or 'unknown'})"
                            for item in result.glossary_actions
                        )
                        or "なし",
                    }
                ],
            }
        ],
    }
