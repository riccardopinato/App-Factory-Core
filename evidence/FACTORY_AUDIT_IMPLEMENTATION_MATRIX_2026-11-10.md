# App Factory Core — audit implementation and consumer adoption gate

Baseline: 2026-11-10, Master v27 / Golden Index v29.
This is a report of CENTRAL POLICY presence, not of real consumer adoption.
No app repository, provider, paid API, release or live model was modified.

## Original 27-item intake

| Review item group | IDs | Central status | Downstream status |
|---|---|---|---|
| Additions | A01–A11 | Registered in specialized policy modules | NOT_VERIFIED per app |
| Modifications | M01–M10 | Registered in specialized policy modules | NOT_VERIFIED per app |
| Conditional removals | R01–R06 | Recorded with historical-preservation rules | NOT_VERIFIED per app |

Do not represent `policy described` as `implemented in product`.
For each adopting app record repository+HEAD, applicability (YES/NO),
Product Bible approval, module/Golden IDs, app-specific diff/PR,
CI exact-head, real platform/provider test where needed and status
(`NOT_APPLICABLE`, `PLANNED`, `IMPLEMENTED`, `SOURCE_TESTED`,
`DEVICE_OR_PROVIDER_VERIFIED`, `RELEASED`).

## Priority consumers / sample matrix

| Scope | Source reference | Adozione reale | Next proof |
|---|---|---|---|
| Anna's Diary | riccardopinato/Agenda-per-Anna | NOT_VERIFIED in this Core-only audit | compare current app HEAD, UI, data, web and device gates |
| Notes-Ecosistema | riccardopinato/Notes-Ecosistema | NOT_VERIFIED in this Core-only audit | independent consumer source and test evidence |
| World Days | app repository to resolve | NOT_VERIFIED | Web/deploy/data source and provider contract |
| AppLab | riccardopinato/AppLab | NOT_VERIFIED | SOURCE-ONLY central/local gate compatibility |
| Existing Kotlin utilities | per-app repositories | NOT_VERIFIED | native permission/device, source-only vs runtime |

## Live-model evaluation

Static routing, simulated adversarial tasks and tokenizer counts are
NOT real-model behavioral equivalence. Use paired consenting live Chat tasks
with same input scope, captured adherence verdict, wall time and retries;
never infer billed usage or actual speedup from local tokenizer estimates.
No paid OpenAI API is needed for this evidence collection.

## Unresolved issues and PR reconciliation

- Core PR #79: v27 evidence ledger; re-check base, overlap and provenance
  before updating/merging, no stale-head PASS.
- Core PR #41 (draft): optional GBrain evidence; reconcile actual privacy,
  PC availability and restore receipts, do not equate draft with installed.
- Core issues #63, #68, #72: scoped donor/ML consumer E5 evidence remains
  independently required; central reference tests alone do not promote an
  app feature or certified Golden.
