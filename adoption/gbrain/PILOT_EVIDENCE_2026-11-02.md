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

1. **PASS (user-reported shutdown flow + observed post-restart readback):** after the earlier instructed WSL shutdown/restart sequence, the user shared `gbrain mcp expose --status` showing systemd active, Tailscale Funnel published, local and HTTPS tailnet health `ok`. A separate real Chat MCP `recall` immediately afterward returned the previously imported seed page and the install-check fact. The Chat assistant cannot independently verify that `wsl --shutdown` actually executed; Windows sleep/reboot recovery remains NOT VERIFIED.
2. **NOT VERIFIED:** Restore rehearsal in an isolated root and validated content/root inventory. Do not restore over the live brain.
3. **NOT VERIFIED:** Encrypted off-host backup and documented retention/recovery controls. The local archive alone is a single-host copy.
4. **NOT VERIFIED:** Negative authorization tests for read-only client and private source; current `read` grant was verified at registration and successful read, but denials were not safely exercised.
5. **NOT VERIFIED:** 20-query usefulness/freshness trial, corrections, revoked-access test, and readiness to merge this PR.

## Post-restart test (user output plus real Chat connector read, 2026-11-02)

The operator returned from the WSL restart test with `gbrain mcp expose --status` reporting all five checks `ok` (receipt, Funnel mapping, user service, local health, tailnet HTTPS health). In the same Chat, `mcp__GBrain__recall` returned imported `app_factory_seed_index_2026-11-02` and retained test fact #1 from the read-only source `default`. **Observed readback PASS, persistent data PASS, connectivity PASS.** Actual `wsl --shutdown` execution is asserted by the surrounding user workflow, not verified from an independent shell transcript. This is not a Windows OS reboot or sleep/resume reliability result.

No MCP write permission was granted, no automatic memory writeback enabled, and no GitHub code/CI governance modified by the memory import.

## First encrypted backup attempt (2026-11-03, reported by operator)

- Operator used external-mounted Windows SSD folder at `/mnt/d/GBrainBackup` and explicitly confirmed the backup rehearsal.
- New native local GBrain archive reported created; GBrain user service restarted before encryption.
- `age -p` then reported `passphrases didn't match`. The `tar` writer reported broken pipe/exit 141 after the reader exited. **No successful encrypted backup was proven, no isolated restore was executed, and off-host backup status remains NOT VERIFIED.**
- Improved the rehearsal script to explain automatic passphrase generation and remove only its own incomplete ciphertext on nonzero encryption exit. Operator must re-download reviewed pinned revision; first downloaded script is unchanged on their machine.
- No passphrase/credentials are included in this evidence record.

## Encrypted backup and isolated restore: PASS (2026-11-03, operator output)

The operator subsequently reran the fixed, commit-pinned manual backup rehearsal script and shared its final, nonsecret terminal output:

```text
PASS: encrypted backup decrypted, independent new-brain restore completed, seed and test fact readable.
PASS: original GBrain service was restarted and answered local HTTP health.
Encrypted file: /mnt/d/GBrainBackup/gbrain-appfactory-postimport-20261103T001238Z.tar.gz.age
Ciphertext checksum: /mnt/d/GBrainBackup/gbrain-appfactory-postimport-20261103T001238Z.tar.gz.age.sha256
CAUTION: remote/cloud replication has NOT been verified; check destination sync/eject independently.
CAUTION: the passphrase is required for recovery. No plaintext copy is uploaded by this script.
```

**Supported acceptance:**
- PASS (operator-run script): a fresh native PGLite archive was encrypted with age and written to the selected SSD-backed Windows D: mount.
- PASS (operator-run script): encrypted file was read back and successfully decrypted; ciphertext checksum generation/check were required by the script.
- PASS (operator-run script): independent `gbrain backup restore --mode new-brain` to a new temporary root, isolated from the live database; CLI recall found the imported App Factory seed and installation test fact.
- PASS (operator-run script): original systemd user service restarted and local HTTP health responded.
- PASS (separate assistant action): GBrain Chat-only read-only MCP `recall` after this report again returned `app_factory_seed_index_2026-11-02` and fact #1 from source `default`.

**Still NOT VERIFIED:** whether Windows D: is a physically separate *detachable* SSD rather than an internal SSD or logical partition; media unplug/eject and separate physical retention; copies outside this PC or independently completed cloud replication; operating-system full shutdown/sleep-resume reliability; read-only negative authorization; 20-query usefulness/freshness review. The script did not itself test whole native harness reinstallation, OAuth token reconnection, or loss of the live machine. No passphrase or key material was shared or committed. Earlier sections describe historical interim states (first failed encryption attempt) and should not be interpreted as current final state.

## Operational memory v1 prepared for import (interim state, 2026-11-03)

Eight small, source-pinned, operator-curated project/governance Markdown pages now live in `adoption/gbrain/operational-seed-2026-11-03/`, the contents pinned to commit `32f51cc184e991e93885e73692d9f944cc5bc551`. Coverage: live Factory resolver Golden v27 (prior GBrain Golden v24 now explicitly historical), Anna's Diary, TrailPath, Notes, CamperBoss, AppLab, capability catalog and Cooking Anime. The last was reconciled to the live PR states (#41 merged, #44 draft) rather than the old roadmap's snapshot.

An explicit manual WSL script `adoption/gbrain/import_operational_seed_wsl.sh` was added, with preflight/download, GitHub commit pin, interactive `IMPORTA_8`, PGLite service quiescence and backup, separate canonical-content snapshot, `--no-embed` local import, restart/health check and one-shot marker. Full instructions: `adoption/gbrain/OPERATIONAL_MEMORY_RUNBOOK_2026-11-03.md`.

**At this preparation stage (now superseded by the readback below):** these eight pages had not yet been imported into the operator's GBrain database; no new Chat MCP readback then proved they could be found; no post-import external encrypted backup existed. Chat's grant remains read-only, with no unattended data ingestion or paid embedding provider. The earlier encrypted SSD backup and isolated restore success remain valid for the older brain snapshot, not yet this new content.

## Operational memory v1: all eight MCP readbacks PASS (2026-11-03)

Operator pasted `gbrain mcp expose --status` after the eight-page import sequence: receipt/Funnel/service/local /health/tailnet HTTPS all reported `ok`. This status-only output does not independently attest that the local import command was run.

**Independent direct ChatGPT connector proof**: eight distinct `mcp__GBrain__recall({query: GBRAIN_OP_*_2026_11_03, source_id:"default", limit:5, return_unit:"page"})` calls from this Chat returned exact page-title matches, every one with `source_id:"default"`, `origin:"managed_file_import"`, and `evidence:"keyword_exact"`:

| Query topic | Returned GBrain slug | Result |
| --- | --- | --- |
| Factory authority | `00_factory_resolver` | PASS |
| Anna's Diary | `10_annas_diary` | PASS |
| TrailPath | `20_trailpath` | PASS |
| Notes Ecosistema | `30_notes_ecosistema` | PASS |
| CamperBoss | `40_camperboss` | PASS |
| AppLab boundaries | `50_app_lab_gates` | PASS |
| Capability archive | `60_capability_reuse` | PASS |
| Cooking Anime | `70_cooking_anime` | PASS |

The Factory page explicitly records **Golden Index v27 as-of 2026-11-03** and **Golden v24 in the prior seed as historical**. The initial test fact #1 also remains returned in the connector response. Keyword-only search is still intentional (`search_degraded: keyword_only_embedding_disabled`), not a missing import. No credential, raw chat, user data or paid embedding provider was imported by the assistant.

**Still PENDING after 8/8 readback:** a *new* `age` encrypted SSD export with isolated restore **of the newly imported eight pages**, verification that D: is physically separate/detachable, optional Windows sleep/reboot durability, negative scope tests, 20-query usefulness/freshness audit, and PR review/merge gates. The earlier external SSD encrypted backup predates operational v1 and should be retained until refreshed successfully. Local backup existence for this specific run was not independently audited beyond the operator's status and GBrain readback.
