# OpenSpec Shadow Mode — opt-in deep SHA/byte pilot · 27 November 2026

**Status: consumer PR validation ongoing; Core deep adapter merged and postmerge CI PASS.**

## Exact source

- Factory source and 18 adversarial deep tests: [Core PR #142](https://github.com/riccardopinato/App-Factory-Core/pull/142), main `8a5034483a4b0574907012903894fa39ebeb1f51`, [postmerge CI SUCCESS](https://github.com/riccardopinato/App-Factory-Core/actions/runs/46000089488).
- [Omni pilot PR #83](https://github.com/riccardopinato/Android-Omni-Cleaner/pull/83): only an existing PR workflow changed. A temporary branch-only deep `75:77,39:77` test was executed; the final PR SHA `548254028b2c9262ada2c5eea66a4e6bf59c4784` has the temporary override **removed**, so the default is lightweight and deep comparisons require explicit manual input.
- [Anna pilot PR #378](https://github.com/riccardopinato/Agenda-per-Anna/pull/378): identical opt-in manual capability with lightweight default, no deep test forced.

## Real runtime of the GitHub READ-ONLY review scanner

| Run | Outcome | GET requests | Response bytes | Scanner elapsed |
|---|---|---:|---:|---:|
| [Omni initial attempt](https://github.com/riccardopinato/Android-Omni-Cleaner/actions/runs/46000245997) | **INCOMPLETE**, PR #77 moved during snapshot | N/A | N/A | N/A |
| [Omni rerun, deep pair selection](https://github.com/riccardopinato/Android-Omni-Cleaner/actions/runs/46000245997) | **SUCCESS**, immutable heads | 35 | 4,945,756 | 15.558 s |
| [Omni final default scan](https://github.com/riccardopinato/Android-Omni-Cleaner/actions/runs/46000499991) | **SUCCESS**, deep OFF | 30 | 2,093,866 | 15.984 s |
| [Anna default scan](https://github.com/riccardopinato/Agenda-per-Anna/actions/runs/46000253698) | **SUCCESS**, deep OFF | 17 | 1,264,836 | 9.650 s |

Because GitHub network conditions and PR content differ, the two Omni durations are **not a reliable performance gain/loss comparison**, and the tests do not establish token savings or human time saved.

## SHA-pinned pair findings

| Omni PRs | Git ancestry | Shared paths | Byte-identical blobs | Different blobs |
|---|---|---:|---:|---:|
| #75 / #77 | PR #75 commit is ancestor of #77 commit | 63 | 40 | 23 |
| #39 / #77 | Distinct/diverged commit histories | 9 | 8 | **1** |

The single differing #39/#77 shared file is `app/src/main/java/com/riccardopinato/omnicleaner/cleaner/StorageInventoryRepository.kt`. This is a source review priority, **not an identified functional regression**.

Only **2 of the 20** Omni overlapping pairs were examined at blob/ancestry depth. All other pairs remain unexamined at that level. Anna's 3 overlap pairs were not deep-reviewed in this pilot. Data is from GitHub source snapshots, **not** tests on user devices or proof of business requirements. No PR rebase, automatic merge, comment, Product Bible modification or app release occurred.

## Deployment and next gate

Core is merged/CI green. Omni #83 and Anna #378 are pending their complete exact-head app CI and merge, followed by postmerge CI. Record actual states before certifying consumer integration. Preserve all existing app-specific release/physical/owner gates. No Golden promotion, new scheduler or global rollout.
