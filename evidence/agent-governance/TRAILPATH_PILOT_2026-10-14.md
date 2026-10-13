# TrailPath Pilot — Agent Governance / Code Hygiene

Date: 2026-10-14

## Factory baseline

App-Factory-Core:
`23c5b0f6b5f02a93e03bb36106f12575a58129d3`

Resolved:
- Master v26.1 FULL
- Golden Index v12
- Agent Governance v1 COPY-READY PROCESS
- Code Hygiene v1 DRAFT / PROCESS CANDIDATE

## TrailPath baseline

Repository:
`riccardopinato/TrailPath`

Canonical post-v1 base:
`feature/v1.1-v1.5 @ 44b95f8cb398cb141938452254c96a20d55b6eea`

Pilot exact head:
`0220a88a867b6d762b103032cf5262e0a0fb0c32`

Merged post-v1 lineage:
`6679b1ef0713e9bf8407e8b07578727e4f73ed2a`

The merged commit tree is identical to the exact-head candidate tree:
`5d81f2b9ca65ab10cd831e26ad7e27b62718abfc`.

PR:
#40 — TrailPath v1.5.22 — App Factory routing hygiene pilot

## Agent Governance findings

- added repository-local `AGENTS.md` as the tool-neutral operating contract;
- deterministic App-Factory-Core resolution and post-v1 product lineage were made explicit;
- review found stale/conflicting CI evidence in README and an ambiguous main-vs-post-v1 lineage statement;
- both documentation findings were corrected before merge;
- no Product Bible/Roadmap/Master authority was replaced;
- no tool-specific duplicated/generated bridge existed, so bridge drift = N/A.

## Code Hygiene — feature replacement

Before:
- snapped remote routing used nested fallback composition;
- fallback behavior and diagnostics were coupled to the wrapper path.

After:
- one ordered `RoutingProviderChain` owns remote snapped provider failover;
- superseded fallback-specific test code was removed;
- intentional local StraightLine routing and Free Smart Trace were retained;
- no unrelated planner decomposition or repository-wide refactor was performed.

## Code Hygiene — bug fix

Root issue:
secondary/final provider failure diagnostics could be hidden behind the original primary failure.

Correction:
- preserve the final provider failure when all snapped providers fail;
- reject unsnapped provider output fail-closed;
- keep `snapToNetwork=false` local and free of remote provider calls.

Regression coverage added for:
- primary provider success;
- secondary provider failover;
- final-error propagation;
- unsnapped provider rejection;
- explicit local routing.

## Exact-head validation

TrailPath CI:
- run number: #844
- run id: `38474177782`
- exact head: `0220a88a867b6d762b103032cf5262e0a0fb0c32`
- final attempt: 2
- conclusion: SUCCESS

Passed:
- formatting;
- flutter analyze;
- flutter test;
- Web Preview build;
- Android ARM64/x86_64 release;
- AAB/size gates;
- live OSM/Valhalla routing-provider smoke;
- Android API 29 release smoke;
- AppLab Android E2E;
- AppLab v1.5 Pro routing;
- upgrade/migration;
- 360x640 / 130% text UX matrix;
- Release Certification Evidence job.

## Hosted-emulator flake handling

The first exact-head UX attempt produced a real transient Android
`TrailPath isn't responding` dialog during Safe Interaction Crawler stress.
The app runtime code had not changed relative to a previously green UX run, and
the same exact head passed the rerun.

The response was intentionally conservative:
- no application workaround was added without a reproducible root cause;
- no runtime assertion was removed;
- the E2E navigation retry was bounded and only re-tapped when the previous Plan state was still visibly active;
- the final exact-head matrix remained fail-closed and passed.

## Promotion conclusion

Agent Governance:
- downstream adoption in CamperBoss: PASS;
- downstream adoption in TrailPath: PASS;
- drift detection/correction on both projects: PASS;
- bounded context + authority hierarchy: PASS;
- tool-specific bridge drift: N/A in both pilots.

Result:
Eligible for CERTIFIED PROCESS.

Code Hygiene:
- dead-code/dependency cleanup evidence: PASS (CamperBoss);
- real feature replacement with superseded path removed: PASS (TrailPath);
- bug fix + regression coverage: PASS (TrailPath);
- intentional-path safe-retain decision: PASS;
- final validation after cleanup: PASS.

Result:
Eligible for COPY-READY PROCESS.
