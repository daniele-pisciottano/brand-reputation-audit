#!/usr/bin/env bash
# Verifica che i server MCP necessari all'audit siano configurati.
# Non tocca niente e non installa niente: guarda e riferisce.
#
#   bash scripts/preflight.sh
#
# Uscita 0 se ci sono entrambi, 1 se ne manca almeno uno.

set -uo pipefail

echo "Preflight brand-reputation-audit"
echo "--------------------------------"

if ! command -v claude >/dev/null 2>&1; then
  echo "La CLI 'claude' non e' nel PATH."
  echo "Questa skill e' pensata per Claude Code. Verifica i server MCP dal tuo client."
  exit 1
fi

LIST="$(claude mcp list 2>&1 || true)"

if [ -z "${LIST// }" ]; then
  echo "Nessun server MCP configurato."
  LIST=""
fi

check() {
  local key="$1" label="$2"
  if printf '%s' "$LIST" | grep -qi -- "$key"; then
    local line
    line="$(printf '%s' "$LIST" | grep -i -- "$key" | head -1)"
    if printf '%s' "$line" | grep -qiE 'fail|error|disconnect'; then
      echo "  [!] $label: configurato ma non risponde"
      echo "      -> $line"
      return 2
    fi
    echo "  [ok] $label: presente"
    return 0
  fi
  echo "  [--] $label: NON configurato"
  return 1
}

check "dataforseo" "DataForSEO"; DFS=$?
check "apify"      "Apify";      APY=$?

echo
if [ "$DFS" -eq 0 ] && [ "$APY" -eq 0 ]; then
  echo "Entrambi i server rispondono."
  echo "Prima di raccogliere fai comunque una chiamata di prova per fonte:"
  echo "  - DataForSEO: un elenco di location, oppure una SERP su una keyword banale"
  echo "  - Apify: una ricerca attori, che e' gratuita"
  exit 0
fi

echo "Manca qualcosa. Comandi da eseguire NEL TERMINALE, sostituendo i segnaposto."
echo "Non incollare mai token o password dentro la chat."
echo

if [ "$DFS" -ne 0 ]; then
  cat <<'EOF'
DataForSEO (SERP, AI Overview, risposte degli LLM)
  Credenziali: dashboard DataForSEO, sezione API Access. Sono diverse da quelle
  con cui accedi al sito. Account prepagato, nessun abbonamento necessario.

  claude mcp add dataforseo \
    --env DATAFORSEO_USERNAME=IL_TUO_USERNAME_API \
    --env DATAFORSEO_PASSWORD=LA_TUA_PASSWORD_API \
    --env ENABLED_MODULES="SERP,AI_OPTIMIZATION,CONTENT_ANALYSIS,BUSINESS_DATA,KEYWORDS_DATA" \
    -- npx -y dataforseo-mcp-server

  I nomi dei moduli sono maiuscoli ed esatti. Se dopo l'installazione non vedi
  nessuno strumento, togli del tutto ENABLED_MODULES e reinstalla.

EOF
fi

if [ "$APY" -ne 0 ]; then
  cat <<'EOF'
Apify (recensioni, social, scraping del sito)
  Consigliato, con autenticazione dal browser al primo uso:

  claude mcp add --transport http apify https://mcp.apify.com

  In alternativa, con token locale preso dalla console Apify:

  claude mcp add apify \
    --env APIFY_TOKEN=apify_api_IL_TUO_TOKEN \
    -- npx -y @apify/actors-mcp-server

EOF
fi

echo "Dopo l'installazione RIAVVIA Claude Code: i server MCP si caricano all'avvio."
echo "Poi rilancia questo preflight."
exit 1
