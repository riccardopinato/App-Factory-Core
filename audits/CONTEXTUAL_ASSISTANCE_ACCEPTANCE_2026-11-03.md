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

## Evidence to fill
- Factory reference-engine exact-head CI: PENDING
- Notes consumers exact-head and merged-main CI: PENDING
- Anna consumers exact-head and merged-main CI: PENDING
- Device / tablet / offline long-run proof: NOT VERIFIED
- Public release and retention impact: NOT VERIFIED
