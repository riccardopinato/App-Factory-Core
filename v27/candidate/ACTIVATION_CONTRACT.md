# App Factory v27E — Promotion and rollback contract (preflight only)

Current authoritative baseline: Master v26.8. This document describes
a **future promotion**, not permission to skip evidence or governance checks.

## Already prepared
- v27 modular core, registered modules, generated synchronized full fallback.
- Deterministic route selection, Golden Registry freshness warnings, fallback integrity.
- Schema/validator v7 can validate either v26.8 CURRENT or future v27 CURRENT.
- Shadow resolver tests construct an isolated mock v27 CURRENT to ensure
  correct modular loading and fail-closed behavior without modifying main.
- v27D1 static 11-case replay; v27D2 16-prompt tokenizer benchmark.
- For all future Master/Core updates: change modular source and regenerate
  full fallback in the SAME PR; retain versioned historical v26.8 untouched.

## Promotion gate — ALL required
1. **Real paired-model evidence:** 16 x 2 independent runs, same model,
   reasoning effort, task and project context; input hashes, provider request
   IDs, actual model responses and token/time receipts. No fixtures posing as model output.
2. **Independent semantic review:** zero severe regressions on PIN/Keystore,
   data migration, audit-only, exact-head CI, human release authority, fallback
   validity, external untrusted prompts, or unauthorized rollout.
3. **Operational benchmark:** real comparable time-to-first-edit and validated
   integration/merge observations; state the limits of the sample. Tokenizer
   reduction alone does not prove latency savings.
4. **Atomic activation PR** on exact current main, with:
   - CURRENT.yaml master.version = "27"; master.path = registered v27 core;
     master.versioned_path = synchronized full fallback; modular_manifest set.
   - Manifest status/router ACTIVE; Golden Registry master_version = "27";
     core and generated fallback remove candidate-only claims; regenerate pins.
   - Bootstrap and Project instruction pointer adopt version-aware flow.
     The ChatGPT Project settings are external to GitHub and must be aligned
     separately; changing repo pointer does not alter those settings automatically.
   - README, changelog, validator and schema agree on version, paths and fallback.
   - Old complete v26.8 source is retained read-only as emergency recovery.
   - All required CI, review, exact-head and mergeability checks GREEN.
5. **Rollback drill:** if activation reveals critical policy/routing regressions,
   revert the activation PR on a protected branch with checks. No silent
   downgrade to the archived v26.8 while still advertising v27.

## Activation decision
**HOLD** while real paired-model runs and real workflow-time evidence are
unavailable. Do not set CURRENT v27 based only on simulated shadow tests.

Future activation is a new atomic PR, not a direct push to main.

## Optional real-model evidence capture pathway

After the user configures the OpenAI API secret and explicitly dispatches the manual workflow, use its actual response artifact as provenance for the 16 paired cases. An independent reviewer must verify each answer; a completed API run alone does not authorize activation. This workflow has not been run merely by merging its definition. Do not store API credentials in the repository or in output artifacts.
