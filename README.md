# App Factory Core

Canonical source of truth for the App Utility Factory.

## Current baseline

Do **not** guess the current Master Prompt from chat memory or old attachments.
Resolve it deterministically:

1. `CURRENT.yaml`
2. `master/MASTER_PROMPT_CURRENT.txt`
3. `golden/GOLDEN_INDEX_CURRENT.txt`
4. `golden/GOLDEN_REGISTRY.yaml`
5. only the Golden documents relevant to the task

The commit SHA used for this read becomes the **Factory baseline** for the session.
Do not refresh it between consecutive steps unless the central framework changes or a refresh is explicitly requested.

## Current versions

- Master Prompt: **v25 FULL**
- Golden Components Index: **v9**
- Golden registry: **v1**

## Repository layout

```text
CURRENT.yaml
CHANGELOG.md
master/
  MASTER_PROMPT_CURRENT.txt
  MASTER_PROMPT_UTILITY_FLUTTER_CHATGPT_v25_FULL.txt
  archive/
golden/
  GOLDEN_INDEX_CURRENT.txt
  GOLDEN_COMPONENTS_INDEX_v9.txt
  GOLDEN_REGISTRY.yaml
  <category>/GOLDEN_*.txt
  archive/
bootstrap/
  APP_FACTORY_BOOTSTRAP.txt
  app_factory_manifest.example.yaml
schemas/
scripts/validate_factory.py
.github/workflows/validate-factory.yml
evidence/
```

## Governance

- `CURRENT.yaml` is the resolver.
- `MASTER_PROMPT_CURRENT.txt` and `GOLDEN_INDEX_CURRENT.txt` are stable aliases.
- Versioned files remain available for audit/history.
- The Golden registry is the canonical path/status/freshness map.
- DRAFT/CANDIDATE never becomes COPY-READY or CERTIFIED automatically.
- CI validates repository consistency only; it does not certify app runtime behavior.
- No secrets, API keys, signing keys or credentials belong in this repository.

## Update rule

A Master/Golden framework update should update, in one coherent change:

1. versioned document;
2. CURRENT alias;
3. `CURRENT.yaml`;
4. Golden index/registry when applicable;
5. `CHANGELOG.md`.

See `bootstrap/APP_FACTORY_BOOTSTRAP.txt` for the short reusable bootstrap instruction.

## ChatGPT Project pointer

To prevent old chats from selecting a stale Master Prompt, copy the instruction in `bootstrap/PROJECT_CUSTOM_INSTRUCTION.txt` into the ChatGPT Project instructions. The repository remains the canonical source of truth.
