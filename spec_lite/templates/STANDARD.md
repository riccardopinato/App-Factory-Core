# Factory Spec Lite — STANDARD

**Purpose:** feature or bug change with meaningful dependencies and regression risk but no high-risk mutation. Keep productive parallel tasks independent and idempotent.

## Specification (`spec.md`)
- Link approved Product Bible/roadmap and canonical FR-/AC- IDs; missing approval remains PROPOSED.
- Include success paths, negative paths, accessibility/UX where relevant and explicit exclusions.
- Identify existing PRs, implementers, Golden/donors and impacted contracts.

## Plan (`plan.md`)
- Describe affected files, callers, persistence boundary, regression suite and behavior rollback.
- Map each AC ID to a test type; do not make behavior tests optional by accident.
- Parallel work only with nonoverlapping paths/ownership; use exact-head integration once.

## Tasks (`tasks.md`)
- [ ] T001 Baseline/PR/reuse reconciliation and source verification.
- [ ] T002 Test/fixture that exhibits required behavior or original bug reproduction.
- [ ] T003 Bounded implementation and compatibility checks.
- [ ] T004 Independent regression tests, CI at exact PR head, cleanup recheck.
- [ ] T005 AppLab checks only to the required risk boundary, record missing evidence.

**Manifest:** use `spec_lite/examples/STANDARD.json`; source/Factory SHA and all FR/AC IDs are validated before execution.
