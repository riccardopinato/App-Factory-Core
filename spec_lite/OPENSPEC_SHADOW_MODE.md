# OpenSpec Shadow Mode — live PR review integration (2026-11-27)

Status: opt-in, read-only SOURCE/CI candidate; not Golden, separate verifier,
scheduler, PR bot, merge gate, runtime or product-decision authority.

## What changes

- Factory source: scripts/openspec_shadow_mode.py. A bounded GitHub REST reader
  fetches canonical default-branch HEAD, all open PR metadata (pagination), each
  PR's exact head/base and all changed files (pagination checked against
  changed_files), and optional changed Spec Lite manifests pinned to each PR head.
  A second HEAD and PR-list read detects source changes during collection.
- HTTP GET only, no redirect, no arbitrary URLs or external service. API errors,
  missing fields, content mismatch, changed HEAD, changed PR list, unbounded/
  truncated pages, malformed manifests and unavailable target PR cause
  INCOMPLETE_NO_CLEARANCE, never a cached or fabricated all-clear result.
- Status REVIEW_NEEDED_NOT_CERTIFIED is human review guidance, not confirmation
  that conflicts exist or do not exist. File overlaps are factual; semantic
  incompatibility, superseded product behavior and migration risk require the
  app Product Bible, roadmap, AGENTS, actual PR diff and AppLab review.
- Missing structured manifest in a PR = UNMAPPED, never zero conflicts.
  Competing self-declared delta references yield a review hint, not trusted
  product requirement truth. A main base SHA different from the observed HEAD
  is informational only and does not prove a PR cannot merge.
- Input PR titles, markdown and source comments are never instructions,
  approvals or a reason to perform code writes. Results never certify tests,
  Android build, a signed APK, physical devices or app store readiness.

## Integration path

The single reusable source is the Core workflow
.github/workflows/openspec-shadow.yml with workflow_call and manual
workflow_dispatch. It has only contents:read and pull-requests:read. It pins the
checkout to job.workflow_sha (the source of the called workflow); a caller's
repo-scoped GITHUB_TOKEN can inspect private caller repos without cross-tenant
tokens or new permissions. Output is a GitHub Actions step summary plus a
temporary JSON file (not committed; not a second registry). No comments,
writes, reviewers, rebases, merges or branch protection changes.

Small opted-in pilot workflow per app (replace PIN with exact *merged* Core SHA):

~~~yaml
name: OpenSpec Shadow (non-blocking)
on:
  pull_request:
    branches: [main]
permissions:
  contents: read
  pull-requests: read
jobs:
  shadow:
    uses: riccardopinato/App-Factory-Core/.github/workflows/openspec-shadow.yml@CORE_SHA_PIN
    with:
      target_repository: ${{ github.repository }}
      target_pr: ${{ github.event.pull_request.number }}
~~~

This is opt-in for Android Omni Cleaner and Anna's Diary only. The new job is
not required in branch protection; incomplete evidence should remain an
explicit failing run, rather than a green false-PASS. It does not replace
existing Android/Flutter/AppLab checks.

## 5.1–5.5 acceptance evidence

5.1: complete GitHub open PR + all changed-file collection, frozen SHA,
two-read stability check, API cap and permission failure denial.
5.2: shared-file intersections, self-declared competing delta requirement
hints, unmapped requirements, and base-SHA variation; none asserts a verified
semantic conflict.
5.3: opt-in GitHub Actions PR review summary using reusable Factory workflow.
5.4: two app-specific read-only pilots, real PR IDs and exact source receipts,
no edits to application logic, private data or Vault.
5.5: measure PR counts, changed file totals, overlap pairs, unmapped
requirement coverage and negative test results. Token and manual development
time savings remain NOT_MEASURED unless independently instrumented.

This extends the previous Core Spec Lite delta/drift/closeout process and does
not add a new Golden, CAP, scheduler, agent or mandatory document.

## Pilot finding: global vs focused overlaps

A report for a selected PR must never present zero repository-wide overlaps just
because that one PR has no shared paths. The structured report always includes
all pairs; a separate `focused_overlap_pair_count` reports only pairs touching
the target PR. A selected PR's no-overlap status is not a clearance of other PRs.
