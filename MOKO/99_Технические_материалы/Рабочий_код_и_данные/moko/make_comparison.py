from PIL import Image,ImageDraw,ImageFont,ImageOps
import json,zipfile,os
vs=json.load(open('/home/user/moko/videos.json'));pairs=[(25,'01_graph'),(19,'02_drivers'),(8,'03_headlight')]
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
im=Image.new('RGB',(1344,1256),'#111827');d=ImageDraw.Draw(im)
d.text((24,20),'СЕЙЧАС',font=f,fill='#a8b4c6');d.text((684,20),'НОВАЯ КОНЦЕПЦИЯ',font=f,fill='white')
for row,(idx,name) in enumerate(pairs):
 y=72+row*392
 for x,p in [(24,'/home/user/moko/originals/'+vs[idx]['id']+'.jpg'),(684,'/home/user/moko/concepts/'+name+'.png')]:
  t=Image.open(p).convert('RGB');t=ImageOps.fit(t,(636,358));im.paste(t,(x,y))
 t=Image.open('/home/user/moko/concepts/'+name+'.png').convert('RGB');t=ImageOps.fit(t,(1280,720));t.save('/home/user/moko/concepts/'+name+'_1280x720.jpg',quality=95)
im.save('/home/user/moko/comparison.jpg',quality=95)
with zipfile.ZipFile('/home/user/moko/concepts.zip','w',zipfile.ZIP_DEFLATED) as z:
 for _,name in pairs:z.write('/home/user/moko/concepts/'+name+'_1280x720.jpg',name+'_1280x720.jpg')
