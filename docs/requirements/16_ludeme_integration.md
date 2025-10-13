# Ludeme 語彙統合の検証計画

> 目的: Digital Ludeme Project / Ludii が提供する**語彙（ludeme）**を、既存の Fact / Variant / Evidence / JSON Schema / Alloy モデルに**参照可能な語彙層**として取り込み、表現力・一貫性・引用性の向上を図る。

## 1. 背景と根拠
- **Ludii** は汎用ゲームシステムであり、ゲーム記述言語（GDL）として**ludeme**と呼ばれる語彙・構文を提供する（Language Reference）。
- 配布物は**非商用・改変不可 (CC BY-NC-ND 4.0)** の条件で公開されている。ただし、**語彙・概念の参照や引用（出典明記）**は適法な範囲で可能と解釈する（文言確認は法務／版元と別途行う）。
- 期待効果: 語彙の**粒度とカバレッジ**を外部研究成果に合わせ、**シリーズ間の一貫性**と**Alloy 検証の明確さ**を高める。

### 参考
- Ludii Portal / Downloads（CC BY-NC-ND 4.0 ライセンス記載）
- Ludii Language Reference（ludeme の定義群）
- “The Ludii Game Description Language is Universal”（表現力の理論的裏付け）

## 2. 適用範囲（Scope）
- **対象**: Series / Edition / Preset / Package の**語彙付与**（tag/enum/型名）。
- **非対象**: Ludii 実装や .lud ファイルの転載・配布、Ludii プレイヤの同梱。

## 3. 評価指標（KPI）
1. **粒度一致度 (Granularity Alignment)**  
   - 定義: Fact/Variant に付与する語彙ブロックが、Ludeme の語彙階層（Move/Board/Piece/Goal/Condition 等）と**1:1 or 1:多**で矛盾なく対応している割合。  
   - 測定: 代表10項目（SETUP/TURN/WIN 主要項目）で**対応表**を作成し、**「完全一致/要派生/不可」**の比率で評価。目標 **完全一致 ≥ 70%**。

2. **エビデンス記述適合度 (Evidence Compatibility)**  
   - 定義: 両者のメタデータ（説明、出典、注釈）が**JSON Schema の `evidence`**、**Alloy の `Evidence` 型**にロスなく写像できる度合い。  
   - 測定: Catan seed の各 Fact/Variant に **`evidence[*].sourceId/page/loc`** が欠落なく保持されること。**Schema/Alloy CI 100% Green**。

3. **ライセンス整合度 (License Compatibility)**  
   - 定義: 本リポジトリの商用運用において、Ludii/Ludeme の**ライセンス条件**に抵触しないこと。  
   - 判定: **非同梱・非二次配布・引用は出典明記**・文言転載は**短い引用に限定**であること。法務チェックの**承認取得**。

## 4. 語彙棚卸し（Ludeme → 本モデル）

| Ludeme（例） | 本モデルの対応 | 備考 |
|---|---|---|
| `game` / `equipment` / `board` / `piece` | **Series / Edition / Sources** | 用語は説明にのみ使用（内部構造は従来通り） |
| `rules` / `moves` / `end` (goal) | **Fact.tag = TURN / RESOLVE / WIN** | 主要タグに対応 |
| `players` (range) | **Variant（人数別 SETUP）** | 3人/4人などの Variant にマップ |
| `option` / `parameter` | **Preset / Variant** | 大会標準・初心者向け等 |
| `metadata` (credits, refs) | **Sources / evidence** | 既存の出典メタで吸収 |

> 方針: **語彙を“付加属性”として付ける**（`fact.ludeme = "end"` など）。**既存 ID/構造は不変**。

## 5. ギャップ分析
- **吸収可**: SETUP/TURN/WIN/RESOLVE の大半、人数・勝利条件・手番基本操作。  
- **派生語彙**: graph-based board 等、Ludeme 固有の抽象構造（必要に応じて `ludemeHint` の補助属性を追加）。  
- **保留**: 同時手番や不完全情報など高度な表現（現行 UI/QA では未使用のため優先度低）。

## 6. PoC（Catan seed 置換）
- `models/catan/5th/edition.json` の **主要 Fact（board_setup / initial_placement / robber_on_seven / victory_condition）** に `ludeme` 属性を追加。  
- **validate:models → check:alloy → build → validate:dist** を現行と同条件で実行。  
- **差分レポート**: 生成 Q&A と citations が一致していること、`evidence` 欄が劣化していないこと。

### 例: 付加属性（案）
```json
{
  "id": "victory_condition",
  "tag": "WIN",
  "text": "勝利点が規定点に達した最初のプレイヤーが勝利。",
  "evidence": [{ "sourceId": "rulebook_jp5_pdf", "page": "TBD" }],
  "ludeme": { "category": "end", "term": "goal", "note": "Win by reaching target score." }
}
```

## 7. CI / スクリプト（追加要件）
- `schemas/overlays/<series>.series.overlay.json` に **`ludeme` フィールド定義（任意）**を追加。  
- `spec/base.als` に **`LudemeTag` の存在制約（任意）**を追加可能（※導入段階では警告レベル）。  
- `tools/report-ludeme-diff`：語彙付与の有無・一致率・欠落率を CSV 出力。

## 8. リスクと軽減策
- **ライセンス**: 非商用・改変不可 → *同梱/転載を避ける*。**語彙参照**は**出典明記＋短い引用**に限定。  
- **メンテ負荷**: Ludeme 更新追従 → *語彙は “補助属性” とし、未定義は許容*。  
- **監修負荷**: 新用語の認知 → *UI には既存タグ表記を維持、語彙は内部メタに限定*。

## 9. アクセプタンス基準（補足）
- Catan seed PoC で **KPI（粒度≥70%、CI 100% Green、法務承認）**を満たす。  
- Q&A 出力の文言・引用ラベルが**現状と完全一致**（語彙導入による可観測な退行なし）。

## 10. 参考文献 / 出典
- Ludii Downloads（ライセンス: CC BY-NC-ND 4.0）  
- Ludii Language Reference（語彙定義）  
- Soemers et al., *The Ludii Game Description Language is Universal*（表現力の裏付け）
