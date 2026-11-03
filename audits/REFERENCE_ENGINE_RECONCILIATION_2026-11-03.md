# Reference engine evidence reconciliation — 2026-11-03

Factory base at start: daaeb8faf5b7cbe702150e6f94d81eb05e792f98
Master remains v27; Golden Index remains v28; 59 registered entries.

The Golden/Registry wording for four candidates previously said extraction was
still pending, despite real integrated and tested Dart code. This fixes the
documentation to "DRAFT / CANDIDATE — REFERENCE IMPLEMENTED, CONSUMER PENDING",
NOT to CERTIFIED GOLDEN or COPY-READY.

| Engine | Core merged PR | Postmerge proof | Remaining scope |
|---|---|---|---|
| Hybrid Search & Local Rules | #47 | https://github.com/riccardopinato/App-Factory-Core/actions/runs/41558127847 | persistent search/executor, external consumer |
| Explainable Recommendation | #48 | https://github.com/riccardopinato/App-Factory-Core/actions/runs/41558127847 | editorial policy, external consumer |
| Spatial Clustering (radius mode) | #49 | https://github.com/riccardopinato/App-Factory-Core/actions/runs/41578714172 | grid mode, consumer/physical map |
| GPX | #45 | https://github.com/riccardopinato/App-Factory-Core/actions/runs/41578714172 | independent source-using consumer |

Other evidence: CamperBoss GPX donor hardening #29, merged
ae30d08f23aa7e8c835927bc98127f25662d2f6a.
Postmerge https://github.com/riccardopinato/CamperBoss/actions/runs/41596537929 SUCCESS.
It did NOT import the Core GPX engine; hence not E5 independent reuse.

Portable vectors: contracts/engine_reuse_acceptance_v1.json.
Source modules: reference_engines/lib/src.
No rebranding of donor CI as consumer CI. No external/physical verification.
