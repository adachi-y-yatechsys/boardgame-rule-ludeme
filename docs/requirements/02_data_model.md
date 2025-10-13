## 上位概念
- **Series**（シリーズ）: ボキャブラリ/共通質問テンプレを持つ。
- **Edition Model**（版モデル）: `sources / facts / variants` を保持（版ごとに分離）。
- **Preset**（プリセット）: `enabledVariantSet` の名前付きセット（公式標準/初心者/大会標準）。
- **Package**: `edition + players + preset` を評価した**配信用集合**（最終facts, enabled variants）。

## Fact
- 最小ルール単位。`id`, `tag`（WORLD/SETUP/TURN/RESOLVE/WIN…）, `text`, `evidence[]`。
- `appliesWhen.players` 等の条件可。
- **全てのFactは evidence >= 1 が必須**（出典の存在保証）。

## Variant
- 差分パッチ。`id`, `patch{add/replace/remove}`, `evidence[]`。
- 競合/依存は **Variant間**で定義（初期実装）。  
- （拡張）検証用に `replaces/requires/removes` を導出してAlloyで矛盾検知。

## Sources（出典）
- 版に紐づくカタログ：`id, kind, title, publisher, locator(pdf/url/print), rev, date_published?`。
- **UI表示**は“短いラベル”とページ/アンカーのみ。

## Q&A出力
- 質問テンプレ（シリーズ共通/ゲーム個別）に map → 短文化しプリレンダー。
- 回答は**監修済み文**のみ（丁寧/カジュアル等の**許可された表現バリアント**で切替）。

