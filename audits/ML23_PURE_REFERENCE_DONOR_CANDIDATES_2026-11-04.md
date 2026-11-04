# ML23 pure reference donor candidate — 2026-11-04

Pinned App Factory baseline: 6cbb3449ba375496029bee93b45bc9f939dcd794. Master 27 / Golden Index 28.

Reference package adds three narrow deterministic source-only implementations: CAP-0152 bounded fuzzy search, CAP-0160 TF-IDF keyword suggestions and CAP-0158 signal filtering with hysteresis.

## Evidence and ownership
- SOURCE: reference_engines/lib/src/on_device_algorithms.dart; tests reference_engines/test/on_device_algorithms_test.dart.
- No third-party package added; existing Dart math and RegExp only. No app repository or stored user data altered.
- No trained semantic model; search remains lexical; no graph clustering or TextRank implemented by this change.
- No runtime sensor access, calibration, hardware anti-theft guarantee or foreground-service logic.
- Source checks required: Dart analyze and tests on exact PR head; after successful CI, may evaluate E3 donor admission strictly for mathematical functions.
- E4 device sensor sampling and E5 independent consumer remain PENDING. No registry change or Golden COPY-READY promotion in this PR.

## Downstream fan-out
- CAP-0152 -> CAP-0015 search, CAP-0032 hybrid retrieval, CAP-0148 Smart Inbox candidate shortlist.
- CAP-0160 -> CAP-0124 topic discovery, CAP-0151 future TextRank, CAP-0148 tag suggestion review.
- CAP-0158 -> CAP-0057 alarm/pocket engine, CAP-0062 focus sensor conditions; app-local hardware adapters required.

## Actual E3 direct-source gate — 04/11/2026

Source pinned after PR #67 squash: ae76e4267b67fe0e913d650d8e89a010dd235a5c
- Core reference-dart and Factory validate checks SUCCESS on the exact merged source: https://github.com/riccardopinato/App-Factory-Core/commit/ae76e4267b67fe0e913d650d8e89a010dd235a5c/checks
- E3 donor admission: CAP-0152 Levenshtein/fuzzy (bounded), CAP-0160 lexical TF-IDF and CAP-0158 EWMA/hysteresis (pure sample math).
- NO Golden INDEX/REGISTRY promotion beyond the existing scoped donor governance catalog; E5 cross-app consumer pending and E4 physical/sensor OEM pending.
- This corrects the prior snapshot section which said E3 was only potential: tests now ran and passed. It does not convert E0 app proposals into delivered features.

## Next work
Implement source provenance adapter in Notes for fuzzy/TF-IDF and one native sensor consumer in Pocket-Guard, each with own CI, privacy and hardware gates before considering E5. Store no user text in telemetry or CI.
