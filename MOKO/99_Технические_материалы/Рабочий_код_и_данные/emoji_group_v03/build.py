"""Group emoji v03 candidate: strict corporate flat marks, no circles at all.
Solid colored glyphs on transparent background, dark same-hue details.
Built alongside v02 (current) for comparison; does not touch main files.
"""
from pathlib import Path
import base64, csv, hashlib, io, json, re, zipfile
import cairosvg
from PIL import Image, ImageDraw, ImageFont
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'00_НАЧНИТЕ_ЗДЕСЬ.md').exists())
B = ROOT/'02_Telegram/04_Эмодзи_Главная_группа'
SRC = Path(__file__).resolve().parent
for d in ('png_v03','webp_v03','svg_v03'): (B/d).mkdir(parents=True, exist_ok=True)
MARK='<path d="M160 4.27406L271 154.274L176 192.274L160 4.27406Z" fill="#b93636"/><path d="M94.8938 0L127.894 44L101.894 82L94.8938 0Z" fill="#b93636"/><path d="M160 4.27406L176 192.274L53 163.274L160 4.27406Z" fill="#d64545"/><path d="M93.5 2.27405L58 147.274L0 132.274L93.5 2.27405Z" fill="#d64545"/><path d="M95 0.274048L102 81.774L58 147.274L0 132.274L95 0.274048Z" fill="#d64545"/>'
rows=[]
def add(slug,title,emoji,c,d,body):rows.append(dict(slug=slug,title=title,emoji=emoji,c=c,d=d,body=body))
add('01_about','О проекте','🔺','#d64545','#b93636',f'<g transform="translate(12.1 23) scale(0.28)">{MARK}</g>')
add('02_news','Новости','📰','#D64545','#8F2F2F','<path fill-rule="evenodd" d="M25 28H69Q72 28 72 31V69Q72 72 69 72H25Q22 72 22 69V31Q22 28 25 28ZM28 36H46V47H28ZM28 53H64V57H28ZM28 61H64V65H28ZM28 69H50V73H28Z" fill="{c}"/><rect x="74" y="38" width="7" height="34" rx="2" fill="{d}"/>')
add('03_forum','Форум','💬','#55C9FF','#2A8DC0','<path fill-rule="evenodd" d="M23 26H61Q65 26 65 30V48Q65 52 61 52H42L31 62V52H23Q19 52 19 48V30Q19 26 23 26ZM30 39a3.6 3.6 0 1 0 7.2 0a3.6 3.6 0 1 0 -7.2 0ZM40 39a3.6 3.6 0 1 0 7.2 0a3.6 3.6 0 1 0 -7.2 0ZM50 39a3.6 3.6 0 1 0 7.2 0a3.6 3.6 0 1 0 -7.2 0Z" fill="{c}"/><path d="M69 40H77Q81 40 81 44V58Q81 62 77 62H75V70L66 62H56Z" fill="{d}"/>')
add('04_soft','Софт','🖥️','#B8EB55','#7FA832','<path fill-rule="evenodd" d="M25 26H71Q74 26 74 29V69Q74 72 71 72H25Q22 72 22 69V29Q22 26 25 26ZM22 36H74V39H22ZM27 29a2.6 2.6 0 1 0 5.2 0a2.6 2.6 0 1 0 -5.2 0ZM35 29a2.6 2.6 0 1 0 5.2 0a2.6 2.6 0 1 0 -5.2 0Z" fill="{c}"/><path d="M60 44V40M60 72V76M46 58H42M78 58H74M50 48L47 45M70 68L73 71M70 48L73 45M50 68L47 71" stroke="{d}" stroke-width="5" stroke-linecap="round"/><circle cx="60" cy="58" r="10" fill="{d}"/><circle cx="60" cy="58" r="3.4" fill="{c}"/>')
add('05_docs','Документация','📄','#6B7177','#464B50','<path fill-rule="evenodd" d="M30 22H56L70 36V78H30ZM37 46H61V50H37ZM37 55H61V59H37ZM37 64H51V68H37Z" fill="{c}"/><path d="M56 22L70 36H56Z" fill="{d}"/>')
add('06_lifehack','Лайфхаки','✨','#FF9A48','#C06A26','<circle cx="48" cy="42" r="17" fill="{c}"/><rect x="41" y="58" width="14" height="7" rx="2" fill="{c}"/><rect x="42" y="67" width="12" height="6" rx="2" fill="{d}"/><rect x="45" y="14" width="6" height="11" rx="2" fill="{c}"/><rect x="17" y="39" width="11" height="6" rx="2" fill="{c}"/><rect x="68" y="39" width="11" height="6" rx="2" fill="{c}"/><path d="M27 20L35 28L31 32L23 24Z" fill="{c}"/><path d="M69 20L61 28L65 32L73 24Z" fill="{c}"/><path d="M42 42Q45 36 48 42Q51 48 54 42" stroke="{d}" stroke-width="3.4" fill="none" stroke-linecap="round"/>')
add('07_projects','Проекты','📐','#B69AFF','#7E63C4','<path d="M50 18L80 33L50 48L20 33Z" fill="{c}"/><path d="M20 37L48 51V82L20 68Z" fill="{d}"/><path d="M80 37L52 51V82L80 68Z" fill="{c}"/>')
add('08_books','Литература','📚','#55D6C2','#2B9C8A','<path fill-rule="evenodd" d="M48 28C41 22 29 22 22 26V72C29 68 41 68 48 74ZM29 36C33 34 40 34 43 36V40C40 38 33 38 29 40ZM29 46C33 44 40 44 43 46V50C40 48 33 48 29 50Z" fill="{c}"/><path fill-rule="evenodd" d="M52 28C59 22 71 22 78 26V72C71 68 59 68 52 74ZM57 36C61 34 68 34 71 36V40C68 38 61 38 57 40ZM57 46C61 44 68 44 71 46V50C68 48 61 48 57 50Z" fill="{d}"/>')
add('09_gallery','Галерея','🖼️','#ED6262','#B03A3A','<path fill-rule="evenodd" d="M25 26H75Q78 26 78 29V71Q78 74 75 74H25Q22 74 22 71V29Q22 26 25 26ZM28 32H72V68H28Z" fill="{c}"/><path d="M30 66L43 48L51 58L59 46L70 66Z" fill="{c}"/><circle cx="62" cy="40" r="5" fill="{d}"/>')
add('10_drivers','Драйвера','🔌','#8CC63F','#5F8C26','<rect x="37" y="16" width="7" height="16" rx="2" fill="{c}"/><rect x="56" y="16" width="7" height="16" rx="2" fill="{c}"/><path d="M30 32H70V46Q70 61 50 66Q30 61 30 46Z" fill="{c}"/><rect x="46" y="66" width="8" height="16" rx="2" fill="{d}"/>')
add('11_suggest','Предложения','📮','#2E9BD6','#1B6C97','<g transform="rotate(-6 50 30)"><path fill-rule="evenodd" d="M43 18H57V40H43ZM46.5 27L49 30.5L54 23.5L56 25L49.5 34L44.5 28.5Z" fill="{d}"/></g><path fill-rule="evenodd" d="M24 42H76Q78 42 78 44V50Q78 52 76 52H24Q22 52 22 50V44Q22 42 24 42ZM42 45H58V49H42Z" fill="{c}"/><rect x="27" y="54" width="46" height="22" rx="3" fill="{c}"/>')
add('12_code','Код','💻','#3ECF6E','#23934C','<path d="M36 28L16 50L36 72H45L25 50L45 28Z" fill="{c}"/><path d="M64 28L84 50L64 72H55L75 50L55 28Z" fill="{c}"/><path d="M56 22H64L48 78H40Z" fill="{d}"/>')
add('13_video','Видео','🎬','#B93636','#7E2424','<path fill-rule="evenodd" d="M24 46L30 26H80L74 46ZM38 28L34 44H39L43 28ZM52 28L48 44H53L57 28ZM66 28L62 44H67L71 28Z" fill="{c}"/><path fill-rule="evenodd" d="M24 48H76Q78 48 78 50V74Q78 76 76 76H24Q22 76 22 74V50Q22 48 24 48ZM46 54L62 62L46 70Z" fill="{d}"/>')
add('14_archive','Архив','🗃️','#9CA3AF','#6B7177','<rect x="21" y="26" width="58" height="15" rx="3" fill="{c}"/><path fill-rule="evenodd" d="M27 45H73V74Q73 77 70 77H30Q27 77 27 74ZM42 53H58V59H42Z" fill="{c}"/>')
add('15_live','Эфир','📡','#FF7A59','#C24E31','<rect x="47" y="48" width="7" height="32" rx="2" fill="{c}"/><circle cx="50.5" cy="42" r="7.5" fill="{c}"/><path d="M33 30L39 24L43 28L37 34Z" fill="{c}"/><path d="M25 22L31 16L35 20L29 26Z" fill="{c}"/><path d="M68 30L62 24L58 28L64 34Z" fill="{c}"/><path d="M76 22L70 16L66 20L72 26Z" fill="{c}"/><path d="M28 52L34 46L38 50L32 56Z" fill="{d}"/><path d="M73 52L67 46L63 50L69 56Z" fill="{d}"/>')
add('16_question','Вопрос','❓','#6EA8FE','#2F5FC4','<path d="M25 24H75Q79 24 79 28V54Q79 58 75 58H48L36 70V58H25Q21 58 21 54V28Q21 24 25 24Z" fill="{c}"/><path d="M43 37Q43 30 50 30Q58 30 58 37Q58 43 50 45.5V50" stroke="{d}" stroke-width="6" fill="none" stroke-linecap="round"/><circle cx="50" cy="56" r="3.8" fill="{d}"/>')
add('17_tests','Испытания','🧪','#FFC53D','#C08A1D','<path d="M25 68A25 25 0 0 1 75 68H65A15 15 0 0 0 35 68Z" fill="{c}"/><path d="M47 70L61 50L66 54L52 74Z" fill="{d}"/><circle cx="50" cy="68" r="5.5" fill="{d}"/>')
add('18_moko_se','MOKO SE','📏','#0FA3A3','#067070','<path fill-rule="evenodd" d="M22 36H80Q82 36 82 38V46Q82 48 80 48H22Q20 48 20 46V38Q20 36 22 36ZM28 38V43H30V38ZM36 38V43H38V38ZM44 38V43H46V38ZM52 38V43H54V38ZM68 38V43H70V38ZM76 38V43H78V38Z" fill="{c}"/><rect x="24" y="48" width="9" height="22" rx="2" fill="{c}"/><rect x="56" y="28" width="13" height="20" rx="3" fill="{d}"/><rect x="59.5" y="48" width="6" height="15" rx="2" fill="{d}"/>')
for r in rows:
 s='<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">'+r['body'].replace('{c}',r['c']).replace('{d}',r['d'])+'</svg>'
 (B/'svg_v03'/f'{r["slug"]}.svg').write_text(s)
 raw=cairosvg.svg2png(bytestring=s.encode(),output_width=400,output_height=400)
 im=Image.open(io.BytesIO(raw)).convert('RGBA').resize((100,100),Image.Resampling.LANCZOS)
 im.save(B/'png_v03'/f'{r["slug"]}.png',optimize=True)
 im.save(B/'webp_v03'/f'{r["slug"]}.webp',lossless=True,method=6)
 r['file']=f'png_v03/{r["slug"]}.png';r['svg']=f'svg_v03/{r["slug"]}.svg';r['webp']=f'webp_v03/{r["slug"]}.webp'
def jost(n):return ImageFont.truetype(str(ROOT/'05_Бренд_MOKO/03_Шрифты/Jost.ttf'),n)
def inter(n):return ImageFont.truetype(str(ROOT/'05_Бренд_MOKO/03_Шрифты/Inter.ttf'),n)
board=Image.new('RGB',(1440,1240),'#FFFFFF');d=ImageDraw.Draw(board)
d.text((70,46),'РАЗДЕЛ 03 · MOKO / ГЛАВНАЯ ГРУППА · V03',font=inter(20),fill='#6b7177')
d.text((70,92),'Разделы главной группы',font=jost(52),fill='#050505')
d.text((70,168),'Строгий корпоративный стиль: без кругов и обводок, свой цвет раздела',font=inter(22),fill='#6b7177')
for n,r in enumerate(rows):
 x=70+n%6*218;y=250+n//6*210
 a=Image.open(io.BytesIO(cairosvg.svg2png(url=str(B/r['svg']),output_width=130,output_height=130))).convert('RGBA');board.paste(a,(x+33,y),a)
 d.text((x+98,y+142),r['title'],font=inter(21),fill='#050505',anchor='mt')
 d.text((x+98,y+174),r['c'],font=inter(13),fill='#9ca3af',anchor='mt')
d.line((70,952,1370,952),fill='#e5e7eb',width=2)
d.text((70,982),'В строке сообщения: тёмная и светлая тема',font=jost(26),fill='#050505')
strip_l=Image.new('RGB',(1300,86),'#FFFFFF');strip_dk=Image.new('RGB',(1300,86),'#0a0a0a')
x=20
for r in rows:
 a=Image.open(B/r['file']).convert('RGBA').resize((40,40),Image.Resampling.LANCZOS)
 strip_l.paste(a,(x,23),a);strip_dk.paste(a,(x,23),a);x+=71
board.paste(strip_l,(70,1030));board.paste(strip_dk,(70,1126))
board.save(B/'MOKO_Группа_v03_Превью.jpg',quality=93,optimize=True)
def data(rel):
 p=B/rel;mime='image/svg+xml' if p.suffix=='.svg' else 'image/png'
 return 'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
css='''*{box-sizing:border-box}body{margin:0;background:#fff;color:#050505;font:16px/1.5 Inter,system-ui,sans-serif}main{max-width:1100px;margin:auto;padding:30px 22px 55px}.eyebrow{color:#6b7177;font-size:11px;letter-spacing:.13em}h1{font-family:Jost,Inter,sans-serif;font-size:clamp(31px,5vw,46px);line-height:1.1;margin:18px 0}h2{font-family:Jost,Inter,sans-serif;font-size:25px;margin-top:35px}p{color:#6b7177}.grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;margin:26px 0}.card{background:#fafafa;border:1px solid #e5e7eb;padding:13px 8px;border-radius:10px;text-align:center}.open{padding:0;border:0;background:none;cursor:zoom-in;max-width:100%}.open img{display:block;width:110px;max-width:100%;height:auto}.card strong{display:block;font-size:13px;margin-top:8px}.card small{font-size:10px;color:#9ca3af}.tests{display:grid;grid-template-columns:1fr 1fr;gap:16px}.test{padding:20px;border-radius:10px;background:#0a0a0a;color:#f2f5fa}.test.light{background:#fff;color:#050505;border:1px solid #e5e7eb}.test p{color:inherit;margin:15px 0;font-size:17px}.inline{display:inline-block;width:22px;height:22px;vertical-align:-5px;margin:0 2px}.bigline .inline{width:28px;height:28px;vertical-align:-7px}.strip{display:flex;gap:7px;flex-wrap:wrap;margin:15px 0}.strip img{width:22px;height:22px}.note{padding:12px 16px;border-left:3px solid #d64545;background:#fafafa;font-size:14px;color:#374151}li{margin:8px 0;color:#6b7177}.foot{border-top:1px solid #e5e7eb;margin-top:32px;padding-top:18px;font-size:12px;color:#9ca3af}dialog{max-width:94vw;max-height:94vh;padding:15px;background:#0a0a0a;color:white;border:1px solid #374151;border-radius:12px}dialog::backdrop{background:#000d}dialog img{display:block;width:300px;max-width:80vw;height:auto;margin:18px auto}.bar{display:flex;justify-content:space-between;align-items:center;gap:14px}#close{padding:10px 12px;color:white;background:#1f2937;border:1px solid #374151;border-radius:8px;cursor:pointer}@media(max-width:650px){main{padding:25px 16px}.grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:9px}.card{padding:10px 5px}.card strong{font-size:12px}.open img{width:90px}.tests{grid-template-columns:1fr}}'''
s='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MOKO — эмодзи главной группы, v03</title><style>'+css+'</style></head><body><main><div class="eyebrow">РАЗДЕЛ 03 · MOKO / ГЛАВНАЯ ГРУППА · V03</div><h1>Строгий корпоративный.<br>Без кругов.</h1><p>Третья версия по брендбуку: плоские залитые знаки без подложек, обводок и градиентов. У каждого раздела свой цвет, детали — тёмный тон того же цвета.</p><p class="note">Это вариант для сравнения с v02. Нажмите на значок, чтобы рассмотреть.</p><div class="grid">'
for r in rows:s+=f'<article class="card"><button class="open" aria-label="Увеличить: {r["title"]}"><img src="{data(r["svg"])}" alt="{r["title"]}"></button><strong>{r["title"]}</strong><small>{r["c"]}</small></article>'
s+='</div><h2>В строке сообщения</h2><p>Реальные PNG 100 × 100 в 22 и 28 px на фирменном тёмном и светлом фоне.</p><div class="tests">'
def inline(i):return f'<img class="inline" src="{data(rows[i]["file"])}" alt="{rows[i]["title"]}">'
for theme in ['','light']:
 s+=f'<div class="test {theme}"><b>{"Тёмная тема" if theme else "Светлая тема"}</b><p>Новости {inline(1)} Форум {inline(2)} Софт {inline(3)}</p><p>Код {inline(11)} Видео {inline(12)} Архив {inline(13)}</p><p class="bigline">О проекте {inline(0)} Эфир {inline(14)} Вопрос {inline(15)}</p><div class="strip">'+''.join(f'<img src="{data(r["file"])}" alt="{r["title"]}">' for r in rows)+'</div></div>'
s+='</div><h2>Состав</h2><ul><li>18 PNG 100 × 100 RGBA, прозрачный фон.</li><li>18 WebP без потерь и 18 SVG.</li><li>Цвета разделов разные; «О проекте» — фирменный знак #d64545/#b93636.</li></ul><footer class="foot">Вариант v03 · строгая геометрия, без круглых подложек · шрифты Jost/Inter по брендбуку.</footer></main><dialog id="zoom"><div class="bar"><span id="caption"></span><button id="close">Закрыть ✕</button></div><img id="large" alt=""></dialog><script>const d=document.getElementById("zoom"),im=document.getElementById("large");document.querySelectorAll(".open").forEach(b=>b.onclick=()=>{const a=b.querySelector("img");im.src=a.src;im.alt=a.alt;document.getElementById("caption").textContent=a.alt;d.showModal()});document.getElementById("close").onclick=()=>d.close();d.onclick=e=>{if(e.target===d)d.close()};</script></body></html>'
assets={}
def dedup(m):
 v=m.group(1)
 if v not in assets:assets[v]='p'+str(len(assets))
 return 'data-png="'+assets[v]+'"'
s=re.sub(r'src="(data:image/png;base64,[^"]+)"',dedup,s)
lookup={k:v for v,k in assets.items()}
s=s.replace('</body>','<script>const PNGS='+json.dumps(lookup)+';document.querySelectorAll("img[data-png]").forEach(i=>i.src=PNGS[i.dataset.png]);</script></body>')
(B/'MOKO_Группа_v03_Просмотр.html').write_text(s)
manifest=[{k:v for k,v in r.items() if k!='body'} for r in rows]
(SRC/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
qa={'count':18,'style':'flat_corporate_v03','files':[]}
for r in rows:
 p=B/r['file'];im=Image.open(p).convert('RGBA')
 assert im.size==(100,100) and im.getchannel('A').getextrema()==(0,255) and im.getpixel((0,0))[3]==0
 assert '<text' not in (B/r['svg']).read_text()
 qa['files'].append({'file':r['file'],'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(SRC/'QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
with zipfile.ZipFile(B/'MOKO_18_эмодзи_группа_v03.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for folder in ('png_v03','webp_v03','svg_v03'):
  for p in sorted((B/folder).glob('*')):z.write(p,p.relative_to(B))
 for name in ('MOKO_Группа_v03_Превью.jpg','MOKO_Группа_v03_Просмотр.html'):z.write(B/name,name)
with zipfile.ZipFile(B/'MOKO_18_эмодзи_группа_v03.zip') as z:assert z.testzip() is None
print(json.dumps({'count':18,'max_png_bytes':max(x['bytes'] for x in qa['files']),'zip':(B/'MOKO_18_эмодзи_группа_v03.zip').stat().st_size},ensure_ascii=False))
