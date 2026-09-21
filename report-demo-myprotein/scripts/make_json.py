import json
from collections import Counter
it=[x for x in json.load(open('../raw/items_classified.json')) if x['pertinent']]
allit=json.load(open('../raw/items_classified.json'))
themes=json.load(open('../raw/themes.json'))
Q={
'CONSEGNA E CORRIERE':[("Lento, farraginoso, tempo biblici, difficoltà di tracciamento degli articoli, lentezza nella consegna.","Trustpilot","2026-09-02","negative"),
  ("Azienda seria, con prodotti decisamente buoni anche se non da 5 stelle. Prezzi eccellenti e servizio di spedizione molto veloce.","Trustpilot","2026-03-27","positive"),
  ("Dopo 20 giorni senza spedizione mi viene offerto solo il rimborso. È il minimo previsto per legge, non un servizio.","Instagram","2026-04-24","negative")],
'PREZZO E SCONTI':[("Grumi ovunque, sapore chimico e la meccanica \"prezzo gonfiato a 130 e scontato al 50%+\" è proprio subdola.","Trustpilot","2026-05-29","negative"),
  ("se in passato il rapporto qualità prezzo era ottimo, ora è nella norma. Oggi acquisto solo in occasione di sconti importanti, altrimenti scelgo altri brand.","Trustpilot","2025-11-15","mixed"),
  ("Pagare 50€ al kg per le myprotein lo trovo onestamente folle, allo stesso prezzo prenderesti delle iso fuji che sono infinitamente migliori","Reddit","2026-08-03","negative")],
'QUALITÀ E SCADENZE':[("Articolo inviato con soltanto 2 mesi di validità prima della scadenza! Più della metà dovrò buttarlo!","Trustpilot","2026-01-29","negative"),
  ("Acquisto Myprotein da anni, ottimo rapporto qualità prezzo, buoni prodotti!!","Trustpilot","2026-07-10","positive"),
  ("Myprotein (come Bulk) ormai fa i kitkat e i biscotti, altro che fitness...","YouTube","","negative")],
'ASSISTENZA, RESI E RIMBORSI':[("Fate di tutto per rendere difficile fare il reso e oltretutto quest'ultimo è anche a carico del ricevente...","Trustpilot","2026-04-23","negative"),
  ("Ero cliente fisso, poi un giorno il corriere non ha effettuato la consegna e dall' azienda non ho avuto alcun supporto, ho scritto diverse mesi ma non ho risolto nulla. Addio!!","Trustpilot","2026-04-20","negative"),
  ("hanno un assistenza che fa pena","Instagram","2026-06-04","negative")],
'PACCO E IMBALLAGGIO':[("La confezione era sul fondo del cartone, schiacciata e non protetta dal pluriball. La chiusura salva freschezza non funziona","Trustpilot","2026-02-14","negative"),
  ("Un barattolo di burro di arachidi crunchy è arrivato aperto e con il contenuto fuori dal barattolo, aveva impronte di dita, per cui è stato aperto.","Trustpilot","2026-03-28","negative"),
  ("Spedizione veloce ma creatina arrivata con tappo spaccato.fortunatamente la pellicola di sicurezza interna era intatta.I prodotti sono ottimi","Trustpilot","2026-04-24","mixed")],
'GUSTO E CONSISTENZA':[("Per me il sapore delle proteine è troppo chimico. Non buono. Mi dispiace tanto ma per me è così.","Trustpilot","2026-03-24","mixed"),
  ("Il sapore delle proteine è buono, ho preso la referenza cioccolato arancia. La confezione è da migliorare...","Trustpilot","2026-02-25","mixed"),
  ("consumavo le MyProtein clear, avevo acquistato tipo 4 barattoli ed era diventato un inferno finirle, uno schifo dopo l'altro (vari gusti presi per via di una super offerta).","Reddit","2026-09-20","negative")],
'ORDINE ERRATO O INCOMPLETO':[("È la terza volta che mi inviano il prodotto del gusto sbagliato.","Trustpilot","2026-09-20","negative"),
  ("Durante l'ordine se volevo degli omaggi dovevo incrementare la spesa. Così ho fatto e gli omaggi non sono arrivati.","Trustpilot","2026-01-14","negative"),
  ("Facile da ordinare, corrispondente alla descrizione e con un omaggio.","Trustpilot","2026-02-26","positive")],
'GIUDIZIO GENERALE':[("Non è la prima volta che ordino, ma ogni volta mi trovo bene. Ottimi prodotti e ottimo servizio.","Trustpilot","","positive"),
  ("Sono cliente Myprotein e mi trovo bene.","YouTube","","positive"),
  ("Mai più comprerò un prodotto da voi","Instagram","2026-07-29","negative")],
'SITO, APP E PAGAMENTO':[("Il pagamento non è chiaro e spesso induce a sbagliare ritrovandosi con una spesa superiore","Trustpilot","2026-04-19","negative"),
  ("Buoni prodotti ma il loro circuito di pagamento un disastro. Identifica come flaggate carte prepagate impedendo di completare l'ordine.","Trustpilot","2026-03-05","negative"),
  ("Ho ordinato diverse volte sul sito. I prodotti sono di ottima qualità e il gusto delle proteine è fantastico. Spedizione veloce e prezzi onesti.","Trustpilot","2026-09-17","positive")],
'COMPETITOR E ALTERNATIVE':[("HSN. Rapporto qualità prezzo migliore attualmente. E hanno anche le analisi certificate.","Reddit","2026-09-08","neutral"),
  ("Prima compravo da MyProtein, quest'anno sono passato a Bulk","Reddit","2025-03-23","negative"),
  ("Anche io utilizzo i prodotti di myprotein da 3 anni, ma ormai ho lasciato tutto meno che l'abbigliamento o i dolcificanti","YouTube","","negative")],
'CREATOR E SPONSOR':[("IL DISLIKE È DI MYPROTEIN","YouTube","","negative"),
  ("Perché alla fine della fiera è stato proprio grazie a te che mi sono affiliato a questo brand e mensilmente acquisto i loro prodotti","YouTube","","positive")],
'ABBIGLIAMENTO':[("L'abbigliamento è di altissima qualità. Uso leggins e shorts ed entrambi sono comodi durante l'allenamento, splendida vestibilità...","Trustpilot","","positive"),
  ("Ho acquistato il completo shorts e top, le cuciture, sia di uno che dell'altro, sono letteralmente esplose la prima volta che li ho indossati","Trustpilot","2026-06-10","negative")],
'ASSORTIMENTO':[("Prodotti fantastici e vasto assortimento sia di proteine e sia di vitamine","Trustpilot","","positive"),
  ("Prezzi schizzati alle stelle e assortimento sempre minore","Trustpilot","2026-03-21","neutral")],
}
for t in themes:
    t['quotes']=[dict(text=a,source=b,date=c,sentiment=d) for a,b,c,d in Q[t['name']]]
sbs={}
for s in ['Trustpilot','Instagram','YouTube','Reddit']:
    c=Counter(x['sentiment'] for x in it if x['source']==s)
    sbs[s]=dict(source=s,positive=c['positive'],neutral=c['neutral'],negative=c['negative'],mixed=c['mixed'],unclassified=0)
raw=Counter(x['source'] for x in allit)
cnt={s:sum(1 for x in it if x['source']==s) for s in sbs}
print(cnt,raw)
data={
"meta":{"brand":"Myprotein","domain":"myprotein.it","market":"Italia","language":"it","depth":"quick","collected_at":"2026-09-21",
 "period":{"from":"2025-09-21","to":"2026-09-21"},"competitors":["Prozis","Bulk","Foodspring","Yamamoto Nutrition"],
 "questions":["Di cosa si lamentano davvero i clienti","Myprotein compare negli LLM quando si chiede la categoria senza nominarlo","Quali fonti costruiscono la percezione del brand agli occhi degli LLM","Che distanza c'è fra come il brand si racconta e come viene raccontato"],
 "author":"Moca Interactive"},
"summary":{
 "headline":"Negli AI Overview italiani Myprotein ha 268 menzioni, più di tre volte Yamamoto (82). Ma non compare nella top 10 di Google per \"migliori proteine whey\", e la sua reputazione si divide in due: chi ha già comprato si lamenta della logistica, chi sta valutando se comprare si lamenta del prezzo.",
 "bullets":[
  "Nelle risposte di ChatGPT e Perplexity a domande di categoria (senza nominare il brand) Myprotein compare in 7 risposte su 8, quasi sempre al primo posto. L'unica assenza è la domanda più commerciale: \"migliori whey 2026\" su ChatGPT, dove la risposta elenca solo prodotti Bulk.",
  "Nelle recensioni Trustpilot da 1-2 stelle (89) i temi principali riguardano il dopo-acquisto: assistenza, resi e rimborsi in 36, consegna in 31, pacco danneggiato in 23, ordine sbagliato o incompleto in 21. Il prezzo compare in 20.",
  "Su Reddit e sui social, dove parla chi sta ancora valutando se comprare, i temi più citati sono prezzo e alternative: 31 contenuti su 75 toccano prezzo o passaggio ad altri brand. HSN è l'alternativa proposta più spesso, e gli sconti \"fino al -50%\" non vengono percepiti come veri.",
  "Myprotein risponde al 98% delle recensioni Trustpilot (234 su 239). Però 157 risposte sono identiche ad almeno un'altra, e le recensioni positive ricevono risposta dopo circa 5 giorni, contro le 16 ore di quelle negative.",
  "Quattro delle pagine di classifica più citate da LLM e AI Overview (Project inVictus, BestBody, TrovaIntegratori, Farmacia Loreto) non nominano mai Myprotein. BestBody e TrovaIntegratori citano invece Yamamoto."],
 "kpis":[
  {"label":"Contenuti pertinenti analizzati","value":"314","note":"su 837 raccolti in 5 fonti social e recensioni","tone":"neutral"},
  {"label":"Menzioni negli AI Overview Italia","value":"268","note":"Yamamoto 82, Bulk 80, Prozis 31, Foodspring 0","tone":"good"},
  {"label":"Presenza nelle risposte LLM di categoria","value":"7 su 8","note":"ChatGPT gpt-5.4 e Perplexity sonar-pro, 1 esecuzione per prompt","tone":"good"},
  {"label":"Top 10 Google sulle query di categoria","value":"1 su 3","note":"assente su \"migliori proteine whey\" e \"proteine in polvere migliori marche\"","tone":"warning"},
  {"label":"Trustpilot myprotein.it","value":"4,4","note":"su 28.714 recensioni, dato della SERP del 21/09/2026","tone":"good"},
  {"label":"Risposte Trustpilot con testo duplicato","value":"67%","note":"157 su 234 risposte identiche ad almeno un'altra","tone":"warning"}]},
"sources":[
 {"id":"trustpilot","name":"Trustpilot","items":cnt['Trustpilot'],"period":"set 2025 - set 2026","status":"partial","note":"Campione stratificato: fino a 50 recensioni italiane per ogni valore di stelle (2 stelle: 39). Non riflette la distribuzione reale delle stelle, quindi le quote di sentiment di questa fonte non vanno lette come media dei clienti."},
 {"id":"instagram","name":"Instagram","items":cnt['Instagram'],"period":"ultimi 50 post di @myproteinit","status":"partial","note":"%d commenti raccolti (solo gli ultimi visibili per post), %d pertinenti al brand. La maggior parte sono emoji o complimenti ai creator."%(raw['Instagram'],cnt['Instagram'])},
 {"id":"youtube","name":"YouTube","items":cnt['YouTube'],"period":"video 2016-2025, date dei commenti approssimate","status":"ok","note":"11 video (5 del canale MyproteinIT e 6 di terzi, i più visti), %d commenti raccolti, %d pertinenti. Trascrizioni dei 6 video di terzi analizzate a parte."%(raw['YouTube'],cnt['YouTube'])},
 {"id":"reddit","name":"Reddit","items":cnt['Reddit'],"period":"feb 2025 - set 2026","status":"ok","note":"r/ItalyFitness: 5 thread su Myprotein negli ultimi 12 mesi, più 2 thread del 2025 citati da Perplexity. r/gymitalia_ senza risultati."},
 {"id":"tiktok","name":"TikTok","items":0,"period":"2023 - set 2026","status":"partial","note":"75 post (profilo @myprotein globale in inglese e hashtag) e %d commenti dei 5 video italiani di terzi più visti: nessun commento pertinente al brand, parlano dei contenuti del creator."%raw['TikTok']},
 {"id":"llm","name":"Risposte LLM","items":21,"period":"21/09/2026","status":"ok","note":"10 prompt su ChatGPT gpt-5.4 con web search e Perplexity sonar-pro, 1 esecuzione (E2 su ChatGPT ripetuto due volte)."},
 {"id":"aio","name":"Archivio AI Overview","items":268,"period":"archivio DataForSEO, senza storico","status":"partial","note":"Metriche aggregate Italia per brand e competitor. ChatGPT non disponibile per l'Italia in questo archivio."},
 {"id":"serp","name":"SERP Google.it","items":10,"period":"21/09/2026","status":"ok","note":"Top 10 organici su 10 query: brand, brand con modificatori, confronto, categoria."},
 {"id":"gmaps","name":"Google Maps","items":0,"period":"","status":"skipped","note":"Nessun punto vendita fisico in Italia."},
 {"id":"facebook","name":"Facebook","items":0,"period":"","status":"skipped","note":"Escluso dal perimetro Quick per contenere la spesa."}],
"sentiment_by_source":list(sbs.values()),
"channels":[
 {"name":"Trustpilot","note":"Campione stratificato per stelle: il sentiment dipende dal campionamento. Qui conta la composizione dei temi per fascia di voto, non la quota di negativi."},
 {"name":"Instagram","note":"Sotto i post del brand i commenti pertinenti sono pochi (16) e quasi tutti negativi: prezzo, spedizioni ferme, assistenza. Instagram viene usato come canale per i reclami."},
 {"name":"YouTube","note":"I commenti pertinenti si concentrano su due video del 2019-2020 in cui dei creator annunciano l'addio a Myprotein come sponsor."},
 {"name":"Reddit","note":"Conversazione orientata alla scelta del brand: prezzo al kg e alternative. HSN è l'alternativa più proposta."}],
"timeline":{
 "unit":"month",
 "narrative":"La cronistoria in questo audit Quick è parziale, e va detto subito. Il campione Trustpilot è stratificato per stelle (50 per voto, raccolte a ritroso dalla più recente), quindi una serie mensile del sentiment rifletterebbe il campionamento e non la realtà: le 5 stelle coprono solo da giugno 2026, le 1 stella da febbraio. L'archivio delle menzioni AI non ha uno storico disponibile. L'unica serie affidabile è il volume di ricerca Google su \"myprotein\": 33.100 ricerche a settembre 2025, picchi di 60.500 a novembre (Black Friday) e a gennaio, poi un calo fino a 27.100 a luglio e agosto 2026, il 18% sotto settembre 2025. Nello stesso periodo i thread Reddit sul prezzo si concentrano fra agosto e settembre 2026 (\"prezzo folle sui 50 euro al kg\"). La coincidenza fra calo delle ricerche e malumore sul prezzo è un'ipotesi da verificare con un campione Trustpilot continuo, non un risultato.",
 "milestones":[
  {"date":"2025-11","kind":"picco","label":"Black Friday","explanation":"Le ricerche di brand raddoppiano: da 33.100 a 60.500. Su Reddit c'è chi dice di comprare le scorte per l'anno durante il Black Friday."},
  {"date":"2026-01","kind":"picco","label":"Buoni propositi","explanation":"Nuovo picco di 60.500 ricerche, legato alla stagionalità di inizio anno nel fitness."},
  {"date":"2026-07","kind":"svolta","label":"Minimo delle ricerche","explanation":"27.100 ricerche a luglio e ad agosto, il valore più basso della finestra. Una parte del calo è stagionale estiva: senza lo storico degli anni precedenti non si può stabilire quanta."},
  {"date":"2026-08","kind":"evento","label":"Thread Reddit sul prezzo","explanation":"Due thread su r/ItalyFitness (3 agosto e 8 settembre) mettono il prezzo delle whey Myprotein al centro e propongono HSN come alternativa."},
  {"date":"2026-09","kind":"evento","label":"Risultati semestrali THG","explanation":"Fra le fonti citate da Perplexity compaiono articoli sui risultati semestrali 2026 di THG, che attribuiscono la crescita al rebranding di Myprotein. Non verificato nel dettaglio in questo audit."}]},
"themes":themes,
"llm":{
 "models":["ChatGPT gpt-5.4 (web search)","Perplexity sonar-pro"],"runs_per_prompt":1,
 "share_of_voice":[
  {"entity":"Myprotein","mentions":7,"runs":8,"share":0.875,"avg_position":1.43,"is_brand":True},
  {"entity":"Bulk","mentions":5,"runs":8,"share":0.625,"avg_position":2.2},
  {"entity":"Yamamoto","mentions":3,"runs":8,"share":0.375,"avg_position":4.0},
  {"entity":"Prozis","mentions":1,"runs":8,"share":0.125,"avg_position":2.0},
  {"entity":"Foodspring","mentions":0,"runs":8,"share":0.0}],
 "by_family":[
  {"family":"A. Scoperta senza brand","brand_share":0.833,"runs":6},
  {"family":"B. Confronto senza brand","brand_share":1.0,"runs":2},
  {"family":"C. Conoscenza del brand","brand_share":1.0,"runs":4},
  {"family":"D. Fiducia e obiezioni","brand_share":1.0,"runs":4},
  {"family":"E. Confronto con brand","brand_share":1.0,"runs":5}],
 "facts":[
  {"claim":"Spedizione standard 4-7 giorni lavorativi, 4,99 euro sotto 55, gratis da 55. Oppure: spedizione tracciabile da 1,99 euro, 2-5 giorni, gratis sopra 50.","verdict":"impreciso","reality":"Entrambe le versioni sono sul sito: la pagina delivery-information dice 4-7 giorni e soglia 55, la pagina international-delivery (riga ITALY) dice da 1,99 euro, 2-5 giorni, soglia 50. È il sito a essere incoerente, e i due modelli riportano tutte e due le versioni.","source_guess":"myprotein.it/c/new-delivery/international-delivery","prompt":"Myprotein quanto ci mette a spedire in Italia e quanto costa la spedizione?"},
  {"claim":"Reso entro 30 giorni, costo del reso 10,69 euro con DHL.","verdict":"corretto","reality":"Confermato dalla pagina returns-policy.","source_guess":"myprotein.it/c/customer-services/returns-policy","prompt":"Myprotein o Prozis, quale è meglio?"},
  {"claim":"Myprotein fa parte di THG plc, nel gruppo dal 2011, nata nel 2004.","verdict":"corretto","reality":"Coerente con le pagine about-us e thg.com.","source_guess":"thg.com, us.myprotein.com","prompt":"Cos'è Myprotein e di quale gruppo fa parte?"},
  {"claim":"Stabilimento principale certificato BRCGS AA, prodotti Informed Sport, Informed Choice e Informed Protein.","verdict":"corretto","reality":"Confermato dalla pagina qualità (stabilimento di Warrington, BRCGS AA Grade). ChatGPT usa questa pagina per preferire Myprotein a Prozis, perché di Prozis trova solo le pagine sui resi.","source_guess":"myprotein.it/c/about-us/quality","prompt":"Myprotein o Prozis, quale è meglio?"},
  {"claim":"Trustpilot 4,4 su oltre 27.000 recensioni.","verdict":"corretto","reality":"4,4 su 28.714 alla data della raccolta.","source_guess":"it.trustpilot.com","prompt":"Myprotein è affidabile?"},
  {"claim":"Negli USA il profilo BBB mostra diversi reclami e alcune mancate risposte.","verdict":"impreciso","reality":"Riguarda il mercato statunitense: il modello lo usa per rispondere a una domanda italiana. Non verificato.","source_guess":"bbb.org","prompt":"Myprotein è affidabile?"}],
 "objections":[
  {"text":"Ritardi di consegna, pacchi fermi o non consegnati, poco coordinamento con il corriere","frequency":4,"cited_sources":["it.trustpilot.com","myprotein.it"]},
  {"text":"Assistenza clienti lenta o poco risolutiva","frequency":4,"cited_sources":["it.trustpilot.com"]},
  {"text":"Resi e rimborsi percepiti come macchinosi","frequency":3,"cited_sources":["it.trustpilot.com","myprotein.it"]},
  {"text":"Gusto, solubilità o qualità peggiorati o variabili da prodotto a prodotto","frequency":3,"cited_sources":["myprotein.it (recensioni prodotto)","it.trustpilot.com"]},
  {"text":"Pacchi danneggiati o arrivati aperti","frequency":1,"cited_sources":["it.trustpilot.com"]},
  {"text":"Prezzi molto aumentati rispetto al passato","frequency":1,"cited_sources":["myprotein.it (recensioni Impact Whey)"]},
  {"text":"Reclami BBB negli Stati Uniti","frequency":1,"cited_sources":["bbb.org"]}]},
"video_mentions":{
 "videos_analysed":6,"occurrences":7,
 "note":"I 6 video italiani di terzi più visti fra le ricerche \"myprotein recensione/opinioni/vs prozis\", con sottotitoli automatici in italiano scaricati via yt-dlp. I sottotitoli storpiano il nome (\"My proten\", \"mai pronti in\", \"m protein\"): le citazioni sono testuali, con il nome come trascritto. I due video di categoria più visti del 2025 (Project inVictus, 69mila visualizzazioni, e Alan Valca, 90mila) non nominano mai Myprotein.",
 "items":[
  {"video_title":"PROTEINE TUTTI I GUSTI +1 | Recensione EPICA W/ Marco Sarcone","channel":"Michael Spampinato","url":"https://www.youtube.com/watch?v=_3acKpG18xs&t=44","views":132663,"published":"2016-10-19","role":"soggetto","timestamp":"00:44","quote":"mi hanno chiesto tipo 246 volte di fare tipo una mezza recensione dei prodotti e dei gusti più che altro delle impact Way cioè delle proteine di My proten","sentiment":"neutral","theme":"GUSTO E CONSISTENZA"},
  {"video_title":"PROTEINE TUTTI I GUSTI +1 | Recensione EPICA W/ Marco Sarcone","channel":"Michael Spampinato","url":"https://www.youtube.com/watch?v=_3acKpG18xs&t=557","views":132663,"published":"2016-10-19","role":"soggetto","timestamp":"09:17","quote":"questo è in assoluto però uno dei gusti più buoni di che ho provato di m protein","sentiment":"positive","theme":"GUSTO E CONSISTENZA","divergence":"I commenti sotto il video parlano quasi solo dei due presentatori, non dei prodotti."},
  {"video_title":"LASCIO MYPROTEIN | TUTTA LA VERITA'","channel":"Giulio Ramazio","url":"https://www.youtube.com/watch?v=STsPe8r_ba8&t=349","views":76325,"published":"2020-02-29","role":"soggetto","timestamp":"05:49","quote":"secondo me in termini di qualità prezzo ma è una delle migliori compagnie di integratori soprattutto perché è studente magari non avete un budget pazzesco il fatto che fanno tanti sconti","sentiment":"positive","theme":"PREZZO E SCONTI"},
  {"video_title":"LASCIO MYPROTEIN | TUTTA LA VERITA'","channel":"Giulio Ramazio","url":"https://www.youtube.com/watch?v=STsPe8r_ba8&t=382","views":76325,"published":"2020-02-29","role":"soggetto","timestamp":"06:22","quote":"mai pronti in aveva questa gamma vastissima di prodotti e ogni 2 3 mesi magari facendo dei lanci di nuovi prodotti [...] non credevo cento per cento nel prodotto perché magari non c'era abbastanza ricerca scientifica","sentiment":"mixed","theme":"QUALITÀ E SCADENZE","divergence":"Il creator resta positivo sul brand, ma tra i commenti ci sono attacchi diretti: \"IL DISLIKE È DI MYPROTEIN\", e c'è chi scrive che ormai fa \"i kitkat e i biscotti\"."},
  {"video_title":"LASCIO MYPROTEIN | TUTTA LA VERITA'","channel":"Giulio Ramazio","url":"https://www.youtube.com/watch?v=STsPe8r_ba8&t=437","views":76325,"published":"2020-02-29","role":"soggetto","timestamp":"07:17","quote":"secondo me mai provata che rimane comunque qualità prezzo la migliore scelta a mio parere","sentiment":"positive","theme":"PREZZO E SCONTI"},
  {"video_title":"VLOG02| HO ABBANDONATO MYPROTEIN...","channel":"Mattia Martorelli","url":"https://www.youtube.com/watch?v=2ZwwkOHmnR0&t=27","views":19466,"published":"2019-12-09","role":"soggetto","timestamp":"00:27","quote":"ho cambiato semplicemente perché avevo ricevuto un'offerta migliore","sentiment":"neutral","theme":"CREATOR E SPONSOR","divergence":"Il nuovo sponsor è Foodspring. Nei commenti Foodspring viene definita \"di qualità decisamente superiore\", ma più cara."},
  {"video_title":"LE ANALISI DELLE PROTEINE MYPROTEIN!","channel":"Bodybuilding-natural.com","url":"https://www.youtube.com/watch?v=zDejmupnl0E&t=40","views":32833,"published":"2016-09-27","role":"soggetto","timestamp":"00:40","quote":"ho fatto analizzare tre pacchi di proteine le ho portate allo Zoff profilattico di Roma un ente Sanitario Nazionale Affinché si potesse vedere la quantità di proteine contenute in quei pacchi","sentiment":"positive","theme":"QUALITÀ E SCADENZE","divergence":"Il video difende le proteine economiche, ma nei commenti c'è chi contesta le analisi: \"indica il contenuto proteico ma non il profilo aminoacidico\"."}]},
"sources_map":[
 {"domain":"myprotein.it","llm_citations":15,"aio_citations":268,"serp_positions":8,"total":291,"brand_status":"presente","note":"Sito ufficiale. Le pagine più citate dagli AI Overview sono articoli di allenamento di The Zone, non pagine di prodotto."},
 {"domain":"youtube.com","llm_citations":0,"aio_citations":252,"serp_positions":6,"total":258,"brand_status":"parziale","note":"Canale brand presente, ma i video di categoria più visti del 2025 non nominano Myprotein."},
 {"domain":"my-personaltrainer.it","llm_citations":1,"aio_citations":108,"serp_positions":5,"total":114,"brand_status":"presente","note":"L'articolo \"Prodotti Myprotein sicuri?\" è del 2020 ed esce su 5 query di brand."},
 {"domain":"instagram.com","llm_citations":0,"aio_citations":91,"serp_positions":2,"total":93,"brand_status":"presente","note":"@myproteinit, 174mila follower."},
 {"domain":"projectinvictus.it","llm_citations":1,"aio_citations":72,"serp_positions":2,"total":75,"brand_status":"assente","note":"La guida \"Le 6 migliori proteine in polvere\" non nomina alcun brand: ragiona per tipologia."},
 {"domain":"facebook.com","llm_citations":0,"aio_citations":60,"serp_positions":3,"total":63,"brand_status":"presente","note":"Il comunicato del 2017 su una \"notizia falsa\" esce ancora su \"myprotein truffa\" e \"scandalo myprotein\"."},
 {"domain":"it.trustpilot.com","llm_citations":6,"aio_citations":0,"serp_positions":7,"total":13,"brand_status":"presente","note":"Due profili: www.myprotein.it (4,4 su 28.714) e myprotein.com (4,3 su 222.700)."},
 {"domain":"darwin-nutrition.fr","llm_citations":1,"aio_citations":32,"serp_positions":2,"total":35,"brand_status":"parziale","note":"Primo risultato su \"migliori proteine whey\". Nomina Myprotein, ma i primi posti vanno a Nutri&Co, AM Nutrition e Nutripure."},
 {"domain":"bestbody.it","llm_citations":2,"aio_citations":28,"serp_positions":2,"total":32,"brand_status":"assente","note":"La classifica non nomina Myprotein, mentre cita Yamamoto Iso-Fuji."},
 {"domain":"trovaintegratori.it","llm_citations":4,"aio_citations":0,"serp_positions":0,"total":4,"brand_status":"assente","note":"\"Migliori proteine whey 2026\": Myprotein non c'è, Yamamoto sì."},
 {"domain":"reddit.com","llm_citations":3,"aio_citations":0,"serp_positions":5,"total":8,"brand_status":"presente","note":"Thread r/ItalyFitness citati da Perplexity, tra cui \"alternative a myprotein\". In SERP escono thread stranieri tradotti in automatico."},
 {"domain":"ilfattoalimentare.it","llm_citations":0,"aio_citations":0,"serp_positions":1,"total":1,"brand_status":"presente","note":"Primo risultato su \"scandalo myprotein\": la multa AGCM da 260mila euro del 2018."}],
"gap":[
 {"promise":"\"MYPROTEIN è il No. 1 in Europa per la Nutrizione Sportiva\" (meta description della home)","verdict":"confermata","evidence":"Il dato regge sulla visibilità generativa: 268 menzioni negli AI Overview contro 82 di Yamamoto, e 7 risposte LLM di categoria su 8. Non regge sulle classifiche di qualità: il brand non compare nella top 10 delle due query di categoria, e le classifiche più citate premiano altri marchi.","items":268},
 {"promise":"\"FINO AL -50% SU QUASI TUTTO\" (banner fisso su ogni pagina del sito)","verdict":"contraddetta","evidence":"Chi valuta se comprare non crede allo sconto: \"prezzo gonfiato a 130 e scontato al 50%+ è proprio subdola\" (Trustpilot), \"scontate al 50% sono sul prezzo di sempre su Amazon\" (Reddit). Il prezzo compare in 73 contenuti pertinenti, 26 negativi e 14 misti.","items":73},
 {"promise":"Spedizione in 4-7 giorni, oppure in 2-5 giorni da 1,99 euro (due pagine del sito)","verdict":"contraddetta","evidence":"Già il sito dà due versioni. La consegna è il tema più citato in assoluto (98 contenuti) ed è ambivalente: 38 positivi e 33 negativi. Nelle 1-2 stelle compare in 31 recensioni su 89.","items":98},
 {"promise":"\"Qualità Garantita\": BRCGS AA, Informed Sport e Informed Choice (pagina qualità)","verdict":"confermata","evidence":"È l'argomento con cui ChatGPT preferisce Myprotein a Prozis. Viene però contestata su YouTube e Reddit, dove 16 contenuti su 75 toccano la qualità e più della metà in negativo.","items":71},
 {"promise":"Assistenza clienti: sul sito non c'è una promessa esplicita di livello di servizio","verdict":"non_rivendicata","evidence":"Assistenza, resi e rimborsi è il primo tema nelle recensioni da 1-2 stelle (36 su 89), e reso a pagamento (10,69 euro) è un'obiezione ricorrente. Il sito non comunica niente su questo terreno.","items":54}],
"competitors":[
 {"name":"Myprotein","sov":0.875,"note":"268 menzioni negli AI Overview, 40.500 ricerche di brand al mese in media."},
 {"name":"Bulk","sov":0.625,"note":"80 menzioni negli AI Overview. Unico brand nella risposta ChatGPT su \"migliori whey 2026\", con 16 citazioni a bulk.com."},
 {"name":"Yamamoto Nutrition","sov":0.375,"note":"82 menzioni negli AI Overview. In top 10 su entrambe le query di categoria, presente nelle classifiche BestBody e TrovaIntegratori. Posizionata come premium e made in Italy."},
 {"name":"Prozis","sov":0.125,"note":"31 menzioni negli AI Overview. Su Reddit è citata sia come alternativa sia come \"troppo cara ormai\"."},
 {"name":"Foodspring","sov":0.0,"note":"0 menzioni negli AI Overview Italia e 0 nelle risposte LLM. Compare solo come nuovo sponsor di un creator (2019)."}],
"methodology":{
 "notes":[
  "Raccolta del 21 settembre 2026. Finestra di analisi da settembre 2025 a settembre 2026. I video YouTube sono stati scelti per visualizzazioni, anche se più vecchi.",
  "Deduplica per fonte sul testo normalizzato. Esclusi i commenti degli account del brand. 837 contenuti unici, 314 pertinenti al brand.",
  "Pertinenza: tutte le recensioni Trustpilot e i contenuti Reddit. Per i social, solo i commenti che nominano il brand o toccano prodotto, prezzo o servizio. I contenuti di Reddit, Instagram e YouTube sono stati poi rivisti uno per uno a mano.",
  "Temi fatti emergere da un campione trasversale e assegnati con regole testuali (più temi per contenuto), con revisione manuale di tutti i contenuti non Trustpilot. Nessun contenuto è rimasto senza tema: i giudizi generici sono raccolti in GIUDIZIO GENERALE.",
  "Sentiment Trustpilot: dal voto, corretto sul testo (1-2 stelle negativo, 3 stelle neutro o misto, 4-5 stelle positivo o misto se il testo contiene una riserva). Social e Reddit: etichetta manuale.",
  "Share of voice LLM calcolato solo sulle famiglie A e B (8 risposte), le uniche in cui il brand non è nominato nella domanda.",
  "Verifiche fattuali confrontate con le pagine delivery-information, international-delivery, returns-policy e about-us/quality di myprotein.it, scaricate il 21/09/2026."],
 "limits":[
  "Trustpilot: il campione è stratificato per stelle, quindi le quote di sentiment dipendono da come è stato raccolto. La distribuzione reale delle stelle non è nota: la pagina Trustpilot blocca le richieste dirette e l'attore non la restituisce. Il blocco non è stato aggirato.",
  "Quick: 1 sola esecuzione per prompt LLM, quindi il dato di presenza è indicativo e non una frequenza.",
  "Archivio menzioni AI: disponibile solo AI Overview per l'Italia (ChatGPT non supportato) e senza storico mensile. La cronistoria della visibilità AI non si può ricostruire da qui.",
  "YouTube: le date dei commenti sono approssimate (\"x anni fa\") e i video più visti sono del 2016-2020. I commenti YouTube sono fuori dalle serie temporali.",
  "Instagram restituisce solo gli ultimi commenti visibili per post: 108 in 50 post.",
  "Sottotitoli automatici: il nome del brand viene trascritto male, quindi possono mancare occorrenze non riconosciute neanche con il matching fuzzy.",
  "Il sentiment dei contenuti raccolti non misura la soddisfazione della clientela: chi scrive è autoselezionato."],
 "failed_sources":[
  {"source":"TikTok (commenti pertinenti)","reason":"I commenti dei video italiani di terzi riguardano i contenuti del creator. Il profilo @myprotein è globale e in inglese."},
  {"source":"Instagram (prima esecuzione)","reason":"Handle sbagliato (@myprotein_it). Rilanciato con @myproteinit, preso dal footer del sito."}],
 "calls":{"dataforseo":37,"apify_runs":9,"reddit_mcp":7,"yt_dlp_video":11},
 "cost_estimate":"Circa 1,8 USD: DataForSEO circa 0,9 (21 prompt LLM 0,75, poi SERP, menzioni e keyword), Apify 0,85 da consuntivo (Trustpilot 0,35, Instagram 0,12, TikTok 0,39). YouTube e Reddit a costo zero.",
 "cap":{"requested":1000,"collected":862,"note":"Tetto Quick di circa 1.000 contenuti e 4 USD: rispettato."}},
"custom_sections":[]
}
# custom: search volume + trustpilot replies
sv={"2025-09":33100,"2025-10":33100,"2025-11":60500,"2025-12":33100,"2026-01":60500,"2026-02":40500,"2026-03":40500,"2026-04":40500,"2026-05":49500,"2026-06":33100,"2026-07":27100,"2026-08":27100}
mx=max(sv.values())
rows=''.join(f'<div style="display:flex;align-items:center;gap:10px;margin:4px 0"><span style="width:64px;font-variant-numeric:tabular-nums">{k}</span><span style="height:14px;border-radius:3px;background:var(--accent,#E52217);width:{round(v/mx*70,1)}%"></span><span style="font-variant-numeric:tabular-nums">{v:,}'.replace(',', '.')+'</span></div>' for k,v in sv.items())
data['custom_sections'].append({"title":"RICERCHE GOOGLE DEL BRAND","html":"<p>Volume mensile di ricerca su Google Italia per \"myprotein\" (DataForSEO, dati Google Ads). È l'unica serie continua su 12 mesi disponibile in questo audit.</p>"+rows+"<p>Le ricerche correlate più frequenti sono di tipo transazionale: \"codice sconto myprotein\" (2.400 al mese), \"myprotein creatina\" (1.600), \"myprotein italia\" (1.300). Fra le ricerche correlate delle SERP di brand compaiono \"Scandalo Myprotein\" e \"Myprotein recensioni negative\".</p>"})
data['custom_sections'].append({"title":"COME RISPONDE IL BRAND SU TRUSTPILOT","html":"<p>Sul campione di 239 recensioni: <strong>234 hanno una risposta (98%)</strong>. Le risposte distinte sono 106, e <strong>157 sono identiche ad almeno un'altra</strong>. Il testo più ripetuto compare 17 volte.</p><table><thead><tr><th>Stelle</th><th>Risposte</th><th>Tempo mediano di risposta</th></tr></thead><tbody><tr><td>1</td><td>50</td><td>15,5 ore</td></tr><tr><td>2</td><td>39</td><td>16,5 ore</td></tr><tr><td>3</td><td>48</td><td>130 ore</td></tr><tr><td>4</td><td>50</td><td>132 ore</td></tr><tr><td>5</td><td>47</td><td>120 ore</td></tr></tbody></table><p>La lettura: le negative vengono prese in carico in meno di un giorno, le positive e le neutre dopo circa 5 giorni con testi standard. 88 risposte su 89 alle recensioni da 1-2 stelle rimandano all'area messaggi dell'account (\"Le ho inviato un messaggio sul suo account online\"), quindi chi legge la recensione non vede mai come si è risolto il problema.</p>"})
json.dump(data,open('../data.json','w'),ensure_ascii=False,indent=1)
print('ok',sum(t['volume'] for t in themes))
