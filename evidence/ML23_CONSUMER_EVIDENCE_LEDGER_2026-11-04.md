# ML23 — immutable source and consumer evidence ledger
Date: 2026-11-04
Status: E3 Core verified; independent consumer gates pending exact-head completion.
Authority: App Factory Master v27 / Golden Index v28 / Single-Donor Capability Admission.

## Canonical source (immutable)

- Core repository: riccardopinato/App-Factory-Core
- Source commit (40 SHA): ae76e4267b67fe0e913d650d8e89a010dd235a5c
- Source file: reference_engines/lib/src/on_device_algorithms.dart
- Direct unit vectors: reference_engines/test/on_device_algorithms_test.dart
- Dart package: reference_engines/ (pure Dart)
- CI run: https://github.com/riccardopinato/App-Factory-Core/actions/runs/41814145600 (reference-dart SUCCESS)
- Factory validation: https://github.com/riccardopinato/App-Factory-Core/actions/runs/41814145585 (SUCCESS)
- Source introduction: https://github.com/riccardopinato/App-Factory-Core/pull/67
- Admission issue: https://github.com/riccardopinato/App-Factory-Core/issues/68
- Ownership: first-party source from the user's App Factory; no third-party code claimed or external model.
- Dependencies: Dart core library only (dart:math); no cloud, AI weights, native permissions, storage or writes.

## CAP-0152 — local Levenshtein fuzzy reference

Pure behavior: Unicode codepoint token edit distance, cutoff and bounded candidate search, stable ties, validation and hidden/deleted flags.
Core vectors: riunone => riunione stable ID order; caffè exact match; hidden/deleted excluded; duplicate ID, oversized input and oversized candidates rejected; cutoff deterministic.

Notes consumer proposal: https://github.com/riccardopinato/Notes-Ecosistema/pull/56
Base: Notes-Ecosistema main cd3e28f3a22bbd9cd25bf8c6b76b44dc66bdb4f7
Port path: flutter_app/lib/src/domain/on_device_text_reference.dart
Adapter: flutter_app/lib/src/domain/note_local_signals.dart
Production call: flutter_app/lib/src/data/unified_retrieval_service.dart
Tests: flutter_app/test/ml23_local_text_consumer_test.dart
Adaptation: only text classes extracted; native sensor portion omitted; bounded read-only active-note projection; typo results supplement existing canonical lexical/semantic retrieval, not a new search index.
Limitations: caller owns account ACL, text authorization, source revision, visibility; algorithm is codepoint-based, not grapheme-normalized. Only one token query >=4 runes; 5000-note cap; no new persisted index. Existing broader semantic matching remains separate.
Consumer exact-head test: PENDING. E5: NOT YET VERIFIED.

## CAP-0160 — sparse lexical TF-IDF reference

Pure behavior: bounded Unicode tokens, local document frequency, smoothed IDF, deterministic keyword ranking; not a trained embedding or generative model.
Core vectors: camper / batteria ranking, multilingual accented token, custom stopwords, empty corpus and oversized corpus fail-safe.

Notes consumer proposal: same PR #56.
Adapter: flutter_app/lib/src/domain/note_local_signals.dart
UI call: flutter_app/lib/src/screens/editor_screen.dart (canonical tag editor).
Tests: flutter_app/test/ml23_local_text_consumer_test.dart
Adaptation: small multilingual stopword set; proposals exclude already assigned tags; user selects chip, then confirms through the existing editor Save; no auto-writer.
Limits: caller must supply only visible/authorized corpus; suggestions are lexical, not user intent and never an authority to mutate data. Source revision/ACL at final Save remains the canonical writer's responsibility.
Consumer exact-head test: PENDING. E5: NOT YET VERIFIED.

## CAP-0158 — EWMA/hysteresis sensor transition math

Pure behavior: finite input/config guards, bounded alpha/deltas/streak; consecutive rising samples trigger, consecutive low samples clear; baseline updates in quiet state.
Core vectors: 10 -> 11 -> 25 -> 24 triggers, then 20 -> 10 -> 10 clears; NaN and invalid threshold rejected.

Pocket Guard/Pockara consumer proposal: https://github.com/riccardopinato/Pocket-Guard/pull/6
Base: Pocket-Guard main b7b1c74de66e047c32083365b44561e42237b4fc
Kotlin port: app/src/main/java/com/riccardopinato/pocketguard/detection/AdaptiveSignalMath.kt
Production adapter: app/src/main/java/com/riccardopinato/pocketguard/detection/SmartProtectionEngine.kt
Tests: AdaptiveSignalMathTest.kt; SmartProtectionEngineTest.kt
Adaptation: Kotlin translation of the scalar state transition; live protected-session motion samples observed in diagnostic shadow mode; resets on owner verification, forceState or config changes.
Limits: NOT in alarm decision path. No false-positive, OEM, low-power or lifecycle certification. Existing alert behavior remains untouched.
Consumer exact-head test: PENDING. E5 for math consumption: NOT YET VERIFIED; E4 physical: BLOCKED PENDING USER DEVICE.

## Evidence acceptance matrix

| Gate | Core | Notes | Pockara |
|---|---|---|---|
| E1 immutable source | PASS | proposal pinned above | proposal pinned above |
| E3 direct source tests + CI | PASS | exact-head pending | exact-head pending |
| E5 independent production call + tests | not applicable | pending | pending, shadow only |
| Hardware / OEM / battery | not claimed | device UI pending | multi-OEM field matrix pending |
| Store/release certified | not claimed | no | no |

Promotion: keep Golden Index v28 / GOLDEN_REGISTRY.yaml unchanged. Scope any subsequent Golden to demonstrated pure math, NOT NLP model, ACL engine, generic sensor monitoring, Play readiness, power optimization or product-level protection. A separate reviewed, validated Core PR is required for any Golden status change.

## Deferred gates
1. Resolve Notes and Pocket exact-head CI, add URLs and final full head SHAs to this ledger.
2. Validate ACL/account-switch/stale revision at the real Notes call site and canonical save; add multi-locale and 500/5000 benchmark timing (fixture existence is not a timing measurement).
3. Verify Pocket on at least two OEM/device families, including dark pocket, false light/motion spike, aborted extraction, background lifecycle, power sampling and no duplicate listener.
4. Decide if any consumer-bound behavior justifies E5, then create scoped Golden Draft and review promotion separately.
