# Python Factory Performance QA v1 — capability candidate

**Owner:** App-Factory-Core. **State:** implementation candidate, not yet Golden or cross-app certified.
**Factory baseline:** `43e9c6cd83fe162d9979c8ca9ff73d3e6c3d4ac6`, Master v27 / Golden Index v30.
**Reference:** `golden/governance/GOLDEN_PERFORMANCE_REGRESSION_FIXTURES_v1_DRAFT.txt`.

## Purpose
Improve correctness and throughput of App Factory **development and testing** without putting Python in Android or Flutter runtime. This tool generates byte-verifiable synthetic file collections for local QA and compares source-pinned benchmark series under strict hardware/fixture/mode/integrity comparability. Python standard library only; no APIs, model calls, credentials, app data, provider billing, or user-content scans.

## Execute

```bash
python3 reference_engines/performance_qa/factory_performance_qa.py fixture --output /tmp/omni-qa-demo-unique --files 2000 --duplicate-pairs 10 --seed 19
python3 reference_engines/performance_qa/factory_performance_qa.py verify --input /tmp/omni-qa-demo-unique
python3 -m unittest discover -s tests -p 'test_factory_performance_qa.py' -v
```

The destination **must not exist**; it will never be removed or overwritten. Every file name begins `synthetic_`. The manifest encodes generator version, seed, count, total bytes, full SHA-256 and exact duplicate-family count. Default budget 64 MiB; hard limits 100,000 files and 256 MiB. The tool rejects wrong bytes, unexpected/missing/symlink entries, malformed manifest, over-budget requests and an existing target. Fixture records contain no private user data. File count remains operator-bounded: generating 100k files is **not** recommended as a default CI step.

## Comparable evidence protocol

JSONL: **one independently measured iteration per line**, with required fields:

```json
{"schema_version":1,"fixture_id":"fixture-unchanged","device":"Xiaomi M2101K6G","environment":"physical","api_level":33,"mode":"cold","file_count":88352,"rows_reused":88351,"rows_replaced":1,"integrity_digest":"sha256:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee","source_sha":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","file_rows_ms":9840}
```

The example above is a *shape only*, not measured Factory evidence: a matched candidate series does not yet exist. Each series must have at least **3** records with the **same** full 40-character Git source SHA, fixture, device, API, mode, file count, reused/replaced count and full 64-hex SHA-256 integrity digest. Baseline and candidate may use different source SHAs but must match all other identity fields. Median comparisons are restricted to the requested phase `file_rows_ms`, `scan_ms`, `wall_ms` or `peak_bytes`.

```bash
python3 reference_engines/performance_qa/factory_performance_qa.py compare \
  --baseline baseline.jsonl --candidate candidate.jsonl --metric file_rows_ms \
  --min-runs 3 --max-regression-pct 5 --report r1-candidate-report.json
```

- `BLOCKED` / exit 2 for incomplete, mixed, corrupted or incomparable evidence. Existing reports are never overwritten.
- `REVIEW_REGRESSION` for a median worse by more than the policy threshold.
- `PHYSICAL_REPLAY_REQUIRED` for emulator-only series, even when numerically faster.
- `CANDIDATE_NO_CERTIFICATION` for physically comparable series that meet the nonregression policy. It is **not** a release approval or a battery/thermal guarantee.
- Every result carries `certification=NOT_CERTIFIED`. Conservative gate semantics prevent CI numbers being mistaken for an OEM or Play release certificate.

## App ownership and adoption
- Core owns and tests the Python engine. Golden status does not change merely because Core CI is green.
- Consumer app pins the exact **merged Core commit SHA**, generates a small fixture and independently verifies its native scanner/SQLite results against the manifest. No runtime Python, permission changes, user-file mutation or automatic merge.
- For Android Omni Cleaner, use this as the R0/R1 physical performance evidence parser once **matched same-device runs** have been collected; the existing R1 PR #39 remains DRAFT until that gate passes.
- To promote the Golden, require at least one independent consumer and repeatable machine-readable outputs, then update the relevant registry/index through a separate reviewed admission.
