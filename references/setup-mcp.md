# Collegare DataForSEO e Apify a Claude Code

Questa pagina serve in due momenti: quando il preflight dice che manca un server,
e quando un server c'è ma risponde con un errore. Le istruzioni sono scritte per
essere passate all'utente quasi così come sono.

**Regola di sicurezza prima di tutto: non chiedere mai all'utente di scrivere token
o password nella chat.** Dagli il comando con i segnaposto e lascia che lo esegua
nel suo terminale. Quello che finisce nella conversazione resta nella cronologia
della conversazione.

---

## Indice

- [Verificare cosa è già collegato](#verificare-cosa-è-già-collegato)
- [DataForSEO](#dataforseo)
- [Apify](#apify)
- [Verifica che funzionino davvero](#verifica-che-funzionino-davvero)
- [Errori frequenti e rimedi](#errori-frequenti-e-rimedi)

---

## Verificare cosa è già collegato

```bash
claude mcp list
```

Restituisce i server configurati e il loro stato di connessione. Cerca una voce che
contenga `dataforseo` e una che contenga `apify`. I nomi sono scelti da chi ha fatto
l'installazione, quindi non aspettarti una stringa esatta: cerca per sottostringa.

Se un server risulta presente ma in stato di errore, il problema non è
l'installazione ma le credenziali o la rete, e la sezione degli errori frequenti in
fondo copre i casi tipici.

---

## DataForSEO

Serve per le SERP, per l'AI Overview, per interrogare gli LLM in modo programmatico
e per le menzioni del brand nelle risposte generative.

### Credenziali

Si prendono dalla dashboard DataForSEO, nella sezione API Access. Sono una coppia
utente più password dedicata alle API, diversa dalle credenziali di login al sito.
L'account è a consumo con ricarica prepagata, quindi non serve un abbonamento
mensile per iniziare.

### Installazione

```bash
claude mcp add dataforseo \
  --env DATAFORSEO_USERNAME=IL_TUO_USERNAME_API \
  --env DATAFORSEO_PASSWORD=LA_TUA_PASSWORD_API \
  -- npx -y dataforseo-mcp-server
```

Richiede Node.js 18 o superiore. Dopo il comando, **riavvia Claude Code**: i server
MCP vengono caricati all'avvio e un server aggiunto a sessione in corso non compare.

### Limitare i moduli attivi

Per impostazione predefinita il server espone tutti i moduli, compresi quelli più
costosi come Labs e Backlinks. Per questo audit servono questi:

```bash
claude mcp add dataforseo \
  --env DATAFORSEO_USERNAME=IL_TUO_USERNAME_API \
  --env DATAFORSEO_PASSWORD=LA_TUA_PASSWORD_API \
  --env ENABLED_MODULES="SERP,AI_OPTIMIZATION,CONTENT_ANALYSIS,BUSINESS_DATA,KEYWORDS_DATA" \
  -- npx -y dataforseo-mcp-server
```

I nomi dei moduli sono **maiuscoli ed esatti**. Questo è l'errore numero uno con
questo server: un nome sbagliato non produce un messaggio di errore, produce
semplicemente zero strumenti disponibili. Se dopo l'installazione non vedi nessuno
strumento DataForSEO, il sospettato principale è una variabile `ENABLED_MODULES`
scritta male. In caso di dubbio togli del tutto la variabile, così vengono caricati
tutti i moduli, e restringi dopo.

---

## Apify

Serve per tutto lo scraping di recensioni, social e sito.

### Via server remoto, la strada consigliata

```bash
claude mcp add --transport http apify https://mcp.apify.com
```

Al primo utilizzo parte l'autenticazione via browser e non serve mettere nessun
token in un file di configurazione. Il server remoto è mantenuto da Apify e si
aggiorna da solo, quindi gli attori nuovi sono disponibili senza reinstallare
niente.

### Via pacchetto locale, se il remoto non è praticabile

```bash
claude mcp add apify \
  --env APIFY_TOKEN=apify_api_IL_TUO_TOKEN \
  -- npx -y @apify/actors-mcp-server
```

Il token si genera dalla console Apify, nelle impostazioni di integrazione. Il piano
gratuito include un credito mensile che basta per un audit Quick, quindi si può
provare tutto senza pagare.

### Nota importante sugli attori disponibili

Il server MCP di Apify espone un insieme di attori più gli strumenti per cercarne e
aggiungerne altri a sessione in corso. Se un attore che ti serve non risulta
disponibile come strumento diretto, non concludere che non si possa usare: cerca
prima con gli strumenti di ricerca degli attori e aggiungilo. La procedura è in
`apify-actors.md`.

---

## Verifica che funzionino davvero

Un server che compare nell'elenco non è ancora un server che risponde. Prima di
lanciare la raccolta fai due chiamate di prova, scelte perché costano pochissimo:

- **DataForSEO**: una richiesta di elenco delle location disponibili, oppure una
  singola SERP su una keyword banale. Se torna un errore 401, le credenziali sono
  sbagliate. Se torna un 402, il credito è esaurito.
- **Apify**: una chiamata di ricerca attori, che è gratuita, oppure una singola run
  di uno scraper leggero con limite a cinque risultati.

Se la prova fallisce, fermati e risolvi. Lanciare una raccolta completa su una
connessione incerta significa pagare per delle run che falliscono a metà.

---

## Errori frequenti e rimedi

| Sintomo | Causa più probabile | Rimedio |
|---------|--------------------|---------|
| Il server non compare dopo `claude mcp add` | Claude Code non è stato riavviato | Riavvia Claude Code |
| Nessuno strumento DataForSEO disponibile | `ENABLED_MODULES` con nomi sbagliati | Rimuovi la variabile e reinstalla, poi restringi |
| Errore 401 su DataForSEO | Credenziali del sito invece di quelle API | Prendi utente e password dalla sezione API Access |
| Errore 402 o messaggio di credito | Prepagato esaurito | Ricarica, oppure riduci la profondità dell'audit |
| Apify chiede di autenticarsi a ogni chiamata | Sessione OAuth non persistita | Passa all'installazione con token locale |
| Un attore restituisce zero risultati | Input schema cambiato o handle sbagliato | Rileggi lo schema dell'attore, verifica l'URL o l'handle di partenza |
| Una run Apify resta appesa | Attore lento o volumi troppo alti | Abbassa il limite di risultati, non rilanciare uguale |
| Timeout ripetuti su un attore | Attore non mantenuto | Scegli un attore alternativo con la procedura in `apify-actors.md` |

### Quando un server manca e l'utente non può installarlo subito

Proponi l'audit parziale, dicendo con precisione cosa resta fuori:

- **Senza DataForSEO** perdi SERP, AI Overview, risposte degli LLM e share of voice
  generativo. Resta un'analisi di recensioni e conversazioni, utile ma senza il
  pezzo che collega la reputazione alla visibilità.
- **Senza Apify** perdi recensioni, social e commenti, cioè il volume e le citazioni
  vere degli utenti. Resta un'analisi di posizionamento e di percezione negli LLM,
  che però poggia su una base più stretta.

In entrambi i casi il limite va scritto in `METODOLOGIA.md` e ricordato nella prima
schermata del report, non nascosto in fondo.
