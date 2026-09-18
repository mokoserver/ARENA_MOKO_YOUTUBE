"""Emoji set for the main MOKO Telegram group: dark circles, light graphics.
Deliberately opposite to the light style B of the channel set. 18 emoji.
"""
from pathlib import Path
import base64, csv, hashlib, io, json, re, zipfile
import cairosvg
from PIL import Image, ImageDraw, ImageFont
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'00_НАЧНИТЕ_ЗДЕСЬ.md').exists())
B = ROOT/'02_Telegram/04_Эмодзи_Главная_группа'
SRC = Path(__file__).resolve().parent
for d in ('png_100','webp_100','svg'): (B/d).mkdir(parents=True, exist_ok=True)
INK='#17263A'; PAPER='#F2F0E8'; RING='#31435C'
RED='#D64545'; BLUE='#2587B3'; ORANGE='#C7772D'; GREEN='#91B943'; GOLD='#C59D32'; PURPLE='#8C64B2'; TEAL='#238F83'; MAGENTA='#C13E7A'
def st(d,w=4.6,c=PAPER):return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
MARK='<path d="M160 4.27406L271 154.274L176 192.274L160 4.27406Z" fill="#b93636"/><path d="M94.8938 0L127.894 44L101.894 82L94.8938 0Z" fill="#b93636"/><path d="M160 4.27406L176 192.274L53 163.274L160 4.27406Z" fill="#d64545"/><path d="M93.5 2.27405L58 147.274L0 132.274L93.5 2.27405Z" fill="#d64545"/><path d="M95 0.274048L102 81.774L58 147.274L0 132.274L95 0.274048Z" fill="#d64545"/>'
rows=[]
def add(slug,title,emoji,accent,body):rows.append(dict(slug=slug,title=title,emoji=emoji,accent=accent,body=body))
add('01_about','О проекте','🔺',RED,f'<g transform="translate(22.5 30.5) scale(0.203)">{MARK}</g>')
add('02_news','Новости','📰',BLUE,st('M28 34H64V70H32Q28 70 28 66Z')+st('M64 44H72V66Q72 70 68 70H64',4.2)+f'<path d="M35 44H57M35 52H57M35 60H49" stroke="{BLUE}" stroke-width="3.6" stroke-linecap="round"/>')
add('03_forum','Форум','💬',TEAL,st('M26 30H58Q62 30 62 34V48Q62 52 58 52H40L32 60V52H26Q22 52 22 48V34Q22 30 26 30Z')+f'<circle cx="34" cy="41" r="2.6" fill="{TEAL}"/><circle cx="42" cy="41" r="2.6" fill="{TEAL}"/><circle cx="50" cy="41" r="2.6" fill="{TEAL}"/><path d="M66 44H74Q78 44 78 48V58Q78 62 74 62H72V68L65 62H52" fill="none" stroke="{PAPER}" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/>')
add('04_soft','Софт','🖥️',GREEN,st('M27 30H73V70H27Z',4.4)+st('M27 40H73',4.4)+f'<circle cx="34" cy="35" r="2.4" fill="{GREEN}"/><circle cx="41" cy="35" r="2.4" fill="{GREEN}"/>'+st('M58 50V46M58 66V70M48 58H44M72 58H68M51 51L48 48M65 65L68 68M65 51L68 48M51 65L48 68',3.4,GREEN)+f'<circle cx="58" cy="58" r="7.5" fill="none" stroke="{GREEN}" stroke-width="4"/><circle cx="58" cy="58" r="2.2" fill="{PAPER}"/>')
add('05_docs','Документация','📄',GOLD,st('M34 26H56L66 36V74H34Z')+st('M56 26V36H66',4)+f'<path d="M41 46H59M41 54H59M41 62H52" stroke="{GOLD}" stroke-width="3.6" stroke-linecap="round"/>')
add('06_lifehack','Лайфхаки','✨',MAGENTA,st('M30 70L60 40',5)+st('M60 40L64 36',5)+st('M70 22V34M64 28H76',3.8,MAGENTA)+st('M40 30V36M37 33H43',3,MAGENTA)+f'<circle cx="30" cy="70" r="3.4" fill="{MAGENTA}"/>')
add('07_projects','Проекты','📐',ORANGE,st('M50 24L76 38V62L50 76L24 62V38Z')+st('M50 24V50M24 38L50 50L76 38M50 76V50',3.6)+f'<circle cx="50" cy="50" r="3" fill="{ORANGE}"/>')
add('08_books','Литература','📚',PURPLE,st('M50 32C43 26 33 26 28 29V68C33 65 43 65 50 71C57 65 67 65 72 68V29C67 26 57 26 50 32Z')+st('M50 32V71',4)+f'<path d="M35 38C39 36 43 36 45 38M35 46C39 44 43 44 45 46M55 38C59 36 63 36 65 38" stroke="{PURPLE}" stroke-width="3" stroke-linecap="round" fill="none"/>')
add('09_gallery','Галерея','🖼️',TEAL,st('M27 30H73V70H27Z')+st('M32 62L44 47L52 57L60 45L68 62',4,TEAL)+f'<circle cx="62" cy="39" r="4" fill="{TEAL}"/>')
add('10_drivers','Драйвера','🔌',ORANGE,st('M42 24V36M58 24V36',5)+st('M34 36H66V48Q66 60 50 64Q34 60 34 48Z')+st('M50 64V76',5,ORANGE))
add('11_suggest','Предложения','📮',GREEN,st('M30 50H70V72H30Z')+st('M26 50H74',4.4)+st('M44 50V46Q44 42 50 42Q56 42 56 46V50',4)+f'<rect x="45" y="26" width="10" height="16" rx="2" fill="none" stroke="{GREEN}" stroke-width="3.6"/><path d="M48 33L50 36L54 30" stroke="{GREEN}" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
add('12_code','Код','💻',GREEN,st('M27 30H73V70H27Z',4.4)+st('M35 44L43 51L35 58',4.6,GREEN)+st('M49 58H61',4.6))
add('13_video','Видео','🎬',RED,st('M28 44H72V70H28Z')+st('M28 44L33 30H77L72 44')+f'<path d="M40 31L36 43M52 31L48 43M64 31L60 43" stroke="{RED}" stroke-width="4" stroke-linecap="round"/>')
add('14_archive','Архив','🗃️',GOLD,st('M30 46H70V72H30Z')+st('M26 34H74V46H26Z',4.4)+st('M44 54H56',5,GOLD))
add('15_live','Эфир','📡',RED,st('M50 76V50',5)+f'<circle cx="50" cy="45" r="5" fill="{PAPER}"/>'+st('M39 34Q30 45 39 56M61 34Q70 45 61 56',4,RED)+st('M31 27Q18 45 31 63M69 27Q82 45 69 63',3.4,RED))
add('16_question','Вопрос','❓',BLUE,st('M28 30H72Q76 30 76 36V54Q76 60 72 60H46L36 70V60H28Q24 60 24 54V36Q24 30 28 30Z')+st('M45 42Q45 36 50 36Q56 36 56 42Q56 47 50 49V53',4,BLUE)+f'<circle cx="50" cy="58" r="2.6" fill="{BLUE}"/>')
add('17_tests','Испытания','🧪',MAGENTA,st('M30 64Q30 40 50 40Q70 40 70 64',4.6)+st('M50 62L62 48',5,MAGENTA)+f'<circle cx="50" cy="62" r="3.2" fill="{MAGENTA}"/>'+st('M36 52L39 55M64 52L61 55M50 46V50',3))
add('18_moko_se','MOKO SE','📏',TEAL,st('M26 40H74V50H26Z',4.4)+st('M32 50V66M40 50V60',4.4)+f'<rect x="56" y="34" width="12" height="22" rx="3" fill="none" stroke="{TEAL}" stroke-width="4"/><path d="M46 45H52" stroke="{TEAL}" stroke-width="3.4" stroke-linecap="round"/>')
for r in rows:
 s='<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="'+INK+'"/><circle cx="50" cy="50" r="46" fill="none" stroke="'+RING+'" stroke-width="1.4"/><circle cx="50" cy="50" r="41.5" fill="none" stroke="'+r['accent']+'" stroke-width="1.2" opacity="0.55" stroke-dasharray="1.5 5.2"/>'+r['body']+'</svg>'
 (B/'svg'/f'{r["slug"]}.svg').write_text(s)
 raw=cairosvg.svg2png(bytestring=s.encode(),output_width=400,output_height=400)
 im=Image.open(io.BytesIO(raw)).convert('RGBA').resize((100,100),Image.Resampling.LANCZOS)
 im.save(B/'png_100'/f'{r["slug"]}.png',optimize=True)
 im.save(B/'webp_100'/f'{r["slug"]}.webp',lossless=True,method=6)
 r['file']=f'png_100/{r["slug"]}.png';r['svg']=f'svg/{r["slug"]}.svg';r['webp']=f'webp_100/{r["slug"]}.webp'
def font(n):return ImageFont.truetype(str(ROOT/'05_Бренд_MOKO/03_Шрифты/Inter.ttf'),n)
board=Image.new('RGB',(1440,1160),'#F2F0E8');d=ImageDraw.Draw(board)
d.text((70,44),'MOKO / ГЛАВНАЯ ГРУППА · CUSTOM EMOJI · V01',font=font(24),fill='#5B6B80')
d.text((70,99),'Разделы главной группы',font=font(45),fill='#17263A')
d.text((70,167),'18 эмодзи · тёмный круг и светлая графика · отлично от набора канала',font=font(22),fill='#5B6B80')
for n,r in enumerate(rows):
 x=70+n%6*218;y=244+n//6*210
 a=Image.open(io.BytesIO(cairosvg.svg2png(url=str(B/r['svg']),output_width=130,output_height=130))).convert('RGBA');board.paste(a,(x+33,y),a)
 d.text((x+98,y+142),r['title'],font=font(21),fill='#17263A',anchor='mt')
 d.text((x+98,y+174),r['slug'][:2],font=font(13),fill='#7A8AA0',anchor='mt')
d.line((70,932,1370,932),fill='#C9CFD6',width=2)
d.text((70,960),'Примеры в строке сообщения',font=font(23),fill='#17263A')
x=70;y=1020
for txt,ids in [('Новости ',[1]),('  Документация ',[4]),('  Эфир ',[14]),('  В архив ',[13])]:
 d.text((x,y),txt,font=font(25),fill='#2A3A50');x+=d.textlength(txt,font=font(25))
 for i in ids:
  a=Image.open(B/rows[i]['file']).convert('RGBA').resize((28,28),Image.Resampling.LANCZOS);board.paste(a,(round(x),y+2),a);x+=34
board.save(B/'MOKO_Группа_Превью.jpg',quality=93,optimize=True)
def data(rel):
 p=B/rel;mime='image/svg+xml' if p.suffix=='.svg' else 'image/png'
 return 'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
css='''*{box-sizing:border-box}body{margin:0;background:#f2f0e8;color:#17263a;font:16px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}main{max-width:1100px;margin:auto;padding:30px 22px 55px}.eyebrow{color:#5b6b80;font-size:11px;letter-spacing:.13em}h1{font-size:clamp(31px,5vw,46px);line-height:1.1;margin:18px 0}h2{font-size:25px;margin-top:35px}p{color:#5b6b80}.grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;margin:26px 0}.card{background:#fff;border:1px solid #d8d5cc;padding:13px 8px;border-radius:14px;text-align:center}.open{padding:0;border:0;background:none;cursor:zoom-in;max-width:100%}.open img{display:block;width:110px;max-width:100%;height:auto}.card strong{display:block;font-size:13px;margin-top:8px}.card small{font-size:10px;color:#7a8aa0}.tests{display:grid;grid-template-columns:1fr 1fr;gap:16px}.test{padding:20px;border-radius:14px;background:#182b41;color:#f2f5fa}.test.light{background:#fff;color:#17263a;border:1px solid #d8d5cc}.test p{color:inherit;margin:15px 0;font-size:17px}.inline{display:inline-block;width:22px;height:22px;vertical-align:-5px;margin:0 2px}.bigline .inline{width:28px;height:28px;vertical-align:-7px}.strip{display:flex;gap:7px;flex-wrap:wrap;margin:15px 0}.strip img{width:22px;height:22px}.note{padding:12px 16px;border-left:3px solid #b93636;background:#fff;font-size:14px;color:#3a4a60}li{margin:8px 0;color:#5b6b80}.foot{border-top:1px solid #d8d5cc;margin-top:32px;padding-top:18px;font-size:12px;color:#7a8aa0}dialog{max-width:94vw;max-height:94vh;padding:15px;background:#142137;color:white;border:1px solid #516781;border-radius:16px}dialog::backdrop{background:#000d}dialog img{display:block;width:300px;max-width:80vw;height:auto;margin:18px auto}.bar{display:flex;justify-content:space-between;align-items:center;gap:14px}#close{padding:10px 12px;color:white;background:#1b2c45;border:1px solid #516781;border-radius:8px;cursor:pointer}@media(max-width:650px){main{padding:25px 16px}.grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:9px}.card{padding:10px 5px}.card strong{font-size:12px}.open img{width:90px}.tests{grid-template-columns:1fr}}'''
s='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MOKO — эмодзи главной группы</title><style>'+css+'</style></head><body><main><div class="eyebrow">MOKO / ГЛАВНАЯ ГРУППА · CUSTOM EMOJI · V01</div><h1>Разделы<br>главной группы.</h1><p>18 статичных эмодзи для разделов: О проекте, Новости, Форум, Софт, Документация, Лайфхаки, Проекты, Литература, Галерея, Драйвера, Предложения, Код, Видео, Архив + Эфир, Вопрос, Испытания, MOKO SE.</p><p class="note">Стиль намеренно отличается от набора канала: тёмный круг и светлая графика вместо светлой основы с диагональю. Нажмите на значок, чтобы рассмотреть.</p><div class="grid">'
for r in rows:s+=f'<article class="card"><button class="open" aria-label="Увеличить: {r["title"]}"><img src="{data(r["svg"])}" alt="{r["title"]}"></button><strong>{r["title"]}</strong><small>{r["slug"][:2]}</small></article>'
s+='</div><h2>Проверка в сообщениях</h2><p>Реальные PNG 100 × 100 в размере 22 и 28 пикселей на двух фонах.</p><div class="tests">'
def inline(i):return f'<img class="inline" src="{data(rows[i]["file"])}" alt="{rows[i]["title"]}">'
for theme in ['','light']:
 s+=f'<div class="test {theme}"><b>{"Тёмная тема" if theme else "Светлая тема"}</b><p>Новости {inline(1)} Документация {inline(4)}</p><p>Эфир скоро {inline(14)} Вопрос {inline(15)}</p><p>Софт {inline(3)} Драйвера {inline(9)}</p><p class="bigline">О проекте {inline(0)} Испытания {inline(16)} В архив {inline(13)}</p><div class="strip">'+''.join(f'<img src="{data(r["file"])}" alt="{r["title"]}">' for r in rows)+'</div></div>'
s+='</div><h2>Что подготовлено</h2><ul><li>18 PNG 100 × 100 с прозрачностью вокруг круга — для загрузки.</li><li>18 WebP без потерь — альтернатива, не дополнительные эмодзи.</li><li>18 SVG — исходники для правок.</li><li>CSV привязки к обычным эмодзи и README с порядком загрузки через @Stickers.</li></ul><p class="note">Набор не опубликован: загрузка через @Stickers. Использование кастомных эмодзи зависит от Telegram Premium и контекста.</p><footer class="foot">Версия 01 для главной группы MOKO. «О проекте» использует исходный фирменный знак MOKO.</footer></main><dialog id="zoom"><div class="bar"><span id="caption"></span><button id="close">Закрыть ✕</button></div><img id="large" alt=""></dialog><script>const d=document.getElementById("zoom"),im=document.getElementById("large");document.querySelectorAll(".open").forEach(b=>b.onclick=()=>{const a=b.querySelector("img");im.src=a.src;im.alt=a.alt;document.getElementById("caption").textContent=a.alt;d.showModal()});document.getElementById("close").onclick=()=>d.close();d.onclick=e=>{if(e.target===d)d.close()};</script></body></html>'
assets={}
def dedup(m):
 v=m.group(1)
 if v not in assets:assets[v]='p'+str(len(assets))
 return 'data-png="'+assets[v]+'"'
s=re.sub(r'src="(data:image/png;base64,[^"]+)"',dedup,s)
lookup={k:v for v,k in assets.items()}
s=s.replace('</body>','<script>const PNGS='+json.dumps(lookup)+';document.querySelectorAll("img[data-png]").forEach(i=>i.src=PNGS[i.dataset.png]);</script></body>')
(B/'MOKO_Группа_Просмотр.html').write_text(s)
with (B/'Привязка_эмодзи_группы.csv').open('w',encoding='utf-8-sig',newline='') as fp:
 w=csv.writer(fp,delimiter=';');w.writerow(['№','Файл PNG','Название','Обычный эмодзи для привязки'])
 for i,r in enumerate(rows,1):w.writerow([i,r['file'],r['title'],r['emoji']])
(B/'README.md').write_text('''# MOKO — эмодзи главной группы Telegram

Версия 01 · 18 статичных эмодзи · на согласование

Отдельный набор для главной группы. Стиль отличается от набора канала (светлый круг с диагональю): здесь **тёмный круг со светлой графикой** и цветным пунктирным кольцом раздела, чтобы наборы не смешивались.

## Разделы
О проекте (фирменный знак MOKO), Новости, Форум, Софт, Документация, Лайфхаки, Проекты, Литература, Галерея, Драйвера, Предложения, Код, Видео, Архив — по вашей структуре; плюс добавлены по контексту канала: **Эфир, Вопрос, Испытания, MOKO SE**.

## Форматы
- `png_100/` — комплект для загрузки, PNG 100 × 100 RGBA.
- `webp_100/` — альтернативные копии без потерь; используйте либо PNG, либо WebP.
- `svg/` — векторные исходники.
- `Привязка_эмодзи_группы.csv` — рекомендуемые обычные эмодзи для привязки в @Stickers.

## Загрузка
Через @Stickers: `/newemojipack`, статичный набор, файлы из `png_100/` отправляйте как документы без сжатия, привязка по CSV. Пак не опубликован; использование кастомных эмодзи зависит от Telegram Premium и контекста отправки.
''')
manifest=[{k:v for k,v in r.items() if k!='body'} for r in rows]
(SRC/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
qa={'count':18,'style':'dark_circle','size':[100,100],'published':False,'files':[]}
for r in rows:
 p=B/r['file'];im=Image.open(p).convert('RGBA')
 assert im.size==(100,100) and im.getchannel('A').getextrema()==(0,255) and im.getpixel((0,0))[3]==0
 assert Image.open(B/r['webp']).size==(100,100)
 assert '<text' not in (B/r['svg']).read_text()
 qa['files'].append({'file':r['file'],'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(SRC/'QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
with zipfile.ZipFile(B/'MOKO_18_эмодзи_группа_v01.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for folder in ('png_100','webp_100','svg'):
  for p in sorted((B/folder).glob('*')):z.write(p,p.relative_to(B))
 for name in ('MOKO_Группа_Превью.jpg','MOKO_Группа_Просмотр.html','Привязка_эмодзи_группы.csv','README.md'):z.write(B/name,name)
with zipfile.ZipFile(B/'MOKO_18_эмодзи_группа_v01.zip') as z:assert z.testzip() is None and len(z.namelist())==58
print(json.dumps({'count':18,'max_png_bytes':max(x['bytes'] for x in qa['files']),'zip':(B/'MOKO_18_эмодзи_группа_v01.zip').stat().st_size},ensure_ascii=False))
