# Admission audit — REA CLI / Reverse Engineering & Software Intelligence

**2026-11-19 · Factory baseline 5f744d4714c9bacd9b19fdf1b37be4855ed03f09 · Index v30 / Registry v2**

## Decision

**ADMIT `rea_cli_reverse_intelligence` as COPY-READY PROCESS, not CERTIFIED GOLDEN.**
The user requested Golden registration. An important external repository alone
is not sufficient to certify code, providers, runtime, or copied functionality.
The existing bounded AppLab CLI procedure has real repeatable evidence
supporting a written, manually reusable process under Golden governance.

## Evidence evaluated (pinned and independent scopes)

| Evidence | Exact fact | Limit |
|---|---|---|
| External tool | morluto/rea@4491c84c82140a43fa12390b727840a433875ba8, MIT, rea-agents@6.9.0 | The REA package is not automatically copied or installed into apps |
| Adapter | AppLab PR #236 merged main b1acac133d4b44d21e3995aa35e99498ee77f897 | PE imports + certificate operations only |
| CLI runtime | https://github.com/riccardopinato/AppLab/actions/runs/44604806371 PASS | Inert synthetic PE; not a Windows runtime proof |
| Public binary | https://github.com/riccardopinato/AppLab/actions/runs/44615407360 PASS | Exact public Deskland Preview v0.1.3, not historical uploaded installer |
| Payload evidence | Original public installer 28,001,125 bytes, SHA256 e253cad56f1ea0ee2fb9d13ebe8a44f7dbe7232a506ba752cbe54c939c17bf44, 48 files extracted with 43/43 published hashes matching | NSIS static unpack, not execution; other 5 installer stage files have separate status |
| Host evidence | host/bin/Deskland.exe SHA256 5337c513e8c14dc492900d315cd57e287e9dfb4ba750ccf96c2fb668fa4ea530; PE32+ x64, 94,208 bytes; 40 P/Invoke metadata entries, WebView2 references | Static metadata != API execution or Android portability |
| Consumer research | Adaptive-Landscape-Android PR #41 merged f27dc9623f8b06c9258db3a486961c71dfe76e8c | Documentation-only; no Android feature introduced |
| Donor catalog | Idee-app-Archivi-riferimenti PR #173 merged 922ccd15911bbc15260981a34148073e5ed76190 | REI-REA-20261119 remains E1 research, not donor E3 |

## Why this is not E5 / Certified

There is only one proven AppLab CLI/research harness used for a public
Deskland target; a source-only Android report and catalog entry do not count
as independent execution consumers. No second app/harness completed a
separate adoption and evidence chain. The original user-uploaded Windows
installer is unavailable, and physical or dynamic inspection has not been
performed. Static analysis does not prove the decompiled functionality or
license-safe portability. No new transferable Android feature was found.

## Unique scope versus existing Goldens

- OSS Reconnaissance Golden owns external source discovery and licenses.
- Single-Donor Admission Golden owns E1–E5 grading and certification.
- AppLab QA Golden owns trusted app verification.
- This new Golden owns **bounded, on-demand CLI binary research procedure**,
  preserving untrusted evidence and exact artifact/source identity.
- No new workflow or permanent REA service is mandated across apps.

## Gates for next promotion

1. Second **independent** product or investigation harness explicitly
   adopts this copy-ready process using an authorized different artifact.
2. Pin source/binary/engine (including dependency integrity), capture
   success plus negative/partial cases with exact-head CI.
3. Review license, privacy, schema, changes in external tool behavior.
4. Independently demonstrate the findings add actionable insight beyond
   source-only study, without importing forbidden third-party code/assets.
5. Promote only the demonstrated narrower scope to CERTIFIED PROCESS
   or stronger E5 with a separate authorized admission decision.

**No automatic runtime claim, app integration, donor E3 or Golden E5.**
