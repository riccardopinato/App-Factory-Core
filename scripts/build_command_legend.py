#!/usr/bin/env python3
"""Generate and verify the public App Factory command legend from one registry."""
from __future__ import annotations
import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "commands/REGISTRY.json"
MANIFEST = ROOT / "v27/candidate/MODULE_MAP.json"
OUTPUT = ROOT / "commands/LEGGENDA.md"
GROUPS = ["Consultazione", "Verifica", "Catalogo", "Esecuzione", "Design"]
EFFECTS = {
    "SOLA LETTURA",
    "SCRITTURA SOLO CATALOGO (PR + CI)",
    "MODIFICHE SOLO NELLO SCOPE AUTORIZZATO",
    "DESIGN INTERATTIVO; NON IMPLEMENTA IL CODICE",
    "IMPLEMENTAZIONE CON GATE",
}

def normalize(text):
    t = unicodedata.normalize("NFKD", text.casefold())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", t)).strip()

def validate(registry, manifest, root=ROOT):
    if registry.get("schema_version") != 1:
        raise ValueError("Unsupported command registry schema")
    commands = registry.get("commands", [])
    if not commands:
        raise ValueError("Empty command registry")
    routes = {x["id"]: x for x in manifest.get("task_routes", [])}
    public_routes = {rid for rid, x in routes.items() if x.get("public_command") is True}
    ids, triggers, phrases, declared_routes = set(), set(), set(), set()
    for item in commands:
        for k in ("id", "group", "trigger", "title", "description", "effect", "entrypoint", "examples", "notes"):
            if not item.get(k):
                raise ValueError("Incomplete command: " + str(item.get("id")) + "/" + k)
        if item["id"] in ids or normalize(item["trigger"]) in triggers:
            raise ValueError("Duplicate command ID or trigger")
        ids.add(item["id"])
        triggers.add(normalize(item["trigger"]))
        if item["group"] not in GROUPS or item["effect"] not in EFFECTS:
            raise ValueError("Invalid group/effect for " + item["id"])
        source = (root / item["entrypoint"]).resolve()
        if not source.is_relative_to(root.resolve()) or not source.is_file():
            raise ValueError("Missing/unsafe command entrypoint: " + item["entrypoint"])
        route_id = item.get("route_id")
        if route_id:
            if route_id not in public_routes:
                raise ValueError("Route not declared public: " + str(route_id))
            terms = {normalize(t) for t in routes[route_id].get("terms", [])}
            if normalize(item["trigger"]) not in terms:
                raise ValueError("Command trigger not covered by router: " + item["trigger"])
            declared_routes.add(route_id)
        elif item["id"] != "procedi":
            raise ValueError("Only Procedi is a contextual Master command")
        for example in item["examples"]:
            if not example.get("text") or not example.get("description"):
                raise ValueError("Empty command example")
            phrase = normalize(example["text"])
            if phrase in phrases:
                raise ValueError("Duplicate command example: " + phrase)
            phrases.add(phrase)
        if normalize(item["trigger"]) not in {normalize(ex["text"]) for ex in item["examples"]}:
            raise ValueError("Missing trigger among examples: " + item["trigger"])
    if declared_routes != public_routes:
        raise ValueError("Unregistered public route(s): " + repr(sorted(public_routes-declared_routes)))
    for must in ("legenda", "audit", "capability"):
        if must not in ids:
            raise ValueError("Missing core public command: " + must)
    return True

def render(registry, manifest):
    code = lambda text: chr(96) + str(text) + chr(96)
    lines = [
        "# Legenda dei comandi — App Factory",
        "",
        "> Vista generata automaticamente da " + code("commands/REGISTRY.json") + ". Non modificare questo file manualmente.",
        "",
        "**Uso rapido:** scrivi " + code("Legenda") + " in una chat collegata ad App-Factory-Core. Puoi scrivere " + code("Legenda Audit") + " o " + code("Legenda Capability") + " per filtrare.",
        "",
        "## Panoramica",
        "",
        "| Comando | Funzione | Effetto |",
        "| --- | --- | --- |",
    ]
    for group in GROUPS:
        for item in registry["commands"]:
            if item["group"] == group:
                lines.append("| " + code(item["trigger"]) + " | " + item["description"] + " | " + item["effect"] + " |")
    lines += ["", "## Comandi ed esempi", ""]
    for group in GROUPS:
        items = [x for x in registry["commands"] if x["group"] == group]
        if not items:
            continue
        lines += ["### " + group, ""]
        for item in items:
            lines += ["**" + item["title"] + "** — " + item["description"], "", "| Scrivi | Cosa succede |", "| --- | --- |"]
            lines.extend("| " + code(ex["text"]) + " | " + ex["description"] + " |" for ex in item["examples"])
            lines += ["", "**Effetto:** " + item["effect"] + ". " + item["notes"], ""]
    lines += [
        "## Altri argomenti riconosciuti dal router",
        "",
        "Queste sono parole chiave di instradamento tecnico, non comandi autonomi garantiti: richiedono contesto e non conferiscono autorizzazioni aggiuntive.",
        "",
        "| Area | Esempi di termini |",
        "| --- | --- |",
    ]
    for route in manifest.get("task_routes", []):
        if route.get("public_command") is True:
            continue
        label = route["id"].replace("_", " ").title()
        terms = ", ".join(code(t) for t in route.get("terms", [])[:4])
        lines.append("| " + label + " | " + terms + " |")
    lines += [
        "",
        "## Regole e aggiornamento",
        "",
        "- " + code("Legenda") + " mostra i comandi senza eseguirli; " + code("Audit") + " è sola lettura; " + code("Capability") + " può aggiornare soltanto il catalogo, con PR/CI; " + code("Procedi") + " dipende dallo scope autorizzato.",
        "- Per nuovi comandi: aggiornare " + code("commands/REGISTRY.json") + " e dichiarare " + code("public_command: true") + " nella rispettiva route di " + code("v27/candidate/MODULE_MAP.json") + ". Registrare una entrypoint canonica e i gate necessari.",
        "- Generare con " + code("python3 scripts/build_command_legend.py --write") + " e verificare con " + code("--check") + ". La CI blocca legende obsolete, route pubbliche non registrate e duplicati.",
        "- Ogni chat futura deve leggere il registro sul commit Factory fissato per la sessione; non usare una legenda ricordata dalla chat come fonte più recente.",
        "- La modifica GitHub non aggiorna da sola le istruzioni dei ChatGPT Project esterni; il pointer App Factory Core deve essere presente.",
        "",
    ]
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser()
    act = parser.add_mutually_exclusive_group(required=True)
    act.add_argument("--write", action="store_true")
    act.add_argument("--check", action="store_true")
    args = parser.parse_args()
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    validate(reg, manifest)
    expected = render(reg, manifest)
    if args.write:
        OUTPUT.write_text(expected, encoding="utf-8")
        print("COMMAND LEGEND: generated " + str(OUTPUT))
    elif not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != expected:
        raise SystemExit("COMMAND LEGEND DRIFT: run python3 scripts/build_command_legend.py --write")
    else:
        print("COMMAND LEGEND: PASS (registry, public routes and generated Markdown)")

if __name__ == "__main__":
    main()
