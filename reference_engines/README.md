# Golden Reference Engines v28 — pure Dart harness

Reference package for two independently reusable algorithms. No application,
Flutter widget, database, provider, network or device permission is required.

- `lib/src/gpx.dart`: bounded offline GPX parser/exporter/simplifier.
- `lib/src/civil_date.dart`: Gregorian date-only recurrence and identity.
- `test/`: positive/negative algorithm regression and portable consumer
  vectors from `../contracts/engine_reuse_acceptance_v1.json`.

Run from `reference_engines/`:
```sh
dart pub get
dart analyze --fatal-infos .
dart test
```

## Donors and provenance

GPX reference derived by selective reimplementation of:
- TrailPath@3f44ab37c0881e4315033797c451cec723e23cd2,
  `lib/infrastructure/gpx/xml_gpx_service.dart`.
- CamperBoss@cf4202e25bf3bc630f9cfe5e3823219acfba84b4,
  `lib/core/services/gpx_service.dart`.

Civil date reference derived by selective reimplementation of:
- World-Days@622e5c2f00c08b0905207c6765c9b51e199e706f,
  `lib/domain/recurrence_engine.dart`.
- Agenda-per-Anna@827bb61620960d8867eb03e453d142013aada786,
  `test/v053_recurring_life_engine_test.dart`.

The reference package is a **testable source adapter**, not a claim that all
original app behavior or every GPX extension has been ported. Limitations:
- GPX: no route snapping, no extension passthrough, no file/provider IO,
  maximum 5 MiB / 10k points by default, precision 7 decimal places.
- CivilDate: no timezone scheduler, notifications, persisted recurring series
  or conflict-aware sync. Calendar math only.

## Consumer policy

A consumer may vendor the required narrowly-scoped source with a provenance
header and its OWN exact-head regression tests. This does not require a
shared runtime dependency or force app code to import a GitHub repository.
A different project importing it must implement consumer adapters and test
platform/native behavior separately. These boundaries follow Master v27 and
Golden E3/E5 donor policy.

The `contracts/engine_reuse_acceptance_v1.json` file provides fixture vectors:
only GPX and CivilDate are executed by this harness; Search/Automation remain
unimplemented reference engines.
