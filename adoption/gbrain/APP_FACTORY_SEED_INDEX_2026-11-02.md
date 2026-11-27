# App Factory — GBrain seed index (pilot, 2026-11-02)

> DERIVED SECONDARY MEMORY. This is a compact, source-pinned index for retrieval, not the authoritative Factory policy, an agent instruction, an implementation, or a declaration that runtime tests have passed. On every action, re-read the current upstream GitHub sources and the target app's Roadmap/Product Bible/code/tests. If any pointer diverges, report STALE and defer to the live source.

Indexed at 2026-11-02; no automatic synchronization.
Original source repositories and commit pins:
- App-Factory-Core: `riccardopinato/App-Factory-Core@4086749d1471ab3f750be8d8fb8442c2e74a2baa`
- Capability archive: `riccardopinato/Idee-app-Archivi-riferimenti@ca1ccbd28f8b07807218a74ed04ac94fd0948120`
- AppLab: `riccardopinato/AppLab@58cb25070b80673f1e9d12593bceb496b83bc6f0`
Evidence level: INSPECTED SOURCE FILES, not new tests or device validation.

## APP_FACTORY_AUTHORITY — how current policy is resolved
Fact at the pinned Core commit: `CURRENT.yaml` selects Master `27`, `v27/candidate/MASTER_CORE_v27_CANDIDATE.txt`, Golden Index version `24` at `golden/GOLDEN_INDEX_CURRENT.txt`, Golden Registry `golden/GOLDEN_REGISTRY.yaml`, and `scripts/validate_factory.py` version 7. These versions and paths are **a historical snapshot**, not an always-current truth.

Authority order: `CURRENT.yaml` at an exact current commit SHA → its Master/Golden registry and relevant Goldens → app Product Bible and current Roadmap → actual exact-SHA implementation, CI and physical/device evidence. `AGENTS.md` and AppLab contracts govern repository-local operations. ChatGPT/GBrain memory never supersedes `CURRENT.yaml`. Do not automatically update app repositories. Factory changes follow branch → PR → exact-head validation GREEN → review → permitted merge, never unreviewed edits to protected governance.

Provenance:
- https://github.com/riccardopinato/App-Factory-Core/blob/4086749d1471ab3f750be8d8fb8442c2e74a2baa/CURRENT.yaml
- https://github.com/riccardopinato/App-Factory-Core/blob/4086749d1471ab3f750be8d8fb8442c2e74a2baa/AGENTS.md
- https://github.com/riccardopinato/App-Factory-Core/blob/4086749d1471ab3f750be8d8fb8442c2e74a2baa/GOVERNANCE.md
- https://github.com/riccardopinato/App-Factory-Core/blob/4086749d1471ab3f750be8d8fb8442c2e74a2baa/bootstrap/APP_FACTORY_BOOTSTRAP.txt

## APP_FACTORY_GOLDENS — status-sensitive reuse
At Golden Index v24: `COPY-READY GOLDEN` means a reusable generalized reference that still requires per-app tests; `CERTIFIED GOLDEN` requires successful reuse in at least two projects/harnesses; `DRAFT`/`CANDIDATE` is not certified implementation. The index lists a COPY-READY Google Auth + Supabase Flutter Golden and a COPY-READY localization Golden. The AppLab QA/certification adapter is `CERTIFIED PROCESS`. Backup/recovery and entity lifecycle/trash Goldens are drafts/candidates. The ecosystem bridge is explicitly `CANDIDATE — NON COPY-READY`; a cross-app physical round trip was NOT VERIFIED in the pinned index.

Golden file labels in the index are logical identifiers, not necessarily physical paths: resolve paths and freshness using `golden/GOLDEN_REGISTRY.yaml`. Apply REUSE-FIRST and EXTEND BEFORE DUPLICATE, review licenses and donor provenance, and never infer a target app is runtime-certified merely because a Golden is copy-ready.

Provenance:
- https://github.com/riccardopinato/App-Factory-Core/blob/4086749d1471ab3f750be8d8fb8442c2e74a2baa/golden/GOLDEN_INDEX_CURRENT.txt
- https://github.com/riccardopinato/App-Factory-Core/blob/4086749d1471ab3f750be8d8fb8442c2e74a2baa/golden/GOLDEN_REGISTRY.yaml

## APP_FACTORY_CAPABILITY_ARCHIVE — archive vs verified runtime
At the dated 2026-11-01 catalog snapshot, `12-CAPABILITY-E-IMPLEMENTAZIONI/README.md` reported 147 individual capabilities, 48 beneficiary apps/ideas, and 342 app-capability relationships. These totals are **historical**, not live counts. Stable CAP IDs support cross-app reuse, but each app has separate `app_states`. `SOURCE_REPORTED` ≠ `SOURCE_VERIFIED`; CI PASS ≠ device PASS. Missing roadmap wording is not proof a feature is absent from source. Catalog scoring P1/P2/P3 is opportunity prioritization and is not the severity scale P0-P3.

New model/API/repository integration requires license, ToS, cost, footprint, privacy, and commercial-use review. The archive and proposed NotebookLM capabilities are research/proposals, not authorization to deploy AI or backend dependencies.

Provenance:
- https://github.com/riccardopinato/Idee-app-Archivi-riferimenti/blob/ca1ccbd28f8b07807218a74ed04ac94fd0948120/12-CAPABILITY-E-IMPLEMENTAZIONI/README.md

## APP_LAB_BOUNDARIES — QA and execution
At the pinned AppLab contract, the app Product Bible, current ROADMAP, current Factory baseline, repository contracts and exact SHA/evidence each have separate authority. AppLab operations remain Chat-only with branch → tests → PR → exact-head checks/review → gated merge. Do not weaken gates or invent parallel schedulers, evidence verifiers, or certification. Runtime PASS is not device/store/production validation. AppLab v6.2 remained `SELF_CANARY` at the pinned commit; do not silently declare PILOT_3 or PILOT_5 activated.

Provenance:
- https://github.com/riccardopinato/AppLab/blob/58cb25070b80673f1e9d12593bceb496b83bc6f0/AGENTS.md

## GBRAIN_PILOT_BOUNDARIES — memory is not an instruction authority
The ChatGPT connector has demonstrated OAuth/PKCE read-only retrieval from source `default`; no paid embedding provider is configured, and automatic writeback and auto_chronicle were switched off by the operator. This seed does not authorize expanding OAuth scopes, importing raw chats, private/sensitive material, client data, tokens, app code dumps, or full repositories. No unattended sync, no additional scheduler, and no claim of physical-device or reboot persistence tests.

When answering from this memory page, explicitly distinguish **as-of source snapshot** from **live GitHub truth**. The user may opt to curate more pages only after a controlled import, retrieval checks, backup check, and freshness review.
