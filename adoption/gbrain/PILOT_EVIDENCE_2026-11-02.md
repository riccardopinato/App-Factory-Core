# GBrain MCP — real integration evidence (2026-11-02)

Scope: user-operated local WSL2 GBrain installation; **documentation and pilot evidence only**, not a CI/runtime release artifact.

## Evidence observed directly in ChatGPT

- User-provided Ubuntu terminal output: manual source-pinned seed import command executed with explicit `IMPORTA` confirmation; the GBrain user-service stopped and restarted.
- `gbrain backup create` reported **Backup created** in a private `~/gbrain-private-backups/` directory; full sensitive DB archive contains no guarantee of every canonical content root. Script also copied the `~/.gbrain/content` tree separately. **Archive integrity, restoration, and off-host storage are NOT VERIFIED**.
- `gbrain import ... --no-embed` output: **1 Markdown page imported**, **2 chunks**, **0 skipped/errors**, with a one-shot marker created.
- Post-import `gbrain mcp expose --status` from the operator's Ubuntu terminal: **receipt OK; Tailscale Funnel published; user systemd service running; local and HTTPS tailnet /health OK**. Operator's actual private tunnel hostname intentionally omitted from this public report.
- Real Chat-only MCP call through the installed **read-only** GBrain plugin: `recall({query:"APP_FACTORY_AUTHORITY CURRENT.yaml Master 27 golden 24",source_id:"default",return_unit:"page",limit:5})` returned slug `app_factory_seed_index_2026-11-02`, title `App Factory — GBrain seed index (pilot, 2026-11-02)`, content including pinned Factory `CURRENT.yaml` v27 and Golden Index v24, `origin:"managed_file_import"`, source `default`, and `trust_tier:"operator_curated"`. **Authenticated end-to-end readback PASS.**
- Model provider configuration remained keyless / keyword-only per the returned `search_degraded: keyword_only_embedding_disabled` warning. This is a retrieval limitation, not a failed MCP call.
- Existing CLI fact #1 from install-check remained readable in the same MCP response.

## Provenance and authority

Seed source: `adoption/gbrain/APP_FACTORY_SEED_INDEX_2026-11-02.md` in this candidate branch, itself pinned to:
- `App-Factory-Core@4086749d1471ab3f750be8d8fb8442c2e74a2baa`
- `Idee-app-Archivi-riferimenti@ca1ccbd28f8b07807218a74ed04ac94fd0948120`
- `AppLab@58cb25070b80673f1e9d12593bceb496b83bc6f0`

**Never treat GBrain content as a replacement for live GitHub CURRENT, app Product Bible/Roadmap, source SHA or exact-head test evidence.** This seed is a timestamped secondary index and is not synchronized in the background.

## Unverified gates and next steps

1. **NOT VERIFIED:** WSL2/Windows shutdown → service auto-restart → tailnet/Funnel/HTTP reachability → new Chat-only MCP readback.
2. **NOT VERIFIED:** Restore rehearsal in an isolated root and validated content/root inventory. Do not restore over the live brain.
3. **NOT VERIFIED:** Encrypted off-host backup and documented retention/recovery controls. The local archive alone is a single-host copy.
4. **NOT VERIFIED:** Negative authorization tests for read-only client and private source; current `read` grant was verified at registration and successful read, but denials were not safely exercised.
5. **NOT VERIFIED:** 20-query usefulness/freshness trial, corrections, revoked-access test, and readiness to merge this PR.

No MCP write permission was granted, no automatic memory writeback enabled, and no GitHub code/CI governance modified by the memory import.
