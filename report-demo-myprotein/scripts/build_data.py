import json,re
from collections import Counter,defaultdict
it=[x for x in json.load(open('../raw/items_classified.json')) if x['pertinent']]
N=len(it)
DEF={
 'CONSEGNA E CORRIERE':"Tempi di consegna, corriere, punto di ritiro, pacchi mai arrivati. Include le lodi alla consegna rapida.",
 'PREZZO E SCONTI':"Livello dei prezzi, aumenti, credibilità degli sconti, soglia di spedizione gratuita.",
 'QUALITÀ E SCADENZE':"Qualità percepita del prodotto, analisi, ingredienti, digeribilità, date di scadenza ravvicinate.",
 'ASSISTENZA, RESI E RIMBORSI':"Servizio clienti, tempi e qualità delle risposte, resi a pagamento, rimborsi.",
 'PACCO E IMBALLAGGIO':"Confezioni rotte, aperte, sporche o schiacciate, protezione del pacco. Non include gli articoli mancanti.",
 'GUSTO E CONSISTENZA':"Sapore, odore, solubilità e grumi delle proteine e degli snack.",
 'ORDINE ERRATO O INCOMPLETO':"Articoli sbagliati o mancanti, misurino assente, omaggi promessi e non arrivati.",
 'GIUDIZIO GENERALE':"Valutazioni complessive senza un tema specifico (per esempio 'tutto perfetto').",
 'SITO, APP E PAGAMENTO':"Checkout, app, modifica dell'ordine, account, metodi di pagamento.",
 'COMPETITOR E ALTERNATIVE':"Passaggio ad altri brand o consigli di alternative (HSN, Bulk, Prozis, Yamamoto, Foodspring).",
 'CREATOR E SPONSOR':"Commenti sui creator che hanno lasciato Myprotein come sponsor (video del 2019-2020).",
 'ABBIGLIAMENTO':"Taglie, vestibilità e tenuta dei capi della linea abbigliamento.",
 'ASSORTIMENTO':"Ampiezza della gamma, prodotti ritirati o mancanti a catalogo.",
}
BAD=re.compile(r'zioporc|cazz|@\w',re.I)
def short(t,n=190):
    t=t.strip()
    return t if len(t)<=n else t[:n].rsplit(' ',1)[0]+'...'
themes=[]
for name,d in DEF.items():
    X=[x for x in it if name in x['themes']]
    s=Counter(x['sentiment'] for x in X)
    bs=Counter(x['source'] for x in X)
    # quotes: prefer 1 negative TP, 1 positive/mixed TP, 1 non-TP
    cand=[x for x in X if 30<=len(x['text'])<=400 and not BAD.search(x['text'])]
    q=[]
    for pred in [lambda x:x['source']=='Trustpilot' and x['sentiment']=='negative',
                 lambda x:x['source']=='Trustpilot' and x['sentiment'] in('positive','mixed'),
                 lambda x:x['source']!='Trustpilot',
                 lambda x:x['source']!='Trustpilot' and x['sentiment']=='negative']:
        for x in sorted(cand,key=lambda x:(-len(set(x['text'].split())),x['id'])):
            if pred(x) and x not in q: q.append(x); break
    themes.append(dict(name=name,definition=d,volume=len(X),share=round(len(X)/N,3),
        sentiment={k:s.get(k,0) for k in('positive','neutral','negative','mixed')},
        by_source=dict(bs),
        quotes=[dict(text=short(x['text']),source=x['source'],date=x['date'] if x['source']!='YouTube' else '',sentiment=x['sentiment']) for x in q[:3]]))
themes.sort(key=lambda t:-t['volume'])
json.dump(themes,open('../raw/themes.json','w'),ensure_ascii=False,indent=1)
for t in themes:
    print(t['name'],t['volume'],t['sentiment'],t['by_source'])
    for q in t['quotes']: print('    -',q['source'],q['sentiment'],q['text'])
