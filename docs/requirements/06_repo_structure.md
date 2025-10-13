```
repo/
  schemas/
    edition-model.schema.json
    qa-package.schema.json
    overlays/<series>.series.overlay.json
  spec/
    base.als
    base_patch_ext.als
    <series>.als
  models/<series>/<edition>/edition.json
  presets/<series>/<edition>/{official,novice,tournament}.json
  dist/qa/<series>/<edition>/<players>/<preset>/<revHash>.json
  tools/   # （実装はCodexタスク。ここでは仕様のみ）
  .github/workflows/ci.yml
  CODEOWNERS
```

