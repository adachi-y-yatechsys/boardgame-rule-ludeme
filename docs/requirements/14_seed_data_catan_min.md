# 最小シードデータ（Catan 5th, ja）
> **目的**: Codex が end-to-end を最短で Green にするための**検証用データ**。
> 実装時は `models/` と `presets/` に配置。本文は短縮版（監修提出用ではない）。

## models/catan/5th/edition.json（最小）
```json
{
  "gameId": "catan_base",
  "edition": "5th_japanese",
  "seriesId": "catan_series",
  "sources": [
    {
      "id": "rulebook_jp5_pdf",
      "kind": "rulebook",
      "title": "カタン スタンダード 5版 ルールブック",
      "publisher": "GP",
      "language": "ja",
      "locator": { "type": "pdf", "url": "https://www.gp-inc.jp/assets/rule/catan_standard_manual1_web.pdf" },
      "rev": 1
    },
    {
      "id": "official_rules_web",
      "kind": "website",
      "title": "カタン公式ルールページ",
      "publisher": "Catan Japan / GP",
      "language": "ja",
      "locator": { "type": "url", "url": "https://catan.jp/guide/" },
      "rev": 1
    }
  ],
  "facts": [
    {
      "id": "board_setup",
      "tag": "SETUP",
      "text": "六角タイルをランダムに配置し、数字チップを並べる。",
      "evidence": [{ "sourceId": "rulebook_jp5_pdf", "page": "TBD" }]
    },
    {
      "id": "initial_placement",
      "tag": "SETUP",
      "text": "初期配置は順番に開拓地と道を置き、逆順でもう一度置く。",
      "evidence": [{ "sourceId": "rulebook_jp5_pdf", "page": "TBD" }]
    },
    {
      "id": "turn_roll",
      "tag": "TURN",
      "text": "自分の番の開始時に2個のサイコロを振る。",
      "evidence": [{ "sourceId": "rulebook_jp5_pdf", "page": "TBD" }]
    },
    {
      "id": "turn_production",
      "tag": "TURN",
      "text": "出目の土地から隣接する開拓地/都市へ資源が配られる。",
      "evidence": [{ "sourceId": "rulebook_jp5_pdf", "page": "TBD" }]
    },
    {
      "id": "robber_on_seven",
      "tag": "RESOLVE",
      "text": "7が出たら盗賊を移動し、隣接プレイヤーから資源を1枚奪う。",
      "evidence": [{ "sourceId": "rulebook_jp5_pdf", "page": "TBD" }]
    },
    {
      "id": "victory_condition",
      "tag": "WIN",
      "text": "勝利点が10に到達したプレイヤーが勝つ。",
      "evidence": [{ "sourceId": "rulebook_jp5_pdf", "page": "TBD" }]
    },
    {
      "id": "players_3_tile_removal",
      "tag": "SETUP",
      "text": "3人は六角タイルを2枚外して17枚にする。",
      "evidence": [{ "sourceId": "rulebook_jp5_pdf", "page": "TBD" }]
    }
  ],
  "variants": [
    {
      "id": "base_novice",
      "evidence": [{ "sourceId": "official_rules_web" }],
      "patch": {
        "replace": [
          {
            "target": "robber_on_seven",
            "text": "7が出たら盗賊を移動。資源を奪うかは任意。",
            "evidence": [{ "sourceId": "official_rules_web" }]
          }
        ]
      }
    },
    {
      "id": "friendly_robber",
      "evidence": [{ "sourceId": "official_rules_web" }],
      "patch": {
        "replace": [
          {
            "target": "robber_on_seven",
            "text": "7が出たら盗賊を移動。得点3未満の相手からは奪わない。",
            "evidence": [{ "sourceId": "official_rules_web" }]
          }
        ]
      }
    }
  ]
}
```

## presets/catan/5th/official.json
```json
{ "enabledVariantSet": [] }
```

## presets/catan/5th/novice.json
```json
{ "enabledVariantSet": ["base_novice"] }
```

## presets/catan/5th/tournament.json
```json
{ "enabledVariantSet": ["friendly_robber"] }
```

## シードの利用条件（CIが通るために）
- `schemas/edition-model.schema.json`／`schemas/overlays/catan.series.overlay.json`／`spec/*.als` が配置済み。
- `TBD` ページ番号は **一時的に許容**（Schema 側で `string|null`）。後続で差し替え可能。
- Alloy シリーズ制約（catan.als）側で **必須IDのちょうど1件** を検査する想定。

