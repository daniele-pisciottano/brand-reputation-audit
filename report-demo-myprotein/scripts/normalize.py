import json,glob,os,re
R='../raw'; items=[]
def add(**k): items.append(k)
# Trustpilot
for s in range(1,6):
    for x in json.load(open(f'{R}/trustpilot_{s}star.json')):
        add(id='tp_'+x['reviewId'],source='Trustpilot',date=x['reviewPublishedDate'][:10],lang=x.get('reviewLanguage'),
            text=((x.get('reviewTitle') or '')+'. '+(x.get('reviewText') or '')).strip(),rating=x['reviewRating'],
            reply=x.get('replyText'),reply_date=(x.get('replyPublishedDate') or '')[:19],pub=x['reviewPublishedDate'][:19],kind='review')
# Instagram posts + comments
ig=json.load(open(f'{R}/instagram_posts.json'))
for p in ig:
    for c in (p.get('latestComments') or []):
        add(id='ig_'+str(c.get('id')),source='Instagram',date=(c.get('timestamp') or '')[:10],text=c.get('text') or '',kind='comment',
            parent=p.get('url'),owner=c.get('ownerUsername')=='myproteinit')
# TikTok comments
for c in json.load(open(f'{R}/tiktok_comments.json')):
    add(id='tt_'+str(c.get('cid')),source='TikTok',date=(c.get('createTimeISO') or '')[:10],text=c.get('text') or '',kind='comment',parent=c.get('videoWebUrl'))
# YouTube comments
for f in glob.glob(f'{R}/yt/*.info.json'):
    v=json.load(open(f))
    third= 'myprotein' not in (v.get('channel') or '').lower()
    for c in (v.get('comments') or []):
        ts=c.get('timestamp'); import datetime
        d=datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d') if ts else ''
        add(id='yt_'+c['id'],source='YouTube',date=d,text=c.get('text') or '',kind='comment',parent=v['id'],third_party=third,
            owner=c.get('author_is_uploader',False))
# Reddit
for t in json.load(open(f'{R}/reddit.json'))['threads']:
    add(id='rd_'+t['id'],source='Reddit',date=t['date'],text=t['title']+'. '+t['op'],kind='post',out_of_window=t.get('out_of_window',False))
    for i,c in enumerate(t['comments']):
        add(id=f"rd_{t['id']}_{i}",source='Reddit',date=c.get('date',t['date']),text=c['text'],kind='comment',out_of_window=t.get('out_of_window',False))
# drop empty & brand-owned replies, dedupe on text
seen=set(); out=[]
for it in items:
    t=re.sub(r'\s+',' ',it['text']).strip()
    if not t or it.get('owner'): continue
    key=(it['source'],t.lower())
    if key in seen: continue
    seen.add(key); it['text']=t; out.append(it)
json.dump(out,open('../raw/items_raw.json','w'),ensure_ascii=False,indent=0)
from collections import Counter
print(len(items),len(out),Counter(i['source'] for i in out))
print(Counter((i['source'],i['date'][:4]) for i in out))
