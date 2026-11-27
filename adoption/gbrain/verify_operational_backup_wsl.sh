#!/usr/bin/env bash
# Manually verify eight App Factory pages INSIDE an existing age-encrypted GBrain backup.
# No writes to live ~/.gbrain, no service restart, no GitHub changes, no model API.
set -Eeuo pipefail
umask 077

ARCHIVE="${1:-}"
[[ -n "$ARCHIVE" && -f "$ARCHIVE" && "$ARCHIVE" == *.tar.gz.age ]] || {
  echo "Usage: bash verify_operational_backup_wsl.sh /mnt/d/GBrainBackup/<filename>.tar.gz.age" >&2
  exit 2
}
ARCHIVE="$(realpath -- "$ARCHIVE")"
for dep in age gbrain tar python3 sha256sum mktemp; do
  command -v "$dep" >/dev/null 2>&1 || { echo "Missing required command: $dep" >&2; exit 1; }
done
if [[ -e "$ARCHIVE.sha256" ]]; then
  echo "Checking existing ciphertext checksum..."
  ( cd -- "$(dirname -- "$ARCHIVE")" && sha256sum --check --status -- "$(basename -- "$ARCHIVE").sha256" ) || {
    echo "FAIL: encrypted archive SHA-256 mismatch; do not decrypt this file." >&2; exit 1;
  }
else
  echo "CAUTION: no SHA-256 sidecar present. Age authentication still protects against tampering."
fi

echo "Source archive: $ARCHIVE"
echo "This test decrypts the archive LOCALLY, restores into a NEW temporary brain,"
echo "checks eight exact memory-page slugs, then deletes the temporary plaintext."
echo "The live GBrain service and database are not changed."
read -r -p "Type VERIFICA_8 to proceed: " CONFIRM
[[ "$CONFIRM" == VERIFICA_8 ]] || { echo "Cancelled."; exit 0; }

PRIVATE="$HOME/gbrain-private-backups"
mkdir -p -- "$PRIVATE"
chmod 700 -- "$PRIVATE"
TMP="$(mktemp -d "$PRIVATE/.verify-operational-backup-XXXXXX")"
cleanup() {
  rc=$?
  trap - EXIT
  [[ -z "${TMP:-}" || ! -d "$TMP" ]] || rm -rf -- "$TMP"
  exit "$rc"
}
trap cleanup EXIT

echo "Decrypting archived ciphertext (enter your secret passphrase only at age's prompt)..."
age -d -o "$TMP/decrypted.tar.gz" "$ARCHIVE"
echo "Extracting ONLY the named native GBrain archive member..."
tar -xOzf "$TMP/decrypted.tar.gz" brain.gbrain-backup > "$TMP/brain.gbrain-backup"
[[ -s "$TMP/brain.gbrain-backup" ]] || { echo "FAIL: missing native brain archive." >&2; exit 1; }

RESTORED="$TMP/isolated-new-brain"
[[ ! -e "$RESTORED" ]] || { echo "Refusing existing restore directory." >&2; exit 1; }
echo "Restoring to a separate absent root using mode new-brain..."
gbrain backup restore "$TMP/brain.gbrain-backup" --into "$RESTORED" --mode new-brain --json > "$TMP/restore.json"
python3 - "$TMP/restore.json" <<'PY'
import json, sys
with open(sys.argv[1], encoding='utf-8') as fh:
    r = json.load(fh)
if not isinstance(r, dict) or not r.get('ok'):
    raise SystemExit('FAIL: native restore did not return ok=true')
print('PASS: native GBrain restore reported ok=true')
PY

echo "Querying only the isolated restored database..."
while IFS='|' read -r query slug; do
  [[ -n "$query" ]] || continue
  GBRAIN_HOME="$RESTORED" gbrain recall --query "$query" --source default --json > "$TMP/recall.json"
  python3 - "$TMP/recall.json" "$slug" <<'PY'
import json, sys
with open(sys.argv[1], encoding='utf-8') as fh:
    result = json.load(fh)
wanted = sys.argv[2]
results = result.get('results', []) if isinstance(result, dict) else []
if not any(isinstance(row, dict) and row.get('slug') == wanted for row in results):
    raise SystemExit(f'FAIL: {wanted} missing from the ISOLATED recovered database')
print(f'PASS: restored GBrain page {wanted}')
PY
done <<'PAGES'
GBRAIN_OP_FACTORY_RESOLVER_2026_11_03|00_factory_resolver
GBRAIN_OP_ANNA_DIARY_2026_11_03|10_annas_diary
GBRAIN_OP_TRAILPATH_2026_11_03|20_trailpath
GBRAIN_OP_NOTES_ECOSISTEMA_2026_11_03|30_notes_ecosistema
GBRAIN_OP_CAMPERBOSS_2026_11_03|40_camperboss
GBRAIN_OP_APP_LAB_GATES_2026_11_03|50_app_lab_gates
GBRAIN_OP_CAPABILITY_REUSE_2026_11_03|60_capability_reuse
GBRAIN_OP_COOKING_ANIME_2026_11_03|70_cooking_anime
PAGES

echo
echo "PASS: 8/8 operational App Factory pages restored from this exact encrypted SSD archive."
echo "PASS: verification ran in an isolated temporary GBrain root; live service left unchanged."
echo "CAUTION: detachability and off-PC retention of the SSD are not proven by this test."
echo "CAUTION: preserve your passphrase separately from the encrypted archive."
