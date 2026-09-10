from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageFilter,ImageEnhance
from pathlib import Path
import json,math
R=Path('/home/user/moko');D=R/'revision2';(D/'thumbs').mkdir(exist_ok=True)
def f(size,w=700,inter=False):
 font=ImageFont.truetype(str(R/'brand'/('Inter.ttf' if inter else 'Jost.ttf')),size)
 try:font.set_variation_by_axes([14,w] if inter else [w])
 except:pass
 return font
BG='#0b1220';WHITE='#f6f8fc';GREEN='#b8eb55';ORANGE='#ff9a48';BLUE='#55c9ff';RED='#ed6262'
def base():
 im=Image.new('RGB',(1280,720),BG);d=ImageDraw.Draw(im)
 for x in range(0,1280,40):d.line((x,100,x,720),fill='#101b2b')
 for y in range(120,720,40):d.line((0,y,1280,y),fill='#101b2b')
 return im

def brand(im):
 d=ImageDraw.Draw(im);font=f(25,500,True)
 # Identical 44px top/right safe area on all six thumbnails.
 parts=[('MOKO ',WHITE),('/','#d64545'),(' SYSTEMS',WHITE)]
 tw=sum(d.textlength(t,font=font) for t,c in parts);x=1236-tw
 logo=Image.open(R/'brand/logo.png').convert('RGBA');logo.thumbnail((39,29),Image.Resampling.LANCZOS);im.paste(logo,(int(x-53),42),logo)
 for t,c in parts:d.text((x,42),t,font=font,fill=c);x+=d.textlength(t,font=font)
def tag(im,text,c):
 d=ImageDraw.Draw(im);d.rectangle((48,43,53,66),fill=c);d.text((66,40),text,font=f(21,550,True),fill=c)
def textfit(im,text,x,y,size,c,maxwidth):
 d=ImageDraw.Draw(im)
 while d.textlength(text,font=f(size))>maxwidth:size-=1
 d.text((x,y),text,font=f(size),fill=c)
def pill(im,text,x,y,c):
 d=ImageDraw.Draw(im);font=f(20,600,True);w=int(d.textlength(text,font=font))+30
 d.rounded_rectangle((x,y,x+w,y+40),radius=9,fill=c);d.text((x+15,y+8),text,font=font,fill=BG)
def art(im,path,box):
 a=ImageOps.fit(Image.open(path).convert('RGB'),(box[2],box[3]))
 # Feather square background into common engineering background.
 mask=Image.new('L',a.size,255);md=ImageDraw.Draw(mask)
 for k in range(45):md.rectangle((k,k,a.width-1-k,a.height-1-k),outline=int(255*k/45))
 im.paste(a,box[:2],mask)
def save(im,name):
 brand(im);im.save(D/'thumbs'/name,quality=96)
# 1 Core tutorial
im=base();tag(im,'MOKO SE / УРОКИ',GREEN);art(im,D/'assets/graph.png',(710,145,550,550))
textfit(im,'ГРАФИКИ',48,198,119,WHITE,680);textfit(im,'В MOKO SE',48,332,109,GREEN,680)
pill(im,'УРОК 12.1',48,621,GREEN);ImageDraw.Draw(im).text((218,631),'MOKO GRAPH',font=f(20,500,True),fill='#a3aebe');save(im,'01_graph.jpg')
# 2 Driver tutorial
im=base();tag(im,'РАЗРАБОТКА',ORANGE);art(im,D/'assets/driver.png',(706,149,558,558))
textfit(im,'СОЗДАЁМ',48,182,114,WHITE,690);textfit(im,'ДРАЙВЕР',48,312,119,ORANGE,690)
ImageDraw.Draw(im).text((52,482),'Разработка и компиляция',font=f(28,450,True),fill='#c6ceda');pill(im,'УРОК 1.1',48,621,ORANGE);save(im,'02_driver.jpg')
# 3 Same tutorial rubric, deliberately reversed composition + recognisable blue Telegram symbol
im=base();tag(im,'MOKO SE / УРОКИ',GREEN);art(im,D/'assets/telegram.png',(5,138,607,564))
textfit(im,'TELEGRAM',590,209,99,WHITE,642);textfit(im,'+ MOKO SE',590,327,91,GREEN,642)
ImageDraw.Draw(im).text((596,466),'Подключаем бота',font=f(31,450,True),fill='#c6ceda');pill(im,'УРОК 10',599,621,GREEN);save(im,'03_telegram.jpg')
# 4 Approved first AI concept portrait reused as an explicitly provisional asset.
im=base();tag(im,'ПРАКТИКА / ИСПЫТАНИЯ',BLUE)
a=Image.open(R/'concepts/03_headlight.png').convert('RGB');a=a.crop((850,120,a.width,a.height));a=ImageOps.fit(a,(488,581))
mask=Image.new('L',a.size,255);md=ImageDraw.Draw(mask)
for k in range(35):md.line((k,0,k,a.height),fill=int(k/35*255))
im.paste(a,(778,139),mask)
textfit(im,'ТЕСТ',48,201,135,WHITE,710);textfit(im,'LED-ФАРЫ',48,347,110,BLUE,735)
ImageDraw.Draw(im).text((52,507),'Автоматизация в MOKO SE',font=f(29,450,True),fill='#c6ceda');pill(im,'ИСПЫТАНИЯ',48,621,BLUE);save(im,'04_headlight.jpg')
# 5 Stream on software development: same orange rubric; format is a badge, not a new category.
im=base();tag(im,'РАЗРАБОТКА',ORANGE)
a=Image.open(R/'originals/feEv04DYWbA.jpg').convert('RGB').crop((922,55,1277,720));a=ImageOps.fit(a,(395,597));im.paste(a,(840,123))
d=ImageDraw.Draw(im);d.polygon([(818,123),(843,123),(843,720),(802,720)],fill=ORANGE)
textfit(im,'ПИШЕМ',48,159,107,WHITE,733);textfit(im,'ПЛАГИН',48,271,118,ORANGE,733)
ImageDraw.Draw(im).text((52,437),'Скоростное считывание данных',font=f(28,450,True),fill='#c6ceda')
pill(im,'● СТРИМ 4.1',48,621,ORANGE);save(im,'05_stream.jpg')
# 6 Events: real photo crop left; red brand color right and very different editorial layout.
im=base();tag(im,'MOKO / СОБЫТИЯ',RED)
a=Image.open(R/'originals/ex8ibsNSCiA.jpg').convert('RGB').crop((50,160,563,675));a=ImageOps.fit(a,(470,538));im.paste(a,(48,138))
d=ImageDraw.Draw(im);d.rectangle((48,672,518,679),fill=RED)
textfit(im,'EXPO',565,142,92,WHITE,665);textfit(im,'ELECTRONICA',565,242,71,WHITE,665);textfit(im,'2026',565,326,131,RED,665)
d.text((570,500),'MOKO SE → RF-SE',font=f(34,600,True),fill=WHITE);d.text((571,551),'Партнёрство с RFTEX',font=f(25,450,True),fill='#c6ceda');pill(im,'МОСКВА / ВЫСТАВКА',568,631,RED);save(im,'06_expo.jpg')
vs=json.load(open(R/'videos.json'))
items=[]
rows=[('01_graph.jpg',25,'Уроки MOKO SE','Зелёный · график как главный объект','concepts/01_graph_1280x720.jpg'),('02_driver.jpg',19,'Разработка','Оранжевый · код и устройство','concepts/02_drivers_1280x720.jpg'),('03_telegram.jpg',29,'Уроки MOKO SE','Тот же зелёный · обратная композиция',None),('04_headlight.jpg',8,'Практика','Голубой · человек и объект испытаний','concepts/03_headlight_1280x720.jpg'),('05_stream.jpg',5,'Разработка','Тот же оранжевый · фотография и метка стрима',None),('06_expo.jpg',0,'События','Красный · фото с выставки и крупная дата',None)]
for file,idx,cat,note,old in rows:
 items.append(dict(file=file,video=vs[idx],category=cat,note=note,previous=old,asset_note=('Лицо и фара пока из первого ИИ-концепта. Для финала нужны реальное фото и точное изображение испытываемой фары.' if idx==8 else 'Использована фотография из исходной обложки, без генеративной перерисовки лица.' if idx in [0,5] else 'Концептуальная иллюстрация, не скриншот программы и не спецификация оборудования.')))
json.dump(items,open(D/'manifest.json','w'),ensure_ascii=False,indent=2)
# High quality contact sheet.
sheet=Image.new('RGB',(1968,1048),'#080d15');sd=ImageDraw.Draw(sheet)
sd.text((36,26),'MOKO / SYSTEMS',font=f(33,600),fill=WHITE);sd.text((36,73),'ОБНОВЛЁННАЯ СЕРИЯ / 6 РОЛИКОВ / 4 РУБРИКИ',font=f(20,500,True),fill='#a3aebe')
for i,it in enumerate(items):
 x=36+(i%3)*644;y=136+(i//3)*437
 sheet.paste(Image.open(D/'thumbs'/it['file']).resize((608,342),Image.Resampling.LANCZOS),(x,y))
 sd.text((x,y+356),f'{i+1:02} / '+it['category'],font=f(23,600),fill=WHITE)
 sd.text((x,y+391),it['note'],font=f(15,400,True),fill='#a3aebe')
sheet.save(D/'series_overview.jpg',quality=96)
