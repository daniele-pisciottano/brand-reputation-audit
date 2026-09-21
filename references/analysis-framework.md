# Framework di analisi

Come si passa da qualche migliaio di righe di testo raccolto a qualcosa che una
persona può leggere e usare.

## Indice

- [Il principio: tre piani separati](#il-principio-tre-piani-separati)
- [Sentiment](#sentiment)
- [Tassonomia dei temi](#tassonomia-dei-temi)
- [Cronistoria](#cronistoria)
- [Cosa si dice dentro i video](#cosa-si-dice-dentro-i-video)
- [Share of voice generativo](#share-of-voice-generativo)
- [La mappa delle fonti](#la-mappa-delle-fonti)
- [Il gap fra racconto e percezione](#il-gap-fra-racconto-e-percezione)
- [Confronto con i competitor](#confronto-con-i-competitor)
- [Dalle evidenze alle raccomandazioni](#dalle-evidenze-alle-raccomandazioni)
- [Come marcare l'incertezza](#come-marcare-lincertezza)

---

## Il principio: tre piani separati

Ogni cosa che finisce nel report appartiene a uno di tre piani, e mescolarli è il
modo più rapido per rendere un audit incontestabile e quindi inutile.

1. **Rilevato.** Numeri e citazioni. "Su 480 recensioni Trustpilot raccolte il 12
   febbraio, 103 citano i tempi di consegna."
2. **Interpretato.** Cosa quei numeri suggeriscono. "La consegna è il primo motivo
   di insoddisfazione dichiarata, davanti al prezzo."
3. **Raccomandato.** Cosa farne. "Presidiare le query su tempi e costi di spedizione
   con una pagina dedicata, oggi assente."

Il lettore deve poter dissentire dal piano tre senza dover mettere in dubbio il
piano uno. Nel report i tre piani hanno una resa visiva diversa, ed è il template a
occuparsene, ma sta a te tenere le affermazioni nel piano giusto.

---

## Sentiment

### Come classificare

Classifica ogni item su tre valori, positivo, neutro, negativo, più un quarto valore
"misto" per i contenuti che dicono bene di una cosa e male di un'altra, che sono
tanti e che schiacciati su neutro spariscono.

Tre accortezze che cambiano il risultato:

- **La valutazione numerica non è il sentiment.** Una recensione da tre stelle su
  cinque può essere entusiasta con un appunto, o distruttiva con una concessione.
  Dove esiste un voto numerico, registralo come campo separato e usalo come
  controllo incrociato: se voto e sentiment divergono spesso, la classificazione
  ha un problema.
- **Classifica nella lingua originale.** Tradurre prima di classificare perde
  ironia, modi di dire e intensità. Registra la lingua di ogni item e, dove i volumi
  lo permettono, riporta il sentiment anche per lingua.
- **Il sarcasmo è la trappola classica.** Su Reddit e TikTok una parte non piccola
  dei commenti positivi in apparenza sono ironici. Se un item è ambiguo, marcalo
  come incerto invece di forzarlo: una quota dichiarata di non classificati è un
  segno di serietà, non una lacuna.

### Come riportarlo

Sempre e solo insieme a tre informazioni: la **fonte**, il **volume** e la
**finestra temporale**. Un sentiment aggregato su tutte le fonti è un numero che
non descrive niente, perché Trustpilot e Reddit hanno popolazioni e norme
completamente diverse.

Non presentare mai il sentiment come percentuale di clienti soddisfatti. Chi scrive
è autoselezionato e sistematicamente più polarizzato della base clienti. La
formulazione corretta parla di contenuti raccolti, non di persone.

---

## Tassonomia dei temi

Il passaggio che dà più valore al report, e anche l'unico che non si può
automatizzare del tutto.

**Procedura:**

1. Leggi un campione trasversale di almeno cento item, presi da tutte le fonti, non
   solo dalla più abbondante.
2. Fai emergere i temi dal materiale, non da una lista preconfezionata. Una lista
   calata dall'alto trova quello che si aspetta e manca proprio le sorprese, che
   sono il motivo per cui si fa l'audit.
3. Arriva a un numero di temi fra sei e dodici. Meno di sei significa che stai
   appiattendo, più di dodici che il report diventa illeggibile.
4. Definisci ogni tema in una riga, con due o tre citazioni esemplificative che ne
   chiariscano i confini.
5. Classifica tutti gli item, ammettendo temi multipli per item e una categoria
   residua "altro" che non deve superare il quindici per cento.

**Per ogni tema riporta:** volume assoluto, quota sul totale, distribuzione per
fonte, sentiment prevalente, andamento nel tempo se i dati lo permettono, e le
citazioni più rappresentative.

L'incrocio tema per fonte è quasi sempre la tabella più interessante dell'intero
report, perché mostra che lo stesso brand ha problemi diversi a seconda di dove lo
si ascolta.

---

## Cronistoria

Una fotografia dice com'è il brand oggi. Un cliente questo di solito lo sa già,
almeno per sensazione. Quello che non sa, e che lo fa muovere, è **come ci è
arrivato e in che direzione sta andando**. La cronistoria è la parte dell'audit che
risponde a questo, ed è quella che nessun export di tool produce da solo.

### Le quattro serie da costruire

1. **Volume nel tempo, per fonte.** La base. Serve a capire quando si è parlato di
   più del brand, ma da sola non dice niente sul segno di quella conversazione.
2. **Sentiment nel tempo.** La quota di negativi, positivi e misti periodo per
   periodo. Riportala come **quota percentuale**, non come conteggio, altrimenti
   confondi un aumento di negatività con un aumento di volume, che sono due
   fenomeni completamente diversi. Affianca comunque il volume assoluto, perché una
   quota calcolata su dodici contenuti non è un dato.
3. **Temi nel tempo.** Quanto pesa ciascun tema in ogni periodo. È qui che si vede
   la cosa più utile di tutte: un tema che nasce, uno che cresce, uno che sparisce.
   Limita a cinque temi per non rendere il grafico illeggibile e raccogli il resto
   sotto una voce residua.
4. **Visibilità negli LLM nel tempo.** Dallo storico delle menzioni, non dai prompt
   eseguiti oggi. Tieni questa serie in un blocco separato dalle altre tre, perché
   misura una cosa diversa e con una metrica diversa.

### Come si legge, e come non si legge

**Le percentuali su basi piccole mentono.** Sotto i trenta contenuti in un periodo,
non calcolare quote: riporta il conteggio e marca il periodo come poco popolato.
Un balzo dal dieci al quaranta per cento su sette contenuti non è una tendenza, sono
tre commenti.

**Distingui i picchi di volume dai cambi di tendenza.** Un picco è un evento: un
video virale, una promozione andata male, una notizia. Un cambio di tendenza è una
pendenza che si mantiene su più periodi. Il primo si spiega, il secondo si affronta,
e confonderli porta a piani d'azione sbagliati.

**Ogni picco va spiegato o dichiarato inspiegato.** Quando una serie ha un massimo
evidente, vai a leggere i contenuti di quel periodo e scrivi cosa è successo. Se non
riesci a stabilirlo, scrivi che non è stato possibile: è comunque meglio di un
grafico con una montagna e nessuna didascalia.

**Attenzione all'artefatto di raccolta.** Se la serie crolla nell'ultimo periodo,
prima di annunciare un calo di interesse verifica che non sia solo il periodo
ancora in corso, o che l'attore non abbia restituito meno dati per quella finestra.
È l'errore più frequente e il più imbarazzante da correggere davanti a un cliente.

**Normalizza il primo e l'ultimo periodo.** Se la finestra comincia a metà di un
mese e finisce a metà di un altro, quei due periodi hanno meno giorni degli altri e
sembreranno più bassi. O li escludi dai confronti, o li riporti in media
giornaliera, ma non li lasci lì come se fossero confrontabili.

### Il racconto, non solo i grafici

Chiudi la sezione con cinque o sei righe che raccontano il periodo a parole,
ancorate ai numeri: da dove si partiva, cosa è cambiato e quando, cosa è rimasto
uguale, dove si sta andando se la tendenza continua. Se in fase di briefing è emersa
una data spartiacque, misura esplicitamente il prima e il dopo su volume, sentiment
e composizione dei temi.

È la parte del report che la gente legge per prima e cita nelle riunioni, e vale la
pena scriverla con cura invece di lasciare che i grafici parlino da soli.

---

## Cosa si dice dentro i video

I commenti sotto un video sono il pubblico. La trascrizione è chi ha in mano il
microfono, e pesa in modo sproporzionato: orienta migliaia di persone, resta online
per anni, e spesso è fra le fonti che gli LLM leggono per costruire la loro idea del
brand.

**Analizza le occorrenze, non i video.** Un video di venti minuti sulla categoria
può nominare il brand per quaranta secondi. L'unità di analisi è il passaggio in cui
il brand viene nominato, con una finestra di contesto intorno, non il video intero.

Per ciascuna occorrenza stabilisci:

- **In che ruolo compare il brand.** È il soggetto del video, uno dei termini di
  paragone, o una citazione di passaggio. Sono tre pesi diversi.
- **Il giudizio espresso**, con le stesse categorie del resto dell'audit, più il
  valore misto, che qui è frequentissimo perché chi recensisce tende a bilanciare.
- **Il tema toccato**, dalla stessa tassonomia usata per le altre fonti. Solo così
  i video entrano nei conteggi per tema invece di restare un'appendice.
- **Il peso del canale**, cioè visualizzazioni del video e ordine di grandezza degli
  iscritti. Un giudizio negativo su un canale da mezzo milione di iscritti non vale
  come lo stesso giudizio su uno da mille.

**Confronta il detto con il commentato.** L'incrocio più interessante di questa
sezione è fra quello che dice chi presenta e quello che rispondono i commenti sotto
lo stesso video. Quando divergono, per esempio uno youtuber entusiasta con i commenti
che lo smentiscono, hai trovato qualcosa che nessun'altra fonte dell'audit può
mostrare.

**Cita sempre con il minutaggio.** Chi legge il report deve poter verificare in
dieci secondi. È anche la tutela contro l'errore più insidioso di questa fonte: le
trascrizioni automatiche sbagliano i nomi propri, e un brand è un nome proprio.
Prima di usare un passaggio come prova, controlla che il nome sia davvero quello e
non un'omofonia inventata dal riconoscimento vocale.

---

## Share of voice generativo

Sui prompt delle famiglie A e B, cioè quelli che non nominano il brand:

```
share of voice = menzioni del brand / esecuzioni totali dei prompt senza brand
```

Calcolalo anche per ciascun competitor, sugli stessi prompt, così il numero ha un
termine di paragone. Poi scomponilo su due assi che dicono cose diverse:

- **Per famiglia di prompt.** Un brand può essere forte sulle query di scoperta e
  assente su quelle di confronto, e sono due problemi diversi.
- **Per modello**, se ne hai usati più di uno. Le differenze fra modelli sono spesso
  marcate e indicano quali ecosistemi di fonti stanno funzionando.

Riporta anche la **posizione media nell'elenco** quando il brand viene menzionato.
Essere citato sempre per ultimo su dieci è un risultato diverso dall'essere citato
raramente ma per primo.

---

## La mappa delle fonti

È la parte più azionabile dell'audit e quella che nessun tool standard restituisce.

1. Raccogli tutti i domini citati dagli LLM nelle risposte, con la frequenza.
2. Aggiungi i domini citati come fonte dagli AI Overview.
3. Aggiungi i domini che occupano le prime posizioni sulle query di brand più
   modificatore.
4. Unisci tutto in un'unica classifica per frequenza.
5. Per ciascun dominio in cima alla classifica segna: il brand è presente, è
   presente ma male, oppure è assente.

Il risultato è una lista di priorità concreta. I domini frequenti dove il brand è
assente sono obiettivi di digital PR. Quelli dove è presente ma raccontato male sono
obiettivi di gestione della reputazione, spesso più urgenti e più economici da
sistemare.

---

## Il gap fra racconto e percezione

Estrai dalle pagine del sito le cinque o sei promesse principali del brand, quelle
che compaiono in home, nelle pagine prodotto e nel chi siamo. Poi verifica, per
ciascuna, cosa dicono le conversazioni raccolte.

Tre esiti possibili, tutti e tre interessanti:

- **Confermata**: il brand promette una cosa e gli utenti la riconoscono. È un
  asset, va difeso e usato di più.
- **Contraddetta**: il brand promette una cosa e gli utenti dicono il contrario. È
  il rischio più grosso, perché la promessa attira proprio le persone che resteranno
  deluse.
- **Assente**: il brand promette una cosa di cui nessuno parla. Di solito significa
  che la promessa non è rilevante per il pubblico, oppure che non arriva.

Il caso più frequente e meno atteso è il quarto, speculare: **gli utenti apprezzano
qualcosa che il brand non rivendica affatto**. È quasi sempre la raccomandazione
più facile da implementare di tutto il report.

---

## Confronto con i competitor

Non serve un audit completo per ciascun competitor, sarebbe sproporzionato. Servono
tre confronti mirati:

- **Share of voice generativo** sugli stessi prompt, già calcolato sopra.
- **Sentiment e volume** sulla fonte di recensioni principale, che è il confronto
  più immediato da leggere.
- **Temi**: quali problemi sono specifici del brand e quali invece sono di
  categoria. È una distinzione che cambia le conclusioni: se tutti i concorrenti
  hanno lo stesso problema di spedizione, quel tema è un costo di settore, e
  risolverlo diventa un vantaggio competitivo invece che un recupero di terreno.

---

## Dalle evidenze alle raccomandazioni

Ogni raccomandazione del report deve avere tre attributi, altrimenti non entra:

1. **L'evidenza che la sostiene**, richiamata esplicitamente, con il numero.
2. **Chi la esegue e con quale leva**: contenuti, digital PR, prodotto, servizio
   clienti, presidio di una piattaforma.
3. **Una stima di impatto e sforzo**, anche solo alta, media, bassa.

Ordinale per rapporto fra impatto e sforzo, non per gravità del problema. Un audit
che si chiude con quindici azioni tutte importanti non fa agire nessuno. Da cinque
a otto raccomandazioni sono il formato giusto.

Distingui sempre le azioni realizzabili entro un mese da quelle strutturali: chi
riceve il report deve poter cominciare da qualcosa lunedì.

---

## Come marcare l'incertezza

L'audit poggia su campioni non probabilistici e su modelli che cambiano risposta nel
tempo. Dirlo apertamente rafforza il documento, non lo indebolisce.

- **Volumi bassi**: sotto i cinquanta item per fonte, la fonte si riporta con una
  nota esplicita e non si usa per confronti percentuali.
- **Fonti mancate**: vanno elencate con il motivo, non omesse.
- **Risposte degli LLM**: sempre con data, modello e numero di esecuzioni.
- **Contenuti senza data**: contati a parte e mai inclusi nei grafici temporali.
- **Item non classificabili**: dichiarati come quota, non redistribuiti d'ufficio
  sulle altre categorie.

La domanda di controllo, prima di consegnare: se un cliente contestasse il numero
più scomodo del report, avrei i grezzi e la metodologia per difenderlo in cinque
minuti? Se la risposta è no, quel numero non è pronto.
