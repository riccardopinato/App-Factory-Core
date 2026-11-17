# Design review and visual evidence contract v1

**Status:** PROCESS CANDIDATE / NOT CERTIFIED · 2026-11-17
**Authority:** App-Factory-Core CURRENT -> Master v27, section 23; Theme M3 (COPY-READY), App Shell/Responsive/Visual QA (DRAFT), AppLab QA Adapter (CERTIFIED PROCESS). Product Bible and app roadmap retain all product/design decisions.
**Evidence source:** Design-App Impeccable DSK-002, PR #34, merge `ae190d5bed59a37bebf7189d7a26b6647a797440`. This is a workflow reference, not an imported Flutter/Android package.

## 1. Ownership and boundaries

- App-Factory-Core defines cross-app technical constraints, Golden admission and release truth.
- Design-App curates references, per-app design suggestions, visual QA checklists and reusable design candidates.
- Each app's Product Bible defines its actual brand, approved screen hierarchy, content, controls and product scope. Its roadmap coordinates rollout.
- AppLab is the runtime/evidence verifier; a reviewer's aesthetic approval is a separate decision.
- In conflicts, apply Master/Golden technical requirements before selecting a Design-App resource; never use a design example to override privacy, safety, data, accessibility or release constraints.
- No blanket style enforcement across apps; validate internal consistency for the particular product.
- Do not create another runtime UI implementation, token library, data owner, router or dependency without an identified gap and admission decision.

## 2. Bounded workflow — eight inherited gates

| Gate | Question | Minimum evidence |
|---|---|---|
| IWC-01 Context | Are app, task, Product Bible, brand and target platforms known? | Exact source SHA, approved visual constraints and scope |
| IWC-02 Direction | Is mockup-first or code-first justified, with no implicit product change? | Target screens, intended outcome, up to three alternatives only when valuable |
| IWC-03 Critique | Are actual current screenshots reviewed for hierarchy, density and content priority? | Findings, screenshot paths/URLs, severity and reviewer disposition |
| IWC-04 Technical audit | Does layout work with accessibility, insets, keyboard and supported form factors? | Font scale, semantics/focus, >=48dp touch where applicable, no overflow |
| IWC-05 Resilient states | Do empty/loading/offline/error/timeout/permission states explain the real behavior? | Per-state test cases; do not show fictitious progress or success |
| IWC-06 Polish | Are typography, palette, spacing, images and motion coherent and purposeful? | Before/after on same fixtures; reduced-motion and performance check |
| IWC-07 Reuse | Is the existing Golden/donor/design token preferable to new code? | Candidate identifier, origin/license, reuse mode and consumer validation |
| IWC-08 Platform split | Which evidence is Web vs Flutter/Android native? | Separate evidence per target; Web tooling never certifies native runtime |

Small isolated visual fixes may link to existing context/evidence instead of rerunning every phase; no mandatory new feature or ten-screen redesign.

## 3. Evidence manifest (per surface, per source)

Store a JSON or Markdown manifest in the app repository or a linked evidence artifact. Suggested stable fields:
`app`, `target_repo`, `source_sha`, `source_branch_or_pr`, `screen_id`, `approved_design_ref`, `platform`, `device_or_viewport`, `locale`, `font_scale`, `theme`, `state`, `before_image`, `after_image`, `test_run_url`, `visual_findings`, `technical_findings`, `reviewer_decision`, `runtime_gate`, `physical_gate`, `notes`.

Statuses: `PLANNED`, `CAPTURED`, `REVIEWED`, `PASS`, `FAIL`, `BLOCKED`, `NOT_VERIFIED`, `NOT_APPLICABLE` (reason mandatory for last). Missing screenshots always mean `NOT_VERIFIED`, never `PASS`. Record negative results and unavailable test environments explicitly.

**Visual review** must use real app screenshots; mockups and Play Store illustrations are not runtime screenshots. Compare same screen/state/data fixture and viewport. Baseline updates require an explicit reason and review; never auto-accept screenshots merely because CI regenerated them.

**Technical checks** independently cover semantics/TalkBack/VoiceOver, touch/focus, large text, light/dark/system, locale elongation/RTL where supported, small and large screens, tablets where targeted, gesture/3-button insets, keyboard, ad/no-ad, offline/error and reduced motion. Add performance measurement when animation, gallery or rendering is affected.

**Trust ladder:** `SOURCE_IMPLEMENTED` -> `CI_TESTED` -> `RUNTIME_VISUAL_REVIEWED` -> `PHYSICAL_ACCEPTED` -> `RELEASE_CERTIFIED`; each label requires independent existing AppLab/Release Reality evidence. The visual approval of a screen does not promote the app to STORE READY.

## 4. Review rubric

Use findings `BLOCKING` (unreachable control, privacy/safety/cropped content, deceptive state), `MAJOR` (legibility, hierarchy, overflow, missing content), `MINOR` (spacing, typography inconsistency) and `OPTIONAL` (subjective preference). Record why. Do not turn the rubric into a fictitious 9/10 score without a real observation.

Anti-patterns to inspect, not blanket bans: nested cards, excessive modals, flat hierarchy, overused gradients, motion without state purpose, clipping, misleading CTAs, duplicated instructions and excessive loading chrome. Respect each app's approved visual language.

## 5. Platform/tooling

Impeccable's Web HTML/CSS detector and hooks can support Web/PWA review after dependency/setup approval. They are not Android/iOS native analyzers and do not provide Flutter widget runtime certification. Native Flutter/Compose uses source tests, real screenshots, accessibility/instrumentation and AppLab trusted runtime/physical lanes as warranted. No dependency or hook is installed by this contract.

## 6. Pilot and reusable pattern promotion

First pilots: Anna's Diary (Today, Calendar, Memories, Settings; preserve Organic iOS Journal, Manrope/Lora, rose/HSV, private Vault and Classic) and Android Omni Cleaner (Home, dedicated Clean/Gallery/Privacy, real video player, deletion safety). Pilot files should cite exact app main and any concurrently open UI PR; do not rewrite active branches.

Only after actual consumer implementation and evidence can a visual component become `SOURCE_VERIFIED` / `LIBRARY_VERIFIED` / `COPY_READY` in Design-App. Golden promotion remains exclusively governed by Core Golden Registry and its independent reuse/validation requirements. No automatic promotion from this document.

## 7. Exit rule

A design mini-step may be marked source-complete when the approved UI code is merged with exact-head checks. It is marked **visual-accepted** only with actual screenshot evidence and explicit review outcome. It is marked **native/physical validated** only after the applicable device gates. Keep these statuses separate in all PR summaries and reports.
