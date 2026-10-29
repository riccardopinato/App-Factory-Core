# App Factory v27E — Controlled zero-cost activation and rollback

**Contract revision: 2026-10-29.** Activation may proceed through a
**controlled, preliminary, no-API-expense release path**. The earlier v27D2
32-call real-model equivalence study remains optional research and is **not**
a billing prerequisite. This is an explicit change to the release protocol
following the owner's no-additional-cost instruction; it is NOT a claim
that 32 real GPT-6 evaluations happened or that ChatGPT latency was measured.

## Current authority / release identity

Until the exact activation PR is merged, CURRENT.yaml still selects v26.8.
A successful activation sets the real CURRENT version to v27 in one coherent PR.
The new commit SHA is the sole Factory baseline after merge.
The old full v26.8 Master remains immutable historical recovery.

## What is ready

- Compact modular Master, 8 registered modular sections, 55-section
  reconstructible v26.8 policy, and synchronized generated full v27 fallback.
- Hash-pinned modules/manifest, Golden readiness routing, fail-closed resolver.
- Dual-version schema/validator, negative tests, shadow activation and fallback.
- 11-case deterministic routing replay and 16-case v27D2 prompt/tokenizer suite.
- Source/policy risk review of 16 cases in
  `pilots/V27E_ZERO_COST_SOURCE_REVIEW_2026-10-29.md`.
- Historical local tokenizer observation: 48.96% median prompt reduction for
  13 modular scenarios, not actual ChatGPT usage or time-to-merge speedup.

## Controlled release gates — ALL required before merging v27

1. **Exact-head CI:** validate Factory, 55-section fidelity, core/manifest/
   generated-full-fallback integrity, 16-case prompt generation/tokenizer tests,
   candidate routing, negative/fail-closed cases, simulated v27 activation.
2. **Source-level safety review:** source-backed mapping for the 16 critical
   scenarios must preserve audit/read-only boundaries, owner-auth/PIN/Keystore,
   data migration/recovery, exact-head CI, signing, release/physical proof,
   untrusted-input containment, fallback integrity and unauthorized rollout.
   Zero known critical rule omissions; a new critical finding blocks merge.
3. **Atomic v27 activation:** CURRENT, Master Core alias, core+modules,
   generated full fallback, manifest, Golden Registry, bootstrap, Project
   pointer, schema, validator, README/changelog must agree. Generated fallback
   is NEVER hand-edited. Historical v26.8 bytes do not change.
4. **Protected PR and release reality:** no unresolved blocking review thread,
   PR mergeable, required exact-head checks successful, branch protection
   respected. A green CI does not imply physical app certification.
5. **Transparent limitation:** label activation `CONTROLLED/PRELIMINARY`.
   Do not report model behavioral equivalence, actual provider API token
   savings, or ChatGPT end-to-end speedup as verified. Retain the former 32
   independent model responses gate ONLY for an optional higher-confidence
   model-behavior certification, not for ordinary Factory operation.

## Post-activation operational confirmation

The next genuine ChatGPT app workflow becomes the initial **no-cost practical
pilot**, not a pre-release paid dependency. Log verifiable wall-clock events
(time of start, first meaningful edit, exact-head CI, and validated merge) and
any routing/safety regression. Separate real observations from assumptions.
Only compare performance to v26.8 if sufficiently comparable observations
exist; otherwise record `SPEEDUP_NOT_VERIFIED`.

If a critical policy/routing regression appears, suspend use and revert the
v27 activation PR through the normal protected branch/CI process. Never
silently advertise CURRENT v27 while loading the archived v26.8 Master.

## Optional later research, NOT an activation gate

The v27D2 Responses API study supports 16 x 2 independent calls with provider
receipts and independent semantic review. It remains available but is **not**
required or automatically launched. GitHub workflow dispatch is manually
confirmed and billable; an installed secret NEVER grants billing authorization.
Ordinary development uses ChatGPT Plus/Chat without an additional API purchase.
No paid test or model-behavior certification has been executed in this release.

## Project settings

GitHub cannot edit the ChatGPT Project custom instructions. The Project must
continue using a version-aware pointer to CURRENT.yaml; changing repository
state alone does not update external settings. The project's existing
version-aware pointer remains compatible with v27.
