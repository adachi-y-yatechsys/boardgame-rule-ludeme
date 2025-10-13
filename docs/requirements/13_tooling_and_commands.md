# ツール定義とコマンド規約（単一出典）

> 実装は Codex 側で行う。ここでは **バージョン固定** と **npm scripts 名称** を合意する。

## ランタイム／ツールのバージョン
- Node.js: **20.x**
- パッケージマネージャ: **npm**（pnpm/yarnは採用しない）
- Ajv CLI: **ajv-cli@^5**（Draft 2020-12 対応）
- Alloy: **Alloy Analyzer 6**（CLI 実行; `java -jar alloy6.jar` を想定）
- TypeScript: **^5.6**（tools/ 配下のユーティリティ用）

> Alloy の jar 配置は `tools/vendor/alloy/alloy6.jar` に固定（CIでキャッシュ可）。

## npm scripts 規約
- `validate:models` — models の **JSON Schema 検証**（+ 参照整合チェックを内包）
- `check:alloy` — **Alloy 検証**（base + series + patch_ext を順に）
- `build` — **プリレンダー生成**（models + presets → dist/qa/**）
- `validate:dist` — 出力（dist/**）を **QA Package スキーマ**で再検証
- `package:review` — 監修提出用の **対象絞り込み出力**（series/edition/players/preset 指定）

### 期待される実行順（ローカル）
```bash
npm run validate:models && npm run check:alloy && npm run build && npm run validate:dist
```

## 返り値と失敗条件（必須）
- いずれのコマンドも **非0 exit code** を失敗とする。
- `validate:models` 失敗条件：Schema不一致／参照切れ（evidence.sourceId 不存在）／必須フィールド欠落。
- `check:alloy` 失敗条件：`Valid`/`TagCoverage`/`PatchConsistent` のいずれかが **unsat** にならない（= 矛盾が検出された）場合は **exit 1**。
- `build` 失敗条件：ビルド時に参照欠落・パッチ適用不可・プリセット解決不可。
- `validate:dist` 失敗条件：QA Package スキーマ不一致。

## Alloy 実行パスとルール
- jar: `tools/vendor/alloy/alloy6.jar`
- ルート: `spec/` 配下。
- 実行対象:
  - `spec/base.als` — 常に実行
  - `spec/base_patch_ext.als` — 常に実行
  - `spec/<series>.als` — 変更があったシリーズのみ、なければスキップ可
- 射影データ: `tools/.work/alexpkg/<series>/<edition>/<preset>/<players>/package.als.json` （生成物）
- ラッパー: `tools/alloy_check.ts` が jar を `java -jar ...` で起動し、**結果を exit code に反映**。

## ログとアーティファクト
- 失敗時は **人間語エラー**（どの Fact/Variant/ID が原因か）を標準出力に整形。
- CI では `artifacts/` に以下を保存：
  - `dist/qa/**`（監修提出物）
  - `logs/**`（Schema/Alloyの詳細ログ）
  - `work/**`（任意; デバッグ用、一部はアップロード対象外）

## 差分ビルドの基本方針
- 変更ファイルから **影響グラフ** を算出：
  - edition.json / presets が変わった **シリーズ/版/プリセット/players** だけ再ビルド
  - schemas/spec の変更は **全再検証**

## コマンド引数（例）
- `npm run package:review -- --series catan --edition 5th --preset official --players 3,4`
  - 複数値はカンマ区切り。未指定は全通り。

