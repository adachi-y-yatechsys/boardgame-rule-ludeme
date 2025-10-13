// 16g. spec/ludeme_ext.als (minimal, optional)
module ludeme_ext

open util/boolean as bool

sig Fact {
  tag: one Tag
}

abstract sig Tag {}
one sig SETUP, TURN, WIN, RESOLVE extends Tag {}

sig LudemeTag {
  category: one String,
  term: one String
}

sig FactLudeme {
  fact: one Fact,
  ltag: one LudemeTag
}

// Optional advisory constraint: when ludeme used, category/term must be non-empty
pred WellFormedLudeme {
  all fl: FactLudeme | some fl.ltag.category and some fl.ltag.term
}
run {} for 3
