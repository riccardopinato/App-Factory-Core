# OpenSpec Shadow Mode — audit corrective evidence, 27 November 2026

Status: Core corrective code merged, exact postmerge CI SUCCESS. Consumer exact-head checks and merges still pending at this checkpoint.

## Source and controls

App Factory Core PR #144 and #145 merged. Core main source SHA: 3e3056ffb7444a5d37f1279a2a25783366a0d98c.
Postmerge Core CI: https://github.com/riccardopinato/App-Factory-Core/actions/runs/46010932724

57 source regression tests PASS: 20 FAST, 24 deep, 13 audit security and provenance.

- P1: Markdown/HTML escaping of untrusted PR filenames and Spec Lite keys before stdout or step summary; control characters rendered as escapes, not raw GitHub runner workflow command lines. Python invalid-escape warnings removed.
- P1: each deep pair contains two exact full PR SHA commits and every overlapping changed path with blob SHA, Git mode and missing status; final default-branch and all-open-PR identity checks after all tree reads.
- P1: pinned actions/upload-artifact emits JSON, Markdown and SHA256 checksums with 30-day retention; even INCOMPLETE scans provide recoverable error evidence. No automatic PR actions.
- P2: rename-origin previous_filename aliases improve path-intersection detection without double counting; Git file mode changes distinguished from identical blob contents; genuine source Spec Lite v1 fixtures and previous-delta conflicts covered by adversarial unit tests. Unmapped requirements remain UNMAPPED and all source-declared proposals are untrusted.
- P2: complete collection retained, indexed in-memory PR lookups and SHA-based tree cache for each run, hard 500 GET limit. No stale cross-run cache or background agent.
- P1 manual workflow_dispatch: declared by both app workflows, but a true manual dispatch cannot be performed through the current connected GitHub toolset. Remains NOT_VERIFIED; a successful PR-event job is NOT a manual-dispatch receipt.

## Live selected-pair QA and source identity

Real Omni GitHub Actions run: https://github.com/riccardopinato/Android-Omni-Cleaner/actions/runs/46010616643

First attempt was INCOMPLETE_NO_CLEARANCE because an open PR moved after Git trees were inspected. Its artifact is 15203142195.
The rerun was SUCCESS with stable full PR identity; its artifact is 15203877300.
The successful rerun read 37 REST GETs / 5,612,281 bytes / 13.545 seconds, with 3 unique trees and one SHA-keyed reused tree.

- PR #75 SHA c8e785f89c4dc852799171718d380e97d2040966 versus PR #77 SHA 43517778d3093e4ea7af41be17172a2b4d0c7265: ancestor relationship, 63 shared changed paths, 39 byte-identical / 24 different blob SHAs, no Git mode changes.
- PR #39 SHA f0755e6c6bcda3c25616c2b8a081de98522f5941 versus #77 SHA 43517778d3093e4ea7af41be17172a2b4d0c7265: diverged history, 9 common changed paths, 8 identical / 1 different. Review StorageInventoryRepository.kt for differences in background and foreground scan scheduling.

Only 2 of 20 overlapping pairs were inspected deeply; SHA equality never proves functional equivalence. Future #77 heads require a fresh scan.

## Consumer deployment gates

Omni Cleaner PR #84 and Anna's Diary PR #379 update only the pinned read-only Shadow workflow. Both keep pull_request scanning lightweight and deep_pairs strictly manual. Consumer source and postmerge checks must be verified before closing this record.

No new Golden, Master changes, product certification, physical device, app release, provider access, PR comments or measured human time/token savings.

The last verified actions/upload-artifact tag was v4.6.2. GitHub emitted a nonblocking Node.js 20 compatibility warning on runners using forced Node 24; do not invent an unverified replacement action.
