# Collegare DataForSEO e Apify a Claude Code

Questa pagina serve in due momenti: quando il preflight dice che manca un servizio,
e quando un servizio c'è ma risponde con un errore. Le istruzioni sono scritte per
essere passate all'utente quasi così come sono.

**La via breve, che copre quasi tutti i casi.** Entrambi i servizi pubblicano un
server remoto, quindi bastano due comandi e nessuna credenziale da incollare:
l'autorizzazione avviene nel browser al primo utilizzo.

```bash
claude mcp add --transport http dataforseo https://mcp.dataforseo.com/mcp
claude mcp add --transport http apify      https://mcp.apify.com
```

Poi **riavvia Claude Code**, perché i server MCP si caricano all'avvio e uno
aggiunto a sessione in corso non compare.

**Regola di sicurezza: non chiedere mai all'utente di scrivere token o password
nella chat.** Restano nella cronologia della conversazione. Con i server remoti il
problema non si pone, e nelle installazioni locali qui sotto i segreti stanno nei
segnaposto e il comando si esegue nel terminale.

---

## Indice

- [Verificare cosa è già collegato](#verificare-cosa-e-gia-collegato)
- [Installazione locale, se serve](#installazione-locale-se-serve)
- [Verifica che funzionino davvero](#verifica-che-funzionino-davvero)
- [Errori frequenti e rimedi](#errori-frequenti-e-rimedi)
- [Quando un servizio manca e non si può collegare subito](#quando-un-servizio-manca-e-non-si-può-collegare-subito)
- [Se non sei in Claude Code](#se-non-sei-in-claude-code)

---

## Verificare cosa è già collegato

```bash
claude mcp list
```

Restituisce i server configurati e il loro stato. Cerca una voce che contenga
`dataforseo` e una che contenga `apify`. I nomi li sceglie chi installa, quindi
cerca per sottostringa e non per corrispondenza esatta.

## Installazione locale, se serve

Serve solo a chi preferisce far girare i server sulla propria macchina invece di
usare quelli remoti, tipicamente per controllare quali moduli sono attivi o per
policy aziendali. Se i due comandi della via breve hanno funzionato, salta questa
parte.

### DataForSEO in locale

Le credenziali si prendono dalla dashboard DataForSEO, nella sezione API Access.
Sono una coppia utente più password dedicata alle API, diversa dalle credenziali di
accesso al sito.

```bash
claude mcp add dataforseo \
  --env DATAFORSEO_USERNAME=IL_TUO_USERNAME_API \
  --env DATAFORSEO_PASSWORD=LA_TUA_PASSWORD_API \
  --env ENABLED_MODULES="SERP,AI_OPTIMIZATION,CONTENT_ANALYSIS,BUSINESS_DATA,KEYWORDS_DATA" \
  -- npx -y dataforseo-mcp-server
```

Richiede Node.js 18 o superiore. I nomi dei moduli sono **maiuscoli ed esatti**, ed
è l'errore numero uno con questo server: un nome sbagliato non produce un messaggio
di errore, produce zero strumenti disponibili. Se dopo l'installazione non vedi
nessuno strumento DataForSEO, togli del tutto `ENABLED_MODULES`, reinstalla, e
restringi dopo.

### Apify in locale

```bash
claude mcp add apify \
  --env APIFY_TOKEN=apify_api_IL_TUO_TOKEN \
  -- npx -y @apify/actors-mcp-server
```

Il token si genera dalla console Apify. Tieni presente che il server remoto è
mantenuto da Apify e si aggiorna da solo, quindi con la versione locale gli attori
nuovi arrivano solo quando aggiorni il pacchetto.

Dopo qualunque installazione, **riavvia Claude Code**.

### Nota sugli attori Apify disponibili

Il server di Apify espone un insieme di attori più gli strumenti per cercarne e
aggiungerne altri a sessione in corso. Se un attore che ti serve non risulta
disponibile come strumento diretto, non concludere che non si possa usare: cercalo
prima con gli strumenti di ricerca e aggiungilo. La procedura è in
`apify-actors.md`.

---

## Verifica che funzionino davvero

Un servizio che compare nell'elenco non è ancora un servizio che risponde. Prima di
lanciare la raccolta fai due chiamate di prova, scelte perché costano pochissimo:

- **DataForSEO**: una richiesta di elenco delle località disponibili, oppure una
  singola SERP su una keyword banale. Un errore 401 significa credenziali sbagliate,
  un 402 significa credito esaurito.
- **Apify**: una ricerca fra gli attori, che è gratuita, oppure una singola raccolta
  con limite a cinque risultati.

Se la prova fallisce, fermati e risolvi. Lanciare una raccolta completa su una
connessione incerta significa pagare per operazioni che falliscono a metà.

---

## Errori frequenti e rimedi

| Sintomo | Causa più probabile | Rimedio |
|---------|--------------------|---------|
| Il server non compare dopo `claude mcp add` | Claude Code non riavviato | Riavvia Claude Code |
| Il server c'è ma non ha strumenti | Autorizzazione nel browser non completata | Rilancia una chiamata e completa l'autorizzazione |
| Nessuno strumento DataForSEO disponibile | `ENABLED_MODULES` con nomi sbagliati | Rimuovi la variabile e reinstalla, poi restringi |
| Errore 401 su DataForSEO | Credenziali del sito invece di quelle API | Prendile dalla sezione API Access |
| Errore 402 o messaggio di credito | Prepagato esaurito | Ricarica, oppure riduci la profondità dell'audit |
| Un attore restituisce zero risultati | Schema di input cambiato o handle sbagliato | Rileggi lo schema dell'attore, verifica URL o handle di partenza |
| Una raccolta resta appesa | Attore lento o volumi troppo alti | Abbassa il limite di risultati, non rilanciare uguale |
| Timeout ripetuti su un attore | Attore non mantenuto | Scegli un'alternativa con la procedura in `apify-actors.md` |
| Lo script del report non parte | Esecuzione di codice non disponibile | Consegna `data.json` e spiega come generare il report altrove |

---

## Quando un servizio manca e non si può collegare subito

Proponi l'audit parziale, dicendo con precisione cosa resta fuori:

- **Senza DataForSEO** perdi SERP, AI Overview, risposte degli LLM, storico delle
  menzioni e share of voice generativo. Resta un'analisi di recensioni e
  conversazioni, utile, ma senza il pezzo che collega la reputazione alla visibilità
  e senza cronistoria della parte generativa.
- **Senza Apify** perdi recensioni, social, commenti e trascrizioni video, cioè il
  volume e le citazioni vere degli utenti. Resta un'analisi di posizionamento e di
  percezione negli LLM, che però poggia su una base molto più stretta.

Se l'utente può tenerne uno solo e non sa quale scegliere, la domanda che scioglie
il dubbio è: **vuoi sapere cosa dicono le persone, o vuoi sapere cosa dicono le
macchine?** Per un audit di reputazione classico serve Apify, per un audit di
visibilità generativa serve DataForSEO.

In entrambi i casi il limite va scritto in `METODOLOGIA.md` e ricordato nella prima
schermata del report, non nascosto in fondo.

---

## Se non sei in Claude Code

La skill è pensata per Claude Code. Se qualcuno la carica su claude.ai o
nell'app desktop funziona lo stesso, ma lì i due servizi non si aggiungono da
terminale: vanno messi come connettori, da **Personalizza**, **Connettori**,
**Aggiungi connettore personalizzato**, incollando gli stessi due indirizzi
(`https://mcp.dataforseo.com/mcp` e `https://mcp.apify.com`) e autorizzando nel
browser. Sul piano gratuito si può tenere un connettore personalizzato solo,
quindi per usarli entrambi serve un piano superiore.

Verifica anche che l'esecuzione di codice sia disponibile, perché il report si
genera con uno script Python. Se non lo è, puoi comunque produrre `data.json`,
ma dillo all'utente prima di cominciare e non alla fine.
