#!/usr/bin/env python3
"""Free, reproducible PR-lifecycle measurements for App Factory v27.

This reports observed GitHub elapsed time, NEVER active development time or
causal model speedup. No network, credentials, paid API or background process.
"""
from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "evidence/v27-observability/DELIVERY_LEDGER.json"
COHORTS = {"pre_v27", "transition_excluded", "v27_confirmed", "post_v27_unverified"}
CATEGORY = {"feature", "bugfix", "qa_release", "integration", "governance_docs"}
MIN_MATCHED_PAIRS = 3


def parse_time(raw):
    if not isinstance(raw, str):
        raise ValueError("missing timestamp")
    dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("timestamp must include UTC offset")
    return dt


def validate(data):
    if data.get("schema_version") != 1:
        raise ValueError("unsupported ledger schema")
    activation = parse_time(data["v27_activation_utc"])
    seen = set()
    processed = []
    for row in data["records"]:
        key = (row["repo"], row["pr_number"])
        if key in seen:
            raise ValueError("duplicate PR: " + repr(key))
        seen.add(key)
        if row.get("cohort") not in COHORTS:
            raise ValueError("invalid cohort: " + repr(key))
        if row.get("category") not in CATEGORY:
            raise ValueError("invalid category: " + repr(key))
        opened, merged = parse_time(row["opened_at"]), parse_time(row["merged_at"])
        if not opened < merged:
            raise ValueError("invalid PR time order: " + repr(key))
        if row["cohort"] == "pre_v27" and not merged < activation:
            raise ValueError("pre_v27 PR overlaps activation: " + repr(key))
        if row["cohort"] == "transition_excluded" and not (opened < activation <= merged):
            raise ValueError("transition PR not crossing activation: " + repr(key))
        if row["cohort"].startswith("post_v27") and opened < activation:
            raise ValueError("post-v27 PR began before activation: " + repr(key))
        if row["cohort"] == "v27_confirmed":
            if opened < activation or not row.get("factory_baseline_sha"):
                raise ValueError("v27 record lacks post-activation start or pinned Factory SHA: " + repr(key))
            sha = row["factory_baseline_sha"]
            if len(sha) != 40 or not all(ch in "0123456789abcdef" for ch in sha):
                raise ValueError("invalid Factory SHA: " + repr(key))
            if not row.get("baseline_evidence_uri"):
                raise ValueError("v27 baseline attribution lacks evidence link: " + repr(key))
        if row.get("url") != f"https://github.com/{row['repo']}/pull/{row['pr_number']}":
            raise ValueError("missing canonical GitHub PR link: " + repr(key))
        total_minutes = (merged - opened).total_seconds() / 60
        item = dict(row, pr_to_merge_minutes=round(total_minutes, 2))
        requested, first = row.get("request_at"), row.get("first_edit_at")
        if (requested is None) != (first is None):
            raise ValueError("request and first edit require a complete verified pair: " + repr(key))
        if requested is not None:
            a, b = parse_time(requested), parse_time(first)
            if not a <= b <= merged:
                raise ValueError("invalid request to first edit times: " + repr(key))
            if not row.get("request_evidence_uri") or not row.get("first_edit_evidence_uri"):
                raise ValueError("first-edit measurement lacks source evidence: " + repr(key))
            item["request_to_first_edit_minutes"] = round((b-a).total_seconds()/60, 2)
        else:
            item["request_to_first_edit_minutes"] = None
        processed.append(item)
    return processed


def mark_observed_pr_overlap(items):
    """Detect overlapping *open PR windows*, NOT concurrent coding effort.

    Ledger may be a subset of all PRs. An apparent isolated PR means only
    'no overlap observed in the current sample', not actual solo work.
    """
    by_repo = defaultdict(list)
    for item in items:
        item["observed_overlapping_prs"] = 0
        by_repo[item["repo"]].append(item)
    for repo, rows in by_repo.items():
        ordered = sorted(rows, key=lambda item: parse_time(item["opened_at"]))
        episode = []
        episode_end = None

        def flush():
            if len(episode) > 1:
                for entry in episode:
                    entry["observed_overlapping_prs"] = len(episode) - 1

        for item in ordered:
            opened, merged = parse_time(item["opened_at"]), parse_time(item["merged_at"])
            if episode and opened >= episode_end:
                flush()
                episode = []
                episode_end = None
            episode.append(item)
            episode_end = max(episode_end, merged) if episode_end else merged
        if episode:
            flush()
    return items


def summarize(data):
    items = mark_observed_pr_overlap(validate(data))
    cohorts = defaultdict(list)
    by_scope = defaultdict(lambda: defaultdict(list))
    by_repo = defaultdict(list)
    for item in items:
        cohorts[item["cohort"]].append(item)
        by_scope[(item["repo"], item["category"])][item["cohort"]].append(item)
        by_repo[item["repo"]].append(item)
    group_summaries = []
    for (repo, category), subsets in sorted(by_scope.items()):
        old_all, new_all = subsets["pre_v27"], subsets["v27_confirmed"]
        # Overlapping PR windows are not independent time-to-completion samples.
        old = sorted(x["pr_to_merge_minutes"] for x in old_all
                     if x["observed_overlapping_prs"] == 0)
        new = sorted(x["pr_to_merge_minutes"] for x in new_all
                     if x["observed_overlapping_prs"] == 0)
        eligible = len(old) >= MIN_MATCHED_PAIRS and len(new) >= MIN_MATCHED_PAIRS
        old_median = statistics.median(old) if old else None
        new_median = statistics.median(new) if new else None
        group_summaries.append({
            "repo": repo, "category": category, "pre_v27_n": len(old_all),
            "v27_confirmed_n": len(new_all),
            "pre_v27_observed_overlapping_pr_n": len(old_all)-len(old),
            "v27_observed_overlapping_pr_n": len(new_all)-len(new),
            "pre_v27_nonoverlap_in_sample_n": len(old),
            "v27_nonoverlap_in_sample_n": len(new),
            "pre_v27_nonoverlap_median_pr_minutes": old_median,
            "v27_nonoverlap_median_pr_minutes": new_median,
            "descriptive_relative_change_pct": round(100*(new_median/old_median-1), 2)
                if eligible and old_median > 0 else None,
            "sufficient_matched_samples": eligible,
        })
    first_edit = [x["request_to_first_edit_minutes"] for x in items
                  if x["cohort"] == "v27_confirmed" and x["request_to_first_edit_minutes"] is not None]
    return {
        "metric": "PR_OPEN_TO_MERGE_WALL_CLOCK_PROXY",
        "total_observations": len(items),
        "cohorts": {key: {
            "n": len(rows),
            "raw_pr_elapsed_median_minutes_not_active_time": round(
                statistics.median(x["pr_to_merge_minutes"] for x in rows), 2),
            "observed_parallel_window_pr_n": sum(
                x["observed_overlapping_prs"] > 0 for x in rows)
            } for key, rows in sorted(cohorts.items())},
        "per_repo": [{
            "repo": repo,
            "pre_v27_n": sum(x["cohort"] == "pre_v27" for x in rows),
            "pre_v27_overlapping_pr_windows_n": sum(
                x["cohort"] == "pre_v27" and x["observed_overlapping_prs"] > 0
                for x in rows),
            "pre_v27_raw_pr_elapsed_median_minutes_not_active_time": (
                round(statistics.median(
                    x["pr_to_merge_minutes"] for x in rows if x["cohort"] == "pre_v27"), 2)
                if any(x["cohort"] == "pre_v27" for x in rows) else None),
            "can_infer_active_development_time": False
        } for repo, rows in sorted(by_repo.items())],
        "comparable_groups": group_summaries,
        "v27_request_to_first_edit_n": len(first_edit),
        "v27_request_to_first_edit_median_minutes": round(statistics.median(first_edit), 2)
            if first_edit else None,
        "causal_attribution": "NOT_VERIFIED",
        "actual_active_development_time": "NOT_MEASURED",
        "notes": [
            "Pre-v27 includes mixed v26.x; do not label it a pure v26.8 baseline.",
            "PR wall-clock includes reviews, idle time, async waits and CI.",
            "Open-window overlaps are detected by repository; overlapping PRs are excluded from independent PR-duration comparisons.",
            "No overlap in the ledger is not proof of isolated work; the PR sample can omit other concurrent PRs.",
            "Classification by repository+category is a first approximation; scope sizes still vary.",
            "Do not infer a ChatGPT model speedup from shorter PR durations.",
            "v27 attribution requires pinned baseline and evidence URI, not date alone.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=DEFAULT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = summarize(json.loads(args.ledger.read_text(encoding="utf-8")))
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Factory delivery evidence:", result["total_observations"], "merged PR records")
        for cohort, metrics in result["cohorts"].items():
            print(f"{cohort}: n={metrics['n']}, observed parallel windows="
                  f"{metrics['observed_parallel_window_pr_n']}; "
                  f"RAW PR elapsed median={metrics['raw_pr_elapsed_median_minutes_not_active_time']:.2f} min"
                  " (NOT active development time)")
        for r in result["per_repo"]:
            if r["pre_v27_n"]:
                print(f"APP {r['repo']}: {r['pre_v27_overlapping_pr_windows_n']}/"
                      f"{r['pre_v27_n']} pre-v27 PRs have overlapping open windows; "
                      "no GitHub-only estimate of hours worked.")
        for x in result["comparable_groups"]:
            if x["sufficient_matched_samples"]:
                print(f"MATCHED {x['repo']}/{x['category']}: change "
                      f"{x['descriptive_relative_change_pct']:+.2f}% "
                      "(DESCRIPTIVE ONLY)")
        print("Attributable v27 speedup: NOT VERIFIED (no causal comparison)")


if __name__ == "__main__":
    main()
