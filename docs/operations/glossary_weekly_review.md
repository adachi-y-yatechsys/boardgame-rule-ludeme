# Glossary Weekly Review

## 目的
- Diff アーカイブで検出された Ludeme 用語のうち Glossary 未登録語を棚卸しし、対応優先度と担当者を決定する。
- 用語レビューの漏れを防ぎ、Phase 3 以降のドキュメント整備に必要な語彙を事前に確保する。

## 手順
### 週次レビューのチェックリスト
- [ ] `reports/ludeme/glossary_audit.csv` を最新化し、未登録語の一覧を取得する。
- [ ] 直近 1 週間の diff アーカイブを確認し、Glossary 対応が必要な用語の背景（エントリ、フィールド、状況）を整理する。
- [ ] 各用語の影響範囲を確認し、優先度（High / Medium / Low）と対応方針（追加 / 保留 / 別途検討）を決める。
- [ ] 担当者をアサインし、フォローアップ Issue または PR のリンクを記録する。
- [ ] レビュー結果を Slack / メールで共有し、未対応タスクは次週に持ち越すか判断する。

### 優先度・担当者記録テンプレート
| entry_id | term_key | 優先度 | action_owner | 対応方針 | 備考 |
| --- | --- | --- | --- | --- | --- |
| <!-- 例: qna-001 --> | <!-- 例: newTermKey --> | <!-- High / Medium / Low --> | <!-- @owner --> | <!-- 追加 / 保留 / 別途検討 --> | <!-- 背景メモ --> |

### 作業ログ更新
- 対応が決定した用語は `docs/glossary/ludeme_terms.csv` に追加するか、保留理由を `reports/ludeme/glossary_audit.csv` に追記する。
- レビュー後の決定事項は `docs/review/` 以下の定例議事録にリンクを残す。

## 判定基準
- Glossary 未登録語に対し、優先度と担当者がすべて設定されていること。
- 対応方針が `追加` または `保留/別途検討` で明記され、フォローアップ経路が定義されていること。
- チェックリストの項目が完了し、共有・記録が実施されていること。

## 参考
- 差分レポート: `reports/ludeme/diff_report.json`
- Glossary 原本: `docs/glossary/ludeme_terms.csv`
- 棚卸し結果: `reports/ludeme/glossary_audit.csv`
