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
- [ ] Execute GitHub CI deterministic replay on exact candidate head; record selected modules, Golden IDs, UTF-8 context bytes and negative cases.
- [ ] Run independent *model behavioral equivalence* tests (not established by static text/routing checks).
- [ ] Measure real ChatGPT token usage and time-to-first-edit/completion on comparable tasks (not established by script microbenchmarks).
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
