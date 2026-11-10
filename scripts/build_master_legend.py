#!/usr/bin/env python3
"""Deterministic, read-only navigation legend for active modular v27.

Source of truth: MODULE_MAP.json plus CURRENT.yaml. This file creates an index,
not a second editable policy document or new public command.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "v27/candidate/MODULE_MAP.json"
OUT = ROOT / "v27/candidate/MASTER_LEGEND_CURRENT.md"
EXPECTED = {
    *[f"A{x:02d}" for x in range(1, 12)],
    *[f"M{x:02d}" for x in range(1, 11)],
    *[f"R{x:02d}" for x in range(1, 7)],
}


def render(manifest: dict) -> str:
    policies = manifest.get("policy_updates", [])
    reviewed = [tag for p in policies for tag in p.get("review_item_ids", [])]
    if len(reviewed) != len(set(reviewed)) or set(reviewed) != EXPECTED:
        raise ValueError("the 27 approved review items must each have one module owner")
    mods = manifest["modules"]
    routes = manifest["task_routes"]
    lines = [
        "# App Factory v27 — Master Legend",
        "",
        "> GENERATED navigation index. Do not edit manually or use as a second policy source.",
        "> Baseline authority: `CURRENT.yaml` → Master Core → relevant modules → relevant Golden.",
        "",
        "## Canonical documents",
        "",
        "- **Master Core:** `v27/candidate/MASTER_CORE_v27_CANDIDATE.txt`",
        "- **Router and immutable seals:** `v27/candidate/MODULE_MAP.json`",
        "- **Full operative text (generated):** `v27/candidate/MASTER_FULL_FALLBACK_GENERATED.txt`",
        "- **Existing public commands:** `commands/REGISTRY.json` and `commands/LEGGENDA.md`",
        "- **Reusable components and freshness:** `golden/GOLDEN_REGISTRY.yaml` and `golden/GOLDEN_INDEX_CURRENT.txt`",
        "- **Agent operating contract:** `AGENTS.md`",
        "",
        "## Legacy instruction modules (byte-exact v26.8 section allocation)",
        "",
        "| Module | File | Sections | Task selectors |",
        "|---|---|---|---|",
    ]
    for m in mods:
        lines.append(
            f"| `{m['id']}` | `{m['path']}` | "
            f"{', '.join(m['section_ids'])} | {', '.join(m.get('selectors', []))} |"
        )
    lines.extend([
        "",
        "## Specialized policy modules (v27 overrides/additions)",
        "",
        "| Module | File | Selectors | Review item IDs |",
        "|---|---|---|---|",
    ])
    for p in policies:
        lines.append(
            f"| `{p['id']}` | `{p['path']}` | "
            f"{', '.join(p.get('selectors', [])) or '—'} | "
            f"{', '.join(p.get('review_item_ids', [])) or '—'} |"
        )
    lines.extend(["", "## Router map", "", "| Route | Modules | Golden IDs |",
                  "|---|---|---|"])
    for r in routes:
        lines.append(
            f"| `{r['id']}` | {', '.join(r.get('modules', [])) or '—'} | "
            f"{', '.join(r.get('golden_ids', [])) or '—'} |"
        )
    lines.extend([
        "",
        "## How to use this index",
        "",
        "1. Resolve `CURRENT.yaml` once and pin the Factory commit SHA.",
        "2. Classify the user's task and respect public-command isolation.",
        "3. Load only its registered modules and relevant Golden/consumer evidence.",
        "4. On ambiguity or invalid module seals, use the verified synchronized fallback or BLOCK.",
        "5. Treat E3 donor, E5 consumer, CI, device, provider, deploy and Store as distinct evidence.",
        "",
        "## Review intake coverage",
        "",
        "All 27 selected options from 2026-11-10 are assigned exactly once in the table above: ",
        "A01–A11 (add), M01–M10 (modify) and R01–R06 (retire/clean up conditionally).",
        "A retirement proposal never authorizes deletion of protected history or bypass of a gate.",
        "",
        "This navigation index does not prove runtime behavior, commercial viability or source availability.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser()
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = p.parse_args()
    expected = render(json.loads(MAP.read_text(encoding="utf-8")))
    if args.write:
        OUT.write_text(expected, encoding="utf-8")
        print(f"MASTER LEGEND GENERATED: {OUT.relative_to(ROOT)}")
    else:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != expected:
            raise SystemExit("MASTER LEGEND DRIFT: run --write")
        print("MASTER LEGEND CHECK: PASS — 27 review items, modules and routes synchronized")


if __name__ == "__main__":
    main()
