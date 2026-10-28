#!/usr/bin/env python3
"""Read-only v27D replay on three independently pinned app-repository snapshots.

This is a deterministic instruction-selection and byte-cost experiment, NOT a
model-behavior eval, production deploy, or proof of end-to-end time savings.
No remote calls or writes to app repositories are made by this script.
"""
from __future__ import annotations
import argparse
import json
import re
import statistics
import sys
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import resolve_v27_candidate as resolver

MATRIX=ROOT/"v27/candidate/pilots/PILOT_MATRIX.json"
BASE_MASTER=ROOT/"master/MASTER_PROMPT_UTILITY_FLUTTER_CHATGPT_v26_8_FULL.txt"
BASE_INDEX=ROOT/"golden/GOLDEN_INDEX_CURRENT.txt"
BASE_REGISTRY=ROOT/"golden/GOLDEN_REGISTRY.yaml"
MANDATORY={"anna":"privacy / no parallel store","phone":"PIN / Android runtime trust","applab":"exact-head / SELF_CANARY"}

def file_size(path:Path)->int:
    return len(path.read_bytes())

def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--report",help="Optional JSON result path (outside source files)")
    args=ap.parse_args()
    matrix=json.loads(MATRIX.read_text(encoding="utf-8"))
    projects={p["id"]:p for p in matrix["projects"]}
    assert len(projects)==3, "expected 3 source-backed project snapshots"
    assert set(projects)==set(MANDATORY)
    for p in projects.values():
        assert re.fullmatch(r"[0-9a-f]{40}",p["source_sha"])
        assert p["repository"].startswith("riccardopinato/")
        assert all(p["evidence_files"]), "missing repository evidence pointers"
        assert p["boundary"]

    base_master=file_size(BASE_MASTER)
    base_index=file_size(BASE_INDEX)
    base_registry=file_size(BASE_REGISTRY)
    baseline_fixed=base_master+base_index+base_registry
    records=[]
    failures=[]
    for case in matrix["cases"]:
        if case["project"] not in projects and case["project"]!="factory":
            failures.append(f'{case["id"]}: unknown evidence project')
            continue
        start=time.perf_counter_ns()
        result=resolver.resolve(case["request"],case["context"],
                                load_text=True,load_golden=True)
        elapsed_ms=round((time.perf_counter_ns()-start)/1e6,3)
        expected=case["expect"]
        if result.get("selection")!=expected:
            failures.append(f'{case["id"]}: expected {expected}, got {result.get("selection")} ({result.get("reason")})')
        ids=set(result.get("modules",[]))
        for required in case.get("required_modules",[]):
            if required not in ids: failures.append(f'{case["id"]}: missing module {required}')
        for forbidden in case.get("forbidden_modules",[]):
            if forbidden in ids: failures.append(f'{case["id"]}: unnecessary module {forbidden}')
        docs=result.get("documents",{})
        combined="\n".join(docs.values())
        for token in case.get("must_contain",[]):
            if token.casefold() not in combined.casefold():
                failures.append(f'{case["id"]}: key policy text absent: {token}')

        module_bytes=sum(len(doc.encode("utf-8")) for path,doc in docs.items()
                         if path.startswith("v27/candidate/"))
        golden_bytes=sum(len(doc.encode("utf-8")) for path,doc in docs.items()
                         if path.startswith("golden/"))
        if result.get("selection")=="MODULES":
            # Conservative estimate includes Registry even when parser consumes
            # it without placing the whole text into the model context.
            candidate_bootstrap=module_bytes+base_registry+golden_bytes
            legacy_bootstrap=baseline_fixed+golden_bytes
            saved=legacy_bootstrap-candidate_bootstrap
            pct=round(saved/legacy_bootstrap*100,1)
            if candidate_bootstrap>=legacy_bootstrap:
                failures.append(f'{case["id"]}: modular bootstrap not smaller')
            if not ids:
                failures.append(f'{case["id"]}: no modules for case selected')
        else:
            candidate_bootstrap=module_bytes+base_registry
            legacy_bootstrap=baseline_fixed
            saved=legacy_bootstrap-candidate_bootstrap
            pct=round(saved/legacy_bootstrap*100,1)

        records.append({
            "id":case["id"],"project":case["project"],
            "selection":result["selection"],"modules":result.get("modules",[]),
            "golden_ids":[g["id"] for g in result.get("goldens",[])],
            "candidate_bytes":candidate_bootstrap,
            "legacy_bytes":legacy_bootstrap,
            "difference_bytes":saved,"difference_percent":pct,
            "selected_module_bytes":module_bytes,
            "golden_content_bytes":golden_bytes,
            "resolver_ms_diagnostic":elapsed_ms
        })
        print(f'V27D CASE {case["id"]}: {result["selection"]} | '
              f'{candidate_bootstrap}/{legacy_bootstrap} bytes '
              f'({pct:+.1f}% reduction) | modules={",".join(result.get("modules",[])) or "-"}')

    modular=[r for r in records if r["selection"]=="MODULES"]
    unknown=[r for r in records if r["selection"]=="FALLBACK_BASELINE_USED"]
    assert len(matrix["cases"])>=10
    if len(modular)<7: failures.append("insufficient modular scenarios")
    if len(unknown)<2: failures.append("missing ambiguous-routing fallback cases")
    mean_reduction=round(statistics.mean(r["difference_percent"] for r in modular),1) if modular else None
    median_reduction=round(statistics.median(r["difference_percent"] for r in modular),1) if modular else None
    output={
        "study":"v27D read-only deterministic routing/byte-cost replay",
        "factory_baseline":matrix["factory_baseline"],
        "source_repositories":[{"repo":p["repository"],"sha":p["source_sha"],"evidence_files":p["evidence_files"]} for p in projects.values()],
        "units":"UTF-8 bytes, NOT tokens, model speed or downstream runtime",
        "old_baseline_fixed_bytes":baseline_fixed,
        "old_master_bytes":base_master,
        "old_golden_index_bytes":base_index,
        "old_registry_bytes":base_registry,
        "selected_modular_cases":len(modular),"fallback_cases":len(unknown),
        "mean_modular_reduction_pct":mean_reduction,
        "median_modular_reduction_pct":median_reduction,
        "records":records,
        "policy_behavior_equivalence":"NOT_VERIFIED (no independent model response evaluation)",
        "cross_repo_changes":"NONE",
        "release_readiness":"HOLD",
        "errors":failures
    }
    if args.report:
        out=Path(args.report)
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("V27D SUMMARY "+json.dumps({
        "cases":len(records),"modular":len(modular),"fallback":len(unknown),
        "mean_modular_reduction_pct":mean_reduction,
        "median_modular_reduction_pct":median_reduction,
        "errors":len(failures),"behavior":"NOT_VERIFIED","release":"HOLD"
    },ensure_ascii=False))
    if failures:
        for f in failures: print("V27D FAIL "+f)
        raise SystemExit(1)
    print("V27D REPLAY: PASS (routing/bytes only, no agent behavioral certification)")

if __name__=="__main__":
    main()
