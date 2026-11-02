# GBrain — encrypted off-host backup and isolated restore rehearsal

**Status:** candidate procedure. Maintains existing Chat-only, read-only OAuth and local keyless GBrain configuration. The script is *manual* and is **not** a daemon or recurring task. Never paste a passphrase, admin token or archive contents into ChatGPT or a GitHub PR.

## What this script actually does

`backup_encrypt_restore_rehearsal_wsl.sh`:

1. Checks that the GBrain user service is running and `age` (and standard GNU command-line tools) is installed.
2. Asks for a **pre-existing writable destination directory**. Supply a mounted external USB/removable drive, or an explicitly synchronized cloud-storage folder mounted into WSL. A normal Windows disk directory, even under `/mnt/c`, is **not** evidence of an off-device backup. No cloud sync is performed by this script.
3. Requests explicit `ESEGUI` confirmation. Stops `gbrain-serve.service` to take a consistent new **post-import** PGLite snapshot; copies `~/.gbrain/content` separately because native GBrain archives may omit externally-owned canonical files; restarts the original server as soon as snapshotting finishes. EXIT cleanup attempts service restart even if an earlier step fails.
4. Streams the native archive and canonical content into an `age -p` passphrase-encrypted `.tar.gz.age` file **at the specified destination**. The passphrase is entered in the local terminal, never as a command argument. A SHA-256 checksum of the ciphertext is written alongside the encrypted file. `age` also cryptographically authenticates encrypted content on decryption.
5. Reads the encrypted file back from that destination, decrypts it to an owner-only temporary folder, extracts **only** the native archive member and runs `gbrain backup restore ... --into NEW_ABSENT_ROOT --mode new-brain --json`. This mode creates an isolated, unpublished brain and does **not** reauthorize existing OAuth tokens or reactivate automation.
6. Uses `GBRAIN_HOME=ISOLATED_ROOT` to run two CLI `--json` recall checks against the *restored* database (the App Factory seed and the original installation test fact). Then deletes temporary cleartext and scratch-restore directories. The normal GBrain database is never overwritten or restored over.

### First-time dependency

On Ubuntu WSL, if `age` is missing, install it interactively with:

```bash
sudo apt update
sudo apt install age
```

No dependency is installed by the backup script. `age` is free and runs locally; no embedding/LLM API or subscription is involved.

### Run safely

Download the exact reviewed script from its immutable **commit SHA** (not a moving branch). Confirm it has expected content and execute it:

```bash
curl -fLsS --proto '=https' --tlsv1.2 \
  'https://raw.githubusercontent.com/riccardopinato/App-Factory-Core/REPLACE_WITH_REVIEWED_SCRIPT_COMMIT/adoption/gbrain/backup_encrypt_restore_rehearsal_wsl.sh' \
  -o "$HOME/gbrain-backup-rehearsal.sh"
bash -n "$HOME/gbrain-backup-rehearsal.sh"
bash "$HOME/gbrain-backup-rehearsal.sh"
```

The script is intended for the Ubuntu WSL owner terminal, **not PowerShell**. Before the `ESEGUI` prompt, inspect the script in the linked GitHub PR. Choose a destination you control with enough free storage. If selecting a synced cloud folder, check the provider's own upload/sync confirmation independently; this script does **not** certify cloud completion or remote retention.

### Security and recovery considerations

- `age -p` asks for a long, unique passphrase and may offer to generate a secure one. Record it in a trusted password manager/offline safe. **Loss of the passphrase prevents recovery.** Do not record it in shell history, chat, PRs, environment variables, or files next to the encrypted backup.
- Data is decrypted only in a restricted temporary directory on the Ubuntu/WSL host during the verification; sudden power loss might leave local plaintext temporary files. Clean up abandoned `$HOME/gbrain-private-backups/.export-rehearsal-*` only after independently checking that no verification operation is running.
- The `.age` file contains the sensitive full database and external source content **encrypted**; the `.sha256` is a transport integrity aid and **not** a substitute for decryption/restore verification.
- Checking an encrypted copy from a folder on the same physical disk tests restoreability but **does not** test loss of that disk. A truly off-host copy requires separate transfer/sync confirmation or a removable drive physically detached and retained elsewhere.
- GBrain native backup excludes some runtime packages, local environment secrets, unmanaged credential deliveries and native client setup. A restored brain is intentionally not a drop-in replacement for the original running server: reconstruct runtime and carefully reissue credentials in a separate documented disaster recovery.
- Avoid putting private backups or passphrases in `App-Factory-Core`, `Idee-app-Archivi-riferimenti`, or public issue/PR logs. Only the script, policy and redacted evidence belong in GitHub.

### Acceptance evidence

Until the user shares terminal results, **NOT VERIFIED**: new ciphertext created, readback decryption, isolated restore, post-restore fact/seed retrieval, actual off-device transfer/cloud sync. GitHub CI success validates repository consistency only; it cannot see the user's WSL host.

Do not mark off-host backup as PASS until a physically separate medium, or the actual cloud provider's completed remote-sync evidence, has been checked.
