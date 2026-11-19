# Semantic QA Engine v1 — reusable App Factory capability

Status: **IMPLEMENTED CANDIDATE / NOT GOLDEN** (pending two-app adoption and semantic model evidence). Domain: public editorial content, local-first Flutter apps. No app-runtime dependency.

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
