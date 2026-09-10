import requests,json,re,concurrent.futures
from pathlib import Path
R=Path('/home/user/moko'); ids=['tgIy0Ra-mn0','pzxfkmvQW2U','9QniN5XarQo','koGtgs5iNfk','w9YARQn9SFs','S3gTxhKKBOs']
def get(vid):
 r=requests.get('https://www.youtube.com/watch?v='+vid,timeout=25)
 result={'id':vid,'http':r.status_code,'description':None,'source':'public watch page'}
 for pat in [r'var ytInitialPlayerResponse\s*=\s*',r'ytInitialPlayerResponse\s*=\s*']:
  m=re.search(pat,r.text)
  if m:
   try:
    d=json.JSONDecoder().raw_decode(r.text[m.end():])[0];detail=d.get('videoDetails',{});result['title']=detail.get('title');result['description']=detail.get('shortDescription');result['playability']=d.get('playabilityStatus',{}).get('status')
    tracks=d.get('captions',{}).get('playerCaptionsTracklistRenderer',{}).get('captionTracks',[]);result['caption_tracks']=[{'language':x.get('languageCode'),'url':x.get('baseUrl')} for x in tracks]
    break
   except Exception:pass
 (R/'batch03/research'/(vid+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2))
 print(vid, result.get('title'), result.get('playability'),(result.get('description') or '')[:6000])
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:all=list(ex.map(get,ids))
(R/'batch03/research/descriptions.json').write_text(json.dumps(all,ensure_ascii=False,indent=2))
