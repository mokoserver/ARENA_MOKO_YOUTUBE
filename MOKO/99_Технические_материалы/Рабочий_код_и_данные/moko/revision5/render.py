from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageOps,ImageFilter
R=Path('/home/user/moko');O=R/'revision5'
exec((R/'revision2/render.py').read_text().split('# 1 Core tutorial')[0])
old=Image.open(R/'revision4/05_stream_framed.png').convert('RGB');im=old.copy()
left=base();d=ImageDraw.Draw(left);d.ellipse((45,199,526,680),fill='#192331')
a=Image.open(O/'assets/plugin_portrait_cutout.png').convert('RGBA')
mask=a.getchannel('A');bbox=mask.point(lambda p:255 if p>60 else 0).getbbox();a=a.crop(bbox)
a=a.resize((round(a.width*582/a.height),582),Image.Resampling.LANCZOS)
# Align face with the approved left-hand composition. Shoulders can naturally run off canvas.
x=round((550-a.width)/2);left.paste(a,(x,144),a)
pill(left,'● СТРИМ 4.1',48,646,ORANGE)
im.paste(left.crop((0,100,548,720)),(0,100))
# The complete right-hand typography, frame and screenshot stay exactly as approved.
assert np.array_equal(np.asarray(im)[:,548:],np.asarray(old)[:,548:])
im.save(O/'05_stream_stylized.png');im.save(O/'05_stream_stylized.jpg',quality=97)
sheet=Image.new('RGB',(1648,609),'#080d15');s=ImageDraw.Draw(sheet)
s.text((32,25),'MOKO / SYSTEMS · ОБРАБОТКА ПОРТРЕТА',font=f(29,600),fill=WHITE)
s.text((32,83),'БЫЛО',font=f(20,550,True),fill='#a3aebe');s.text((848,83),'СТИЛИЗОВАННЫЙ ПОРТРЕТ',font=f(20,550,True),fill=ORANGE)
for x,a in [(32,old),(848,im)]:sheet.paste(a.resize((768,432),Image.Resampling.LANCZOS),(x,129))
s.text((32,579),'Портрет обработан генеративно. Программа, рамка и надписи сохранены.',font=f(17,450,True),fill='#a3aebe')
sheet.save(O/'portrait_comparison.jpg',quality=96)
print('Right-side UI/frame/text verified unchanged, pixel-for-pixel in PNG.')
