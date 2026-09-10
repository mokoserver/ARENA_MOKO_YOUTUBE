from pathlib import Path
import requests,json,re,concurrent.futures,shutil
R=Path('/home/user/moko');D=R/'catalog/details';D.mkdir(exist_ok=True)
V=json.load(open(R/'catalog/all_videos.json'))
for p in (R/'batch03/research').glob('*.json'):
 if len(p.stem)==11:shutil.copy2(p,D/p.name)
def get(a):
 f=D/(a['id']+'.json')
 if f.exists():return json.load(open(f))
 o={'id':a['id'],'title':a['title'],'description':None}
 try:
  rr=requests.get(a['url'],timeout=18);o['http']=rr.status_code
  m=re.search(r'(?:var )?ytInitialPlayerResponse\s*=\s*',rr.text)
  if m:
   x=json.JSONDecoder().raw_decode(rr.text[m.end():])[0];o['description']=x.get('videoDetails',{}).get('shortDescription');o['playability']=x.get('playabilityStatus',{}).get('status')
 except Exception as e:o['error']=str(e)
 f.write_text(json.dumps(o,ensure_ascii=False,indent=2));return o
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as p:ds=list(p.map(get,V))
(R/'catalog/descriptions_all.json').write_text(json.dumps(ds,ensure_ascii=False,indent=2))
print('Descriptions available',sum(bool(x.get('description')) for x in ds),'of',len(ds))
for x in ds:
 if x['id'] in ['feEv04DYWbA','OhPQyqKovhA','i3N3CFncdw8','BSgXt5addDM','oJktpGbr7WA','lSWbtmhcpfc']:
  print('\n',x['title'],'\n',x.get('description'))
