import json,requests,concurrent.futures
from PIL import Image,ImageDraw,ImageFont
x=json.load(open('/home/user/moko/channel_data.json'));vs=[]
def walk(x):
 if isinstance(x,dict):
  if 'lockupViewModel'in x and x['lockupViewModel'].get('contentType')=='LOCKUP_CONTENT_TYPE_VIDEO':vs.append(x['lockupViewModel'])
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(x)
a=[]
for v in vs:
 m=v['metadata']['lockupMetadataViewModel']; a.append({'id':v['contentId'],'title':m['title']['content'],'thumbnail':v['contentImage']['thumbnailViewModel']['image']['sources'][-1]['url']})
json.dump(a,open('/home/user/moko/videos.json','w'),ensure_ascii=False,indent=2)
def dl(v):
 r=requests.get('https://i.ytimg.com/vi/'+v['id']+'/maxresdefault.jpg',timeout=20)
 if r.status_code!=200:r=requests.get(v['thumbnail'],timeout=20)
 open('/home/user/moko/originals/'+v['id']+'.jpg','wb').write(r.content)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as p:list(p.map(dl,a))
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
im=Image.new('RGB',(1200,((len(a)+2)//3)*270),'#eeeeee');d=ImageDraw.Draw(im)
for i,v in enumerate(a):
 x=(i%3)*400;y=(i//3)*270
 t=Image.open('/home/user/moko/originals/'+v['id']+'.jpg').convert('RGB');t=t.resize((384,216));im.paste(t,(x+8,y))
 text=str(i+1)+'. '+v['title'];lines=[]
 while text:
  n=min(46,len(text));lines.append(text[:n]);text=text[n:]
 d.text((x+8,y+219),'\n'.join(lines[:3]),fill='black',font=f)
im.save('/home/user/moko/current_overview.jpg')
for i,v in enumerate(a):print(i+1,v['title'])
print('Downloaded',len(a))
