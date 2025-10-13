# 16a. KPI チェックリスト（Ludeme 語彙導入）

## 粒度一致度（Granularity Alignment）
- [ ] 代表 10 項目（SETUP/TURN/WIN/RESOLVE を最低各2件含む）を選定した
- [ ] それぞれに対し `ludeme.category` / `ludeme.term` を暫定割当した
- [ ] 対応結果を「完全一致 / 要派生 / 不可」に分類した
- [ ] 「完全一致」割合が **70% 以上**である
- [ ] 不一致項目に対し UI/UX 影響を記述した

## エビデンス記述適合度（Evidence Compatibility）
- [ ] `evidence[*].sourceId/page/loc` がマッピング後も欠落していない
- [ ] CI（validate:models / check:alloy / build / validate:dist）がすべて Green
- [ ] 差分レポートで Q&A と citations が PoC 前後で一致

## ライセンス整合度（License Compatibility）
- [ ] Ludii/Ludeme 配布物の同梱・改変配布を行っていない
- [ ] 語彙・短い文言の引用には出典明記を行っている
- [ ] 法務レビューの承認を記録した（承認日 / 担当）

## DOR（Definition of Ready）
- [ ] Catan seed の対象 Fact/Variant が 10 項目以上選定済み
- [ ] 追加 `ludeme` 属性の JSON 例が共有済み

## DOD（Definition of Done）
- [ ] KPI 3軸を満たす（粒度≥70%、CI Green、法務承認）
- [ ] ドキュメント（16* 章）が埋まっている
