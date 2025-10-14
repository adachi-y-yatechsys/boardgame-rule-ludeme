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
6. Codex スレッドでレビューおよびフォローアップ手順を共有し、担当・期限を明示する。

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

## CLI 実装方針（P4-BL-01 / P4-BL-02）

### 目的
- `reports/ludeme/diff_report.json` の差分を機械的に評価し、統一訳・引用・証跡の逸脱を早期に検知する。
- Glossary（ドラフト）とマッピング CSV の整合性を CI で担保し、Phase 4 バックログの High 優先タスクを着手可能な状態にする。

### 手順
1. Diff レポートパーサ CLI（`ludeme-diff verify`）の I/O・エラー仕様を定義し、PoC で必要なフィールド集計を網羅する。
2. Glossary 照合モジュールのデータ読込・正規化ルールを設計し、訳語の判定条件（厳密一致 / 許容差分）を明文化する。
3. CLI の構造をモジュール単位で分割し、テストスタブと拡張ポイントを設ける。
4. 各モジュールの担当と締切を Codex スレッドに記載し、進捗レビューの頻度を決める。

### 実装骨子

#### Diff レポートパーサ（P4-BL-01）
- **コマンド名**: `ludeme-diff verify --report reports/ludeme/diff_report.json --output reports/ludeme/diff_verify_results.json`
- **構成案**:
  - `cli.py`: 引数処理とサブコマンド登録。
  - `parsers/diff_report.py`: JSON/CSV 双方の読み込み、`DiffEntry` データクラス化。
  - `rules/status.py`: `status` 列の集計と `qa_text` / `citation` / `evidence` の失敗条件判定。
  - `reporters/summary.py`: GitHub Checks・Slack に共通利用するサマリ JSON を生成。
- **失敗条件**:
  - `qa_text` で Glossary 既定訳と不一致なエントリが存在。
  - `citation` または `evidence` の `status` が `review`・`pending`・`n/a` のまま検出。
  - Diff レポートのフォーマット不整合（必須フィールド欠損、JSON パースエラー）。
- **出力**:
  - `summary`: フィールド別失敗件数、最初の 10 件の詳細、再現手順リンク。
  - `checks_payload`: GitHub Checks API 用の conclusion / annotations。
- **担当・期限**:
  - 実装: ChatGPT（CI 支援）。
  - レビュー: 依頼者（CI オーナー）。
  - 期限: Phase 4 キックオフ T-5 営業日（2024-05-13 まで）。

#### Glossary 照合モジュール（P4-BL-02）
- **データ入力**: `docs/glossary/ludeme_terms.csv`（列: `term_key`,`canonical_ja`,`notes`）を想定。未整備の場合は Codex スレッドでドラフトを共有。
- **正規化手順**:
  - Unicode 正規化（NFKC）、全角/半角の統一、記号類のトリミング。
  - 括弧内ルビや注記を除外した `canonical_ja_core` を比較キーとして生成。
- **照合ロジック**:
  - Diff レポート中の `qa_text` → Glossary 参照キーへマッピング（`mapping matrix` の `ludeme.term` と突合）。
  - 許容差分ルール（P4-BL-05）を呼び出し、句読点のみの差異は `warning` として記録。
  - Glossary 未登録語は `needs_glossary` タグ付きで失敗扱いとし、Codex フォローアップに回す。
- **テスト観点**:
  - サンプル Glossary（3 例）で一致/不一致/許容差分を含むユニットテストを作成。
  - JSON/CSV 形式の diff レポート双方を fixture 化し、将来拡張に対応。
- **担当・期限**:
  - 実装: ChatGPT（CI 支援、翻訳補助）。
  - Glossary 承認: 依頼者（QA 兼任）。
  - 期限: Phase 4 スプリント Week 1（2024-05-17 終業まで）。

### 判定基準
- CLI 実装ドラフトにより `ludeme-diff verify` コマンドの入出力、失敗条件、責務が明文化されている。
- Diff レポートパーサおよび Glossary モジュールの担当・期限・レビュー手順が Codex スレッドで追跡可能。
- 許容差分ルール呼び出し点が定義され、通知モジュールとの連携が文書化されている。

### 参考
- `docs/mapping/matrix.csv`
- `reports/ludeme/diff_report.json`
- `docs/roadmap/ludeme_phase4.md`

## CI 実行計画（P4-BL-03）

### 目的
- `diff:verify` ジョブを GitHub Actions 上で再現し、PoC ブランチでの動作検証を可能にする。
- GitHub Checks 連携により、訳語揺れ検知結果を PR 上で即時可視化する。

### 手順
1. PoC 用ブランチ（`feature/phase4-diff-verify-poc`）に対してのみ `workflow_dispatch` / `pull_request` トリガーで `diff:verify` を実行する。
2. `reports/ludeme/diff_report.json` をアーティファクトとして取り込み、CLI 実行結果を JSON で保存。
3. GitHub Checks API（`actions/github-script` または `peter-evans/create-check`）を通じて、失敗時に注釈を投稿。
4. Slack Webhook 連携のためのシークレット（`SLACK_WEBHOOK_URL`）を PoC ブランチに限定して登録し、通知ジョブに渡す。

### GitHub Actions 雛形
```yaml
name: diff-verify

on:
  workflow_dispatch:
  pull_request:
    branches:
      - feature/phase4-diff-verify-poc
    paths:
      - 'reports/ludeme/**'
      - 'docs/**'
      - '.github/workflows/diff-verify.yml'

jobs:
  diff-verify:
    runs-on: ubuntu-latest
    permissions:
      checks: write
      contents: read
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-diff.txt

      - name: Run diff verify CLI
        run: |
          python -m ludeme_diff.cli verify \
            --report reports/ludeme/diff_report.json \
            --matrix docs/mapping/matrix.csv \
            --glossary docs/glossary/ludeme_terms.csv \
            --output reports/ludeme/diff_verify_results.json

      - name: Upload diff verify results
        uses: actions/upload-artifact@v4
        with:
          name: diff-verify-results
          path: reports/ludeme/diff_verify_results.json

      - name: Publish GitHub Check
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const payload = JSON.parse(fs.readFileSync('reports/ludeme/diff_verify_results.json', 'utf8'));
            const annotations = payload.checks_payload.annotations.slice(0, 50);
            await github.rest.checks.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              name: 'diff:verify',
              head_sha: context.payload.pull_request ? context.payload.pull_request.head.sha : context.sha,
              status: 'completed',
              conclusion: payload.checks_payload.conclusion,
              output: {
                title: 'Ludeme diff verification',
                summary: payload.summary,
                annotations,
              },
            });

      - name: Notify Slack (conditional)
        if: failure()
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        run: |
          curl -X POST -H 'Content-type: application/json' \
            --data @reports/ludeme/slack_payload.json "$SLACK_WEBHOOK_URL"
```

### PoC 実行条件
- 依存パッケージは `requirements-diff.txt`（新規作成、`pydantic`, `rich`, `requests` 等）に集約する。
- `ludeme_diff.cli` はリポジトリ内の `tools/ludeme_diff/` パッケージとして配置し、`python -m` で呼び出す。
- GitHub Checks 投稿では 50 件を超える注釈を切り捨て、詳細はアーティファクトで確認する運用とする。
- フォローアップ: チェック失敗時は Codex スレッドで `@codex follow-up: diff verify failure` コメントを投稿し、失敗条件と Slack 通知ログを共有する。

### 判定基準
- `diff:verify` ジョブの YAML 雛形が PoC ブランチのみに影響する構成で定義されている。
- GitHub Checks 投稿ロジックと Slack 連携の条件分岐が明文化され、失敗時の処理フローが Codex でレビュー可能。
- 依存パッケージと CLI 配置パスが文書化され、再現性のあるセットアップ手順になっている。

### 参考
- `.github/workflows` ディレクトリ
- `actions/github-script`
- `docs/roadmap/ludeme_phase4.md`

## 通知と差分許容ルール設計（P4-BL-04 / P4-BL-05）

### 目的
- Slack への失敗通知と Codex でのフォローアップ手順を統一し、訳語差分の対応遅延を防止する。
- 差分許容ルールを定義し、CI ノイズ（句読点変更等）を最小化する。

### 手順
1. Slack Webhook 送信フォーマットをテンプレ化し、失敗・警告・情報の 3 区分で色分けする。
2. 差分許容ルールを `rules/tolerance.py` として CLI に組み込み、通知レベル（`failure` / `warning` / `info`）を返す。
3. Codex スレッドでのフォローアップ文言テンプレートを定義し、実行者・期限を明示する。

### 通知パターン
| 失敗条件 | GitHub Checks | Slack | Codex フォローアップ |
| --- | --- | --- | --- |
| Glossary 不一致（`qa_text` が統一訳から逸脱） | `failure` 結果。対象エントリにアノテーション | :rotating_light: Critical（赤）で投稿。担当: ChatGPT → 依頼者へ mention | `@codex follow-up` で差分 URL、Glossary 更新案、対応期限（T+1 営業日）を記載 |
| `citation` ステータス `review` 以下 | `failure`。サマリに該当 ID を列挙 | :warning: Warning（黄）。担当: 依頼者（QA） | Codex でレビュー依頼コメント、期限（T+2 営業日）。証跡追加で再実行 |
| 許容差分（句読点・全角半角のみ） | `neutral`（結論: `success`、アノテーションなし） | :information_source: Info（青）。サマリのみ通知 | Codex 追記不要。次回 Glossary 更新で自動吸収 |
| CLI エラー（JSON パース不可等） | `failure`。`summary` に例外スタック | :rotating_light: Critical。担当: ChatGPT（CI 支援） | Codex でログ添付、再実行手順、期限（当日内）を共有 |

### 差分許容ルールドラフト
- **対象フィールド**: `qa_text` の句読点（。、，．）、半角スペース、波ダッシュ（〜）の正規化。
- **正規化処理**:
  1. Unicode NFKC 変換。
  2. 句読点を `。、` に統一。
  3. 連続スペースを単一スペースへ縮約。
- **判定**:
  - 正規化後に完全一致 → `info` レベル（CI 成功、Slack info）。
  - 正規化後も不一致 → Glossary チェックに移行し `failure`。
- **将来拡張**:
  - 数値・単位表記の揺れ（例: "1 枚" vs "一枚"）を外部辞書で吸収。
  - 否定語の挿入・削除は常に `failure`。

### フォローアップ運用
- **Codex コメントテンプレ**:
  - 形式: ``@codex follow-up: diff verify failure
    - 対象: qna-001 (qa_text)
    - 事象: Glossary 不一致
    - 対応者: 依頼者（QA）
    - 期限: 2024-05-15 EOD JST``
- **エスカレーション**:
  - 期限超過時は Slack #ludeme-ci でリマインドし、Codex コメントにリンク。
  - 2 サイクル連続で失敗した場合は Phase 4 レトロスペクティブに持ち越し、許容ルール見直しを検討。

### 判定基準
- Slack 通知テンプレートと差分許容ロジックが仕様化され、`diff:verify` 失敗条件とのマッピングが明確である。
- Codex フォローアップ手順がテンプレート化され、担当・期限の明示方法が定義されている。
- 許容差分ルールの将来拡張ポイントが記載され、Phase 4 の継続改善計画に沿っている。

### 参考
- Slack #ludeme-ci チャンネル運用ガイド（別紙）
- `docs/roadmap/ludeme_phase4.md`
- `docs/requirements/15_ci_workflow_template.md`

## PR 作成と完了報告フロー

### 目的
- Phase 4 差分検証 PoC の準備タスクを完了させる際の PR 作成・レビュー・報告手順を明文化し、担当者が迷わずタスクをクローズできるようにする。

### 手順
1. `feature/phase4-diff-verify-poc` ブランチで CLI/CI/通知の下準備が完了したら、`git status` で差分を確認し、必要なテスト（CLI ドライラン、Workflow Lint など）を実行する。
2. `docs/roadmap/ludeme_phase4.md` のマイルストーン達成状況を更新し、担当者・期限の変更がある場合は Codex スレッドで共有する。
3. PR タイトル案: `"Ludeme PoC/phase-4: diff verify PoC kickoff"` を用い、概要に以下の 3 点を必ず記載する。
   - 対応したバックログ ID（例: P4-BL-01〜P4-BL-05）
   - `diff:verify` 失敗条件と通知パターンのドラフト
   - フォローアップ手順の更新点（Codex コメントテンプレ等）
4. PR 作成後は GitHub Checks の結果を確認し、`diff:verify` が未実装のため `neutral` または `skipped` となる旨をレビュー依頼コメントに添えて説明する。
5. レビューで指摘が入った場合、コメントに対する対応方針と予定日を Codex スレッドに記載し、修正完了後は該当コメントを Resolve する。
6. マージ後（または PoC ブランチへの反映後）は Slack #ludeme-ci に要約を投稿し、Codex スレッドにてフォローアップ項目のクローズを宣言する。

### 判定基準
- PR 説明がバックログ ID、失敗条件、フォローアップ手順を含み、レビュー観点が明確になっている。
- Codex スレッドでの完了報告が Slack 投稿と整合し、Phase 4 のタスク残数が共有されている。

### 参考
- `.github/pull_request_template.md`
- Codex 運用ノート（Phase 3）
