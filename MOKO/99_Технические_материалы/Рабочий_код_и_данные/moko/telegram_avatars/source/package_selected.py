from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,base64,zipfile,hashlib
R=Path(__file__).resolve().parents[2];T=R/'telegram_avatars';B=T/'selected'
B.mkdir(parents=True,exist_ok=True)
records=json.loads((T/'concept03/source/manifest.json').read_text())
for r in records:
 r['source_png']='concept03/'+r['png'];r['source_svg']='concept03/'+r['svg']
records[0]['source_png']='alternatives04/png/news_01_megaphone.png';records[0]['source_svg']='alternatives04/svg/news_01_megaphone.svg'
records[2]['source_png']='group05/png/group_04_symbol.png';records[2]['source_svg']='group05/svg/group_04_symbol.svg'
records[0]['symbol']='Мегафон';records[2]['symbol']='Крупный фирменный знак MOKO'
for r,s in zip(records,['Мегафон','Диалоги','Крупный знак MOKO','Робот SE','Гарнитура','JR']):r['symbol']=s
sel={'news':{'status':'approved','variant':'Н1 — Мегафон','file':records[0]['source_png']},'group':{'status':'approved','variant':'Г4 — Крупный фирменный знак MOKO','file':records[2]['source_png']},'base':'concept03','other_four':'carried_over_unchanged','release':'selected/MOKO_Telegram_Итоговый_комплект.zip'}
(T/'source/selection.json').write_text(json.dumps(sel,ensure_ascii=False,indent=2))

def uri(p):return 'data:image/svg+xml;base64,'+base64.b64encode(p.read_bytes()).decode()
s=(T/'concept03/MOKO_Telegram_Концепт_03.html').read_text()
for n in [0,2]:
 old=T/'concept03'/records[n]['svg'];new=T/records[n]['source_svg'];assert uri(old) in s;s=s.replace(uri(old),uri(new))
s=s.replace('MOKO Telegram — концепт 03','MOKO Telegram — итоговый комплект').replace('КОНЦЕПТ 03','ИТОГОВЫЙ КОМПЛЕКТ')
s=s.replace('Разные роли.<br>Фирменная фактура MOKO.','Шесть аватаров.<br>Одна семья MOKO.')
s=s.replace('Крупные символы и цвета из второго концепта сохранены. Добавлен узор из исходного знака MOKO, крупные геометрические грани и общая тёмная нижняя часть с красным знаком. Не универсальный шум, а фирменная фактура.','Комплект с выбранными вариантами: мегафон для новостей и крупный фирменный знак MOKO для основной группы. Чат новостей, бот MOKO SE, бот связи и Johnny Respect сохранены из версии с фирменной текстурой.')
s=s.replace('Голубая газета — новости.','Голубой мегафон — новости.').replace('Красная сетка — группа с разделами.','Крупный белый знак MOKO на красном фоне — основная группа с разделами.')
s=s.replace('Концепт 03 · На согласование · 09.09.2026','Итоговая сборка с выбранными символами · 09.09.2026')
s=s.replace('Предыдущие концепты сохранены отдельно. Ничего не опубликовано.','Предыдущие концепты сохранены отдельно. Ничего не опубликовано. Для установки используйте PNG из итогового ZIP: квадрат целиком, без дополнительного приближения.')
(B/'MOKO_Telegram_Все_6_аватаров.html').write_text(s)

def circle(p,n):
 im=Image.open(p).convert('RGBA').resize((n,n),Image.Resampling.LANCZOS);mask=Image.new('L',(n*3,n*3));ImageDraw.Draw(mask).ellipse((0,0,n*3-1,n*3-1),fill=255);im.putalpha(mask.resize((n,n),Image.Resampling.LANCZOS));return im
f=lambda n:ImageFont.truetype(str(R/'brand/Inter.ttf'),n)
board=Image.new('RGB',(1440,1460),'#0B1220');d=ImageDraw.Draw(board)
d.text((70,48),'MOKO / TELEGRAM · ИТОГОВЫЙ КОМПЛЕКТ',font=f(25),fill='#A4B4C9')
d.text((70,103),'Шесть аватаров. Фирменный стиль MOKO.',font=f(40),fill='#F7F9FC')
d.text((70,172),'Новости — мегафон. Группа — крупный фирменный знак.',font=f(24),fill='#A4B4C9')
for n,r in enumerate(records):
 x=72+n%3*442;y=250+n//3*470;a=circle(T/r['source_png'],322);board.paste(a,(x+38,y),a)
 d.text((x+199,y+345),r['title'],font=f(28),fill='#F7F9FC',anchor='mt');d.text((x+199,y+389),r['description'],font=f(17),fill='#A4B4C9',anchor='mt')
d.line((70,1210,1370,1210),fill='#2B3B52',width=2);d.text((70,1243),'Проверка в малом размере',font=f(24),fill='#F7F9FC')
for n,r in enumerate(records):
 a=circle(T/r['source_png'],64);board.paste(a,(70+n*133,1310),a)
d.text((912,1308),'PNG 1024 × 1024 + SVG\nФирменная текстура сохранена.',font=f(21),fill='#A4B4C9',spacing=10)
board.save(B/'MOKO_Telegram_Итоговое_превью.jpg',quality=93,optimize=True)
readme='MOKO / TELEGRAM — ИТОГОВЫЙ КОМПЛЕКТ\n09.09.2026\n\nВыбранные варианты: новости — Н1, мегафон; основная группа — Г4, крупный фирменный знак MOKO. Остальные четыре аватара сохранены без изменений из концепта 03 с фирменной текстурой.\n\n'
for r in records:readme+=r['png']+' — '+r['title']+'; '+r['description']+'. Символ: '+r['symbol']+'.\n'
readme+='\nВ архиве только шесть выбранных аватаров, без альтернатив.\nPNG — файлы для установки, 1024 × 1024. SVG — векторные исходники с текстом в контурах. HTML — автономный просмотр крупных аватаров и условного списка чатов. JPG — общий обзор, не файл для установки.\n\nДля установки используйте квадратный PNG целиком: не вырезайте круг и не приближайте изображение дополнительно. Круг формируется при отображении в Telegram. Названия файлов и подписи служат для выбора, переименовывать паблики необязательно.\n\nИзображение гарнитуры обозначает связь с командой, а не наличие функции звонков. Предыдущие концепты сохранены отдельно. На площадках ничего не опубликовано и не изменено.\n'
(B/'README.txt').write_text(readme)
q={'news_selection':'Н1 — Мегафон','group_selection':'Г4 — Крупный знак MOKO','other_four_unchanged':True,'published':False,'files':[]}
for r in records:
 p=T/r['source_png'];im=Image.open(p);assert im.size==(1024,1024);im.verify();q['files'].append({'file':r['png'],'source':r['source_png'],'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(B/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
with zipfile.ZipFile(B/'MOKO_Telegram_Итоговый_комплект.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for r in records:
  z.write(T/r['source_png'],r['png']);z.write(T/r['source_svg'],r['svg'])
 for name in ['MOKO_Telegram_Все_6_аватаров.html','MOKO_Telegram_Итоговое_превью.jpg','README.txt']:z.write(B/name,name)
with zipfile.ZipFile(B/'MOKO_Telegram_Итоговый_комплект.zip') as z:
 assert z.testzip() is None
 assert len([n for n in z.namelist() if n.endswith('.png')])==6
 for r in records:assert z.read(r['png'])==(T/r['source_png']).read_bytes()
q['zip_byte_identity']=True;(B/'QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2))
print('Release ready; ZIP bytes:',(B/'MOKO_Telegram_Итоговый_комплект.zip').stat().st_size)
