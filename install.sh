#!/usr/bin/env bash
# Installa la skill brand-reputation-audit per Claude Code.
#
#   bash install.sh              installa per l'utente, disponibile in ogni progetto
#   bash install.sh --project    installa solo nel progetto corrente
#
# Non tocca la configurazione dei server MCP: quella la fa scripts/preflight.sh,
# che stampa i comandi giusti quando manca qualcosa.

set -euo pipefail

NAME="brand-reputation-audit"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "${1:-}" = "--project" ]; then
  DEST="$(pwd)/.claude/skills"
  SCOPE="progetto corrente"
else
  DEST="$HOME/.claude/skills"
  SCOPE="utente, disponibile in ogni progetto"
fi

if [ ! -f "$SRC/SKILL.md" ]; then
  echo "SKILL.md non trovato in $SRC: lancia lo script dalla cartella della skill." >&2
  exit 1
fi

mkdir -p "$DEST"
TARGET="$DEST/$NAME"

if [ -e "$TARGET" ]; then
  BACKUP="$TARGET.bak.$(date +%Y%m%d%H%M%S)"
  echo "Esiste gia' una versione installata, la sposto in:"
  echo "  $BACKUP"
  mv "$TARGET" "$BACKUP"
fi

mkdir -p "$TARGET"
for item in SKILL.md README.md references scripts assets examples; do
  [ -e "$SRC/$item" ] && cp -R "$SRC/$item" "$TARGET/"
done
chmod +x "$TARGET/scripts/preflight.sh" 2>/dev/null || true

echo
echo "Installata: $TARGET"
echo "Ambito: $SCOPE"
echo
echo "Passi successivi"
echo "  1. Riavvia Claude Code, le skill si caricano all'avvio"
echo "  2. Verifica i server MCP:  bash \"$TARGET/scripts/preflight.sh\""
echo "  3. Prova a chiedere:       analizza la reputazione online di <un brand>"
echo
echo "Per vedere che aspetto ha un report senza spendere niente:"
echo "  python3 \"$TARGET/scripts/build_report.py\" \"$TARGET/examples/data.demo.json\" --open"
