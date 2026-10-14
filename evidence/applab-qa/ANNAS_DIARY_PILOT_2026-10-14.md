# Anna's Diary Pilot — AppLab QA / Certification Adapter

Date: 2026-10-14

## Factory baseline

App-Factory-Core:
`03406ef5e511dfc580b67967c67a11ab58e20141`

Resolved:
- Master v26.3 FULL;
- Golden Index v15;
- AppLab QA / Certification Adapter v1 DRAFT / PROCESS CANDIDATE.

## AppLab verifier baseline

Repository:
`riccardopinato/AppLab`

Hardened verifier merged by PR #110:
`931c124dbb1a36d43842db5b60bd5f04843e5330`

The pilot exposed and fixed one AppLab failure-path defect:
when build-contract validation failed before effective-mode resolution, the finalizer
lost the requested analysis mode and added secondary evidence noise.

PR #110 preserved the requested mode without converting failures into PASS.

All AppLab #110 canonical gates passed:
- AppLab CI;
- CodeQL;
- Repository Governance Audit;
- Live Emulator Browser E2E;
- Emulator Self Test;
- True Autonomous App Review v5.3.5;
- Canonical Runtime Fixture Build.

## Anna's Diary target

Repository:
`riccardopinato/Agenda-per-Anna`

Pre-pilot baseline:
`f30bd347954d397859b77e431b7725e9d3bb4b6a`

Pilot PR:
#103 — Pilot Golden AppLab QA on Anna's Diary

Final FULL source SHA verified before integrated-tree replay:
`4d7da8974e2dc3cfa475bbf4d600ea4ed044bc89`

Integrated merge-test SHA:
`1425ab64ae4440a10228d397444eea1883ec371a`

## Fail-closed canary

Canary source SHA:
`1a24841ce625797f38bcb8b5e037f33aa1e7b38c`

AppLab Production Gate:
run #652 / `38527684391`

Intentional mutation:
- wrong package id supplied to the trusted verifier.

Observed result:
- FAIL;
- `Declared package id does not match APK package id`.

Conclusion:
package/application identity is fail-closed and target-authored configuration
cannot override the APK identity.

## Certification boundary probe

Source SHA:
`0f43469f921eacf8709ad6e99a87195790130d98`

AppLab Production Gate:
run #658 / `38546895821`

Observed:
- build contract PASS;
- trusted runtime PASS;
- Maestro PASS;
- repository/SHA/package/APK evidence materialized;
- aggregate certification result did not promote to PASS because release/physical
  requirements were incomplete.

Conclusion:
runtime PASS is not silently upgraded to release certification.

## Final FULL trusted-runtime pilot

Source SHA:
`4d7da8974e2dc3cfa475bbf4d600ea4ed044bc89`

AppLab Production Gate:
run #667 / `38551989501` — SUCCESS

Trusted verifier:
`931c124dbb1a36d43842db5b60bd5f04843e5330`

Bound identity:
- package: `com.riccardopinato.agenda_per_anna`;
- version: `1.0.0-rc.1 (2110)`;
- APK SHA-256: `7878f9aa84c31fd6b9a3f6bf06aec8818cc22532e0c9bec0531803354abd5fb6`;
- source SHA: `4d7da8974e2dc3cfa475bbf4d600ea4ed044bc89`;
- workflow run: `38551989501`;
- analysis mode: `full`.

Observed runtime evidence:
- aggregate result: PASS;
- runtime result: PASS;
- Maestro: PASS;
- analyze/test/build: PASS;
- network/offline lab: PASS;
- persistence/restart lab: PASS;
- configuration/lifecycle lab: PASS;
- background/doze/recovery lab: PASS;
- system lab: PASS;
- trusted evidence manifest produced;
- release-reality record produced.

Advisory/non-blocking observations remained evidence rather than being hidden:
- visual QA/journey warnings;
- performance warnings;
- resource-pressure/storage warnings;
- visual/upgrade baseline not yet established.

## Integrated-tree final verification and merge

Exact integrated merge-test source SHA:
`1425ab64ae4440a10228d397444eea1883ec371a`

AppLab Production Gate:
run #668 / `38558260017` — SUCCESS

Trusted verifier:
`931c124dbb1a36d43842db5b60bd5f04843e5330`

Bound identity:
- package: `com.riccardopinato.agenda_per_anna`;
- version: `1.0.0-rc.1 (2110)`;
- APK SHA-256: `fdbfdf7f50337fd26c95587d63fc9deb00464bc7e4c327be0f6694daa413f165`;
- source SHA: `1425ab64ae4440a10228d397444eea1883ec371a`;
- workflow run: `38558260017`;
- analysis mode: `full`.

Observed:
- aggregate result: PASS;
- runtime result: PASS;
- Maestro: PASS;
- exact APK bytes verified;
- trusted runtime level: PASS;
- physical-device level: BLOCKED as required;
- distribution/store/production: NOT_VERIFIED.

Anna's Diary PR #103 was then merged to `main` at:
`f929a1f48989d48eb8c6a3d75f53a16b5bae297f`.

This integrated-tree run is the strongest final pilot evidence. The earlier #667
run remains useful as pre-integration evidence.

## Physical-validation boundary

Anna now provides `applab.project.json` with:

`physical_validation.required=true`

Required capabilities:
- biometrics;
- keystore;
- notifications;
- storage;
- file_picker;
- billing;
- play_delivery;
- cross_app.

The final Release Reality record correctly reports:
- TRUSTED_RUNTIME_VERIFIED: PASS;
- PHYSICAL_DEVICE_VERIFIED: BLOCKED;
- DISTRIBUTION_VERIFIED: NOT_VERIFIED;
- STORE_READY: NOT_VERIFIED;
- PRODUCTION_RELEASED: NOT_VERIFIED.

This boundary is intentional and is a promotion requirement, not a defect.

## Client contract changes

Anna's Diary now:
- pins AppLab to an immutable merged verifier SHA;
- grants only the additional `actions: read` permission required by the reusable runner;
- uses planner-safe build-command syntax;
- uses `analysis_mode: full` for the normal PR/runtime gate;
- declares real-device requirements in the canonical AppLab project adapter;
- locks the integration contract with repository tests.

No product behavior was changed by the pilot.

## Promotion conclusion

Golden AppLab QA / Certification Adapter:
- one real external Flutter integration: PASS;
- immutable source binding: PASS;
- artifact SHA binding: PASS;
- package binding: PASS;
- trusted evidence manifest: PASS;
- runtime journey: PASS;
- log/crash evidence: PASS;
- failure detection: PASS;
- BLOCKED preserved instead of converted to PASS: PASS;
- physical-device requirement preserved: PASS;
- second independent project integration: PENDING.

Result:
Eligible for **COPY-READY PROCESS**.

A second stable external project integration with comparable evidence is still
required before **CERTIFIED PROCESS**.
