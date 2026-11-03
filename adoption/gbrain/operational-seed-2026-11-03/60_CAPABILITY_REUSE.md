# GBRAIN_OP_CAPABILITY_REUSE_2026_11_03 — Operational memory

DERIVED SECONDARY MEMORY; AS-OF 2026-11-03; business/engineering catalog metadata, no private content.

Repo `riccardopinato/Idee-app-Archivi-riferimenti`, main SHA **07a7dc4dabc73082e803f52a9bc697ca5229f9b8**.
- Central catalog README: https://github.com/riccardopinato/Idee-app-Archivi-riferimenti/blob/07a7dc4dabc73082e803f52a9bc697ca5229f9b8/12-CAPABILITY-E-IMPLEMENTAZIONI/README.md
- Catalog system of record: `12-CAPABILITY-E-IMPLEMENTAZIONI/REGISTRO_CAPABILITY.json`.
- Build/check: `python3 scripts/build_catalog.py --check`.

The README reports a dated 2026-11-01 snapshot of **147** capability IDs, **48** app/idea beneficiaries and **342** app-capability links. These numbers are historical and MUST NOT be labeled current counts. Stable CAP ID describes responsibility across apps; `app_states` distinguish implementation per app. `SOURCE_REPORTED` != `SOURCE_VERIFIED`; CI PASS != device PASS. P1/P2/P3 opportunity scoring is NOT P0–P3 bug severity. A catalog occurrence is not a pre-approved deployment.

When starting app work: scan existing CAP IDs and relevant Golden Registry before inventing a new component; reuse/extend before duplicate; check actual donor code, LICENSE, ToS, costs, storage footprint, privacy, commercial-use rights, SHA and tests. CAP proposals (including Hugging Face/NotebookLM research) are not permission to install external models, enable background AI, call paid APIs or migrate private data. Research cannot be promoted to runtime status without target app evidence.

The 2026-11-03 Anna CAP audit is a source/evidence reconciliation only; not physical Android verification. Do not import raw whole catalog blobs to GBrain: keep a curated summary and pointers that can be independently re-read from GitHub.
