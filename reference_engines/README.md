# Golden Reference Engines v28 — pure Dart harness

Reference package for five independently reusable algorithms. No application,
Flutter widget, database, provider, network or device permission is required.

- `lib/src/gpx.dart`: bounded offline GPX parser/exporter/simplifier.
- `lib/src/civil_date.dart`: Gregorian date-only recurrence and identity.
- `lib/src/hybrid_search.dart` and `lib/src/semantic_embeddings.dart`: local lexical + optional deterministic feature-hash retrieval; no neural LLM.
- `lib/src/local_rules.dart`: pure deterministic item mutation proposals; no background execution.
- `test/`: positive/negative algorithm regression and portable consumer
  vectors from `../contracts/engine_reuse_acceptance_v1.json`.

Run from `reference_engines/`:
```sh
dart pub get
dart analyze --fatal-infos .
dart test
```

## Donors and provenance

GPX reference derived by selective reimplementation of:
- TrailPath@3f44ab37c0881e4315033797c451cec723e23cd2,
  `lib/infrastructure/gpx/xml_gpx_service.dart`.
- CamperBoss@cf4202e25bf3bc630f9cfe5e3823219acfba84b4,
  `lib/core/services/gpx_service.dart`.

Civil date reference derived by selective reimplementation of:
- World-Days@622e5c2f00c08b0905207c6765c9b51e199e706f,
  `lib/domain/recurrence_engine.dart`.
- Agenda-per-Anna@827bb61620960d8867eb03e453d142013aada786,
  `test/v053_recurring_life_engine_test.dart`.

The reference package is a **testable source adapter**, not a claim that all
original app behavior or every GPX extension has been ported. Limitations:
- GPX: no route snapping, no extension passthrough, no file/provider IO,
  maximum 5 MiB / 10k points by default, precision 7 decimal places.
- CivilDate: no timezone scheduler, notifications, persisted recurring series
  or conflict-aware sync. Calendar math only.

## Consumer policy

A consumer may vendor the required narrowly-scoped source with a provenance
header and its OWN exact-head regression tests. This does not require a
shared runtime dependency or force app code to import a GitHub repository.
A different project importing it must implement consumer adapters and test
platform/native behavior separately. These boundaries follow Master v27 and
Golden E3/E5 donor policy.

The `contracts/engine_reuse_acceptance_v1.json` file provides fixture vectors:
all 20 GPX, CivilDate, Search and Automation vectors execute against reference sources. Search and automation are not yet integrated in consumer apps.

## 2026-11-03 extension provenance
- Hybrid search exact source embedding donor Notes-Ecosistema@3fd9b0df5ab3b7470c65721b4bad7f3fd8c59e6c `flutter_app/lib/src/domain/semantic_embeddings.dart`, byte-identical blob de96c2dbf0da2c0c4695308efd5b9bbab25b75f5; retrieval adapter inspired by Notes UnifiedRetrievalService and CamperBoss local search, but reimplemented as a pure no-I/O port.
- Local rules reference selectively adapts Notes-Ecosistema `flutter_app/lib/src/domain/workflow_automation.dart`, source-pinned at the same SHA.
- Search security filtering is applied to each canonical result before lexical/semantic scoring. The index identity is a caller-supplied snapshot; no durable index implementation is provided.
- Automation is a pure evaluator. It does NOT certify exactly-once persisted delivery, cross-account permissions, outbox recovery or background platform execution.

- `lib/src/explainable_recommendation.dart`: immutable eligible-only scorer and deterministic per-group diversity cap based on FrameLab and Wonderlog reference behavior; does not check legal rights or publish editorial content itself.

## Grid + deterministic performance fixtures (v28 tranche)
- `SpatialReferenceClustering.clusterGrid` uses zoom-scaled latitude/longitude cells with an anti-meridian seam merge. This is distinct from O(n²) radius transitive grouping; grid is bounded at 10k points and does not claim point clustering within a physical meter radius.
- `SyntheticGeoFixture` generates deterministic uniform, repeated-location, or anti-meridian data. `ReferencePerformanceHarness.measure` verifies output digest across warmup and repetitions, reports p50/p95 and immutable source SHA. These CI-run elapsed times are *not* mobile thermal, fps, battery or provider measurements.

## Infinite Canvas / Ink — bounded foundation only
- `lib/src/canvas_ink.dart`: framework-independent camera transforms, anchor-preserving zoom/pan, bounded ink and sticky-node scene codec, immutable undo/redo history. Derives geometry/ink contracts from Notes-Ecosistema@3fd9b0df5ab3b7470c65721b4bad7f3fd8c59e6c. No Flutter widgets, lasso, full note-link ownership, eraser gestures, stylus input or physical-device tests. These omissions prevent full COPY-READY classification.

## Local Rules transactional port — 2026-11-03
- `LocalRulesReferenceExecutor.execute` proposes and commits deterministic changes via an injected `LocalRuleCommitPort` that MUST atomically store state plus idempotency receipt. Tests simulate replay after a fresh executor/port, concurrent duplicate delivery, permission denial, fingerprint mismatch and failure-before-commit.
- The test port is an in-memory transaction model only. The package intentionally ships NO SQLite/Drift implementation or native worker. No crash-durability or device-background claim without an independent app adapter and evidence.

## Candidate ML23 reusable math — 04/11/2026

- src/on_device_algorithms.dart: bounded Unicode-codepoint Levenshtein and read-only filtered fuzzy token ranking (candidate CAP-0152); corpus-local sparse TF-IDF keyword suggestions (CAP-0160); bounded EWMA+hysteresis upward signal transition (CAP-0158).
- Tests: test/on_device_algorithms_test.dart, deterministic source vectors including hidden/deleted notes, duplicate IDs, Unicode and invalid sensor values.
- Does not perform learned embeddings, TextRank, POS tagging, GPS processing, platform sampling, permission checks, app writes or binary model downloads. Code-point edit distance is NOT grapheme-aware normalization.
- Reference source is a CANDIDATE pending exact-head Dart CI and independent consumer verification. The existing Golden Index/Registry and all DRAFT classifications remain unchanged; adoption requires separate scoped Golden admission.
