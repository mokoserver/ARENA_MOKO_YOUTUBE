from pathlib import Path
import json, base64, html, zipfile, hashlib
import cairosvg
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2]; B=R/'telegram_avatars'
for d in ['png','svg','source']:(B/d).mkdir(parents=True,exist_ok=True)
ns={};exec((R/'branding/source/build.py').read_text().split('files=[]')[0],ns)
mark,text=ns['mark'],ns['text']
items=[
 ('01_news','MOKO · Новости','Новостной канал','#55C9FF','news'),
 ('02_news_chat','Чат новостей','Обсуждение публикаций канала','#B69AFF','chat'),
 ('03_moko_systems','MOKO Systems','Группа с разделами','#ED6262','sections'),
 ('04_moko_se_bot','MOKO SE Bot','Бот-диспетчер для MOKO SE','#55D6C2','se'),
 ('05_contact_bot','Связь с MOKO','Бот для обращений к команде','#FF9A48','contact'),
 ('06_johnny_respect','Johnny Respect','Личный бот в фирменном стиле MOKO','#E8C782','jr')]
BG='#0b1220'
def icon(kind):
 # 200 × 200 pictograms; broad shapes remain readable at chat-list scale.
 pre='<g transform="translate(642 650)" fill="none" stroke="#0b1220" stroke-width="18" stroke-linecap="round" stroke-linejoin="round">'
 if kind=='news':
  s='<rect x="19" y="32" width="162" height="136" rx="13"/><path d="M48 65H150M101 101H150M101 135H150"/><rect x="45" y="96" width="30" height="42" rx="3" fill="#0b1220" stroke="none"/>'
 elif kind=='chat':
  s='<path d="M72 31H168Q180 31 180 45V117Q180 130 166 130H150L128 150V130"/><path d="M28 62H124Q138 62 138 77V137Q138 150 124 150H70L41 177V150H28Q15 150 15 137V76Q15 62 28 62Z" fill="'+items[1][3]+'"/><path d="M45 102H106"/>'
 elif kind=='sections':
  s=''.join(f'<rect x="{x}" y="{y}" width="64" height="64" rx="12" fill="#0b1220" stroke="none"/>' for x in [23,113] for y in [23,113])
 elif kind=='contact':
  s='<path d="M28 108V88A72 72 0 0 1 172 88V117M172 130V144Q172 176 133 176H109"/><rect x="18" y="92" width="36" height="59" rx="13" fill="#0b1220" stroke="none"/><rect x="146" y="92" width="36" height="59" rx="13" fill="#0b1220" stroke="none"/><rect x="88" y="162" width="40" height="25" rx="12" fill="#0b1220" stroke="none"/>'
 else:
  return text('SE' if kind=='se' else 'JR',742,803,150,BG,'Inter',750,anchor='middle')
 return pre+s+'</g>'
records=[]
for slug,title,desc,col,kind in items:
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024"><defs><radialGradient id="wash" cx=".18" cy=".2" r=".85"><stop offset="0" stop-color="{col}" stop-opacity=".13"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient><pattern id="grid" width="64" height="64" patternUnits="userSpaceOnUse"><path d="M64 0H0V64" fill="none" stroke="#65778e" stroke-opacity=".045" stroke-width="2"/></pattern></defs><rect width="1024" height="1024" fill="{BG}"/><rect width="1024" height="1024" fill="url(#wash)"/><rect width="1024" height="1024" fill="url(#grid)"/><circle cx="512" cy="512" r="456" fill="none" stroke="{col}" stroke-opacity=".23" stroke-width="7"/>'''
 svg+=mark(194,176,636)
 svg+=f'<circle cx="742" cy="750" r="157" fill="{BG}"/><circle cx="742" cy="750" r="143" fill="{col}"/>'+icon(kind)+'</svg>'
 (B/'svg'/f'{slug}.svg').write_text(svg)
 p=B/'png'/f'{slug}.png';cairosvg.svg2png(bytestring=svg.encode(),write_to=str(p))
 records.append(dict(slug=slug,title=title,description=desc,color=col,png=f'png/{slug}.png',svg=f'svg/{slug}.svg'))

def circle(im,size):
 im=im.convert('RGBA').resize((size,size),Image.Resampling.LANCZOS)
 mask=Image.new('L',(size*3,size*3));ImageDraw.Draw(mask).ellipse((0,0,size*3-1,size*3-1),fill=255);mask=mask.resize((size,size),Image.Resampling.LANCZOS);im.putalpha(mask);return im
# Main static overview: an immediately visible image, not a screenshot of a website.
board=Image.new('RGB',(1440,1450),'#080f1b');d=ImageDraw.Draw(board)
f=lambda n:ImageFont.truetype(str(R/'brand/Inter.ttf'),n)
d.text((72,50),'MOKO / TELEGRAM',font=f(27),fill='#9eacbf')
d.text((72,100),'Шесть аватаров. Один стиль.',font=f(48),fill='#f4f7fb')
d.text((72,170),'Каналы · группы · боты    /    Версия 01',font=f(24),fill='#9eacbf')
for n,r in enumerate(records):
 x=72+(n%3)*442;y=253+(n//3)*470
 a=circle(Image.open(B/r['png']),322);board.paste(a,(x+38,y),a)
 d.text((x+199,y+344),r['title'],font=f(26),fill='#f4f7fb',anchor='mt')
 d.text((x+199,y+385),r['description'],font=f(16),fill='#9eacbf',anchor='mt')
d.line((72,1213,1368,1213),fill='#23334a',width=2)
d.text((72,1250),'Проверка в малом размере',font=f(24),fill='#f4f7fb')
for n,r in enumerate(records):
 a=circle(Image.open(B/r['png']),64);board.paste(a,(72+n*130,1310),a)
d.text((907,1315),'Красный знак сохранён.\nОтличия — в цвете и символе роли.',font=f(19),fill='#9eacbf',spacing=8)
board.save(B/'MOKO_6_аватаров_Telegram.jpg',quality=94,optimize=True)

def uri(path):return 'data:image/svg+xml;base64,'+base64.b64encode((B/'svg'/Path(path).with_suffix('.svg').name).read_bytes()).decode()
css='''*{box-sizing:border-box}body{margin:0;background:#080f1b;color:#f4f7fb;font:16px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}main{max-width:1100px;margin:auto;padding:38px 22px 50px}.kicker{color:#55d6c2;letter-spacing:.18em;font-size:11px}h1{font-size:clamp(31px,5vw,48px);line-height:1.12;margin:16px 0}h2{font-size:25px;margin-top:40px}p{color:#9eacbf}.intro{max-width:700px}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin:30px 0}.card{background:#101a2a;border:1px solid #25344a;border-radius:18px;padding:22px 16px;text-align:center}.avatar{cursor:zoom-in;border:0;padding:0;background:none;max-width:100%}.avatar img{width:230px;max-width:100%;border-radius:50%;display:block}h3{font-size:18px;margin:18px 0 4px}.card p{font-size:13px;min-height:40px;margin:4px 0 12px}.meta{font-size:11px;color:#8094ae;overflow-wrap:anywhere}.list{max-width:630px;background:#101a2a;border:1px solid #25344a;border-radius:16px;padding:7px 16px}.row{display:flex;gap:14px;align-items:center;padding:14px 0;border-bottom:1px solid #223047}.row:last-child{border:0}.row img{width:56px;height:56px;border-radius:50%}.row strong{font-size:15px}.row p{font-size:12px;margin:3px 0}.check{display:flex;gap:18px;flex-wrap:wrap;margin:25px 0}.check div{text-align:center;color:#8295b0;font-size:11px}.check img{display:block;width:40px;height:40px;border-radius:50%;margin:auto auto 7px}.note{border-left:3px solid #55d6c2;background:#101a2a;padding:12px 16px;color:#9eacbf;font-size:14px}.foot{border-top:1px solid #25344a;margin-top:35px;padding-top:18px;color:#8295b0;font-size:12px}dialog{background:#0b1220;color:white;border:1px solid #485b75;border-radius:16px;padding:14px;max-width:94vw;max-height:94vh}dialog::backdrop{background:#000d}dialog img{display:block;max-width:85vw;max-height:74vh;width:auto;height:auto;border-radius:50%;margin:12px auto}dialog .bar{display:flex;gap:16px;align-items:center;justify-content:space-between}#close{border:1px solid #52637c;background:#172439;color:white;padding:10px;border-radius:8px;cursor:pointer}@media(max-width:700px){.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.card{padding:16px 9px;border-radius:13px}h3{font-size:15px}.card p{font-size:12px;min-height:53px}.meta{font-size:9px}main{padding:28px 16px}.avatar img{width:160px}.check{gap:16px}}@media(max-width:350px){.grid{grid-template-columns:1fr}}'''
s='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MOKO — 6 аватаров Telegram</title><style>'+css+'</style></head><body><main><div class="kicker">MOKO / TELEGRAM · ВЕРСИЯ 01</div><h1>Разные роли.<br>Одна фирменная семья.</h1><p class="intro">Шесть аватаров для новостей, обсуждения, группы с разделами и трёх ботов. Исходный красный знак сохранён. Крупные цветные обозначения помогают различать их без мелких подписей.</p><p class="note">Нажмите на аватар, чтобы увеличить. Здесь показана круглая обрезка; файлы для установки — квадратные PNG 1024 × 1024.</p><div class="grid">'
for r in records:s+=f'<article class="card"><button class="avatar" aria-label="Увеличить {html.escape(r["title"])}"><img src="{uri(r["png"])}" alt="{html.escape(r["title"])}"></button><h3>{r["title"]}</h3><p>{r["description"]}</p><div class="meta">{r["slug"]}.png · SVG</div></article>'
s+='</div><h2>Как различаются в списке чатов</h2><p>Условный макет списка, а не снимок вашего аккаунта. Аватары — 56 пикселей.</p><div class="list">'
for r in records:s+=f'<div class="row"><img src="{uri(r["png"])}" alt=""><div><strong>{r["title"]}</strong><p>{r["description"]}</p></div></div>'
s+='</div><h2>Ещё меньше: 40 пикселей</h2><div class="check">'
for r in records:s+=f'<div><img src="{uri(r["png"])}" alt="{r["title"]}">{r["slug"][:2]}</div>'
s+='</div><p class="note">Новости — голубой знак газеты; чат — фиолетовые диалоги; группа — коралловая сетка разделов; бот MOKO SE — бирюзовый SE; связь с командой — оранжевая гарнитура; Johnny Respect — золотистый JR.</p><h2>Установка</h2><p>Выберите нужный PNG из папки png и установите фото канала, группы или бота через доступные вам настройки Telegram. Сохраните полный квадрат: круг формируется при показе. Названия в этой презентации — подписи для выбора файлов, а не предложение обязательно переименовать паблики.</p><p>В папке svg лежат векторные исходники. Варианты SE и JR переведены в контуры, установка шрифтов не требуется. Баннеры в этот выпуск не входят — выбран комплект аватарок.</p><footer class="foot">Комплект на согласование. Ничего не установлено в Telegram; ранее подготовленные обложки и брендинг не изменялись.</footer></main><dialog id="zoom"><div class="bar"><span id="caption"></span><button id="close">Закрыть ✕</button></div><img id="large" alt=""></dialog><script>const d=document.getElementById("zoom"),im=document.getElementById("large");document.querySelectorAll(".avatar").forEach(b=>b.onclick=()=>{const s=b.querySelector("img");im.src=s.src;im.alt=s.alt;document.getElementById("caption").textContent=s.alt;d.showModal()});document.getElementById("close").onclick=()=>d.close();d.onclick=e=>{if(e.target===d)d.close()};</script></body></html>'
(B/'MOKO_Аватары_Telegram.html').write_text(s)
readme='MOKO / TELEGRAM — 6 АВАТАРОВ\nВерсия 01 · На согласование\n\n'
for r in records:readme+=f'{r["png"]}\n{r["title"]} — {r["description"]}. Цвет: {r["color"]}.\n\n'
readme+='Все PNG: 1024 × 1024. Устанавливать полный квадрат, без дополнительного обрезания и приближения: круг формируется Telegram при отображении. SVG — векторные исходники, текст SE/JR в контурах. Круглая обрезка и малые размеры показаны в HTML-презентации. JPG — общий обзор, не файл для установки в профиль.\n\nКрасный фирменный знак сохранён геометрически и по цветам. Обозначения роли добавлены отдельно. Гарнитура обозначает связь с командой, а не обещание функции звонков. Рабочие названия в презентации нужны для выбора файла; переименовывать каналы, группы и ботов необязательно. Johnny Respect оформлен в фирменной семье MOKO по выбранному направлению.\n\nНичего не опубликовано и не установлено. Старые обложки и комплект брендинга не менялись.\n'
(B/'README.txt').write_text(readme)
qa={'count':6,'dimensions':[1024,1024],'approval':'pending','published':False,'files':[]}
for r in records:
 p=B/r['png'];im=Image.open(p);assert im.size==(1024,1024);im.verify()
 source=(B/r['svg']).read_text();assert '<text' not in source and 'href=' not in source
 for path,col in ns['LOGO']:assert path in source
 qa['files'].append({'file':r['png'],'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
# Entire role badge fits inside the circular avatar crop: distance(center)+outer radius < 512.
assert ((742-512)**2+(750-512)**2)**.5+157<512
qa['role_badges_circle_safe']=True
(B/'source/QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
(B/'source/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
with zipfile.ZipFile(B/'MOKO_6_аватаров_Telegram_v01.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for directory in ['png','svg']:
  for p in sorted((B/directory).iterdir()):z.write(p,p.relative_to(B))
 for f in ['MOKO_Аватары_Telegram.html','MOKO_6_аватаров_Telegram.jpg','README.txt']:z.write(B/f,f)
with zipfile.ZipFile(B/'MOKO_6_аватаров_Telegram_v01.zip') as z:assert z.testzip() is None
print('Done:',len(records),'avatars. ZIP bytes:',(B/'MOKO_6_аватаров_Telegram_v01.zip').stat().st_size)
