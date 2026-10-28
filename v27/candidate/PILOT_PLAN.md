# v27 — Evidence gates before activation

## Phase 27A/B: structural preparation (this PR)
- [x] Pin exact fallback v26.8 full document already stored in repository.
- [x] Create compact candidate entrypoint and domain modules without touching CURRENT.
- [x] Map all 55 original sections, verify reconstruction and fallback Git identity in CI when passing.
- [ ] Prove candidate rules have equivalent actual model decisions.

## Phase 27C: resolver, only after policy contract approval
- Implement a lazy resolver driven by CURRENT for v27 (not ad hoc text search).
- Route task to only relevant modules and relevant Golden docs.
- Guard failures with verified fallback and explicit `FALLBACK_BASELINE_USED`.
- Detect unavailable/corrupt/outdated module or missing dependency; fail closed.
- Test deterministic selection, version pinning and one-baseline-per-session.

## Phase 27D: behavioral and performance pilots
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
