#!/usr/bin/env python3
"""Execute v27D2 real paired model evaluations using an explicit API key.

This command is MANUAL and PAID; never run from pull_request or scheduled CI.
It saves real model IDs, request IDs, usage, elapsed time, prompt hashes and
unmodified model response text. It does NOT claim a qualitative PASS.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import evaluate_v27d2 as eval_d2

def prepare():
    fixture=eval_d2.source_cases()
    prompts=[]
    for case,b,v,_ in eval_d2.prompts(fixture):
        for variant,text in (("baseline",b),("modular",v)):
            prompts.append((case["id"],variant,text,eval_d2.sha(text)))
    return fixture,prompts

def extract_text(response):
    contents=[]
    for item in response.get("output",[]):
        if item.get("type")!="message":
            continue
        for part in item.get("content",[]):
            if part.get("type")=="output_text" and isinstance(part.get("text"),str):
                contents.append(part["text"])
    return "\n".join(contents)

def perform(prompt,model,effort,timeout):
    payload=json.dumps({
        "model":model,
        "input":[{"role":"user","content":prompt}],
        "reasoning":{"effort":effort},
        "max_output_tokens":3000,
        "store":False,
        "text":{"format":{"type":"json_object"}},
    }).encode("utf-8")
    request=urllib.request.Request(
        "https://api.openai.com/v1/responses",method="POST",data=payload,
        headers={"Content-Type":"application/json",
                 "Authorization":"Bearer "+os.environ["OPENAI_API_KEY"]}
    )
    start=time.perf_counter()
    with urllib.request.urlopen(request,timeout=timeout) as resp:
        obj=json.loads(resp.read().decode("utf-8"))
    duration=round((time.perf_counter()-start)*1000,3)
    if obj.get("status")!="completed":
        raise ValueError("Response did not complete")
    if not obj.get("id") or not obj.get("model"):
        raise ValueError("Response missing provider identity")
    usage=obj.get("usage") or {}
    if not isinstance(usage.get("input_tokens"),int) or not isinstance(usage.get("output_tokens"),int):
        raise ValueError("Response missing provider token usage")
    body=extract_text(obj)
    if not body: raise ValueError("Response lacks output_text")
    parsed=json.loads(body)
    if not isinstance(parsed,dict):
        raise ValueError("Model response was not an object")
    return {
        "source_kind":"ACTUAL_MODEL_RUN","request_id":obj["id"],
        "model":obj["model"],"effort":effort,
        "elapsed_ms":duration,
        "input_tokens":usage["input_tokens"],
        "output_tokens":usage["output_tokens"],
        "response_text":body,"decision":parsed.get("decision"),
        "gates":parsed.get("gates"),
        "reasoning_tokens":(usage.get("output_tokens_details") or {}).get("reasoning_tokens")
    }

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model",default="gpt-6-sol")
    ap.add_argument("--effort",choices=["low","medium","high"],default="high")
    ap.add_argument("--timeout",type=int,default=240)
    ap.add_argument("--out",type=Path,default=Path("v27d2-real-model-outputs.json"))
    ap.add_argument("--dry-run",action="store_true")
    ap.add_argument("--confirm-paid-run",action="store_true")
    args=ap.parse_args()
    fixture,inputs=prepare()
    if args.dry_run:
        print(f"DRY_RUN: {len(inputs)} independent API requests planned; "
              f"model={args.model}, effort={args.effort}; 0 requests executed.")
        return
    if not args.confirm_paid_run:
        ap.error("Explicit --confirm-paid-run required; OpenAI API usage is billed.")
    if not os.environ.get("OPENAI_API_KEY"):
        ap.error("Missing OPENAI_API_KEY in environment (never paste key into code/logs).")
    run_url=os.environ.get("GITHUB_SERVER_URL","https://github.com")+"/"+os.environ.get("GITHUB_REPOSITORY","unknown")+"/actions/runs/"+os.environ.get("GITHUB_RUN_ID","unknown")
    output={
        "kind":"INDEPENDENT_MODEL_RUNS","model":None,"model_requested":args.model,
        "effort":args.effort,"evidence_uri":run_url,
        "records":[],"independent_reviews":[],
        "completed":False,"case_count":len(fixture["cases"]),
        "warning":"Actual model outputs only. Independent qualitative reviews are required before scorer PASS."
    }
    if args.out.is_file():
        output=json.loads(args.out.read_text(encoding="utf-8"))
        if output.get("model_requested")!=args.model or output.get("effort")!=args.effort:
            raise SystemExit("Existing result has different model/effort; do not mix runs.")
        if output.get("completed"):
            raise SystemExit("Already completed: avoid duplicate paid requests.")
    found={(x["case_id"],x["variant"]):x for x in output["records"]}
    for case_id,variant,prompt,digest in inputs:
        existing=found.get((case_id,variant))
        if existing:
            if existing.get("prompt_sha256")!=digest:
                raise SystemExit("Prompt changed since existing provider result; cannot resume.")
            continue
        try:
            item=perform(prompt,args.model,args.effort,args.timeout)
        except (urllib.error.HTTPError,urllib.error.URLError,ValueError,
                json.JSONDecodeError,TimeoutError) as exc:
            # Do not print an HTTP body, which could contain sensitive content.
            print(f"MODEL_RUN_FAILED case={case_id} arm={variant} reason_type={type(exc).__name__}")
            raise SystemExit(2)
        item.update(case_id=case_id,variant=variant,prompt_sha256=digest)
        if output["model"] is None:output["model"]=item["model"]
        if item["model"]!=output["model"]:
            raise SystemExit("Provider resolved a different model; abort mixed-model evaluation.")
        output["records"].append(item)
        args.out.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",
                            encoding="utf-8")
        print(f"MODEL_RUN_RECORDED case={case_id} arm={variant} "
              f"request_id={item['request_id']} input_tokens={item['input_tokens']} "
              f"output_tokens={item['output_tokens']} elapsed_ms={item['elapsed_ms']}")
    output["completed"]=True
    args.out.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"COMPLETE: {len(output['records'])}/{len(inputs)} real model calls recorded; "
          "independent semantic review still required, v27E HOLD.")

if __name__=="__main__":
    main()
