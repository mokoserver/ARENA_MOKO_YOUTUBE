from pathlib import Path
import subprocess,json,concurrent.futures,requests
R=Path('/home/user/moko');C=R/'catalog'
pls=json.load(open(C/'playlists_raw.json'))['entries']
def getpl(v):
 p=subprocess.run(['yt-dlp','--flat-playlist','--dump-single-json','--skip-download',v['url']],capture_output=True,text=True)
 if p.returncode==0:
  x=json.loads(p.stdout);(C/(v['id']+'.json')).write_text(json.dumps(x,ensure_ascii=False));return {'id':v['id'],'title':v['title'],'videos':[{'id':a.get('id'),'title':a.get('title')} for a in x.get('entries',[])]}
 return {'id':v['id'],'title':v['title'],'error':p.stderr}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as p:members=list(p.map(getpl,pls))
(C/'existing_playlists.json').write_text(json.dumps(members,ensure_ascii=False,indent=2))
all=[]
for source,file in [('Видео','all_videos_raw.json'),('Shorts','shorts_raw.json')]:
 for a in json.load(open(C/file)).get('entries',[]):
  a['source_tab']=source;a['existing_playlists']=[p['title'] for p in members if a['id'] in [x['id'] for x in p.get('videos',[])]];all.append(a)
def dl(a):
 path=R/'originals'/(a['id']+'.jpg')
 if path.exists():return
 try:
  rr=requests.get(f"https://i.ytimg.com/vi/{a['id']}/maxresdefault.jpg",timeout=20)
  if rr.status_code!=200:rr=requests.get(a['thumbnails'][-1]['url'],timeout=20)
  if rr.status_code==200:path.write_bytes(rr.content)
 except Exception as e:print('DL failed',a['id'],str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as p:list(p.map(dl,all))
(C/'all_videos.json').write_text(json.dumps(all,ensure_ascii=False,indent=2))
for p in members:print(p['title'],len(p.get('videos',[])))
print('TOTAL',len(all))
print('LabVIEW driver series:')
for a in all:
 if any('драйверов' in t for t in a['existing_playlists']):print(a['id'],a['title'])
