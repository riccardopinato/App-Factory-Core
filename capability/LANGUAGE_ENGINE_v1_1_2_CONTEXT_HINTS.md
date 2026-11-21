# Language Engine 1.1.2 — precision-oriented triage

Cooking Anime artifact on Language Engine 1.1.1: 180 REVIEW pairs; 114
WORD_NUMBER_CONTEXT_REVIEW findings with no literal digit on either side.
Examples include nonnumeric grammatical constructions and rephrasings.
Treating every such result as a numeric error makes the Fast Track noisy.

This change:
- Reports purely word-based numeric uncertainty as numericContextHints
  rather than a confirmed issue. The target still remains
  OFFLINE_REVIEW_REQUIRED, NEVER certified for semantic correctness.
- Keeps explicit numeric drift, ingredient grade differences (Farina 00),
  and concrete unit mismatches in REVIEW, with priority and excerpts.
- Limits frequency alias normalization to unambiguous full expressions
  such as una o due volte / once or twice, avoiding accidental numeric
  semantics from isolated adverbs.
- Source-bound SHA256 and HOLD for missing/unsafe translations remain.
No recipe content changes, provider calls, new dependencies or automation of
publishing translations.
