## ビルド手順（論理）
1) **入力**：`models/**/edition.json` + `presets/**`  
2) **Schema検証**：Ajvで edition.json の構文/参照（＋独自参照チェック）  
3) **パッチ適用**：`players`/`preset`を評価 → **最終facts集合**を確定  
4) **Alloy検証**：`base + series.als` と `base_patch_ext` を射影・実行  
5) **Q&A生成**：質問テンプレにmap → **短文＋citations** を出力  
6) **出力Schema検証**：`qa-package.schema.json` で dist/** を検証  
7) **成果物**：`dist/qa/.../<revHash>.json`（revHashはメタのダイジェスト）

## CI要件
- **差分ビルド**（変更のあった版/プリセットのみ対象）  
- **Artifacts**：dist/qa をアップロード（監修提出用）  
- **main直push禁止**、PR必須、CODEOWNERSで承認フロー。

