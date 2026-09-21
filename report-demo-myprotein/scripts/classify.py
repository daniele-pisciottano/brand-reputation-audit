import json,re
from collections import Counter
it=json.load(open('../raw/items_raw.json'))
T={
 'PREZZO E SCONTI': r'prezz|cost[ai]|cost[oa]no|\bcaro\b|\bcara\b|car[ei] |€|\beuro\b|scont|offert|aument|ladri|convenien|economic|risparm|\bkg\b.*€|al kg|folli|vertiginos|spedizione gratuita a 55',
 'CONSEGNA E CORRIERE': r'delivery|tempi di preparazione|consegn|spedi[tz]|spediz|corrier|ritard|punto di ritiro|poste|\bbrt\b|\bdhl\b|\bgls\b|tracking|mai ricevut|mai arrivat|non (è|e\') (mai )?arrivat|arrivat[oa] (in|dopo)|giorni senza|inviare i prodotti|veloc|rapid|puntual|tempestiv|in tempo',
 'PACCO E IMBALLAGGIO': r'distrutt|sporc|dirt|damage|danneggi|rott[oia]|\baperto\b|aperta|schiacciat|bucat|spaccat|imballag|pluriball|sigill|tappo|coperchio|fuoriusc|macchiat|tagliat[oa]|chiusura',
 'ORDINE ERRATO O INCOMPLETO': r'avevo chiesto solo|regalo|mancan|sbagliat|errat[oa]|misurino|omagg|incomplet|non c.era|pacca sbagliato|non corrispond',
 'ASSISTENZA, RESI E RIMBORSI': r'assistenz|servizio clienti|customer|operator|risposta|rispond|chat\b|e-?mail|call center|rimbors|\breso\b|\bresi\b|reclam|profilo bloccato|perculano|ignor|supporto',
 'GUSTO E CONSISTENZA': r'odore|gust[oi]|sapor|\bsa di\b|sanno di|imbevibil|disgust|schifo|grumi|sciogli|solubil|consistenz|chimico|nauseant|buonissim|delizios|squisit|\bbuon[eoi]?\b.*(gusto|sapore)',
 'QUALITÀ E SCADENZE': r'qualit|analisi|amminoacid|aminoacid|additiv|zuccher|peggiorat|scadenz|scadono|digest|stomaco|\bbagno\b|lassativ|standard qualitativo|ingredient|etichett|ricerca scientifica',
 'ABBIGLIAMENTO': r'abbigliam|\btaglia\b|taglie|shorts|leggin|cucitur|felpa|tessut|vestibilit',
 'ASSORTIMENTO': r'molta scelta|assortiment|vasta|gamma|non vendono pi|ampia',
 'SITO, APP E PAGAMENTO': r'\bsito\b|\bapp\b|pagament|paypal|checkout|account|carrello|modificar|correggere un ordine',
}
TR={k:re.compile(v,re.I) for k,v in T.items()}
POS=re.compile(r'ottim|eccellent|perfett|buon[oaie]?\b|bene\b|consiglio|consigliat|soddisf|veloc|rapid|puntual|top\b|super\b|fantastic|gentil|favolos|love|spaccano|droga|migliore|piace',re.I)
NEG=re.compile(r'pessim|delus|schifo|imbevibil|terribil|ladri|mai più|mai piu|vergogn|scandal|peggior|pena\b|disappoint|danneggi|rott|sbagliat|mancan|ritard|folli|troppo car|insopportabil|problem|lament|non (è|e\') arrivat|mai ricevut|fallire|aument|rubat|truff',re.I)
BRAND=re.compile(r'my ?protein|\bmp\b|impact whey|clear whey|myproteinit',re.I)
SERV=re.compile(r'ordin|spedi|consegn|assistenz|prezz|cost|€|euro|reso|rimbors|app\b|pagat|compr|gust|prodott|creatin|proteine|taglia|shorts|qualit|ladri|arrivat',re.I)
def sentiment(x):
    if x['source']=='Trustpilot':
        r=x['rating']; p=bool(POS.search(x['text'])); n=bool(NEG.search(x['text']))
        if r<=2: return 'mixed' if (p and re.search(r'\bma\b|però|peccato',x['text'],re.I) and r==2) else 'negative'
        if r==3: return 'mixed' if (p or n) else 'neutral'
        return 'mixed' if re.search(r'\bma\b|però|peccato|purtroppo',x['text'],re.I) and n else 'positive'
    p=bool(POS.search(x['text'])); n=bool(NEG.search(x['text']))
    if p and n: return 'mixed'
    if n: return 'negative'
    if p: return 'positive'
    return 'neutral'
for x in it:
    t=x['text']
    if x['source'] in ('Trustpilot','Reddit'): pert=True
    elif x['source']=='Instagram': pert=bool(BRAND.search(t) or SERV.search(t))
    elif x['source']=='YouTube': pert=bool(BRAND.search(t) or (x.get('parent') in ('STsPe8r_ba8','2ZwwkOHmnR0','zDejmupnl0E','_3acKpG18xs') and SERV.search(t) and re.search(r'prodott|qualit|prezz|sponsor|gust|marca|brand',t,re.I)))
    else: pert=bool(BRAND.search(t))
    x['pertinent']=pert
    x['themes']=[k for k,r in TR.items() if r.search(t)] if pert else []
    x['sentiment']=sentiment(x) if pert else None
OV=__import__('json').load(open('overrides.json'))
for k,v in OV.items():
    x=it[int(k)]
    if v.get('drop'): x['pertinent']=False; x['themes']=[]; x['sentiment']=None; continue
    x['pertinent']=True
    if 'sentiment' in v: x['sentiment']=v['sentiment']
    if 'themes' in v: x['themes']=v['themes']
for x in it:
    if x['pertinent'] and not x['themes'] and x['source']=='Trustpilot': x['themes']=['GIUDIZIO GENERALE']
json.dump(it,open('../raw/items_classified.json','w'),ensure_ascii=False,indent=0)
P=[x for x in it if x['pertinent']]
print('pertinent',len(P),Counter(x['source'] for x in P))
print('no theme',Counter(x['source'] for x in P if not x['themes']))
