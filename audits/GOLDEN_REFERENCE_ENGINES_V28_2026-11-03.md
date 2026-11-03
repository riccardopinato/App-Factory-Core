# GOLDEN FACTORY v28 — REFERENCE ENGINES
Date: 2026-11-03
Factory baseline: riccardopinato/App-Factory-Core@2d58d23b1f8e0cabe5efe44b83b63ff56ddeb67f
Master: v27 (UNMODIFIED); Index: v27 -> v28; Golden entries: 59 -> 59.

## Implemented artifact — pure Dart reference harness
Repo: riccardopinato/App-Factory-Core
Merge PR: https://github.com/riccardopinato/App-Factory-Core/pull/45
Merged commit: ce3d0c743a0b2cee3ac26fbc72023e479b178837
Exact-source postmerge Dart analyze + tests PASS:
https://github.com/riccardopinato/App-Factory-Core/actions/runs/41553706803
Factory validation postmerge PASS:
https://github.com/riccardopinato/App-Factory-Core/actions/runs/41553706786

Source paths:
- reference_engines/lib/src/gpx.dart (blob 970b0555ab905655be4f6d221522b18cb37cc212)
- reference_engines/lib/src/civil_date.dart (blob bc85a8848dc563ea148ec979f05b1a7bc72816e3)
- reference_engines/lib/golden_reference_engines.dart
- reference_engines/test/gpx_test.dart
- reference_engines/test/civil_date_test.dart
- reference_engines/test/acceptance_vectors_test.dart
- reference_engines/pubspec.yaml
- .github/workflows/reference-engines.yml

The CI runs Dart analyze, full Dart test suite and 10 executable v27 acceptance
vectors (5 GPX, 5 CivilDate). Another 10 search/automation acceptance vectors
exist as specifications but NO runtime reference implementation is claimed.

## GPX reference scope
XML GPX parse/export, namespaced tracks, segments/routes/waypoints, UTC parsing,
WGS84 finite coordinate validation, escape, resource limits and optional
same-segment RDP simplification. XML parser exceptions normalize to a documented
typed GPX error (initial CI caught and fixed a real XmlTagException regression).
Limits: 5 MiB / 10k points default. Extensions, provider routing, app-level
atomic import and low-end device memory outside validated scope.
Status: DRAFT — REFERENCE IMPLEMENTED, CONSUMER PENDING.
A source-tested reference is not the same as a used/verified app feature.

## CivilDate reference scope and World Days pilot
Source-derived from World-Days and Anna's Diary donors, not invented calendar
policy. Typed Gregorian CivilDate, explicit monthly/leap overflow policies,
nth/last weekday, last day, cross-year spans, unresolved authority rules and
stable occurrence identity. Does not own notifications, timezone scheduling,
data sync, user-owned store state or app native release.

Consumer PR: https://github.com/riccardopinato/World-Days/pull/38
Consumer merged main SHA: 474fdc405217bf05ab28bd250b2e613c86e0506e
Exact PR head: 4d5e4c8ff218a729e62f060f5dcd9422d90a10cb
Consumer full Development checks (Flutter analyze, all tests, Web build) PASS:
https://github.com/riccardopinato/World-Days/actions/runs/41554690827

Source: lib/domain/golden_civil_date.dart is byte-identical to Core reference.
Real app integration: lib/domain/recurrence_engine.dart delegates dates, nth
and last weekday, and month-end while retaining public World Days API and
observance identity. New parity test:
test/domain/golden_civil_reference_adapter_test.dart.

Important evidence boundary: World Days was ALSO an original donor; this
proves reference extraction/reintegration but is NOT independent E5 reusable
consumer evidence. Certified Golden requires further independent integration.
COPY-READY status covers the pure Dart calendar behavior and documented adapter
only, not store/play/native notification certification.

## Reproducibility hardening of consumer
Initial consumer PR failed at pubspec.lock, before any analysis/tests, due 8
transitive dependency upgrades required by the currently pinned Flutter 3.47.3
toolchain. Locked versions+SHA hashes were reproduced exactly from actual
CI diff, including stable YAML SHA formatting, not opportunistically upgraded.
The existing CI gate still checks git diff --exit-code -- pubspec.lock.
No new app permission, billing feature, account, external provider or migration
is introduced by Golden integration. Billing provider QA is separate from CI.

## Validation gates
- Core GitHub Action pure Dart reference engine CI on integrated exact SHA.
- Factory validator version 7 plus engine harvest structure/vector validator.
- Full consumer Flutter PR CI exact tested head.
- Golden Registry/Index file/path equality, alias SHA/parity and 59 entries.
- App main native device/Google Play gate remains independent (do not claim).

## Next use
1. New app imports only required CivilDate source with provenance and tests.
2. A non-donor app integrates CivilDate; record new E5 evidence separately.
3. Integrate GPX into a non-donor app using a parse/export adapter with test
   and app-level staging; then consider COPY-READY.
4. Hybrid Search and Local Rules remain v27 DRAFT for future reference engines.
