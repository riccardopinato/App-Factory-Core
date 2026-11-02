# Exact-source CI — TrailPath and FrameLab — 2026-11-02
Factory baseline at test start:
riccardopinato/App-Factory-Core@95b08d9777330998bb8be7b802155200fc6ee0b2.
Master v27; Golden Index v25; single-donor policy E3.

## TrailPath
- Original repository source SHA:
  3f44ab37c0881e4315033797c451cec723e23cd2.
- Ephemeral PR: https://github.com/riccardopinato/TrailPath/pull/42
- Workflow head (workflow YAML only):
  6be4ba3be606dfd56dbe692954bd8ed2e7012451.
- CI: https://github.com/riccardopinato/TrailPath/actions/runs/41536514653
- Explicit runner checkout of original SHA + SHA assertion: PASS.
- Flutter version 3.47.5, pub get, Drift generated code: PASS.
- Flutter analyze: PASS.
- Targeted geo, battery mode, routing/fallback, navigation, elevation tests:
  PASS.
- Flutter test (entire suite): PASS.
- Workflow: SUCCESS.
- The normal broader PR TrailPath CI is independent, not used to claim
  physical routing correctness.

## FrameLab
- Original repository source SHA:
  e7538d7dfc484f81f37a8e4363cd56a5b742e804.
- Ephemeral PR: https://github.com/riccardopinato/app-fotografia/pull/16
- Workflow head (workflow YAML only):
  0d94a7ff06789da1f7d08b2fa0516047b5bb1c85.
- CI: https://github.com/riccardopinato/app-fotografia/actions/runs/41536521211
- Explicit runner checkout of original SHA + SHA assertion: PASS.
- Flutter 3.47.5, pub get: PASS.
- Flutter analyze: PASS.
- Targeted Step 9A/9B/9D editorial + Step 6 recommendation tests: PASS.
- Flutter test (entire suite): PASS.
- Workflow: SUCCESS.

## Promotion policy
Old "source tests exist, source-CI not proven" candidates can now be
registered as **CERTIFIED DONOR** for scoped tested Dart behaviors only.
Do NOT promote live TrailPath road routing/gesture/GPS, published editorial
rights/correctness or actual on-device platform runtime.
Real provider/device/Play/human editorial gates remain open.
No app production code was changed. Only ephemeral workflow QA branches.
