#!/usr/bin/env python3
"""Prototype v27C on-demand resolver (CANDIDATE ONLY).

It does NOT supersede CURRENT.yaml. Call only to inspect/evaluate candidate
routing. On unsafe selection, use integrity-verified synchronized full fallback.
No model agents, remote calls, or background processes are created here.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST="v27/candidate/MODULE_MAP.json"

def digest(raw:bytes)->str:
    return hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\0"+raw).hexdigest()

def normal(text:str)->str:
    folded=unicodedata.normalize("NFKD",text.casefold())
    stripped="".join(x for x in folded if not unicodedata.combining(x))
    return re.sub(r"\s+"," ",re.sub(r"[^a-z0-9]+"," ",stripped)).strip()

def has_term(haystack:str,term:str)->bool:
    needle=normal(term)
    return bool(needle) and bool(re.search(r"(?:^| )"+re.escape(needle)+r"(?: |$)",haystack))

def within_repo(path:str,root:Path=ROOT)->Path:
    if not isinstance(path,str) or not path.startswith("v27/candidate/"):
        raise ValueError("untrusted candidate path: "+repr(path))
    p=(root/path).resolve()
    if not p.is_relative_to(root.resolve()):
        raise ValueError("candidate path escapes repository")
    return p

def read_checked(path:str,seal:str,root:Path=ROOT)->str:
    if not re.fullmatch(r"[0-9a-f]{40}",seal or ""):
        raise ValueError("missing/invalid source Git blob pin for "+path)
    raw=within_repo(path,root).read_bytes()
    if digest(raw)!=seal: raise ValueError("source Git blob mismatch for "+path)
    return raw.decode("utf-8")

def git_sha(root:Path=ROOT)->str|None:
    result=subprocess.run(
        ["git","rev-parse","HEAD"],cwd=root,capture_output=True,text=True,
        check=False
    )
    sha=result.stdout.strip()
    return sha if result.returncode==0 and re.fullmatch(r"[0-9a-f]{40}",sha) else None

def route(task:str,context:str,manifest:dict)->tuple[list[str],list[str],list[str]]:
    desc=normal(task+" "+context)
    selected=[]
    goldens=[]
    labels=[]
    for rule in manifest.get("task_routes",[]):
        if any(has_term(desc,term) for term in rule["terms"]):
            labels.append(rule["id"])
            selected.extend(rule["modules"])
            goldens.extend(rule.get("golden_ids",[]))
    ids={entry["id"] for entry in [*manifest["modules"],*manifest.get("policy_updates",[])]}
    # A continuation command must load the complete parallel-first/authorization
    # contract, not only the short Core summary. Bare "Procedi" with no task
    # context remains ambiguous and must use the verified full fallback.
    command=normal(task)
    continuation=any(has_term(command,word) for word in
                     ("procedi","continua","vai avanti","completa"))
    if selected and continuation:
        selected.append("authority-execution")
        labels.append("continuation_authority")
    if any(name not in ids for name in selected):
        raise ValueError("route references missing module")
    ordered=[entry["id"] for entry in [*manifest["modules"],*manifest.get("policy_updates",[])] if entry["id"] in selected]
    return ordered,list(dict.fromkeys(goldens)),labels

def resolve(task:str,context:str="",expected_sha:str|None=None,
            load_text:bool=False,load_golden:bool=False,root:Path=ROOT)->dict:
    """Return data and selected docs, or fail closed to a pinned full fallback."""
    result={"candidate":"v27C","active":False,"task":task,
            "selection":"", "note":"CURRENT.yaml remains authoritative (v26.8)."}
    current=(root/"CURRENT.yaml").read_text(encoding="utf-8")
    if not re.search(r'(?m)^  version: "26\.8"$',current):
        return {**result,"selection":"BLOCKED","reason":"CURRENT_UNEXPECTED; candidate not activated"}
    sha=git_sha(root)
    if expected_sha is not None:
        if not re.fullmatch(r"[0-9a-f]{40}",expected_sha):
            return {**result,"selection":"BLOCKED","reason":"INVALID_EXPECTED_SHA"}
        if sha!=expected_sha:
            return {**result,"selection":"BLOCKED","reason":"FACTORY_SHA_MISMATCH_OR_UNAVAILABLE"}
    result["factory_sha"]=sha
    try:
        manifest=json.loads((root/MANIFEST).read_text(encoding="utf-8"))
        if manifest.get("status")!="CANDIDATE_NOT_ACTIVE":
            raise ValueError("v27 candidate activation state invalid")
        names,golden_ids,matched=route(task,context,manifest)
        if not names: raise ValueError("NO_SAFE_MODULE_ROUTE")
        seals=manifest["integrity_blob_sha"]
        core=read_checked(manifest["core"]["path"],seals["core"],root)
        docs={manifest["core"]["path"]:core}
        for entry in [*manifest["modules"],*manifest.get("policy_updates",[])]:
            if entry["id"] in names:
                docs[entry["path"]]=read_checked(entry["path"],seals[entry["id"]],root)
        result.update(selection="MODULES",reason="ROUTE_MATCHED",route_rules=matched,
                      modules=names,document_paths=list(docs),
                      loaded_bytes=sum(len(s.encode("utf-8")) for s in docs.values()))
        if load_golden and golden_ids:
            # Registry path/status is authoritative; no need to load full Golden Index.
            import yaml
            registry=yaml.safe_load((root/"golden/GOLDEN_REGISTRY.yaml").read_text(encoding="utf-8"))
            if str(registry.get("master_version"))!="26.8":
                raise ValueError("Golden Registry baseline mismatch")
            registry_map={g["id"]:g for g in registry["goldens"]}
            chosen=[]
            for gid in golden_ids:
                golden=registry_map.get(gid)
                if not golden: raise ValueError("unknown Golden ID: "+gid)
                if golden.get("status")=="DEPRECATED":
                    raise ValueError("deprecated Golden ID: "+gid)
                # Golden file content only materialized on explicit request.
                loc=(root/golden["path"]).resolve()
                if not loc.is_relative_to(root.resolve()) or not loc.is_file():
                    raise ValueError("unavailable Golden file: "+gid)
                needs_review=(golden.get("freshness_status")!="CURRENT"
                              or "DRAFT" in str(golden.get("status","")).upper())
                chosen.append({"id":gid,"path":golden["path"],
                               "status":golden["status"],
                               "freshness_status":golden.get("freshness_status"),
                               "provider_sensitive":golden.get("provider_sensitive",False),
                               "requires_review":needs_review})
                if load_text: docs[golden["path"]]=loc.read_text(encoding="utf-8")
            result["goldens"]=chosen
            if any(g["requires_review"] for g in chosen):
                result["golden_readiness"]="REVIEW_REQUIRED_NOT_CERTIFIED"
                result["golden_review_ids"]=[g["id"] for g in chosen
                                              if g["requires_review"]]
        if load_text:
            result["documents"]=docs
            result["loaded_bytes"]=sum(len(s.encode("utf-8")) for s in docs.values())
        return result
    except (KeyError,ValueError,OSError,UnicodeError,json.JSONDecodeError) as exc:
        cause=str(exc)
        try:
            manifest=json.loads((root/MANIFEST).read_text(encoding="utf-8"))
            fb=manifest["living_fallback"]
            content=read_checked(fb["path"],fb["git_blob_sha"],root)
            # No old baseline silently used: only synchronized v27 artifact.
            result.update(selection="FALLBACK_BASELINE_USED",
                          reason=cause,
                          fallback_path=fb["path"],
                          fallback_sha256=fb["git_blob_sha"],
                          loaded_bytes=len(content.encode("utf-8")))
            if load_text:result["documents"]={fb["path"]:content}
            return result
        except (KeyError,ValueError,OSError,UnicodeError,json.JSONDecodeError) as second:
            return {**result,"selection":"BLOCKED_FACTORY_BASELINE_UNVERIFIED",
                    "reason":cause,"fallback_error":str(second)}

def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--task",required=True)
    p.add_argument("--context",default="",help="Known task/roadmap scope. Required for bare 'Procedi' to route safely.")
    p.add_argument("--expected-sha",help="Optional pinned session SHA; reject mismatch or unavailable git SHA.")
    p.add_argument("--include-text",action="store_true",help="Include selected document contents in output")
    p.add_argument("--include-goldens",action="store_true",help="Resolve relevant Golden IDs against the Registry")
    args=p.parse_args()
    response=resolve(args.task,args.context,args.expected_sha,args.include_text,args.include_goldens)
    print(json.dumps(response,ensure_ascii=False,indent=2))
    if response["selection"] in ("BLOCKED","BLOCKED_FACTORY_BASELINE_UNVERIFIED"):
        raise SystemExit(2)

if __name__=="__main__":
    main()
