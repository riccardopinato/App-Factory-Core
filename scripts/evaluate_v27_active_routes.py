#!/usr/bin/env python3
"""Current-v27 routing/context benchmark (offline). Never invokes a model.

This is an ACTIVE v27 test: historic D2 v26.8 paired results remain separate.
Bytes are real UTF-8 source input sizes; tokenizer and billed usage are not inferred.
"""
from __future__ import annotations
import json
import statistics
import sys
import time
from pathlib import Path
import resolve_v27_candidate as resolver

ROOT=Path(__file__).resolve().parents[1]
CASES=[
    ("next_chat","Avanti Anna's Diary","approved current step","cmd_avanti"),
    ("next_roadmap","Avanti roadmap Notes-Ecosistema","approved roadmap","cmd_avanti_roadmap"),
    ("audit","Audit Anna's Diary","read-only","audit"),
    ("catalog","Capability Notes-Ecosistema","catalog only","capability_sync"),
    ("legend","Legenda Avanti","display commands only","legend"),
    ("mockup","Mock-up interattivi","design, no code","mockup_interactive"),
    ("integrate_mockup","Integra i mock-up","approved designs only","mockup_integration"),
    ("native","Verifica PIN Android Keystore","strong biometrics","android_security"),
    ("web","Progetta una web utility SEO multilingua","multi-market","web_utility_specialist"),
    ("factory","Aggiorna App Factory Core","Master Prompt","factory_update"),
    ("bare_procedi","Procedi","","FALLBACK_BASELINE_USED"),
]


def main() -> None:
    manifest=json.loads((ROOT/"v27/candidate/MODULE_MAP.json").read_text(encoding="utf-8"))
    fallback=(ROOT/manifest["living_fallback"]["path"]).stat().st_size
    rows=[]
    for name,task,context,expected in CASES:
        start=time.perf_counter_ns()
        result=resolver.resolve(task,context,load_text=True)
        elapsed_ms=(time.perf_counter_ns()-start)/1e6
        if not result["active"]:
            raise ValueError("not on ACTIVE v27: "+name)
        if expected=="FALLBACK_BASELINE_USED":
            if result["selection"]!=expected:
                raise ValueError("expected verified fallback: "+name)
        elif result["selection"]!="MODULES":
            raise ValueError("routing blocked or ambiguous: "+name+" "+str(result))
        elif expected not in result["route_rules"]:
            # One scenario may use generic classifier, but its configured
            # route still MUST be identified.
            raise ValueError("unexpected router decision: "+name+" "+str(result["route_rules"]))
        rows.append({"id":name,"selection":result["selection"],
                     "route_rules":result.get("route_rules",[]),
                     "loaded_bytes":result["loaded_bytes"],
                     "fallback_bytes":fallback,
                     "local_resolver_ms":round(elapsed_ms,3),
                     "model_executed":False})
    modular=[r for r in rows if r["selection"]=="MODULES"]
    out={"baseline":"ACTIVE_V27",
         "cases":len(rows),
         "fallback_cases":len(rows)-len(modular),
         "median_selected_byte_reduction_pct":round(statistics.median(
             (1-r["loaded_bytes"]/fallback)*100 for r in modular),2),
         "local_resolver_median_ms":round(statistics.median(
             r["local_resolver_ms"] for r in rows),3),
         "model_runs":0,
         "actual_billed_tokens":None,
         "behavioral_equivalence":"NOT_VERIFIED",
         "downstream_adoption":"NOT_VERIFIED",
         "rows":rows}
    print("ACTIVE V27 OFFLINE EVAL "+json.dumps(out,ensure_ascii=False))
    if out["fallback_cases"]!=1:
        raise ValueError("unexpected number of fallback cases")

if __name__=="__main__":
    main()
