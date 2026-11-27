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

## Opt-in deep triage of pinned PR pairs — new limited capability

The default pull-request workflow continues to execute **only** the lightweight
complete-repo changed-file scan. The optional `deep_pairs` parameter (blank
by default) accepts 1–4 exact open PR pairs in a compact form such as
`75:77,39:77`. It must be explicitly supplied on `workflow_dispatch` or
`workflow_call`; it is not enabled fleet-wide.

The deep reader reuses the same complete, stable snapshot and performs only
read-only, SHA-pinned GitHub compare and recursive Git tree GET requests for
the requested pairs. It caches the file trees per immutable head SHA, rejects
truncated/malformed tree responses and mismatched compare commit identities,
and reports:
- verified ancestor/diverged relationship between **specific PR HEAD commits**;
- identical vs changed Git blob SHA among overlapping changed file paths;
- missing/removed/nonblob paths as **unverified**, never silently equal;
- the number of unexamined overlap pairs and the actual GitHub GET/byte/time cost.

The distinctions are **file-content and commit-ancestry only**. Even 100%
identical selected paths do not certify behavioral equivalence, other
unexamined paths, tests, privacy, user data or merge safety. Any incomplete
deep evidence yields `INCOMPLETE_NO_CLEARANCE`; no false global PASS. The
existing Product Bible, roadmap, AppLab and owner/device checks still govern.

The exact-source Core CI runs dedicated adversarial tests from
`tests/test_openspec_shadow_deep_triage.py`. Apps may opt into the new
`deep_pairs` input after the version has passed exact-head and postmerge CI,
without making deep review a new required gate.

## Audit remediation — correctness, provenance and output safety (2026-11-27)

P1 rendering: any GitHub PR filename, manifest spec_id or delta ID is
untrusted data; before printing into GitHub Actions stdout/step summary it
is HTML/Markdown escaped and control characters (including newline and ANSI)
are rendered as literal hexadecimal escape text. JSON artifacts preserve
original source data for inspection but never execute it.

P1 provenance: each deep pair JSON now records the two exact full PR HEAD SHAs,
commit ancestry, every overlapping path with each side's Git blob SHA and
file mode, missing data and the final HEAD/open-PR inventory recheck. The
workflow uploads immutable execution artifacts (JSON, Markdown and SHA256
checksums) via a pinned upload-artifact action, with 30-day retention and
repository-scoped access. A GitHub Actions CI PASS alone does not certify
semantic equivalence or physical/runtime behavior. No report is a canonical
source of Product Bible changes.

P2 rename/file mode: changed-path overlap now also considers previous_filename
for files marked renamed, without counting a path twice for one PR.
Non-blob, removed or missing paths remain explicitly incomplete for file
comparison; unchanged blob bytes with changed Git file mode are tracked
separately. Renamed-path overlap is review-only; it is not proof of conflict.

P2 Spec Lite: validated real Factory v1 manifest example and previous delta
proposals with offline adversarial tests. An unmapped PR is UNMAPPED.
DECLARED_UNTRUSTED means proposed metadata, never trusted semantic
compatibility; canonical refs must be reviewed independently.

P2 cost: normal read-only PR scans still collect all PRs, their exact
changed files and a later HEAD/PR list recheck; bypassing these would
risk false all-clear. In-memory indexes avoid quadratic PR lookups,
deep tree results are reused for identical immutable SHAs within one run,
and a 500-GET hard budget denies unbounded scans. No cross-run cache,
extra permanent registry, scheduler or server is added. Request/response/
elapsed metrics are uploaded for before/after comparison; any inferred
time/token saving remains NOT_MEASURED without controlled data.

workflow_dispatch is exposed in the two consumer repositories with the
optional deep_pairs input, default empty. A completed PR-event deep pilot
does not substitute for a real manual-dispatch execution. The manual
run must be explicitly tested and logged before marking that gate PASS.
