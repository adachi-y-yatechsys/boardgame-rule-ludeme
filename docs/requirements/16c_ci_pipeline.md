# 16c. CI パイプライン（Ludeme 検証）

## 目的
- Catan seed での Ludeme 参照導入に伴い、`validate` → `check:alloy` → `build` → `validate:dist` の基幹ジョブを連続実行できるよう CI 手順を統一する。
- Overlay と Alloy 拡張を任意ジョブとして扱い、PoC で追加した差分レポート生成までを一貫したワークフローとして記録する。

## 手順
1. **ベース検証チェーンを実行する**。
   - `npm run validate:models`
   - `npm run check:alloy`
   - `npm run build`
   - `npm run validate:dist`
2. **Ludeme 専用の任意検証を併走させる**。
   - `npm run validate:ludeme:overlay` : `schemas/overlays/*.overlay.json` を JSON Schema Draft 2020-12 で検証する。
   - `npm run check:alloy:ludeme` : `spec/base.als` と `spec/ludeme_ext.als` を組み合わせ、存在制約を警告レベルで確認する。
3. **差分レポートを生成する**。
   - `npm run report:ludeme:diff -- --series catan --edition 5th`
   - 出力物は `reports/ludeme/diff_report.csv` / `diff_report.json` を起点に、必要に応じて `reports/ludeme/glossary_audit.csv` を更新する。
   - `python -m tools.ludeme_diff.cli verify --report reports/ludeme/diff_report.json --matrix docs/mapping/matrix.csv --glossary docs/glossary/ludeme_terms.csv --output reports/ludeme/diff_verify_results.json --slack-payload reports/ludeme/slack_payload.json --archive-dir reports/ludeme/archive --archive-label <run-id>` を実行し、Glossary 整合を確認する。
   - CLI の結果として `reports/ludeme/diff_verify_results.json` / `slack_payload.json` が生成され、`reports/ludeme/archive/<timestamp>-<run-id>/` にアーカイブされる。
4. **成果物を保存・共有する**。
   - CI では `reports/ludeme/` 配下をアーティファクト化し、失敗時でも `diff_report.*` がレビュー可能な状態を保つ。
   - 手動実行時は `reports/ludeme/archive/` へアーカイブするか、`tools/ludeme_diff/` 系 CLI を使って要約を生成する。
   - `python reports/ludeme/archive/generate_summary.py --count 5 --output reports/ludeme/archive/latest_summary.json` で最新アーカイブ一覧を更新し、共有リンクと突合できるようにする。

## 判定基準
- 4 段階のベース検証チェーンが順番どおりに成功し、Ludeme 導入前と同じ QA 出力を維持していること。
- Overlay / Alloy 拡張ジョブが CI 上で任意実行できるよう手順に記載されていること。
- 差分レポート (`diff_report.*`, `diff_verify_results.json`, `slack_payload.json`, `glossary_audit.csv`) と `reports/ludeme/archive/` の最新アーカイブが同期しており、Phase 2 のレビューで参照できること。

## 参考
- `docs/requirements/05_build_and_ci.md`
- `docs/requirements/15_ci_workflow_template.md`
- `docs/checklists/kpi.md`
- `reports/ludeme/diff_report.csv`
