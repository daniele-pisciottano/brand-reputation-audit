# Metodologia, audit Myprotein Italia

Raccolta: 21 settembre 2026. Livello: Quick. Finestra: settembre 2025 - settembre 2026.
Brand: Myprotein (myprotein.it). Competitor: Prozis, Bulk, Foodspring, Yamamoto Nutrition.

## Fonti e volumi

| Fonte | Strumento | Raccolti | Pertinenti | File grezzo |
|---|---|---|---|---|
| Trustpilot, profilo www.myprotein.it | Apify azzouzana/trustpilot-scraper, 5 esecuzioni (una per stella), lingua it, ultimi 12 mesi | 239 | 239 | raw/trustpilot_{1..5}star.json |
| Instagram @myproteinit | Apify apify~instagram-scraper, 50 post | 108 commenti | 16 | raw/instagram_posts.json |
| TikTok, profilo @myprotein e hashtag #myprotein #myproteinitalia | Apify clockworks~tiktok-scraper e tiktok-comments-scraper | 75 post, 89 commenti | 0 | raw/tiktok_posts.json, raw/tiktok_comments.json |
| YouTube, 5 video del canale MyproteinIT e 6 video di terzi | yt-dlp (metadati, 60 commenti top, sottotitoli automatici it) | 376 commenti, 6 trascrizioni | 35 commenti, 7 occorrenze in video | raw/yt/ |
| Reddit r/ItalyFitness | MCP Reddit, search_reddit e analyze_post | 25 | 24 | raw/reddit.json |
| Risposte LLM | DataForSEO ai_optimization llm_responses, gpt-5.4 con web search e sonar-pro | 21 | 21 | raw/llm_responses.json |
| Archivio menzioni AI Overview | DataForSEO llm_mentions (cross_agg, top_domains, top_pages), Italy/it | 5 entità | | raw/llm_mentions.json |
| SERP Google.it | DataForSEO serp_organic_live_advanced, depth 10 | 10 query | | raw/serp.json |
| Ricerche correlate al brand | DataForSEO keyword_suggestions | 40 keyword | | raw/keyword_suggestions.json |
| Pagine del sito e di terzi | curl | 5 pagine myprotein.it, 9 pagine di terzi | | raw/site_*.html, raw/pages/ |

Dopo la deduplica sul testo e l'esclusione delle risposte del brand restano 837 contenuti unici. Di questi, 314 sono pertinenti al brand e alimentano temi e sentiment.

## Prompt LLM

Una esecuzione per prompt su entrambi i modelli. Il prompt E2 su ChatGPT è stato eseguito per errore due volte: sono tenute tutte e due le esecuzioni.

- A1 Quali sono le migliori proteine whey da comprare online in Italia nel 2026?
- A2 Dove conviene comprare integratori sportivi online in Italia?
- A3 Che marca di proteine in polvere mi consigli per iniziare in palestra, con un buon rapporto qualità prezzo? Vivo in Italia.
- B1 Quali sono delle buone alternative a Prozis per comprare integratori online in Italia?
- C1 Cos'è Myprotein e di quale gruppo fa parte?
- C2 Myprotein quanto ci mette a spedire in Italia e quanto costa la spedizione?
- D1 Myprotein è affidabile?
- D2 Myprotein recensioni negative: di cosa si lamentano i clienti italiani?
- E1 Myprotein o Prozis, quale è meglio?
- E2 Myprotein o Yamamoto Nutrition, quale scegliere?

A tutti i prompt è stato aggiunto "Rispondi in italiano". Lo share of voice è calcolato solo su A e B (8 risposte). raw/llm_responses.json contiene un estratto strutturato di ogni risposta, non il testo integrale: i brand in ordine di apparizione, i domini citati, le affermazioni fattuali e una sintesi con citazioni brevi.

## Query SERP

myprotein; myprotein recensioni; myprotein opinioni; myprotein truffa; scandalo myprotein; myprotein recensioni negative; myprotein o prozis; migliori proteine whey; proteine in polvere migliori marche; dove comprare integratori online.

## Classificazione

- Pertinenza: tutte le recensioni Trustpilot e i contenuti Reddit. Per Instagram e YouTube, solo i commenti che nominano il brand o toccano prodotto, prezzo o servizio. Ogni commento social e Reddit è stato poi rivisto a mano (overrides.json).
- Temi: 13 temi emersi da un campione trasversale, assegnati con regole testuali (classify.py) e più temi per contenuto. Tutti i contenuti non Trustpilot sono stati rivisti a mano. Nessun contenuto è rimasto senza tema: i giudizi generici sono in GIUDIZIO GENERALE.
- Sentiment: su Trustpilot parte dal voto e viene corretto sul testo (1-2 stelle negativo, 3 neutro o misto, 4-5 positivo o misto se il testo contiene una riserva). Su social e Reddit l'etichetta è manuale ed è riferita al brand: "consiglio HSN" è neutro per Myprotein, non positivo.
- Video: occorrenze del nome cercate con matching fuzzy sui sottotitoli automatici, perché il nome viene storpiato ("My proten", "mai pronti in"). Le citazioni sono testuali, con il nome come lo ha trascritto YouTube.

## Limiti

1. **Il campione Trustpilot è stratificato**: 50 recensioni per stella (39 per le 2 stelle), raccolte a ritroso. Le quote di sentiment di questa fonte non sono la media dei clienti, e la serie mensile non è utilizzabile: le 5 stelle coprono da giugno 2026, le 1 stella da febbraio 2026. La distribuzione reale delle stelle non è nota, perché la pagina Trustpilot blocca le richieste dirette e il blocco non è stato aggirato.
2. Quick: una esecuzione per prompt, quindi la presenza negli LLM è indicativa e non una frequenza.
3. L'archivio menzioni AI per l'Italia copre solo gli AI Overview di Google (la piattaforma chat_gpt restituisce errore 40501) ed è senza storico.
4. Le date dei commenti YouTube sono approssimate da yt-dlp e restano fuori dalle serie temporali. I video più visti sono del 2016-2020.
5. Instagram restituisce solo gli ultimi commenti visibili per post.
6. Il primo lancio Instagram con l'handle @myprotein_it ha reso zero risultati. È stato rilanciato con @myproteinit, preso dal footer del sito.
7. TikTok: nessun commento pertinente. Il profilo @myprotein è globale e in inglese, e i commenti ai video italiani di terzi parlano del creator.

## Chiamate e costi

- DataForSEO: 37 chiamate (21 LLM, 10 SERP, 3 menzioni, 1 keyword, 2 utility). Circa 0,9 USD, di cui 0,75 per i prompt LLM.
- Apify: 9 esecuzioni (Trustpilot 5, Instagram 2, TikTok 2). 0,85 USD da consuntivo della console Apify.
- Reddit MCP e yt-dlp: costo zero.
- **Totale circa 1,8 USD**, sotto il tetto di 4 USD. Contenuti raccolti: 862 lordi, dentro il tetto di circa 1.000.

## Come ripetere l'audit

Gli script sono in scripts/. Sequenza: run_apify.sh e run_apify2.sh, poi run_yt.sh e il download dei video, poi normalize.py, classify.py (con overrides.json), build_data.py, make_json.py, e infine build_report.py della skill. Per un confronto fra sei mesi conviene raccogliere Trustpilot in modo continuo per data, senza filtro stelle, così da avere una serie mensile del sentiment.
