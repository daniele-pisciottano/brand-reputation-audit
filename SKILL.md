---
name: brand-reputation-audit
description: >-
  Audit della reputazione di un brand sul web orchestrando i server MCP di DataForSEO e Apify: raccoglie dati da SERP, risposte degli LLM, Reddit, Trustpilot, Google Maps, TikTok, Instagram e YouTube, li incrocia e produce un report HTML navigabile con grafici più i file dati grezzi. Usa questa skill ogni volta che serve capire come si parla di un brand online, cosa sanno e cosa dicono gli LLM di un brand, che sentiment emerge da recensioni e conversazioni, quali fonti alimentano le risposte AI su un brand, o preparare un audit di reputazione per un cliente o un prospect. Trigger tipici: analizza la reputazione di X, cosa dicono di X online, cosa sa ChatGPT di X, fammi un brand audit di X, come viene percepito X sul web, share of voice di X nelle risposte AI, brand reputation audit for X, what do LLMs say about X. Attivala anche quando la richiesta nomina una sola fonte, per esempio solo le recensioni o solo i thread Reddit, perché il valore sta nell'incrocio fra fonti.
license: MIT
---

# Brand Reputation Audit

Raccoglie in modo strutturato quello che si dice di un brand su fonti diverse, lo
incrocia e lo consegna come report HTML navigabile più i dati grezzi.

Il valore non sta nel singolo scraping, che chiunque può fare con un tool
qualsiasi. Sta in tre cose che solo l'incrocio delle fonti produce: i **temi
ricorrenti** che emergono dagli stessi utenti su piattaforme diverse, il **gap**
tra come il brand si racconta e come viene raccontato, e la mappa delle **fonti
che alimentano le risposte degli LLM**, che è quella che trasforma un audit in un
piano di lavoro.

Il processo è sempre lo stesso, il perimetro cambia per ogni brand. Non partire
mai dalla lista delle fonti: parti dalle domande a cui l'audit deve rispondere,
perché sono quelle a decidere quali fonti valgono i soldi della raccolta.

## Come procedere

Sei fasi, in ordine. Le fasi 0, 1 e 2 si chiudono con una conferma dell'utente,
perché da lì in poi si spendono soldi veri.

| Fase | Cosa fai | Dove sono i dettagli |
|------|----------|----------------------|
| 0 | Preflight delle connessioni MCP | `references/setup-mcp.md` |
| 1 | Briefing, le domande all'utente | qui sotto |
| 2 | Piano di raccolta, con stima costi | qui sotto |
| 3 | Raccolta dati | `references/apify-actors.md`, `references/dataforseo-playbook.md` |
| 4 | Normalizzazione in `data.json` | `references/report-spec.md` |
| 5 | Analisi e report | `references/analysis-framework.md`, `scripts/build_report.py` |

---

## Fase 0, preflight

Prima di qualsiasi altra cosa verifica che DataForSEO e Apify rispondano. Farlo
adesso evita di scoprire a metà raccolta che manca una credenziale, con dei dati
a metà e un utente che ha già speso.

```bash
bash scripts/preflight.sh
```

Lo script elenca i server MCP configurati e dice quali dei due mancano. Se ne manca
uno, la procedura completa è in `references/setup-mcp.md`, scritta per essere
passata all'utente così com'è. Nella maggior parte dei casi bastano due comandi,
perché entrambi i servizi hanno un server remoto che si autorizza dal browser:

```bash
claude mcp add --transport http dataforseo https://mcp.dataforseo.com/mcp
claude mcp add --transport http apify      https://mcp.apify.com
```

Due regole non negoziabili:

- **Non chiedere mai all'utente di incollare token o password nella chat.** Restano
  nella cronologia della conversazione. Con i server remoti il problema non si pone,
  e per le installazioni locali il comando si esegue nel terminale con i segnaposto
  al posto dei segreti.
- **Non inventare credenziali e non proseguire "a secco".** Se un servizio manca,
  l'audit si ferma lì. Meglio una fase di setup di cinque minuti che un report
  costruito su metà dati senza dirlo.

Se manca solo uno dei due servizi puoi proporre un audit parziale, dichiarando in
modo esplicito cosa resta fuori. Senza DataForSEO perdi SERP, risposte LLM e storico
delle menzioni, cioè il pezzo più interessante. Senza Apify perdi recensioni, social
e trascrizioni video, cioè il volume e le citazioni vere.

---

## Fase 1, briefing

Servono poche informazioni, ma senza queste il resto è rumore. Chiedile in un
blocco solo, con dei default già proposti, così l'utente risponde in trenta
secondi invece di sostenere un interrogatorio. Se hai a disposizione uno strumento
di domande strutturate usalo, altrimenti una lista numerata va benissimo.

**Le sette domande che contano sempre:**

1. **Brand e sito.** Nome esatto, dominio, ed eventuali varianti con cui lo si
   scrive o lo si storpia (sigle, errori di battitura frequenti, il nome legale se
   diverso da quello commerciale). Le varianti servono davvero: buona parte delle
   conversazioni non usa il nome ufficiale.
2. **Mercato e lingua.** Paese e lingua dell'analisi. Un brand internazionale ha
   reputazioni diverse per mercato, e mischiarle produce medie che non descrivono
   nessuno. Se l'utente ne vuole più di uno, trattali come analisi separate che
   confluiscono in un confronto, non come un unico calderone.
3. **Competitor di riferimento.** Da due a quattro. Senza un termine di paragone
   un sentiment del 62 per cento non significa niente, perché non si sa se in quel
   settore sia un buon risultato o un disastro.
4. **Le domande a cui il report deve rispondere.** Questa è la domanda più
   importante e quasi nessuno la fa. Proponi tu tre o quattro ipotesi tipiche
   ("di cosa si lamentano davvero i clienti", "il brand compare quando si cerca la
   categoria senza nominarlo", "quali fonti stanno costruendo la percezione del
   brand agli occhi degli LLM") e fatti dire quali tiene.
5. **Orizzonte temporale.** Da quando a quando guardiamo, e con che granularità.
   Non è un dettaglio di filtro: decide se l'audit è una fotografia o un film.
   Proponi dodici mesi con granularità mensile come default, e spiega il compromesso
   in una riga: una finestra corta dice com'è adesso, una lunga dice come ci si è
   arrivati. Chiedi anche se c'è una **data spartiacque** da tenere a mente, un
   lancio, una crisi, un rebranding, un cambio di prezzo o di formulazione: sapere
   dove cade il confine trasforma la cronistoria da grafico a racconto.

| Finestra | Granularità | Quando |
|----------|-------------|--------|
| 3-6 mesi | settimanale | dopo un evento preciso, o su un brand molto discusso |
| 12 mesi | mensile | il default, copre la stagionalità e regge i confronti |
| 24-36 mesi | mensile o trimestrale | per vedere un cambio di percezione strutturale |

   Se il brand è piccolo e la conversazione scarsa, una finestra lunga con
   granularità larga è meglio di una corta con granularità fine, altrimenti i
   grafici mostrano rumore e non tendenze.

6. **Tetto massimo di contenuti e di spesa.** Quanti post, commenti e recensioni al
   massimo, in totale, e se c'è un limite di budget da non superare. È la domanda che
   evita la sorpresa in fattura ed è anche quella che tiene onesto il perimetro:
   con un tetto dichiarato bisogna scegliere quali fonti meritano i contenuti
   disponibili, invece di raccogliere tutto e decidere dopo.

   Proponi un tetto complessivo coerente con la profondità scelta, per esempio
   1.000, 3.000 o 10.000 contenuti, e un tetto per singola fonte, così una
   piattaforma prolissa non si mangia l'intero budget. Se l'utente non ha
   un'idea, usa i valori del livello di profondità come tetto e dillo.

   **Il tetto va rispettato anche quando i dati sono interessanti.** Se una fonte
   sta per sforare, fermati e chiedi, non proseguire perché "ne valeva la pena".

7. **Profondità.** Tre livelli, spiegati in termini di tempo e di costo, non di
   numero di chiamate. I volumi qui sotto sono il default se l'utente non fissa un
   tetto proprio:

| Livello | Tempi | Uso tipico | Volumi indicativi |
|---------|-------|-----------|-------------------|
| **Quick** | 10-15 min | demo, primo colpo d'occhio, pitch | circa 1.000 contenuti in tutto, 8-10 prompt LLM |
| **Standard** | 30-45 min | audit per un cliente, punto di partenza di un progetto | circa 3.000 contenuti, 20-25 prompt LLM |
| **Deep** | 1-2 ore | baseline di un monitoraggio, analisi competitiva seria | circa 10.000 contenuti, 40+ prompt LLM, competitor inclusi |

**Domande condizionali, da fare solo se pertinenti:**

- Ha punti vendita fisici? Se no, Google Maps vale poco e va escluso invece che
  raccolto per completezza. Dirlo all'utente è già un pezzo di analisi.
- Ha canali social attivi? Chiedi gli handle esatti di TikTok, Instagram e YouTube.
  Cercarli a tentoni brucia budget di scraping su profili sbagliati.
- Interessa cosa si dice **dentro** i video di terzi, e non solo nei commenti? Se sì,
  la raccolta include le trascrizioni: costa di più e vale quasi sempre la pena,
  perché il giudizio di uno youtuber pesa sul pubblico più di cento commenti.
- Ci sono temi che l'utente si aspetta di trovare? Serve a validare l'analisi, non
  a guidarla: se un tema atteso non emerge, è un risultato.

---

## Fase 2, piano di raccolta

Scrivi il piano in `output/<brand>-<YYYY-MM-DD>/audit-plan.md` e fattelo approvare
prima di lanciare qualsiasi raccolta. Il piano dice, per ciascuna fonte scelta:
perché è nel perimetro, quale attore o endpoint userai, quanti risultati, e la
stima di costo. Le fonti scartate vanno elencate con il motivo dello scarto, che
è informazione utile quanto le altre.

Per scegliere gli attori Apify e verificare che non abbiano un abbonamento
mensile leggi `references/apify-actors.md`. Per scegliere gli endpoint DataForSEO
e costruire la matrice dei prompt leggi `references/dataforseo-playbook.md`.

Sulla stima costi sii onesto e approssimativo per eccesso. Un audit Standard su un
brand con buon volume di conversazione sta tipicamente fra i tre e gli otto dollari
di crediti Apify più il consumo DataForSEO. Dare un ordine di grandezza sbagliato
per difetto è il modo più rapido per perdere la fiducia dell'utente alla prima
fattura.

---

## Fase 3, raccolta

Lancia le raccolte e salva ogni risposta grezza, senza rielaborarla, in
`output/<brand>-<data>/raw/`. Un file per fonte, nome parlante, formato originale
(JSON per i dataset, CSV dove l'attore lo produce già).

Questo è il punto in cui è forte la tentazione di leggere i dati, riassumerli al
volo e buttare via il resto. Non farlo: i grezzi sono metà del deliverable. Servono
a chi riceve il report per verificare una tua affermazione, e servono a te se fra
tre mesi l'utente vuole un confronto.

Regole di condotta durante la raccolta:

- **Procedi per fonte e riporta man mano.** Una riga per fonte completata, con il
  numero di item ottenuti. Se una fonte rende molto meno del previsto dillo subito:
  di solito significa handle sbagliato, perimetro troppo stretto o attore che ha
  cambiato comportamento.
- **Una fonte che fallisce non ferma l'audit.** Annota il fallimento, prosegui, e
  riportalo nella sezione metodologia del report. Un audit onesto con cinque fonti
  su sette vale più di un audit fermo.
- **Non raddoppiare la spesa per recuperare un buco.** Se Instagram rende poco,
  chiedi all'utente se vuole spendere ancora prima di rilanciare con volumi
  maggiori.
- **Rispetta il tetto dichiarato in fase 1.** Quando una fonte sta per sforare,
  fermati e chiedi. Il tetto è un impegno preso, non un suggerimento.
- **Raccogli solo contenuti pubblici** e non aggirare login, paywall o misure di
  protezione. Gli attori indicati lavorano tutti su contenuto pubblico.

### Due raccolte che vale la pena non saltare

**Lo storico delle menzioni negli LLM.** Le risposte che generi adesso descrivono
oggi e nient'altro. Per sapere com'era sei mesi fa servono gli endpoint storici
delle menzioni, che restituiscono l'andamento mensile e le variazioni periodo su
periodo. È l'unico pezzo di cronistoria che non puoi ricostruire a posteriori se
non lo raccogli ora, e alimenta direttamente la sezione cronistoria del report.
I dettagli sono in `references/dataforseo-playbook.md`.

**Le trascrizioni dei video di terzi.** I commenti sotto un video dicono cosa pensa
il pubblico, la trascrizione dice cosa gli è stato detto. Su molti brand il giudizio
di chi recensisce in video pesa più di centinaia di commenti, e finisce anche fra
le fonti che gli LLM citano. Raccogli le trascrizioni dei video di canali terzi,
non di quelli del brand, ed estrai i passaggi in cui il brand viene nominato con il
loro minutaggio. La procedura è in `references/apify-actors.md`.

---

## Fase 4, normalizzazione

Tutte le fonti confluiscono in un unico `data.json`, con lo schema documentato in
`references/report-spec.md`. È il file che alimenta il report e va costruito con
cura, perché ogni approssimazione fatta qui diventa un grafico sbagliato dopo.

Tre attenzioni che fanno la differenza:

- **Le date vanno normalizzate in ISO** e i contenuti senza data vanno marcati come
  tali, non attribuiti a oggi. Un grafico temporale costruito su date inventate è
  peggio di nessun grafico.
- **La lingua di ogni item va riconosciuta e registrata.** Su brand internazionali
  ti ritroverai conversazioni in cinque lingue e il sentiment va letto per lingua,
  perché le norme espressive cambiano.
- **Deduplica.** Lo stesso contenuto ricompare su fonti diverse, e contarlo due
  volte gonfia esattamente i temi più virali, che sono quelli su cui poi si
  prendono le decisioni.
- **Assegna ogni item al suo periodo.** Ogni contenuto datato va etichettato con il
  periodo della granularità scelta in fase 1, perché è quello a rendere possibile
  la cronistoria. Gli item senza data restano fuori dalle serie temporali e vengono
  contati a parte, mai spalmati sull'ultimo periodo per far quadrare i totali.

---

## Fase 5, analisi e report

L'analisi segue il framework in `references/analysis-framework.md`, che copre la
classificazione del sentiment, la tassonomia dei temi, la cronistoria, il calcolo
dello share of voice nelle risposte LLM, l'analisi delle trascrizioni video e la
mappa delle fonti citate.

**Non fermarti alla fotografia.** La parte che distingue un audit utile da uno
scaricabile da un tool è la cronistoria: come sono cambiati volume, sentiment e temi
lungo la finestra scelta, quali picchi ci sono stati e cosa li ha causati, quali temi
sono nati, cresciuti o spariti. Un cliente che legge "il 34 per cento dei giudizi è
negativo" alza le spalle. Uno che legge "era il 21 per cento a gennaio ed è il 34
per cento oggi, e la crescita è quasi tutta su un tema solo" prende il telefono.

Il report si costruisce con lo script, non a mano:

```bash
python3 scripts/build_report.py output/<brand>-<data>/data.json
```

Lo script inietta i dati nel template in `assets/report_template.html` e produce
`report.html`, un file unico che si apre con un doppio clic e si può mandare per
email. Non riscrivere l'HTML a mano a ogni audit: il template implementa già la
palette validata, i grafici, la modalità scura e le tabelle dei dati sotto ogni
grafico. Se serve una sezione che il template non prevede, passala in
`custom_sections` dentro `data.json` invece di modificare il template.

### Cosa consegni

```
output/<brand>-<YYYY-MM-DD>/
├── report.html          il report navigabile, autoconsistente
├── data.json            il dataset normalizzato che alimenta il report
├── audit-plan.md        il perimetro approvato in fase 2
├── METODOLOGIA.md       fonti, volumi, date di raccolta, limiti, fonti fallite
└── raw/                 le risposte grezze, una per fonte
    ├── serp_brand.json
    ├── llm_responses.json          le risposte generate adesso, con data e modello
    ├── llm_mentions_history.json   lo storico mensile delle menzioni
    ├── reddit.json
    ├── trustpilot.json
    ├── youtube_videos.json
    ├── youtube_transcripts.json    le trascrizioni dei video di terzi
    └── ...
```

`METODOLOGIA.md` non è un adempimento burocratico. È il file che rende l'audit
difendibile davanti a un cliente che chiede "da dove viene questo numero", ed è
anche quello che permette di ripetere l'analisi identica fra sei mesi.

---

## Regole che valgono per tutto l'audit

**Il sentiment è un segnale, non un verdetto.** Chi scrive una recensione o apre un
thread è autoselezionato e tipicamente più insoddisfatto della media dei clienti.
Riporta sempre il sentiment accanto al volume e alla fonte, mai come numero unico,
e non presentarlo mai come una percentuale di clienti soddisfatti.

**Distingui il rilevato dall'interpretato.** "Quarantadue recensioni su duecento
citano i tempi di spedizione" è un dato. "Il brand ha un problema di logistica" è
un'ipotesi che quel dato suggerisce. Nel report i due piani devono restare
visibilmente separati, perché il lettore deve poter dissentire dall'interpretazione
senza dover dubitare dei numeri.

**Attenzione ai dati personali.** Le recensioni e i commenti contengono nomi,
username e a volte dettagli personali. Nel report usa citazioni brevi e funzionali
all'analisi, senza nomi di privati cittadini, e tieni i dati identificativi nei
grezzi. Gli username pubblici di account aziendali o di creator sono un altro
discorso e si possono citare.

**Non produrre affermazioni diffamatorie.** La differenza è tutta nella
formulazione: "gli utenti in questi thread segnalano ritardi" si può scrivere,
"il brand spedisce in ritardo" no, a meno che il dato non lo dimostri in modo
inequivocabile. Vale doppio quando il report riguarda un brand che non è del
committente.

**Dichiara sempre la data di raccolta.** Le risposte degli LLM cambiano di
settimana in settimana, le SERP pure. Un audit senza data è inutilizzabile dopo un
mese e, peggio, può essere citato come attuale quando non lo è più.
