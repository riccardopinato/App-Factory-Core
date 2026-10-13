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

- Master Prompt: **v26 FULL**
- Golden Components Index: **v11**
- Golden registry: **v2**
- Semantic validator: **v3**

## Repository layout

```text
CURRENT.yaml
AGENTS.md
CHANGELOG.md
governance/
  agents/
    code-hygiene.md
    testing-validation.md
    git-workflow.md
    research-reuse.md
master/
  MASTER_PROMPT_CURRENT.txt
  MASTER_PROMPT_UTILITY_FLUTTER_CHATGPT_v25_1_FULL.txt
  archive/
golden/
  GOLDEN_INDEX_CURRENT.txt
  GOLDEN_COMPONENTS_INDEX_v10.txt
  GOLDEN_REGISTRY.yaml
  <category>/GOLDEN_*.txt
  archive/
bootstrap/
  APP_FACTORY_BOOTSTRAP.txt
  app_factory_manifest.example.yaml
schemas/
scripts/validate_factory.py
scripts/requirements.txt
.github/workflows/validate-factory.yml
evidence/
```

## Governance

- `CURRENT.yaml` is the resolver.
- `MASTER_PROMPT_CURRENT.txt` and `GOLDEN_INDEX_CURRENT.txt` are stable aliases.
- Versioned files remain available for audit/history.
- The Golden registry is the canonical path/status/freshness map.
- Root `AGENTS.md` is the agent operating contract for Core work; it does not replace Master/Golden authority.
- Tool-specific agent bridges must remain thin/derived rather than independent policy sources.
- DRAFT/CANDIDATE never becomes COPY-READY or CERTIFIED automatically.
- CI validates repository consistency only; it does not certify app runtime behavior.
- No secrets, API keys, signing keys or credentials belong in this repository.

## Update rule

A Master/Golden framework update should update, in one coherent change:

1. versioned document;
2. CURRENT alias;
3. `CURRENT.yaml`;
4. Golden index/registry when applicable;
5. `CHANGELOG.md`;
6. agent-governance contract/modules/validator when that policy changes.

See `bootstrap/APP_FACTORY_BOOTSTRAP.txt` for the short reusable bootstrap instruction.

## ChatGPT Project pointer

To prevent old chats from selecting a stale Master Prompt, copy the instruction in `bootstrap/PROJECT_CUSTOM_INSTRUCTION.txt` into the ChatGPT Project instructions. The repository remains the canonical source of truth.


## Validation semantics

A green Factory validation now means YAML/schema parsing, CURRENT alias equality,
Index↔Registry semantic consistency, orphan detection, freshness invariants,
basic secret-pattern scanning, immutable GitHub Action SHA checks, and Agent
Governance contract/module/invariant checks all pass.

It still does **not** certify runtime behavior of any app.

## Main branch governance

Normal Core changes follow branch -> PR -> green Factory validation -> merge.
Repository branch/ruleset protection should require the validation check and
block force-push/delete. See `GOVERNANCE.md`.
