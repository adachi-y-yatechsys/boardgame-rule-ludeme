**タイトル:** ボードゲームルール要約プロジェクト 要件まとめ（モノレポ運用）

## 目的
- 版元の説明書・公式サイト・FAQを入力に、**監修済みの固定Q&A（短文スワイプ）**を生成・配信する。
- **内部モデル（facts/variants/evidence）**は秘匿。版元は**最終Q&Aのみ**を確認。
- 品質担保は **JSON Schema（構文/参照）＋ Alloy（論理）** の二段構え。
- **外部語彙（Ludeme Project の語彙）**の導入可否を検証し、モデルの語彙一貫性を高める。

## 前提
- モノレポで全シリーズ・全版を集中管理。
- 監修者からの差し戻しは **自由テキスト（Word赤入れ/メール）**想定。
- 自由質問（将来オプション）は“**既存Q&Aへのマッピングのみ**”。生成的回答はしない。

## 成果物
- **プリレンダー済み Q&A JSON**（短文・出典ラベル付き）を配信/提出。
- 内部：Editionモデル（sources/facts/variants）、プリセット、CI検証、ビルドパイプライン。

## 参照ドキュメント
- 01-project-scope.md（範囲・非対象）
- 02-data-model.md（データモデル/語彙）
- 03-json-schema.md（スキーマ要件）
- 04-alloy-spec.md（論理制約要件）
- 05-build-and-ci.md（ビルドとCI）
- 06-repo-structure.md（ディレクトリ/ブランチ）
- 07-security-and-governance.md（権限/秘匿）
- 08-review-workflow.md（監修差し戻し）
- 09-freeform-search-plan.md（自由質問の導入計画）
- 10-caching-strategy.md（コスト最適化）
- 11-acceptance-criteria.md（受け入れ基準）
- 12-open-questions.md（未決事項）
- 16-ludeme-integration.md（Ludeme語彙統合の検証計画）
- 16f-ci-diff-verification.md（Phase 4 差分検証ジョブ設計メモ）

