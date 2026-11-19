# Semantic QA Engine v1 — reusable App Factory capability

Status: **3-CONSUMER TECHNICAL REUSE VERIFIED / NOT GOLDEN** (actual independent semantic-model evidence and Golden admission still pending). Domain: public editorial content, local-first Flutter apps. No app-runtime dependency.

## Scope and capability levels

- **P0:** Cooking Anime (Italian authoritative recipe authoring + EN/ES/FR/DE/PT) and World Days (English authoritative observance narratives + IT/ES/FR/DE/PT) normalize canonical IDs and compare content without changing app data. Domain-specific adapters own schema and risk rules.
- **P1:** `reference_engines/semantic_qa/semantic_qa.py` is one shared, pure-stdlib Python engine; downstream repositories pin the Core **commit SHA** and consume it through a thin adapter. No copy/paste divergent engines.
- **P2:** Up to 100 source IDs per lane, 1–8 concurrent independent comparisons, fingerprint-keyed incremental cache, optional two-pass independent semantic review, bounded, deterministic JSON reports. No automatic source mutation, merge or content overwrite.

## Real semantic review vs offline scans

Offline mode is **not** meaning-level AI. It tests field parity, missing locales, measurable number anchors and protected entity mentions, and builds work queues. All offline passes remain `OFFLINE_REVIEW_REQUIRED`, never `SEMANTICALLY_CERTIFIED`.

Actual meaning-level review uses the Responses API with `text.format=json_schema` and evidence-rich issues on each source/translation pair. It checks omissions, reversals, cooking instructions, chronology, factual claims, false friends, context, units and idiomatic vocabulary. This requires explicit `--provider openai --allow-external --model <approved-model>`, a configured `OPENAI_API_KEY` secret and `privacy=PUBLIC_EDITORIAL` in the normalized dataset. No implicit cloud calls, AI billing, creation of credentials or personal-content exfiltration.

The optional `--second-pass` obtains an independent reviewer opinion with no access to the first verdict. Model disagreements are REVIEW; concrete unsafe changes are HOLD. Outputs are advisory and do not verify external sources. Official dates, event origin, anime appearance, safety of raw food and medical claims still require authoritative evidence where appropriate.

## Data contract

```json
{
  "schemaVersion": 1,
  "adapter": "cooking_anime",
  "privacy": "PUBLIC_EDITORIAL",
  "sourceLocale": "it",
  "targetLocales": ["en", "es", "fr", "de", "pt"],
  "domainRubric": "Compare culinary techniques, amounts, times, safety and ingredients.",
  "records": [
    {
      "id": "recipe_000051",
      "source": {"title": "...", "steps": {"step_1": "..."}, "ingredients": {}},
      "translations": {"en": {"title": "...", "steps": {"step_1": "..."}, "ingredients": {}}},
      "protectedTerms": ["chashu"],
      "context": {"servings": 2},
      "sourceRefs": []
    }
  ]
}
```

`report.json`: per-ID/locale verdicts, evidence, cache hits, model-used flag, issue codes and certification=NOT_CERTIFIED. `cache.json`: only results keyed by hash of input, engine version, model, second-pass configuration and rubric. Changes to source, locale, model or rubric force re-review. Avoid storing private text in cache or reports.

Recommended commands:

```bash
python3 reference_engines/semantic_qa/semantic_qa.py --input corpus.json --report report.json --cache .semantic-qa-cache.json --provider offline --batch-size 100 --workers 4
python3 -m unittest discover -s tests -p 'test_semantic_qa_engine.py'
```

## QA acceptance

- 100% canonical ID coverage where the adapter is configured for that catalog; missing/duplicate IDs fail closed.
- No silent English fallbacks as valid target translations. Structural failures and obvious unsafe instructions become HOLD; uncertain number/unit conversions become REVIEW.
- Two independent model passes available for high-risk changes; don't treat AI PASS as an external certification.
- Fast Track publishes only accepted source edits by normal app authoring workflow, deterministic compilers, GitHub PR and exact-head CI.
- On all reports clearly distinguish `OFFLINE_ONLY`, `AI_SEMANTIC`, `HOLD`, `REVIEW`, `integrated_main`, `branch_PR`.
- Performance is benchmarked by **cache hits and comparisons skipped**, not promised wall-clock speedups.

## Future adapter reuse

Notes, Wonderlog, Edu and other apps may adopt the same adapter contract after checking data privacy, user consent, domain semantics and offline UX. **Anna's Diary/private notes must never be sent to a cloud semantic provider by default**. Local-only deterministic audit or opted-in private/on-device provider is the safe boundary.

Provenance: feature requested and approved in App Factory conversation on 2026-11-19. Source references: Cooking Anime `tool/fast_track_catalog_audit.py` (donor triage), World Days editorial source and its English master. This capability is NOT registered as a COPY-READY Golden.

## FrameLab pilot — regional Portuguese contract (engine 1.0.1)
- Third consumer: `riccardopinato/FrameLab-Google-AI-Studio`, authoritative published editorial records only (`editorial/catalog/package.json`), EN original vs IT/ES/FR/DE/PT/**pt-BR**. The separate `pt` and `pt-BR` variants are never collapsed or silently skipped.
- Technical photography-specific rubric: exposure (EV, ISO, aperture, shutter), focusing, optics, framing, measurement units and sequence of exercises; do not mistake fluent generic advice for faithful translation of camera-setting instructions.
- Exclude `needsReview`, private PDF/OCR workspace, personal notes, images and user profiles. Only public, rights-cleared editorial record text is eligible for a separately authorized semantic provider.
- Engine 1.0.1 adds `pt-BR` to the allowed locale contract, with regression and cache-isolation checks. Existing pinned adopters are compatible; refresh consumers' immutable SHA explicitly.
- This is an additional independent reuse pilot, **not an automatic new Golden certification**. An offline PASS is never proof of semantic equivalence, technical accuracy or editorial sign-off.

## Independently verified consumer adoption — 2026-11-19

All three applications consume the same source implementation `reference_engines/semantic_qa/semantic_qa.py`, centrally pinned to immutable **App-Factory-Core@827a271dcbd8f1608afabb60ca07184b20926991** (engine v1.0.1, including distinct `pt` and `pt-BR`).

| Consumer | Main merge evidence | Exact-head CI evidence | Canonical source and offline comparison scope |
| --- | --- | --- | --- |
| Cooking Anime | [PR #61](https://github.com/riccardopinato/In-Cucina-con-gli-Anime/pull/61), main `285e1820787090625270fb25f618151d7295e006` | Semantic QA, R1 Quality Engine, Development checks PASS | 162 IT-source recipes × EN/ES/FR/DE/PT = **810** |
| World Days | [PR #149](https://github.com/riccardopinato/World-Days/pull/149), main `c339131b129d497db7de7d116b1157fec7f6975a` | Semantic QA and Development checks PASS | 463 EN-source *published dossiers* × IT/ES/FR/DE/PT = **2,315**; **not** entire World Days catalog |
| FrameLab | [PR #4](https://github.com/riccardopinato/FrameLab-Google-AI-Studio/pull/4), main `f022e1cca01849ff44356c96d4c32f694d65df64` | Semantic QA on exact PR head PASS and post-merge main PASS | 38 EN-source public published photography records × IT/ES/FR/DE/PT/pt-BR = **228**; 1 `needsReview` excluded |

**Total: 3 independently integrated consumers, 663 unique source records within these scoped datasets, 3,353 source-to-target comparison entries.** All observed engine comparisons are in `OFFLINE_ONLY` / `OFFLINE_REVIEW_REQUIRED` mode. The three green technical pipelines establish reuse, normalized coverage and structural checks, **not semantic translation accuracy, source factuality, professional certification or a Certified Golden**.

Known next QA requirement: independent meaning-level review on actual public editorial data with explicit user approval of external model/fees, evidence for discrepancies and remediated source fingerprints. FrameLab [issue #5](https://github.com/riccardopinato/FrameLab-Google-AI-Studio/issues/5) tracks a concrete candidate loss of technical exposure-setting instructions. Follow the separate Golden Index/Registry admission and consumer-specific privacy/security gates for any future promotion.

## Zero-paid-AI delivery and domain triage — 2026-11-19

**Explicit consumer constraint:** no paid AI API calls in the three app workflows. The current consumer YAML files no longer offer a paid provider selector, model input or `OPENAI_API_KEY` secret; they invoke the shared SHA-pinned engine only with `--provider offline`. Core retains its optional adapter capability, but consumers cannot invoke external models through these workflows without an explicit new code change. GitHub-hosted workflow minutes are a separate infrastructure resource and are not represented as "free" by this evidence.

| Consumer | PR / main merge | Zero-API editorial evidence | Meaning-level limits |
| --- | --- | --- | --- |
| Cooking Anime | [PR #62](https://github.com/riccardopinato/In-Cucina-con-gli-Anime/pull/62), `main@16b264d1c949d1d15e0b635c344d2cffb2b21c07` | Full 810-pair offline coverage and 112-recipe Fast Track inventory; corrected EN false positive for legitimate word `marinate`; 0 lexical hits, **112 still needing contextual review** | [Issue #63](https://github.com/riccardopinato/In-Cucina-con-gli-Anime/issues/63) documents degraded multi-language descriptions of Tori Tsukune and preserves 74°C/egg-safety instruction |
| World Days | [PR #150](https://github.com/riccardopinato/World-Days/pull/150), `main@94aec2ea6d36f0a0c7edae1128ae3a199408c090` | 2,315-pair offline coverage; 23 year-anchor/provenance REVIEW findings across 6 dossiers in last pre-merge run; decade recognition reduces heuristic false positives | [Issue #151](https://github.com/riccardopinato/World-Days/issues/151) retains six dossiers requiring historical and multilingual review |
| FrameLab | [PR #6](https://github.com/riccardopinato/FrameLab-Google-AI-Studio/pull/6), `main@d70ad10138382e2eef64bc191905d7ef79ac2e7a`; [repair PR #7](https://github.com/riccardopinato/FrameLab-Google-AI-Studio/pull/7), `main@4bce03ac2ff6b8af3d16536afa4b28193874e749` | Detected **180** specific procedures missing across 30 public lessons, repaired all **30 × 6** translated bodies, bumped package/content version 2→3, matched bootstrap version, passed catalog validation and Flutter editorial CI exact-head, and reduced this defect class to **0** | All **228** language comparisons still `OFFLINE_REVIEW_REQUIRED`; absence of one known defect pattern cannot certify semantics of the 8 untouched lessons or all revised passages |

The work includes editorial assistance performed **within the ongoing ChatGPT conversation**, without external billable model endpoints. This is human-readable/in-chat assisted text revision plus offline quality evidence, not an independent second paid-model review and not professional language or subject-matter approval. No user images, private OCR/PDF workspace, recipe source scans, family notes or personal data were sent to an external semantic provider.

**Admission status:** THREE-CONSUMER REUSE VERIFIED, OPEN SEMANTIC CERTIFICATION. No automatic elevation to `CERTIFIED GOLDEN` in the registry; a formal promotion needs independent defensible context review and rights/source gates. Zero-paid-API work may continue using source-grounded in-chat inspection and domain-focused deterministic tests without requiring external model fees.
