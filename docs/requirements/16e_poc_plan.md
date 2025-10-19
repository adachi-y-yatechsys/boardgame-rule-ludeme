# 16e. PoC 実施計画（Catan seed）

## スコープ
- 対象: 代表 10 Fact/Variant（SETUP/TURN/WIN/RESOLVE）
- 非対象: UI 表示の語彙変更（内部メタのみ）

## 手順
1. 対象 Fact/Variant に `ludeme` 属性を追加（category / term / note）
2. Overlay Schema を通過（任意フィールド）
3. Alloy（ludeme 拡張）を通過（警告レベル）
4. `npm run validate:models && npm run check:alloy && npm run build && npm run validate:dist` を通し、Node/Alloy パイプラインで出力整合性を確認
5. 差分レポートをレビュー会議で承認

## Phase 2 追加タスク（Codex 実装分）
- `package.json` を新設し、`validate:models` / `check:alloy` / `build` / `validate:dist` スクリプトを実装する（参照: `boardgame-rule-model` の雛形）。Alloy CLI は `tools/vendor/alloy/alloy6.jar` を前提に `java -jar` で呼び出す。
- Ajv ベースの schema/overlay 検証スクリプト（例: `tools/scripts/validate-schemas.mjs`）を整備し、`validate:models` から呼び出す。
- 必要なランタイム（Node 20.x、Alloy 6、Ajv CLI など）とセットアップ手順を `docs/requirements/13_tooling_and_commands.md` および本書へ追記する。
- npm チェーンのローカル実行ログと生成物（`dist/**`、`logs/**` など）を `reports/ludeme/` 配下に保存し、`tools.ludeme_diff.cli verify` の結果と合わせて Phase 2 成果物として共有する。

### Phase 2 実績サマリ（2025-10-19）
- `npm run validate:models && npm run check:alloy && npm run build && npm run validate:dist` をローカル実行し、各ログを `reports/ludeme/pipeline/` に保存済み。
- `python -m tools.ludeme_diff.cli verify ...` の結果を再取得し、`reports/ludeme/diff_verify_results.json` およびアーカイブ配下に反映済み。
- `reports/ludeme/archive/latest_summary.json` を更新し、最新アーカイブ（`20251019T035553794319Z-local-run`）を参照するよう調整済み。
- 以降は Phase 3 にて KPI 判定と導入判断のドキュメント化を進める。

### 環境セットアップと検証フロー
1. [`docs/requirements/13_tooling_and_commands.md`](13_tooling_and_commands.md) に従い Node.js 20.x／Ajv CLI／Alloy6 を導入し、`tools/vendor/alloy/alloy6.jar` を配置する。
2. リポジトリ直下で `npm install` を実行し、`validate:models` / `validate:dist` から参照する Ajv ランタイムを揃える。
3. `npm run validate:models && npm run check:alloy && npm run build && npm run validate:dist` を通し、`reports/ludeme/pipeline/*.log` に実行ログを収集する。
4. `python -m tools.ludeme_diff.cli verify ... --archive-dir reports/ludeme/archive` を実行し、`diff_verify_results.json`／`slack_payload.json`／アーカイブを更新する。
5. `reports/ludeme/archive/generate_summary.py` を併用し、最新アーカイブが `latest_summary.json` に反映されていることを確認する。

## 受け入れ基準
- KPI 3軸達成
- Q&A 出力が PoC 前後で文言・引用一致
- `npm run validate:models && npm run check:alloy && npm run build && npm run validate:dist` が成功し、実行ログが `reports/ludeme/` に残っている
- 差分レポート検証（`python -m tools.ludeme_diff.cli verify ...`）と npm チェーン双方の成果物をレポート済みである
