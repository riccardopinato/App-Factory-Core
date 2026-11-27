# OpenSpec Shadow Mode — audit corrective evidence, 27 November 2026

Status: Core corrective code and both consumer workflows MERGED; all source/postmerge CI SUCCESS. Real manual workflow_dispatch executed by owner and rerun PASSED with verified artifact integrity.

## Source and controls

App Factory Core PR #144 and #145 merged. Core main source SHA: 3e3056ffb7444a5d37f1279a2a25783366a0d98c.
Postmerge Core CI: https://github.com/riccardopinato/App-Factory-Core/actions/runs/46010932724

57 source regression tests PASS: 20 FAST, 24 deep, 13 audit security and provenance.

- P1: Markdown/HTML escaping of untrusted PR filenames and Spec Lite keys before stdout or step summary; control characters rendered as escapes, not raw GitHub runner workflow command lines. Python invalid-escape warnings removed.
- P1: each deep pair contains two exact full PR SHA commits and every overlapping changed path with blob SHA, Git mode and missing status; final default-branch and all-open-PR identity checks after all tree reads.
- P1: pinned actions/upload-artifact emits JSON, Markdown and SHA256 checksums with 30-day retention; even INCOMPLETE scans provide recoverable error evidence. No automatic PR actions.
- P2: rename-origin previous_filename aliases improve path-intersection detection without double counting; Git file mode changes distinguished from identical blob contents; genuine source Spec Lite v1 fixtures and previous-delta conflicts covered by adversarial unit tests. Unmapped requirements remain UNMAPPED and all source-declared proposals are untrusted.
- P2: complete collection retained, indexed in-memory PR lookups and SHA-based tree cache for each run, hard 500 GET limit. No stale cross-run cache or background agent.
- P1 manual workflow_dispatch: real owner-triggered workflow_dispatch run #46014830454 on Omni main, exact input 75:77,39:77. Attempt 1 correctly failed closed on a moving PR. Rerun attempt 2 SUCCESS, source-only review and verified JSON/Markdown SHA256 receipt.

## Live selected-pair QA and source identity

Real Omni GitHub Actions run: https://github.com/riccardopinato/Android-Omni-Cleaner/actions/runs/46010616643

First attempt was INCOMPLETE_NO_CLEARANCE because an open PR moved after Git trees were inspected. Its artifact is 15203142195.
The rerun was SUCCESS with stable full PR identity; its artifact is 15203877300.
The successful rerun read 37 REST GETs / 5,612,281 bytes / 13.545 seconds, with 3 unique trees and one SHA-keyed reused tree.

- PR #75 SHA c8e785f89c4dc852799171718d380e97d2040966 versus PR #77 SHA 43517778d3093e4ea7af41be17172a2b4d0c7265: ancestor relationship, 63 shared changed paths, 39 byte-identical / 24 different blob SHAs, no Git mode changes.
- PR #39 SHA f0755e6c6bcda3c25616c2b8a081de98522f5941 versus #77 SHA 43517778d3093e4ea7af41be17172a2b4d0c7265: diverged history, 9 common changed paths, 8 identical / 1 different. Review StorageInventoryRepository.kt for differences in background and foreground scan scheduling.

Only 2 of 20 overlapping pairs were inspected deeply; SHA equality never proves functional equivalence. Future #77 heads require a fresh scan.

## Lightweight scanner cost comparison (not causal)

| Pilot | Open PRs | Changed-file records | REST GETs | Response bytes | Scanner elapsed |
|---|---:|---:|---:|---:|---:|
| Initial Omni pilot | 12 | 242 | 30 | 2,086,846 | 16.074 s |
| Corrected Omni PR #84 | 12 | 253 | 30 | 2,201,414 | 9.276 s |
| Initial Anna pilot | 6 | 130 | 17 | 1,298,193 | 10.646 s |
| Corrected Anna PR #379 | 6 | 130 | 17 | 1,264,874 | 7.094 s |

The two final lightweight scans both have **SUCCESS** and downloadable per-run
JSON/Markdown/SHA256 evidence: Omni artifact `15203417383` from
[run 46011075524](https://github.com/riccardopinato/Android-Omni-Cleaner/actions/runs/46011075524),
Anna artifact `15204471529` from
[run 46011029169](https://github.com/riccardopinato/Agenda-per-Anna/actions/runs/46011029169).
No rename was observed in these live PR sets; rename logic is tested offline.
The initial and later datasets differ, and network load and PR contents vary.
These figures are **observed costs, not measured savings**. No improvement
in total GitHub REST GET count has been demonstrated.

## Full receipt integrity and consumer CI

Downloaded the four relevant GitHub Actions artifact ZIPs (Omni failed attempt,
Omni successful deep rerun, Omni final lightweight, Anna final lightweight).
Verified their JSON and Markdown SHA-256 values against each accompanying
checksum manifest: **all four integrity checks PASS**. Deep JSON contains
63 complete per-path blob fingerprints for #75/#77 and 9 for #39/#77.

- [Anna PR #379](https://github.com/riccardopinato/Agenda-per-Anna/pull/379)
  merged to `8838391fca9e8592a8c7e51c884a8be389936502` after exact-head
  check/UI5/Shadow SUCCESS. [Postmerge CI SUCCESS](https://github.com/riccardopinato/Agenda-per-Anna/actions/runs/46011922947).
- [Omni PR #84](https://github.com/riccardopinato/Android-Omni-Cleaner/pull/84)
  merged to `c37994a80f77e45c8ffe9add09ea595a1c82b666` after exact-head
  verify/visual-capture/Shadow SUCCESS. [Postmerge Android CI](https://github.com/riccardopinato/Android-Omni-Cleaner/actions/runs/46012403519)
  has completed with SUCCESS on the exact merge commit; this is source/CI only, never on-device certification.

## Consumer deployment gates

Omni Cleaner PR #84 and Anna's Diary PR #379 update only the pinned read-only Shadow workflow. Both keep pull_request scanning lightweight and deep_pairs strictly manual. Both consumer exact-head source checks and postmerge main-commit CI are verified SUCCESS. The separate manual workflow_dispatch event is now verified PASS on the owner-triggered run, attempt 2.

No new Golden, Master changes, product certification, physical device, app release, provider access, PR comments or measured human time/token savings.

The last verified actions/upload-artifact tag was v4.6.2. GitHub emitted a nonblocking Node.js 20 compatibility warning on runners using forced Node 24; do not invent an unverified replacement action.

## Final gate — real workflow_dispatch PASS

The GitHub workflow was **actually triggered by the repository owner** on
`main` with `deep_pairs=75:77,39:77`. This was a real
`workflow_dispatch` event (not a synthetic PR event).

[Run #46014830454](https://github.com/riccardopinato/Android-Omni-Cleaner/actions/runs/46014830454):
- Attempt 1: the PR list advanced mid-scan, resulting in
  `PR_INVENTORY_CHANGED_DURING_SCAN` and
  `INCOMPLETE_NO_CLEARANCE`. Failure artifact ID `15204757606`.
- Attempt 2 (rerun of the failed job): job `140560009128`,
  **SUCCESS**, with artifact ID `15205662146`.
- Independently downloaded the attempt-2 ZIP and recomputed
  SHA-256 for both source report files; both checks match the
  included `openspec-shadow.sha256`. JSON:
  `0809c32437c1b28c38b9f8ab75cfc7c93b874be5b357ec402706e20f5f1889a0`.
  Markdown:
  `2afea2229eb1981bf2b686f3894e585a043c98f123758740edbbfa6ef05ccff6`.
- Real manually triggered deep comparison used 35 GitHub REST GET,
  6,194,149 response bytes and 20.398 wall seconds. These are costs,
  NOT proven token/human-time savings.
- PR #75 at `c8e785f89c4dc852799171718d380e97d2040966`
  and PR #77 at `9efecbb96f64acc57179f97bd15278b64689f0d3`:
  ancestry A→B, 63 shared changed paths, 38 identical blob hashes,
  25 different, 0 file-mode differences.
- PR #39 at `f0755e6c6bcda3c25616c2b8a081de98522f5941`
  and that same #77 SHA: diverged history, 9 shared changed paths,
  8 identical hashes, 1 differing file (`StorageInventoryRepository.kt`).
- Final `main` and open-PR inventory recheck passed; this means
  the reviewed snapshot was stable, **not** that code or product
  semantics were certified.

**The previously pending manual trigger gate is now PASS.** All source/CI
corrective roadmap gates are fulfilled. Requirements mapping remains
`UNMAPPED` where no manifest exists; a change to #77 after the
recorded exact SHA requires another scan. No automatic PR merge, APK
release, physical device, Golden promotion or semantic QA approval.
