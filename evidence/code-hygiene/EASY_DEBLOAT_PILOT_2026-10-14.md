# Easy Debloat Pilot — Code Hygiene

Date: 2026-10-14

## Factory baseline

App-Factory-Core:
`e183de8f811873a146eaa78bb1daa2617e11f466`

Resolved:
- Master v26.2 FULL
- Golden Index v13
- Agent Governance v1 CERTIFIED PROCESS
- Code Hygiene v1 COPY-READY PROCESS

## Easy Debloat source truth

Repository:
`riccardopinato/btrader`

The repository is historically a bTrader repository. Easy Debloat was stored
on the dedicated `easydebloat-build` lineage and must not be confused with
bTrader main.

Packed-source baseline:
`10ffcd4e86bb88807703d0fcaa65017a4c16b505`

The source was stored as five base64 tar chunks. It was decoded and materialized
without functional changes first:

`2bebd3e139181fbaa90033af26c528f445027d71`

## Audit truth

No active manual ADB or Wireless ADB privilege implementation existed.
The real privilege path was already:

`ShizukuController -> Shizuku UserService -> /system/bin/sh`

Therefore the pilot did not invent or delete a fake legacy ADB path.

## Feature replacement

Before:
- DebloatRepository owned raw shell composition;
- package-state actions used `&&` chains;
- required state changes and optional helper operations shared one aggregate exit
  status.

After:
- `PackageOperationExecutor` owns the ordered operation plan;
- required and best-effort steps are explicit;
- DebloatRepository delegates package-state operations;
- PackageScanner depends on a narrow `PrivilegedCommandExecutor` contract;
- package validation remains before privileged interpolation;
- obsolete post-enable force-stop removed.

## Bug fixes

### Diagnostic truth

Old ENABLE path:
`pm enable ... && am force-stop ...`

A successful enable could therefore be reported as failure when the later
force-stop failed.

The replacement reports required package-state truth independently from
best-effort process-control.

### Shizuku lifecycle

The sticky binder-received listener can fire immediately when a binder is
already available. The old `start()` also called `refreshAndBind()`
unconditionally, creating a duplicate bind path.

The pilot:
- registers dead/permission listeners before the sticky listener;
- explicit-probes only when the binder is not alive;
- uses one in-flight `binding` gate;
- clears that gate on connect/disconnect/death/failure;
- keeps manual retry explicit.

### Android backup rules

Release lint exposed invalid `domain="cache"` entries in backup XML.
They were removed at the source; no lint baseline or suppression was introduced.

## Regression evidence

Pure Kotlin command-plan harness:
PASS

Covered:
- best-effort force-stop failure does not mask successful disable;
- enable no longer force-stops after the required transition;
- restore stops after install-existing failure;
- final enable failure is surfaced;
- invalid package never reaches privileged shell.

Exact-head:
`32c3660129d85cc12121b68f3d56d8630e1db5f1`

GitHub Actions:
`38483735583` — SUCCESS

Passed:
- Android unit tests;
- assembleDebug;
- assembleRelease;
- lintVitalRelease.

Merged Easy Debloat lineage:
`30277ac9eab8d614c9c0f6bfd04048680a3f0e76`

Exact-head tree:
`ce09b218b7312b0340ba3af66f372d46a4d50bab`

Merged tree:
`ce09b218b7312b0340ba3af66f372d46a4d50bab`

## Safe-retain decisions

Retained intentionally:
- Shizuku API/provider;
- AIDL UserService;
- user-0 package commands;
- best-effort pre-stop for disable/remove;
- QUERY_ALL_PACKAGES pending separate Play-policy review;
- DataStore/history/catalog/UI.

No unrelated bTrader Rust code was refactored.

## Runtime boundary

Physical Shizuku permission, binder and real package-action validation is
**NOT VERIFIED** in this pilot.

This blocks an Easy Debloat native-runtime certification claim, but does not
invalidate the Code Hygiene process evidence because the replacement logic,
regressions and Android build/lint gates are independently verified.

## Promotion conclusion

Code Hygiene now has:
- CamperBoss: dead-code/dependency cleanup + safe retain;
- TrailPath: feature replacement + bug fix + regression suite;
- Easy Debloat: second comparable replacement/bug-fix cleanup on a different
  stack (native Kotlin/Compose), with Android unit/build/lint evidence.

Result:
Eligible for **CERTIFIED PROCESS**.
