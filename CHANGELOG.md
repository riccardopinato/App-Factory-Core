# Changelog

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
