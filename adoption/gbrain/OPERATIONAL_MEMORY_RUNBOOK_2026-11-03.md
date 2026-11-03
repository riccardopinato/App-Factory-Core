# GBrain App Factory — operational memory expansion (2026-11-03)

**Status (2026-11-03):** eight curated GitHub seed pages committed; all **8/8 authenticated read-only Chat MCP readbacks PASS** after operator's local import. The original import instructions below remain useful for fresh installations, not evidence of unfinished import. GitHub is always authoritative; GBrain is an explicitly sourced, *secondary*, as-of index.

## Sources and evidence

The eight memory files are at [`adoption/gbrain/operational-seed-2026-11-03/`](operational-seed-2026-11-03/), pinned by the import script to exact content commit `32f51cc184e991e93885e73692d9f944cc5bc551`.

| Memory | Source repo @ inspected main SHA | Scope and explicit limitations |
| --- | --- | --- |
| `00_FACTORY_RESOLVER.md` | App-Factory-Core@2d58d23b1f8e0cabe5efe44b83b63ff56ddeb67f | Current Master 27, Golden Index **27**, Registry 2, Validator 7; old GBrain Golden 24 is historical |
| `10_ANNAS_DIARY.md` | Agenda-per-Anna@cb477cbecc85c1b1c415c60fd69bbd128fb82904 | Signed +120, general attestation, subsequent source-only quick wins, incomplete device/visual evidence |
| `20_TRAILPATH.md` | TrailPath@3f44ab37c0881e4315033797c451cec723e23cd2 | Flutter v0.9.15 RC, routing failure transparency, offline/release QA limits |
| `30_NOTES_ECOSISTEMA.md` | Notes-Ecosistema@3fd9b0df5ab3b7470c65721b4bad7f3fd8c59e6c | Flutter 0.56.3, optional local Needle pack, no device-certified Needle QA |
| `40_CAMPERBOSS.md` | CamperBoss@cf4202e25bf3bc630f9cfe5e3823219acfba84b4 | Step16/16Q BLOCKED, Step17 local AI deferred, provider trust boundaries |
| `50_APP_LAB_GATES.md` | AppLab@58cb25070b80673f1e9d12593bceb496b83bc6f0 | Chat-only source gates, SELF_CANARY, bounded worker contract |
| `60_CAPABILITY_REUSE.md` | Idee-app-Archivi-riferimenti@07a7dc4dabc73082e803f52a9bc697ca5229f9b8 | Stable CAP IDs, as-of-2026-11-01 counts, SOURCE_REPORTED vs SOURCE_VERIFIED |
| `70_COOKING_ANIME.md` | In-Cucina-con-gli-Anime@478f6db6d6cdcfe9adcbddacfe834cb7fbc345e7 | Editorial/release QA, #41 MERGED / #44 DRAFT checked separately on 2026-11-03 |

**Excluded:** chats/transcripts, photographs, identities, personal diaries, private documents, addresses, credentials, secrets, GitHub source code dumps, medical/relationship data and complete app databases. No raw repository clone is imported, only eight short technical summaries and immutable source links. Do not infer that any included repo was rebuilt or tested physically during curation. Per-app approval/status in dated documents may diverge from current CI; check live repository before any action.

## Operator import on Ubuntu WSL (one time)

1. Ensure the original GBrain user service is running, and save existing encrypted backup and passphrase.
2. Download exactly the reviewed commit-pinned import script:

```bash
curl -fLsS --proto '=https' --tlsv1.2 \
 'https://raw.githubusercontent.com/riccardopinato/App-Factory-Core/d3faa0a2112e98c995c34b0a1e9522d51a55240d/adoption/gbrain/import_operational_seed_wsl.sh' \
 -o "$HOME/gbrain-import-operational.sh"
bash -n "$HOME/gbrain-import-operational.sh" &&
bash "$HOME/gbrain-import-operational.sh"
```

3. Review the eight source pages and then enter `IMPORTA_8` in the terminal when asked. Script downloads only those pinned Markdown files, stops the local systemd service for exclusive PGLite access, creates a new **local private plaintext** native backup and a separately retained canonical-content snapshot, imports with `--no-embed`, restarts the user service and checks local health. A local marker prevents normal accidental second import. No MCP grant changes.
4. Run `gbrain mcp expose --status`; return **only nonsecret output** to ChatGPT to check real `mcp__GBrain__recall` for factory, project and governance pages.
5. **Refresh the encrypted SSD backup** using the previously validated `backup_encrypt_restore_rehearsal_wsl.sh`, because the older encrypted `.age` file predates these eight new pages. Safely retain the previous backup until the new one passes isolated restore, then review backup retention.
6. Do not keep uncontrolled copies of the new local plaintext native archive or its separately copied content. Both can contain sensitive database material. After an independently validated encrypted copy, review retention of local plaintext backup under the owner's backup policy. Never put plaintext backup or passphrase in GitHub or ChatGPT.

## Acceptance matrix

- **PASS:** GitHub seed curation with exact source pins and explicit evidence labels.
- **PASS:** Local GBrain and remote MCP read-only operation prior to this phase, prior encrypted SSD backup/restoration drill.
- **PASS (real Chat MCP):** eight exact named pages recalled from the `default` source with `origin=managed_file_import`; updated Factory v27 resolves the old Golden v24 as historical. Operator status output independently shows MCP service/tailnet healthy.
- **PENDING:** post-import encrypted SSD backup and isolated restore retest; detachable/off-host storage proof; additional negative authorization and usefulness/freshness tests. Local import output itself was not supplied, but real MCP content is present.
- **NOT REQUESTED:** GitHub auto-sync, GBrain remote writes, schedule/cron, paid embedding models, unrestricted chat ingestion, automatic app mutation or release.

Suggested read-only retrieval tests (after import):
- `GBRAIN_OP_FACTORY_RESOLVER_2026_11_03` → Golden Index 27, old 24 marked historical.
- `GBRAIN_OP_ANNA_DIARY_2026_11_03` → +120 general acceptance ≠ per-scenario device certification.
- `GBRAIN_OP_NOTES_ECOSISTEMA_2026_11_03` → Needle AI model pack optional, hardware QA pending.
- `GBRAIN_OP_CAMPERBOSS_2026_11_03` → 16Q BLOCKED.
- `GBRAIN_OP_APP_LAB_GATES_2026_11_03` → SELF_CANARY, no implicit pilot promotion.

When changing any project, **re-read live GitHub**. A hit in GBrain is a dated search aid, not proof of current app state.
