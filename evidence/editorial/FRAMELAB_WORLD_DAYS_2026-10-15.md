# Versioned Editorial Catalog — multi-app donor evidence

Date: 2026-10-15

## FrameLab donor
Repository: riccardopinato/app-fotografia
Main: e7538d7dfc484f81f37a8e4363cd56a5b742e804

Evidence inspected:
- EDITORIAL_PIPELINE.md
- editorial package/import/bootstrap code
- step_9b multilingual catalog tests

Demonstrates format/package/content versioning, stable IDs, complete locales,
source/license/rights/assets, deterministic validation, transactional import,
same-version no-op, downgrade rejection, rollback, user-state preservation,
install cache and multilingual FTS/filter/pagination.

## World Days donor
Repository: riccardopinato/World-Days
Main: b44ceeafa95e6add4d561ab658377ab25ecf7cc4

Demonstrates canonical facts separate from editorial prose, source-policy and
review date, REVIEWED/REVIEWED_TRANSLATION, locale packs + English fallback,
canonical related IDs and deterministic editorial validation.

Current World Days main:
- Development checks #127 PASS
- Web Preview #21 PASS

## Boundary
Two real donors justify extraction, not automatic certification of the
generalized Golden.
