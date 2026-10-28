#!/usr/bin/env python3
from __future__ import annotations
from datetime import date, datetime
from pathlib import Path
import json, re, sys, subprocess, tempfile
import yaml
from jsonschema import Draft202012Validator, FormatChecker

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
    v=Draft202012Validator(schema,format_checker=FormatChecker())
    for e in sorted(v.iter_errors(instance),key=lambda x:list(x.path)):
        loc=".".join(str(x) for x in e.path) or "<root>"
        fail(f"{label} schema violation at {loc}: {e.message}")

current=load_yaml("CURRENT.yaml")
manifest=load_json("schemas/golden_manifest.schema.json")
registry=load_yaml("golden/GOLDEN_REGISTRY.yaml")
schema_validate(current,"schemas/current.schema.json","CURRENT.yaml")
registry_schema=load_json("schemas/golden_registry.schema.json")
if registry_schema:
    # Inline the entry schema for deterministic local validation without remote/ref resolution.
    registry_schema["properties"]["goldens"]["items"] = manifest
    v=Draft202012Validator(registry_schema,format_checker=FormatChecker())
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

alias_pairs=[
 (str(current.get("golden_index",{}).get("path","")),str(current.get("golden_index",{}).get("versioned_path","")))
]
if str(current.get("master",{}).get("version")) not in ("27","27.0"):
    alias_pairs.insert(0,(str(current.get("master",{}).get("path","")),str(current.get("master",{}).get("versioned_path",""))))
for a,b in alias_pairs:
    if a and b:
        pa,pb=req(a),req(b)
        if pa.exists() and pb.exists() and pa.read_bytes()!=pb.read_bytes(): fail(f"alias drift: {a} != {b}")

mp=req(str(current.get("master",{}).get("path","")))
active_version=str(current.get("master",{}).get("version"))
if mp.exists():
    if active_version in ("27","27.0"):
        if "APP FACTORY v27" not in mp.read_text(encoding="utf-8"):
            fail("Active modular Master does not declare v27")
        if "CANDIDATE ONLY" in mp.read_text(encoding="utf-8"):
            fail("Active modular Master still marked as candidate")
        mod_manifest=load_json("v27/candidate/MODULE_MAP.json")
        if mod_manifest.get("status")!="ACTIVE":
            fail("Active v27 must have ACTIVE manifest status")
        if current.get("master",{}).get("modular_manifest")!="v27/candidate/MODULE_MAP.json":
            fail("v27 current.modular_manifest mismatch")
        if mod_manifest.get("core",{}).get("path")!=str(mp.relative_to(ROOT)):
            fail("v27 manifest core path mismatch")
        if mod_manifest.get("living_fallback",{}).get("path")!=str(current.get("master",{}).get("versioned_path")):
            fail("v27 operative full fallback path mismatch")
        check=subprocess.run([sys.executable,"scripts/build_v27_fallback.py","--check"],
                             cwd=ROOT,capture_output=True,text=True,check=False)
        if check.returncode!=0:
            fail("v27 fallback check failed: "+(check.stderr+check.stdout)[-1200:])
    else:
        expected=f"Versione v{active_version} FULL CONSOLIDATA"
        if expected not in mp.read_text(encoding="utf-8"):
            fail(f"Master CURRENT header does not contain {expected!r}")
# Adaptive Execution v26.8: deterministic policy/playbook drift check.
# This proves presence/consistency, NOT that a model actually follows the policy.
if str(current.get("master",{}).get("version"))=="26.8" and mp.exists():
    source=mp.read_text(encoding="utf-8")
    header="1.3 ADAPTIVE EXECUTION — MINIMUM NECESSARY PROCESS"
    section=source.split(header,1)[1].split("\n2. GITHUB / REMOTE ACCESS",1)[0] if header in source else ""
    must_contain=[
        '"Procedi"',
        "DIRETTO",
        "PARALLELO",
        "CONTROLLATO",
        "READ-ONLY",
        "FAIL-FAST BEFORE EXPENSIVE CI",
        "source SHA",
        "exact head",
        "required checks",
        "non aggiungere tracking",
        "CASI DI CONTROLLO",
    ]
    for token in must_contain:
        if token.casefold() not in section.casefold():
            fail(f"Adaptive Execution v26.8 policy missing: {token}")
    fast=load_json("playbooks/FAST_DELIVERY.json")
    steps={s.get("id"):s for s in fast.get("steps",[]) if isinstance(s,dict)}
    for step_id,markers,gate in (
        ("BASELINE",("pinned","SHA"),"EVIDENCE_REQUIRED"),
        ("PREFLIGHT",("BEFORE expensive CI","instrumentation"),"STOP_ON_BLOCKER"),
        ("EXACT_HEAD",("exact integrated head","source SHA"),"EXACT_HEAD_GREEN"),
    ):
        st=steps.get(step_id,{})
        action=st.get("action","")
        if st.get("gate")!=gate or any(m.casefold() not in action.casefold() for m in markers):
            fail(f"FAST_DELIVERY {step_id} drifted from Adaptive Execution v26.8")

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

signing_paths=[str(g.get("path")) for g in goldens if g.get("id")=="android_signing_release_identity"]
if len(signing_paths)!=1:
    fail("expected exactly one android_signing_release_identity Golden")
else:
    sp=req(signing_paths[0])
    if sp.exists():
        st=sp.read_text(encoding="utf-8")
        required_signing_contract=[
            "ANDROID_KEYSTORE_BASE64",
            "ANDROID_KEYSTORE_PASSWORD",
            "ANDROID_KEY_ALIAS",
            "ANDROID_KEY_PASSWORD",
            "CI GREEN != PRODUCTION SIGNING VERIFIED",
            "first production run",
            "workflow_dispatch",
            "certificateSha256",
            "build once -> hash -> test -> distribute same bytes",
            "UPLOAD KEY",
            "PLAY APP SIGNING KEY",
        ]
        for token in required_signing_contract:
            if token not in st:
                fail(f"Android signing Golden missing required contract token: {token}")

ci_paths=[str(g.get("path")) for g in goldens if g.get("id")=="ci_release_web_deploy"]
for cp in ci_paths:
    p=req(cp)
    if p.exists():
        txt=p.read_text(encoding="utf-8")
        if "GOLDEN_ANDROID_SIGNING_RELEASE_IDENTITY_v1_DRAFT.txt" not in txt:
            fail("CI/Release Golden must reference Android Signing / Release Identity Golden")
        if "PRODUCTION SIGNING VERIFIED != STORE READY" not in txt:
            fail("CI/Release Golden missing production-signing vs Store Ready boundary")


# Agent Governance contract: keep the canonical entrypoint compact, modular and
# mechanically tied to the critical Factory invariants.
agent_path=req("AGENTS.md")
agent_modules=[
    "governance/agents/code-hygiene.md",
    "governance/agents/testing-validation.md",
    "governance/agents/git-workflow.md",
    "governance/agents/research-reuse.md",
]
for p in agent_modules: req(p)

if agent_path.exists():
    agent_bytes=agent_path.read_bytes()
    agent_text=agent_bytes.decode("utf-8")
    agent_lines=len(agent_text.splitlines())
    if agent_lines>200: fail(f"AGENTS.md portability budget exceeded: {agent_lines} lines > 200")
    if len(agent_bytes)>24000: fail(f"AGENTS.md portability budget exceeded: {len(agent_bytes)} bytes > 24000")
    required_agent_tokens=[
        "CURRENT.yaml",
        "governance/agents/code-hygiene.md",
        "governance/agents/testing-validation.md",
        "governance/agents/git-workflow.md",
        "governance/agents/research-reuse.md",
        "Adding a replacement without evaluating removal of the superseded implementation is incomplete work.",
        "tool-specific",
        "Once implementation is authorized, no separate user approval is required for a PR merge.",
    ]
    for token in required_agent_tokens:
        if token not in agent_text:
            fail(f"AGENTS.md missing required contract token: {token}")

for gid in ("agent_governance","code_hygiene"):
    matches=[g for g in goldens if g.get("id")==gid]
    if len(matches)!=1:
        fail(f"expected exactly one {gid} Golden")
    else:
        gp=req(str(matches[0].get("path")))
        if gp.exists():
            gt=gp.read_text(encoding="utf-8")
            required = (
                ["AGENTS.md","CURRENT.yaml","tool-specific","drift"]
                if gid=="agent_governance"
                else [
                    "Adding a replacement without evaluating removal of the superseded implementation is incomplete work.",
                    "BOUNDED",
                    "unused dependencies",
                    "DOPO cleanup",
                ]
            )
            for token in required:
                if token not in gt:
                    fail(f"{gid} Golden missing required contract token: {token}")


# Factory automation layer v22.
for path in [
    "contracts/failure_taxonomy_v1.json",
    "contracts/maintenance_lanes_v1.json",
    "contracts/exact_artifact_manifest_v1.schema.json",
    "contracts/rollout_state_v1.json",
    "contracts/recovery_scenario_matrix_v1.json",
]:
    load_json(path)

playbook_schema=load_json("schemas/factory_playbook.schema.json")
for path in [
    "playbooks/FAST_DELIVERY.json",
    "playbooks/FAILURE_TRIAGE.json",
    "playbooks/DONOR_PROMOTION.json",
    "playbooks/CONTROLLED_ROLLOUT.json",
    "playbooks/BUILD_ONCE_VERIFY_MANY.json",
    "playbooks/ADOPT_FACTORY_MODE.json",
]:
    data=load_json(path)
    if playbook_schema and data:
        v=Draft202012Validator(playbook_schema,format_checker=FormatChecker())
        for e in sorted(v.iter_errors(data),key=lambda x:list(x.path)):
            loc=".".join(str(x) for x in e.path) or "<root>"
            fail(f"{path} schema violation at {loc}: {e.message}")

failure_contract=load_json("contracts/failure_taxonomy_v1.json")
required_failure_classes={"APP_RUNTIME_FAILURE","APP_VISUAL_FAILURE","BUILD_OR_QUALITY_FAILURE","INFRA_ERROR","FLAKY_SUSPECT","UNKNOWN_FAILURE"}
if set((failure_contract.get("classes") or {}).keys())!=required_failure_classes:
    fail("failure taxonomy classes do not match canonical v1 set")

maintenance_contract=load_json("contracts/maintenance_lanes_v1.json")
if set((maintenance_contract.get("lanes") or {}).keys())!={"BLOCKING_NOW","FIX_CURRENT_STEP","BACKGROUND_MAINTENANCE","FUTURE"}:
    fail("maintenance lanes do not match canonical v1 set")
if (maintenance_contract.get("pattern_recurrence") or {}).get("threshold")!=3:
    fail("Pattern-3 recurrence threshold must remain 3")
if (maintenance_contract.get("pattern_recurrence") or {}).get("auto_promote") is not False:
    fail("Pattern-3 must never auto-promote")

recovery_contract=load_json("contracts/recovery_scenario_matrix_v1.json")
required_recovery={"EVENT_LOSS","DUPLICATE_DELIVERY","EXECUTOR_OUTAGE","INTERRUPTED_OPERATION","COORDINATOR_RESTART","EXPIRED_LEASE","SUPERSEDING_SHA","WATCHER_RECOVERY"}
if {x.get("id") for x in recovery_contract.get("scenarios",[]) if isinstance(x,dict)}!=required_recovery:
    fail("recovery scenario matrix does not match canonical v1 set")

runner=req("scripts/run_factory_playbook.py")
if runner.exists():
    rt=runner.read_text(encoding="utf-8")
    for token in ("PROCESS_ONLY","--playbook","--inputs-json","missing_inputs"):
        if token not in rt: fail(f"Factory playbook runner missing required token: {token}")
    try:
        compile(rt, "scripts/run_factory_playbook.py", "exec")
    except SyntaxError as e:
        fail(f"Factory playbook runner syntax error: {e}")
    smoke=subprocess.run(
        [sys.executable, str(runner), "--list"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    if smoke.returncode!=0:
        fail(f"Factory playbook runner --list failed: {smoke.stderr.strip()}")
    else:
        for playbook_id in ("FAST_DELIVERY","FAILURE_TRIAGE","DONOR_PROMOTION","CONTROLLED_ROLLOUT","BUILD_ONCE_VERIFY_MANY","ADOPT_FACTORY_MODE"):
            if playbook_id not in smoke.stdout:
                fail(f"Factory playbook runner --list missing {playbook_id}")
    ready=subprocess.run(
        [
            sys.executable, str(runner),
            "--playbook","FAST_DELIVERY",
            "--inputs-json",
            '{"repository":"owner/repo","baseline_sha":"0123456789012345678901234567890123456789","authorized_scope":"step"}',
            "--json",
        ],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    if ready.returncode!=0:
        fail(f"Factory playbook runner READY smoke failed: {ready.stderr.strip()}")
    else:
        try:
            ready_payload=json.loads(ready.stdout)
        except json.JSONDecodeError as e:
            fail(f"Factory playbook runner READY smoke invalid JSON: {e}")
        else:
            if ready_payload.get("ready") is not True:
                fail("Factory playbook runner READY smoke did not report ready=true")
            if ready_payload.get("authority")!="PROCESS_ONLY":
                fail("Factory playbook runner READY smoke authority drift")


# Factory Adoption Kit v1.
profile=load_yaml("adoption/FACTORY_MODE_PROFILE_v1.yaml")
schema_validate(profile,"schemas/factory_mode_profile.schema.json","FACTORY_MODE_PROFILE_v1.yaml")
adoption_template=load_yaml("adoption/APP_FACTORY_ADOPTION.yaml")
adoption_schema=load_json("schemas/factory_adoption.schema.json")
if adoption_schema and adoption_template:
    v=Draft202012Validator(adoption_schema,format_checker=FormatChecker())
    for e in sorted(v.iter_errors(adoption_template),key=lambda x:list(x.path)):
        loc=".".join(str(x) for x in e.path) or "<root>"
        fail(f"adoption/APP_FACTORY_ADOPTION.yaml schema violation at {loc}: {e.message}")

if (profile.get("workflow_integration") or {}).get("strategy")!="INTEGRATE_PRESERVE_EXISTING":
    fail("Factory mode profile must preserve/integrate existing workflows")
if (profile.get("workflow_integration") or {}).get("overwrite_existing_workflows") is not False:
    fail("Factory mode profile must forbid workflow overwrite")
if (profile.get("workflow_integration") or {}).get("replace_existing_workflows") is not False:
    fail("Factory mode profile must forbid workflow replacement")
if (profile.get("authority") or {}).get("can_overwrite_custom_workflows") is not False:
    fail("Factory mode authority drift: custom workflow overwrite enabled")

for path in ("scripts/adopt_factory_mode.py","scripts/validate_factory_adoption.py"):
    p=req(path)
    if p.exists():
        text_value=p.read_text(encoding="utf-8")
        try:
            compile(text_value,path,"exec")
        except SyntaxError as e:
            fail(f"{path} syntax error: {e}")

adopter=req("scripts/adopt_factory_mode.py")
adoption_validator=req("scripts/validate_factory_adoption.py")
if adopter.exists() and adoption_validator.exists():
    with tempfile.TemporaryDirectory(prefix="factory-adoption-") as tmp:
        repo_root=Path(tmp)
        workflows=repo_root/".github"/"workflows"
        workflows.mkdir(parents=True)
        custom=workflows/"custom.yml"
        custom_bytes=b"name: Custom\non: [push]\njobs: {}\n"
        custom.write_bytes(custom_bytes)

        dry=subprocess.run(
            [
                sys.executable,str(adopter),
                "--repo-root",str(repo_root),
                "--repository","owner/sample",
                "--json",
            ],
            cwd=ROOT,capture_output=True,text=True,check=False,
        )
        if dry.returncode!=0:
            fail(f"Factory adoption dry-run failed: {dry.stderr.strip()}")
        else:
            try: dry_payload=json.loads(dry.stdout)
            except json.JSONDecodeError as e: fail(f"Factory adoption dry-run invalid JSON: {e}")
            else:
                if dry_payload.get("workflow_action")!="PRESERVE_EXISTING_AND_INTEGRATE":
                    fail("Factory adoption dry-run did not preserve existing workflow")
                if (repo_root/"APP_FACTORY_ADOPTION.yaml").exists():
                    fail("Factory adoption dry-run wrote the manifest")

        apply1=subprocess.run(
            [
                sys.executable,str(adopter),
                "--repo-root",str(repo_root),
                "--repository","owner/sample",
                "--apply","--json",
            ],
            cwd=ROOT,capture_output=True,text=True,check=False,
        )
        if apply1.returncode!=0:
            fail(f"Factory adoption apply failed: {apply1.stderr.strip()}")
        manifest_path=repo_root/"APP_FACTORY_ADOPTION.yaml"
        first_manifest=manifest_path.read_bytes() if manifest_path.is_file() else b""
        if not first_manifest:
            fail("Factory adoption apply did not create APP_FACTORY_ADOPTION.yaml")
        if custom.read_bytes()!=custom_bytes:
            fail("Factory adoption modified an existing custom workflow")

        check=subprocess.run(
            [sys.executable,str(adoption_validator),"--repo-root",str(repo_root),"--json"],
            cwd=ROOT,capture_output=True,text=True,check=False,
        )
        if check.returncode!=0:
            fail(f"Factory adoption validator smoke failed: {check.stderr.strip()} {check.stdout.strip()}")
        else:
            try: check_payload=json.loads(check.stdout)
            except json.JSONDecodeError as e: fail(f"Factory adoption validator smoke invalid JSON: {e}")
            else:
                if check_payload.get("aligned") is not True:
                    fail("Factory adoption validator smoke did not report aligned=true")
                if check_payload.get("workflow_overwrite_allowed") is not False:
                    fail("Factory adoption validator allowed workflow overwrite")

        apply2=subprocess.run(
            [
                sys.executable,str(adopter),
                "--repo-root",str(repo_root),
                "--repository","owner/sample",
                "--apply","--json",
            ],
            cwd=ROOT,capture_output=True,text=True,check=False,
        )
        if apply2.returncode!=0:
            fail(f"Factory adoption second apply failed: {apply2.stderr.strip()}")
        second_manifest=manifest_path.read_bytes() if manifest_path.is_file() else b""
        if first_manifest!=second_manifest:
            fail("Factory adoption is not idempotent")
        if custom.read_bytes()!=custom_bytes:
            fail("Factory adoption second apply modified an existing custom workflow")

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
print(f"APP FACTORY VALIDATION: PASS ({len(goldens)} Golden entries, semantic validator v7)")
