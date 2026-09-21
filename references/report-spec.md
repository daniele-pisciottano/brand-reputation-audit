# Specifica del report e schema di `data.json`

Il report si genera sempre con lo script, mai scrivendo HTML a mano:

```bash
python3 scripts/build_report.py output/<brand>-<data>/data.json
```

Lo script legge `data.json`, lo inietta dentro `assets/report_template.html` e
scrive `report.html` accanto al file dati. Il risultato è un file unico, senza
dipendenze locali, che si apre con un doppio clic e si può allegare a una mail.

Con `--open` lo apre anche nel browser, con `--out` si sceglie un percorso diverso.

---

## Perché uno schema fisso

Il template disegna solo quello che trova. **Ogni blocco è facoltativo**: se manca
`llm`, la sezione sulle risposte generative non compare e la navigazione si accorcia
da sola. Questo permette di usare lo stesso template per un audit Quick con tre
fonti e per un Deep con nove, senza toccare una riga di codice.

La conseguenza pratica è che l'unica cosa che devi fare bene è `data.json`. Se un
grafico esce storto, il problema è quasi sempre nei dati, non nel template.

---

## Schema

```jsonc
{
  "meta": {
    "brand": "Nome del brand",              // obbligatorio
    "domain": "brand.it",
    "market": "Italia",
    "language": "it",                        // lingua del report
    "depth": "standard",                     // quick | standard | deep
    "collected_at": "2026-09-21",            // obbligatorio, data della raccolta
    "period": { "from": "2025-09-01", "to": "2026-09-21" },
    "competitors": ["Competitor 1", "Competitor 2"],
    "questions": ["Le domande approvate in fase di briefing"],
    "author": "Chi firma il report",
    "accent": "#E52217",                     // colore di accento, facoltativo
    "logo": "https://.../logo.svg",          // facoltativo: se manca, quello Moca
    "logo_dark": "https://.../logo-light.svg" // variante per il fondo scuro
    // meta.logo = false toglie del tutto il logo dalla testata
  },

  "summary": {
    "headline": "Una frase sola che dice la cosa più importante emersa",
    "bullets": ["3-5 punti, uno per riga, ciascuno con il suo numero dentro"],
    "kpis": [
      { "label": "Contenuti analizzati", "value": "2.847", "note": "su 6 fonti",
        "tone": "neutral" }                  // neutral | good | warning | critical
    ]
  },

  "sources": [
    { "id": "trustpilot", "name": "Trustpilot", "items": 480,
      "period": "ultimi 12 mesi", "status": "ok", "note": "" }
    // status: ok | partial | failed | skipped
    // le fonti saltate o fallite vanno incluse: il perché è informazione
  ],

  // Alimenta due sezioni: il grafico del sentiment per fonte e, insieme a
  // sources e ai temi, l'intera vista "Canale per canale". I nomi qui devono
  // combaciare con sources[].name e con le chiavi di themes[].by_source.
  "sentiment_by_source": [
    { "source": "Trustpilot", "positive": 210, "neutral": 80,
      "negative": 170, "mixed": 20, "unclassified": 0 }
  ],

  // Facoltativo: arricchisce la scheda di un canale nella vista per canale.
  // Senza questo blocco la scheda si costruisce comunque da sola.
  "channels": [
    { "name": "Trustpilot", "note": "Nota specifica per questo canale" }
  ],

  "volume_over_time": {
    "unit": "month",                         // month | week | day
    "points": [
      { "date": "2026-01", "by_source": { "Trustpilot": 40, "Reddit": 22 } }
    ]
  },

  // La cronistoria: come sono cambiati sentiment, temi e visibilita' negli LLM.
  // E' la sezione che distingue un audit da un export, quindi vale la pena
  // riempirla anche quando i dati sono imperfetti, dichiarando le imperfezioni.
  "timeline": {
    "unit": "month",
    "narrative": "Cinque o sei righe che raccontano il periodo a parole, ancorate ai numeri.",
    "sentiment": [
      { "date": "2026-01", "total": 120, "positive": 40, "neutral": 30,
        "negative": 42, "mixed": 8, "sparse": false }
      // sparse: true sui periodi con meno di 30 contenuti, dove le quote non reggono
    ],
    "themes": [
      { "name": "TEMPI DI CONSEGNA",
        "points": [ { "date": "2026-01", "volume": 30, "share": 0.25 } ] }
      // al massimo 5 temi, il resto va aggregato sotto "Altri temi"
    ],
    "milestones": [
      { "date": "2026-03", "kind": "picco", "label": "Etichetta breve",
        "explanation": "Cosa e' successo, o che non e' stato possibile stabilirlo" }
      // kind: picco | svolta | evento | artefatto
    ],
    "llm_visibility": {
      "metric": "menzioni mensili",          // come si chiama cio' che stai contando
      "note": "Dall'archivio delle menzioni, non dai prompt eseguiti oggi",
      "points": [
        { "date": "2026-01", "by_entity": { "Il brand": 120, "Competitor 1": 210 } }
      ]
    }
  },

  "themes": [
    {
      "name": "TEMPI DI CONSEGNA",
      "definition": "Una riga che dice cosa ci sta dentro e cosa no",
      "volume": 103,
      "share": 0.21,                         // quota sul totale classificato
      "sentiment": { "positive": 5, "neutral": 10, "negative": 85, "mixed": 3 },
      "by_source": { "Trustpilot": 70, "Reddit": 25, "YouTube": 8 },
      "quotes": [
        { "text": "Citazione breve e testuale", "source": "Trustpilot",
          "date": "2026-03-04", "sentiment": "negative" }
      ]
    }
  ],

  "llm": {
    "models": ["modello-1", "modello-2"],
    "runs_per_prompt": 3,
    "share_of_voice": [
      { "entity": "Il brand", "mentions": 14, "runs": 30, "share": 0.47,
        "avg_position": 3.2, "is_brand": true },
      { "entity": "Competitor 1", "mentions": 22, "runs": 30, "share": 0.73,
        "avg_position": 1.8 }
    ],
    "by_family": [
      { "family": "Scoperta senza brand", "brand_share": 0.40, "runs": 21 }
    ],
    "facts": [
      { "claim": "Cosa afferma il modello", "verdict": "errato",
        "reality": "Cosa dice davvero il sito", "source_guess": "dominio.com",
        "prompt": "Il prompt che l'ha prodotta" }
      // verdict: corretto | impreciso | errato | obsoleto
    ],
    "objections": [
      { "text": "L'obiezione riportata dal modello", "frequency": 7,
        "cited_sources": ["dominio1.com", "dominio2.com"] }
    ]
  },

  // Cosa si dice DENTRO i video di canali terzi, dalle trascrizioni.
  // L'unita' e' l'occorrenza in cui il brand viene nominato, non il video.
  "video_mentions": {
    "videos_analysed": 15,
    "occurrences": 42,
    "note": "Come sono stati scelti i video e come sono state ottenute le trascrizioni",
    "items": [
      { "video_title": "Titolo del video", "channel": "Nome del canale",
        "url": "https://...", "views": 120000, "published": "2026-02-14",
        "role": "confronto",                 // soggetto | confronto | citazione
        "timestamp": "07:12",
        "quote": "Il passaggio testuale, verbatim dalla trascrizione",
        "sentiment": "negative",
        "theme": "TEMPI DI CONSEGNA",
        "divergence": "Facoltativo: se i commenti sotto il video dicono altro" }
    ]
  },

  "sources_map": [
    { "domain": "dominio.com", "llm_citations": 18, "aio_citations": 4,
      "serp_positions": 6, "total": 28, "brand_status": "assente", "note": "" }
    // brand_status: presente | parziale | assente
  ],

  "gap": [
    { "promise": "La promessa estratta dal sito", "verdict": "contraddetta",
      "evidence": "Il dato che lo mostra", "items": 103 }
    // verdict: confermata | contraddetta | assente | non_rivendicata
  ],

  "competitors": [
    { "name": "Competitor 1", "sov": 0.73, "sentiment_negative": 0.22,
      "review_volume": 1200, "note": "" }
  ],

  "methodology": {
    "notes": ["Come sono stati raccolti e classificati i dati"],
    "limits": ["I limiti dichiarati, uno per riga"],
    "failed_sources": [{ "source": "Instagram", "reason": "Perché" }],
    "calls": { "dataforseo": 240, "apify_runs": 9 },
    "cost_estimate": "Ordine di grandezza della spesa",
    "cap": { "requested": 3000, "collected": 1800,
             "note": "Il tetto concordato e quanto e' stato effettivamente raccolto" }
  },

  "custom_sections": [
    { "title": "TITOLO IN MAIUSCOLO", "html": "<p>HTML già pronto</p>" }
  ]
}
```

---

## Regole per riempirlo bene

**I numeri devono tornare.** La somma dei valori di sentiment di una fonte deve dare
il numero di item dichiarato per quella fonte in `sources`. Il lettore attento lo
verifica, e un totale che non quadra fa cadere la fiducia su tutto il resto.

**Le citazioni devono essere testuali.** Non riassumere una recensione dentro
`quotes`, copiala. Se è lunga, taglia con dei puntini di sospensione invece di
riscriverla. Niente nomi di privati cittadini.

**Non inventare mai campi per riempire una sezione.** Se non hai i dati per
`volume_over_time`, ometti il blocco: il report si adatta. Una sezione costruita su
stime inventate è il modo peggiore di far bella figura.

**Il campo `share` va espresso da 0 a 1**, non in percentuale: il template formatta.

**Massimo cinque voci** in `sentiment_by_source`, in `share_of_voice` e nelle serie
di `volume_over_time`, `timeline.themes` e `timeline.llm_visibility`. La palette ha
cinque colori validati e non si cicla: se hai più voci, aggrega le minori sotto
"Altre fonti" o "Altri temi", che resta leggibile. L'elenco dei temi nella sezione
dedicata non ha questo limite, perché usa una scala di intensità e non colori
diversi.

**Nella cronistoria marca i periodi poco popolati.** Metti `sparse: true` su ogni
periodo con meno di trenta contenuti: il template lo segnala e chi legge sa che
quella quota non regge. Un periodo con sette contenuti che passa dal dieci al
quaranta per cento di negativi non è una tendenza, sono tre commenti.

**Le percentuali della cronistoria si calcolano sul periodo**, non sul totale
dell'audit, altrimenti la serie racconta la distribuzione della raccolta invece che
il cambiamento del sentiment.

**Le sezioni pesanti stanno in fondo.** Riepilogo, temi, canali e risposte generative
sono la parte che la gente legge. Mappa delle fonti, confronto competitor e
metodologia sono quella che si va a controllare. L'ordine del template rispetta già
questo criterio.

**La vista per canale non si compila.** Si costruisce da sola incrociando
`sentiment_by_source`, `sources` e la ripartizione `by_source` dei temi, e pesca le
citazioni dai temi filtrandole per fonte. L'unica cosa che devi fare è **scrivere i
nomi dei canali sempre allo stesso modo** nei tre blocchi: "YouTube" in uno e
"Youtube" nell'altro producono un canale fantasma e uno vuoto. Lo script lo
segnala, ma è più semplice non sbagliarlo.

---

## Personalizzare l'aspetto

Il template usa il carattere Figtree e una palette di accento che si cambia in un
punto solo, nel blocco `:root` in cima al file. Per adattarlo ai colori di un
cliente basta modificare le variabili di accento, oppure passare `meta.accent` nel
JSON, che ha la precedenza.

**I colori delle serie nei grafici non vanno cambiati a cuor leggero.** Sono stati
verificati per leggibilità e per distinguibilità in caso di daltonismo, sia in
modalità chiara sia in quella scura. Se li sostituisci con i colori di un brand,
rivalidali prima invece di fidarti dell'occhio.

Il carattere viene caricato dal web con una sequenza di ripiego solida. Se il report
deve funzionare offline in modo garantito, incorpora il carattere in base64 nel
blocco di stile, sostituendo la riga di importazione.
