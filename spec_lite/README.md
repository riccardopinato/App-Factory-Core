# Factory Spec Lite v1 — candidate process, not a new authority

**Status:** PROCESS CANDIDATE. This is a bounded implementation of the accepted external-OSS audit [Spec Kit E1 admission](https://github.com/riccardopinato/Idee-app-Archivi-riferimenti/blob/559a13508558948ce57e91fe14df492328bdeb0d/12-CAPABILITY-E-IMPLEMENTAZIONI/OSS_GITHUB_SPEC_KIT_ADMISSION_2026-11-27.md). It is not a certified Golden and does not install Spec Kit CLI or run agents.

## Ownership and precedence

Product Bible and approved roadmap define product behavior; Factory CURRENT/Master/Golden govern process; AGENTS refines repository behavior; code, CI and AppLab provide evidence. This manifest cannot create product approval, authorize shell/PR/merge, or bypass a human/provider/physical gate.

Modes: **FAST** isolated low-risk; **STANDARD** bounded behavior/regression; **CONTROLLED** migration/security/payment/data/native/release risk. The existing Master DIRECT/PARALLEL/CONTROLLED router takes precedence. Risk flags force CONTROLLED regardless of declared mode. The upstream Spec Kit workflow does not supply a security sandbox.

## Layout and use

- `schemas/factory_spec_lite_v1.schema.json`: strict metadata/requirements/approval contract.
- `spec_lite/templates/{FAST,STANDARD,CONTROLLED}.md`: guidance for feature-scoped `spec.md`, `plan.md`, `tasks.md`.
- `spec_lite/examples/{FAST,STANDARD,CONTROLLED}.json`: synthetic **PROPOSED / NOT_VERIFIED** manifests with pinned example source SHAs, not approved app features.
- `scripts/validate_spec_lite.py`: offline fail-closed validator; no network, writes, credentials or side effects.
- `tests/test_factory_spec_lite.py`: positive mode tests and negative vectors.

For a real app manifest, first pin the ACTUAL target HEAD SHA and Factory resolver SHA, provide the product/roadmap/AGENTS paths that exist and the approved scope/decision where available. Never infer approval from a populated string; the trusted control plane must verify the decision independently. A null Product Bible or roadmap is valid only for a PROPOSED case, not an authorized implementation.

```bash
python3 scripts/validate_spec_lite.py path/to/manifest.json \
  --expected-factory-sha <actual-40-char-Factory-SHA> \
  --expected-source-sha <actual-40-char-target-HEAD-SHA>
python3 -m unittest discover -s tests -p 'test_factory_spec_lite.py' -v
```

The example manifests are validated by tests but must **never** be treated as evidence that the underlying feature has been implemented. After admission, actual source/CI/Android/emulator/physical/provider validation follows normal AppLab and repository gates.

## Anti-drift rules

1. Stable globally unique `spec_id` per feature and unique `FR-###` + `AC-###` within it; no duplicate IDs, unresolved `conflicts_with`, or contradictory path allow/deny lists.
2. Every canonical reference embeds a 40-character commit SHA. Factory/current ref matches the supplied Factory SHA. App Product Bible/roadmap/AGENTS refs match target source SHA and repository.
3. `approval.status=APPROVED` requires a decision reference, Product Bible and roadmap references and all requirements marked APPROVED. This is still metadata and never authenticates the reviewer by itself.
4. Only NOT_VERIFIED manifests may have no evidence links; any claimed verification needs at least one receipt. A receipt must be verified by AppLab/CI before treating it as proof.
5. High-risk flags force CONTROLLED with manual gate, explicit rollback plan, integration-level checking. Every AC has a mapped required test kind.
6. No cross-repo code write, new CAP, Golden promotion, external service, install, deployment or CI bypass follows from the schema itself.


## 2026-11-27 — Selective adoption decision (stage 5)

[Decision and measurements](adoption/2026-11-27.md) · [machine-readable governance record](adoption/2026-11-27.json). **Status: optional source/CI-traced process**, not a new Golden or permission authority. All three source/CI pilots and both adapter PRs have merged on main with green post-merge checks; there is still no measured token/time improvement, Windows worker E2E or independently authenticated real AppLab durable-operation handoff.

**FAST:** prefer a single short note or manifest *when justified*; do not require `spec.md` + `plan.md` + `tasks.md` + manifest + report for an isolated change. **STANDARD:** optional FR/AC mapping for approved, nontrivial changes with integration/regression risk. **CONTROLLED:** optional evidence trace only, never replacing approvals, rollback, migrations, privacy, payments, physical/Play or exact-head gates. The three original templates remain reusable examples, not mandatory bundles.

Use the existing Agent Core and AppLab bridge adapters only with trusted source, job, manifest, WorkItem, operation and AppLab identities, plus the existing verified permission and evidence pathways. No automatic fleet rollout; at the next approved substantial feature/bug request consider the contract only if proportional to risk. For editorial batches such as World Days/Cooking Anime, document the pipeline/batch boundary at most, not each record.

The Master v27 and Golden Registry/Index remain unchanged. The decision is covered by `tests/test_factory_spec_lite_adoption.py` and the existing Factory CI, without creating a second Master or verifier.

## Provenance

Reference: github/spec-kit v1.4.5 MIT (release 6ba8beefff8d6408cadd62038e92d459093e33a8; reviewed main f2010547121b3351e4923fe467205079e4593a32). Conceptual adaptation only; templates/validator are Factory-specific, not copied from upstream code. Existing Golden Lean Engineering and AppLab verification remain controlling.
