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

def validate_resume(output, fixture, inputs, model, effort):
    """Reject stale, duplicate, mixed or detached partial evidence before reuse.

    This validates local structure, NOT provider authenticity; independent
    review of the completed artifact remains mandatory.
    """
    if (output.get("kind") != "INDEPENDENT_MODEL_RUNS"
            or output.get("model_requested") != model
            or output.get("effort") != effort
            or output.get("case_count") != len(fixture["cases"])):
        raise ValueError("Resume evidence is incompatible with this study")
    if output.get("completed"):
        raise ValueError("Completed study cannot be resumed")
    allowed={(case_id,variant):digest for case_id,variant,_,digest in inputs}
    records=output.get("records")
    if not isinstance(records,list) or len(records) >= len(inputs):
        raise ValueError("Resume records are missing or unexpectedly complete")
    seen=set()
    provider_ids=set()
    resolved_model=output.get("model")
    for item in records:
        if not isinstance(item,dict):
            raise ValueError("Invalid resume record")
        key=(item.get("case_id"),item.get("variant"))
        if key not in allowed or key in seen:
            raise ValueError("Unknown or duplicate case in resume evidence")
        seen.add(key)
        if item.get("prompt_sha256") != allowed[key]:
            raise ValueError("Resume prompt hash differs from current source")
        request_id=item.get("request_id")
        if (item.get("source_kind")!="ACTUAL_MODEL_RUN"
                or not isinstance(request_id,str) or not request_id
                or request_id in provider_ids):
            raise ValueError("Missing or duplicate provider request identity")
        provider_ids.add(request_id)
        if (item.get("model") != resolved_model or not resolved_model
                or item.get("effort") != effort):
            raise ValueError("Mixed model or effort in resumed output")
        if (not isinstance(item.get("input_tokens"),int)
                or item["input_tokens"] <= 0
                or not isinstance(item.get("output_tokens"),int)
                or item["output_tokens"] <= 0
                or not isinstance(item.get("elapsed_ms"),(int,float))
                or item["elapsed_ms"] <= 0):
            raise ValueError("Missing provider usage or measured timing")
        try:
            body=json.loads(item.get("response_text") or "")
        except (ValueError,TypeError) as exc:
            raise ValueError("Malformed stored provider response") from exc
        if (not isinstance(body,dict)
                or body.get("decision") != item.get("decision")
                or body.get("gates") != item.get("gates")):
            raise ValueError("Stored response is detached from its metadata")
    return seen


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model",default="gpt-6.1-sol")
    ap.add_argument("--effort",choices=["low","medium","high"],default="high")
    ap.add_argument("--timeout",type=int,default=240)
    ap.add_argument("--out",type=Path,default=Path("v27d2-real-model-outputs.json"))
    ap.add_argument("--dry-run",action="store_true")
    ap.add_argument("--confirm-paid-run",action="store_true")
    ap.add_argument("--max-new-requests",type=int,default=32,
                    help="Paid calls allowed in THIS dispatch (1-32); use 2 for preflight.")
    args=ap.parse_args()
    if not 1 <= args.max_new_requests <= 32:
        ap.error("--max-new-requests must be between 1 and 32")
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
        try:
            output=json.loads(args.out.read_text(encoding="utf-8"))
            validate_resume(output,fixture,inputs,args.model,args.effort)
        except (ValueError,TypeError,KeyError) as exc:
            raise SystemExit("Resume rejected before any paid call: "+str(exc)) from exc
    found={(x["case_id"],x["variant"]):x for x in output["records"]}
    new_requests=0
    for case_id,variant,prompt,digest in inputs:
        existing=found.get((case_id,variant))
        if existing:
            continue
        if new_requests >= args.max_new_requests:
            break
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
        new_requests += 1
        args.out.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",
                            encoding="utf-8")
        print(f"MODEL_RUN_RECORDED case={case_id} arm={variant} "
              f"request_id={item['request_id']} input_tokens={item['input_tokens']} "
              f"output_tokens={item['output_tokens']} elapsed_ms={item['elapsed_ms']}")
    output["completed"]=len(output["records"])==len(inputs)
    args.out.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if output["completed"]:
        print(f"COMPLETE: {len(output['records'])}/{len(inputs)} real model calls recorded; "
              "independent semantic review still required, v27E HOLD.")
    else:
        print(f"CHECKPOINT: {len(output['records'])}/{len(inputs)} real model calls recorded; "
              f"{new_requests} billed in this dispatch. Resume with same model/effort "
              "and downloaded artifact. v27E HOLD.")

if __name__=="__main__":
    main()
