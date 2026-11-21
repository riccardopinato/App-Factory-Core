# Language Engine v1.1.1 — targeted audit-driven refinements

Observed from Cooking Anime actual artifact 162 x 5:
- Engine 1.1 reported 148 REVIEW pairs with 190 NUMBER_ANCHOR_REVIEW fields
  and 8 UNIT_ANCHOR_REVIEW fields, plus 29 number-form equivalence hints.
- Valid phrases include Italian 'una o due volte' / English 'once or twice',
  and German compound measurements such as '18-cm-Form'.
- Ingredient type 'Farina 00' translated 'Plain flour' is not automatically
  equivalent; it is a culinary terminology concern, not a missing quantity.

Improvements:
- Detect explicit count-frequency idioms and numeric-unit hyphen compounds
  without broad semantic guessing.
- Emit source/target excerpts, P1/P2 triage priority and distinct codes for
  ingredient flour grades and ambiguous written-number contexts.
- Preserve REVIEW for possible culinary meaning loss; no automatic source
  rewrites or certified translation labels.
- Existing SHA-pinned semantic evidence and stale-draft gates remain unchanged.

All rules are offline, stdlib-only, covered by regression tests.
