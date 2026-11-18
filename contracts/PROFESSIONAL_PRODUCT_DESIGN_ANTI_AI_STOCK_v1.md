# Professional Product Design — Anti AI-Stock Standard v1

**Date:** 2026-11-19  
**Status:** ACTIVE DESIGN POLICY COMPANION; process and expectations, NOT a certified Golden or external library.  
**Owner:** App-Factory-Core Master v27 (resolved through CURRENT.yaml).  
**Purpose:** make App Factory products look and behave as professionally designed consumer applications rather than recognizable, interchangeable AI-generated templates.

## 1. Authority and source precedence

1. Product Bible, approved screenshots/mock-ups and explicit owner taste decisions define product identity.
2. Inspect **riccardopinato/Design-App** curated references FIRST. A saved user reference has priority over aesthetic inventions from ChatGPT when suitable/adaptable; record source ID/link and DIRECT / ADAPT / NOT SUITABLE justification. Licenses, accessibility and security remain binding.
3. Reuse existing approved product-specific design tokens and compatible internal donor/Golden technical contracts; do not start from a random new design kit.
4. For unresolved visual direction, inspect original screens on Dribbble / Collect UI and sources already cataloged in Design-App (Ruixen, Uiverse, etc.). Research *the particular surface*, not the entire site.
5. For implementation consult Flutter style-neutral widget primitives (https://docs.flutter.dev/ui), official packages (https://pub.dev/), Flutter Gems category (https://fluttergems.dev/) and maintainers of any Forui/Mix/shadcn_ui/etc. package. For motion, prefer native first, Rive only for meaningful stateful design with profiling (https://pub.dev/packages/rive).
6. Support quality practices from Design-App curated DSK-001 Anti UI Slop, DSK-002 Impeccable, DSK-004 Emil Design Engineering, DSK-008 Better Interfaces and DSK-009 UI UX Pro Max. These are **design/QA references**, not automatically executable Flutter SDK code; Web hooks do not prove native UI.

External package list and example app screens are discovery/reference, never mandatory aesthetic choices. Validate source, version, platform, license, permission, binary impact, maintenance and integration tests individually. No automatic donor/Golden promotion.

## 2. Definition of an original, professional-quality app

Each app needs a meaningful distinct visual language, not merely a new accent color:
- **Audience and brand**: what users are doing; personality, contrast, accessibility, icon and copy treatment coherent with the domain.
- **Art direction**: product-specific palette (neutrals + meaningful accents where appropriate), distinctive but readable type scale, spacing rhythm, media treatment and composition.
- **Information architecture**: prioritized data and actions, predictable navigation, progressive disclosure and content density appropriate to task.
- **Interaction design**: stateful feedback, real actions, sensible gestures, transitions where they communicate direction/state, accessible focus and reduced-motion support.
- **Systematic consistency**: UI primitives, typography, corner radii, elevations, icons and motion documented as reusable tokens; screen variants follow shared logic but need not look identical.
- **Realistic polish**: populated and empty screens both look intentional; loading/permission/offline/error/retry states are truthful; images keep proper aspect ratios; forms and long localized text fit.

Do **not** imply that AI use is absent; the standard concerns observable product quality, not author identity. No detector can reliably decide from visual style alone who wrote a UI.

## 3. Visual anti-pattern review (not an unconditional blacklist)

Flag and justify any unjustified combination of:
- default blue/purple gradients, generic rounded hero cards, uniform overrounded card grid;
- randomly mixed radii, borders/shadows everywhere, glass blur, neon glow, ubiquitous pastel/purple sheen;
- generic icons, emojis used as substitute for iconography, random stock/AI illustrations, unlicensed assets;
- pseudo-bento grids with equal visual weight or arbitrary asymmetry;
- lookalike layouts across unrelated product families, empty dashboards and placeholder data presented as true;
- giant headings/hero blocks burying the user's first task, generic praise/marketing copy as UI content;
- needless animation, long delays, low-contrast labels, excess whitespace or overpacked controls;
- copied identifiable competitor appearance or visual brand.

These elements can be appropriate when the Product Bible and UX justify them. A principle is not a ban on a color, shape or framework implementation.

## 4. Lightweight workflow for substantial visual work

**A. Product brief.** Identify target users, one primary job-to-be-done, target platform, screen/state inventory, existing app baseline, constraints and approved identity.

**B. Reference-first.** List 2–3 relevant user-curated Design-App references, or explain why none fits. Cite source IDs/links and use mode (DIRECT/ADAPT/REJECT). Add examples from competitor products only when helpful; research their behavior rather than copying assets.

**C. Art direction.** Decide typography hierarchy, color semantics, spacing/radius/elevation, media style, icon set, navigation, motion and responsive behavior. Record 2–3 anti-references: e.g. 'generic violet dashboard' when inconsistent with this specific product.

**D. Propose/review.** Compare one or more meaningful app screens with content that represents real conditions, including sparse and dense states. For interactive mock-up cycles, respect the existing owner-approval/10-step contract. Do not silently integrate proposed designs.

**E. Build and visual QA.** Preserve app architecture/data/privacy. On exact-source test fixtures, review screenshot pairs, empty/populated/dark/light, long strings/large text, small/large screens and tablet/Web when targeted; verify touch/keyboard/TalkBack/VoiceOver, reduced motion, scroll performance, APK size, state truth and route discoverability. Reference `contracts/DESIGN_VISUAL_QA_PROCESS_v1.md` (IWC-01..IWC-08) and AppLab, not a new QA engine.

**F. Aesthetic acceptance.** Record reviewer disposition `APPROVED`, `REVISE`, `REJECTED` or `NOT_VERIFIED` separately from source `IMPLEMENTED`, exact-head CI and physical/store gates. If screenshots are missing, report `NOT_VERIFIED`, never visual PASS. Design strength is a review judgment supported by explicit observations and the selected references, not a fabricated objective "AI percentage".

Small isolated UI copy/accessibility fixes can use existing project design tokens and evidence without a full research cycle.

## 5. Reuse/maintenance

Store approved product-specific decisions in the app's own design/product records and Design-App app dossier (not a duplicate Product Bible). A repeatable validated pattern can be nominated for donor/Golden evaluation only with source provenance, tests and appropriate consumer evidence. Never create a single universal look for all apps.

## 6. Examples of acceptable differentiation

- **Anna's Diary:** preserve its approved personal diary art direction; editorial typography, memories with real media and calm hierarchy. Do not replace it with a generic SaaS dashboard.
- **Notes-Ecosistema:** content-first responsive workspace; robust canvas/editor and structured information density, not a page of decorative cards.
- **Android Omni Cleaner:** precise state/space reporting and trustworthy destructive-action UX; no fake progress bars or security badges.
- **World Days:** readable editorial storytelling and imagery, cultural diversity and accessible typography; not a dashboard palette repeated for every day.
- **Battery Guard / FocusSense:** measured charts and functional, legible controls; no ornamental charts or continuously running visual effects.

No app code or Golden certification is changed by this design contract.
