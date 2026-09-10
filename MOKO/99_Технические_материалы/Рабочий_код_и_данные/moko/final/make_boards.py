from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math
R=Path('/home/user/moko');F=R/'final';rows=json.load(open(R/'catalog/registry.json'));new=json.load(open(F/'briefs/new_76.json'));newby={a['id']:a for a in new}
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
boards=[]
for key in ['PY','LV','SE','DEV','TEST','HW','CO','MEDIA']:
 its=[a for a in rows if a['key']==key and a['id'] in newby and a['tab']!='Shorts']
 for page in range(math.ceil(len(its)/12)):
  batch=its[page*12:(page+1)*12];im=Image.new('RGB',(1440,60+math.ceil(len(batch)/3)*302),'#0b1220');d=ImageDraw.Draw(im);d.text((14,15),key+' / '+str(page+1)+' — новые обложки',font=font,fill='white')
  for i,a in enumerate(batch):
   x=(i%3)*480+8;y=60+(i//3)*302;pic=Image.open(R/'production/thumbnails'/(a['id']+'.jpg')).resize((464,261),Image.Resampling.LANCZOS);im.paste(pic,(x,y));d.text((x,y+267),str(a['number'])+' '+newby[a['id']]['headline'][:45],font=font,fill='white')
  name=f'check_{key}_{page+1}.jpg';im.save(F/'briefs'/name,quality=88);boards.append(name)
print('\n'.join(boards))
