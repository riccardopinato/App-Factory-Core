# Contextual Assistance — quality and Donor admission

Date: 2026-11-03. Scope: local, read-only suggestions for Notes-Ecosistema
and Anna's Diary. This is a **QA contract**, not a feature release or a
CERTIFIED GOLDEN promotion.

## Validated dimensions
- Source authorization and visibility MUST precede ranking.
- Duplicate or stale source identity fails closed.
- No automatic write, notification, cloud upload or access to hidden sources.
- Fixed clock and deterministic input order with shuffled-input parity.
- Locales: IT, EN, ES, FR, DE and PT where a consumer supports them.
- Curated tasks: orphan project, actionable checkbox, busy day, event preparation,
  explicit Q/A note, changed/removed source, unconfirmed/declined proposal.
- Record precision@K, recall@K and MRR against **curated ground truth only**.
- Capture false positive/false negative examples; do not claim real retention uplift.
- 500/5000 candidate stress and physical mobile benchmarks are separate gates.

## Consumer requirements
1. Pin donor SHA and exact file blob; record adaptation.
2. Run pure-engine tests on the pinned source.
3. Map only source-visible authorized projections, never Vault/secret data.
4. Present reason code and source link, require confirmation for any edit.
5. Ensure lifecycle invalidation and consistent revisions before committing.
6. Run consumer widget/domain tests, Flutter analyze, release builds and
   physical checks where platform/native behavior matters.
7. Only call an individual capability CERTIFIED DONOR after E3 evidence.
   Independent successful consumer evidence is E5 and does not by itself
   certify device or Store behavior.

## Source-CI evidence verified on 4 November 2026

The following evidence reconciles GitHub's completed Actions runs. It proves
only the checks actually included in those workflows; it is not device or
customer effectiveness evidence.

| Surface | Immutable source / workflow | Result |
| --- | --- | --- |
| Factory main | `5ef3f121c2376450ba8f942a05dd0a9ae0316940` — [Factory validation](https://github.com/riccardopinato/App-Factory-Core/actions/runs/41733571498), [reference-engine Dart CI](https://github.com/riccardopinato/App-Factory-Core/actions/runs/41733571483) | SUCCESS / SUCCESS |
| Factory PR #60 exact head | `7c6cbc26104f66d6ff4357642d934924286d0af7` — [Factory validation](https://github.com/riccardopinato/App-Factory-Core/actions/runs/41733426848), [Dart CI](https://github.com/riccardopinato/App-Factory-Core/actions/runs/41733426390) | SUCCESS / SUCCESS |
| Notes main | `5845e7335ddbdad588affc4ea8f9059fcc5281f9` — [Flutter Port CI](https://github.com/riccardopinato/Notes-Ecosistema/actions/runs/41738362996), [Web Preview](https://github.com/riccardopinato/Notes-Ecosistema/actions/runs/41738362958) | SUCCESS / SUCCESS |
| Notes PR #41 exact head | `4102fc84898bf61af4385acc1d9579ab7ff78ede` — [Flutter CI](https://github.com/riccardopinato/Notes-Ecosistema/actions/runs/41736569912), [Web Preview](https://github.com/riccardopinato/Notes-Ecosistema/actions/runs/41736569771) | SUCCESS / SUCCESS |
| Anna main | `a383c1674365813a468a3ef2d34be27f2d6558a0` — [Development checks](https://github.com/riccardopinato/Agenda-per-Anna/actions/runs/41739763949), [Web](https://github.com/riccardopinato/Agenda-per-Anna/actions/runs/41739763876) | SUCCESS / SUCCESS |
| Anna PR #221 exact head | `a870cee2557b627b073f049edfebe37cd3ead49a` — [Development](https://github.com/riccardopinato/Agenda-per-Anna/actions/runs/41739215313), [Web](https://github.com/riccardopinato/Agenda-per-Anna/actions/runs/41739215355), [AppLab Source Gate](https://github.com/riccardopinato/Agenda-per-Anna/actions/runs/41739215308) | SUCCESS / SUCCESS / SUCCESS |

Factory PR #58 (engine), Notes PRs #39 (Next Action/Inbox) and #40 (Study),
and Anna PR #220 (realistic day/preparation) were also merged. Their follow-up
hardening PRs #41 and #221 are included in the integrated main evidence above.

The [Anna automatic signed-release workflow](https://github.com/riccardopinato/Agenda-per-Anna/actions/runs/41740305682)
concluded SUCCESS on the preflight, but its `signed-apk` job was SKIPPED.
It supplied no release artifact and must not be reported as a fresh signed APK.

## Open certification and effectiveness evidence

- Factory's synthetic suggestion-quality metrics are fixture-relative only.
  Real user precision, usefulness, retention and false-positive rates: NOT VERIFIED.
- Cross-repository source adaptation/provenance and independent consumer E5
  evidence are not established merely by separately green workflows. No automatic
  promotion to CERTIFIED DONOR or CERTIFIED GOLDEN.
- Real Android/iPhone/tablet behavior, notification/calendar provider health,
  offline long-run, account-switch journeys and physical performance: NOT VERIFIED.
- Installation of an APK built from the latest Anna main, Play distribution
  and real-world impact: NOT VERIFIED.
- Keep the candidate Golden in its existing DRAFT status until all scoped
  promotion evidence is explicitly assembled.

## Evidence update — 4 November 2026 (post audit remediation)

The preceding historical snapshot remains valid **for its pinned commits**, but
the earlier signed-APK SKIPPED statement is superseded **for the newer Anna
build +122 only**.

- Factory main `0638862b92a4a64ae380d20a2ea6ba19a4bc76b2` includes
  QA matrix [PR #62](https://github.com/riccardopinato/App-Factory-Core/pull/62):
  50 IT/EN synthetic source gate scenarios, plus deterministic 500/5000-candidate
  fixtures; pure Dart reference CI and Factory validation succeeded. No
  device performance, product precision, independent E5 or E3 proof inferred.
- Notes main `4ecc3e340b9ef94a872da48490f0d61c1adc3bdb` integrates
  source lifecycle safety [#43](https://github.com/riccardopinato/Notes-Ecosistema/pull/43),
  workload/WIP [#45](https://github.com/riccardopinato/Notes-Ecosistema/pull/45),
  feedback-controlled Smart Inbox [#44](https://github.com/riccardopinato/Notes-Ecosistema/pull/44)
  and explicit Markdown study Q/A [#52](https://github.com/riccardopinato/Notes-Ecosistema/pull/52),
  with their exact-head Flutter + Web required checks successful before merge.
  These are source/CI facts, not field-effectiveness receipts.
- Anna main `ab5360b78187a643e2b101be21e6951441406059` from
  [#223](https://github.com/riccardopinato/Agenda-per-Anna/pull/223) passed
  Development, UI5, Web and Android Calendar bridge checks. Automatic
  [signed ARM64 run 41755099241](https://github.com/riccardopinato/Agenda-per-Anna/actions/runs/41755099241)
  has **both release-preflight SUCCESS and signed-apk / build SUCCESS**.
  Manifest records version `1.0.0-rc.6+122`, package
  `com.riccardopinato.agenda_per_anna`, artifact SHA256
  `1e3b81dc698f7cf4246b160a8f4d3372466eb0dc94c9a832edb0546c15fd8e9d`,
  signing cert SHA256
  `31BE63155C831F062238179EC9B8F19D1C16A925BED1D526BC7E6A4712C62DC3`.
  This is **ARTIFACT_BUILT**, not PHYSICAL PASS.
- Physical in-place installation/data continuity, multi-device authorization,
  user-value measurement, E3 Donor and E5 independent-consumer reuse remain
  **PENDING**. Privacy V2 PR #215 remains DRAFT/BLOCKED; Google Calendar #199
  remains PAUSED. No Store deployment or Golden promotion authorized.
