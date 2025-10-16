# AGENTS.md — Agent Runbook for `boardgame-rule-ludeme`

本ドキュメントは、GitHub 上でエージェント（例: `@codex`）にタスクを依頼し、ドキュメント整備・PoC・CI 検証・レポーティングを安全かつ再現性高く進めるための運用方針を定義します。

---

## 1. 目的と範囲
- **目的**: Ludeme 語彙を既存ルールモデルへ**非破壊で参照導入**し、KPI（粒度一致・エビデンス適合・ライセンス整合）に基づいて検証を自動化する。
- **対象**: `docs/` の要件/チェックリスト/マッピング、`schemas/overlays`、`spec/*.als`、`reports/` の生成と更新。
- **非対象**: Ludii 実装/バイナリの配布、`.lud` の転載、機密/秘密情報の取り扱い。

---

## 2. ロールと権限
- **@codex（自動エージェント）**
  - 役割: ドキュメント整備、チェックリスト作成、CSV マッピング更新、軽微なスクリプト雛形の提案、PR 作成。
  - 権限: ドキュメント編集・PR 作成まで（**main への直接 push 禁止**）。
  - 出力責務: 変更点のサマリ、根拠（参照ファイル/章）、未決事項の TODO 化。
- **メンテナ**
  - 役割: 仕様の承認、CI 結果の確認、法務/版元との調整、PR マージ。

---

## 3. 依頼の基本原則（Ground Rules）
- **最小 context** を渡す（対象フォルダ/章、KPI、受け入れ基準）。
- **生成系は PR 経由**（直接コミット不可）。
- **引用は短く＋出典明記**（ライセンス: CC BY-NC-ND 4.0 準拠。転載禁止箇所は自前要約）。
- **不確実点は質問させる**（Issue スレッド上で Q&A）。
- **秘密情報を投げない**（鍵・認証情報・非公開 PDF 等は渡さない）。

---

## 4. リポジトリ構成（エージェントが触る主対象）
```
docs/
  README.md
  checklists/
    kpi.md
  mapping/
    matrix.csv
  legal/
    approval.md (法務承認の記録; 人間が記入)
schemas/
  overlays/
    16f_schema_overlay.json (ludeme 補助属性の Overlay)
spec/
  base.als
  ludeme_ext.als
reports/
  ludeme/
    (エージェントが生成する差分や CI サマリ)
.github/
  ISSUE_TEMPLATE/
    ludeme-poc.yml
  pull_request_template.md
AGENTS.md (本書)
```

---

## 5. ワークフロー（Phase）
- **Phase 1: Checklist & Mapping**（`docs/requirements/16e_poc_plan.md` 手順1-2）
  - 目的: KPI チェックリストと Catan seed 10件の仮マッピングを作成。
  - 成果物: `docs/checklists/kpi.md`、`docs/mapping/matrix.csv`、PR。
- **Phase 2: CI Integration**（`docs/requirements/16e_poc_plan.md` 手順3-4）
  - 目的: validate → alloy → build → validate:dist + overlay 検証の自動化。
  - 成果物: `reports/ludeme/*.csv|json`、CI 結果の要約、PR。
- **Phase 3: レポート & 導入判断**（`docs/requirements/16e_poc_plan.md` 手順5）
  - 目的: KPI 判定、リスク/メンテ負荷、段階導入案の提示。
  - 成果物: `docs/` 追記、最終レビュー用 PR。

### Phase 進捗チェックリスト
- [ ] Phase 1: Checklist & Mapping 完了
  - [ ] `docs/checklists/kpi.md` に KPI 3軸の記述と DOR/DOD を反映した
  - [ ] `docs/mapping/matrix.csv` に 10 件以上を登録し `notes` へ出典/理由を追記した
  - [ ] PR "Ludeme PoC/phase-1: checklist & mapping" を作成した
- [ ] Phase 2: CI Integration 完了
  - [ ] validate → alloy → build → validate:dist の手順を `docs/requirements` 系へ追記した
  - [ ] `reports/ludeme/` に差分レポート（Q&A / citations / evidence）を出力した
  - [ ] PR "Ludeme PoC/phase-2: CI integration & reports" を作成した
- [ ] Phase 3: レポート & 導入判断 完了
  - [ ] KPI 3軸の判定結果とリスク/次アクションを `docs/` に記録した
  - [ ] 法務承認 (`docs/legal/approval.md`) を更新し、導入判断の PR を作成した

---

## 6. 依頼テンプレ（Issue/コメントで貼る）
**初回呼びかけ**
```
@codex 次のタスクを順に進めてください：

1) docs/ の章立てを走査し、Ludeme 導入に必要な項目の不足を洗い出して checklists/kpi.md を更新
2) Catan seed の Fact/Variant を 10 件抽出し、docs/mapping/matrix.csv に (ludeme.category/term) を仮割当
3) 上記の変更を含む PR を作成（タイトル: "Ludeme PoC/phase-1: checklist & mapping"）

受け入れ基準:
- kpi.md に KPI 3軸の記述と DOR/DOD が反映されている
- matrix.csv に 10 件以上の行が追加されている
- 不明点/前提はこの Issue スレッドで質問があること
```
**CI 連携（Phase 2）**
```
@codex 次を実施：
- overlay/schema/alloy の検証コマンドを整理し、docs に手順を追記
- 差分レポート（Q&A/citations/evidence 一致）の CSV を reports/ludeme に出力
- PR 作成: "Ludeme PoC/phase-2: CI integration & reports"
```

---

## 7. 出力スタイルと品質基準
- **PR 説明**: 要約 / 変更点 / 参照ファイル / 未決事項 / 次アクション。
- **CSV（matrix.csv）**: 既存ヘッダを保持。`mapping_type` は `exact|derived|hold` を使用。
- **ドキュメント**: 章内で「目的→手順→判定基準→参考」を統一。
- **KPI 判定**: 粒度一致 ≥ 70%、CI Green、法務承認（`docs/legal/approval.md` に記録）。

---

## 8. ライセンスと法務ガード
- Ludii/Ludeme: **CC BY-NC-ND 4.0**。**同梱・改変配布禁止**。引用は**短く**＆**出典明記**。
- 長文転載や .lud 記述は不可。必要箇所は**自前要約**で置き換える。
- 法務承認は人間レビューで `docs/legal/approval.md` に記録。

---

## 9. トラブルシュート
- **エージェントが迷子**: 対象フォルダ/ファイルを明示し、受け入れ基準を再掲。
- **反映漏れ**: PR のファイル差分に期待パスが含まれるか確認。含まれない場合はコメントで再実行依頼。
- **用語不整合**: `docs/mapping/matrix.csv` に `notes` で差分理由を記録し、次回で収束。

---

## 10. バージョニングと責任
- すべてのエージェント変更は **PR 経由**でレビュー/承認。
- `main` は常時デプロイ可能な状態を維持。PoC は `ludeme-integration` ブランチ上で行い、段階導入は PR で合流。
- CODEOWNERS/Reviewer ルールは `.github/CODEOWNERS` にて別途管理（任意）。
