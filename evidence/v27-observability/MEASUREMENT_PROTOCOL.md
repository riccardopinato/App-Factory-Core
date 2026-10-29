# App Factory v27 — Cumulative development-speed observatory

Status: **ACTIVE DATA COLLECTION**, not a verified speedup or behavioral certification.
Cost: **EUR 0 extra**; no OpenAI API calls, no purchased analytics or additional subscriptions.

## What is measured

Persistent evidence: `DELIVERY_LEDGER.json`, pinning the exact source PR links.
Local read-only report: `python3 scripts/summarize_v27_delivery.py`.
JSON summary: `python3 scripts/summarize_v27_delivery.py --json`.

**Objectively measurable now**
- GitHub PR opening timestamp to actual merge timestamp, UTC, as elapsed wall clock.
- PR category and app repository (classification is heuristic and is reviewable).
- Where actually available later: exact-head CI start/finish, reruns, commits,
  PR review and merge timestamp, source SHA, delivered scope.

**Only with separate provenance**
- User's request timestamp and first meaningful edit timestamp.
- Time to the first validated build and time spent actively coding.
- Whether the app task really loaded v27 (record actual Factory SHA and
  link to contemporaneous task/PR evidence; date alone is insufficient).

**Not measurable from GitHub PR metadata alone**
- ChatGPT internal reasoning duration or its billed/context token usage.
- Actual human/agent active working time rather than waiting.
- Causal effect of v27 with changing app complexity or tools.
- Model-behavior safety equivalence.

## Cohorts and attribution rules

Activation boundary: **2026-10-29 09:14:41 UTC**, commit
`477de1e3cb3788ac828311cb1f04c8bbcfb97be7` on App-Factory-Core.

- `pre_v27`: PR started and merged before the boundary, including older
  v26.x periods. **Not a pure v26.8 baseline.**
- `transition_excluded`: PR was already open before activation and
  merged after. Never use it to claim gains.
- `post_v27_unverified`: PR started after activation but there is no
  documented evidence that the app task adopted v27. Not a v27 treatment.
- `v27_confirmed`: the task started after activation and the actual pinned
  Factory SHA used by the task, with a contemporaneous PR/task evidence URL,
  is available. Merely copying a CURRENT link is insufficient to prove usage.

The initial ledger has **40 merged PRs**, comprising **37 pre-v27**,
**2 transition-excluded** and **1 post-v27-unverified** PRs across Agenda-per-Anna, AppLab, CamperBoss and
TrailPath. These are real GitHub PR timestamps; the source's exact factory
version and first-edit times were generally not recorded, so leave them null.
Never invent these missing fields.

## Accuracy correction — Anna's Diary parallel PRs (29 October 2026)

**PR open→merge is elapsed GitHub latency, NOT coding or ChatGPT working time.**
The initial median of **582.58 minutes** (~9h43m) among eight historical
Anna PRs was numerically correct but **misleading as a development-duration
baseline**. Six of those eight PRs have overlapping open windows:

- #138 opened 2026-10-28 10:35 UTC; merged 20:59 UTC.
- #139 opened 11:47 UTC; merged 22:19 UTC.
- #140–#143 all opened about 13:08 UTC and merged between 22:50 and
  22:51 UTC, within 41 seconds of one another.

The overlapping PR windows prove that these intervals are **not independent
samples of elapsed development work**. Overlap alone does NOT prove concurrent
coding or identify actual active effort. Only two of the eight pre-v27
records lack observed overlap with another PR in the ledger, and they are
different scopes (UI and docs), so **there is no defensible estimate of
active historical Anna development time from this sample**.

The summarizer now reports raw PR latency explicitly as
`raw_pr_elapsed_median_minutes_not_active_time` and the number of
`observed_parallel_window_pr_n`. For descriptive same-app/category
comparisons it does not count overlapping open-window PRs as separate
independent duration samples. This is deliberately conservative, and a
missing overlap in the sampled ledger is NOT proof that there was no other
concurrent PR.

**Never publish `9h43m` as the old development time or promise its
reduction.** With no contemporaneous time-to-first-edit/activity record,
show `ACTIVE_WORK_BASELINE_NOT_MEASURED`.

## Collection workflow during ordinary app development

After each meaningful merged PR or completed roadmap step:

1. Reuse the Factory baseline SHA already pinned for that app task.
   Add a stable line to the PR description or delivery log stating
   `Factory baseline: <sha>` and the relevant task/step. This is evidence
   of declared policy adoption, not proof of model obedience.
2. Record the repo, PR number, title, type, opened/merged dates and canonical
   URL from GitHub (not from memory). Include real CI evidence/reruns when
   available.
3. If start time and first meaningful edit are genuinely observable and linked
   to specific sources, add `request_at`, `first_edit_at`,
   `request_evidence_uri` and `first_edit_evidence_uri`. Otherwise null.
4. Append the new record **once** to `DELIVERY_LEDGER.json` through the
   normal protected branch/PR/CI procedure. Avoid rewriting old records.
   Deduplicate on `repo` + `pr_number`. Do not create a paid background task.
5. Run `python3 scripts/test_v27_delivery_metrics.py` and
   `python3 scripts/summarize_v27_delivery.py --json` before claims.
6. Record additional deployment or issue data only when it is relevant,
   source-backed and inexpensive to collect.

For speed, batch new records into a single evidence-only PR at review time;
do **not** open an App-Factory-Core PR for every app fix.

## Decision criteria for a real time-saving claim

Compare **within the same app and scope category** (bugfix, feature,
integration, QA/release, governance/docs). The summarizer requires at least
**3 independently merged PRs per cohort** per comparable group to display
an exploratory median percentage. More comparable data is preferable.

The formula for a descriptive change in elapsed PR duration is

`100 * (median_v27_minutes / median_pre_v27_minutes - 1)`.

Negative = shorter elapsed PR duration. This is still only a proxy;
PR open->merge includes overnight waiting, human approvals, CI contention,
parallel streams, and task-size differences.
The analyzer detects overlapping open-PR windows and excludes those PRs from
independent PR duration comparisons; the raw historic median remains only
for audit and must not be presented as active development hours. Use similar change size,
dependency/risk tier and scope when interpreting an observed improvement.
Report medians, sample sizes, per-group breakdown and uncertainty rather than
one impressive percentage. Avoid Simpson's paradox from mixing apps.

**Claim `REAL TIME SAVING VERIFIED` only after prospective task measurements
and comparable historical/baseline evidence support the conclusion, with
quality/safety/rework gates not worsened.** A raw PR median alone never
proves a causal gain, and the script deliberately reports
`causal_attribution: NOT_VERIFIED`.

## Owner-friendly reporting

A concise update can include: pre/post sample sizes per app/category,
PR-open->merge medians, exact-head CI retries, request->first-edit times
when genuinely known, linked PR outliers, and a verdict:
`NOT_ENOUGH_DATA`, `EARLY_INDICATION`, or
`REAL_TIME_SAVING_VERIFIED` only with appropriate supporting evidence.

Recommended cadence: aggregate once a week, plus a short update when the
user asks. This is telemetry on **existing GitHub evidence**, not monitoring
ChatGPT invisibly between chats. The central ledger can be updated as new
source-backed data becomes available; do not treat scheduled summary text
as a substitute for a persisted PR record.
