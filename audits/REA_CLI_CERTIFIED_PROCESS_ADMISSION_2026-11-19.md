# REA CLI process certified admission — v31 (2026-11-19)

**Decision:** Scoped `CERTIFIED PROCESS` for repeatable, authorized read-only static software intelligence; **not** `CERTIFIED GOLDEN` of REA source or output.

## Distinct independent evidence

| Harness | Proven target | Execution | Boundaries |
|---|---|---|---|
| AppLab | Official public Deskland Preview v0.1.3 Windows installer & managed host | [REA CLI PASS #44615407360](https://github.com/riccardopinato/AppLab/actions/runs/44615407360), 43/43 published hashes, 48 extracted payload files, x86 installer vs x64 managed host | Source-only user historical Deskland-Setup.exe not analyzed; no Windows runtime |
| AppLab Flutter | Public Flutter Gallery v2.9.2 compiled APK | [REA Flutter build/AOT PASS #44626932001](https://github.com/riccardopinato/AppLab/actions/runs/44626932001) under PR #238 merged `b8bfeb0765451adc95eda15f0c6d6abf5e10639f` | Public fixture, not app AOT or source reconstruction |
| Independent Omni Cleaner | Actual locally built own debug APK from `riccardopinato/Android-Omni-Cleaner@b594adc670bce482d0768638648196d92a3b8eaf`, SHA256 `b2cb75cd332f1261ba5bfee69c47c994fd8acc0d64df88886be81c32fa14e977` | [Actual REA/JADX PASS #44626294217](https://github.com/riccardopinato/Android-Omni-Cleaner/actions/runs/44626294217) and [PR #44 exact-head checks #44627485559 PASS](https://github.com/riccardopinato/Android-Omni-Cleaner/actions/runs/44627485559), PR merged | Static manifest/DEX metadata only; app cleaning and device behavior not executed |

## Negative and recovery coverage

- REA adapter tests reject wrong artifact hash, wrong engine version, ZIP/symlink errors, unsupported commands and immutable evidence collisions.
- Independent Android consumer uses real REA `identify-flutter-build` as a negative control on a Kotlin native APK and tests deliberately mismatched SHA refusal before analysis.
- Initial [Omni run #44625530368](https://github.com/riccardopinato/Android-Omni-Cleaner/actions/runs/44625530368) failed due to unavailable JADX prerequisite. Subsequent successful run pins/verifies the independent JAR SHA `6e5eacf500b64292bfb73c49797c1958f6ee44646e43e868039ae7feb573ff75`, requiring Java 21. This failure stays in the record.

## Scope and no-inference controls

**CERTIFIED:** reproducible research procedure across distinct project-owning harnesses; rights/source SHA, target checksum, bounded static CLI inspection, negative cases, raw evidence provenance and strict research-only output.

**NOT CERTIFIED:** REA as universal reverse-engineer, product code donor, decompilation correctness, every APK/desktop tool family or architecture, E5 transferable implementation of third-party features, PE runtime, physical Android/Play, installer security or virus clearance. `UNVALIDATED_EXTERNAL_OUTPUT` remains the default for unreviewed REA output. No release or app-source changes are implied.

**Factory baseline:** `App-Factory-Core@cac009697970490e45f9aaa9e7e7634016607273` (Master v27, Index v30). This PR promotes Index to v31 without changing Master. The original external REA project stays an E1 research source, license MIT; target licenses remain separately governed (Deskland GPL-3.0).

## Conditions for broader promotion

Additional independent consumers and exact-head, negative, provider/physical controls must prove each wider command family, not silently inherit this process status. A new `CERTIFIED GOLDEN` capability requires separate E5 admission with implemented reusable functionality and consumer evidence.
