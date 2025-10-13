**目的:** 論理関係・充足性の保証（矛盾の早期検知）

## ベース制約（全シリーズ共通）
- Packageは **facts: some Fact**（空不可）。
- **Fact.idの一意性**、**tag非空**、**Fact/Variantはevidence>=1**。
- **Variant競合/依存**：`no v1 in v2.conflicts`、`depends ⊆ enabled`。
- **タグ網羅**：SETUP/TURN/WIN 各 >=1（必要ならシリーズ側で上書き）。

## 拡張（Variant→Fact検証）
- `replaces/requires/removes`（パッチから導出）を使って：
  - **二重置換禁止**、**remove↔requires矛盾禁止**、**remove対象が最終factsに残らない**。

## シリーズ追加制約（例：Catan）
- `board_setup/initial_placement/robber_on_seven/victory_condition` が **各ちょうど1**。
- 3人/4人用SETUPが同時に存在しない。

## 成果物
- `spec/base.als`, `spec/base_patch_ext.als`（共通）
- `spec/<series>.als`（シリーズ固有）

> **注意:** 本ドキュメントは仕様。**Alloy本体は既に雛形あり**（この要件に沿ってCodexで整備）。

