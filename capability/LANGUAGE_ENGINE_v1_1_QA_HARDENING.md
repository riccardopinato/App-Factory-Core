# Language Engine v1.1: lessons from Cooking Anime 162 x 6

The prior audits had 99 REVIEW translation pairs, including several numeric form
differences. Five actual omissions were corrected, leaving 31 numeric warnings
in the independent Cooking Anime structural scan. They include source digits
versus spelled target numerals, plus valid 74 C / 165 F annotations.

Changes:
- Normalize unambiguous number words (2-10) in IT, EN, ES, FR, DE and PT;
  recognize C/F temperature equivalence and retain original values in reports.
- Preserve REVIEW for genuinely changed numbers and explicit unit discrepancies
  (e.g. minutes vs hours). Ambiguous quarter-turn and other idioms remain REVIEW.
- Surface numericFormNormalizationHints as traceable **heuristic evidence**, not
  a pass on culinary accuracy or translation meaning.
- Reject translation drafts if their source text differs from the canonical text.
- Semantic QA v1.0.2 records the SHA256 of its complete normalized input.
  Language Engine requires the matching fingerprint and a complete, duplicate-
  free per-recipe/per-locale matrix before importing the Semantic QA report.
- Existing reports from older Semantic QA engines without that fingerprint are
  intentionally rejected: rebuild the report on an updated pinned engine.

Status: candidate technical capability; no external API, billing, data mutations,
app release or model-based semantic certification. Use exact SHA in consumers.
