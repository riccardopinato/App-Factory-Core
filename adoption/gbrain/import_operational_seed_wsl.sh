#!/usr/bin/env bash
# GBrain operational App Factory seed — manual import, not an unattended sync.
# ChatGPT MCP grant stays READ ONLY. This runs ONLY on owner's Ubuntu WSL host.
set -Eeuo pipefail
umask 077

SEED_SHA="32f51cc184e991e93885e73692d9f944cc5bc551"
SEED_ROOT="adoption/gbrain/operational-seed-2026-11-03"
BASE_URL="https://raw.githubusercontent.com/riccardopinato/App-Factory-Core/$SEED_SHA/$SEED_ROOT"
SERVICE="gbrain-serve.service"
MARKER="$HOME/.gbrain/appfactory-operational-seed-2026-11-03.imported"
PRIVATE_BACKUPS="$HOME/gbrain-private-backups"
WORK=""
SERVICE_NEEDS_RESTART=0
cleanup() {
  rc=$?
  trap - EXIT
  if (( SERVICE_NEEDS_RESTART )); then
    echo "Restarting original GBrain service..."
    if ! systemctl --user start "$SERVICE"; then
      echo "ERROR: service restart failed; inspect systemctl --user status $SERVICE" >&2
      rc=1
    fi
  fi
  if [[ -n "$WORK" && -d "$WORK" ]]; then rm -rf -- "$WORK"; fi
  exit "$rc"
}
trap cleanup EXIT

for dep in curl gbrain systemctl grep mktemp cp mv date sleep; do
  command -v "$dep" >/dev/null 2>&1 || { echo "Missing: $dep" >&2; exit 1; }
done
[[ "$(uname -s)" == Linux ]] || { echo "Run in Ubuntu WSL." >&2; exit 1; }
[[ -e "$MARKER" ]] && {
  echo "Already imported according to local marker: $MARKER"
  echo "No second import performed. Corrections require a new versioned package."
  exit 0
}
systemctl --user is-active --quiet "$SERVICE" || {
  echo "GBrain user service not running; inspect it before PGLite writes." >&2
  exit 1
}
mkdir -p -- "$PRIVATE_BACKUPS"
chmod 700 "$PRIVATE_BACKUPS"
WORK="$(mktemp -d "$PRIVATE_BACKUPS/.operational-import-XXXXXX")"
mkdir -p -- "$WORK/seed" "$WORK/content-snapshot"
echo "Downloading exactly eight commit-pinned, curated pages..."
for f in \
  00_FACTORY_RESOLVER.md 10_ANNAS_DIARY.md 20_TRAILPATH.md \
  30_NOTES_ECOSISTEMA.md 40_CAMPERBOSS.md 50_APP_LAB_GATES.md \
  60_CAPABILITY_REUSE.md 70_COOKING_ANIME.md; do
  curl --fail --location --silent --show-error --retry 2 \
    --proto '=https' --tlsv1.2 \
    "$BASE_URL/$f" -o "$WORK/seed/$f"
  [[ -s "$WORK/seed/$f" ]] && grep -q '^# GBRAIN_OP_' "$WORK/seed/$f" || {
    echo "Invalid page/header: $f; refusing import." >&2; exit 1;
  }
  echo "  verified page: $f"
done

echo
echo "Scope: eight operator-curated engineering pages in GBrain source default."
echo "No raw chats, user records, private diary, credentials, app code dumps."
echo "WARNING: old v24 Golden memory remains historical; new snapshot records v27."
echo "No embedding provider, OAuth permission change, writer/scheduler or paid API."
echo "Brief GBrain service pause, native local backup, separate content snapshot, import."
read -r -p "To import these eight pages, type IMPORTA_8: " APPROVAL
[[ "$APPROVAL" == IMPORTA_8 ]] || { echo "Cancelled. GBrain unchanged."; exit 0; }

BACKUP="$PRIVATE_BACKUPS/gbrain-pre-operational-$(date -u +%Y%m%dT%H%M%SZ).gbrain-backup"
SERVICE_NEEDS_RESTART=1
echo "Stopping GBrain service for PGLite exclusive access..."
systemctl --user stop "$SERVICE"
echo "Creating private native GBrain backup: $BACKUP"
gbrain backup create --output "$BACKUP"
if [[ -d "$HOME/.gbrain/content" ]]; then
  echo "Copying external canonical content separately..."
  cp -a -- "$HOME/.gbrain/content/." "$WORK/content-snapshot/"
  CONTENT_COPY="$BACKUP-content"
  mv -- "$WORK/content-snapshot" "$CONTENT_COPY"
  chmod 700 "$CONTENT_COPY"
  echo "Private content copy: $CONTENT_COPY"
fi
echo "Importing eight pages without embeddings..."
gbrain import "$WORK/seed" --no-embed
echo "Restarting GBrain..."
systemctl --user start "$SERVICE"
SERVICE_NEEDS_RESTART=0
systemctl --user is-active --quiet "$SERVICE" || {
  echo "GBrain user service not active." >&2; exit 1;
}
OK=0
for attempt in 1 2 3 4 5 6 7 8; do
  if curl --silent --fail "http://127.0.0.1:3131/health" >/dev/null; then
    OK=1; break
  fi
  sleep 1
done
(( OK )) || { echo "GBrain HTTP health failed; not marking as validated." >&2; exit 1; }
printf 'import_sha=%s\nimported_utc=%s\npages=8\n' "$SEED_SHA" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$MARKER"
chmod 600 "$MARKER"
echo
echo "PASS: local operational seed imported, original GBrain service healthy."
echo "Marker: $MARKER"
echo "Next: gbrain mcp expose --status; ChatGPT readback; then refresh encrypted SSD backup."
