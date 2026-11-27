# Factory Spec Lite — CONTROLLED

**Purpose:** any changes involving data loss, schema migration, security, payment, sensitive personal data, native lifecycle or risky release. Existing human/provider/physical gates remain non-bypassable.

## Specification (`spec.md`)
- Approved Product Bible + roadmap references, explicit FR-/AC- IDs and exclusion of unapproved scope.
- Data integrity, privacy, permissions, destructive effects, migration invariants, recovery and release boundaries.
- All new/modified requirements remain PROPOSED until supported by a trusted approval decision.

## Plan (`plan.md`)
- Define backups, version transitions, rollback rehearsal, invariants, negative-path probes and staged rollout.
- Identify exact source/artifact identities and corresponding AppLab or provider/physical evidence.
- Require explicit manual gate where indicated. No automation expands authority or releases to Store.

## Tasks (`tasks.md`)
- [ ] T001 Approval and exact source/Factory authority verification.
- [ ] T002 Migration/rollback contract and disposable test fixture.
- [ ] T003 Implement isolated reversible steps with bounded permissions.
- [ ] T004 Execute required integration/runtime/device checks and destructive-failure regression.
- [ ] T005 Independent AppLab evidence, actual review/approval, exact-head PR gate.
- [ ] T006 No release/store or data migration activation without separately authorized proof.

**Manifest:** use `spec_lite/examples/CONTROLLED.json`. An approved manifest is not proof of actual authorized reviewer identity.
