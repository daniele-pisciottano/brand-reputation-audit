# Brand Reputation Audit

Una skill per Claude Code che raccoglie quello che si dice di un brand su fonti
diverse, lo incrocia e produce un report HTML navigabile più i dati grezzi.

Orchestra due servizi, DataForSEO e Apify, per coprire SERP, AI Overview, risposte
e storico delle menzioni negli LLM, Reddit, Trustpilot, Google Maps, TikTok,
Instagram, commenti e trascrizioni YouTube e il sito del brand. Il processo resta lo
stesso per qualunque cliente, cambia solo il perimetro.

---

## Installazione

In Claude Code una skill è **una cartella dentro `~/.claude/skills/`**. Non c'è
altro da sapere: qualunque strada scegli, il risultato è quella cartella al suo
posto. Non esiste un comando `claude skill install`, quindi non cercarlo.

### Se hai il link al repository

Una riga, niente download e niente cartelle da spostare. È anche la via che si
aggiorna con un `git pull`.

```bash
git clone https://github.com/UTENTE/brand-reputation-audit.git \
  ~/.claude/skills/brand-reputation-audit
```

### Se hai scaricato lo zip

```bash
unzip brand-reputation-audit.zip
cd brand-reputation-audit
bash install.sh
```

Lo script copia la cartella in `~/.claude/skills/`, mette da parte una eventuale
versione precedente e stampa i passi successivi. Con `--project` la installa solo
nel progetto corrente, sotto `.claude/skills/`.

Se preferisci non eseguire uno script altrui, e fai bene a chiedertelo, le due
righe che fa sono queste:

```bash
mkdir -p ~/.claude/skills
cp -R brand-reputation-audit ~/.claude/skills/
```

### Se hai il file .skill

È uno zip con dentro la stessa cartella. Rinominalo e apri, oppure:

```bash
unzip brand-reputation-audit.skill -d ~/.claude/skills/
```

### Poi, sempre

**Riavvia Claude Code.** Le skill si caricano all'avvio e una appena copiata non
compare nella sessione già aperta.

Poi servono i due servizi: i comandi sono qui sotto, e li stampa anche
`bash scripts/preflight.sh` quando ne manca uno.

### Verificare che la skill ci sia

Apri Claude Code e scrivi una frase come "analizza la reputazione online di
[un brand]". Se la skill è installata, Claude la usa da solo. In alternativa
digita `/` e cerca `brand-reputation-audit` nell'elenco.

Se non compare, nel novantanove per cento dei casi è una di queste tre:

- Claude Code non è stato riavviato
- la cartella è annidata due volte, cioè `~/.claude/skills/brand-reputation-audit/brand-reputation-audit/SKILL.md`
  invece di `~/.claude/skills/brand-reputation-audit/SKILL.md`
- il percorso è `~/.claude/skill/` invece di `~/.claude/skills/`

Per controllare in un colpo solo:

```bash
ls ~/.claude/skills/brand-reputation-audit/SKILL.md
```

Se questo comando stampa il percorso, la skill è al posto giusto.

---

## Cosa serve prima di partire

Due servizi, entrambi a consumo e senza abbonamento mensile obbligatorio. Tutti e
due pubblicano un server remoto, quindi bastano due comandi e nessuna credenziale da
incollare: l'autorizzazione si fa nel browser al primo utilizzo.

```bash
claude mcp add --transport http dataforseo https://mcp.dataforseo.com/mcp
claude mcp add --transport http apify      https://mcp.apify.com
```

Poi **riavvia Claude Code** e verifica:

```bash
bash scripts/preflight.sh
```

**DataForSEO** copre SERP, AI Overview, risposte degli LLM e storico delle menzioni.
L'account è prepagato, si ricarica quanto serve e non c'è nessun canone.
**Apify** copre recensioni, social, commenti, trascrizioni video e scraping del
sito. Il piano gratuito include un credito mensile che basta per provare un audit
veloce.

Se preferisci far girare DataForSEO in locale con le tue credenziali API, invece
del server remoto, il comando alternativo e la nota sui moduli da abilitare sono in
`references/setup-mcp.md`.

---

## Come si usa

Basta chiedere. Qualche esempio di frase che fa partire la skill:

- "Analizza la reputazione online di [brand] sul mercato italiano"
- "Cosa dicono gli LLM di [brand], e da dove lo prendono"
- "Fammi un brand audit di [brand] per un pitch di giovedì"
- "Raccogli recensioni e conversazioni su [brand] e confrontalo con [competitor]"

La skill fa sette domande iniziali, brand, mercato, competitor, cosa vuoi sapere,
su quale **orizzonte temporale**, con quale **tetto massimo di contenuti e di spesa**
e quanto a fondo vuoi andare. Poi propone un piano di raccolta con la stima dei
costi, che si approva prima che parta qualsiasi spesa. Il tetto dichiarato viene
rispettato anche quando i dati sono interessanti: se una fonte sta per sforare, la
skill si ferma e chiede.

### I tre livelli di profondità

| Livello | Tempi | Quando |
|---------|-------|--------|
| Quick | 10-15 minuti | Una prima occhiata, o una demo |
| Standard | 30-45 minuti | Un audit vero per un cliente |
| Deep | 1-2 ore | La baseline di un monitoraggio, con i competitor |

---

## Cosa ottieni

```
output/<brand>-<data>/
├── report.html          il report navigabile, un file solo, si apre e si manda
├── data.json            il dataset normalizzato che alimenta il report
├── audit-plan.md        il perimetro approvato prima della raccolta
├── METODOLOGIA.md       fonti, volumi, date, limiti, fonti fallite
└── raw/                 le risposte grezze di ogni fonte
```

Il report contiene la sintesi, il sentiment per fonte, la **cronistoria**, i temi
ricorrenti con le citazioni testuali, la vista **canale per canale**, **cosa si dice
dentro i video** di canali terzi, lo share of voice nelle risposte generative, la
mappa dei domini che costruiscono la reputazione del brand e il confronto fra come
il brand si racconta e come viene raccontato.

Tre sezioni meritano una riga in più.

**La cronistoria** mostra come sono cambiati volume, giudizio e temi lungo la
finestra scelta, con i picchi spiegati uno per uno e la visibilità negli LLM nel
tempo. È la differenza fra "il 34 per cento dei giudizi è negativo", che fa alzare
le spalle, e "era il 19 per cento a ottobre, la salita comincia a marzo ed è quasi
tutta su un tema solo", che fa prendere il telefono.

**La vista per canale** mostra gli stessi contenuti per piattaforma invece che per
tema: volume, giudizio, di cosa si parla e come lo si dice, un canale alla volta.
La riga che conta è il tema dominante, perché quando cambia da un canale all'altro
vuol dire che il brand ha problemi diversi a seconda di dove lo si ascolta.

**La sezione sui video** analizza le trascrizioni dei canali terzi, non del brand.
I commenti dicono cosa pensa il pubblico, la trascrizione dice cosa gli è stato
detto da chi ha in mano il microfono. Ogni citazione riporta il minutaggio, così si
verifica in dieci secondi.

Per vedere come si presenta senza spendere niente:

```bash
python3 scripts/build_report.py examples/data.demo.json --open
```

I dati di quell'esempio sono inventati e il brand non esiste: serve solo a mostrare
la forma del risultato.

---

## Com'è fatta

```
brand-reputation-audit/
├── SKILL.md                          il processo in sei fasi
├── references/
│   ├── setup-mcp.md                  collegare i due server, errori frequenti
│   ├── apify-actors.md               scegliere gli attori, criteri e candidati
│   ├── dataforseo-playbook.md        SERP, LLM, storico menzioni, matrice prompt
│   ├── analysis-framework.md         sentiment, temi, cronistoria, video, fonti
│   └── report-spec.md                schema di data.json e regole del report
├── scripts/
│   ├── preflight.sh                  verifica le connessioni MCP
│   └── build_report.py               genera il report e controlla i dati
├── assets/
│   └── report_template.html          il template, con grafici e modalità scura
└── examples/
    └── data.demo.json                un dataset finto per vedere il risultato
```

Due scelte progettuali che vale la pena conoscere.

**Gli attori Apify non sono scritti nel codice.** Lo store cambia in continuazione,
gli attori vengono deprecati e i prezzi si spostano. La skill parte da una lista di
candidati e li verifica ogni volta, scartando quelli con canone mensile. Così non
invecchia.

**Il report si genera con uno script, non a mano.** Lo script controlla anche la
coerenza dei dati prima di scrivere: segnala i totali che non tornano, le quote
espresse in percentuale invece che da 0 a 1, i temi senza citazioni, i periodi della
cronistoria troppo poco popolati perché una percentuale abbia senso, le citazioni
video senza minutaggio e il tetto di raccolta sforato. Sono quasi sempre errori veri.

**Le due API generative di DataForSEO non fanno la stessa cosa**, e la skill le usa
entrambe. Una interroga i modelli adesso con i prompt che scrivi tu, ed è una
rilevazione controllata ma senza storia. L'altra cerca dentro un archivio molto
grande di risposte già raccolte, e dà la scala e lo storico che la prima non può
avere. Un audit con una sola delle due è monco, e quasi tutti ne usano una sola.

---

## Personalizzare

**Logo.** In testata compare il logo di chi firma il report, con una variante per il
fondo scuro. Si cambia con `meta.logo` e `meta.logo_dark` dentro `data.json`, e con
`meta.logo: false` si toglie del tutto. Se il file non si carica il logo sparisce da
solo, senza lasciare l'icona di un'immagine rotta.

**Colori.** Il template usa un accento rosso che si cambia in un punto solo, nel
blocco `:root` in cima a `assets/report_template.html`, oppure passando
`meta.accent` dentro `data.json`. I colori delle serie nei grafici sono stati
verificati per leggibilità e per distinguibilità in caso di daltonismo, in chiaro
e in scuro: se li sostituisci con quelli di un cliente, rivalidali.

**Carattere.** Figtree, caricato dal web con una sequenza di ripiego solida. Per un
report che deve funzionare offline in modo garantito, incorpora il carattere in
base64 al posto della riga di importazione.

**Fonti.** Per aggiungere una piattaforma, aggiungi una voce in
`references/apify-actors.md` con i suoi candidati e i volumi per livello. Non serve
toccare altro: il report disegna quello che trova.

---

## Costi indicativi

Un audit Standard su un brand con buon volume di conversazione sta tipicamente fra
i tre e gli otto dollari di crediti Apify, più il consumo DataForSEO, che dipende
soprattutto da quanti prompt generativi esegui e quante volte li ripeti. Un audit
Quick costa una frazione. La skill stima i costi nel piano e li riporta a
consuntivo in `METODOLOGIA.md`, così un monitoraggio ricorrente diventa prevedibile.

---

## Avvertenze

La skill raccoglie solo contenuti pubblici e non aggira login o protezioni.

Il sentiment è un segnale, non un verdetto: chi scrive recensioni e commenti è
autoselezionato e più polarizzato della base clienti, e il report lo dichiara
invece di nasconderlo dietro una percentuale.

Nel report i dati rilevati e le interpretazioni restano su piani separati, così chi
legge può dissentire dalle conclusioni senza dover dubitare dei numeri. Le
affermazioni sui brand vanno formulate come rilevazioni, non come accertamenti.

Le risposte degli LLM e le SERP cambiano di settimana in settimana: ogni audit
riporta la data di raccolta ed è da considerarsi datato.

---

MIT.
