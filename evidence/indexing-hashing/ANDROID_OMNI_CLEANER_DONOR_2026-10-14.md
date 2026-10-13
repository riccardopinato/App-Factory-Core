# Android Omni Cleaner — donor provenance for indexing / bounded hashing

Date: 2026-10-14

## Source

- source repository: `riccardopinato/Android-Omni-Cleaner`
- source URL: `https://github.com/riccardopinato/Android-Omni-Cleaner`
- immutable source commit: `aa5f6e9951237fcfafaa1c361c4aa643c439ad63`
- source PR: `#12 step-9-performance-deep-qa`
- source license: **no LICENSE file present at the referenced commit**
- classification: **INTERNAL_DONOR / PATTERN DONOR**
- code copied into App-Factory-Core: **none**
- text copied from donor: **none**
- external dependency introduced in Core: **none**

Because the donor is an internal project without a repository license file, this
record does not treat it as an OSS code donor. The two Golden documents are a
provider-agnostic rewrite/generalization of observed implementation patterns.

## Concepts referenced

Persistent indexing:
- persistent SQLite-backed file catalog;
- scan generations;
- warm snapshot reuse;
- explicit invalidation;
- strong revision binding for reusable derived hashes;
- manual/full reconciliation path;
- destructive operations continue to revalidate real files.

Bounded hashing:
- size prefilter;
- prefix/suffix fingerprint;
- bounded worker count;
- no task-per-file fanout;
- deterministic output ordering;
- persistent sample/full-hash reuse only under trustworthy revision identity;
- physical alias/hard-link collapse before duplicate grouping;
- byte-for-byte final verification.

## Donor files inspected

At `aa5f6e9951237fcfafaa1c361c4aa643c439ad63`:
- `app/src/main/java/com/riccardopinato/omnicleaner/cleaner/PersistentStorageIndex.kt`
- `app/src/main/java/com/riccardopinato/omnicleaner/cleaner/StorageInventoryRepository.kt`
- `app/src/main/java/com/riccardopinato/omnicleaner/cleaner/FileInventoryScanner.kt`
- `app/src/main/java/com/riccardopinato/omnicleaner/cleaner/FileSystemIdentity.kt`
- `app/src/main/java/com/riccardopinato/omnicleaner/cleaner/FileScanner.kt`
- related JVM/instrumentation tests and CI configuration.

## Donor validation evidence

Exact-head `aa5f6e9951237fcfafaa1c361c4aa643c439ad63`:
- Android CI run `38484281905`: **PASS**
- locale resource parity: PASS
- JVM tests: PASS
- debug APK assembly: PASS
- Android instrumentation test sources: compiled on PR
- exact-head development APK release: `fast-apk-aa5f6e995123`

Not yet claimed:
- instrumentation execution on physical device;
- cold/warm benchmark on representative large real library;
- low-end thermal/battery benchmark;
- Store/production certification.

## Golden adaptation

The Golden documents deliberately do **not** copy Android/Kotlin-specific
implementation details as requirements.

Generalized:
- revision-bound cache reuse;
- generation-based reconciliation;
- bounded producer/worker model;
- cancellation/backpressure;
- deterministic grouping;
- alias identity;
- evidence and benchmark requirements.

Retained as DRAFT because:
- one donor only;
- no cross-app reuse yet;
- physical benchmark evidence pending.

## Evidence boundary

This provenance record supports donor reproducibility and conceptual lineage.
It does not promote either Golden beyond DRAFT / NON COPY-READY.
