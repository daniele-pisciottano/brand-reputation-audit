# DataForSEO: SERP, LLM e menzioni

## Indice

- [Le due API generative, che non fanno la stessa cosa](#le-due-api-generative-che-non-fanno-la-stessa-cosa)
- [Quali strumenti servono](#quali-strumenti-servono)
- [Lo storico delle menzioni](#lo-storico-delle-menzioni)
- [La matrice dei prompt](#la-matrice-dei-prompt)
- [Quante volte ripetere un prompt](#quante-volte-ripetere-un-prompt)
- [Cosa estrarre da ogni risposta](#cosa-estrarre-da-ogni-risposta)
- [SERP e AI Overview](#serp-e-ai-overview)
- [Menzioni e contenuti](#menzioni-e-contenuti)
- [Location e lingua](#location-e-lingua)
- [Controllo dei costi](#controllo-dei-costi)

---

## Le due API generative, che non fanno la stessa cosa

Dentro il modulo AI Optimization ci sono due famiglie che è facile confondere e che
rispondono a due domande diverse. Usarle entrambe è quello che rende l'audit
completo, perché ciascuna copre il buco dell'altra.

**LLM Responses** interroga i modelli **adesso**, con i prompt che scrivi tu. È una
rilevazione controllata: decidi tu le domande, il modello, quante volte ripetere.
Ti dice cosa risponde oggi un modello a una domanda che ti interessa, ma non ti dice
niente di ieri, e quello che misuri oggi non sarà riproducibile domani.

**LLM Mentions** cerca dentro un archivio molto grande di prompt e risposte già
raccolte, dell'ordine delle centinaia di milioni, su ChatGPT e sugli AI Overview di
Google. Non scegli tu le domande, ma in cambio ottieni due cose che la prima non può
dare: un **volume di ricerca AI** confrontabile fra entità, e soprattutto lo
**storico**. È l'equivalente funzionale di uno strumento di brand monitoring
generativo, e vive dentro DataForSEO invece che in un abbonamento a parte.

La regola pratica:

| Domanda | Quale famiglia |
|---------|----------------|
| Cosa risponde un modello se chiedo esattamente questo | LLM Responses |
| Il brand compare su una domanda che ho scelto io | LLM Responses |
| Quanto è visibile il brand nelle risposte AI, in assoluto | LLM Mentions |
| Com'era sei mesi fa, sta crescendo o calando | LLM Mentions, endpoint storici |
| Quali domini e pagine vengono citati sul tema | LLM Mentions, top domains e top pages |
| Come sta il brand rispetto ai competitor sulle stesse metriche | LLM Mentions, metriche incrociate |

Un audit fatto solo con LLM Responses è una fotografia senza scala. Uno fatto solo
con LLM Mentions ha la scala e la storia ma non risponde alle domande specifiche
del cliente. Servono tutte e due.

---

## Quali strumenti servono

I nomi esatti degli strumenti dipendono dalla versione del server MCP e dai moduli
abilitati. Quelli qui sotto sono i nomi tipici: se non trovi una corrispondenza
esatta, cerca fra gli strumenti disponibili per funzione, non per nome.

| Serve per | Strumento tipico |
|-----------|------------------|
| Interrogare un LLM con un prompt | `ai_optimization_llm_response` |
| Sapere quali modelli sono disponibili | `ai_optimization_llm_models` |
| Interrogare ChatGPT con contesto di ricerca | `ai_optimization_chat_gpt_scraper` |
| Cercare menzioni di un brand nelle risposte degli LLM | `ai_opt_llm_ment_search` |
| Metriche aggregate sulle menzioni | `ai_opt_llm_ment_agg_metrics` |
| Domini più citati dagli LLM su un tema | `ai_opt_llm_ment_top_domains` |
| Pagine più citate dagli LLM | `ai_opt_llm_ment_top_pages` |
| Confronto fra più entità | `ai_opt_llm_ment_cross_agg_metrics` |
| SERP organica con AI Overview | `serp_organic_live_advanced` |
| Menzioni del brand nei contenuti web | `content_analysis_search` |
| Sintesi e sentiment delle menzioni | `content_analysis_summary` |
| Andamento delle frasi nel tempo | `content_analysis_phrase_trends` |
| Schede attività locali | `business_data_business_listings_search` |
| Ricerca e commenti su YouTube | `serp_youtube_organic_live_advanced`, `serp_youtube_video_comments_live_advanced` |
| Volumi di ricerca sulle query di brand | `kw_data_google_ads_search_volume` |
| Idee di query correlate al brand | `dataforseo_labs_google_keyword_suggestions` |
| Volume di ricerca AI su un termine | `ai_optimization_keyword_data_search_volume` |
| Località e lingue supportate dalle menzioni | `ai_opt_llm_ment_loc_and_lang` |
| Filtri disponibili sulle menzioni | `ai_optimization_llm_mentions_filters` |
| Sottotitoli e trascrizione di un video YouTube | `serp_youtube_video_subtitles_live_advanced` |

Prima di costruire una richiesta sulle menzioni, interroga lo strumento dei filtri:
restituisce i campi effettivamente filtrabili nella tua versione ed evita mezz'ora
persa a indovinare nomi di parametri.

---

## Lo storico delle menzioni

È il pezzo che alimenta la cronistoria del report, e l'unico che non si può
ricostruire dopo: se non lo raccogli oggi, fra sei mesi avrai comunque solo sei mesi
di storia.

Tre tipi di dato da chiedere, per il brand e per ogni competitor:

- **Storico mensile.** Conteggio delle menzioni e volume di ricerca AI mese per
  mese. L'archivio parte da una certa data, quindi non aspettarti anni di
  profondità: verifica da quando ci sono dati e dichiaralo nel report invece di
  presentare una serie che comincia dove comincia l'archivio come se fosse l'inizio
  della storia del brand.
- **Variazione periodo su periodo.** Le differenze fra un periodo e il successivo,
  che è quello che serve davvero per raccontare una tendenza. Una serie di conteggi
  assoluti dice poco, la sua derivata dice tutto.
- **Menzioni nuove e perse.** Dove il brand ha guadagnato o perso presenza. Le perse
  sono la parte più interessante e quella che nessuno guarda.

Due accortezze:

- **Confronta sempre con i competitor sullo stesso periodo.** Un calo del quindici
  per cento è un problema se i concorrenti crescono, ed è stagionalità se calano
  tutti. Senza il confronto non si può distinguere fra i due casi, e si rischia di
  far partire un piano per risolvere un inverno.
- **Le metriche dell'archivio e quelle che misuri tu con i prompt non sono la
  stessa cosa** e non vanno sommate né messe nello stesso grafico. Nel report vivono
  in due blocchi distinti, ciascuno con la sua etichetta.

---

## La matrice dei prompt

È il cuore della parte generativa dell'audit e l'errore più comune è costruirla
male, cioè chiedere solo cose che nominano il brand. Se nomini sempre il brand
scopri soltanto cosa il modello sa dirti quando glielo chiedi, e non scopri mai la
cosa che conta davvero: **se il brand esiste nella testa del modello quando nessuno
lo nomina.**

Cinque famiglie, e servono tutte e cinque.

### A. Scoperta senza brand

Query di categoria in cui il brand non compare. Misurano se il brand viene tirato
fuori spontaneamente.

- "quali sono i migliori [categoria prodotto] nel 2026"
- "cosa mi consigli per [bisogno che il prodotto risolve]"
- "dove conviene comprare [categoria] online"
- "[categoria] per [segmento di pubblico specifico]"

**Cosa misuri**: se il brand compare, in che posizione dell'elenco, con quali
aggettivi, e quali concorrenti compaiono al suo posto. È lo share of voice
generativo, la metrica singola più utile di tutto l'audit.

### B. Confronto senza brand

- "[competitor 1] o [competitor 2], quale scegliere"
- "alternative a [competitor più forte]"

**Cosa misuri**: se il brand viene proposto come alternativa credibile a chi è già
nella considerazione dell'utente. Un brand che non compare mai qui ha un problema di
presenza nelle fonti, non di prodotto.

### C. Conoscenza del brand

- "cos'è [brand]"
- "chi c'è dietro [brand], di quale gruppo fa parte"
- "cosa vende [brand] e a che prezzi"
- "[brand] dove spedisce e in quanto tempo"

**Cosa misuri**: accuratezza. Qui si trovano le informazioni sbagliate, obsolete o
inventate, ed è il materiale che convince un cliente più di qualunque grafico.
Confronta sempre quello che il modello dice con quello che il sito dice davvero:
**ogni scostamento va registrato come errore fattuale con la sua fonte probabile.**

### D. Fiducia e obiezioni

- "[brand] è affidabile"
- "ci sono problemi noti con [brand]"
- "[brand] recensioni negative, di cosa si lamentano i clienti"
- "conviene comprare da [brand] o è meglio evitare"

**Cosa misuri**: quali obiezioni il modello riporta e da dove le prende. Queste
risposte sono quelle che un potenziale cliente legge prima di comprare, quindi hanno
un impatto commerciale diretto.

Attenzione a come riporti i risultati di questa famiglia: stai registrando cosa dice
un modello, non stai accertando un fatto sul brand. La formulazione nel report deve
renderlo evidente.

### E. Confronto con brand

- "[brand] o [competitor], quale è meglio"
- "alternative a [brand]"
- "perché scegliere [brand] invece di [competitor]"

**Cosa misuri**: il posizionamento relativo e i criteri con cui il modello
differenzia. Spesso emergono criteri che il brand non presidia nella propria
comunicazione, ed è un'indicazione diretta per il piano contenuti.

### Come distribuire i prompt

| Famiglia | Quick | Standard | Deep |
|----------|-------|----------|------|
| A. Scoperta senza brand | 3 | 7 | 12 |
| B. Confronto senza brand | 1 | 3 | 6 |
| C. Conoscenza del brand | 2 | 5 | 8 |
| D. Fiducia e obiezioni | 2 | 5 | 8 |
| E. Confronto con brand | 2 | 5 | 8 |

Le famiglie A e B insieme dovrebbero pesare circa il quaranta per cento del totale.
Se pesano meno, l'audit sta guardando allo specchio invece che al mercato.

---

## Quante volte ripetere un prompt

Le risposte degli LLM non sono deterministiche: lo stesso prompt può nominare il
brand una volta su tre. Una singola esecuzione produce un sì oppure un no che non
descrive la realtà.

- **Quick**: una esecuzione per prompt, e nel report va dichiarato che il dato è
  indicativo.
- **Standard e Deep**: tre esecuzioni per prompt, e il risultato si riporta come
  **frequenza di menzione**, per esempio due su tre, non come presenza o assenza.

Se sono disponibili più modelli, distribuisci i prompt su almeno due, perché i
modelli attingono a fonti diverse e un brand può essere forte su uno e assente
sull'altro. È un'informazione strategica, non un dettaglio tecnico.

---

## Cosa estrarre da ogni risposta

Per ogni esecuzione di ogni prompt, registra sempre questi campi, perché sono
quelli che poi alimentano i grafici del report:

- Il testo completo della risposta, che va nei grezzi
- **Se il brand è menzionato** e in quale posizione rispetto agli altri
- **Quali altri brand sono menzionati**, in ordine di apparizione
- **Quali fonti o domini sono citati**, che è il campo più importante di tutti
- Gli aggettivi e i giudizi associati al brand
- Eventuali **affermazioni fattuali verificabili**, da confrontare con il sito
- Modello usato, data e ora dell'esecuzione

Il campo delle fonti citate è quello che trasforma l'audit in un piano operativo. Se
su dieci prompt di categoria ricorrono sempre gli stessi sei domini e il brand non
è presente su nessuno di quei sei, quei sei domini sono la lista di lavoro per i
prossimi tre mesi. Questo è il passaggio in cui l'analisi della reputazione si
salda con la SEO e con la digital PR.

---

## SERP e AI Overview

Raccogli tre gruppi di query, nella lingua e nel paese del mercato scelto:

1. **Brand puro**: il nome del brand e le sue varianti. Serve a vedere chi controlla
   la prima pagina, se ci sono risultati ostili e quali profili terzi compaiono.
2. **Brand più modificatore**: recensioni, opinioni, problemi, reclami, alternative,
   codice sconto, truffa, funziona. Sono le query che fa chi sta decidendo se
   fidarsi, e la prima pagina di queste query è la reputazione vera del brand.
3. **Categoria senza brand**: le stesse query usate nella famiglia A dei prompt.
   Servono a confrontare la SERP tradizionale con la risposta generativa, e lo
   scarto fra le due è uno dei risultati più interessanti da mostrare.

Per ogni SERP registra chi occupa le prime dieci posizioni, la presenza e il
contenuto dell'AI Overview, e quali domini vengono citati come fonte dall'AI
Overview. Quell'ultimo elenco va incrociato con le fonti citate dagli LLM: la
sovrapposizione fra i due insiemi è la mappa delle fonti che contano davvero.

---

## Menzioni e contenuti

Gli strumenti di content analysis trovano le citazioni del brand nei contenuti web
indicizzati e ne restituiscono una valutazione di sentiment aggregata. Servono a
due cose: dare un volume di menzioni confrontabile nel tempo, e trovare i contenuti
influenti che non erano emersi dalle SERP.

Tratta il sentiment restituito da questi strumenti come un indicatore grossolano, da
confrontare con quello che ricavi dalle recensioni e dai commenti. Se i due divergono
molto, la divergenza è essa stessa un risultato da indagare, non un errore da
nascondere facendo una media.

---

## Location e lingua

Quasi tutti gli endpoint richiedono un codice di località e uno di lingua. Sbagliarli
è l'errore più costoso, perché produce dati plausibili ma riferiti al mercato
sbagliato, e l'errore si scopre solo alla fine.

- Risolvi sempre il codice località con lo strumento apposito prima di lanciare la
  raccolta, non a memoria.
- Verifica che le località supportate per gli strumenti generativi coincidano con
  quelle degli strumenti SERP, perché non sempre lo sono.
- Se il brand opera su più mercati, ripeti l'intero blocco per ciascun mercato e
  tieni i risultati separati fino alla fase di confronto.

---

## Controllo dei costi

- Parti sempre da una chiamata singola per verificare formato e credenziali.
- Le SERP costano poco, gli strumenti generativi molto di più, e le ripetizioni si
  moltiplicano in fretta: tre esecuzioni per quaranta prompt su due modelli sono
  duecentoquaranta chiamate.
- Se il budget stringe, taglia sulle ripetizioni dei prompt delle famiglie C ed E
  prima che su quelle della famiglia A, perché la scoperta senza brand è la parte
  che non si può ricostruire in altro modo.
- Registra il numero di chiamate effettuate per tipo e mettilo in `METODOLOGIA.md`,
  così il costo di un eventuale monitoraggio ricorrente è prevedibile.
