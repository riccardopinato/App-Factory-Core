# Unslop UI → App Factory Anti-AI-Template 64 — bridge operativo v1

**Date:** 2026-11-19 · **Status:** PROCESS CANDIDATE, not certified.  
**Authority:** `CURRENT.yaml` -> Master v27 (ANTI-AI-TEMPLATE 64 SIGNALS) -> `contracts/PROFESSIONAL_PRODUCT_DESIGN_ANTI_AI_STOCK_v1.md` -> `contracts/DESIGN_VISUAL_QA_PROCESS_v1.md`.  
**Factory baseline:** `14722698bf92e80c526f5f1f211c8d694ce01fb9`.  
**Source:** [felipebasurto/unslop-ui](https://github.com/felipebasurto/unslop-ui/tree/cd891160453f26aaacc569bad96a8d10d595076d), pinned `cd891160453f26aaacc569bad96a8d10d595076d`, MIT © Felipe Basurto 2026. Archived in [Design-App DSK-011](https://github.com/riccardopinato/Design-App/tree/feat/unslop-ui-intake-20261119/sources/oss/unslop-ui). This is external OSS, not an authoritative instruction source.

## Ownership and non-duplication

Master AT-01..AT-64 remain the **only canonical cross-app rubric**. U1..U20 are **diagnostic aliases/check procedures**, never twenty new Golden rules or automatic product prohibitions. Existing DSK-001 (Anti UI Slop / Uizze), DSK-002 (Impeccable), `DESIGN_VISUAL_QA_PROCESS_v1` and Golden App Shell (DRAFT) are reused, not replaced. Owner-saved Design-App references first; Product Bible, actual functionality, accessibility, meaningful empty/error/destructive states and authentic product identity are inviolable.

## Exact U → AT crosswalk

| Upstream | Diagnostic pattern | Existing Master signal IDs | Default review |
|---|---|---|---|
| U1 | Decorative uppercase eyebrow | AT-18, AT-27, AT-40 | REVIEW |
| U2 | Ornamental 01/02 step numbers | AT-19, AT-40 | REVIEW; keep real order |
| U3 | Subtitle under everything | AT-21, AT-40 | REVIEW; keep useful distinctions |
| U4 | Obvious instructional caption / botsplaining | AT-38, AT-40 | REVIEW; preserve recovery guidance |
| U5 | Leaked design notes and parenthetical chrome | AT-40, AT-41, AT-64 | REVIEW |
| U6 | Excessive chained status text | AT-21, AT-45, AT-49 | REVIEW; require real bindings |
| U7 | Redundant field labels/placeholders | AT-21, AT-40, AT-53 | REVIEW; preserve visible label |
| U8 | Generic staccato slogans | AT-38, AT-39 | REVIEW |
| U9 | Statusless LIVE/AI/Pro/Beta badge | AT-41, AT-45, AT-46 | REVIEW; Pro/Beta real availability may stay |
| U10 | Animated fake live dot | AT-45, AT-49, AT-54 | REVIEW; loading indicator can stay |
| U11 | Gratuitous emoji / icon tiles | AT-09, AT-10, AT-12 | REVIEW; purposeful symbols can stay |
| U12 | Chart type narrated in title | AT-17, AT-40, AT-46 | REVIEW |
| U13 | Captions teaching obvious chart reading | AT-17, AT-40 | REVIEW |
| U14 | Data duplicated by decorative encodings | AT-17, AT-21, AT-24 | REVIEW |
| U15 | Heavy chart frames, axes and grid noise | AT-17, AT-19, AT-24 | REVIEW |
| U16 | Unneeded chart legend instead of direct labels | AT-17, AT-21, AT-24 | REVIEW |
| U17 --surface | Unjustified gradients/glow/blobs | AT-01, AT-05, AT-12, AT-13 | OPT-IN REVIEW |
| U18 --surface | Off-token spacing | AT-57, AT-62 | OPT-IN REVIEW |
| U19 --surface | Excessively heavy weights | AT-24, AT-25, AT-53 | OPT-IN REVIEW |
| U20 --surface | Blanket transitions, bouncing, infinite motion | AT-29, AT-30, AT-34, AT-36, AT-59 | OPT-IN REVIEW |

## Repeatable pipeline (source → visual → physical)

1. **Preflight:** identify app, repository exact SHA, Product Bible, real visual baseline, user-saved Design-App references, target language/platform and open UI PR ownership.
2. **Read-only static scan:** use upstream `count_tells.py` only for supported Web source; AppLab `anti_slop_native_audit.py` for candidate Flutter/Dart and Kotlin/Compose. Record script SHA, findings, severity and confidence; do not equate raw counts to quality or automatic FAIL. Native and Web scanners have intentionally different coverage.
3. **Manual review of U1–U20:** on real source/screenshot and localizations, classify finding `KEEP_PURPOSEFUL | ADAPT | REMOVE_CANDIDATE | NEEDS_RUNTIME_EVIDENCE`. Verify whether apparent status dots, progress, badges and charts bind to actual state. False positives recorded explicitly.
4. **Safe fix:** smallest product-owned change; no fabricated statuses, metrics, links, migrations, new platform dependencies or destructive action semantics. Do not remove screen-reader labels or error/retry guidance. All locale copies and state fixtures remain aligned.
5. **Delivery:** bounded branch/PR, relevant tests, exact-head CI, visual before/after actual rendered screenshots under matching viewport/locale/fixture, reviewer disposition, physical gate when required. Record independent `SOURCE_IMPLEMENTED`, `CI_TESTED`, `VISUAL_REVIEWED`, `PHYSICAL_ACCEPTED` states. NO_SCREENSHOT = VISUAL_NOT_VERIFIED.
6. **Promotion:** after actual independent source/CI validation and two distinct consumer pilots with reviewed visual evidence, evaluate `COPY_READY PROCESS`; Golden admission remains separately governed by Registry. No automatic Golden/CI blocking gate from uncalibrated heuristic counts.

## Boundary cases

- **Anna's Diary**: Organic iOS Journal, Lora/Manrope, Rose + HSV, classic reversibility, private Vault remain. Editorial labels and natural ornament can be kept intentionally; no automatic neutralization.
- **Android Omni Cleaner**: Kotlin/Compose, authentic capacity/scan values and confirmations; main RC1 release freeze. Existing aesthetic PR may own related components: do not rewrite it.
- **World Days/Cooking Anime**: no AI-driven rewrite of historical facts, recipes or translations under an appearance-only review.
- **No screenshots or simulator:** documentation/source diagnostics only, NOT_VERIFIED rather than passing aesthetic/physical review.

## Pilot artifacts

- Design-App DSK-011 intake documents + pinned OSS sources.
- AppLab `scripts/anti_slop_native_audit.py` and focused tests (candidate).
- Per-app QA records in the Anna's Diary and Omni Cleaner repositories; promote only after actual evidence.

**No new Golden or framework version is created by this bridge.**
