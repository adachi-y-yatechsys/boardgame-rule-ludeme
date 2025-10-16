# Ludeme PoC KPI チェックリスト

## 目次
- [評価観点別チェックリスト](#評価観点別チェックリスト)
- [DOR/DOD トラッキング](#dordod-トラッキング)
- [未解決事項リスト](#未解決事項リスト)
- [参照ドキュメント](#参照ドキュメント)

## 評価観点別チェックリスト

### 粒度一致度（Granularity Alignment）
- **目的**: Seed データの Fact/Variant が Ludeme 語彙で再現可能な粒度で揃っていることを確認する。
- **手順**:
  1. `docs/mapping/matrix.csv` に SETUP/TURN/RESOLVE/WIN/VARIANT の代表例を 10 件以上登録する。
  2. 各行に `ludeme.category` と `ludeme.term` を暫定割り当てし、`mapping_type` で一致度を分類する。
  3. `notes` 欄へ UI/UX 影響や派生理由を記録する。
- **判定基準**:
  - [x] 代表 10 件（SETUP/TURN/WIN/RESOLVE 各 2 件以上）を登録済み（現状: SETUP=3, TURN=2, RESOLVE=3, WIN=2, VARIANT=2）。
  - [x] `mapping_type` を `exact/derived/hold` で記録し、派生理由を `notes` に明示した。
  - [ ] 「完全一致（`exact`）」の割合が 70% 以上（現状: 4/12 = 33%、派生語彙の設計が追加課題）。
- **参考**: `docs/mapping/matrix.csv`

### エビデンス記述適合度（Evidence Compatibility）
- **目的**: ルール参照情報（sourceId/page/loc）がマッピング後も欠落しないことを保証する。
- **手順**:
  1. 各マッピング行の `evidence_source_id` / `page` を Seed モデルのエビデンスと突き合わせる。
  2. `TBD` となっているページ番号の補完計画を `notes` に記述する。
  3. CI で `validate:models` → `check:alloy` → `build` → `validate:dist` を連続実行し、欠落を検出する。
- **判定基準**:
  - [ ] `evidence_source_id/page/loc` 欄に欠落がない（現状: `page` が `TBD` のまま、ルールブック差し戻し待ち）。
  - [ ] CI チェーンが Green で完走（現状: Phase 2 で実装予定、まだ手動確認のみ）。
  - [x] 差分レポートで Q&A と citations が PoC 前後で整合（現状: `qa_text`/`citation` の差分が収束済み）。
- **参考**: `docs/requirements/16e_poc_plan.md`

### ライセンス整合度（License Compatibility）
- **目的**: CC BY-NC-ND 4.0 の制約下で語彙導入を行い、法務監査に耐える状態を作る。
- **手順**:
  1. マッピングで引用する語句を短文化し、`notes` に出典メモを残す。
  2. 監査ログを `docs/legal/approval.md` に記録できるようチェックリストと連動させる。
  3. 定期的に配布物を棚卸しし、Ludii バイナリや `.lud` が混入していないかを確認する。
- **判定基準**:
  - [x] Ludii/Ludeme 配布物を同梱・改変していない（現状: 配布物なし、棚卸し計画は Phase 2 で更新予定）。
  - [ ] `notes` 欄に引用元メモを記録（現状: ルールブック URL の追記が未着手）。
  - [ ] 法務レビューの承認記録を更新（現状: `docs/legal/approval.md` での記録待ち）。
- **参考**: `docs/legal/approval.md`

### 差分レポート集計（最新）

| KPI軸 | diff_report ステータス集計 | リスク/備考 |
| --- | --- | --- |
| 粒度一致度 | `qa_text` 更新1件 = **confirmed** | 派生語彙の定義と CI テンプレート化が Phase 2 の宿題。 |
| エビデンス適合度 | `citation` 追加1件 = **confirmed**／`evidence` 変化なし1件 = **n/a** | ルールブックのページ差し戻しを待ちつつ、CI 手順化を準備。 |
| ライセンス整合度 | 該当差分なし | 出典メモの記載ルールを Phase 1.5 で策定予定。 |

## DOR/DOD トラッキング
- **Definition of Ready (DOR)**
  - [x] Catan seed の対象 Fact/Variant が 10 項目以上選定済み（現状: 12 件登録し、粒度バランスを確保）。
  - [x] 追加 `ludeme` 属性の JSON 例が共有済み（現状: `docs/requirements/16_ludeme_integration.md` にサンプルあり）。
  - [ ] 参照ルールのページ番号が確定（現状: 監修待ち）。
- **Definition of Done (DOD)**
  - [ ] KPI 3軸が基準を満たす（粒度≥70%、CI Green、法務承認）。（現状: 粒度と法務が進行中、CI は Phase 2）。
  - [ ] ドキュメント（16* 章）が最新化され、手順が追記されている（現状: 16 系列は骨子あり、検証手順を追記予定）。

## 未解決事項リスト
- 粒度評価の判定ルールを `mapping_type` 以外にも定義し、CI で測定できる指標に落とし込む。
- エビデンス整合チェックを自動化する CI 手順（Phase 2 で実装予定）を整理する。
- ライセンス監査の承認フロー（担当者・記録場所・頻度）を法務と確認する。
- 差分レポートの `qa_text` 統一訳（盗賊アクション＝移動＋資源カード1枚奪取）が維持されているかを Phase 2 レポートでモニタリングする。

## 参照ドキュメント
- `docs/requirements/16_ludeme_integration.md`
- `docs/requirements/16a_kpi_checklist.md`
- `docs/requirements/16e_poc_plan.md`
- `docs/requirements/14_seed_data_catan_min.md`
