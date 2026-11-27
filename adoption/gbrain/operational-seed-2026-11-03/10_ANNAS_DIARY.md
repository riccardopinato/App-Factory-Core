# GBRAIN_OP_ANNA_DIARY_2026_11_03 — Operational memory

DERIVED SECONDARY MEMORY; AS-OF 2026-11-03; no user diary data. Not an APK certification. Before action re-read original Product Bible, roadmap, relevant contracts and current code/CI.

Repository `riccardopinato/Agenda-per-Anna`, main SHA **cb477cbecc85c1b1c415c60fd69bbd128fb82904**.
- Product Bible: https://github.com/riccardopinato/Agenda-per-Anna/blob/cb477cbecc85c1b1c415c60fd69bbd128fb82904/docs/PRODUCT_BIBLE.md
- Roadmap: https://github.com/riccardopinato/Agenda-per-Anna/blob/cb477cbecc85c1b1c415c60fd69bbd128fb82904/docs/ROADMAP.md
- Architecture and implementation must be checked separately, not inferred from the Bible.

Scope and invariants: Flutter local-first diary and personal agenda, daily timeline, memories, reminders, bounded explicitly shared space, private vault, user-initiated interoperable copies/links. Canonical data stays with its owner. Avoid duplicate persistence/write paths and silent bidirectional sync; do not expand export of private content. Private Vault and passwords are never material for GBrain. Reusable engineering architecture may be indexed; private user records and keys must not be imported.

Verified documentary status from roadmap dated 2026-11-02: stable-signed ARM64 artifact **1.0.0-rc.6+120**, source **fb476545426fb6bf290e74f53e735fa13616e4e9**, workflow **41367895694** SUCCESS. Product records **USER_ATTESTED_GENERAL_PASS**, NOT per-scenario PHYSICAL DEVICE VERIFIED. Quick Wins 2 merged PR **#211** after the +120 source pin; other current source changes likewise require newly signed versionCode > 120 for device testing. PR #206 daily quick wins, #203 permission diagnostics and #204 visual regression tooling merged; the 70 real approved and candidate screenshots remained missing. Privacy UX PR **#200** remains DRAFT / DO NOT MERGE; Google Calendar API PR #199 staged only; do not bypass security review.

Open evidence: version upgrade with data inventory, private vault and two-device flows, native notifications/Web Push, Play purchase, 70-pair visual screenshots and individual device scenarios. Release +120 does NOT include later merged source work. Never infer Play publication. Ask for exact tested versionCode and hash if physical validation is requested.

Reusable knowledge: bounded capture and daily projections; permissions diagnostics as observability rather than proof of delivery; strict comparison tooling requires real pixel baselines; privacy UI masking is not encryption. For any new release, first reconcile current main SHA, product truth, exact artifact/version and per-scenario evidence.
