# GBrain MCP — App Factory memory pilot (candidate)

Date: 2026-11-02. Status: **LIVE MCP READ-ONLY CONNECTION VERIFIED; CURATED SEED PREPARED; IMPORT, BACKUP AND REBOOT TEST PENDING**.
Scope: optional external memory service for ChatGPT, in **Chat** (not Work). No change to the App Factory governance, Master, Golden, application repositories, CI, background execution, or current baseline.

## Current execution evidence (2026-11-02)

- Live operator logs: WSL2 Ubuntu systemd, Bun 1.4.4, GBrain 0.60.554.0, local PGLite keyless, initial doctor 100/100, explicit remember/recall fact #1 PASS.
- Automatic event extraction and ambient memory writeback explicitly disabled. No paid embedding provider configured.
- Tailscale Funnel exposure and HTTPS health PASS; user-service status ACTIVE, no exact personal endpoint or credentials reproduced in this public document.
- Native ChatGPT OAuth public-PKCE registration with **read-only** grant on source `default`; owner approval completed.
- Real Chat-mode GBrain connector call to `recall` returned fact #1 with `install-check` provenance: **MCP READ E2E PASS**.
- Pending: secure local backup, staged import of reviewed App Factory memory seed, post-import MCP readback, restart/reboot/sleep recovery, negative permission checks, source freshness audits, final pilot review. Live proof of these is NOT VERIFIED.
- The curated, source-pinned first seed is `adoption/gbrain/APP_FACTORY_SEED_INDEX_2026-11-02.md`; a guarded manual WSL import helper is `adoption/gbrain/import_seed_wsl.sh`. The helper stops the GBrain PGLite service briefly, attempts private backup before importing, and restarts it. **Neither has been run on the operator host.** Import is not a background or automatic update.

## 0. Decision and authority

Use GBrain as an **optional, secondary memory index** for cross-project decisions and references, not as an authority for runtime facts or official roadmaps.

Strict authority:
1. `App-Factory-Core/CURRENT.yaml` selects current Master, Goldens and validation, at a pinned exact SHA per session.
2. The target app's Product Bible, Roadmap, actual code, exact-head CI, device tests and release evidence determine the app's state.
3. `AppLab` controls its own QA/orchestration contracts.
4. `Idee-app-Archivi-riferimenti` holds the portfolio/research archive; proposals are not approvals.
5. GBrain is *derived, potentially stale context*. It never overrides items 1–4.

Do not update protected governance, create automatic app-repo refresh, add runtime dependencies, widen tool permissions, or auto-merge because a GBrain memory says so. External memory is always untrusted input until checked against sources.

## 1. Pilot scope: only five memory categories

- Explicit architecture decisions, each with project, date, status and citation to current GitHub source.
- Resolved bug patterns and reusable fixes, including validation evidence and limits.
- Cross-app reusable capability references (not code copies), respecting `REUSE-FIRST`.
- Accepted user workflow preferences for the Factory, without importing sensitive personal conversations.
- Superseded or rejected ideas with the newer decision reference, so that old proposals are not resurrected.

Excluded: credentials/tokens/private keys, personal/medical/relationship information, raw conversation history, app data, user uploads, customer data, private documents, unverified build successes, all-code or full-repository ingestion.

Memory record format (logical template; not a hard-coded GBrain schema):
- `entity`: e.g. `appfactory/anna-diary`
- `claim`: one atomic technical fact or decision
- `status`: candidate | approved | superseded | rejected | verified
- `valid_from` and `last_verified_at` (UTC)
- `source_repo`, `source_path`, `source_commit_sha`, optional `pr_or_issue`
- `evidence_level`: proposal | inspected | tests | physical-device
- `supersedes`: older record identifier, if relevant

Do not fabricate fields supported by GBrain: encode metadata in content/provenance where necessary and map through actual live tool schemas.

## 2. Cost and deployment choice

**Pilot preference: self-host, keyless** using local PGLite and keyword retrieval. MIT-licensed GBrain and keyless local storage avoid mandatory model API usage; hosting/computer electricity/network/tunnel arrangements can still cost money.

- For quick local verification, use an Ubuntu/Linux host; on a Windows desktop, WSL2 is a possible lab environment, but service persistence, systemd and Tailscale Funnel require separate verification. Never assume WSL2 remains available when Windows sleeps.
- ChatGPT cloud access needs a reachable **HTTPS MCP** endpoint (or a supported Secure MCP Tunnel). GBrain's documented default for self-hosted cloud clients is Tailscale **Funnel**, not tailnet-only Serve. Funnel publicly exposes an authenticated endpoint: review access boundaries and grants before enabling.
- For 24/7 use a managed always-on host or paid hosting later, only after a distinct cost/security decision.
- GBrain hosted service is optional and paid; do not provision it without separate approval.

Official implementation references:
- https://github.com/garrytan/gbrain/blob/master/docs/mcp/CHATGPT.md
- https://github.com/garrytan/gbrain/blob/master/docs/mcp/DEPLOY.md
- https://github.com/garrytan/gbrain/blob/master/docs/mcp/ADMIN.md
- https://github.com/garrytan/gbrain/blob/master/docs/guides/remote-mcp.md
- https://developers.openai.com/plugins/deploy/connect-chatgpt
- https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt

## 3. Operator-run setup — no secrets in GitHub or ChatGPT messages

Prerequisites: supported Linux/macOS host, Bun >=1.4.4, a real GBrain CLI from the upstream GitHub repository, private GBrain home directory, an HTTPS/tunnel choice. This is not a command that the chat assistant can execute on the user's PC.

```bash
# Bun must already be available at version >= 1.4.4.
# GBrain is NOT the unrelated npm "gbrain" package.
bun install -g github:garrytan/gbrain#latest-stable
gbrain init --pglite --no-embedding
gbrain doctor

# Local keyless smoke test; disposable, non-sensitive test fact only:
gbrain remember "App Factory pilot memory roundtrip" --provenance "gbrain-pilot-test-2026-11-02"
gbrain recall --query "App Factory pilot memory roundtrip"

# Preview BEFORE agreeing to install a service / expose HTTPS:
gbrain mcp expose --dry-run
# After reviewing security and the plan, on the brain host:
gbrain mcp expose --funnel
gbrain mcp expose --status
```

Never paste or commit `~/.gbrain/serve/admin-token`, OAuth credentials, consent links, access tokens, full request logs or private server config. Do not use `--yes` unattended for initial exposure. Confirm the server URL reported by GBrain ends with `/mcp`, and that no unrelated service is exposed.

## 4. Register ChatGPT with read-only access first

**First check the current ChatGPT account UI**: Plugins > + > Add custom MCP server. Account/workspace permissions may restrict creation. The current Plugins experience does not require the old explicit Developer Mode switch. Copy the **exact OAuth redirect URI** shown by ChatGPT; never guess a callback.

On the GBrain host, with owner-only credentials in a protected file:

```bash
gbrain mcp admin register appfactory-chatgpt-pilot \
  --redirect-uri 'EXACT_REDIRECT_URI_FROM_CHATGPT' \
  --token-endpoint-auth-method none --source default \
  --url https://YOUR-ACTUAL-HOST/mcp \
  --admin-token-file /absolute/private/admin-token --dry-run --json

# Review scopes, source grants and operations: default without --profile/--scopes is read-only.
# Repeat the same command WITHOUT --dry-run to register.
gbrain mcp admin setup CLIENT_ID --harness chatgpt --flow authorization-code \
  --url https://YOUR-ACTUAL-HOST/mcp \
  --admin-token-file /absolute/private/admin-token --json
```

Use the real setup output and enter the MCP URL and OAuth client metadata in ChatGPT Plugins. Review the risk warning, begin linking, sign in to GBrain owner dashboard and explicitly approve the pending OAuth request. If the owner session needs a login link, follow ADMIN.md privately and preserve the `oauth_request` ID. Do not hand the owner token to the ChatGPT client. If ChatGPT requests a registration method not supported by this GBrain release, stop rather than improvising.

**Only after the read-only pilot passes**, propose a deliberate change to `read write`, restricted to the intended source, with user-approved memory-writing semantics. Do not request OAuth `admin`.

## 5. Acceptance tests, to be executed from real ChatGPT Chat

Each gate remains **NOT VERIFIED** until observed, with timestamp and evidence. On 2026-11-02, gate 1 (custom MCP UI), 2 (Chat-native tool call), and 3 (read-only recall of fact #1 with provenance) were observed as PASS. Gates 4–8 remain NOT VERIFIED.

1. Plugin creation available to the actual user account. If unavailable, mark **BLOCKED: PLAN/ACCOUNT GATE** and keep this candidate documentation only.
2. Authenticated MCP call from a fresh ChatGPT **Chat** conversation using `@GBrain` or selection supported by that UI; if supported only in Work, mark **BLOCKED: CHAT-ONLY REQUIREMENT**.
3. A read-only `recall` of the disposable test fact succeeds with correct provenance.
4. Unpermitted write is denied in read-only pilot; private/excluded source cannot be read.
5. GBrain cannot modify GitHub and cannot perform `localOnly` file operations via HTTP; test denied access safely.
6. A deliberately stale test fact does not override the live `App-Factory-Core/CURRENT.yaml` version or any app's current Roadmap.
7. Disconnect/reconnect works; a new session can retrieve the known test, without leakage into unrelated domains.
8. Review actual cost, response latency, memory freshness and error/timeout behavior. Remove/forget the disposable test fact when complete.

Record evidence in a *separate* dated pilot report/PR before any go-live or read/write promotion.

## 6. Future conditional integration — not enabled by this PR

A. Keep memory writes **event-driven and explicit**: approved decision, merged PR, verified resolution, or formally superseded decision. Never convert every chat message into a memory.

B. For citations, store exact repository path + commit SHA. On `recall`, re-read `CURRENT.yaml` and relevant target repo, and label discrepancies **STALE**.

C. The existing daily capability archive updater and weekly Factory report remain their current independent workflows. No duplicate scheduler or new paid API usage. GBrain indexing is not an excuse to broaden automation permissions.

D. Evaluate usefulness after 20 real retrieval questions: correct provenance, stale recall rate, search recall, manual correction burden, monthly cost, and availability. If no measurable benefit relative to GitHub + native ChatGPT memory, close the pilot and do not deploy.

## 7. Rollback

- In ChatGPT, disconnect/uninstall only the new GBrain plugin.
- Revoke the OAuth client/token from GBrain admin dashboard.
- If self-hosted, follow the upstream `gbrain mcp expose` cleanup guide; do not delete the local brain without explicit backup/approval.
- Leave original GitHub and ChatGPT memory unchanged; no backfill or destructive migration is part of this pilot.
