# Language Engine v1 — Fast Track translation memory and QA

Status: **CANDIDATE**. Implementation: 
\`reference_engines/language_engine/language_engine.py\`.
Tests: \`tests/test_language_engine.py\`.

## What is implemented

This zero-dependency, offline engine consumes the **same normalized records**
as \`reference_engines/semantic_qa/semantic_qa.py\`: canonical IDs, sourceLocale,
targetLocales, original structured fields, and locale translations.

- Existing target strings remain untouched.
- Missing target fields are HOLD and produce **non-publishable proposals**:
  exact fingerprint-matching, explicitly \`approved\` memory hits first,
  optional authoring-time machine draft next, otherwise NEEDS_TRANSLATION.
- Preserve ICU-like placeholders, review numeral anchors and domain glossary
  terms. Missing numbers can be false positives when numbers are spelled out
  or units converted; this is REVIEW, not proof of error.
- Import an optional Semantic QA report to carry HOLD evidence into the same
  Fast Track per-record decision. Offline-only checks never become AI_SEMANTIC.
- Partition source records into deterministic <=100-ID lanes (three lanes
  for 201 IDs). Separate execution workers, if used, must own disjoint IDs.
- The engine never edits authoritative source files, publishes translations,
  calls providers or sends data to a service.

## Input contracts

\`--input canonical.json --report build/language-report.json\`
with optional \`--memory memory.json --glossary glossary.json
--drafts draft.json --semantic-report semantic-report.json\`.

Memory:
\`\`\`json
{"entries":[{"domain":"cooking_anime","sourceLocale":"it","targetLocale":"en",
"sourceText":"Incidi la pelle","sourceSha256":"<SHA256 of the exact UTF-8 source text>",
"targetText":"Score the skin","status":"approved"}]}
\`\`\`

Glossary:
\`\`\`json
{"entries":[{"domain":"cooking_anime","source":"daikon",
"targets":{"en":"daikon","de":"Daikon"}}]}
\`\`\`

Drafts must have the same normalized adapter, source locale, target locales
and record IDs as the input. Missing draft IDs or fields remain unresolved.
Only a separate, explicit editorial decision can approve a draft and add its
source-locked fingerprint to memory.

## Wiring with existing Fast Track and other components

1. App adapter exports normalized source/current translations (Cooking Anime:
   \`tool/semantic_qa_adapter.py\`; World Days/FrameLab: own adapters).
2. The app's authoring-time MT adapter (currently Cooking Anime MarianMT) or
   manually curated translations can supply \`--drafts\` if available.
3. Run Language Engine for memory/review/placeholder/terminology triage.
4. Run existing shared Semantic QA against the resulting content through
   the existing app workflow and optionally pass its report into the engine.
5. **Only approved corrections** go to app authoring, deterministic locale
   compiler, tests, PR, exact-head CI and authorized merge.
6. AppLab handles runtime, screenshots, native/device/release evidence as
   separate gates. No app ships this engine or model as an APK dependency.

This is a reusable **translation workflow component**, not a general-purpose
machine translation model. Machine drafts still rely on a pinned provider.
It does not claim translated-content certification or certified Golden status.
No paid API or automatic external/cloud content upload is authorized.

## Test locally

\`\`\`sh
python3 -m unittest discover -s tests -p 'test_language_engine.py' -v
python3 reference_engines/language_engine/language_engine.py \
  --input cooking-normalized.json \
  --report build/language-report.json --batch-size 100
\`\`\`
