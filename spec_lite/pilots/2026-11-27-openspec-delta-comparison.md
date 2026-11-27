# OpenSpec-derived incremental Spec Lite — comparative source/CI evidence

Date: 2026-11-27. Record: `FSL-OPENSPEC-COMPARISON-20261127`. Status **SOURCE/CI pilot evidence, not a Golden or autonomous/runtime certification**.

## Baseline and integration

Factory baseline before work: `a185c16000608b90c5db639f37903b49b059b10b`, Master v27, Golden Index v31. Factory Core PR [#137](https://github.com/riccardopinato/App-Factory-Core/pull/137) merged `52a7e1c3a84edf942ad80a022ba6f67e80186921`; [postmerge CI SUCCESS](https://github.com/riccardopinato/App-Factory-Core/actions/runs/45984256654). The existing Spec Lite contract now supports optional prior-SHA deltas; drift checks are read-only and missing/untrusted PR inventory blocks. Closeout returns a reviewable proposal only, without modifying Product Bible or roadmap. New CI covers **32** adversarial cases including rename collisions, history preservation, invalid approval, PR unknown IDs and intersecting globs.

## Pilot A — FAST, Gallery Drift

- PR [#20](https://github.com/riccardopinato/GalleryDrift/pull/20), base `c7f0f51c764b48228e803e3a64e2d4f9e971beae`, merged main `30c26f2b23bccbf9237163467ef0fe664e915967`.
- Real bounded bug: album with 9 photos, page size 4, final prefetch used to request range `8:12`; now requests `8:9` and foreground `at(8)` reuses same cached future. No file write or Art Drift shared-core edit.
- One added regression, existing tests; branch Android [CI PASS](https://github.com/riccardopinato/GalleryDrift/actions/runs/45983739023). **[Postmerge Android CI SUCCESS](https://github.com/riccardopinato/GalleryDrift/actions/runs/45984531353)** on exact merge SHA (342 s). Canonical album viewer reconciliation [PR #22](https://github.com/riccardopinato/GalleryDrift/pull/22) merged to `14e7a3b58a928257344774a9fb306bf95ce31905`, [branch exact-head CI PASS](https://github.com/riccardopinato/GalleryDrift/actions/runs/45985395678), [documentation postmerge Android CI](https://github.com/riccardopinato/GalleryDrift/actions/runs/45986147848) pending.
- Changed files 3; additions: 17 doc, 11 source, 15 test, deletions 1 source. Single compact contract, no five documents. Device/Play and real user-photo behavior NOT_VERIFIED.

## Pilot B — STANDARD, App Factory Agent Core

- PR [#38](https://github.com/riccardopinato/App-Factory-Agent-Core/pull/38), base `117b56b20dff1e63012c314ef32a2aa80fc558ab`, merged `8cad58bc7aace24b91647bd1d994228b3259ed64`; [postmerge CI PASS](https://github.com/riccardopinato/App-Factory-Agent-Core/actions/runs/45984356385) (159 tests).
- Real coverage weakness: Agent adapter accepted mandatory SOURCE_TEST without associated AC. Now rejects unmapped and duplicate required kinds; optional prior-SHA delta lineage stays explicitly UNVERIFIED in existing read-only WorkItem projection. No scheduler, queue, auto-dispatch or Windows runtime.
- PR #38 changed 3 files: 21 doc, 37 source, 62 tests (+120/-1); six new focused adversarial cases. Follow-up canonical [PR #39](https://github.com/riccardopinato/App-Factory-Agent-Core/pull/39) merged `7e36dbadf8177aab71e9c5d25e95a4e61fe0cc62`; [postmerge CI PASS](https://github.com/riccardopinato/App-Factory-Agent-Core/actions/runs/45984562104) (+14 doc lines) and history preserved.

## Quantitative comparison (observations only)

| CI run | Baseline | Pilot | Interpretation |
|---|---:|---:|---|
| Gallery Android | 384 s | 330 s | Difference -54 s; different head/source, runner variance; **not evidence of development speedup** |
| Agent validate | 9 s | 6 s | Difference -3 s; very short, not a controlled benchmark |

Document-to-source ratio: Gallery initial pilot 17 documentation added / 26 source+test added; Agent initial pilot 21 / 99, plus later 14 documentation lines to reconcile canonical status. These pilots are **different features**, not a randomized before/after comparison of the same feature. Prior initial Spec Lite trials reported 462 doc vs 154 source+test; do not infer savings or percentage gains by directly comparing across scopes.

No measured token usage, human/AI development time, physical performance, runtime agent operation, AppLab durable E2E or store certification. Existing external-OSS references remain donor/methodology only. Cost-benefit re-evaluation requires comparable repeated work with instrumented usage, and may rationally reject broader rollout.

## PR coexistence review

Gallery has open exploratory PRs affecting other surfaces (notably AI/search/media and pinned shared core); this pilot only changed `lib/services/album_pager.dart`, its test, and one FAST note. Agent pilot only touched `scripts/spec_lite_work_item_adapter.py`, its tests and documentation; no second scheduler/authority. A full authenticated inventory of the requirements affected by **all** open PRs was not produced. The drift checker must not claim global conflict-free status from this sampled review.

## Decision boundary

Keep this as selective source/CI pilot. Update consumer canonical product documentation only after verified exact-head postmerge gates. Preserve real prior history and independent product approval. No new Golden, CAP, global rollout, Windows executor, device evidence or authority. See `spec_lite/OPENSPEC_DELTA_RUNBOOK.md`.
