"""Group emoji v02: bigger, bolder, filled glyphs for 22px readability.
Same dark-circle identity, same 18 sections, replaces v01 pixels in place.
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
def st(d,w=6,c=PAPER):return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
MARK='<path d="M160 4.27406L271 154.274L176 192.274L160 4.27406Z" fill="#b93636"/><path d="M94.8938 0L127.894 44L101.894 82L94.8938 0Z" fill="#b93636"/><path d="M160 4.27406L176 192.274L53 163.274L160 4.27406Z" fill="#d64545"/><path d="M93.5 2.27405L58 147.274L0 132.274L93.5 2.27405Z" fill="#d64545"/><path d="M95 0.274048L102 81.774L58 147.274L0 132.274L95 0.274048Z" fill="#d64545"/>'
rows=[]
def add(slug,title,emoji,accent,body):rows.append(dict(slug=slug,title=title,emoji=emoji,accent=accent,body=body))
add('01_about','О проекте','🔺',RED,f'<g transform="translate(14.8 24.9) scale(0.26)">{MARK}</g>')
add('02_news','Новости','📰',BLUE,f'<rect x="26" y="28" width="48" height="44" rx="5" fill="{PAPER}"/><rect x="32" y="35" width="20" height="12" rx="2" fill="{BLUE}"/><path d="M32 54H68M32 61H68M32 68H56" stroke="{INK}" stroke-width="4.2" stroke-linecap="round"/>')
add('03_forum','Форум','💬',TEAL,f'<path d="M24 28H60Q65 28 65 33V49Q65 54 60 54H43L32 64V54H24Q19 54 19 49V33Q19 28 24 28Z" fill="{PAPER}"/><circle cx="32" cy="41" r="3.6" fill="{INK}"/><circle cx="42" cy="41" r="3.6" fill="{INK}"/><circle cx="52" cy="41" r="3.6" fill="{INK}"/><path d="M69 42H76Q81 42 81 47V59Q81 64 76 64H74V72L65 64H56Z" fill="{TEAL}"/>')
add('04_soft','Софт','🖥️',GREEN,f'<rect x="24" y="27" width="52" height="44" rx="6" fill="{PAPER}"/><path d="M24 38H76" stroke="{INK}" stroke-width="4.5"/><circle cx="32" cy="32.5" r="2.8" fill="{RED}"/><circle cx="40" cy="32.5" r="2.8" fill="{GOLD}"/><g transform="translate(61 57)"><path d="M0 -14V-10M0 10V14M-14 0H-10M10 0H14M-10 -10L-7 -7M7 7L10 10M10 -10L7 -7M-7 7L-10 10" stroke="{GREEN}" stroke-width="5" stroke-linecap="round"/><circle r="9.5" fill="{GREEN}"/><circle r="3.6" fill="{INK}"/></g>')
add('05_docs','Документация','📄',GOLD,f'<path d="M32 24H57L69 36V76H32Z" fill="{PAPER}"/><path d="M57 24L69 36H57Z" fill="{GOLD}"/><path d="M40 47H61M40 55H61M40 63H53" stroke="{INK}" stroke-width="4.4" stroke-linecap="round"/>')
add('06_lifehack','Лайфхаки','✨',MAGENTA,f'<circle cx="50" cy="44" r="17.5" fill="{PAPER}"/><path d="M43 59H57V67Q57 72 50 72Q43 72 43 67Z" fill="{PAPER}"/><path d="M44 63H56M45 67.5H55" stroke="{INK}" stroke-width="2.8"/><path d="M44 44Q47 38 50 44Q53 50 56 44" stroke="{INK}" stroke-width="3.2" fill="none" stroke-linecap="round"/><path d="M50 20V13M29 29L24 24M71 29L76 24M24 46H17M76 46H83" stroke="{MAGENTA}" stroke-width="5" stroke-linecap="round"/>')
add('07_projects','Проекты','📐',ORANGE,st('M50 21L79 37V63L50 79L21 63V37Z',6.5)+st('M21 37L50 52L79 37M50 52V79',5)+f'<circle cx="50" cy="52" r="3.6" fill="{ORANGE}"/>')
add('08_books','Литература','📚',PURPLE,f'<path d="M50 30C42 23 29 23 24 27V71C29 67 42 67 50 74C58 67 71 67 76 71V27C71 23 58 23 50 30Z" fill="{PAPER}"/><path d="M50 30V74" stroke="{INK}" stroke-width="4.5"/><path d="M31 37C35 35 42 35 45 37M31 45C35 43 42 43 45 45M31 53C35 51 42 51 45 53M55 37C59 35 66 35 69 37M55 45C59 43 66 43 69 45M55 53C59 51 66 51 69 53" stroke="{PURPLE}" stroke-width="3.6" fill="none" stroke-linecap="round"/>')
add('09_gallery','Галерея','🖼️',TEAL,f'<rect x="24" y="27" width="52" height="46" rx="6" fill="{PAPER}"/><rect x="30" y="33" width="40" height="34" rx="3" fill="{INK}"/><path d="M33 61L45 45L52 54L60 42L67 61Z" fill="{TEAL}"/><circle cx="61" cy="39" r="4.6" fill="{TEAL}"/>')
add('10_drivers','Драйвера','🔌',ORANGE,st('M40 18V32M60 18V32',7)+f'<path d="M31 32H69V47Q69 62 50 67Q31 62 31 47Z" fill="{PAPER}"/>'+st('M50 67V82',7,ORANGE))
add('11_suggest','Предложения','📮',GREEN,f'<g transform="rotate(-8 50 31)"><rect x="43" y="20" width="14" height="22" rx="2.5" fill="{GREEN}"/><path d="M46.5 29L49 32.5L54 25.5" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g><rect x="23" y="42" width="54" height="11" rx="3.5" fill="{PAPER}"/><rect x="28" y="53" width="44" height="22" rx="4" fill="{PAPER}"/><rect x="42" y="45.5" width="16" height="4.5" rx="2.2" fill="{INK}"/>')
add('12_code','Код','💻',GREEN,st('M37 30L20 50L37 70',7.5)+st('M63 30L80 50L63 70',7.5)+st('M56 24L44 76',6.5,GREEN))
add('13_video','Видео','🎬',RED,f'<path d="M25 46L31 28H79L73 46Z" fill="{PAPER}"/><path d="M39 30L35 44M53 30L49 44M67 30L63 44" stroke="{RED}" stroke-width="5.5" stroke-linecap="round"/><rect x="25" y="46" width="50" height="27" rx="5" fill="{PAPER}"/><path d="M45 52L61 59.5L45 67Z" fill="{INK}"/>')
add('14_archive','Архив','🗃️',GOLD,f'<rect x="23" y="28" width="54" height="15" rx="4" fill="{PAPER}"/><rect x="28" y="47" width="44" height="28" rx="5" fill="{PAPER}"/><rect x="42" y="55" width="16" height="6" rx="3" fill="{GOLD}"/>')
add('15_live','Эфир','📡',RED,st('M50 80V52',7)+f'<circle cx="50" cy="45" r="7" fill="{PAPER}"/>'+st('M38 33Q27 45 38 57M62 33Q73 45 62 57',6,RED)+st('M30 25Q15 45 30 65M70 25Q85 45 70 65',5,RED))
add('16_question','Вопрос','❓',BLUE,f'<path d="M26 26H74Q79 26 79 32V54Q79 60 74 60H48L36 72V60H26Q21 60 21 54V32Q21 26 26 26Z" fill="{PAPER}"/><path d="M43 39Q43 31 50 31Q58 31 58 39Q58 45 50 47.5V51" stroke="{BLUE}" stroke-width="6" fill="none" stroke-linecap="round"/><circle cx="50" cy="57.5" r="3.8" fill="{BLUE}"/>')
add('17_tests','Испытания','🧪',MAGENTA,st('M27 67Q27 37 50 37Q73 37 73 67',6.5)+st('M50 65L65 48',7,MAGENTA)+f'<circle cx="50" cy="65" r="4.5" fill="{MAGENTA}"/>'+st('M33 52L38 57M67 52L62 57M50 43V49',4.5))
add('18_moko_se','MOKO SE','📏',TEAL,f'<rect x="21" y="37" width="58" height="11" rx="3.5" fill="{PAPER}"/><path d="M29 40V45M37 40V45M45 40V45M53 40V45M61 40V45M69 40V45" stroke="{INK}" stroke-width="2.6"/><rect x="25" y="48" width="9" height="22" rx="2.5" fill="{PAPER}"/><rect x="53" y="30" width="13" height="18" rx="3.5" fill="{TEAL}"/><rect x="56.5" y="48" width="6" height="15" rx="2" fill="{TEAL}"/>')
for r in rows:
 s='<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="'+INK+'"/><circle cx="50" cy="50" r="46" fill="none" stroke="'+RING+'" stroke-width="1.4"/>'+r['body']+'</svg>'
 (B/'svg'/f'{r["slug"]}.svg').write_text(s)
 raw=cairosvg.svg2png(bytestring=s.encode(),output_width=400,output_height=400)
 im=Image.open(io.BytesIO(raw)).convert('RGBA').resize((100,100),Image.Resampling.LANCZOS)
 im.save(B/'png_100'/f'{r["slug"]}.png',optimize=True)
 im.save(B/'webp_100'/f'{r["slug"]}.webp',lossless=True,method=6)
 r['file']=f'png_100/{r["slug"]}.png';r['svg']=f'svg/{r["slug"]}.svg';r['webp']=f'webp_100/{r["slug"]}.webp'
def font(n):return ImageFont.truetype(str(ROOT/'05_Бренд_MOKO/03_Шрифты/Inter.ttf'),n)
board=Image.new('RGB',(1440,1160),'#F2F0E8');d=ImageDraw.Draw(board)
d.text((70,44),'MOKO / ГЛАВНАЯ ГРУППА · CUSTOM EMOJI · V02',font=font(24),fill='#5B6B80')
d.text((70,99),'Разделы главной группы',font=font(45),fill='#17263A')
d.text((70,167),'18 эмодзи · крупные контрастные знаки · читается в 22 px',font=font(22),fill='#5B6B80')
for n,r in enumerate(rows):
 x=70+n%6*218;y=244+n//6*210
 a=Image.open(io.BytesIO(cairosvg.svg2png(url=str(B/r['svg']),output_width=130,output_height=130))).convert('RGBA');board.paste(a,(x+33,y),a)
 d.text((x+98,y+142),r['title'],font=font(21),fill='#17263A',anchor='mt')
 d.text((x+98,y+174),r['slug'][:2],font=font(13),fill='#7A8AA0',anchor='mt')
d.line((70,932,1370,932),fill='#C9CFD6',width=2)
d.text((70,960),'Примеры в строке сообщения',font=font(23),fill='#17263A')
x=70;y=1020
for txt,ids in [('Новости ',[1]),('  Софт ',[3]),('  Эфир ',[14]),('  В архив ',[13])]:
 d.text((x,y),txt,font=font(25),fill='#2A3A50');x+=d.textlength(txt,font=font(25))
 for i in ids:
  a=Image.open(B/rows[i]['file']).convert('RGBA').resize((28,28),Image.Resampling.LANCZOS);board.paste(a,(round(x),y+2),a);x+=34
board.save(B/'MOKO_Группа_Превью.jpg',quality=93,optimize=True)
def data(rel):
 p=B/rel;mime='image/svg+xml' if p.suffix=='.svg' else 'image/png'
 return 'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
css='''*{box-sizing:border-box}body{margin:0;background:#f2f0e8;color:#17263a;font:16px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}main{max-width:1100px;margin:auto;padding:30px 22px 55px}.eyebrow{color:#5b6b80;font-size:11px;letter-spacing:.13em}h1{font-size:clamp(31px,5vw,46px);line-height:1.1;margin:18px 0}h2{font-size:25px;margin-top:35px}p{color:#5b6b80}.grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;margin:26px 0}.card{background:#fff;border:1px solid #d8d5cc;padding:13px 8px;border-radius:14px;text-align:center}.open{padding:0;border:0;background:none;cursor:zoom-in;max-width:100%}.open img{display:block;width:110px;max-width:100%;height:auto}.card strong{display:block;font-size:13px;margin-top:8px}.card small{font-size:10px;color:#7a8aa0}.tests{display:grid;grid-template-columns:1fr 1fr;gap:16px}.test{padding:20px;border-radius:14px;background:#182b41;color:#f2f5fa}.test.light{background:#fff;color:#17263a;border:1px solid #d8d5cc}.test p{color:inherit;margin:15px 0;font-size:17px}.inline{display:inline-block;width:22px;height:22px;vertical-align:-5px;margin:0 2px}.bigline .inline{width:28px;height:28px;vertical-align:-7px}.strip{display:flex;gap:7px;flex-wrap:wrap;margin:15px 0}.strip img{width:22px;height:22px}.note{padding:12px 16px;border-left:3px solid #b93636;background:#fff;font-size:14px;color:#3a4a60}li{margin:8px 0;color:#5b6b80}.foot{border-top:1px solid #d8d5cc;margin-top:32px;padding-top:18px;font-size:12px;color:#7a8aa0}dialog{max-width:94vw;max-height:94vh;padding:15px;background:#142137;color:white;border:1px solid #516781;border-radius:16px}dialog::backdrop{background:#000d}dialog img{display:block;width:300px;max-width:80vw;height:auto;margin:18px auto}.bar{display:flex;justify-content:space-between;align-items:center;gap:14px}#close{padding:10px 12px;color:white;background:#1b2c45;border:1px solid #516781;border-radius:8px;cursor:pointer}@media(max-width:650px){main{padding:25px 16px}.grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:9px}.card{padding:10px 5px}.card strong{font-size:12px}.open img{width:90px}.tests{grid-template-columns:1fr}}'''
s='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MOKO — эмодзи главной группы, v02</title><style>'+css+'</style></head><body><main><div class="eyebrow">MOKO / ГЛАВНАЯ ГРУППА · CUSTOM EMOJI · V02</div><h1>Разделы<br>главной группы.</h1><p>Вторая версия: знаки стали крупнее и контрастнее — заливка вместо тонких линий, чтобы каждый раздел читался в строке сообщения.</p><p class="note">Тёмный круг и светлая графика — стиль главной группы, отличный от набора канала. Нажмите на значок, чтобы рассмотреть.</p><div class="grid">'
for r in rows:s+=f'<article class="card"><button class="open" aria-label="Увеличить: {r["title"]}"><img src="{data(r["svg"])}" alt="{r["title"]}"></button><strong>{r["title"]}</strong><small>{r["slug"][:2]}</small></article>'
s+='</div><h2>Проверка в сообщениях</h2><p>Реальные PNG 100 × 100 в размере 22 и 28 пикселей на двух фонах.</p><div class="tests">'
def inline(i):return f'<img class="inline" src="{data(rows[i]["file"])}" alt="{rows[i]["title"]}">'
for theme in ['','light']:
 s+=f'<div class="test {theme}"><b>{"Тёмная тема" if theme else "Светлая тема"}</b><p>Новости {inline(1)} Форум {inline(2)}</p><p>Софт {inline(3)} Драйвера {inline(9)}</p><p>Код {inline(11)} Видео {inline(12)}</p><p class="bigline">О проекте {inline(0)} Эфир {inline(14)} В архив {inline(13)}</p><div class="strip">'+''.join(f'<img src="{data(r["file"])}" alt="{r["title"]}">' for r in rows)+'</div></div>'
s+='</div><h2>Что подготовлено</h2><ul><li>18 PNG 100 × 100 с прозрачностью вокруг круга — для загрузки.</li><li>18 WebP без потерь — альтернатива, не дополнительные эмодзи.</li><li>18 SVG — исходники для правок.</li><li>CSV привязки и README с порядком загрузки через @Stickers.</li></ul><p class="note">Набор не опубликован: загрузка через @Stickers. Использование кастомных эмодзи зависит от Telegram Premium и контекста.</p><footer class="foot">Версия 02 для главной группы MOKO: увеличенные узнаваемые знаки. «О проекте» — исходный фирменный знак MOKO.</footer></main><dialog id="zoom"><div class="bar"><span id="caption"></span><button id="close">Закрыть ✕</button></div><img id="large" alt=""></dialog><script>const d=document.getElementById("zoom"),im=document.getElementById("large");document.querySelectorAll(".open").forEach(b=>b.onclick=()=>{const a=b.querySelector("img");im.src=a.src;im.alt=a.alt;document.getElementById("caption").textContent=a.alt;d.showModal()});document.getElementById("close").onclick=()=>d.close();d.onclick=e=>{if(e.target===d)d.close()};</script></body></html>'
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

Версия 02 · 18 статичных эмодзи · на согласование

Вторая версия после замечаний: знаки значительно крупнее и контрастнее — основные формы залиты светлым, детали цветные. В размере 22 px каждый раздел узнаётся.

Стиль набора отличается от набора канала: тёмный круг со светлой графикой вместо светлой основы с диагональю.

## Разделы
О проекте (фирменный знак MOKO), Новости, Форум, Софт, Документация, Лайфхаки, Проекты, Литература, Галерея, Драйвера, Предложения, Код, Видео, Архив + Эфир, Вопрос, Испытания, MOKO SE.

## Форматы
- `png_100/` — комплект для загрузки, PNG 100 × 100 RGBA.
- `webp_100/` — альтернативные копии без потерь; используйте либо PNG, либо WebP.
- `svg/` — векторные исходники.
- `Привязка_эмодзи_группы.csv` — рекомендуемые обычные эмодзи для привязки в @Stickers.

## Загрузка
Через @Stickers: `/newemojipack`, статичный набор, файлы из `png_100/` отправляйте как документы без сжатия, привязка по CSV. Пак не опубликован; использование кастомных эмодзи зависит от Telegram Premium и контекста отправки.
''')
old_zip=B/'MOKO_18_эмодзи_группа_v01.zip'
if old_zip.exists():old_zip.unlink()
manifest=[{k:v for k,v in r.items() if k!='body'} for r in rows]
(SRC/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
qa={'count':18,'style':'dark_circle_v02','size':[100,100],'published':False,'files':[]}
for r in rows:
 p=B/r['file'];im=Image.open(p).convert('RGBA')
 assert im.size==(100,100) and im.getchannel('A').getextrema()==(0,255) and im.getpixel((0,0))[3]==0
 assert Image.open(B/r['webp']).size==(100,100)
 assert '<text' not in (B/r['svg']).read_text()
 qa['files'].append({'file':r['file'],'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(SRC/'QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
with zipfile.ZipFile(B/'MOKO_18_эмодзи_группа_v02.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for folder in ('png_100','webp_100','svg'):
  for p in sorted((B/folder).glob('*')):z.write(p,p.relative_to(B))
 for name in ('MOKO_Группа_Превью.jpg','MOKO_Группа_Просмотр.html','Привязка_эмодзи_группы.csv','README.md'):z.write(B/name,name)
with zipfile.ZipFile(B/'MOKO_18_эмодзи_группа_v02.zip') as z:assert z.testzip() is None and len(z.namelist())==58
print(json.dumps({'count':18,'max_png_bytes':max(x['bytes'] for x in qa['files']),'zip':(B/'MOKO_18_эмодзи_группа_v02.zip').stat().st_size},ensure_ascii=False))
