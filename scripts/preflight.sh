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
  cat <<'EOF'
La CLI 'claude' non e' disponibile qui, quindi non posso leggere l'elenco dei
server MCP.

Questa skill e' pensata per Claude Code: se sei li', assicurati che 'claude' sia
nel PATH e rilancia questo preflight.

Se invece la stai usando su claude.ai o nell'app desktop, i due servizi si
collegano come connettori invece che da terminale: Personalizza, Connettori,
"Aggiungi connettore personalizzato", e incolla questi indirizzi.

  DataForSEO   https://mcp.dataforseo.com/mcp
  Apify        https://mcp.apify.com

Il dettaglio e' in references/setup-mcp.md, ultima sezione.
EOF
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

echo "Manca qualcosa. Comandi da eseguire NEL TERMINALE."
echo "Entrambi i servizi hanno un server remoto: nessuna credenziale da incollare,"
echo "l'autorizzazione si fa nel browser al primo utilizzo."
echo

if [ "$DFS" -ne 0 ]; then
  echo "DataForSEO (SERP, AI Overview, risposte e storico menzioni negli LLM)"
  echo "  Serve un account DataForSEO, prepagato e senza canone."
  echo
  echo "  claude mcp add --transport http dataforseo https://mcp.dataforseo.com/mcp"
  echo
fi

if [ "$APY" -ne 0 ]; then
  echo "Apify (recensioni, social, commenti, trascrizioni video, scraping del sito)"
  echo "  Il piano gratuito include un credito mensile, sufficiente per un audit Quick."
  echo
  echo "  claude mcp add --transport http apify https://mcp.apify.com"
  echo
fi

echo "Se preferisci far girare i server in locale con le tue credenziali API,"
echo "i comandi alternativi sono in references/setup-mcp.md."
echo
echo "Dopo l'installazione RIAVVIA Claude Code: i server MCP si caricano all'avvio."
echo "Poi rilancia questo preflight."
exit 1
