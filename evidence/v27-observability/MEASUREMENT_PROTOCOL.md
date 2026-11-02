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

## Daily collection: scoped final-head CI observations (30 October 2026)

The first daily increment appends **12 merged PRs** to the existing 40:
3 Anna, 3 AppLab, 6 Cooking Anime (including one activation-crossing
transition PR). Cooking Anime is the repository
`riccardopinato/In-Cucina-con-gli-Anime`. CamperBoss and TrailPath had
no new merged PRs in this observation window.

For these 12 PRs, **41 sampled pull_request workflow runs** were verified
on each PR's final head SHA; all returned `conclusion=success` and
`run_attempt=1`. Optional record fields:
- `ci_observed_final_head_sha`: SHA used for this limited CI sample;
- `ci_observed_run_ids`: actual GitHub Actions run IDs;
- `ci_observed_final_head_rerun_attempts`: sum of observed
  `run_attempt - 1` for those sampled runs, **not all retries in the PR**;
- `ci_observed_last_success_at`: latest observed successful workflow
  update timestamp for that final head, **not proof of all required checks**.

Keep `ci_retries` and `ci_green_at` null until the **complete PR
history**, including earlier head SHAs, required status contexts and
reruns, has been verified. A zero in the scoped final-head field does
not establish zero failed attempts or reruns over the PR lifecycle.
PR description pinning of a Factory SHA is a contemporaneous **declared
task baseline**, not proof of model obedience or a speedup. For a
documentation-only PR which merely records adoption, do not assume
that Factory v27 was used in the actual development task.

## Daily collection: 31 October 2026 (UTC source timestamps)

Append **22** deduplicated merged PRs to the previous 52 (total **74**):
- Anna's Diary: 7 (#154, #156, #157, #159–#162), including UI5 and v1.08 motion.
- AppLab: 2 (#213–#214), FULL shadow pilot and source-only watcher.
- Cooking Anime: 6 (#47–#52), Quality Engine v2.1–v2.4-B.
- Design-App: 7 (#3–#7, #9–#10), reusable design-toolkit components; **not** a deployed app and never a direct app-runtime comparison.
- CamperBoss and TrailPath: no newly merged PRs in this window; their source-gate PRs remain open.

Of the 22: **12 v27_confirmed** by a contemporaneous PR description with exact pinned Factory SHA, **10 post_v27_unverified**. This proves only declared task baselines, not actual model behavior. **72** final-head pull-request workflow runs were sampled by GitHub API with matching head SHA, `conclusion=success`, `run_attempt=1`; zero *observed final-head reruns*, **not** zero failures or retries over complete PR histories. Anna #162 explicitly reports failed CI on an earlier head. Do not replace `ci_retries=null` with zero. No active-time, request-to-first-edit, or causal speedup data became available.

Historical Anna baseline remains **ACTIVE_WORK_BASELINE_NOT_MEASURED**. Open-window overlap detection is per repo and counts only sampled ledger records; avoid conflating PR wait time with effort or treating 22 additional PRs as independent active-work sessions. Exclude documentation-only and toolkit work from consumer-feature productivity claims. Repo `Idee-app-Archivi-riferimenti` and central `App-Factory-Core` changes are governance/ideas, not shipped app-development PRs, and are not added to this app ledger.

## Daily collection: 1 November 2026 (UTC source timestamps)

Append **33** new, deduplicated, merged PRs to the previous **74**
(total **107**), all in `riccardopinato/Agenda-per-Anna` (#163–#198,
excluding #165, #181 and #182 which were not merged in this sample).
Of these, **12 feature**, **7 bugfix**, **8 QA/release** and
**6 governance/docs**. No newly merged app PRs were found for AppLab,
CamperBoss, TrailPath, Cooking Anime or Design-App in the GitHub search
window; App-Factory-Core and Idee-app-Archivi-riferimenti are excluded
as central Factory/governance rather than app delivery.

**3 feature PRs (#191, #193, #195) explicitly pin the contemporaneous
Factory v27 task baseline** `632a66dce4aa00e8e1700b0a3e4dfc7ea008197c`;
the other **30** are `post_v27_unverified`. #185 references a Factory
SHA in a documentation-only planning PR; this is **not** enough to
attribute actual development to v27. A pinned PR description indicates
declared usage, not independent proof of agent behavior.

**91 final-head pull_request workflow runs** were inspected via GitHub
REST using exact head SHA; all were `completed/success`, each
`run_attempt=1`. Thus **0 observed reruns on sampled final heads**,
NOT zero failed earlier revisions or zero full-PR retries.
Keep `ci_retries` and `ci_green_at` null because full CI lifecycle
and required-check set were not independently audited. Source PR #165
was closed without merge and is excluded from delivery counts.

Of the 33 newly appended Anna PRs, **15 have overlapping PR-open
windows** with another merged Anna PR in the cumulative ledger. The
raw median opening→merge duration for this new group is **8.00 minutes**,
which is **NOT active coding time**. By category the raw medians are:
feature 9.85 min (n=12), bugfix 7.98 min (n=7), QA/release 6.42 min
(n=8), governance/docs 4.75 min (n=6). Do not infer a model or Factory
speedup: the source scope and parallelism differ, and no comparable
pre-v27/v27 independent groups reach the protocol's minimum sample size.
Historical Anna baseline stays `ACTIVE_WORK_BASELINE_NOT_MEASURED`.

The report describes observed GitHub delivery latency only, not user
request→first edit, active effort, end-to-end QA, model equivalence or
causal savings. Prioritize timestamped task-start/first-meaningful-edit
evidence and comparable CI durations (cold/warm cache), with source
links, before claiming an improvement.

## Daily collection: 2 November 2026 (UTC source timestamps)

Append **7** deduplicated merged PRs to the previous **107** (total
**114**), all in `riccardopinato/Agenda-per-Anna` (#201–#207):
**4 feature**, **2 QA/release**, **1 governance/docs**.
No new merged PRs were returned by GitHub's merged-PR search for
AppLab, CamperBoss, TrailPath, Cooking Anime
(`In-Cucina-con-gli-Anime`) or Design-App for the period since
1 November UTC. The global author search likewise showed only
Anna app PRs plus governance/capability-catalog PRs, which are
excluded from this app-delivery ledger.

**All 7 are `post_v27_unverified`.** Neither the PR descriptions nor
sampled PR discussion comments contained a contemporaneous,
task-specific Factory baseline SHA. Date of work alone cannot prove
Factory usage. Aggregate cohorts after append: **37 pre_v27**,
**3 transition_excluded**, **22 v27_confirmed** (previously documented),
and **52 post_v27_unverified**.

**22 final-head `pull_request` workflow runs** were sampled using
the exact PR head SHA; all reported `completed/success` and
`run_attempt=1`. **Important:** the Android native compile run on
#205 and on #207 finished **after their PR merge timestamps**.
Thus the 22 successes do not establish that every check was green
*before* merge, nor that the full PR lifecycle had no failed earlier
head/retries. Keep `ci_green_at=null` and `ci_retries=null`; the
observed-final-head rerun count is **0**, narrowly scoped.

The new raw PR open→merge median is **9.85 minutes** (7 PRs).
#203 and #204 have overlapping PR-open windows; this is evidence
of non-independent elapsed PR windows, **not** of concurrent active
coding. Exclude them as independent comparison samples. The
new entries have no verified request→first-edit timestamps or
active-work measurements. Anna's historical baseline remains
`ACTIVE_WORK_BASELINE_NOT_MEASURED`; no causal v27 speedup can
be claimed. Open staging PRs #199 and #200 are not counted as
merged delivery.

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

Recommended cadence: collect and aggregate once per day, with a concise
update only when evidence materially changes, plus a report when the user asks. This is telemetry on **existing GitHub evidence**, not monitoring
ChatGPT invisibly between chats. The central ledger can be updated as new
source-backed data becomes available; do not treat scheduled summary text
as a substitute for a persisted PR record.
