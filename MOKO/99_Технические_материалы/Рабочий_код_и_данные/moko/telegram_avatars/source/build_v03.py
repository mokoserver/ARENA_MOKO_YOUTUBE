from pathlib import Path
import base64,json,zipfile,hashlib,html
import cairosvg
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2]; B=R/'telegram_avatars/concept03'
for f in ['png','svg','source']:(B/f).mkdir(parents=True,exist_ok=True)
ns={};exec((R/'branding/source/build.py').read_text().split('files=[]')[0],ns)
text,mark=ns['text'],ns['mark'];W='#F7F9FC'
items=[('01_news','Новости','Новостной канал','#167DA4','news'),('02_news_chat','Чат новостей','Обсуждение публикаций','#7950AD','chat'),('03_moko_systems','MOKO Systems','Группа с разделами','#B93636','sections'),('04_moko_se_bot','MOKO SE Bot','Бот-диспетчер для MOKO SE','#087E75','se'),('05_contact_bot','Связь с MOKO','Бот для обращений к команде','#B85D1B','contact'),('06_johnny_respect','Johnny Respect','Личный бот','#172238','jr')]
records=[]
for slug,title,desc,bg,kind in items:
 fg='#F0D48C' if kind=='jr' else W
 texture=mark(66,73,225,mono=W,opacity=.10)
 s=f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024"><defs><pattern id="mokoTexture" width="360" height="310" patternUnits="userSpaceOnUse" patternTransform="rotate(-12 512 512)">{texture}</pattern><radialGradient id="shade" cx=".35" cy=".22" r=".85"><stop offset="0" stop-color="#ffffff" stop-opacity=".03"/><stop offset="1" stop-color="#07111f" stop-opacity=".26"/></radialGradient></defs><rect width="1024" height="1024" fill="{bg}"/>'
 # Broad facets follow the supplied mark; small repeated silhouettes create a brand-specific texture.
 s+=mark(-110,-105,1300,mono='#07111f',opacity=.12)
 s+='<rect width="1024" height="1024" fill="url(#mokoTexture)"/><rect width="1024" height="1024" fill="url(#shade)"/>'
 s+=f'<circle cx="512" cy="512" r="460" fill="none" stroke="{fg}" stroke-width="6" opacity=".14"/>'
 if kind=='news':
  s+=f'<rect x="238" y="232" width="548" height="444" rx="43" fill="{fg}"/><rect x="294" y="291" width="434" height="55" rx="9" fill="{bg}"/><rect x="294" y="393" width="136" height="213" rx="12" fill="{bg}"/><g stroke="{bg}" stroke-width="30" stroke-linecap="round"><path d="M484 407H714M484 497H714M484 589H714"/></g>'
 elif kind=='chat':
  s+=f'<path d="M406 242H722Q774 242 774 294V439Q774 488 722 488H684L631 541V488H406Q356 488 356 439V294Q356 242 406 242Z" fill="none" stroke="{fg}" stroke-width="35"/>'
  s+=f'<path d="M254 352H595Q649 352 649 406V559Q649 614 595 614H402L294 706V614H254Q204 614 204 559V406Q204 352 254 352Z" fill="{fg}" stroke="{bg}" stroke-width="19"/>'
  for cx in [322,426,530]:s+=f'<circle cx="{cx}" cy="480" r="22" fill="{bg}"/>'
 elif kind=='sections':
  for x in [264,532]:
   for y in [221,489]:s+=f'<rect x="{x}" y="{y}" width="228" height="228" rx="44" fill="{fg}"/>'
 elif kind=='se':
  s+=f'<g fill="{fg}" stroke="{fg}" stroke-linecap="round"><path d="M512 220V308" stroke-width="27"/><circle cx="512" cy="203" r="37"/><rect x="182" y="380" width="62" height="162" rx="23"/><rect x="780" y="380" width="62" height="162" rx="23"/><rect x="268" y="294" width="488" height="352" rx="66"/></g>'
  s+=text('SE',512,541,226,bg,'Inter',800,anchor='middle')
 elif kind=='contact':
  s+=f'<g fill="none" stroke="{fg}" stroke-width="38" stroke-linecap="round" stroke-linejoin="round"><path d="M263 466V435A249 249 0 0 1 761 435V466M748 578V626Q748 687 641 687H556"/></g><g fill="{fg}"><rect x="225" y="414" width="119" height="218" rx="47"/><rect x="680" y="414" width="119" height="218" rx="47"/><rect x="501" y="659" width="124" height="56" rx="28"/></g>'
 else:s+=text('JR',512,637,500,fg,'Jost',700,anchor='middle')
 # A shared navy footer carries the original red mark; role icons remain dominant.
 s+='<path d="M0 750L512 785L1024 750V1024H0Z" fill="#16253B"/><path d="M0 750L512 785L1024 750" fill="none" stroke="#F7F9FC" stroke-width="4" opacity=".17"/>'
 wordw=ns['tw']('MOKO',94,'Jost',500);total=118+25+wordw;x=(1024-total)/2
 s+=mark(x,811,118)+text('MOKO',x+143,888,94,W,'Jost',500)+'</svg>'
 (B/'svg'/f'{slug}.svg').write_text(s);cairosvg.svg2png(bytestring=s.encode(),write_to=str(B/'png'/f'{slug}.png'))
 records.append(dict(slug=slug,title=title,description=desc,color=bg,png=f'png/{slug}.png',svg=f'svg/{slug}.svg'))

def circle(im,n):
 im=im.convert('RGBA').resize((n,n),Image.Resampling.LANCZOS);a=Image.new('L',(n*3,n*3));ImageDraw.Draw(a).ellipse((0,0,n*3-1,n*3-1),fill=255);im.putalpha(a.resize((n,n),Image.Resampling.LANCZOS));return im
f=lambda n:ImageFont.truetype(str(R/'brand/Inter.ttf'),n)
board=Image.new('RGB',(1440,1460),'#0B1220');d=ImageDraw.Draw(board)
d.text((70,48),'MOKO / TELEGRAM · КОНЦЕПТ 03',font=f(25),fill='#A4B4C9')
d.text((70,103),'Разные роли. Фирменная фактура MOKO.',font=f(39),fill=W)
d.text((70,172),'Крупный символ · узор из знака MOKO · красный знак на тёмной базе',font=f(22),fill='#A4B4C9')
for n,r in enumerate(records):
 x=72+n%3*442;y=250+n//3*470;a=circle(Image.open(B/r['png']),322);board.paste(a,(x+38,y),a)
 d.text((x+199,y+345),r['title'],font=f(28),fill=W,anchor='mt');d.text((x+199,y+389),r['description'],font=f(17),fill='#A4B4C9',anchor='mt')
d.line((70,1210,1370,1210),fill='#2B3B52',width=2);d.text((70,1243),'Проверка в малом размере',font=f(24),fill=W)
for n,r in enumerate(records):
 a=circle(Image.open(B/r['png']),64);board.paste(a,(70+n*133,1310),a)
d.text((912,1308),'Цвет и символ — разные.\nФактура и подпись — общие.',font=f(21),fill='#A4B4C9',spacing=10)
board.save(B/'MOKO_Telegram_Концепт_03.jpg',quality=94,optimize=True)

def uri(r):return 'data:image/svg+xml;base64,'+base64.b64encode((B/r['svg']).read_bytes()).decode()
css='''*{box-sizing:border-box}body{margin:0;background:#0b1220;color:#f7f9fc;font:16px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}main{max-width:1050px;margin:auto;padding:30px 20px 50px}.eyebrow{color:#a4b4c9;font-size:11px;letter-spacing:.16em}h1{font-size:clamp(31px,5vw,49px);line-height:1.08;margin:18px 0}h2{font-size:25px;margin-top:38px}p{color:#a4b4c9}.intro{max-width:720px}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:28px}.card{padding:22px 15px;background:#121e30;border:1px solid #293a52;border-radius:18px;text-align:center}.open{border:0;border-radius:50%;background:transparent;padding:0;cursor:zoom-in;max-width:100%}.open img{display:block;width:230px;max-width:100%;border-radius:50%}h3{margin:16px 0 4px;font-size:18px}.card p{font-size:13px;margin:0;min-height:40px}.list{max-width:620px;border:1px solid #293a52;background:#121e30;border-radius:15px;padding:0 16px}.row{display:flex;gap:13px;align-items:center;border-bottom:1px solid #293a52;padding:14px 0}.row:last-child{border:0}.row img{width:48px;height:48px;border-radius:50%}.row p{font-size:12px;margin:3px 0}.row strong{font-size:15px}.small{display:flex;gap:15px;flex-wrap:wrap;padding:20px 0}.small img{width:40px;height:40px;border-radius:50%}.note{border-left:3px solid #f0d48c;padding:10px 15px;background:#121e30;font-size:14px}.foot{margin-top:36px;border-top:1px solid #293a52;padding-top:18px;color:#8297b3;font-size:12px}dialog{background:#0b1220;color:white;border:1px solid #52647f;border-radius:14px;max-width:94vw;max-height:94vh;padding:12px}dialog::backdrop{background:#000d}dialog img{display:block;max-width:86vw;max-height:76vh;width:auto;height:auto;margin:12px auto;border-radius:50%}.bar{display:flex;align-items:center;justify-content:space-between;gap:14px}#close{padding:9px 13px;background:#182943;color:white;border:1px solid #52647f;border-radius:8px;cursor:pointer}@media(max-width:680px){.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.card{padding:14px 9px;border-radius:13px}h3{font-size:15px}.card p{font-size:12px;min-height:53px}main{padding:25px 16px}.open img{width:160px}}'''
s='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MOKO Telegram — концепт 03</title><style>'+css+'</style></head><body><main><div class="eyebrow">MOKO / TELEGRAM · КОНЦЕПТ 03</div><h1>Разные роли.<br>Фирменная фактура MOKO.</h1><p class="intro">Крупные символы и цвета из второго концепта сохранены. Добавлен узор из исходного знака MOKO, крупные геометрические грани и общая тёмная нижняя часть с красным знаком. Не универсальный шум, а фирменная фактура.</p><p class="note">Нажмите на аватар, чтобы увеличить. Картинки показаны в круглой обрезке; файлы PNG для установки остаются квадратными.</p><div class="grid">'
for r in records:s+=f'<article class="card"><button class="open" aria-label="Увеличить {r["title"]}"><img src="{uri(r)}" alt="{r["title"]}"></button><h3>{r["title"]}</h3><p>{r["description"]}</p></article>'
s+='</div><h2>Проверка в списке чатов · 48 px</h2><p>Условный список с вымышленными соседними чатами, не снимок вашего Telegram. Помогает сравнить MOKO с другими аватарами.</p><div class="list">'
for n,r in enumerate(records):
 s+=f'<div class="row"><img src="{uri(r)}" alt=""><div><strong>{r["title"]}</strong><p>{r["description"]}</p></div></div>'
 if n in [0,2,4]:
  col,initial,lab={0:('#55785c','А','Личный контакт · пример'),2:('#556f89','Д','Другой канал · пример'),4:('#9a6570','Ч','Другой чат · пример')}[n]
  s+=f'<div class="row"><span style="display:grid;place-items:center;width:48px;height:48px;flex-shrink:0;border-radius:50%;background:{col};font-weight:650">{initial}</span><div><strong>{lab}</strong><p>Вымышленный сосед для проверки</p></div></div>'
s+='</div><h2>Ещё меньше · 40 px</h2><div class="small">'+''.join(f'<img src="{uri(r)}" alt="{r["title"]}">' for r in records)+'</div><p class="note">Голубая газета — новости. Фиолетовые диалоги — чат. Красная сетка — группа с разделами. Бирюзовый робот SE — диспетчер. Оранжевая гарнитура — связь с командой. Тёмный фон с золотистыми JR — Johnny Respect.</p><h2>Что в комплекте</h2><p>Шесть PNG 1024 × 1024, шесть SVG в контурах, общий обзор и эта автономная презентация. На нижней тёмной части стоит исходный красный знак MOKO. Фоновый узор повторяет его геометрию в полупрозрачном одноцветном варианте. Гарнитура обозначает связь, а не наличие функции звонков.</p><p>Названия — подписи для выбора файла, а не требование переименовать паблики. Предыдущие концепты сохранены отдельно. Ничего не опубликовано.</p><footer class="foot">Концепт 03 · На согласование · 09.09.2026</footer></main><dialog id="zoom"><div class="bar"><span id="caption"></span><button id="close">Закрыть ✕</button></div><img id="large" alt=""></dialog><script>const d=document.getElementById("zoom"),im=document.getElementById("large");document.querySelectorAll(".open").forEach(b=>b.onclick=()=>{const s=b.querySelector("img");im.src=s.src;im.alt=s.alt;document.getElementById("caption").textContent=s.alt;d.showModal()});document.getElementById("close").onclick=()=>d.close();d.onclick=e=>{if(e.target===d)d.close()};</script></body></html>'
(B/'MOKO_Telegram_Концепт_03.html').write_text(s)
readme='MOKO / TELEGRAM — КОНЦЕПТ 03\nНа согласование\n\nРазвитие концепта 02: крупные символы и индивидуальные цвета сохранены. Добавлена фирменная фактура из геометрии исходного знака MOKO, крупные грани и общая тёмная нижняя часть с оригинальным красным знаком и светлой надписью MOKO. В малом размере основными ориентирами остаются символ роли, цвет и общая нижняя полоса; мелкий узор не должен быть единственным способом узнавания.\n\n'
for r in records:readme+=r['png']+' — '+r['title']+'; '+r['description']+'.\n'
readme+='\nPNG: 1024 × 1024, квадратные файлы для установки. Круг формируется при отображении в Telegram; не приближать изображение дополнительно. SVG — векторы с текстом в контурах. JPG — общий обзор; HTML — просмотр отдельных аватаров и малых размеров.\n\nПредыдущие концепты сохранены отдельно. Названия в презентации служат для выбора файлов. Ничего не установлено на площадках. Гарнитура обозначает связь с командой, а не функцию звонков.\n'
(B/'README.txt').write_text(readme)
q={'concept':3,'status':'awaiting_approval','published':False,'files':[]}
for r in records:
 p=B/r['png'];im=Image.open(p);assert im.size==(1024,1024);im.verify();svg=(B/r['svg']).read_text();assert '<text' not in svg and 'href=' not in svg
 q['files'].append({'file':r['png'],'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(B/'source/QA.json').write_text(json.dumps(q,indent=2));(B/'source/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
with zipfile.ZipFile(B/'MOKO_Telegram_Концепт_03.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for sub in ['png','svg']:
  for p in sorted((B/sub).iterdir()):z.write(p,p.relative_to(B))
 for name in ['MOKO_Telegram_Концепт_03.html','MOKO_Telegram_Концепт_03.jpg','README.txt']:z.write(B/name,name)
with zipfile.ZipFile(B/'MOKO_Telegram_Концепт_03.zip') as z:assert z.testzip() is None
print('Concept 03 ready:',(B/'MOKO_Telegram_Концепт_03.zip').stat().st_size,'bytes')
