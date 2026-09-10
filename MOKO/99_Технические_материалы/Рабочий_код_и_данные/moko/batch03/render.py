from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import json
R=Path('/home/user/moko');B=R/'batch03';P=R/'production/thumbnails'
exec((R/'revision2/render.py').read_text().split('# 1 Core tutorial')[0])
items=[]
def export(im,vid,headline,lesson,note):
 brand(im);path=P/(vid+'.jpg');im.save(path,quality=96);im.save(B/(vid+'.png'))
 items.append({'id':vid,'headline':headline,'lesson':lesson,'note':note,'path':str(path)})
def sub(im,t,x,y,size=27):ImageDraw.Draw(im).text((x,y),t,font=f(size,450,True),fill='#c6ceda')
im=base();tag(im,'PYTHON / MOKO SE',GREEN);art(im,B/'assets/folders.png',(706,145,556,556))
textfit(im,'СТРУКТУРА',48,198,103,WHITE,690);textfit(im,'ПАПОК',48,319,120,GREEN,690);sub(im,'Что где находится в MOKO SE',52,485,27);pill(im,'УРОК 0.1',48,621,GREEN)
export(im,'tgIy0Ra-mn0','Структура папок','0.1','По описанию: назначение Data, Drivers, Images, Plugins, Projects, PythonLibrary и остальных папок. Иллюстрация папок, не абстрактное дерево данных из урока 14.')
im=base();tag(im,'PYTHON / MOKO SE',GREEN);art(im,B/'assets/project.png',(706,145,556,556))
textfit(im,'СОБИРАЕМ',48,198,106,WHITE,690);textfit(im,'ПРОЕКТ',48,323,120,GREEN,690);sub(im,'Скрипты, библиотека, шаблон Word',52,487,25);pill(im,'УРОК 1',48,621,GREEN)
export(im,'pzxfkmvQW2U','Собираем проект','1','Подключение трёх скриптов, MOKO.py и шаблона Microsoft Word. Концептуальная схема сборки, без выдуманных настроек программы.')
im=base();tag(im,'PYTHON / MOKO SE',GREEN);art(im,B/'assets/run.png',(705,145,557,557))
textfit(im,'ЗАПУСКАЕМ',48,198,101,WHITE,694);textfit(im,'ПРОЕКТ',48,322,120,GREEN,694);sub(im,'Импорт MOKO и первые функции',52,487,25);pill(im,'УРОК 2',48,621,GREEN)
export(im,'9QniN5XarQo','Запускаем проект','2','Описание и главы: изменение имени скрипта, заполнение трёх скриптов и повторные запуски. Не смешивать со сборкой проекта в уроке 1.')
im=base();tag(im,'PYTHON / MOKO SE',GREEN)
textfit(im,'ТИПЫ',48,198,130,WHITE,690);textfit(im,'СООБЩЕНИЙ',48,343,100,GREEN,690);sub(im,'info, error, warning и другие',52,491,27);pill(im,'УРОК 3 / STAGE',48,621,GREEN)
d=ImageDraw.Draw(im);d.ellipse((826,149,1270,642),fill='#27391e');d.rounded_rectangle((765,159,1217,647),radius=17,fill='#151f2c',outline='#455346',width=2);d.text((796,183),'Stage / типы',font=f(23,550,True),fill=WHITE);d.line((788,230,1193,230),fill='#35463a',width=1)
mono=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',31)
for i,(text,c) in enumerate([('info',GREEN),('error','#ed6262'),('plugin','#b8eb55'),('driver','#b8eb55'),('report','#b8eb55'),('warning','#ffca65')]):
 y=253+i*60;d.rounded_rectangle((790,y,1192,y+47),radius=7,fill='#1d2a36');d.ellipse((809,y+16,821,y+28),fill=c);d.text((844,y+4),text,font=mono,fill=WHITE)
export(im,'koGtgs5iNfk','Типы сообщений','3','Исправлен прежний черновой смысл «этапы программы». В описании перечислены типы info, error, plugin, driver, report, warning. Правая карточка — схема типов, не снимок интерфейса.')
im=base();tag(im,'PYTHON / MOKO SE',GREEN);art(im,B/'assets/dialog.png',(7,143,569,558))
textfit(im,'ДИАЛОГОВЫЕ',567,212,92,WHITE,663);textfit(im,'ОКНА',567,328,128,GREEN,663);sub(im,'Ввод данных и изображения',574,493,26);pill(im,'УРОК 4 / MESSENGER',574,621,GREEN)
export(im,'w9YARQn9SFs','Диалоговые окна','4','Messenger формирует окна, таймер, ввод string/boolean, выбор и изображения. Не изображать социальный мессенджер, Telegram или переписку.')
im=base();tag(im,'PYTHON / MOKO SE',GREEN);art(im,B/'assets/exchange.png',(701,142,560,560))
textfit(im,'ОБМЕН',48,201,127,WHITE,690);textfit(im,'С ПРИБОРАМИ',48,341,88,GREEN,690);sub(im,'Driver: set и get',52,493,31);pill(im,'УРОК 6 / DRIVER',48,621,GREEN)
export(im,'S3gTxhKKBOs','Обмен с приборами','6','Устанавливаем значения и получаем данные через функцию Driver; далее формируется протокол Word. Это Python-урок, не курс разработки LabVIEW-драйвера. Прибор — условная иллюстрация без модели и показаний.')
(B/'new_items.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
sheet=Image.new('RGB',(1968,1040),'#080d15');d=ImageDraw.Draw(sheet);d.text((36,25),'MOKO / ПАРТИЯ 03',font=f(33,650),fill=WHITE);d.text((36,76),'PYTHON · ПРОВЕРЕНО ПО ОПИСАНИЯМ И ТАЙМКОДАМ',font=f(20,500,True),fill='#a3aebe')
for i,a in enumerate(items):
 x=36+(i%3)*644;y=133+(i//3)*433;sheet.paste(Image.open(a['path']).resize((608,342),Image.Resampling.LANCZOS),(x,y));d.text((x,y+356),'Урок '+a['lesson']+' / '+a['headline'],font=f(21,550),fill=WHITE)
sheet.save(B/'batch03_preview.jpg',quality=96)
print('New batch:',len(items),'Production total:',len(list(P.glob('*.jpg'))))
