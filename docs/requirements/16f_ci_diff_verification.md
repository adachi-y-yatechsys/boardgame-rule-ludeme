# 16f. Phase 4 CI 差分検証ジョブ設計メモ

## 目的
- Phase 4 で追加する CI 差分検証ジョブの設計指針を整理し、Ludeme PoC で求められる訳語揺れ・エビデンス差分の自動検知を実現する。
- PoC 実装に向けたバックログ項目を洗い出し、担当者アサインと着手順序を明確にする。

## 手順
1. 差分検証対象を定義する（`qa_text`、`citation`、`evidence` を最低対象とし、将来的な拡張項目を洗い出す）。
2. 既存の CI ワークフロー（`validate:models` → `check:alloy` → `build` → `validate:dist`）に新ジョブ `diff:verify` を追加し、実行タイミングと依存関係を設計する。
3. 入力ファイル（diff レポート、マッピング CSV、Glossary）をジョブに渡す方法を決定し、キャッシュや成果物の扱いを整理する。
4. 失敗条件と通知チャネル（GitHub Checks / Slack Webhook 等）を定義し、訳語揺れ検知時のエラー文言テンプレートを作成する。
5. PoC バックログ項目の優先度を付け、スプリント計画に組み込む。

### 差分検証ジョブ仕様（ドラフト）
| 項目 | 内容 |
| --- | --- |
| ジョブ名 | `diff:verify` |
| 実行タイミング | `validate:dist` 完了後に実行し、成果物を再利用 |
| 入力 | `reports/ludeme/diff_report.json`、`docs/mapping/matrix.csv`、Glossary（予定: `docs/glossary/ludeme_terms.csv`） |
| 検証ロジック | `qa_text` で統一訳と一致しない差分がある場合は失敗。`citation`/`evidence` の status が `review` 以下の場合も失敗。 |
| 出力 | `reports/ludeme/diff_verify_results.json`（検知内容・ステータス・対応ガイド） |
| 通知 | GitHub Checks のアノテーション、Slack Webhook（#ludeme-ci）にサマリを送信 |
| リトライ | 差分が解消されるまで自動リトライなし。手動再実行のみ。 |

### PoC 実装バックログ
| ID | 項目 | 概要 | 優先度 | 担当（案） |
| --- | --- | --- | --- | --- |
| P4-BL-01 | Diff レポートパーサ | `reports/ludeme/diff_report.json` を解析し、フィールド別に status を集計する CLI を実装。 | High | ChatGPT（CI 支援） |
| P4-BL-02 | Glossary チェック | Glossary から統一訳を読み込み、`qa_text` と比較するモジュールを追加。 | High | ChatGPT（CI 支援、翻訳補助） |
| P4-BL-03 | GitHub Checks 連携 | `diff:verify` の結果を GitHub Checks に投稿し、失敗時にアノテーションを表示。 | Medium | ChatGPT（CI 支援） |
| P4-BL-04 | Slack 通知連携 | 失敗・警告時に Slack Webhook へ要約を送信する。 | Medium | 依頼者（統合担当） |
| P4-BL-05 | 差分許容ルール定義 | テキスト差分の許容条件（例: 句読点のみの変更）を設定する。 | Low | 依頼者（QA 兼任） |
| P4-BL-06 | 履歴アーカイブ | 差分検証結果を `reports/ludeme/archive/` に保存し、履歴を参照可能にする。 | Low | ChatGPT（CI 支援） |

## 判定基準
- `diff:verify` ジョブで `qa_text` の統一訳「盗賊を移動し、隣接プレイヤーから資源カードを1枚奪取」が参照され、揺れが検知されるとジョブが失敗すること。
- バックログ項目 P4-BL-01〜P4-BL-04 が Phase 4 キックオフまでに担当者・締切付きで登録されていること。
- 差分検証結果が CI 成果物として保存され、レビューで根拠を追跡できること。

## 参考
- `docs/requirements/16c_ci_pipeline.md`
- `docs/requirements/16d_license_compliance.md`
- `docs/checklists/kpi.md`
- `reports/ludeme/diff_report.json`
- `docs/roadmap/ludeme_phase3.md`
