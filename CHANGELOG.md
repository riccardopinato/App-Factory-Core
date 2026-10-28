# Changelog

## 2026-10-28 — v27 Lean & Modular candidate / pinned v26.8 fallback

- Prepared the **inactive** v27 modular architecture: compact candidate core, 8 verbatim domain modules, complete 55-section v26.8-to-v27 rule map and six representative routing scenarios.
- Pinned the **existing** `master/MASTER_PROMPT_UTILITY_FLUTTER_CHATGPT_v26_8_FULL.txt` as exact fallback at App Factory SHA `72e6d7fd1c57c64594501d4f05d6bf5a0f21ad20` (Git blob `98fee1ef7ccadc98b947cefa74b33e9fae51022f`); no extra independently edited Master copy.
- Added candidate-only validation to the central CI: exact source reconstruction, fallback identity, no missing/duplicate/altered sections, routing reference checks, compact-core size and negative controls.
- Documented planned Flutter UI, native Android and CI/QA policy pilots and the separate resolver/activation/rollback gate.
- **No activation:** `CURRENT.yaml`, current Master v26.8, Golden Index v23, Golden Registry v2 and downstream apps remain untouched. Static source mapping does not certify behavioral equivalence or speed gains.


## 2026-10-28 — Master v26.8 / Adaptive Execution

- Added a **minimum-necessary-process execution router** without introducing another QA tier, workflow or authority: DIRECT for bounded simple work, PARALLEL for genuinely independent streams, CONTROLLED for high-risk changes.
- "Procedi" and roadmap continuation now reuse valid baseline/roadmap and decide once with the parallel-first rule; avoid repeated plans, audits, permission questions and irrelevant instructions.
- Codified fail-fast focused preflight before costly CI (notably compile instrumentation-test sources when modified), no repeated CI on known preflight failures, and immutable exact-head artifact reuse only on matching source/build/toolchain/signing contracts.
- Preserved existing required checks, CI branch protections, evidence trust boundaries, data safety, audit-only semantics and the repository governance/authorization contract.
- Updated FAST_DELIVERY playbook actions and agent validation module; validator v6 adds static policy/playbook consistency checks (does NOT certify real agent behavior).
- Bumped Master v26.7 to v26.8 (versioned + alias), CURRENT/Registry/README/changelog aligned. Golden Index stays v23 and Golden Registry stays v2; modular Master redesign is deferred to v27.


## 2026-10-28 — Master v26.7 / Parallel-first "Procedi" roadmap execution

- Added mandatory **parallelization assessment** when the user writes "Procedi", "procedi con la roadmap", "continua" or equivalent for an already authorized implementation scope.
- Choose genuine independent workstreams/agents only when supported and beneficial; use serial execution for real dependencies or excessive conflict/coordination costs.
- Defined bounded workstream ownership, shared architecture/design contracts, single-writer file/branch discipline, final integrated exact-head checks and truthful progress reporting.
- Preserved Chat-only preference, existing authorizations, Product Bible/Roadmap authority, protected-branch merge gates and read-only audit boundary.
- Master v26.6 -> v26.7; Golden Index remains v23 and Golden Registry remains v2. Synchronized CURRENT alias, versioned master, resolver, Registry, changelog; corrected stale README version references and Master footer.
- Core validation verifies repository consistency, not actual multi-agent availability or downstream time savings.


## 2026-10-27 — Phone Guard donor harvest / Golden Index v23

- Added **Capability Harvest / Multi-Donor Assembly** process candidate from the Phone Guard foundation pilot.
- Materialized the previously deferred **Sensor Fusion Android** placeholder as a real specialized Golden draft using Pocket Guard, Tabletop Motion Alarm and Phone Guard immutable refs.
- Added **Android Alarm Escalation** draft for siren/vibration/strobe, configurable flash frequency, target alarm volume with restore, high-visibility warning screen and Android/OEM truth boundaries.
- Added **Android Local PIN Verifier / Keystore** draft combining Tabletop PBKDF2 policy with Pockara AndroidKeyStore-HMAC hardening.
- Recorded four donor/evidence files under `evidence/phone-guard/`.
- Recorded Luminous Circle as an unpinned pattern input only; the reusable downstream implementation is pinned through the Phone Guard commit instead of claiming missing source provenance.
- No application source code was copied into App-Factory-Core.
- Bumped Golden Index v22 -> v23; Master remains v26.6.

## 2026-10-26 — Factory Adoption Kit / Golden Index v22

- Added `adoption/FACTORY_MODE_PROFILE_v1.yaml` as the canonical central profile for Roadmap Fast + Continuous Maintenance adoption.
- Added the tiny per-app `APP_FACTORY_ADOPTION.yaml` pointer template.
- Added `adopt_factory_mode.py`: dry-run by default, idempotent apply/update, and no writes to existing GitHub workflow files.
- Added `validate_factory_adoption.py` plus JSON/YAML schemas for profile and per-app adoption contracts.
- Added the PROCESS_ONLY `ADOPT_FACTORY_MODE` playbook for new or existing repositories.
- Codified the fallback rule: inspect and preserve custom workflows; integrate/extend before adding a separate workflow; never overwrite or replace existing workflows as part of adoption.
- Added validator v5 smoke coverage proving dry-run, apply, validation, idempotence and byte-for-byte preservation of an existing custom workflow.
- Bumped Golden Index v21 -> v22; Master remains v26.6.

## 2026-10-26 — Factory Automation Layer / Golden Index v21

- Added Roadmap Fast + Continuous Maintenance as COPY-READY PROCESS from AppLab v5.6.
- Added Event-Driven Execution + Reconciliation as COPY-READY PROCESS from AppLab v5.4G/v5.5B.
- Added Immutable Build / Test Artifact as COPY-READY PROCESS.
- Added five reusable contracts: failure taxonomy, maintenance lanes, exact-artifact manifest, rollout state and recovery scenario matrix.
- Added five machine-readable playbooks: Fast Delivery, Failure Triage, Donor Promotion, Controlled Rollout and Build Once Verify Many.
- Added PROCESS_ONLY playbook runner; it checks inputs/materializes ordered plans without becoming merge/release/certification authority.
- Added PATTERN-3 rule: third materially equivalent occurrence triggers APP-SPECIFIC / DONOR / FACTORY PROCESS / GOLDEN CANDIDATE evaluation, never auto-promotion.
- Registered AppLab v5.4-v5.6 donor evidence at immutable SHA 1c117ca5224232db21d047ce376026509b0924a0.
- Upgraded semantic Factory validation from v3 to v4 for the automation layer.
- Bumped Golden Index v20 -> v21; Master remains v26.6.

## 2026-10-22 — Duplicate / Similarity Review Gate / Golden Index v19

- Added `GOLDEN_DUPLICATE_SIMILARITY_REVIEW_GATE_v1_DRAFT` as a provider-agnostic DESIGN-ONLY process candidate.
- Generalized duplicate detection into normalization -> candidate retrieval -> multi-dimensional comparison -> explainable review -> decision.
- Explicitly prohibited destructive auto-delete/overwrite based only on similarity scores.
- Added configurable domain-specific scoring, variant classification, batch reports, review-memory invalidation and fail-safe comparator semantics.
- Linked the new gate from Versioned Editorial Catalog and Import / Export / Portability without duplicating their responsibilities.
- Recorded In Cucina con gli Anime F1/F2 design provenance while preserving the boundary that the gate is not yet implemented.
- Bumped Golden Index from v18 to v19; Master remains v26.6.


## 2026-10-15 — Reuse audit / Master v26.6 / Golden Index v18

- Audited recent certified/green implementation across Anna's Diary, World Days,
  Send to PC, FrameLab, Android Omni Cleaner and AppLab.
- Added Progressive Disclosure / Module Visibility Golden candidate from Anna v1.01-A/B/C.
- Promoted the provider-agnostic Entitlement Contract to COPY-READY using World Days as a real decoupled donor.
- Added Play Billing Lifetime Entitlement provider candidate; Store sandbox/Play Internal evidence remains NOT VERIFIED.
- Registered World Days as the first real Flutter donor for the AdMob Golden while keeping physical Flutter AdMob/UMP evidence pending.
- Added Resumable Local Transfer candidate from Send to PC v1.28.1; physical interruption/resume remains pending.
- Added Versioned Editorial Catalog candidate from two independent donors: FrameLab + World Days.
- Added Cross-App Verification process candidate from AppLab v4.8; real paired Wonderlog↔Anna physical round-trip remains pending.
- Updated Incremental Persistent Indexing and Bounded Parallel Hashing with Android Omni Cleaner Step 9.7 primary-device physical benchmark evidence.
- Updated Android Signing / Release Identity with Omni Cleaner RC1 fail-closed source-side release pipeline evidence.
- Updated Onboarding, App Shell, Release Reality and AppLab QA boundaries with the newly validated donor evidence.
- No product feature was introduced by this Core update.

## 2026-10-14 — CamperBoss second pilot / AppLab QA CERTIFIED PROCESS

- Completed the second independent external pilot of the AppLab QA / Certification Adapter on CamperBoss.
- Added the Golden client contract to CamperBoss PR #27 and merged it to `main` at `cf4202e25bf3bc630f9cfe5e3823219acfba84b4`.
- Verified exact pilot head `58b83ef630fdb04e0cc6f34d27e03b20ec191787`: Flutter CI #473 PASS and Release Core Platform Builds #363 PASS.
- Bound AppLab run `38566088778` to package `com.camperboss.camperboss`, version `0.2.2 (2018)` and APK SHA-256 `3d14d922b3cfca867fb9ac9c3fbc90d9d143c01b51856321928caa2d98e0cda3`.
- Preserved the first trusted-runtime System UI Lab FAIL as evidence; a failed-job rerun on the same immutable source/build contract and exact APK bytes passed the complete trusted runtime.
- Final trusted runtime, Maestro and System UI Lab are PASS; physical-device remains BLOCKED and distribution/store/production remain NOT VERIFIED.
- Promoted AppLab QA / Certification Adapter v1 to **CERTIFIED PROCESS** after Anna's Diary + CamperBoss.
- Bumped Master from v26.4 to v26.5 and Golden Index from v16 to v17.

## 2026-10-14 — Anna's Diary pilot / AppLab QA COPY-READY PROCESS

- Completed the first real external pilot of the AppLab QA / Certification Adapter on Anna's Diary.
- Upgraded Anna's client contract to the merged hardened AppLab verifier `931c124dbb1a36d43842db5b60bd5f04843e5330`.
- Proved fail-closed package binding with canary AppLab run #652 / `38527684391`.
- Fixed the AppLab pre-runtime failure-path analysis-mode attribution defect in AppLab PR #110 without weakening failures.
- Verified the final integrated Anna tree `1425ab64ae4440a10228d397444eea1883ec371a` with AppLab FULL run #668 / `38558260017`: analyze/test/build/runtime/Maestro PASS and trusted evidence bound to APK SHA-256 `fdbfdf7f50337fd26c95587d63fc9deb00464bc7e4c327be0f6694daa413f165`; merged Anna PR #103 to `main` at `f929a1f48989d48eb8c6a3d75f53a16b5bae297f`.
- Added `applab.project.json` so physical-device requirements remain explicit; Release Reality correctly leaves physical verification BLOCKED and distribution/store/production NOT VERIFIED.
- Promoted AppLab QA / Certification Adapter v1 to **COPY-READY PROCESS**; a second independent project is still required for CERTIFIED PROCESS.
- Bumped Master from v26.3 to v26.4 and Golden Index from v15 to v16.

## 2026-10-14 — AdMob / UMP native production hardening

- Updated **GOLDEN_ADMOB_SAFE_ADAPTIVE_MONETIZATION_v1_DRAFT** from draft revision 0.1 to 0.2 without promoting its Golden status.
- Re-verified current Google provider guidance for Android Mobile Ads Legacy 25.5.0, UMP 4.0.0, test ads, European regulations messages, privacy options/revocation and consent sync.
- Registered **Send to PC v1.27.6** as the first real Android-native App Factory AdMob donor under `evidence/admob/`.
- Captured the production bug/fix where `InterstitialAd.load()` inherited `Dispatchers.IO` and failed with the main-UI-thread requirement.
- Added explicit placement-level failure isolation so one banner/interstitial failure must not disable the whole monetization session.
- Added the two-surface UMP rule: SDK/runtime integration plus AdMob Privacy & messaging server-side publication/configuration.
- Added server-side message reality: publishing/editing UMP content does not require a new APK when the UMP client is already integrated.
- Added fail-closed production ID preflight, diagnostic forced-EEA/test-ID lane, privacy-policy/revocation checks and observability boundaries.
- Marked the provider-sensitive Golden freshness **CURRENT** as of 2026-10-14.
- Kept status **DRAFT / CANDIDATE — NON COPY-READY** because the required Flutter/Web/Premium/full failure-matrix promotion evidence is still incomplete.

## 2026-10-14 — Incremental indexing / bounded hashing Golden candidates

- Added **GOLDEN_INCREMENTAL_PERSISTENT_INDEXING_v1_DRAFT** for large local catalogs, scan generations, warm reuse, trustworthy revision-bound metadata and stale-index safety.
- Added **GOLDEN_BOUNDED_PARALLEL_HASHING_v1_DRAFT** for physical-alias collapse, bounded worker hashing, producer bounds/backpressure, cancellation, deterministic grouping and trusted hash-cache reuse.
- Recorded immutable Android Omni Cleaner donor provenance and exact-head CI/APK evidence.
- Bumped Golden Index from v14 to v15; Master remains v26.3.
- Kept both Goldens provider-agnostic and non-copy-ready until large-library and physical-device evidence exists.


## 2026-10-14 — Easy Debloat pilot / Code Hygiene CERTIFIED PROCESS

- Merged Easy Debloat pilot PR #1 into the dedicated `easydebloat-build` lineage at `30277ac9eab8d614c9c0f6bfd04048680a3f0e76`.
- Verified the merged tree is identical to exact-head `32c3660129d85cc12121b68f3d56d8630e1db5f1`, which passed Easy Debloat Android CI run `38483735583`.
- Promoted Code Hygiene v1 to **CERTIFIED PROCESS** after comparable replacement/bug-fix evidence from TrailPath and Easy Debloat.
- Materialized Easy Debloat's historical packed source into normal Git-tracked files before functional modification, preserving a mechanical normalization boundary.
- Confirmed that no manual ADB/Wireless ADB path existed; Shizuku remained the single privilege transport.
- Replaced ambiguous raw `&&` command composition with a structured package-operation executor and regression coverage.
- Fixed duplicate Shizuku bind bootstrap semantics and invalid Android backup XML surfaced by release lint.
- Kept physical Shizuku runtime validation explicitly NOT VERIFIED; process certification does not imply native runtime certification.
- Bumped Master to v26.3 and Golden Index to v14.


## 2026-10-14 — TrailPath second pilot / Governance certification

- Merged TrailPath pilot PR #40 to the canonical post-v1 lineage at `6679b1ef0713e9bf8407e8b07578727e4f73ed2a`.
- Verified the merged tree is identical to exact-head `0220a88a867b6d762b103032cf5262e0a0fb0c32`, which passed TrailPath CI #844 / run `38474177782`.
- Promoted Agent Governance v1 to **CERTIFIED PROCESS** after successful downstream adoption in CamperBoss and TrailPath.
- Promoted Code Hygiene v1 to **COPY-READY PROCESS** after TrailPath supplied the missing feature-replacement + bug-fix + regression-test evidence.
- TrailPath replaced nested routing fallback composition with one ordered provider chain, removed the superseded fallback-specific test, preserved intentional local/Smart Trace paths, and validated the cleaned tree.
- Recorded one hosted-emulator UX ANR as non-deterministic infrastructure evidence only after the same exact head passed the rerun; no product assertion was weakened.
- Renamed the current Code Hygiene Golden from the draft filename to `GOLDEN_CODE_HYGIENE_v1.txt`; archived the previous draft snapshot.
- Bumped Master to v26.2 and Golden Index to v13.
- Fixed the stale Master footer that still identified itself as v25.


## 2026-10-13 — Agent Governance first real pilot / COPY-READY PROCESS

- Merged CamperBoss pilot PR #26 to main at `19c2b24cd5164caa9f5178679b8fbc961e7af3ce`.
- Promoted Agent Governance v1 to **COPY-READY PROCESS** after a real downstream integration with green CI/build evidence.
- Clarified bridge drift semantics: required only when a duplicated/generated tool-specific bridge actually exists; N/A otherwise.
- Added durable CamperBoss pilot evidence under `evidence/agent-governance/`.
- Recorded real findings from the pilot: stale chat-selected authority, stale implementation-status docs, two dead constant files and one unused direct dependency.
- Kept Code Hygiene v1 as **DRAFT / PROCESS CANDIDATE**; the pilot validates dead-code/dependency cleanup but not yet the required feature-replacement + bug-fix promotion evidence.
- Bumped Master to v26.1 and Golden Index to v12.
- Fixed stale README/index references to historical v25/v10 paths and versions discovered during the same bounded governance cleanup.


## 2026-10-13 — Agent Governance v1 / Code Hygiene v1

- Promoted the Factory baseline to Master v26 and Golden Index v11.
- Added root `AGENTS.md` as the canonical repository-local operating contract for agents working on App-Factory-Core.
- Added modular on-demand policies for code hygiene, testing/validation, Git workflow, and research/reuse.
- Added Golden Agent Governance v0.1 and Golden Code Hygiene v0.1 as DRAFT / PROCESS CANDIDATE.
- Made bounded obsolete-code/dependency/asset cleanup part of substantial implementation work.
- Added the invariant that a replacement is incomplete until the superseded implementation has been evaluated for removal.
- Required relevant validation to be rerun after final cleanup.
- Added App Bootstrap adoption of repository-local AGENTS.md for new apps.
- Added deterministic validator checks for AGENTS portability budget, module presence, and critical governance invariants.
- Defined tool-specific CLAUDE/Copilot/Cursor/Gemini files as thin or generated bridges, not independent policy sources.
- Recorded source research and immutable refs for awesome-copilot, AgentsMD, AGENTS-spec, agentsync, FerroxLabs, agents.md and agent-anatomy.
- Treated jbarbier/CLAUDE.md as pattern-reference-only because no repository license was exposed at review time; no code/text was copied from it.


## 2026-10-11 — Android production signing gate hardening

- Expanded Android Signing / Release Identity Golden from principles to an explicit one-time production signing procedure.
- Standardized permanent keystore generation, separated secure backup, public certificate SHA-256 registration and four GitHub Actions secrets.
- Added explicit USER-ACTION GATE semantics when connectors cannot write repository secrets.
- Required a real first production workflow run before declaring production signing verified.
- Added fail-closed verification of expected vs actual signing certificate identity as the canonical pattern.
- Clarified that manual `Run workflow` starts the production build pipeline and does not itself publish to Google Play.
- Clarified upload key vs Play App Signing key responsibilities.
- Added update-in-place and exact-artifact evidence requirements.
- Linked CI / Android Release Golden to the signing Golden.
- Added validator guards so required signing-gate concepts cannot silently disappear.


## 2026-10-09 — Hardening v25.1 / Golden Index v10 / Registry v2

- Hardened App-Factory-Core governance after heavy audit.
- Added schema-based YAML validation with semantic cross-checks.
- Added orphan Golden detection and Index↔Registry status/path checks.
- Split freshness into migration, content review and provider verification.
- Marked provider-sensitive Goldens without fresh provider verification as NEEDS_REVIEW.
- Corrected Google Auth/Supabase provider sensitivity.
- Replaced CI/Release/Web Golden v1 with v2 and immutable current Action SHA pins.
- Updated central validation workflow to actions/checkout v7.0.1 pinned by SHA.
- Added CODEOWNERS, PR template, security/governance docs and explicit license policy.
- Added main-branch protection requirements; actual GitHub ruleset remains a repository setting.

# Changelog

## 2026-10-09 — Factory Core v25 / Golden Index v9

- Created `riccardopinato/App-Factory-Core` as the canonical Factory source of truth.
- Added deterministic `CURRENT.yaml` resolver.
- Consolidated Master Prompt v25 FULL with central-repository anti-drift rules.
- Added stable `MASTER_PROMPT_CURRENT.txt` and `GOLDEN_INDEX_CURRENT.txt` aliases.
- Imported 28 current Golden documents into categorized paths.
- Added `GOLDEN_REGISTRY.yaml` with status, category, freshness and provider-sensitivity metadata.
- Added App Factory bootstrap instructions and example manifest.
- Added repository validation script and GitHub Action.
- Archived v24 FULL Master and Golden Index v8 as the migration baseline.

## 2026-10-07 — Factory v24 / Golden Index v8

- Full consolidated Master Prompt.
- Assembly First / Golden First.
- Added bootstrap, capability health, Android native reliability, signing identity, portability, entitlement, onboarding, responsive visual QA and offline content-pack candidate Golden modules.
