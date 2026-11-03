# GPX E5 limited independent consumer — Wonderlog read-only preview

Date: 2026-11-03
Factory baseline: `riccardopinato/App-Factory-Core@1b67dbe47d2bddfc415a9925fbd1965560576b21`
Golden id: `gpx_interoperability_engine`
Golden status: DRAFT / CANDIDATE (E5 LIMITED READ-ONLY PREVIEW CONSUMER VERIFIED)

## Source provenance
- Canonical reference: `App-Factory-Core/reference_engines/lib/src/gpx.dart` at `9adf94ed73e17b88806bbf4ef1d0d976ba244ff4`
- Consumer: `Wonderlog/flutter/lib/features/gpx/domain/gpx_reference.dart` at `439a24e02952b351bb9c1f76528575ec1830e3f1`
- Both have identical Git blob SHA `970b0555ab905655be4f6d221522b18cb37cc212` (independently compared through GitHub).
- Consumer adapter: `flutter/lib/features/gpx/domain/gpx_preview_service.dart`.
- Product callsite: `flutter/lib/features/journeys/presentation/journey_detail_page.dart` -> `GpxPreviewPage`.
- Consumer tests: `flutter/test/gpx_preview_test.dart`.

## Immutable evidence
- [Wonderlog PR #22](https://github.com/riccardopinato/Wonderlog/pull/22) merged by squash as `5c3fe1c626104fb7c80d57de6a7871b968ee499a`.
- [Exact-head Flutter Foundation / verify PASS](https://github.com/riccardopinato/Wonderlog/actions/runs/41616436051)
- [Exact-head Apple iOS + macOS build gate PASS](https://github.com/riccardopinato/Wonderlog/actions/runs/41616436017)
- Original PR head: `439a24e02952b351bb9c1f76528575ec1830e3f1`.
- Postmerge jobs were launched but their results were not yet known at time of authoring: [Flutter](https://github.com/riccardopinato/Wonderlog/actions/runs/41619659329), [Web](https://github.com/riccardopinato/Wonderlog/actions/runs/41619659481), [Apple](https://github.com/riccardopinato/Wonderlog/actions/runs/41619659397). Must be checked before claiming postmerge green.

## Proven limited E5 boundary
- User can select a local `.gpx` file from a Journey Detail UI action, validate size (5 MiB cap), strict UTF-8 and GPX structure and see track, segment, route, waypoint and point summaries.
- No user-data writes, journey mutation, map matching, provider/network call or persistent import.
- The integrated parser also exposes export/simplification functions, but these are not an independently proven consumer product feature in this PR.
- Not certified: full GPX import/export/round-trip storage workflow, physical native file picker behavior, device memory/performance and exporter compatibility.
- Global Golden remains DRAFT. Only this narrow consumer evidence reaches E5; no broad CERTIFIED GOLDEN or Store Ready status.

## Promotion policy
Do not widen the status unless independent integration, relevant tests and physical/provider gates for the proposed expanded scope have been recorded separately.
