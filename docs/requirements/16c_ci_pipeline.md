# 16c. CI パイプライン（Ludeme 検証）

## 追加タスク
- `validate:ludeme:overlay` : `schemas/overlays/*.overlay.json` を Schema Draft 2020-12 で検証
- `check:alloy:ludeme` : `spec/base.als` + `spec/ludeme_ext.als` を実行し存在制約を検証（任意）
- `report:ludeme:diff` : 付与前後の Q&A / citations / evidence 欄を比較し CSV 出力

## 参考コマンド（例）
```bash
npm run validate:models
npm run check:alloy
npm run build
npm run validate:dist
npm run validate:ludeme:overlay
npm run check:alloy:ludeme
npm run report:ludeme:diff -- --series catan --edition 5th
```

## 成果物
- `reports/ludeme/mapping-matrix.csv`
- `reports/ludeme/diff-summary.csv`
- `reports/ludeme/ci-status.json`
