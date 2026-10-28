# v27 Lean & Modular — non-authoritative candidate

**Status: CANDIDATE_NOT_ACTIVE.** Current Master remains v26.8, resolved through `CURRENT.yaml`.
Pinned Factory baseline: `72e6d7fd1c57c64594501d4f05d6bf5a0f21ad20`.

## What is implemented
- `MASTER_CORE_v27_CANDIDATE.txt`: lightweight execution and safety entrypoint, 119 lines.
- `MODULE_MAP.json`: section IDs, module ownership, task selector cases and verified fallback pin.
- `modules/*.txt`: 8 on-demand groups copied **verbatim** from the complete v26.8 Master.
- `RULE_COVERAGE.md`: audited map of 55 existing headings/sections.
- `scripts/validate_v27_candidate.py`: checks exact section reconstruction, fallback identity, manifest pointers and negative controls.

## v27C prototype: synchronized operational fallback

- `scripts/resolve_v27_candidate.py --task "Procedi" --context "redesign schermate" --include-goldens` tests deterministic lazy routing. The prototype is read-only and not in the official bootstrap.
- `scripts/build_v27_fallback.py --write` regenerates the full current candidate policy from core + modules + registered policy updates and refreshes hash pins. `--check` runs in CI.
- `MASTER_FULL_FALLBACK_GENERATED.txt` is the living operative fallback, updated atomically whenever the modular Master changes. An unknown or corrupt module triggers the hash-verified fallback with an explicit status; a corrupt fallback blocks execution.
- Central repository `AGENTS.md` and `GOVERNANCE.md` now require simultaneous modular + generated full updates for future Master/Core changes.

## Immutable historical recovery snapshot
Do not create a second independently edited Master. The **immutable historical recovery copy** is the existing:
`master/MASTER_PROMPT_UTILITY_FLUTTER_CHATGPT_v26_8_FULL.txt`.
Its source commit is `72e6d7fd1c57c64594501d4f05d6bf5a0f21ad20` and Git blob SHA is `98fee1ef7ccadc98b947cefa74b33e9fae51022f`.
After v27 activation (a *separate* gated change), first use the **generated synchronized v27 full fallback** with integrity verification and `FALLBACK_BASELINE_USED` disclosure. The historical v26.8 is emergency recovery only and is never silently used as a current-policy replacement.

## Activation rule
This PR must not update `CURRENT.yaml`, replace `master/MASTER_PROMPT_CURRENT.txt`, or change app repositories. v27 becomes CURRENT only after:
1. Structural and negative-control tests.
2. Policy equivalence evaluation on direct, parallel, controlled, read-only, stale-CI cases.
3. Pilots on Flutter UI/roadmap, Android native/privacy, and CI/certification workflows.
4. Concrete before/after context/time measurements without relaxing gates.
5. Explicit activation PR with atomic resolver/bootstrap/schema/validator updates and rollback provision.

This phase delivers a candidate and safety net, **not** a claimed speedup or active modular resolver.

## v27D read-only pilot evidence

Deterministic 11-case replay on pinned Anna's Diary / Phone Guard / AppLab source contexts is documented in [pilots/V27D_RESULTS_2026-10-28.md](pilots/V27D_RESULTS_2026-10-28.md). Real model behavior and end-to-end time improvements are **NOT VERIFIED**. Active Master remains v26.8.
