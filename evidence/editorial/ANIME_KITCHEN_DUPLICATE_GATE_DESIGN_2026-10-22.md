# In Cucina con gli Anime — Duplicate / Similarity Review Gate design origin

Date: 2026-10-22
Repository: riccardopinato/In-Cucina-con-gli-Anime
F1 merged main: ab87c0d008bf2a9e826973873484f37ac9ca2215

## Implemented evidence available

F1 provides:
- stable recipe/ingredient/step IDs;
- JSON-only versioned runtime catalog;
- structured canonical data separated from localized text;
- deterministic catalog validator;
- locale fallback;
- fail-closed runtime loader;
- CI/analyze/test/Web/Android green on merged main.

## F2 design extracted

The planned authoring/import pipeline requires detection of two recipe inputs that
may come from different books/sources but represent the same or near-identical
culinary content.

The proposed gate compares normalized structured dimensions instead of title/text
alone and returns explainable duplicate/variant review candidates.

## Boundary

The Duplicate / Similarity Review Gate itself is NOT IMPLEMENTED in the donor at
the time of this extraction.

This evidence justifies a DESIGN-ONLY process candidate, not COPY-READY or
CERTIFIED status.
