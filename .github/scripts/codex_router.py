#!/usr/bin/env python3
import sys, os, json, pathlib, re, datetime

body = sys.stdin.read()

ack = []
branch_suffix = None

def ensure_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

# Commands
PHASE1 = re.search(r'phase-1', body, re.IGNORECASE)

if PHASE1:
    branch_suffix = "phase-1"
    created = []
    created.append(ensure_file("docs/checklists/kpi.md",
"""# KPI チェックリスト（Ludeme 語彙導入）
- 粒度一致 ≥ 70%
- CI Green（validate/build/alloy/dist）
- ライセンス承認の記録（docs/legal/approval.md）
"""))
    created.append(ensure_file("docs/mapping/matrix.csv",
"""model_id,fact_tag,current_text,proposed_ludeme.category,proposed_ludeme.term,mapping_type,evidence_source_id,page,notes
"""))
    ack.append("📦 phase-1: checklist & mapping を準備しました。必要ファイルがなければ生成済みです。")
else:
    ack.append("👋 @codex 反応しました。`phase-1` と書くと PoC の雛形を用意します。")

# Write acknowledgment message
with open(".codex_router.out", "w", encoding="utf-8") as f:
    f.write("\n".join(ack))

# Set outputs for the workflow
print(f"::set-output name=branch_suffix::{branch_suffix or ''}")
