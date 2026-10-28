# v27 — Evidence gates before activation

## Phase 27A/B: structural preparation (this PR)
- [x] Pin exact fallback v26.8 full document already stored in repository.
- [x] Create compact candidate entrypoint and domain modules without touching CURRENT.
- [x] Map all 55 original sections, verify reconstruction and fallback Git identity in CI when passing.
- [ ] Prove candidate rules have equivalent actual model decisions.

## Phase 27C: candidate resolver and dual-surface fallback
- [x] Implement prototype deterministic lazy resolver with CURRENT guard and a future activation boundary.
- [x] Route tasks to integrity-checked relevant modules and optional relevant Golden Registry entries.
- [x] Use synchronized generated full fallback, verify its blob identity and disclose `FALLBACK_BASELINE_USED`.
- [x] Fail closed when a selected module or full fallback cannot be verified; add test cases.
- [x] Test deterministic selection and optional pinned SHA rejection. Actual cross-session pinning and active v27 bootstrap require the later activation phase.
- [x] Make modular + generated full fallback updates a same-PR governance and CI requirement.
- [ ] Activate resolver via CURRENT.yaml/bootstrap only after real policy pilots and approval.

## Phase 27D: source-backed dry-run pilots and performance measurement

- [x] Inspect pinned HEADs and actual product/roadmap/AGENTS evidence in Anna's Diary, Phone Guard and AppLab (read-only).
- [x] Add ten deterministic routing scenarios across the three app domains and the central Factory update rule.
- [x] Execute CI deterministic replay on exact candidate head: 11/11 cases; 9 modular/2 fallback; median 64.8% estimated UTF-8 context reduction in modular cases; source and results in `pilots/V27D_RESULTS_2026-10-28.md`.
- [ ] Run independent model behavioral equivalence tests (D2 paired prompt/scorer prepared; real outputs NOT YET AVAILABLE).
- [ ] Measure actual ChatGPT tokens and end-to-end time. D2 uses real o200k_base local tokenizer counts only, NOT provider usage or ChatGPT latency.
- [ ] Resolve any genuine safety/selection regressions prior to enabling v27.

## Initial pilot source references
1. **Anna's Diary (Flutter/UX):** a one-screen copy fix, plus separate independent UI workstreams. Validate DIRECT/PARALLEL decisions and shared design contracts.
2. **Phone Guard (Kotlin/native):** permissions and incident security with CONTROLLED checks; don't weaken physical/Play release boundaries.
3. **AppLab (CI/release):** exact-head gates, source/artifact hashes and stale-run failure case.
4. Negative cases: `audit only` must remain READ-ONLY; failed module load selects verified fallback; invalid fallback refuses use; new commit invalidates old CI.

Compare on representative equivalent tasks:
- bytes/tokens loaded before implementation (must decline materially);
- time to first meaningful edit and to validated integration;
- CI retries, redundant fetches and any safety regression;
- if policy decisions regress, no promotion even if bootstrap is faster.

## Phase 27E: explicit activation and rollback
- [ ] Required repo gates green, no unresolved review.
- [ ] No safety-policy regression in scenario evaluations.
- [ ] CURRENT and bootstrap updated atomically in a protected PR.
- [ ] Immutable v26.8 fallback remains readable, hash verified and documented.
- [ ] Fallback decision is visible; rollback of resolver is documented and testable.

No steps marked done above imply that external app pilots have been performed.

## 27D first pilot feedback — resolver defects (2026-10-28)

Initial exact-head CI replay failed as intended on two selection-policy defects: a roadmap continuation selected `audit-roadmap` and `experience` but omitted the complete `authority-execution` parallel-first contract, and the bare name `AppLab` incorrectly routed to delivery because it was listed as a task trigger. The v27D branch corrects the continuation authority requirement and removes the name-only trigger. This finding demonstrates that deterministic static checks can catch selection drift; it does **not** certify real model decisions.

## 27D evidence status as of 2026-10-28

Deterministic routing and byte-cost replay **PASS** on candidate PR #25 exact head. The v27C/v27D resolver has also passed 12 unit tests and the synchronized fallback/section-reconstruction gates. Three routing gaps were corrected during pilot execution: omitted continuation authority, project-name-only AppLab routing and missing specialist PIN Golden. Route metadata is included in the generated full fallback, preventing invisible drift.

**HOLD for v27E**: actual model response equivalence, real token counts and end-to-end time-to-first-edit/merge are not verified. Repository snapshots are source-backed and pinned but tests are read-only; no production app test, physical QA, or rollout is claimed.

## v27D2 — paired behavioral evaluation

- [x] Prepare 16 safety and behavior decision cases, paired prompt exporter, fail-closed evidence scoring protocol and static negative tests.
- [x] Confirm exact-head CI local token-count benchmark with pinned tiktoken 0.12.0: 16 prompts, 13 modular / 3 fallback, modular median token reduction 48.96%. See pilots/V27D2_RESULTS_2026-10-28.md. This is tokenizer output, not actual GPT-6 runtime usage.
- [ ] Execute 32 independent real model prompt runs under the same model/effort, capture verified provider request IDs and token/latency receipts.
- [ ] Obtain independent qualitative review and comparable real development workflow timings.

Activation v27E remains HOLD: model behavior and actual ChatGPT end-to-end performance must not be inferred from green static CI.

## v27D2 result boundary

Pinned tokenization study is recorded in pilots/V27D2_RESULTS_2026-10-28.md. Real model executions: ZERO. Independent policy-equivalence verdicts: NONE. Real ChatGPT token-usage/time-to-edit comparisons: NOT VERIFIED. Activation v27E remains HOLD until these separate gates are met.
