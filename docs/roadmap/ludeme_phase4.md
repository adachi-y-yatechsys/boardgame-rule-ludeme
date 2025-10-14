# Ludeme Phase 4 ロードマップ草案

## 目的
- Phase 4 で着手する CI 差分検証 PoC（P4-BL-01〜P4-BL-05）の役割と期限を整理し、バックログから実装までの流れを明確にする。
- Diff レポートパーサと Glossary 照合モジュールの骨子を共有し、Codex スレッドでのレビューを容易にする。
- `diff:verify` CI・GitHub Checks・Slack 通知の運用手順を Phase 3 までの成果物と接続し、PoC ブランチで安全に検証する。

## 手順

### マイルストーン
| マイルストーン | 内容 | 目標日 | 担当 | 依存タスク |
| --- | --- | --- | --- | --- |
| M1: CLI 骨子確定 | Diff レポートパーサ/Glossary モジュール仕様レビュー完了、`requirements/16f` 更新 | 2024-05-10 | ChatGPT（CI 支援）、依頼者（レビュー） | Phase 3 Glossary 決裁 |
| M2: PoC ブランチ起動 | `feature/phase4-diff-verify-poc` で CLI スタブと `diff:verify` ワークフローを配置、Dry Run 実施 | 2024-05-17 | ChatGPT（CI 支援） | M1 完了 |
| M3: 通知連携検証 | Slack Webhook 仮接続、GitHub Checks アノテーション確認、Codex で対応ログ運用開始 | 2024-05-22 | 依頼者（統合担当）、ChatGPT（CI 支援） | M2 完了、Slack テスト環境 |
| M4: 差分許容ルール評価 | 許容ルール `rules/tolerance.py` の閾値レビュー、Glossary 更新フロー確立 | 2024-05-24 | 依頼者（QA 兼任） | M3 完了 |

### モジュール骨子

#### P4-BL-01: Diff レポートパーサ CLI
```text
tools/
  ludeme_diff/
    __init__.py
    cli.py                  # click / argparse で `verify` サブコマンド定義
    loaders/
      diff_report.py        # JSON/CSV 読み込み・バリデーション（pydantic）
    rules/
      status.py             # status 判定ロジック（critical/warning/info）
      tolerance.py          # 許容差分判定（P4-BL-05 連携）
    outputs/
      summary.py            # GitHub Checks/Slack 向けサマリ生成
      slack.py              # Slack payload 整形（差分許容結果を含む）
tests/
  test_cli_verify.py        # CLI E2E（fixture: diff_report.json）
  test_rules_status.py      # status 判定ユニットテスト
```
- `verify` サブコマンドは `--report` `--matrix` `--glossary` `--output` `--format json|table` をサポート。
- 失敗時は exit code 1、警告のみの場合は 0（Slack info のみ）。
- CLI 実装担当: ChatGPT（CI 支援）。レビュー: 依頼者（CI オーナー）。レビュー期限: 2024-05-13 EOD JST。

#### P4-BL-02: Glossary 照合モジュール
- 入力: `docs/glossary/ludeme_terms.csv`（列: `term_key`,`canonical_ja`,`canonical_en`,`notes`）。
- マッピング: `docs/mapping/matrix.csv` の `ludeme.term` をキーに `term_key` を参照、Diff レポート `entry_id` と結合。
- 判定フロー:
  1. `canonical_ja` を NFKC 正規化。
  2. 許容差分判定（句読点等） → `status = info`。
  3. 完全一致しない場合は `status = failure`、`needs_glossary` タグを付与。
- アウトプット: CLI `summary` JSON に `glossary_actions` 配列（`entry_id`,`term_key`,`action_required`）を追加。
- 担当: 実装 ChatGPT（翻訳補助）、Glossary レビュー 依頼者（QA）。期限: 2024-05-17。

### CI・通知準備
- GitHub Actions 雛形は `docs/requirements/16f_ci_diff_verification.md` に準拠し、`requirements-diff.txt` を生成。
- GitHub Checks 投稿は `actions/github-script` を利用し、最大 50 件のアノテーションを表示。
- Slack 通知: `reports/ludeme/slack_payload.json` を CLI 側で生成し、Webhook は PoC ブランチ限定シークレット。
- Codex フォローアップ: 失敗時に `@codex follow-up: diff verify failure` コメントを投稿し、担当・期限・再実行条件を明示。

## 判定基準
- マイルストーン M1〜M4 の担当・期限が明示され、Phase 3 からの依存関係が解消されている。
- P4-BL-01/P4-BL-02 のモジュール構成・責務・失敗条件が CLI 仕様と一致し、Codex でレビュー可能。
- CI/通知準備項目が `diff:verify` 失敗時のハンドリング（GitHub Checks・Slack・Codex）と整合している。

## 参考
- `docs/requirements/16f_ci_diff_verification.md`
- `docs/roadmap/ludeme_phase3.md`
- `reports/ludeme/diff_report.json`
- `docs/mapping/matrix.csv`
- `docs/checklists/kpi.md`

## Codex 運用メモ（Phase 4）

### 目的
- 差分検証 PoC のフォローアップを Codex スレッドで一元管理し、レビュー負荷を可視化する。

### 手順
1. `diff:verify` 失敗時に Slack 通知と同時に Codex コメントテンプレを投稿（担当・期限・再実行条件を記録）。
2. 対応完了後に同スレッドへ結果報告（コミット ID / CI リンク）を残し、`resolved` を明示。
3. 週次で未クローズのフォローアップを棚卸しし、Phase 4 レトロスペクティブに持ち込む。

### 判定基準
- Codex コメントテンプレが `docs/requirements/16f_ci_diff_verification.md` と一致し、運用者が迷わない。
- 未クローズフォローアップ数を週次報告し、Slack #ludeme-ci でも共有できる仕組みが整っている。

### 参考
- Slack #ludeme-ci チャンネル
- GitHub Checks 履歴
- `docs/review/phase3_summary.md`
