# Ludeme Phase 3 ロードマップ草案

## 目的
- Phase 3 のゴールである KPI 判定と導入判断の準備タスクを時系列で整理し、レビューまでの抜け漏れを防ぐ。
- diff レポートで指摘された review 項目を確実にクローズするための段取りを共有する。
- 用語レビュー会議がどのような会議体なのかを明確にし、参加メンバーとアウトプットの期待値を揃える。

## 手順
### マイルストーン
| マイルストーン | 内容 | 目標日 | 依存タスク |
| --- | --- | --- | --- |
| M1: KPI 集計確定 | `docs/checklists/kpi.md` の差分集計を更新し、レビュー対象を確定 | Week 1 | diff レポート解析完了 |
| M2: 用語統一レビュー | `qa_text` review 項目の用語・訳語を決定し、Q&A とマッピングを修正 | Week 2（2024-04-16 10:00-11:00 JST 会議） | M1 完了、用語レビュー会議 |
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

## 用語レビュー会議（qa_text Terminology Review）

### 会議の概要
- 参加者: 依頼者（PM/QA 兼任）、ChatGPT（@codex、CI/翻訳支援）。現状スタッフが 2 名のみのため、役割は上記で兼務する。
- 入力資料: `reports/ludeme/diff_report.*`、`docs/mapping/matrix.csv`、翻訳ガイドライン（BGG#CatanRulebook2020 抜粋）。
- 成果物: 統一訳の決裁結果、影響ファイルの更新オーナー、Phase 4 PoC backlog への差分検知タスク追加。
- 決裁範囲: `qa_text` を含むレビュー項目全般（訳語・メッセージ・差分検知トリガー）。
- 実施方法: Codex スレッド（このリポジトリの Issue/コメント欄）上で非同期に議論し、必要事項を完了させる。

### 目的
- `qa_text` に関連する訳語を「盗賊を移動し、隣接プレイヤーから資源カードを1枚奪取する」で統一し、PoC 全体でブレなく運用できる状態を確認する。
- Phase 4 の CI で訳語揺れを検知するための要件とトリガーを明文化し、開発・レビュー双方の合意を得る。

### Codex 内での進め方（日本語による補足説明）
- **会話の場**: 物理会議は行わず、本 Codex スレッド上で非同期にコメントを重ねる。必要に応じてメンションで相互にレビューを依頼する。
- **役割の切り替え**: 依頼者は PR 起票者兼 QA リード、ChatGPT は CI/翻訳支援を兼ねる想定であり、コメント内で「どの役割で判断したか」を明示する。
- **決裁の記録方法**: スレッドで合意した内容は、そのまま議事メモとして `docs/review/phase3_summary.md` に転記し、訳語更新や CI 追加タスクのコミット ID を残す。
- **フォローアップ**: 合意後 24 時間以内に差分検知タスクを Phase 4 backlog に追記し、進捗確認は Codex の同スレッドを再利用する。

### 手順
1. 会議前日までに `reports/ludeme/diff_report.*` と `docs/mapping/matrix.csv` を共有し、訳語差分の有無を確認する（Codex スレッドで URL/コミットを提示）。
2. スレッド上で翻訳方針と参照元（BGG#CatanRulebook2020）を再確認し、統一訳を決裁する。
3. 決裁後に `docs/checklists/kpi.md` と `docs/decisions/ludeme_adoption.md` の該当箇所を更新し、CI 差分検証ジョブへの要求をレビューする。
4. スレッドのやり取りをもとに Phase 4 PoC backlog の担当者と締切を合意し、議事録を `docs/review/phase3_summary.md` に追記する。

#### スケジュール
| 日付 | 時間 (JST) | 内容 | 担当 | 備考 |
| --- | --- | --- | --- | --- |
| 2024-04-15 | 18:00-18:30 | 事前資料レビュー（diff レポート確認） | QA リード（依頼者） | Codex スレッドで確認ログを共有 |
| 2024-04-16 | 10:00-11:00 | 用語レビュー会議（アジェンダ 1-4） | プロジェクトマネージャー（依頼者） & ChatGPT | Codex スレッド内で即時決裁・議事メモ作成 |
| 2024-04-17 | 12:00-12:30 | フォローアップ（CI 要件・バックログ確認） | CI エンジニア（ChatGPT） | 未決事項を Codex コメントでクローズ |

### 判定基準
- 会議内で統一訳「盗賊を移動し、隣接プレイヤーから資源カードを1枚奪取」が合意され、関連ドキュメントに反映されていること。
- フォローアップで Phase 4 差分検証ジョブの要件（検知対象フィールド・通知方法）が backlog に追加されていること。
- Codex スレッド上のやり取りを 24 時間以内に `docs/review/phase3_summary.md` へ記録し、アクションアイテムを明確化していること。

### 参考
- `reports/ludeme/diff_report.csv` / `reports/ludeme/diff_report.json`
- `docs/checklists/kpi.md`
- `docs/decisions/ludeme_adoption.md`
- `docs/review/phase3_summary.md`
