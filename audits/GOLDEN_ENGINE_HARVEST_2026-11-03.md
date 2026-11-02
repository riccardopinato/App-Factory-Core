# App Factory — Engine Harvest v27 — 03/11/2026

Factory baseline at start: riccardopinato/App-Factory-Core@a3c65963e9f060f1a02de96ade1b0985a4adcdab
Master v27, Golden Index v26, Golden Registry v2.

## Scope
Full implementation of CATALOG/CONTRACT stage for all eight previously
identified engines plus six existing Golden consolidations. No app production
source changed, no new cross-app Dart package falsely claimed. This audit
does not assert consumer runtime, physical/provider or publication certification.

## Eight distinct Golden candidates
| ID | Owner contract | Donor(s) | Status |
| --- | --- | --- | --- |
| gpx_interoperability_engine | validated GPX import/export | TrailPath + CamperBoss | DRAFT |
| hybrid_local_search_engine | lexical/optional semantic, ranking | Notes-Ecosistema + CamperBoss | DRAFT |
| civil_date_recurrence_engine | civil Gregorian recurrence/override | World Days + Anna's Diary | DRAFT |
| local_rules_automation_engine | local triggers/decisions | Notes-Ecosistema | DRAFT |
| infinite_canvas_ink_engine | world transforms, strokes, reversible ops | Notes-Ecosistema | DRAFT |
| spatial_clustering_engine | zoom grid or radius clusters | CamperBoss + Wonderlog | DRAFT |
| explainable_recommendation_engine | reasons, stable score/diversity | FrameLab + Wonderlog | DRAFT |
| performance_regression_fixtures | deterministic synthetic CI fixtures | CamperBoss + Notes-Ecosistema | DRAFT |

## Six consolidation lanes (seven existing files, no duplicate Golden)
1. Import/Export Portability: GPX format adapter, Notes Markdown and staged commit.
2. Offline Content Packs: concrete CamperBoss POI installer with integrity;
   differentiate it from the NoopOfflinePackageInstaller placeholder.
3. Backup/Recovery: CamperBoss, Notes, Anna layered staging/safety snapshot,
   rollback and physical file reconciliation boundaries.
4. Versioned Editorial Catalog: FrameLab exact-source tests, World Days and
   Cooking Anime human rights/translations/quality boundary.
5. Incremental Persistent Indexing: CamperBoss revision-driven freshness and
   Notes embedding fingerprint/invalidation; no misleading physical benchmark.
6. Immutable Evidence / Donor Admission: two existing processes updated with
   exact original-source checkout plus separate workflow-head SHA pattern.

## Evidence references
TrailPath pinned original source 3f44ab37c0881e4315033797c451cec723e23cd2,
CI: https://github.com/riccardopinato/TrailPath/actions/runs/41536514653
FrameLab pinned original source e7538d7dfc484f81f37a8e4363cd56a5b742e804,
CI: https://github.com/riccardopinato/app-fotografia/actions/runs/41536521211
CamperBoss main cf4202e25bf3bc630f9cfe5e3823219acfba84b4,
CI: https://github.com/riccardopinato/CamperBoss/actions/runs/38570040742
Notes-Ecosistema 3fd9b0df5ab3b7470c65721b4bad7f3fd8c59e6c,
CI: https://github.com/riccardopinato/Notes-Ecosistema/actions/runs/36594580169
Wonderlog 5e07317571df85fbda770583cc3d56cb3aa85040 (source-equivalent
Flutter Foundation pass; differing tested head changed web preview workflow):
https://github.com/riccardopinato/Wonderlog/actions/runs/37625261077
Anna's Diary 827bb61620960d8867eb03e453d142013aada786,
CI: https://github.com/riccardopinato/Agenda-per-Anna/actions/runs/41458618496
World Days and Cooking Anime source/test paths cited in Golden appendices;
these are process donor observations, not new matching-source CI certification.

## Portable acceptance fixtures and validation
contracts/engine_reuse_acceptance_v1.json contains 20 positive/rejection/
unresolved expectations for the top four engines. This is implementation-neutral
input/output test data for future consumer adapters.
scripts/validate_engine_harvest.py checks all eight docs, seven updated files,
registered status, provenance and test vector shape in Factory CI.
This structural check CANNOT prove that a Dart engine passes these vectors.

## Explicit remaining gates
- Implement/extract framework-neutral reference ports and run the vectors
  against actual Dart implementations; no cross-project runtime library exists.
- For each consumer run focused and full exact-head tests, detect superseded
  implementations, document license and adaptation delta.
- Test GPX real exports, optional semantic retrieval against user corpus,
  calendar DST/locale on target platform, automation persistence and recovery,
  canvas stylus/device memory, map anti-meridian, ranking eligibility and
  performance on real devices when applicable.
- Promote to COPY-READY only after actual extracted generic code/harness is
  proven. E3 donor capability must never be presented as E5 app-wide reuse.
- No Master v27 modification or full fallback regeneration is necessary: policy
  remains unchanged and only Golden catalog contracts/evidence were added.
