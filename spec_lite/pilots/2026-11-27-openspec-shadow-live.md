# OpenSpec Shadow Mode — Maxi-step 5 two-app live evidence

Date: 27 November 2026. **Status: source/CI pilot; adoption remains opt-in, not Golden or certification.**

## Factory identity and gates

App Factory Core baseline `ce7503456fce3af757f7160706c02d0cc1694b42`, Master v27, Golden Index v31.
GitHub reader + opt-in review workflow [PR #139](https://github.com/riccardopinato/App-Factory-Core/pull/139) merged.
Global/focused fix, mergeability/containment signals and API-cost metrics [PR #140](https://github.com/riccardopinato/App-Factory-Core/pull/140) merged to `e45600bb4a12db63b3107581587e33e590d2f21b`.
[Exact postmerge Core CI SUCCESS](https://github.com/riccardopinato/App-Factory-Core/actions/runs/45991082917), **20 focused adversarial tests PASS**.
All live scans used the pinned, repo-scoped caller workflow GITHUB_TOKEN with GitHub REST GET only.

## Read-only pilot results

| Metric | Android Omni Cleaner | Anna's Diary |
|---|---:|---:|
| Open PRs during scan (includes the pilot PR) | 12 | 6 |
| Complete changed-file records | 242 | 130 |
| Repository-wide changed-path overlap pairs | **20** | **3** |
| Overlap pairs involving just the pilot workflow PR | 0 | 0 |
| PRs without structured requirement mapping | 12 | 6 |
| PR bases on main whose SHA differs from observed HEAD | 9 | 4 |
| GitHub merge-conflict state PR count | 1 | 2 |
| REST GET requests | 30 | 17 |
| Response bytes | 2,086,846 | 1,298,193 |
| Scanner wall seconds | 16.074 | 10.646 |

- [Omni pilot PR #82](https://github.com/riccardopinato/Android-Omni-Cleaner/pull/82), source main `358176eac8470ff302549702e21aeb164eb49a15`, [live Shadow run PASS](https://github.com/riccardopinato/Android-Omni-Cleaner/actions/runs/45991215364): all 63 paths of PR #75 occur in PR #77, but this is **only file-scope containment**. #77's own PR body explicitly describes consolidation of #75, #73/#76 and #39; do not treat as accidental code equivalence, a proven semantic contradiction, or permission to merge.
- [Anna pilot PR #377](https://github.com/riccardopinato/Agenda-per-Anna/pull/377), source main `7f6a60ff883b664574e3b7404aea12295d5a392b`, [live Shadow run PASS](https://github.com/riccardopinato/Agenda-per-Anna/actions/runs/45991224224): three actual changed-file overlap pairs among #199, #215 and #376. GitHub reports two conflicting merge states; #199 OAuth staging and #215 privacy explicitly remain draft/no-merge, and were not altered.

## Verified commit ancestry — overlap triage

The live source report is supplemented by GitHub commit comparison (not semantic adjudication):

- Omni PR #73 source `c226c4e` is an ancestor of PR #75 source `c8e785f` (0 behind, 39 ahead).
- Omni PR #75 source `c8e785f` is an ancestor of the observed PR #77 source `ccd23bc` (0 behind, 87 ahead).
- Omni PR #39 and #77 have **diverged** histories (26 behind, 232 ahead). A path overlap cannot prove identical SQLite behavior or verify a safe merge.
- Anna's Shadow review-only PR #377 was merged after its own exact-head source checks to main `b00c79d15dbd9e49373b948245f49ca18880da09`; [postmerge checks](https://github.com/riccardopinato/Agenda-per-Anna/actions/runs/45992089708) remain **in progress** at this record's update.
- Omni's Shadow review-only PR #82 was merged after Shadow, Android verify and visual capture checks to main `5172506dde623b08af9fb3b29d2261168d1056b3`; [postmerge checks](https://github.com/riccardopinato/Android-Omni-Cleaner/actions/runs/45992302954) remain **in progress** at this record's update.

The ancestry relationships explain intentional stacked work but do not replace PR diff review, Product Bible, branch protection, physical/device or owner-gated acceptance.

## Exact file blob fingerprint comparison (second-stage triage)

Compared exact Git blob SHA identities at each pair of pinned PR heads. These values reflect **file bytes**, not independently verified behavior:

| PR pair | Shared paths | Byte-identical files | Changed file blobs |
|---|---:|---:|---:|
| Omni #73/#75 | 46 | 38 | 8 |
| Omni #75/#77 | 63 | 40 | 23 |
| Omni #39/#77 | 9 | 8 | 1 |
| Anna #199/#215 | 3 | 0 | 3 |
| Anna #199/#376 | 2 | 0 | 2 |
| Anna #215/#376 | 2 | 0 | 2 |

The one differing shared file for Omni #39/#77 is `app/src/main/java/com/riccardopinato/omnicleaner/cleaner/StorageInventoryRepository.kt`; it merits focused developer review before any consolidation. Do **not** call 8/9 'semantic duplication', classify conflicts as repaired, or compute a false-positive rate from these file-level identities. Git trees returned `truncated=false` for all compared heads.

## Interpreting signals

A shared file is evidence of potential integration work, not a bug. Base SHA differences are not automatic staleness. A source-described planned consolidation is not a verified supersession of product requirements. Without structured canonical requirement IDs, it is impossible to certify a semantic conflict or its absence: every currently scanned PR remains UNMAPPED.

GitHub Actions step summaries and run URLs constitute inspectable live-source evidence. Both app PRs (#377 Anna and #82 Omni) have merged on exact checked heads; each adds only one workflow. **no app logic, data, Vault, deletion, storage, billing, provider, signing or Android runtime was changed by this experiment.** User-required physical and provider acceptance remains independent.

## Cost-benefit boundary

The scanner used **47 GitHub REST GETs**, **3,385,039 response bytes** and **26.72 seconds** summed observed scanner wall time for the two executions. These are consumption observations, **not time savings**, and do not include Github Actions billing, LLM token cost, manual review time, post-merge app build cost or real-device evidence. False-positive rate cannot be measured until actual reviewed PR conflicts are adjudicated. Do not global-roll out or create new Golden/Agent/AppLab verifier based on these two pilots.

## Integration condition

Both app-only workflow PRs passed all their PR-head checks and were merged. Product security/staging drafts remain untouched. The postmerge CI checks for the two consumer main SHAs remain pending at this report update; do not certify them before separate SUCCESS. The deployment remains an opt-in source/CI pilot and does not permit automatic comments, approvals, merge, rebase or release.
