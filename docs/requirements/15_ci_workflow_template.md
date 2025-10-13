# CI ワークフローテンプレート（GitHub Actions）
> ここでは **雛形** を提示する。Codex は本テンプレートを `.github/workflows/ci.yml` に反映し、必要に応じて差分ビルド等を追加する。

```yaml
name: CI
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch: {}

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install deps
        run: npm ci

      - name: Validate models (JSON Schema + refs)
        run: npm run validate:models

      - name: Alloy checks (base + series)
        run: npm run check:alloy

      - name: Build QA packages
        run: npm run build

      - name: Validate dist (QA Package Schema)
        run: npm run validate:dist

      - name: Upload dist artifacts
        uses: actions/upload-artifact@v4
        with:
          name: qa-dist
          path: dist/qa

      - name: Upload logs (optional)
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: logs
          path: |
            logs
            tools/.work
```

## ポイント
- **トリガ**: push/pr/手動の3種。保護ブランチ運用を前提に PR での実行が主。
- **キャッシュ**: `actions/setup-node` の npm キャッシュを使用。
- **Artifacts**: `dist/qa` を提出物として常に添付。失敗時でも `logs` を回収。
- **拡張**: 差分ビルド、出典URL検証、CODEOWNERS 連携は Codex タスクで追加。

