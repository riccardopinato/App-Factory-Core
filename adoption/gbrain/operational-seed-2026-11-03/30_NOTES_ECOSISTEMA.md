# GBRAIN_OP_NOTES_ECOSISTEMA_2026_11_03 — Operational memory

DERIVED SECONDARY MEMORY; AS-OF 2026-11-03. No personal notes, document contents, credentials, private graph or user files included.

Repo `riccardopinato/Notes-Ecosistema`, main SHA **3fd9b0df5ab3b7470c65721b4bad7f3fd8c59e6c**.
- README: https://github.com/riccardopinato/Notes-Ecosistema/blob/3fd9b0df5ab3b7470c65721b4bad7f3fd8c59e6c/README.md
- Roadmap: https://github.com/riccardopinato/Notes-Ecosistema/blob/3fd9b0df5ab3b7470c65721b4bad7f3fd8c59e6c/ROADMAP.md
- Need real-device proof for native Needle: `flutter_app/NATIVE_NEEDLE_0_56_3.md`.

Product: local-first, private-by-default Flutter workspace; active implementation in `flutter_app/` (Kotlin 0.25 is historical branch). Source roadmap lists **0.56.3+74 Native Needle Runtime Activation** implemented; hardware certification still PENDING. 0.55.0 search uses local deterministic 192-dimension sidecar and lexical/semantic hybrid retrieval with index rebuild and purge. Whiteboard 0.54.1–0.54.3 supports sketch layer, pan/zoom, bounding ink, mini-map, with stylus/tablet physical QA separate.

AI boundary in 0.56.3: local provider chain **Needle 3 20L → Gemini Nano → deterministic fallback**, all suggestions validated and user-reviewed; no automatic destructive action or cloud fallback. Native ARM64 runtime approx **1,663,992 bytes** in base APK; Needle model `needle3.cact` approx **35,335,380 bytes** delivered via optional Play AI Delivery pack `notes_needle3_20l`. Notes Plus billing/RevenueCat remains separate; release builds remain Free until real billing is integrated. **38 MiB soft target**, not a hard prohibition; model-weight leakage into base APK remains a hard fail. No model weights belong in GitHub or GBrain.

Do not conflate code/CI/AAB packaging with actual installed Play pack, real physical ARM64 benchmark, RAM/performance, stylus QA or release monetization. Future action requires exact SHA, real APK/AAB evidence, device pack installation and measured quality/latency/RAM.
