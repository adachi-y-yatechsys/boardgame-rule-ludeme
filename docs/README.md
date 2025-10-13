# boardgame-rule-ludeme

Ludeme 語彙を既存のボードゲーム・ルールモデルに非破壊で参照導入する検証プロジェクト。
- 目的: 語彙整合・表現力向上・引用管理の強化
- 成果物: 要件ドキュメント、KPIチェックリスト、PoCマッピング、CI検証

## 進め方（@codex への依頼）
- Issue: "Ludeme PoC: phase-1" を作成し、本READMEに沿ってチェックリストとマッピングを出力
- PR: "Ludeme PoC/phase-1: checklist & mapping" を作成し、docs を更新

## Phase 2: CI 検証フロー

### 目的
- validate → alloy → build → validate:dist + overlay の一連の検証を標準化し、Ludeme 拡張が既存モデルへ非破壊で適用できることを確認する。

### 前提
- このリポジトリはドキュメント／レポート用のスケルトンであり、`package.json`・`spec/`・`schemas/overlays/`・`dist/` などの検証対象資材は同梱されていない。
- 実際の検証は、メンテナが管理するルールモデル本体（例: `ludeme-integration` ブランチ付きリポジトリや CI 用テンプレート）を別途クローンして実施する。
  - 例: `git clone <maintainer-shared-repo-url> ludeme-ci-workspace && cd ludeme-ci-workspace`
  - `package.json` に本節で言及する npm スクリプトが定義されていること、`spec/` および `schemas/overlays/` 配下に検証対象ファイルが配置されていることを確認する。
- `reports/ludeme/` ディレクトリは CI 実行環境と本ドキュメントの両方から参照できる共有パス（例: Git ワークスペース直下）に揃えておく。

### 手順
0. **ワークスペースの整備**: 前提の通り検証用リポジトリを用意し、`npm install` を実行して依存関係を取得する。必要に応じてこのドキュメントを隣接させ、CI が生成する差分レポートの配置先を `reports/ludeme/` に合わせる。
1. **ベースモデルの検証**: `npm run validate:models` を実行し、既存 JSON Schema / データモデルの整合性を確かめる。
2. **Alloy 制約チェック**: `npm run check:alloy` で `spec/base.als` の存在制約を検証し、基礎ルールが充足することを確認する。
3. **ビルド**: `npm run build` を実行し、配布物 (`dist/`) を生成する。
4. **配布物検証**: `npm run validate:dist` でビルド成果物の JSON Schema 検証を行い、Ludeme 適用前の品質を担保する。
5. **オーバーレイ検証**: `npm run validate:ludeme:overlay` を実行し、`schemas/overlays/*.overlay.json` が Draft 2020-12 準拠であることを確認する。
6. **Ludeme 拡張 Alloy**: `npm run check:alloy:ludeme` により `spec/base.als` と `spec/ludeme_ext.als` を合わせた制約を検証し、拡張後も矛盾がないことを確認する。
7. **差分レポート生成**: `npm run report:ludeme:diff -- --series <series> --edition <edition>` を実行し、Q&A／引用／エビデンス欄の差分を `reports/ludeme/` 以下に出力する。

### 判定基準
- 各コマンドがエラー無く完了し、ビルド済み成果物が最新である。
- `schemas/overlays/` の全ファイルが JSON Schema Draft 2020-12 で検証済みである。
- `reports/ludeme/` に差分レポート（CSV/JSON）が生成され、検証対象の Q&A・引用・エビデンス差分が整理されている。

### 参考
- `AGENTS.md`
- `reports/ludeme/diff_report.csv`、`reports/ludeme/diff_report.json`
