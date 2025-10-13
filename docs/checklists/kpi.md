# Ludeme PoC KPI チェックリスト

## 目次
- [評価観点別チェックリスト](#評価観点別チェックリスト)
- [DOR/DOD トラッキング](#dordod-トラッキング)
- [未解決事項リスト](#未解決事項リスト)
- [参照ドキュメント](#参照ドキュメント)

## 評価観点別チェックリスト

### 粒度一致度（Granularity Alignment）
- [ ] 代表10項目（SETUP/TURN/WIN/RESOLVE 各2件以上）を選定し、`docs/mapping/matrix.csv` に登録した（現状: 10件中 RESOLVE=1件、WIN=1件 → 追加候補を要検討）。
- [ ] 各項目に `ludeme.category` / `ludeme.term` を暫定割り当てした（`mapping_type=derived` の理由メモを確認）。
- [ ] 対応結果を「完全一致 / 要派生 / 不可」に分類した（現状: `mapping_type` 列の語彙が暫定、判定ロジック未定義）。
- [ ] 「完全一致」割合が 70% 以上である（現状: `exact` 2件 / 10件 → 20%）。
- [ ] 不一致項目に対し UI/UX 影響を記述した（現状: notes 欄に影響記載なし）。

### エビデンス記述適合度（Evidence Compatibility）
- [ ] `evidence[*].sourceId/page/loc` がマッピング後も欠落していない（現状: page=`TBD` のまま）。
- [ ] CI（`validate:models` → `check:alloy` → `build` → `validate:dist`）がすべて Green（現状: 実施待ち）。
- [ ] 差分レポートで Q&A と citations が PoC 前後で一致（現状: `qa_text` 更新1件=review／`citation` 追加1件=confirmed／`evidence` 変化なし1件=n/a → 用語統一レビュー待ち）。

### ライセンス整合度（License Compatibility）
- [ ] Ludii/Ludeme 配布物の同梱・改変配布を行っていない（現状: 同梱なし、定期監査手順未策定）。
- [ ] 語彙・短い文言の引用には出典明記を行っている（現状: `notes` 欄に出典メモ未記載）。
- [ ] 法務レビューの承認を記録した（現状: `docs/legal/approval.md` 未更新）。

### 差分レポート集計（最新）

| KPI軸 | diff_report ステータス集計 | リスク/備考 |
| --- | --- | --- |
| 粒度一致度 | `qa_text` 更新1件 = **review** | 用語統一が未確定のためレビュー継続。 |
| エビデンス適合度 | `citation` 追加1件 = **confirmed**／`evidence` 変化なし1件 = **n/a** | 引用IDは整合済み。画像証跡は変更なしを確認済み。 |
| ライセンス整合度 | 該当差分なし | 監査手順と承認記録の更新が未実施。 |

## DOR/DOD トラッキング
- [ ] Catan seed の対象 Fact/Variant が 10 項目以上選定済み（現状: 10件を暫定選定、粒度バランス要見直し）。
- [ ] 追加 `ludeme` 属性の JSON 例が共有済み（現状: 要件 16 章にサンプルあり、レビュー要）。
- [ ] KPI 3軸を満たす（粒度≥70%、CI Green、法務承認）（現状: 未達）。
- [ ] ドキュメント（16* 章）が埋まっている（現状: 16 系列は骨子あり、検証手順の追記進行中）。

## 未解決事項リスト
- 粒度評価の判定ルールを `mapping_type` 以外に明文化する（例: `exact/derived/hold` の定義、測定方法）。
- エビデンス整合チェックを自動化する CI 手順（Phase 2 で実装予定）を整理する。
- ライセンス監査の承認フロー（担当者・記録場所・頻度）を法務と確認する。
- diff レポートで review 判定となった `qa_text` の用語統一を Phase 3 内で確定させる。

## 参照ドキュメント
- `docs/requirements/16_ludeme_integration.md`
- `docs/requirements/16a_kpi_checklist.md`
- `docs/requirements/16e_poc_plan.md`
- `docs/requirements/14_seed_data_catan_min.md`
