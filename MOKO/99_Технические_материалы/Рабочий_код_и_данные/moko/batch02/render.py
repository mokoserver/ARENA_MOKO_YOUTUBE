from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
import json
R=Path('/home/user/moko');B=R/'batch02';P=R/'production/thumbnails';P.mkdir(parents=True,exist_ok=True)
exec((R/'revision2/render.py').read_text().split('# 1 Core tutorial')[0])
new=[]
def export(im,vid,label):
 brand(im);im.save(P/(vid+'.jpg'),quality=96);new.append({'id':vid,'label':label,'path':str(P/(vid+'.jpg'))})
# Existing approved thumbnails: add language labels only where confirmed.
selected=[('b5zjy0PHU0s','01_graph.jpg','PYTHON / MOKO SE',GREEN),('EsLUSn9RDL4','02_driver.jpg','LABVIEW / РАЗРАБОТКА',ORANGE),('tXsjlxHMt6Y','03_telegram.jpg','PYTHON / MOKO SE',GREEN),('nnktD99huyE','04_headlight.jpg',None,None),('feEv04DYWbA','05_stream.jpg',None,None),('ex8ibsNSCiA',None,None,None)]
for vid,name,t,c in selected:
 path=R/'selected/thumbs'/name if name else R/'revision12/06_expo_stylized.jpg'
 im=Image.open(path).convert('RGB')
 if t:
  im.paste(base().crop((0,0,775,98)),(0,0));tag(im,t,c)
 im.save(P/(vid+'.jpg'),quality=96)
# Six new thumbnails. All true interfaces remain untouched within their frame.
im=base();tag(im,'PYTHON / MOKO SE',GREEN);art(im,B/'assets/tree.png',(700,140,560,560))
textfit(im,'ДЕРЕВО',48,202,117,WHITE,660);textfit(im,'ДАННЫХ',48,332,114,GREEN,660);ImageDraw.Draw(im).text((52,490),'Регионы и хэши',font=f(29,450,True),fill='#c6ceda');pill(im,'УРОК 14',48,621,GREEN);export(im,'HEmNyEcmrZY','Python · Дерево данных')
im=base();tag(im,'PYTHON / MOKO SE',GREEN);art(im,B/'assets/report.png',(5,145,602,554))
textfit(im,'СОЗДАЁМ',584,199,105,WHITE,648);textfit(im,'ОТЧЁТЫ',584,321,117,GREEN,648);ImageDraw.Draw(im).text((590,479),'Таблицы, строки, изображения',font=f(25,450,True),fill='#c6ceda');pill(im,'УРОК 5 / REPORT',590,621,GREEN);export(im,'oJktpGbr7WA','Python · Создаём отчёты')
im=base();tag(im,'PYTHON / MOKO SE',GREEN);art(im,B/'assets/python_setup.png',(701,144,557,557))
textfit(im,'ПЕРВЫЙ',48,193,115,WHITE,674);textfit(im,'ЗАПУСК',48,323,119,GREEN,674);ImageDraw.Draw(im).text((52,487),'Установка MOKO SE и PyCharm',font=f(27,450,True),fill='#c6ceda');pill(im,'УРОК 0',48,621,GREEN);export(im,'BSgXt5addDM','Python · Первый запуск')
im=base();tag(im,'LABVIEW / РАЗРАБОТКА',ORANGE);art(im,B/'assets/json.png',(703,145,557,557))
textfit(im,'ОБНОВЛЯЕМ',48,192,101,WHITE,680);textfit(im,'БИБЛИОТЕКУ',48,311,93,ORANGE,680);ImageDraw.Draw(im).text((52,474),'На примере JSON',font=f(30,450,True),fill='#c6ceda');pill(im,'LABVIEW / JSON',48,621,ORANGE);export(im,'lSWbtmhcpfc','LabVIEW · Обновление JSON-библиотеки')
im=base();tag(im,'LABVIEW / РАЗРАБОТКА',ORANGE);art(im,R/'revision2/assets/driver.png',(705,144,555,555))
textfit(im,'ПОДКЛЮЧАЕМ',48,193,92,WHITE,694);textfit(im,'ДРАЙВЕР',48,315,117,ORANGE,694);ImageDraw.Draw(im).text((52,479),'Интеграция с MOKO SE',font=f(30,450,True),fill='#c6ceda');pill(im,'УРОК 1.2',48,621,ORANGE);export(im,'shP4XNNsC6Q','LabVIEW · Подключение драйвера')
im=base();tag(im,'LABVIEW / РАЗРАБОТКА',ORANGE)
textfit(im,'STATE',48,202,124,WHITE,625);textfit(im,'MACHINE',48,335,109,ORANGE,625);ImageDraw.Draw(im).text((52,492),'Управление очередью',font=f(29,450,True),fill='#c6ceda');pill(im,'LABVIEW',48,621,ORANGE)
d=ImageDraw.Draw(im);d.rounded_rectangle((700,151,1231,693),radius=16,fill='#182332',outline='#687381',width=2);d.rounded_rectangle((707,158,1224,194),radius=8,fill='#253244');d.line((714,158,1217,158),fill=ORANGE,width=3);d.text((723,166),'LabVIEW / State Machine',font=f(18,550,True),fill=WHITE)
src=Image.open(R/'originals/7DngQ_kX12M.jpg').convert('RGB').crop((556,57,1223,663));screen=ImageOps.contain(src,(504,471),Image.Resampling.LANCZOS);im.paste(screen,(714+(504-screen.width)//2,205+(471-screen.height)//2));export(im,'7DngQ_kX12M','LabVIEW · State Machine — реальная схема')
(B/'new_items.json').write_text(json.dumps(new,ensure_ascii=False,indent=2))
sheet=Image.new('RGB',(1968,1012),'#080d15');d=ImageDraw.Draw(sheet);d.text((36,28),'MOKO / ПАРТИЯ 02',font=f(33,650),fill=WHITE);d.text((36,79),'PYTHON — ЗЕЛЁНЫЙ / LABVIEW — ОРАНЖЕВЫЙ',font=f(20,500,True),fill='#a3aebe')
for i,a in enumerate(new):
 x=36+(i%3)*644;y=136+(i//3)*421;sheet.paste(Image.open(a['path']).resize((608,342),Image.Resampling.LANCZOS),(x,y));d.text((x,y+358),a['label'],font=f(21,550),fill=WHITE)
sheet.save(B/'batch02_preview.jpg',quality=96)
print('Production JPGs',len(list(P.glob('*.jpg'))))
