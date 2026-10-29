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

## Optional real model execution (requires user-configured paid API)

The evaluation can be run only on explicit manual workflow dispatch: [v27D2 Real Paired Model Eval](https://github.com/riccardopinato/App-Factory-Core/actions/workflows/v27d2-real-paired-eval.yml). An OpenAI API key must be configured by the repository owner as an Actions secret named `OPENAI_API_KEY`. The user must type `RUN_32_PAID_REQUESTS` to initiate the paid 16 x 2 API calls and choose an accessible model and reasoning effort. Do not paste the key into source code or conversation; do not assume ChatGPT plan access equals API entitlement.

The workflow uses immutable action revisions, read-only repository permissions, exact source checks and a 7-day evidence artifact. The runner writes real response IDs, model identity, prompt SHA-256, provider input/output token counts, observed elapsed time and unmodified model response text. It never awards itself an independent PASS. Review the 16 pairs separately against the protected decision gates before providing `independent_reviews` and running the separate --score step. API usage is billed, and model availability and actual price depend on the connected project. Workflow dispatch is not automatic and is not part of required PR CI.

## Crash-safe, cost-bounded manual evaluation (runner update)

The manual Actions workflow defaults to a **2-request paid preflight** using
the documented model ID `gpt-6.1-sol` (subject to API project access).
It never starts on PR, push or schedule. The owner must configure the
`OPENAI_API_KEY` Actions secret and type `RUN_32_PAID_REQUESTS` each time.

1. Run the workflow with `max_new_requests=2`, no resume ID.
   Retrieve the `v27d2-real-model-outputs` artifact and inspect the two
   real provider receipts. This is **not** a policy-equivalence verdict.
2. Run the same workflow again with `resume_run_id` set to the previous
   GitHub Actions run ID, the **same model and effort**, and
   `max_new_requests=32`. The runner verifies existing case IDs, prompt
   hashes, model/effort, provider IDs, recorded timings, usage and JSON
   response/metadata agreement before making any additional paid calls.
   It skips already completed pairs; after the 2-request preflight, at most
   30 new calls are necessary to reach 32.
3. If an execution stops, use its partial artifact's run ID as the next
   resume source. Artifacts expire after **7 days**. Do not mix different
   policy source versions, model aliases or reasoning efforts. A corrupt,
   incomplete or expired checkpoint must **fail closed**; never manually
   mark missing model responses as completed.
4. When all 32 receipts exist, independently inspect all 16 pairs against
   the reference case manifest, including each response's
   `rationale` and `proposed_actions`. Record named reviews and
   evidence links separately; the API runner **never** self-certifies.
   Run the existing scorer only against the fully reviewed evidence.

The workflow requests no paid API calls until the explicit manual dispatch.
Its offline CI regression test uses temporary mocked responses only, with
no credentials, network calls, promotion decision or real-model evidence.
The output-token cap and model prices still apply per actual request;
select a model available to your API project before authorizing costs.

## Release authority revision — 2026-10-29

This original D2 protocol is preserved as **OPTIONAL** research. It is **not**
the sole activation pathway. The owner requires zero additional spending.
See `../ACTIVATION_CONTRACT.md` for the controlled zero-cost release gate
with strict exact-head CI, source-level safety checks, fail-closed fallback,
explicit non-certification and rollback. No API run was conducted.
