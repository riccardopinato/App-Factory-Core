# Changelog

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
