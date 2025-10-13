**目的:** 構文・型・参照の機械保証（エディタ補完/CI軽量チェック）

## 要件
- **Edition Modelスキーマ**  
  - `facts[*].evidence` と `variants[*].evidence` は **minItems:1**。  
  - `evidence.sourceId` は **sources[*].id に存在**（※標準Schemaでは困難のため、CI補助スクリプトで厳格化）。
- **シリーズ・オーバーレイ**  
  - シリーズ固有の **必須Fact ID** の存在、**タグ網羅（SETUP/TURN/WIN）**、**許可Variant ID** の加約。
- **QA Packageスキーマ**  
  - 出力の`meta`と`qa[*].citations[*]` の構造検証。

## 成果物
- `schemas/edition-model.schema.json`（共通）
- `schemas/overlays/<series>.series.overlay.json`（シリーズごと）
- `schemas/qa-package.schema.json`（出力）

> **注意:** 本ドキュメントは仕様。**スキーマ本体は既に雛形あり**（この要件に沿ってCodexで整備）。

