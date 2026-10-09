#!/usr/bin/env python3
from __future__ import annotations
from datetime import date, datetime
from pathlib import Path
import json, re, sys
import yaml
from jsonschema import Draft202012Validator, FormatChecker, RefResolver

ROOT=Path(__file__).resolve().parents[1]
errors=[]
def fail(msg): errors.append(msg)
def req(path):
    p=ROOT/path
    if not p.is_file(): fail(f"missing file: {path}")
    return p
def norm(v):
    if isinstance(v,(date,datetime)): return v.isoformat()
    if isinstance(v,list): return [norm(x) for x in v]
    if isinstance(v,dict): return {k:norm(x) for k,x in v.items()}
    return v
def load_yaml(path):
    p=req(path)
    if not p.exists(): return {}
    try: return norm(yaml.safe_load(p.read_text(encoding="utf-8")))
    except yaml.YAMLError as e: fail(f"invalid YAML {path}: {e}"); return {}
def load_json(path):
    p=req(path)
    if not p.exists(): return {}
    try: return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e: fail(f"invalid JSON {path}: {e}"); return {}
def schema_validate(instance,schema_path,label,store=None):
    schema=load_json(schema_path)
    if not schema: return
    resolver=RefResolver.from_schema(schema,store=store or {})
    v=Draft202012Validator(schema,resolver=resolver,format_checker=FormatChecker())
    for e in sorted(v.iter_errors(instance),key=lambda x:list(x.path)):
        loc=".".join(str(x) for x in e.path) or "<root>"
        fail(f"{label} schema violation at {loc}: {e.message}")

current=load_yaml("CURRENT.yaml")
manifest=load_json("schemas/golden_manifest.schema.json")
registry=load_yaml("golden/GOLDEN_REGISTRY.yaml")
schema_validate(current,"schemas/current.schema.json","CURRENT.yaml")
registry_schema=load_json("schemas/golden_registry.schema.json")
if registry_schema:
    store={"golden_manifest.schema.json":manifest,
           "https://github.com/riccardopinato/App-Factory-Core/schemas/golden_manifest.schema.json":manifest}
    resolver=RefResolver.from_schema(registry_schema,store=store)
    v=Draft202012Validator(registry_schema,resolver=resolver,format_checker=FormatChecker())
    for e in sorted(v.iter_errors(registry),key=lambda x:list(x.path)):
        loc=".".join(str(x) for x in e.path) or "<root>"
        fail(f"GOLDEN_REGISTRY.yaml schema violation at {loc}: {e.message}")

for section in ("master","golden_index","golden_registry","bootstrap"):
    obj=current.get(section,{}) if isinstance(current,dict) else {}
    for key in ("path","versioned_path"):
        if key in obj: req(str(obj[key]))
for key in ("script","requirements"):
    if key in current.get("validation",{}): req(str(current["validation"][key]))

if str(registry.get("master_version"))!=str(current.get("master",{}).get("version")): fail("registry master_version != CURRENT master.version")
if registry.get("index_version")!=current.get("golden_index",{}).get("version"): fail("registry index_version != CURRENT golden_index.version")
if registry.get("registry_version")!=current.get("golden_registry",{}).get("version"): fail("registry registry_version != CURRENT golden_registry.version")

goldens=registry.get("goldens",[]) if isinstance(registry,dict) else []
ids=[]; paths=[]
for g in goldens:
    if not isinstance(g,dict): continue
    ids.append(g.get("id")); paths.append(g.get("path"))
    p=str(g.get("path") or ""); req(p)
    cat=str(g.get("category") or "")
    if p and not p.startswith(f"golden/{cat}/"): fail(f"category/path mismatch for {g.get('id')}: {cat} vs {p}")
    if g.get("provider_sensitive") is True and g.get("freshness_status")=="CURRENT" and not g.get("last_provider_verified_at"):
        fail(f"provider-sensitive CURRENT Golden lacks last_provider_verified_at: {g.get('id')}")
    if "last_reviewed" in g: fail(f"deprecated last_reviewed field present: {g.get('id')}")
if len(ids)!=len(set(ids)): fail("duplicate Golden id in registry")
if len(paths)!=len(set(paths)): fail("duplicate Golden path in registry")

idx_path=str(current.get("golden_index",{}).get("path","golden/GOLDEN_INDEX_CURRENT.txt"))
idx_file=req(idx_path); idx=idx_file.read_text(encoding="utf-8") if idx_file.exists() else ""
pairs=re.findall(r"File:\s*\n(GOLDEN_[^\n]+\.txt)\s*\n\s*Stato:\s*\n([^\n]+)",idx)
idx_map=dict(pairs); reg_map={Path(str(g.get("path"))).name:str(g.get("status")) for g in goldens if g.get("path")}
if idx_map!=reg_map:
    for name in sorted(set(idx_map)|set(reg_map)):
        if idx_map.get(name)!=reg_map.get(name): fail(f"Index/Registry mismatch {name}: index={idx_map.get(name)!r}, registry={reg_map.get(name)!r}")

current_files=set()
for p in ROOT.glob("golden/**/*.txt"):
    rel=p.relative_to(ROOT).as_posix()
    if "/archive/" in f"/{rel}/": continue
    if p.name=="GOLDEN_INDEX_CURRENT.txt" or re.fullmatch(r"GOLDEN_COMPONENTS_INDEX_v\d+\.txt",p.name): continue
    if p.name.startswith("GOLDEN_"): current_files.add(rel)
registered={str(p) for p in paths if p}
for rel in sorted(current_files-registered): fail(f"orphan current Golden not in registry: {rel}")
for rel in sorted(registered-current_files): fail(f"registered Golden missing from current tree: {rel}")

for a,b in [
 (str(current.get("master",{}).get("path","")),str(current.get("master",{}).get("versioned_path",""))),
 (str(current.get("golden_index",{}).get("path","")),str(current.get("golden_index",{}).get("versioned_path","")))
]:
    if a and b:
        pa,pb=req(a),req(b)
        if pa.exists() and pb.exists() and pa.read_bytes()!=pb.read_bytes(): fail(f"alias drift: {a} != {b}")

mp=req(str(current.get("master",{}).get("path","")))
if mp.exists():
    expected=f"Versione v{current.get('master',{}).get('version')} FULL CONSOLIDATA"
    if expected not in mp.read_text(encoding="utf-8"): fail(f"Master CURRENT header does not contain {expected!r}")
iv=current.get("golden_index",{}).get("version")
if idx_file.exists() and f"Versione: {iv}.0" not in idx: fail(f"Golden CURRENT index header is not v{iv}")

def check_pins(path):
    p=req(path)
    if not p.exists(): return
    for n,line in enumerate(p.read_text(encoding="utf-8").splitlines(),1):
        m=re.search(r"\buses:\s*([^\s#]+)",line)
        if not m: continue
        spec=m.group(1)
        ref=spec.rsplit("@",1)[1] if "@" in spec else ""
        if not re.fullmatch(r"[0-9a-f]{40}",ref): fail(f"non-immutable Action ref in {path}:{n}: {spec}")
check_pins(".github/workflows/validate-factory.yml")
for p in [str(g.get("path")) for g in goldens if g.get("id")=="ci_release_web_deploy"]: check_pins(p)

secret_patterns={
 "private key":re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
 "OpenAI project key":re.compile(r"sk-proj-[A-Za-z0-9_-]{20,}"),
 "GitHub classic token":re.compile(r"ghp_[A-Za-z0-9]{30,}"),
 "GitHub fine-grained token":re.compile(r"github_pat_[A-Za-z0-9_]{30,}"),
 "AWS access key":re.compile(r"AKIA[0-9A-Z]{16}")
}
for p in ROOT.rglob("*"):
    if not p.is_file() or ".git" in p.parts: continue
    try: content=p.read_text(encoding="utf-8")
    except UnicodeDecodeError: continue
    for label,pat in secret_patterns.items():
        if pat.search(content): fail(f"possible committed secret ({label}) in {p.relative_to(ROOT)}")

if errors:
    print("APP FACTORY VALIDATION: FAIL")
    for e in errors: print("-",e)
    sys.exit(1)
print(f"APP FACTORY VALIDATION: PASS ({len(goldens)} Golden entries, semantic validator v2)")
