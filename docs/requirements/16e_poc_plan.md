# 16e. PoC 実施計画（Catan seed）

## スコープ
- 対象: 代表 10 Fact/Variant（SETUP/TURN/WIN/RESOLVE）
- 非対象: UI 表示の語彙変更（内部メタのみ）

## 手順
1. 対象 Fact/Variant に `ludeme` 属性を追加（category / term / note）
2. Overlay Schema を通過（任意フィールド）
3. Alloy（ludeme 拡張）を通過（警告レベル）
4. build / validate:dist で出力整合性を確認
5. 差分レポートをレビュー会議で承認

## 受け入れ基準
- KPI 3軸達成
- Q&A 出力が PoC 前後で文言・引用一致
