# Golden v28 — scoped independent consumer + execution contract evidence
Date: 2026-11-03
Factory pre-change source: App-Factory-Core@077172920a02cfe45a56d4eba9fa3077d36954e5
No changes Master v27, Index v28, Registry count 59.

Hybrid Search source reference: App-Factory-Core PR #47, current pure Dart in
reference_engines/lib/src/hybrid_search.dart + semantic_embeddings.dart.
E5 LIMITED: independent app Wonderlog PR #21 merged to
main@5e6db031e300f09f5b64db3e1416c62c036907c9; direct source identical
blobs 95de49c3e531451b8984461223a6a5fb1d9cc1f1 and
de96c2dbf0da2c0c4695308efd5b9bbab25b75f5.
Exact-head Flutter Foundation https://github.com/riccardopinato/Wonderlog/actions/runs/41612729813 SUCCESS
Exact-head Apple Gate https://github.com/riccardopinato/Wonderlog/actions/runs/41612729810 SUCCESS
Postmerge Flutter Foundation https://github.com/riccardopinato/Wonderlog/actions/runs/41615273697 SUCCESS
Postmerge Web Preview https://github.com/riccardopinato/Wonderlog/actions/runs/41615273698 SUCCESS
Proved real public-callsite usage of local lexical and optional deterministic
feature hashing; does NOT prove durable index, account isolation across signed
in users, device-permission conditions, trained LLM, native store certification.
Global Golden DRAFT maintained to prevent broad E5 overclaim.

Local Rules: transaction-port-only pure Dart reference Core PR #55 merged
077172920a02cfe45a56d4eba9fa3077d36954e5 with postmerge Dart CI
https://github.com/riccardopinato/App-Factory-Core/actions/runs/41617613583 SUCCESS.
Test-double runs simulate durability/replay under one shared map and fail
before commit; no independent persistent consumer. Global Golden DRAFT.

Search source CI / Local Rules source CI are distinct from consumer validation.
