# CamperBoss Pilot — AppLab QA / Certification Adapter

Date: 2026-10-14

## Purpose

Register the second independent external App Factory integration required to
promote the AppLab QA / Certification Adapter from COPY-READY PROCESS to
CERTIFIED PROCESS.

This evidence certifies the reusable process. It does not certify CamperBoss as
physically verified, Store Ready or production released.

## Factory / verifier baseline

App-Factory-Core baseline at pilot start:
`b0d406223e3469323b02b8ef39cf10ad85012357`

Resolved:
- Master v26.4 FULL;
- Golden Index v16;
- AppLab QA / Certification Adapter: COPY-READY PROCESS.

Trusted AppLab verifier:
`931c124dbb1a36d43842db5b60bd5f04843e5330`

## CamperBoss identity

Repository:
`riccardopinato/CamperBoss`

Pre-pilot main:
`19c2b24cd5164caa9f5178679b8fbc961e7af3ce`

Pilot PR:
#27 — Pilot Golden AppLab QA on CamperBoss

Exact pilot head:
`58b83ef630fdb04e0cc6f34d27e03b20ec191787`

Merged main commit:
`cf4202e25bf3bc630f9cfe5e3823219acfba84b4`

No product behavior was changed by the pilot.

## Client contract

The pilot binds:
- Flutter 3.47.6;
- Java 21;
- package `com.camperboss.camperboss`;
- ARM64 split release QA APK;
- existing STEP 16Q Maestro flow `.maestro/applab-release-core-final.yaml`;
- AppLab analysis mode `full`;
- immutable AppLab verifier SHA;
- cache verification disabled;
- release artifact publication disabled.

The project adapter declares real-device validation as required for:
- gps;
- background;
- camera;
- scanner;
- notifications;
- storage;
- file_picker;
- play_delivery.

These requirements can make certification stricter and cannot be satisfied by
emulator evidence alone.

## Exact-head CI / build evidence

Exact pilot source:
`58b83ef630fdb04e0cc6f34d27e03b20ec191787`

- Flutter CI #473 / `38566087656`: PASS.
- Release Core Platform Builds #363 / `38566087778`: PASS.
- Web release: PASS.
- Android QA release APK: PASS.
- AppLab Production Gate #1 / `38566088778`.

Trusted build contract:
- repository: `riccardopinato/CamperBoss`;
- resolved source SHA: `58b83ef630fdb04e0cc6f34d27e03b20ec191787`;
- package: `com.camperboss.camperboss`;
- version: `0.2.2 (2018)`;
- APK SHA-256: `3d14d922b3cfca867fb9ac9c3fbc90d9d143c01b51856321928caa2d98e0cda3`;
- APK bytes: `49045248`;
- same exact APK bytes verified: true;
- analyze: PASS;
- unit tests: PASS;
- build: PASS.

## First trusted-runtime attempt — retained FAIL evidence

The first trusted-runtime attempt on AppLab run `38566088778` failed only at
the final System UI Lab.

Observed System Lab finding:
`runtime_unhealthy: application process is not running`

The same failed attempt also recorded:
- Maestro full launch/navigation/relaunch flow: PASS;
- process survived background cycle;
- force-stop restart succeeded and returned a new PID;
- no app FATAL EXCEPTION found;
- no app ANR found;
- hosted-emulator graphics context errors immediately before the final lab FAIL.

Release Reality correctly stopped at:
- ARTIFACT_BUILT: PASS;
- TRUSTED_RUNTIME_VERIFIED: FAIL;
- PHYSICAL_DEVICE_VERIFIED: BLOCKED;
- later distribution/store/production stages: NOT_VERIFIED.

The failure was not converted to PASS and is intentionally preserved.

## Exact-source failed-job rerun

Only the failed trusted-verification job was rerun. Source, build contract and
APK bytes remained unchanged.

Final evidence:
- source SHA: `58b83ef630fdb04e0cc6f34d27e03b20ec191787`;
- APK SHA-256: `3d14d922b3cfca867fb9ac9c3fbc90d9d143c01b51856321928caa2d98e0cda3`;
- AppLab run: `38566088778`;
- AppLab evidence artifact id: `11897715291`;
- evidence artifact digest: `sha256:d6385b1376539c3b06402032f9dccd848bba2a8acc8c36da2ac86654fa3592cd`;
- aggregate result: PASS;
- runtime result: PASS;
- Maestro: PASS;
- System UI Lab: PASS;
- network lab: PASS;
- persistence lab: PASS;
- configuration lab: PASS;
- background lab: PASS;
- storage lab: PASS;
- trusted evidence manifest produced;
- trusted evidence manifest binds repository/source/package/workflow/verifier.

Final System Lab:
- result: PASS;
- errors: 0;
- warnings: 0;
- force-stop restart: PASS.

Historical context:
CamperBoss had already passed prior AppLab runtime checks on Android API 29 and
API 35 on 09/10/2026 for version 0.2.2+18. That historical evidence supports,
but does not replace, the exact-head Golden pilot above.

## Release Reality boundary

Final successful rerun reports:
- IMPLEMENTED: PASS;
- STATICALLY_CHECKED: PASS;
- TESTED: PASS;
- CI_GREEN: PASS;
- ARTIFACT_BUILT: PASS;
- TRUSTED_RUNTIME_VERIFIED: PASS;
- PHYSICAL_DEVICE_VERIFIED: BLOCKED;
- DISTRIBUTION_VERIFIED: NOT_VERIFIED;
- STORE_READY: NOT_VERIFIED;
- PRODUCTION_RELEASED: NOT_VERIFIED.

This is the expected fail-closed boundary.

CamperBoss STEP 16Q therefore remains BLOCKED by its external physical/store/Web
acceptance requirements. The AppLab process certification must not be read as a
CamperBoss production-release certification.

## Promotion conclusion

Comparable external integrations now exist for:
1. Anna's Diary;
2. CamperBoss.

Across the two projects the process has demonstrated:
- immutable source binding;
- package binding;
- exact APK SHA binding;
- trusted verifier identity;
- trusted evidence manifest;
- real Maestro/runtime execution;
- failure preservation;
- BLOCKED preservation for physical requirements;
- separation of runtime PASS from store/distribution claims.

Result:
Eligible for **CERTIFIED PROCESS**.
