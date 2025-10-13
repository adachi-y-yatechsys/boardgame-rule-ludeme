# Ludeme 導入判断ドラフト

## 目的
- Phase 3 で収集した差分レポートと KPI チェックリストを突合し、Ludeme 語彙の参照導入可否を判断する。
- 粒度・エビデンス・ライセンスの 3 KPI に対するリスクと残課題を明示し、レビュー会議での意思決定材料を提供する。

## 手順
1. `reports/ludeme/diff_report.csv` / `.json` を確認し、KPI 軸ごとのステータスを集計する。
2. `docs/checklists/kpi.md` のチェック項目と整合させ、未完了項目・レビュー待ちを更新する。
3. Phase 3 最終レビューのアジェンダ（`docs/review/phase3_summary.md`）に反映し、承認プロセスとフォローアップを合意する。

## 判定基準
| KPI | 達成状況 | 未解決リスク | 判断 / 次アクション |
| --- | --- | --- | --- |
| 粒度一致度 | `qa_text` 更新1件が **confirmed**（統一訳を反映） | 統一訳「盗賊を移動し、隣接プレイヤーから資源カードを1枚奪取」が今後の差分検知で崩れるリスク | Phase 4 CI に差分検証ジョブを追加し、`reports/ludeme/diff_report.*` で訳語揺れを監視。 |
| エビデンス適合度 | `citation` 追加1件が **confirmed**、`evidence` 差分は **n/a** | 参照 ID の維持管理手順が未定義 | CI 手順に差分検証を組み込み、証跡維持の運用手順を Phase 4 で策定。 |
| ライセンス整合度 | diff レポートで追加・変更なし | 法務承認と監査ログが未更新 | 法務レビューを依頼し、`docs/legal/approval.md` に記録を追記。 |

## 参考
- `reports/ludeme/diff_report.csv` / `reports/ludeme/diff_report.json`
- `docs/checklists/kpi.md`
- Phase 2 CI 手順書（`docs/requirements/16_ludeme_integration.md`）
