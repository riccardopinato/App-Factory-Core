#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PLAYBOOK_DIR=ROOT/"playbooks"

def load_playbooks():
    out={}
    for path in sorted(PLAYBOOK_DIR.glob("*.json")):
        data=json.loads(path.read_text(encoding="utf-8"))
        out[data["id"]]=data
    return out

def main():
    p=argparse.ArgumentParser(description="Materialize an App Factory canonical playbook plan.")
    p.add_argument("--list",action="store_true")
    p.add_argument("--playbook",default="")
    p.add_argument("--inputs-json",default="{}")
    p.add_argument("--json",action="store_true")
    a=p.parse_args()
    books=load_playbooks()
    if a.list:
        for key in sorted(books): print(f"{key}\t{books[key]['title']}")
        return 0
    if not a.playbook: p.error("--playbook or --list is required")
    if a.playbook not in books: p.error(f"unknown playbook: {a.playbook}")
    try: inputs=json.loads(a.inputs_json)
    except json.JSONDecodeError as exc: p.error(f"invalid --inputs-json: {exc}")
    if not isinstance(inputs,dict): p.error("--inputs-json must decode to an object")
    book=books[a.playbook]
    missing=[name for name in book["required_inputs"] if name not in inputs]
    plan={"schema_version":1,"playbook_id":book["id"],"authority":book["authority"],"ready":not missing,"missing_inputs":missing,"steps":book["steps"],"completion":book["completion"],"note":"PROCESS_ONLY: no PASS/CERTIFIED or authority bypass."}
    if a.json: print(json.dumps(plan,indent=2,sort_keys=True))
    else:
        print(f"PLAYBOOK {book['id']} — {'READY' if plan['ready'] else 'BLOCKED'}")
        if missing: print("Missing inputs: "+", ".join(missing))
        for i,s in enumerate(book["steps"],1): print(f"{i}. {s['id']}: {s['action']} [{s['gate']}]")
    return 0 if plan["ready"] else 2
if __name__=="__main__": raise SystemExit(main())
