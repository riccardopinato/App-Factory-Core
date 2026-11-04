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

## Next work
Implement source provenance adapter in Notes for fuzzy/TF-IDF and one native sensor consumer in Pocket-Guard, each with own CI, privacy and hardware gates before considering E5. Store no user text in telemetry or CI.
