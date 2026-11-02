#!/usr/bin/env bash
# GBrain / App Factory: manual encrypted backup export + isolated restore rehearsal.
# Requires: age, tar, sha256sum, systemctl, gbrain, Bash; run in the GBrain owner's Ubuntu WSL.
# No secrets are sent to GitHub/ChatGPT. The encrypted destination must be chosen by the operator.
set -Eeuo pipefail
umask 077

SERVICE="gbrain-serve.service"
LOCAL_ROOT="$HOME/gbrain-private-backups"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BUNDLE_NAME="gbrain-appfactory-postimport-${STAMP}.tar.gz.age"
WORK=""
SERVICE_MAY_BE_STOPPED=0

cleanup() {
  rc=$?
  trap - EXIT
  if (( SERVICE_MAY_BE_STOPPED )); then
    echo "Restoring existing GBrain user service..."
    if ! systemctl --user start "$SERVICE"; then
      echo "ERROR: GBrain service restart failed. Inspect systemctl --user status $SERVICE" >&2
      rc=1
    fi
  fi
  if [[ -n "$WORK" && -d "$WORK" ]]; then rm -rf -- "$WORK"; fi
  exit "$rc"
}
trap cleanup EXIT

for dep in gbrain systemctl tar sha256sum age mktemp curl find; do
  if ! command -v "$dep" >/dev/null 2>&1; then
    if [[ "$dep" == "age" ]]; then
      echo "Install age in Ubuntu first: sudo apt update && sudo apt install age" >&2
    else
      echo "Missing command: $dep" >&2
    fi
    exit 1
  fi
done
[[ "$(uname -s)" == Linux ]] || { echo "Run in Ubuntu WSL." >&2; exit 1; }
systemctl --user is-active --quiet "$SERVICE" || {
  echo "GBrain service not active; inspect before operating on PGLite." >&2; exit 1;
}
mkdir -p -- "$LOCAL_ROOT"
chmod 700 "$LOCAL_ROOT"
echo "Choose an existing writable folder on a REMOVABLE drive or an explicitly synchronized cloud folder."
echo "Examples (only if YOUR machine uses them): /mnt/e/GBrainBackup or /mnt/c/Users/<windows-user>/OneDrive/GBrainBackup"
echo "WARNING: a folder on the same PC does not provide an independently verified off-PC backup."
read -r -p "Encrypted destination directory: " DEST
[[ -n "$DEST" && -d "$DEST" && -w "$DEST" ]] || { echo "Destination must exist and be writable." >&2; exit 1; }
DEST="$(realpath -- "$DEST")"
case "$DEST" in
  "$HOME/.gbrain"|"$HOME/.gbrain"/*|"$LOCAL_ROOT"|"$LOCAL_ROOT"/*)
    echo "Refusing destination in the live brain or local plaintext backup directory." >&2; exit 1 ;;
esac
ENCRYPTED="$DEST/$BUNDLE_NAME"
[[ ! -e "$ENCRYPTED" && ! -e "$ENCRYPTED.sha256" ]] || { echo "Refusing overwrite of existing backup." >&2; exit 1; }
WORK="$(mktemp -d "$LOCAL_ROOT/.export-rehearsal-XXXXXX")"
chmod 700 "$WORK"
mkdir -p -- "$WORK/bundle/canonical-content" "$WORK/restore-parent"
ARCHIVE="$WORK/bundle/brain.gbrain-backup"
echo
echo "Operation: brief service pause -> fresh post-import PGLite archive + canonical content copy ->"
echo "service restart -> passphrase encryption to destination -> decrypt/readback -> NEW isolated restore -> recall test."
echo "No OAuth changes, no paid models, no background jobs, no changes to live GitHub files."
read -r -p "Type ESEGUI to start: " CONFIRM
[[ "$CONFIRM" == ESEGUI ]] || { echo "Cancelled."; exit 0; }

echo "Stopping the existing GBrain service for a consistent snapshot..."
SERVICE_MAY_BE_STOPPED=1
systemctl --user stop "$SERVICE"
gbrain backup create --output "$ARCHIVE"
if [[ -d "$HOME/.gbrain/content" ]]; then
  cp -a -- "$HOME/.gbrain/content/." "$WORK/bundle/canonical-content/"
fi
echo "Restarting existing GBrain service before encryption..."
systemctl --user start "$SERVICE"
SERVICE_MAY_BE_STOPPED=0
systemctl --user is-active --quiet "$SERVICE" || { echo "GBrain failed to restart." >&2; exit 1; }
HEALTH_OK=0
for _attempt in 1 2 3 4 5; do
  if curl --fail --silent "http://127.0.0.1:3131/health" >/dev/null; then HEALTH_OK=1; break; fi
  sleep 1
done
(( HEALTH_OK )) || { echo "GBrain restarted but health is not yet available; check status." >&2; exit 1; }
echo
echo "Encrypting the backup with age passphrase mode. Choose a LONG unique passphrase."
echo "Do not paste the passphrase in ChatGPT or put it in a script. Losing it makes recovery impossible."
tar -czf - -C "$WORK/bundle" brain.gbrain-backup canonical-content | age -p -o "$ENCRYPTED"
chmod 600 -- "$ENCRYPTED" || true
(
  cd -- "$DEST"
  sha256sum -- "$BUNDLE_NAME" > "$BUNDLE_NAME.sha256"
  sha256sum --check --status "$BUNDLE_NAME.sha256"
)
echo "Encrypted archive and local ciphertext hash created; verifying actual decryption and restore..."
age -d -o "$WORK/bundle-decrypted.tar.gz" "$ENCRYPTED"
# Extract only the one, specifically named native GBrain archive. Canonical source
# files are retained inside the encrypted bundle but are not written into scratch.
# This prevents path traversal or symlink extraction from any other tar members.
tar -tzf "$WORK/bundle-decrypted.tar.gz" > "$WORK/bundle-file-list.txt"
grep -Fxq "brain.gbrain-backup" "$WORK/bundle-file-list.txt" || {
  echo "Bundle lacks the expected native GBrain archive." >&2; exit 1;
}
grep -Eq '^canonical-content(/|$)' "$WORK/bundle-file-list.txt" || {
  echo "Bundle lacks the separately captured canonical content root." >&2; exit 1;
}
mkdir -p -- "$WORK/unpacked"
tar -xzf "$WORK/bundle-decrypted.tar.gz" -C "$WORK/unpacked" --no-same-owner --no-same-permissions -- brain.gbrain-backup
[[ -s "$WORK/unpacked/brain.gbrain-backup" ]] || { echo "Missing restored archive." >&2; exit 1; }

RESTORED="$WORK/restore-parent/restored-brain"
[[ ! -e "$RESTORED" ]] || { echo "Unsafe restore target already exists." >&2; exit 1; }
echo "Restoring from ciphertext into an ABSENT, isolated new-brain root (never over the live brain)..."
gbrain backup restore "$WORK/unpacked/brain.gbrain-backup" --into "$RESTORED" --mode new-brain --json > "$WORK/restore-report.json"
[[ -f "$RESTORED/restore-receipt.json" ]] || { echo "Restore did not create a receipt." >&2; exit 1; }
echo "Testing keyword recall inside the restored brain, not the live service..."
GBRAIN_HOME="$RESTORED" gbrain recall --query "APP_FACTORY_AUTHORITY" --source default --json > "$WORK/recall.txt"
grep -q "app_factory_seed_index_2026-11-02" "$WORK/recall.txt" || {
  echo "Restored brain is missing the App Factory seed search result; test NOT VERIFIED." >&2; exit 1;
}
GBRAIN_HOME="$RESTORED" gbrain recall --query "App Factory test memoria persistente" --json > "$WORK/recall-fact.txt"
grep -q "App Factory test memoria persistente" "$WORK/recall-fact.txt" || {
  echo "Restored brain is missing the original test fact; test NOT VERIFIED." >&2; exit 1;
}
echo
echo "PASS: encrypted backup decrypted, independent new-brain restore completed, seed and test fact readable."
echo "PASS: original GBrain service was restarted and answered local HTTP health."
echo "Encrypted file: $ENCRYPTED"
echo "Ciphertext checksum: $ENCRYPTED.sha256"
echo "CAUTION: remote/cloud replication has NOT been verified; check destination sync/eject independently."
echo "CAUTION: the passphrase is required for recovery. No plaintext copy is uploaded by this script."
