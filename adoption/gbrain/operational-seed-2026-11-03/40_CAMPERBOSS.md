# GBRAIN_OP_CAMPERBOSS_2026_11_03 — Operational memory

DERIVED SECONDARY MEMORY; AS-OF 2026-11-03; source-inspected, no vehicle documents, locations or private travel history imported.

Repo `riccardopinato/CamperBoss`, main SHA **cf4202e25bf3bc630f9cfe5e3823219acfba84b4**.
- README: https://github.com/riccardopinato/CamperBoss/blob/cf4202e25bf3bc630f9cfe5e3823219acfba84b4/README.md
- Roadmap: https://github.com/riccardopinato/CamperBoss/blob/cf4202e25bf3bc630f9cfe5e3823219acfba84b4/ROADMAP.md

Product: local-first Flutter camper utility with Android/Web release targets. iOS release and IAP deferred. Vehicle profile, private documents, trip planner, checklist, maintenance, offline POI/maps, GPX and local search are described in code/README; no automatic account or cloud required. Do not import private documents or location histories to GBrain.

Roadmap: steps 1–6 and 8–15 DONE, with step 7 residual BLOCKED. Step **16 Release Core BLOCKED**; 16Q specifically **BLOCKED — EXTERNAL RUNTIME / STORE EVIDENCE**. 16R source hotfix software DONE, device retest required. Step **17 Local AI** remains TODO, forbidden to claim active before Release Core evidence. Software tests, release candidates and AppLab fixtures do not establish physical offline MapLibre no-network proof, Google Play Internal Test delivery, real browser storage QA, accessibility or battery/FPS/RAM benchmarks.

Commercial/legal integration boundary: production routing requires server-side proxy; direct ORS key/client access is DEV ONLY, Open-Meteo public API limited to approved noncommercial use; offline bulk style/provider requires explicit approval; no credentials in Flutter or this memory. The release endpoint, license and privacy inventory must be current before commerce.

Reuse lessons: scoped offline packages, bounded backup/import and local lifecycle, provider-neutral adapter, distinction source PASS vs released/certified. For any next step, check latest `ROADMAP.md`, branch/main publication and exact SHA tests, not merely old step labels.
