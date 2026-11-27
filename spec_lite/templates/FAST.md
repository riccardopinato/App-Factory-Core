# Factory Spec Lite — FAST

**Purpose:** isolated, low-risk, bounded change. The Master router DIRECT still governs actual execution. Use only if all risk flags are false.

## Specification (`spec.md`)
- Record `spec_id`, app/commit and relevant Product Bible/roadmap or explicit PROPOSAL state.
- Describe one user-observable behavior, its out-of-scope exclusions, FR-001 and AC-001.
- Cross-check open PRs and existing capability/donor before new code.

## Plan (`plan.md`)
- Reuse in-project implementation first; link Design-App references if UI.
- Name exact affected files, scoped preflight, tests and rollback/no-op strategy.
- No new architecture, cloud services, migrations or releases.

## Tasks (`tasks.md`)
- [ ] T001 Confirm pinned source/Factory SHAs and owner/approval.
- [ ] T002 Implement smallest complete approved slice only.
- [ ] T003 Run focused required tests and bounded cleanup.
- [ ] T004 Record PR head, CI evidence and unresolved cases; never self-certify.

**Manifest:** use `spec_lite/examples/FAST.json` against the schema and validator. PROPOSED never implies authorization.
