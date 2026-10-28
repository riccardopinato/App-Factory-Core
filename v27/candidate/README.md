# App Factory v27 — Modular Master release candidate

CURRENT.yaml on this release branch selects the Core at `v27/candidate/MASTER_CORE_v27_CANDIDATE.txt` (original candidate path retained for stable pointers) and the manifest marked ACTIVE. The manifest registers relevant on-demand modules, status/freshness-aware Golden selection and source Git blob identities.

The operative full fallback at `v27/candidate/MASTER_FULL_FALLBACK_GENERATED.txt` is generated from Core + all 55 legacy sections + policy updates + task route catalog; CI verifies its byte identity. Never hand-edit fallback or diverge it from modular rules. Keep `master/MASTER_PROMPT_CURRENT.txt` as a legacy mirror of the short Core, not of the generated full fallback. The complete original v26.8 remains immutable historical emergency recovery, not current policy.

The proof-of-behavior gates remain mandatory: 16 paired cases on a genuine matching model/effort, unique provider request IDs, real token/time receipts, independent semantic review with zero critical regressions, and real workflow completion measurements. The current draft PR MUST NOT be merged without those checks, even if its source-integrity CI is green.

GitHub cannot update the ChatGPT Project settings: the Project instructions must be aligned separately to `bootstrap/PROJECT_CUSTOM_INSTRUCTION.txt`.
