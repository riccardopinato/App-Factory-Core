# GBRAIN_OP_TRAILPATH_2026_11_03 — Operational memory

DERIVED SECONDARY MEMORY; AS-OF 2026-11-03; source-inspected. Re-read repository, code and latest CI before asserting a routing issue fixed on device.

Repo `riccardopinato/TrailPath`, main SHA **3f44ab37c0881e4315033797c451cec723e23cd2**.
- README: https://github.com/riccardopinato/TrailPath/blob/3f44ab37c0881e4315033797c451cec723e23cd2/README.md
- Roadmap: https://github.com/riccardopinato/TrailPath/blob/3f44ab37c0881e4315033797c451cec723e23cd2/docs/ROADMAP.md

Current declared milestone: **Flutter v0.9.15 Release Candidate & Production Readiness, build 27**. v1.0 production rollout still separately planned; do not say published. Code paths and README describe: MapLibre live map, touch and freehand route planning, provider-backed OSM foot/bike snapping and constrained retries, elevation/GPX, track recording and crash recovery, navigation and TTS/haptics, offline map regions and availability reconciliation, safety checks, Flutter Android CI and release-mode AppLab Android E2E.

Critical invariant: failed network routing must remain visibly FAILED; never silently save a straight-line fallback as a road route. Snap geometry and waypoint intent are separated, incremental edits preserve partial routing, Undo is a coherent operation; no invented GPS accuracy or offline readiness. A CI routing test/Android emulator PASS is not verified foot/bike navigation on a physical phone, especially with poor signal or no network. The README states the public routing endpoint is suitable for development/validation; provider-neutral production routing remains a gate.

Prioritize source+device discrepancy investigations by reproducer, versionCode, source SHA and network/offline context before assuming known historical issues still exist. Future provider or offline style requires legal, ToS/licensing and quota validation. GitHub is authority, GBrain only remembers the risk and checks.
