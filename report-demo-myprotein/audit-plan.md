# Piano di raccolta, Myprotein Italia

Data: 21 settembre 2026. Livello: Quick. Tetto di spesa: 4 USD. Tetto contenuti: circa 1.000.

## Perimetro

- Brand: Myprotein (varianti: My Protein, MyProtein, myprotein.it, "mp"). Gruppo THG.
- Mercato: Italia, lingua italiana.
- Competitor: Prozis, Bulk, Foodspring, Yamamoto Nutrition.
- Finestra: settembre 2025 - settembre 2026, granularità mensile.
- Domande: di cosa si lamentano i clienti; presenza negli LLM senza nominare il brand; fonti che alimentano gli LLM; gap fra racconto del brand e percezione.

## Fonti incluse

| Fonte | Strumento | Volume | Stima USD |
|---|---|---|---|
| Risposte LLM (ChatGPT gpt-5.4 con web search, Perplexity sonar-pro) | DataForSEO ai_optimization | 10 prompt x 2 modelli (A3, B1, C2, D2, E2) | 0,75 |
| Archivio menzioni LLM: metriche, confronto competitor, top domini e pagine | DataForSEO llm_mentions | 5 entità, Italia | 0,35 |
| SERP Google.it con AI Overview | DataForSEO serp_organic_live_advanced | 12 query (brand, brand + modificatori, categoria) | 0,05 |
| Ricerche correlate al brand | DataForSEO keyword suggestions | 1 chiamata | 0,02 |
| Trustpilot, profilo myprotein.it | Apify azzouzana/trustpilot-scraper (raccolta per stelle, filterStars stringa, per evitare il bug del limite pagine) | circa 250 recensioni, distribuzione per stelle | 0,30 |
| Instagram @myprotein_it | Apify apify~instagram-scraper, latestComments | 50 post + commenti | 0,20 |
| TikTok profilo + hashtag #myprotein | Apify clockworks~tiktok-scraper + tiktok-comments-scraper | 50 post + commenti dei top 5 | 0,40 |
| Reddit | MCP Reddit (gratuito) | circa 100 commenti | 0 |
| YouTube canale Myprotein Italia e video di terzi | yt-dlp locale (metadati, commenti, sottotitoli automatici) | top 5 + top 5, 5 trascrizioni | 0 |
| Sito myprotein.it (home, chi siamo, spedizioni, FAQ) | fetch diretto | circa 6 pagine | 0 |

**Totale stimato: circa 2,1 USD, arrotondato per eccesso a 2,5 USD.** Sotto il tetto di 4 USD.

## Fonti escluse

- Google Maps: Myprotein è un e-commerce senza punti vendita in Italia.
- Facebook: bassa rilevanza per il target, il budget Quick va su Instagram e TikTok.
- Content analysis DataForSEO: indice scarso sull'italiano, sentiment poco affidabile.

## Note

- Quick: una sola esecuzione per prompt, dato indicativo.
- Trustpilot: il campione recente va letto per stelle, non come media dei clienti.
