# CamperBoss Pilot — Agent Governance / Code Hygiene

Date: 2026-10-13

## Factory baseline

App-Factory-Core:
`a1713e5acc9e157543038bebb4ba83b6d26e5f91`

Resolved:
- Master v26 FULL
- Golden Index v11
- Agent Governance v0.1 DRAFT
- Code Hygiene v0.1 DRAFT

## CamperBoss baseline

Repository:
`riccardopinato/CamperBoss`

Before:
`6c866bf8884b78703401db8ce08dbcf97d3f893c`

Pilot head:
`af8c00ac1710ea958cfd59545eb617f903176221`

Merged main:
`19c2b24cd5164caa9f5178679b8fbc961e7af3ce`

PR:
#26 — Pilot App Factory v26 agent governance and code hygiene

## Findings

Governance drift:
- AGENTS.md relied on an unspecified latest Master/Golden from chat;
- implementation-status documentation still described main as STEP 15/early 16;
- provenance ledger referenced Master v20.

Bounded cleanup:
- removed dead `lib/core/constants/app_strings.dart`;
- removed dead `lib/core/constants/app_radius.dart`;
- removed unused direct dependency `open_route_service: 1.2.7`;
- updated lockfile and provenance.

Correctly retained:
- FakeLocalNotificationService: active test double;
- NoopOfflinePackageInstaller: active default adapter;
- MapEngineV2PreviewScreen: active production widget despite legacy name;
- platform io/stub adapters.

## Automated evidence

Flutter CI run:
`38384769407` — SUCCESS

Passed:
- flutter pub get / lock drift;
- release identity;
- supply-chain/license audit;
- secret scan;
- project SAST;
- provider/trust-boundary audit;
- final static preflight;
- flutter analyze;
- integration contracts;
- full tests + coverage;
- Fastlane immutable-artifact contract.

Release Core Platform Builds run:
`38384769308` — SUCCESS

Passed:
- Web release build;
- Web bundle-size audit;
- Android QA release APK;
- APK hash evidence;
- privacy backup policy.

## Product/runtime truth

This pilot does not promote any existing STEP 16Q device/store/runtime gate.
Those remain governed by CamperBoss Roadmap and Evidence Bundle.

## Governance conclusion

Agent Governance:
- real downstream adoption: PASS;
- authority hierarchy: PASS;
- merge/delta preservation of existing AGENTS: PASS;
- validator/CI evidence: PASS;
- tool-specific bridge drift: N/A because no duplicated/generated bridge existed;
- context increase remained bounded.

Result:
Eligible for COPY-READY PROCESS.

Code Hygiene:
- dead-code/dependency sweep: PASS;
- safe-retain decisions: PASS;
- final validation after cleanup: PASS;
- feature replacement evidence: NOT YET;
- bug-fix cleanup evidence: NOT YET.

Result:
Remain DRAFT / PROCESS CANDIDATE.
