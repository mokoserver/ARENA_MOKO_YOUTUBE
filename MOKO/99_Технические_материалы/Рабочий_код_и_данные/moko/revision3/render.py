from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageFilter,ImageEnhance
# Reuse identical typography, palette and brand positioning from approved set.
exec(Path('/home/user/moko/revision2/render.py').read_text().split('# 1 Core tutorial')[0])
D=R/'revision3'
def portrait(name,size):
 a=Image.open(D/'assets'/(name+'_cutout.png')).convert('RGBA')
 alpha=np.asarray(a.getchannel('A')).copy();alpha=np.clip((alpha.astype(float)-38)*255/217,0,255).astype('uint8');a.putalpha(Image.fromarray(alpha))
 a=ImageOps.contain(a,size,Image.Resampling.LANCZOS)
 rgb=ImageEnhance.Color(a.convert('RGB')).enhance(0.88)
 rgb=ImageEnhance.Contrast(rgb).enhance(1.06)
 rgb.putalpha(a.getchannel('A'));return rgb

def put_portrait(im,a,xy,color):
 # Modest edge separation; no change to facial geometry.
 mask=a.getchannel('A');outer=mask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(2))
 layer=Image.new('RGBA',a.size,color);layer.putalpha(outer.point(lambda x:int(x*.24)))
 im.paste(layer,xy,layer);im.paste(a,xy,a)

im=base();tag(im,'РАЗРАБОТКА',ORANGE)
d=ImageDraw.Draw(im);d.ellipse((45,199,526,680),fill='#192331')
a=portrait('plugin',(545,632));put_portrait(im,a,(0,116),ORANGE)
textfit(im,'ПИШЕМ',560,129,90,WHITE,673);textfit(im,'ПЛАГИН',560,227,96,ORANGE,673)
# Actual source screenshot, no generated substitute.
screen=Image.open(D/'assets/plugin_screenshot.png').convert('RGB');screen=screen.resize((657,319),Image.Resampling.LANCZOS)
d.rounded_rectangle((550,359,1230,701),radius=13,fill='#1b2638',outline='#a46735',width=2)
im.paste(screen,(562,371))
pill(im,'● СТРИМ 4.1',48,646,ORANGE)
# Short, accurate supporting description placed above the software window.
d.text((564,333),'СКОРОСТНОЙ СБОР ДАННЫХ',font=f(19,600,True),fill='#c6ceda')
save(im,'05_stream.jpg')

im=base();tag(im,'MOKO / СОБЫТИЯ',RED)
d=ImageDraw.Draw(im);d.ellipse((806,166,1344,704),fill='#291c29')
a=portrait('expo',(565,565));put_portrait(im,a,(756,156),RED)
d.text((51,145),'EXPO ELECTRONICA / 2026',font=f(31,600,True),fill=RED)
textfit(im,'MOKO SE',48,206,116,WHITE,734);textfit(im,'RF-SE',145,334,119,RED,637)
d.line((54,417,114,417),fill=RED,width=7);d.line((95,398,116,417,95,436),fill=RED,width=7)
# Product identity extracted from the supplied original thumbnail.
a=Image.open(D/'assets/rfse_mark.png').convert('RGB');p=np.asarray(a).astype(float)
# White background becomes transparent, dark wordmark white; red waveform stays red.
alpha=np.clip((255-p.min(axis=2))*1.35,0,255).astype('uint8')
isred=(p[:,:,0]>p[:,:,1]*1.3)&(p[:,:,0]>p[:,:,2]*1.3)
color=np.ones_like(p,dtype='uint8')*238;color[isred]=[214,69,69]
out=Image.fromarray(np.dstack([color,alpha]),'RGBA');out.thumbnail((587,112),Image.Resampling.LANCZOS)
d.rounded_rectangle((52,511,731,634),radius=13,fill='#101928',outline='#59313a',width=2)
im.paste(out,(90,520),out)
d.text((53,658),'ПАРТНЁРСТВО С RFTEX',font=f(25,600,True),fill=WHITE)
save(im,'06_expo.jpg')

# Separate, explicit before-after review of ONLY the two revised thumbnails.
sheet=Image.new('RGB',(1648,1120),'#080d15');sd=ImageDraw.Draw(sheet)
sd.text((32,24),'MOKO / SYSTEMS · ПРАВКИ 03',font=f(30,600),fill=WHITE)
sd.text((32,78),'ПРЕДЫДУЩИЙ ВАРИАНТ',font=f(21,500,True),fill='#a3aebe');sd.text((848,78),'ИСПРАВЛЕННЫЙ',font=f(21,500,True),fill='#b8eb55')
for i,(name,label) in enumerate([('05_stream.jpg','05 / Плагин — человек + реальный интерфейс'),('06_expo.jpg','06 / Выставка — человек + продукт RF-SE')]):
 y=131+i*483
 for x,path in [(32,R/'revision2/thumbs'/name),(848,D/'thumbs'/name)]:
  a=Image.open(path).resize((768,432),Image.Resampling.LANCZOS);sheet.paste(a,(x,y))
 sd.text((32,y+443),label,font=f(22,500,True),fill=WHITE)
sheet.save(D/'before_after.jpg',quality=96)
