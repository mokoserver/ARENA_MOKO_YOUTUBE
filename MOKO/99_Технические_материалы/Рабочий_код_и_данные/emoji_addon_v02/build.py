"""Build only three additional emoji; the approved original 24 are not modified.
Run from any directory. Uses the organized MOKO folder, no restored old paths.
"""
from pathlib import Path
import base64, copy, csv, hashlib, io, json, zipfile
import xml.etree.ElementTree as ET
import cairosvg
from PIL import Image, ImageDraw, ImageFont
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'00_НАЧНИТЕ_ЗДЕСЬ.md').exists())
B = ROOT/'02_Telegram/04_Эмодзи_Дополнение_3'
SOURCE = Path(__file__).resolve().parent
for d in ('png_100', 'webp_100', 'svg'): (B/d).mkdir(parents=True, exist_ok=True)
INK='#17263A'; PAPER='#F2F0E8'
ET.register_namespace('', 'http://www.w3.org/2000/svg')
template = ET.fromstring((ROOT/'02_Telegram/02_Эмодзи_24/svg/01_youtube.svg').read_text())
github = ET.fromstring((SOURCE/'github_simpleicons.svg').read_text())
github_path = next(e.attrib['d'] for e in github if e.tag.endswith('path'))
rows=[
 dict(slug='25_link', title='Ссылка', emoji='🔗', section='Навигация', color='#2587B3', body='<g transform="translate(25 20) scale(2.7)" fill="none" stroke="'+INK+'" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></g>'),
 dict(slug='26_github', title='GitHub', emoji='💻', section='Площадки', color='#63738A', body=f'<path d="{github_path}" transform="translate(28 23) scale(2.5)" fill="{INK}"/>'),
 dict(slug='27_info', title='Информация', emoji='ℹ️', section='Навигация', color='#2587B3', body=f'<circle cx="58" cy="53" r="29" fill="{INK}"/><circle cx="58" cy="39" r="3.8" fill="{PAPER}"/><path d="M54 50H59V69M53 70H65" fill="none" stroke="{PAPER}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
]
for r in rows:
 root=copy.deepcopy(template)
 for e in list(root)[3:]:root.remove(e)
 root[1][1].set('fill',r['color'])
 body=ET.fromstring('<svg xmlns="http://www.w3.org/2000/svg">'+r['body']+'</svg>')
 for e in body:root.append(e)
 svg=ET.tostring(root,encoding='unicode')
 (B/'svg'/f'{r["slug"]}.svg').write_text(svg)
 raw=cairosvg.svg2png(bytestring=svg.encode(),output_width=400,output_height=400)
 im=Image.open(io.BytesIO(raw)).convert('RGBA').resize((100,100),Image.Resampling.LANCZOS)
 im.save(B/'png_100'/f'{r["slug"]}.png',optimize=True)
 im.save(B/'webp_100'/f'{r["slug"]}.webp',lossless=True,method=6)
 r['file']=f'png_100/{r["slug"]}.png';r['svg']=f'svg/{r["slug"]}.svg';r['webp']=f'webp_100/{r["slug"]}.webp'

def render(r,n):
 return Image.open(io.BytesIO(cairosvg.svg2png(url=str(B/r['svg']),output_width=n,output_height=n))).convert('RGBA')
def font(n):return ImageFont.truetype(str(ROOT/'05_Бренд_MOKO/03_Шрифты/Inter.ttf'),n)
board=Image.new('RGB',(1200,760),'#0B1220');d=ImageDraw.Draw(board)
d.text((60,36),'MOKO / TELEGRAM · EMOJI · ДОПОЛНЕНИЕ 02',font=font(18),fill='#A4B4C9')
d.text((60,82),'Ссылка. GitHub. Информация.',font=font(40),fill='#F7F9FC')
d.text((60,142),'3 новых эмодзи в стиле В · теперь всего 27',font=font(22),fill='#A4B4C9')
for i,r in enumerate(rows):
 x=60+i*370
 d.rounded_rectangle((x,205,x+340,485),radius=20,fill='#152238',outline='#30445D',width=1)
 a=render(r,170);board.paste(a,(x+85,229),a)
 d.text((x+170,416),r['title'],font=font(25),fill='#F7F9FC',anchor='mt')
 d.text((x+170,453),r['slug'],font=font(14),fill='#A4B4C9',anchor='mt')
for theme,y,bg,fg in [('Тёмная тема',530,'#182B41','#F2F5FA'),('Светлая тема',620,'#F7F7F4','#17263A')]:
 d.rounded_rectangle((60,y,1140,y+68),radius=13,fill=bg)
 d.text((80,y+22),theme,font=font(18),fill=fg)
 for i,r in enumerate(rows):
  x=290+i*275;a=Image.open(B/r['file']).convert('RGBA').resize((28,28),Image.Resampling.LANCZOS)
  board.paste(a,(x,y+19),a);d.text((x+38,y+20),['Ссылка','Репозиторий','Информация'][i],font=font(20),fill=fg)
d.text((60,720),'PNG / WebP 100 × 100 · SVG · Исходные 24 эмодзи не изменены',font=font(16),fill='#A4B4C9')
board.save(B/'MOKO_3_эмодзи_Превью.jpg',quality=92,optimize=True)

def data(rel):
 p=B/rel;mime='image/svg+xml' if p.suffix=='.svg' else 'image/png'
 return 'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
css='''*{box-sizing:border-box}body{margin:0;background:#0b1220;color:#f7f9fc;font:16px/1.55 system-ui,sans-serif}main{max-width:960px;margin:auto;padding:38px 22px}.eyebrow{font-size:11px;letter-spacing:.12em;color:#a4b4c9}h1{font-size:clamp(29px,5vw,46px);line-height:1.15}p{color:#a4b4c9}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:30px 0}.card{border:1px solid #30445d;background:#152238;border-radius:16px;text-align:center;padding:22px 10px}.card img{width:160px;max-width:100%;display:block;margin:auto}.card strong{display:block;margin-top:12px;font-size:17px}.card small{color:#a4b4c9;font-size:12px}button{border:0;background:none;color:inherit;cursor:zoom-in;padding:0;max-width:100%}.test{padding:18px 22px;background:#182b41;border-radius:14px;margin:12px 0}.test.light{background:#f7f7f4;color:#17263a}.test p{color:inherit}.inline{width:28px;height:28px;vertical-align:-7px;margin-right:8px}.small .inline{width:22px;height:22px;vertical-align:-5px}.note{border-left:3px solid #b8eb55;padding:12px 16px;background:#142137}li{color:#a4b4c9;margin:9px 0}dialog{border:1px solid #516781;border-radius:16px;background:#142137;color:white;max-width:94vw}dialog::backdrop{background:#000d}dialog img{display:block;width:300px;max-width:78vw;margin:20px auto}.bar{display:flex;justify-content:space-between;gap:20px}#close{cursor:pointer;padding:6px}footer{margin-top:30px;border-top:1px solid #30445d;padding-top:16px;color:#a4b4c9;font-size:12px}@media(max-width:600px){main{padding:25px 16px}.grid{gap:8px}.card{padding:14px 5px}.card strong{font-size:12px}.card small{font-size:10px}}'''
s='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MOKO — Ссылка, GitHub, Информация</title><style>'+css+'</style></head><body><main><div class="eyebrow">MOKO / TELEGRAM · ДОПОЛНЕНИЕ 02</div><h1>Ссылка. GitHub.<br>Информация.</h1><p>Три недостающих эмодзи в том же стиле В: светлая основа, цветная диагональ и тёмная графика. Вместе с прежними 24 — теперь 27.</p><p class="note">Исходные 24 не изменены. Этот отдельный комплект содержит только три новых значка. Нажмите на любой, чтобы рассмотреть.</p><div class="grid">'
for r in rows:s+=f'<article class="card"><button class="open" aria-label="Увеличить: {r["title"]}"><img src="{data(r["svg"])}" alt="{r["title"]}"></button><strong>{r["title"]}</strong><small>{r["slug"]}</small></article>'
s+='</div><h2>В строке сообщения</h2><p>Настоящие PNG 100 × 100 в размере 28 и 22 пикселя.</p>'
for theme in ('','light'):
 s+=f'<section class="test {theme}"><b>{"Светлая тема" if theme else "Тёмная тема"}</b>'
 for r,t in zip(rows,['Ссылка на материалы','Репозиторий MOKO','Информация о проекте']):s+=f'<p><img class="inline" src="{data(r["file"])}" alt="{r["title"]}">{t}</p>'
 s+='<p class="small">22 px: '+''.join(f'<img class="inline" src="{data(r["file"])}" alt="{r["title"]}">' for r in rows)+'</p></section>'
s+='''<h2>Как использовать</h2><ul><li>PNG 100 × 100 — для загрузки; WebP — альтернативные копии, не дополнительные эмодзи.</li><li>SVG — для редактирования и масштабирования, не для загрузки как статичных эмодзи.</li><li>Если пак уже создан, добавьте только эти три файла через @Stickers. Если ещё нет — используйте прежние 24 и эти три.</li><li>Это значки, а не активные ссылки: адрес GitHub или другую ссылку добавляйте отдельно в текст сообщения.</li></ul><p class="note">Файлы подготовлены, но не загружены в Telegram. Доступность использования зависит от правил Telegram, Premium и контекста отправки.</p><footer>GitHub представлен узнаваемым знаком площадки; официальное партнёрство не подразумевается. Новые значки подготовлены для вашей проверки.</footer></main><dialog id="zoom"><div class="bar"><span id="caption"></span><button id="close">Закрыть ✕</button></div><img id="large" alt=""></dialog><script>const d=document.getElementById('zoom');document.querySelectorAll('.open').forEach(b=>b.onclick=()=>{const i=b.querySelector('img'),l=document.getElementById('large');l.src=i.src;l.alt=i.alt;document.getElementById('caption').textContent=i.alt;d.showModal()});document.getElementById('close').onclick=()=>d.close();d.onclick=e=>{if(e.target===d)d.close()};</script></body></html>'''
(B/'MOKO_3_эмодзи_Просмотр.html').write_text(s)
with (B/'Привязка_эмодзи.csv').open('w',encoding='utf-8-sig',newline='') as fp:
 w=csv.writer(fp,delimiter=';');w.writerow(['№','Файл PNG','Название','Обычный эмодзи для привязки','Раздел'])
 for r in rows:w.writerow([r['slug'][:2],r['file'],r['title'],r['emoji'],r['section']])
(B/'README.md').write_text('''# MOKO — 3 дополнительных Telegram-эмодзи

Дополнение 02: **Ссылка, GitHub, Информация**. Вместе с предыдущими 24 — 27 эмодзи. Прежние файлы не изменены; новые значки подготовлены для проверки.

| № | Файл | Привязка |
|---|---|---|
| 25 | `png_100/25_link.png` | 🔗 |
| 26 | `png_100/26_github.png` | 💻 |
| 27 | `png_100/27_info.png` | ℹ️ |

- `png_100/` — 3 PNG 100 × 100 с прозрачностью вокруг значка, для загрузки.
- `webp_100/` — те же 3 изображения в WebP без потерь: используйте либо PNG, либо WebP.
- `svg/` — векторные исходники, не формат загрузки статичных эмодзи этого набора.
- HTML — автономная галерея с увеличением и тестами 22/28 px. JPG — общий обзор.

## Загрузка

Если пак уже создан, добавьте эти три файла через **@Stickers** в существующий набор, следуя подсказкам бота. Если пака ещё нет, используйте прежний комплект 24 и это дополнение при создании статичного набора. Отправляйте PNG как файлы/документы, без сжатия. Привязки из CSV рекомендательные; у GitHub нет отдельного стандартного Unicode-эмодзи, поэтому предложен 💻.

Это графические значки, не активные ссылки. URL репозитория или сайта вставляется отдельно в текст сообщения. Набор нами не опубликован, загрузка через бот в аккаунте не проверена. Применение кастомных эмодзи зависит от ограничений Telegram и контекста, включая Premium.

## Стиль и источник

Сохранён стиль В: светлая круглая основа, цветная диагональ, тёмная графика. Знак GitHub использован из Simple Icons: https://github.com/simple-icons/simple-icons/blob/develop/icons/github.svg . Бренд GitHub принадлежит его владельцам; официальное партнёрство не подразумевается.
''')
manifest=[{k:v for k,v in r.items() if k!='body'} for r in rows]
(SOURCE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
qa={'new_count':3,'total_with_originals':27,'published':False,'telegram_bot_acceptance_tested':False,'files':[]}
for r in rows:
 p=B/r['file'];im=Image.open(p).convert('RGBA');wp=Image.open(B/r['webp']).convert('RGBA')
 assert im.size==wp.size==(100,100)
 assert im.getchannel('A').getextrema()==(0,255) and im.getpixel((0,0))[3]==0
 assert p.stat().st_size<64000
 assert all(a==b or (a[3]==b[3]==0) for a,b in zip(im.getdata(),wp.getdata()))
 assert '<text' not in (B/r['svg']).read_text()
 qa['files'].append({'file':r['file'],'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(SOURCE/'QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
with zipfile.ZipFile(B/'MOKO_3_эмодзи_дополнение_v02.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for folder in ('png_100','webp_100','svg'):
  for p in sorted((B/folder).glob('*')):z.write(p,p.relative_to(B))
 for name in ('MOKO_3_эмодзи_Превью.jpg','MOKO_3_эмодзи_Просмотр.html','Привязка_эмодзи.csv','README.md'):z.write(B/name,name)
with zipfile.ZipFile(B/'MOKO_3_эмодзи_дополнение_v02.zip') as z:assert len(z.namelist())==13 and z.testzip() is None
print(json.dumps(qa,ensure_ascii=False,indent=2))
