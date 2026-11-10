# App Factory v27 — Master Legend

> GENERATED navigation index. Do not edit manually or use as a second policy source.
> Baseline authority: `CURRENT.yaml` → Master Core → relevant modules → relevant Golden.

## Canonical documents

- **Master Core:** `v27/candidate/MASTER_CORE_v27_CANDIDATE.txt`
- **Router and immutable seals:** `v27/candidate/MODULE_MAP.json`
- **Full operative text (generated):** `v27/candidate/MASTER_FULL_FALLBACK_GENERATED.txt`
- **Existing public commands:** `commands/REGISTRY.json` and `commands/LEGGENDA.md`
- **Reusable components and freshness:** `golden/GOLDEN_REGISTRY.yaml` and `golden/GOLDEN_INDEX_CURRENT.txt`
- **Agent operating contract:** `AGENTS.md`

## Legacy instruction modules (byte-exact v26.8 section allocation)

| Module | File | Sections | Task selectors |
|---|---|---|---|
| `authority-execution` | `v27/candidate/modules/00-authority-execution.txt` | 0, 1, 1.1, 1.2, 1.3, 2, 6, 13, 49 | governance, policy, permission to modify, parallel execution |
| `foundation-reuse` | `v27/candidate/modules/10-foundation-reuse.txt` | 3, 4, 5, 7, 8, 9, 10, 10.1, 11, 44, 45, 45A, 46, 47, 48 | new app, architecture, golden reuse, dependency |
| `data-offline` | `v27/candidate/modules/20-data-offline.txt` | 12, 14, 15, 16, 17, 18, 19, 20 | migration, database, backup, sync, media, offline |
| `identity-native` | `v27/candidate/modules/30-identity-native.txt` | 21, 25, 26, 27, 28 | auth, permission, native Android, notification, privacy |
| `experience` | `v27/candidate/modules/40-experience.txt` | 22, 23, 24, 37, 38 | visual UI, onboarding, localization, web preview, performance |
| `monetization-ai` | `v27/candidate/modules/50-monetization-ai.txt` | 29, 30, 31 | billing, premium, ads, AI |
| `delivery-verification` | `v27/candidate/modules/60-delivery-verification.txt` | 32, 33, 34, 35, 36, 43 | CI, APK, release, signing, physical QA |
| `audit-roadmap` | `v27/candidate/modules/70-audit-roadmap.txt` | 39, 40, 41, 42 | audit, roadmap, severity, remediation |

## Specialized policy modules (v27 overrides/additions)

| Module | File | Selectors | Review item IDs |
|---|---|---|---|
| `factory-policy-sync` | `v27/candidate/modules/80-factory-policy-sync.txt` | master prompt, app factory core | — |
| `interactive-mockup-review` | `v27/candidate/modules/81-interactive-mockup-review.txt` | mock-up interattivi, interactive mockups, visual design review | — |
| `capability-sync` | `v27/candidate/modules/82-capability-sync.txt` | capability, capabilities, capability registry, portfolio capability synchronization | — |
| `command-legend` | `v27/candidate/modules/83-command-legend.txt` | legenda, command directory, available commands | — |
| `portfolio-commands` | `v27/candidate/modules/84-portfolio-commands.txt` | stato, prossimo, allinea, roadmap, backlog, riprendi, golden, donor, factory, adotta factory, nuova app, ci, test, ripara, apk, deploy, store, peso, sicurezza, ux, monetizzazione, mercato, idee, stelle, stars capability audit, GitHub stars | — |
| `product-family-router` | `v27/candidate/modules/85-product-family-router.txt` | mobile app, web utility, desktop utility, game factory, technology stack | A01, R05 |
| `web-utility-data` | `v27/candidate/modules/86-web-utility-data.txt` | seo, market, data provider, web utility, public data, tutorial audit | A02, A03, A09, R06 |
| `portfolio-operations` | `v27/candidate/modules/87-portfolio-operations.txt` | portfolio, wip, priority, cost, checkpoint, gbrain, github stars, real development time | A04, A05, A08, A10, M03, M05, M06, M09 |
| `verification-boundaries` | `v27/candidate/modules/88-verification-boundaries.txt` | source-only, evidence, physical QA, provider, release, privacy metrics, golden freshness | A06, A07, A11, M01, M02, M04, M07, M08, R01, R02, R03 |
| `modular-navigation` | `v27/candidate/modules/89-modular-navigation.txt` | master legend, modular master, mockup decisions, legacy cleanup | M10, R04 |

## Router map

| Route | Modules | Golden IDs |
|---|---|---|
| `legend` | command-legend | — |
| `mockup_interactive` | experience, interactive-mockup-review | app_shell_responsive_visual_qa |
| `factory_update` | authority-execution, factory-policy-sync, modular-navigation | agent_governance |
| `audit` | audit-roadmap | — |
| `capability_sync` | authority-execution, audit-roadmap, capability-sync | single_donor_capability_admission, scoped_donor_capability_catalog, roadmap_fast_continuous_maintenance |
| `cmd_stelle` | authority-execution, audit-roadmap, capability-sync, portfolio-commands | single_donor_capability_admission, scoped_donor_capability_catalog |
| `roadmap` | audit-roadmap | roadmap_fast_continuous_maintenance |
| `ui` | experience | app_shell_responsive_visual_qa |
| `code` | foundation-reuse | code_hygiene |
| `data` | data-offline | backup_recovery |
| `native` | identity-native, verification-boundaries | android_native_reliability |
| `native_pin` | identity-native | android_local_pin_verifier_keystore |
| `auth` | identity-native | google_auth_supabase |
| `monetization` | monetization-ai, portfolio-operations | entitlement_contract |
| `ai` | monetization-ai | — |
| `delivery` | delivery-verification, verification-boundaries | immutable_build_test_artifact |
| `cmd_stato` | audit-roadmap, portfolio-commands, portfolio-operations | — |
| `cmd_prossimo` | audit-roadmap, portfolio-commands, portfolio-operations | — |
| `cmd_allinea` | authority-execution, audit-roadmap, portfolio-commands | — |
| `cmd_roadmap` | authority-execution, audit-roadmap, portfolio-commands, portfolio-operations | — |
| `cmd_backlog` | authority-execution, audit-roadmap, portfolio-commands | — |
| `cmd_riprendi` | audit-roadmap, portfolio-commands, portfolio-operations | — |
| `cmd_golden` | foundation-reuse, portfolio-commands | — |
| `cmd_donor` | foundation-reuse, portfolio-commands | — |
| `cmd_factory` | authority-execution, factory-policy-sync, portfolio-commands, modular-navigation | — |
| `cmd_adotta_factory` | authority-execution, foundation-reuse, portfolio-commands | — |
| `cmd_nuova_app` | authority-execution, foundation-reuse, portfolio-commands, product-family-router | — |
| `cmd_ci` | delivery-verification, portfolio-commands | — |
| `cmd_test` | delivery-verification, portfolio-commands | — |
| `cmd_ripara` | authority-execution, delivery-verification, portfolio-commands | — |
| `cmd_apk` | authority-execution, delivery-verification, portfolio-commands | — |
| `cmd_deploy` | authority-execution, delivery-verification, portfolio-commands | — |
| `cmd_store` | delivery-verification, monetization-ai, portfolio-commands | — |
| `cmd_peso` | experience, delivery-verification, portfolio-commands | — |
| `cmd_sicurezza` | identity-native, data-offline, portfolio-commands | — |
| `cmd_ux` | experience, portfolio-commands | — |
| `cmd_monetizzazione` | monetization-ai, portfolio-commands | — |
| `cmd_mercato` | audit-roadmap, monetization-ai, portfolio-commands, portfolio-operations | — |
| `cmd_idee` | authority-execution, audit-roadmap, portfolio-commands, portfolio-operations | — |
| `web_utility_specialist` | product-family-router, web-utility-data | — |
| `product_family_specialist` | product-family-router | — |
| `portfolio_observatory` | portfolio-operations, audit-roadmap | — |
| `platform_evidence` | verification-boundaries, delivery-verification | — |
| `master_navigation` | modular-navigation, factory-policy-sync, authority-execution | — |
| `source_admission` | web-utility-data, foundation-reuse | — |
| `controlled_pilot_activation` | authority-execution, delivery-verification, verification-boundaries | — |
| `factory_governance_change` | authority-execution, factory-policy-sync, modular-navigation | — |
| `cmd_avanti` | authority-execution, audit-roadmap, portfolio-commands, portfolio-operations | — |
| `cmd_avanti_roadmap` | authority-execution, audit-roadmap, portfolio-commands, portfolio-operations | — |

## How to use this index

1. Resolve `CURRENT.yaml` once and pin the Factory commit SHA.
2. Classify the user's task and respect public-command isolation.
3. Load only its registered modules and relevant Golden/consumer evidence.
4. On ambiguity or invalid module seals, use the verified synchronized fallback or BLOCK.
5. Treat E3 donor, E5 consumer, CI, device, provider, deploy and Store as distinct evidence.

## Review intake coverage

All 27 selected options from 2026-11-10 are assigned exactly once in the table above: 
A01–A11 (add), M01–M10 (modify) and R01–R06 (retire/clean up conditionally).
A retirement proposal never authorizes deletion of protected history or bypass of a gate.

This navigation index does not prove runtime behavior, commercial viability or source availability.
