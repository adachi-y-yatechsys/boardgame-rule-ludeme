# Ludeme Phase 3 ロードマップ草案

## 目的
- Phase 3 のゴールである KPI 判定と導入判断の準備タスクを時系列で整理し、レビューまでの抜け漏れを防ぐ。
- diff レポートで指摘された review 項目を確実にクローズするための段取りを共有する。

## 手順
### マイルストーン
| マイルストーン | 内容 | 目標日 | 依存タスク |
| --- | --- | --- | --- |
| M1: KPI 集計確定 | `docs/checklists/kpi.md` の差分集計を更新し、レビュー対象を確定 | Week 1 | diff レポート解析完了 |
| M2: 用語統一レビュー | `qa_text` review 項目の用語・訳語を決定し、Q&A とマッピングを修正 | Week 2 | M1 完了、用語レビュー会議 |
| M3: 法務承認準備 | ライセンス監査フローを整理し、`docs/legal/approval.md` 更新案を作成 | Week 3 | 法務チームヒアリング |
| M4: Phase 3 最終レビュー | `docs/review/phase3_summary.md` を用いてレビュー会を実施し、導入判断を合意 | Week 4 | M1-M3 の完了報告 |

## 判定基準
### リスクと Mitigation
| リスク | 影響 | Mitigation | 発生トリガー |
| --- | --- | --- | --- |
| 用語統一が遅延する | 粒度一致度 KPI が review のまま確定せず、導入判断が遅れる | Phase 3 レビュー前に Glossary ドラフトを共有し、承認者コメントを 48h 以内に収集 | 用語レビュー会議で合意が得られない場合 |
| 証跡維持手順が未整備 | エビデンス適合度の運用が属人化し、CI で検知漏れが発生 | Phase 4 の CI 設計に差分検証ジョブを追加し、引き継ぎ手順をドキュメント化 | Phase 3 レビューで運用担当が確定しない場合 |
| 法務承認が遅延 | ライセンス整合度の承認が得られず、リリースがブロックされる | 法務チームと週次タッチポイントを設定し、承認テンプレートを事前に共有 | 法務のレビュー枠が確保できない場合 |

## 参考
- `docs/decisions/ludeme_adoption.md`
- `docs/checklists/kpi.md`
- `reports/ludeme/diff_report.csv` / `reports/ludeme/diff_report.json`
