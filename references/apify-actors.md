# Scegliere gli attori Apify

## Indice

- [Il principio: validare, non fidarsi della lista](#il-principio-validare-non-fidarsi-della-lista)
- [I criteri di selezione](#i-criteri-di-selezione)
- [La procedura di scelta](#la-procedura-di-scelta)
- [Candidati per fonte](#candidati-per-fonte)
- [Volumi per livello di profondità](#volumi-per-livello-di-profondità)
- [Input tipici per categoria](#input-tipici-per-categoria)
- [Gestire una run](#gestire-una-run)

---

## Il principio: validare, non fidarsi della lista

Lo store di Apify cambia continuamente. Gli attori vengono deprecati, cambiano
nome, cambiano modello di prezzo. È già successo che attori storici passassero da
canone mensile a pagamento a consumo, e viceversa, da un giorno all'altro.

Per questo motivo **la lista di candidati qui sotto è un punto di partenza, non una
verità**. La regola operativa è: prendi il candidato, verificane pricing e stato con
gli strumenti del server MCP di Apify, e se non convince cerca un'alternativa. Il
costo di questa verifica è zero, il costo di una run su un attore sbagliato no.

Un audit che ogni volta ricontrolla gli attori invecchia molto meglio di uno che
ha gli identificativi scritti nel codice.

---

## I criteri di selezione

In ordine di importanza:

1. **Nessun canone mensile.** L'attore deve essere a consumo, cioè pagamento per
   risultato o per evento. Gli attori con affitto mensile sono esclusi anche se
   tecnicamente migliori, perché questa skill è pensata per essere usata da chiunque
   senza sottoscrivere abbonamenti.
2. **Manutenzione recente.** Un attore aggiornato negli ultimi mesi, con un numero
   di utilizzi significativo. Gli scraper di piattaforme social si rompono spesso, e
   uno abbandonato è uno che fallirà a metà raccolta.
3. **Costo per mille risultati ragionevole.** A parità di funzione, la forbice fra
   attori è ampia. Sotto il dollaro per mille risultati è economico, fra uno e tre
   è normale, sopra i cinque va giustificato.
4. **Copertura dei campi che servono.** Per l'analisi del sentiment servono almeno
   testo, data, autore e, dove esiste, valutazione numerica. Un attore velocissimo
   che restituisce solo conteggi non serve a niente.
5. **Un solo attore per più fonti, quando possibile.** Alcuni attori coprono più
   modalità con un solo input. Meno attori significano meno schemi di input da
   gestire e meno cose che si rompono.

---

## La procedura di scelta

Per ogni fonte del piano di raccolta:

1. Cerca gli attori disponibili per quella fonte con gli strumenti di ricerca del
   server MCP di Apify, partendo dal candidato indicato qui sotto.
2. Leggi i dettagli dell'attore: modello di prezzo, data dell'ultimo aggiornamento,
   schema di input.
3. Scarta subito chi ha canone mensile.
4. Fra i rimanenti scegli il più economico che copra i campi necessari.
5. Annota nel piano di raccolta quale attore hai scelto e quanto costa, così
   l'utente approva sapendo cosa paga.

Se nessun candidato è utilizzabile, dillo nel piano e proponi di escludere quella
fonte invece di ripiegare su un attore dubbio. Una fonte mancante dichiarata è un
limite. Una fonte raccolta male è un errore che si propaga in tutto il report.

---

## Candidati per fonte

Identificativi nella forma `utente/nome-attore`. Tutti i candidati principali erano
a consumo al momento della scrittura, ma **vanno comunque verificati** secondo la
procedura sopra.

### Recensioni Trustpilot

| Candidato | Note |
|-----------|------|
| `parsebird/trustpilot-reviews-scraper` | Recensioni più dati azienda, pagamento per risultato |
| `azzouzana/trustpilot-scraper` | Alternativa economica |
| `automation-lab/trustpilot` | Alternativa |

Input: l'URL della pagina Trustpilot del brand, oppure il dominio. Verifica di
avere preso la pagina del mercato giusto, perché Trustpilot ha profili separati per
paese e mescolarli falsa tutto.

### Recensioni Google Maps

| Candidato | Note |
|-----------|------|
| `compass/google-maps-reviews-scraper` | Il riferimento della categoria, pagamento per evento |
| `scrapesage/google-reviews-scraper` | Alternativa |

Input: URL dei luoghi, oppure una ricerca per nome più città. Per un brand con molti
punti vendita raccogli i primi dieci o quindici per traffico, non tutti: la
reputazione locale è abbastanza omogenea e il costo cresce in fretta.

**Se il brand non ha punti vendita fisici, salta questa fonte.** Dirlo all'utente
è un risultato dell'analisi, non una mancanza.

### Thread e commenti Reddit

| Candidato | Note |
|-----------|------|
| `trudax/reddit-scraper-lite` | Versione a consumo, post e commenti |
| `automation-lab/reddit-scraper` | Alternativa con ricerca |
| `harshmaur/reddit-scraper-pro` | Alternativa |

Attenzione: esiste una versione non Lite dello stesso autore che storicamente aveva
un canone mensile. Verifica sempre quale variante stai usando.

Input: query di ricerca con il nome del brand e le sue varianti, oppure elenco di
subreddit di settore. Raccogli i commenti, non solo i post: il valore sta lì, perché
il titolo di un thread dice l'argomento mentre i commenti dicono l'opinione.

### Post e commenti TikTok

| Candidato | Note |
|-----------|------|
| `clockworks/free-tiktok-scraper` | Più modalità in un attore solo, incluso profili e ricerca |
| `clockworks/tiktok-comments-scraper` | Specifico per i commenti |
| `apidojo/tiktok-comments-scraper` | Alternativa a consumo |

Input: handle del profilo del brand, hashtag di marca, oppure ricerca per parola
chiave. Su TikTok il contenuto di terzi che parla del brand conta più di quello del
brand stesso, quindi non limitarti al profilo ufficiale.

### Post e commenti Instagram

| Candidato | Note |
|-----------|------|
| `apify/instagram-scraper` | Ufficiale, copre post, reel, profili e commenti |
| `apify/instagram-comment-scraper` | Specifico per i commenti |
| `apidojo/instagram-scraper` | Alternativa più economica |

Input: URL del profilo o dei post, oppure hashtag. I commenti sotto i post del brand
raccontano il rapporto con la community, gli hashtag raccontano cosa ne fanno gli
altri.

### Video YouTube del canale del brand e commenti

| Candidato | Note |
|-----------|------|
| `streamers/youtube-scraper` | Video di un canale, ricerca, metadati |
| `streamers/youtube-comments-scraper` | Commenti dei video |
| `apidojo/youtube-scraper` | Alternativa a consumo |

Input: URL del canale per i video, poi gli URL dei video per i commenti. Prendi i
video più visti, non gli ultimi pubblicati: i commenti si accumulano nel tempo e i
video recenti ne hanno pochi.

### Video YouTube di terzi che citano il brand

Stessi attori, input diverso: una ricerca per nome del brand più termini come
recensione, opinioni, confronto, alternative, nella lingua del mercato. Poi i
commenti dei video più visti fra i risultati.

Questa fonte è quasi sempre la più sottovalutata e una delle più ricche, perché un
video di recensione con migliaia di commenti è una miniera di obiezioni reali,
espresse liberamente.

### Trascrizioni dei video di terzi

I commenti dicono cosa pensa il pubblico. La trascrizione dice **cosa gli è stato
detto**, ed è un'informazione diversa e spesso più pesante: il giudizio di chi
recensisce in video orienta migliaia di persone, finisce citato nelle risposte degli
LLM, e non compare da nessuna altra parte nell'audit.

| Candidato | Note |
|-----------|------|
| `tubelens/youtube-transcript-scraper` | Sottotitoli in blocco, a consumo |
| `scrape.badger/youtube-transcript-scraper` | Pagamento per evento |
| `myagizm/youtube-transcript-scraper` | Alternativa a consumo |
| `apihq/youtube-transcript-scraper` | Alternativa, restituisce JSON |

In alternativa, DataForSEO ha un endpoint per i sottotitoli di un video, utile
quando il server Apify non è disponibile o quando stai già lavorando lì.

**Come procedere:**

1. Parti dai video di terzi già individuati, ordinati per visualizzazioni, non per
   data. Un video di due anni fa con centomila visualizzazioni pesa sulla
   reputazione più di uno di ieri con duecento.
2. Escludi i video del canale del brand. Lì il brand parla di sé, e quello lo sai
   già: serve sapere cosa dicono gli altri.
3. Scarica le trascrizioni, che arrivano come testo con i minutaggi.
4. **Non leggere l'intera trascrizione come se fosse una recensione.** Un video di
   venti minuti su una categoria può nominare il brand per quaranta secondi. Cerca
   le occorrenze del nome del brand e delle sue varianti, ed estrai una finestra di
   contesto intorno a ciascuna, indicativamente trenta secondi prima e dopo, che è
   quanto serve per capire se ne sta parlando bene, male o di sfuggita.
5. Per ogni occorrenza registra: video, canale, visualizzazioni, minutaggio, il
   passaggio testuale, il sentiment e il tema. Il minutaggio serve a chi legge il
   report per andare a verificare in dieci secondi, ed è il dettaglio che rende
   questa sezione credibile.

**Quando la trascrizione non c'è.** Molti video non hanno sottotitoli utilizzabili,
soprattutto in italiano. Alcuni attori ripiegano sulla trascrizione automatica
dell'audio, che costa di più e va dichiarata: le trascrizioni automatiche sbagliano
i nomi propri, e il nome di un brand è esattamente un nome proprio. Prima di citare
un passaggio come prova, controlla che il nome sia trascritto correttamente e non sia
un'omofonia.

Volumi consigliati: 5 video per un audit Quick, 15 per uno Standard, 30 per un Deep,
scelti fra i più visti e non fra i più recenti.

### Scraping del sito e di pagine web

| Candidato | Note |
|-----------|------|
| `apify/website-content-crawler` | Crawler pensato per estrarre testo pulito |
| `apify/web-fetch` | Per singole pagine, veloce, rende Markdown |

Serve per due cose diverse. La prima è leggere come il brand si racconta, cioè home,
pagina chi siamo, pagine prodotto, FAQ, che è il termine di paragone per misurare il
gap con la percezione. La seconda è leggere le pagine di terzi che compaiono nelle
risposte degli LLM e nelle SERP, per capire cosa esattamente stiano dicendo.

---

## Volumi per livello di profondità

Numeri indicativi di item per fonte, da adattare al volume reale di conversazione
sul brand.

| Fonte | Quick | Standard | Deep |
|-------|-------|----------|------|
| Trustpilot | 100 | 500 | 2000 |
| Google Maps | 100 su 3 sedi | 500 su 10 sedi | 2000 su 20 sedi |
| Reddit | 100 commenti | 500 | 2000 |
| TikTok | 50 post + commenti dei top 5 | 200 + top 20 | 500 + top 50 |
| Instagram | 50 post + commenti dei top 5 | 200 + top 20 | 500 + top 50 |
| YouTube canale | top 5 video | top 20 | top 50 |
| YouTube terzi | top 5 video | top 15 | top 30 |
| Trascrizioni video terzi | 5 | 15 | 30 |
| Pagine sito | 10 | 30 | 100 |

**Questi numeri cedono il passo al tetto fissato dall'utente.** Se in fase di
briefing è stato dichiarato un tetto complessivo o per fonte, quello comanda: riduci
proporzionalmente, partendo dalle fonti meno rilevanti per le domande dell'audit, e
scrivi nel piano di raccolta quali volumi hai tagliato e perché.

Per un brand con poca conversazione questi numeri vanno abbassati, altrimenti si
paga per raschiare il fondo. Per un brand molto discusso conviene restringere il
periodo temporale invece di alzare i volumi: mille commenti dell'ultimo anno dicono
più di mille commenti pescati a caso su sei anni.

**L'orizzonte temporale va passato agli attori, non applicato dopo.** Quasi tutti
accettano un filtro di data o un ordinamento per recenza: usarlo significa pagare
solo per i contenuti che rientrano nella finestra. Raccogliere tutto e filtrare a
valle è lo stesso risultato a un costo molto più alto. Dove il filtro non esiste,
ordina per data e fermati quando esci dalla finestra.

**Per la cronistoria servono contenuti distribuiti, non solo recenti.** Se un attore
restituisce gli ultimi N in ordine di data, rischi di avere trecento contenuti tutti
dell'ultimo mese e nulla sul resto dell'anno, con una serie temporale che crolla a
zero solo perché non hai raccolto. Quando succede, raccogli per finestre successive,
per esempio un blocco per trimestre, e dichiara nel report come è stato campionato.

---

## Input tipici per categoria

Lo schema esatto va sempre letto dall'attore, perché cambia. Questi sono i campi
concettuali che quasi tutti gli attori di una categoria richiedono.

**Scraper di recensioni**: URL di partenza, numero massimo di recensioni, ordinamento
(preferisci il più recente), lingua, eventuale filtro per valutazione. Non filtrare
per valutazione in fase di raccolta: serve la distribuzione completa, e filtrare
solo le negative produce un audit che conferma qualunque tesi.

**Scraper social**: handle o URL del profilo, oppure hashtag o query, numero massimo
di post, se raccogliere anche i commenti e quanti per post. Il limite per post conta
più del limite totale: cento commenti su un post virale dicono meno di dieci
commenti su dieci post diversi.

**Scraper di ricerca**: query, numero di risultati, paese e lingua. Costruisci le
query con le varianti del nome del brand raccolte in fase di briefing, non solo con
il nome ufficiale.

**Crawler web**: URL di partenza, profondità, numero massimo di pagine, formato di
output. Chiedi Markdown o testo pulito, non HTML grezzo, perché il passaggio
successivo è un'analisi testuale.

---

## Gestire una run

- **Parti sempre da una run di prova con cinque risultati** su ogni attore nuovo.
  Verifichi lo schema di output e scopri gli input sbagliati spendendo centesimi.
- **Non lanciare tutte le fonti insieme alla cieca.** Procedi a blocchi, controlla
  l'esito, poi prosegui.
- **Se una run supera abbondantemente il tempo atteso**, fermala e abbassa i volumi.
  Un attore che impiega venti minuti per duecento risultati sta incontrando
  protezioni antibot e non migliorerà aspettando.
- **Salva l'output grezzo appena arriva**, prima di qualsiasi elaborazione. Se
  l'analisi va storta non vuoi ripagare la raccolta.
- **Annota il numero reale di item ottenuti per fonte.** Finisce in
  `METODOLOGIA.md` e serve a interpretare i grafici: una fonte con trenta item e una
  con duemila non pesano uguale, e il report deve dirlo.
