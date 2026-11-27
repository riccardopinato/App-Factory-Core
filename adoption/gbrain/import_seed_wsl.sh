#!/usr/bin/env bash
# App Factory -> GBrain single-page pilot seed. Run ONLY in Ubuntu WSL as the GBrain owner.
# This is a one-time manual operation; it never broadens OAuth scopes or enables cron/AI APIs.
set -euo pipefail
umask 077

SEED_COMMIT="c7431296df2d473f3b0157b0dd4079ef29fd04f5"
SEED_URL="https://raw.githubusercontent.com/riccardopinato/App-Factory-Core/${SEED_COMMIT}/adoption/gbrain/APP_FACTORY_SEED_INDEX_2026-11-02.md"
SERVICE="gbrain-serve.service"
BACKUP_DIR="${HOME}/gbrain-private-backups"
MARKER="${HOME}/.gbrain/app-factory-seed-index-2026-11-02.imported"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
TMP_DIR=""

cleanup() {
  rc=$?
  trap - EXIT
  if [[ "${SERVICE_STOPPED:-0}" -eq 1 ]]; then
    echo "Restoring the existing GBrain service..."
    if ! systemctl --user start "$SERVICE"; then
      echo "ERROR: service restart failed. Run: systemctl --user status $SERVICE" >&2
      rc=1
    fi
  fi
  if [[ -n "$TMP_DIR" && -d "$TMP_DIR" ]]; then
    rm -rf -- "$TMP_DIR"
  fi
  exit "$rc"
}
trap cleanup EXIT

[[ "$(uname -s)" == "Linux" ]] || { echo "Run this in the Ubuntu terminal, not PowerShell." >&2; exit 1; }
for cmd in gbrain curl systemctl; do
  command -v "$cmd" >/dev/null || { echo "Missing command: $cmd" >&2; exit 1; }
done
if [[ -e "$MARKER" ]]; then
  echo "Already imported once: $MARKER. Review existing GBrain pages before any re-import." >&2
  exit 2
fi
if ! systemctl --user is-active --quiet "$SERVICE"; then
  echo "GBrain service is not active. Inspect its state before modifying PGLite." >&2
  exit 1
fi

# Stage a small, non-sensitive, commit-pinned derived index. Do not fetch or execute remote shell code.
TMP_DIR="$(mktemp -d)"
chmod 700 "$TMP_DIR"
mkdir -p "$TMP_DIR/seed"
curl -fLsS --proto '=https' --tlsv1.2 "$SEED_URL" -o "$TMP_DIR/seed/APP_FACTORY_SEED_INDEX_2026-11-02.md"
grep -q 'DERIVED SECONDARY MEMORY' "$TMP_DIR/seed/APP_FACTORY_SEED_INDEX_2026-11-02.md" || {
  echo "Downloaded seed did not match its expected header." >&2; exit 1;
}
mkdir -p "$BACKUP_DIR"
chmod 700 "$BACKUP_DIR"
echo "About to pause the local GBrain service, create a private backup, and import ONE derived Markdown page."
echo "No paid model call, no GitHub mutation, no OAuth permission changes; brief ChatGPT MCP downtime expected."
read -r -p "To proceed, type IMPORTA: " confirm
[[ "$confirm" == "IMPORTA" ]] || { echo "Cancelled; nothing imported."; exit 0; }

echo "Stopping $SERVICE..."
systemctl --user stop "$SERVICE"
SERVICE_STOPPED=1

# DB and service-managed backup; keep canonical source roots separately as official docs require.
ARCHIVE="$BACKUP_DIR/gbrain-before-appfactory-${STAMP}.gbrain-backup"
echo "Creating private operational backup: $ARCHIVE"
gbrain backup create --output "$ARCHIVE"

if [[ -d "$HOME/.gbrain/content" ]]; then
  echo "Copying canonical content separately, as it may be omitted from the archive."
  cp -a "$HOME/.gbrain/content" "$BACKUP_DIR/content-before-appfactory-${STAMP}"
fi

echo "Importing source-pinned Markdown index in keyless mode..."
gbrain import "$TMP_DIR/seed" --no-embed
printf 'seed_commit=%s\nsource=App-Factory-Core draft PR #41\nimported_utc=%s\nbackup=%s\n' "$SEED_COMMIT" "$STAMP" "$ARCHIVE" > "$MARKER"
chmod 600 "$MARKER"
echo "Imported seed. Local metadata: $MARKER"
# EXIT trap restarts GBrain even if backup/import fails.
echo "Run 'gbrain mcp expose --status' after the service restarts, then test recall in ChatGPT."
