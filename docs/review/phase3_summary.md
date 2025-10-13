# Phase 3 最終レビューサマリ

## 目的
- Phase 3 の成果物（KPI 集計・導入判断案・ロードマップ）をレビューする際の共通フォーマットと観点を提示する。
- PR と会議体で確認すべき未決事項とフォローアップタスクを明文化し、承認プロセスを迅速化する。

## 手順
1. 下記テンプレートを用いて PR 説明を作成し、レビュー依頼時に貼り付ける。
2. レビュー会議前に `reports/ludeme/diff_report.*` と KPI チェックリストの更新内容を事前確認する。
3. 会議ではテンプレートの「未決事項」「次アクション」を起点にディスカッションを進め、決定事項を記録する。

### PR 説明テンプレート
```
## Summary
- Ludeme Phase 3 evaluation highlights
- Key risks & mitigations

## Referenced Files
- [ ] docs/checklists/kpi.md (KPI status updates)
- [ ] docs/decisions/ludeme_adoption.md (adoption decision draft)
- [ ] docs/roadmap/ludeme_phase3.md (phase roadmap)
- [ ] reports/ludeme/diff_report.csv / diff_report.json (evidence)

## Outstanding Questions
- [ ] Terminology alignment for qa_text (review status)
- [ ] Legal approval timeline confirmation

## Next Actions
- Assign owners for mitigation tasks
- Schedule Phase 4 CI design kickoff
```

## 判定基準
- 粒度一致度: `qa_text` の用語統一が完了し、チェックリストで review がクローズされていること。
- エビデンス適合度: 差分レポートの `citation` / `evidence` が最新 CI で再現されること。
- ライセンス整合度: 法務承認の記録方法と監査頻度が合意されていること。
- ロードマップ妥当性: マイルストーン、リスク、Mitigation が Phase 3 段階の責務と一致していること。

## 参考
### フォローアップ TODO
- diff レポート review 項目の解消後、KPI チェックリストを再更新する。
- 法務レビュー依頼と承認記録のテンプレートを共有し、承認日を追跡する。
- Phase 4 CI 設計ミーティングの議事録テンプレートを準備する。

### 参照資料
- `docs/checklists/kpi.md`
- `docs/decisions/ludeme_adoption.md`
- `docs/roadmap/ludeme_phase3.md`
- `reports/ludeme/diff_report.csv` / `reports/ludeme/diff_report.json`
