#!/usr/bin/env python3
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]

def req(path):
    p=ROOT/path
    if not p.is_file(): errors.append(f"missing file: {path}")
    return p

current=req('CURRENT.yaml')
text=current.read_text(encoding='utf-8') if current.exists() else ''
for path in re.findall(r'^\s*(?:path|versioned_path):\s*([^#\s]+)\s*$', text, flags=re.M):
    req(path)

registry=req('golden/GOLDEN_REGISTRY.yaml')
reg=registry.read_text(encoding='utf-8') if registry.exists() else ''
paths=re.findall(r'^\s*path:\s*(golden/[^#\s]+)\s*$', reg, flags=re.M)
ids=re.findall(r'^\s*- id:\s*([a-z0-9_]+)\s*$', reg, flags=re.M)
if len(ids)!=len(set(ids)): errors.append('duplicate Golden id in registry')
if len(paths)!=len(set(paths)): errors.append('duplicate Golden path in registry')
for p in paths: req(p)

index=req('golden/GOLDEN_INDEX_CURRENT.txt')
idx=index.read_text(encoding='utf-8') if index.exists() else ''
logical=set(re.findall(r'^GOLDEN_[A-Z0-9_()\-]+\.txt$', idx, flags=re.M))
registered={Path(p).name for p in paths}
missing=sorted(logical-registered)
if missing: errors.append('index Golden file(s) not in registry: '+', '.join(missing))

master=req('master/MASTER_PROMPT_CURRENT.txt')
if master.exists() and 'Versione v25 FULL CONSOLIDATA' not in master.read_text(encoding='utf-8'):
    errors.append('MASTER_PROMPT_CURRENT is not v25 FULL')

pairs=[
 ('master/MASTER_PROMPT_CURRENT.txt','master/MASTER_PROMPT_UTILITY_FLUTTER_CHATGPT_v25_FULL.txt'),
 ('golden/GOLDEN_INDEX_CURRENT.txt','golden/GOLDEN_COMPONENTS_INDEX_v9.txt'),
]
for a,b in pairs:
    pa,pb=req(a),req(b)
    if pa.exists() and pb.exists() and pa.read_bytes()!=pb.read_bytes():
        errors.append(f'alias drift: {a} != {b}')

if errors:
    print('APP FACTORY VALIDATION: FAIL')
    for e in errors: print('-',e)
    sys.exit(1)
print(f'APP FACTORY VALIDATION: PASS ({len(ids)} Golden entries)')
