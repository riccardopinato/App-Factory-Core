# App Factory v27 — Modular Master release candidate

CURRENT.yaml on this release branch selects the Core at `v27/candidate/MASTER_CORE_v27_CANDIDATE.txt` (original candidate path retained for stable pointers) and the manifest marked ACTIVE. The manifest registers relevant on-demand modules, status/freshness-aware Golden selection and source Git blob identities.

The operative full fallback at `v27/candidate/MASTER_FULL_FALLBACK_GENERATED.txt` is generated from Core + all 55 legacy sections + policy updates + task route catalog; CI verifies its byte identity. Never hand-edit fallback or diverge it from modular rules. Keep `master/MASTER_PROMPT_CURRENT.txt` as a legacy mirror of the short Core, not of the generated full fallback. The complete original v26.8 remains immutable historical emergency recovery, not current policy.

**Controlled, zero-cost v27 activation:** the required release gate is now the documented exact-head validation, 16-case source-level policy review, fail-closed tests, atomic activation and rollback plan. See `ACTIVATION_CONTRACT.md` and `pilots/V27E_ZERO_COST_SOURCE_REVIEW_2026-10-29.md`. The former 32-call paid-model evaluation remains optional; no behavioral-equivalence or ChatGPT speedup certification is claimed. Any critical policy regression still blocks promotion.

GitHub cannot update the ChatGPT Project settings: the Project instructions must be aligned separately to `bootstrap/PROJECT_CUSTOM_INSTRUCTION.txt`.
