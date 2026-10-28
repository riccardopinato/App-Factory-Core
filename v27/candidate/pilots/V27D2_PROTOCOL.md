# v27D2 — paired model-behavior evaluation protocol

Status: PREPARED; genuine model outputs NOT VERIFIED. This is not certification.

## Scope

Compare a version-pinned v26.8 full Master, Index and Registry against only the v27 core, selected modules and Registry. Provide identical task and source-grounded product context in both arms, with the same relevant Golden documents and output contract.

Case manifest: pilots/D2_BEHAVIORAL_CASES.json (16 cases).
Runner: scripts/evaluate_v27d2.py.

## How to reproduce

Install tiktoken==0.12.0. Then run:

- python3 scripts/evaluate_v27d2.py --self-test --bench --require-tokenizer
- python3 scripts/evaluate_v27d2.py --export /tmp/d2-paired-prompts.jsonl
- After capturing real independent model replies: python3 scripts/evaluate_v27d2.py --score /path/to/real-model-responses.json

Exported prompts contain no expected answer. Do not expose reference verdicts in the model input. Capture two distinct real model calls per case with the same model and effort, unique request IDs, exact prompt hashes, provider input/output token receipts, measured wall time and response text. Independent qualitative review must inspect actions, not keyword presence alone.

## What CI and tokenizer results mean

o200k_base counts are reproducible tokens under that tokenizer for the fully rendered prompt. These are NOT ChatGPT GPT-6 actual billed input tokens, cached tokens, tool frames, hidden routing or model request latency. Local resolver milliseconds are CPU-only timings and are NOT the end-to-end time to first edit, successful build or merge.

## Hard gates

Any regression on audit-write boundaries, PIN/strong biometric proof, storage migrations, old-CI reuse, fake PASS, physical-vs-store certification, rollout authorization, generated fallback synchronization or failing closed is a blocker. Zero severe violations are tolerated; good average token savings cannot offset a single safety regression.

The script does not run any generative model. Its --score operation is evidence-gated and cannot certify externally asserted metadata on its own. A reviewer must match entries against trusted provider logs and inspect semantic correctness. In the absence of actual paired outputs and comparable real workflow measurements, v27E stays HOLD. CURRENT.yaml remains on v26.8.
