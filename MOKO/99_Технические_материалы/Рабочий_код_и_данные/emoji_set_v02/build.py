"""Unified 27-emoji set + MOKO Telegraph avatar. Original 24 pixels stay byte-identical.
Run from any directory; works on the organized MOKO folder.
"""
from pathlib import Path
import base64, hashlib, io, json, re, shutil, zipfile
import cairosvg
from PIL import Image, ImageDraw, ImageFont
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'00_НАЧНИТЕ_ЗДЕСЬ.md').exists())
TECH = ROOT/'02_Telegram'; OLD = TECH/'02_Эмодзи_24'; NEW = TECH/'02_Эмодзи_27'
ADDON = TECH/'04_Эмодзи_Дополнение_3'; TG = TECH/'05_Аватар_MOKO_Telegraph'
SRC = Path(__file__).resolve().parent
INK='#17263A'; PAPER='#F2F0E8'

# ---------- unified emoji set ----------
if not NEW.exists(): OLD.rename(NEW)
for folder in ('png_100','webp_100','svg'):
 for p in sorted((ADDON/folder).glob('*')): shutil.copy2(p, NEW/folder/p.name)
m24=json.loads((ROOT/'99_Технические_материалы/Рабочий_код_и_данные/moko/emoji/source/manifest.json').read_text())
m3=json.loads((ROOT/'99_Технические_материалы/Рабочий_код_и_данные/emoji_addon_v02/manifest.json').read_text())
rows=m24+m3
def data(rel):
 p=NEW/rel;mime='image/svg+xml' if p.suffix=='.svg' else 'image/png'
 return 'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
css='''*{box-sizing:border-box}body{margin:0;background:#0b1220;color:#f7f9fc;font:16px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}main{max-width:1100px;margin:auto;padding:30px 22px 55px}.eyebrow{color:#a4b4c9;font-size:11px;letter-spacing:.13em}h1{font-size:clamp(31px,5vw,46px);line-height:1.1;margin:18px 0}h2{font-size:25px;margin-top:35px}p{color:#a4b4c9}.grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;margin:26px 0}.card{background:#152238;border:1px solid #30445d;padding:13px 8px;border-radius:14px;text-align:center}.open{padding:0;border:0;background:none;cursor:zoom-in;max-width:100%}.open img{display:block;width:110px;max-width:100%;height:auto}.card strong{display:block;font-size:13px;margin-top:8px}.card small{font-size:10px;color:#93A9C4}.tests{display:grid;grid-template-columns:1fr 1fr;gap:16px}.test{padding:20px;border-radius:14px;background:#182B41;color:#f2f5fa}.test.light{background:#F7F7F4;color:#17263A}.test p{color:inherit;margin:15px 0;font-size:17px}.inline{display:inline-block;width:22px;height:22px;vertical-align:-5px;margin:0 2px}.bigline .inline{width:28px;height:28px;vertical-align:-7px}.strip{display:flex;gap:7px;flex-wrap:wrap;margin:15px 0}.strip img{width:22px;height:22px}.note{padding:12px 16px;border-left:3px solid #B8EB55;background:#142137;font-size:14px}li{margin:8px 0;color:#a4b4c9}.foot{border-top:1px solid #30445d;margin-top:32px;padding-top:18px;font-size:12px;color:#8b9fb9}dialog{max-width:94vw;max-height:94vh;padding:15px;background:#142137;color:white;border:1px solid #516781;border-radius:16px}dialog::backdrop{background:#000d}dialog img{display:block;width:300px;max-width:80vw;height:auto;margin:18px auto}.bar{display:flex;justify-content:space-between;align-items:center;gap:14px}#close{padding:10px 12px;color:white;background:#1b2c45;border:1px solid #516781;border-radius:8px;cursor:pointer}@media(max-width:650px){main{padding:25px 16px}.grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:9px}.card{padding:10px 5px}.card strong{font-size:12px}.open img{width:90px}.tests{grid-template-columns:1fr}}'''
s='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MOKO — 27 эмодзи для общения и инженерии</title><style>'+css+'</style></head><body><main><div class="eyebrow">MOKO / TELEGRAM · CUSTOM EMOJI · V02</div><h1>Общение +<br>инженерный MOKO.</h1><p>27 статичных кастомных эмодзи в стиле выбранного варианта В: прежние 24 и добавленные «Ссылка», «GitHub», «Информация». Светлая основа, цветная диагональ, тёмная графика.</p><p class="note">Это файлы для собственного набора эмодзи, не стикеры и не опубликованный Telegram-пак. Нажмите на значок, чтобы рассмотреть его.</p><div class="grid">'
for r in rows:s+=f'<article class="card"><button class="open" aria-label="Увеличить: {r["title"]}"><img src="{data(r["svg"])}" alt="{r["title"]}"></button><strong>{r["title"]}</strong><small>{r["slug"][:2]} · {r["section"]}</small></article>'
s+='</div><h2>Проверка в сообщениях</h2><p>Условные примеры на светлом и тёмном фоне. Используются реальные PNG 100 × 100 в размере 22 и 28 пикселей.</p><div class="tests">'
def inline(i):return f'<img class="inline" src="{data(rows[i]["file"])}" alt="{rows[i]["title"]}">'
for theme in ['','light']:
 s+=f'<div class="test {theme}"><b>{"Светлая тема" if theme else "Тёмная тема"}</b><p>Новое видео {inline(0)} {inline(2)}</p><p>Код работает {inline(16)} {inline(10)}</p><p>Ссылка на репозиторий {inline(24)} {inline(25)}</p><p>Информация о проекте {inline(26)}</p><p class="bigline">Спасибо! {inline(9)} {inline(4)}</p><div class="strip">'+''.join(f'<img src="{data(r["file"])}" alt="{r["title"]}">' for r in rows)+'</div></div>'
s+='</div><h2>Что подготовлено</h2><ul><li>27 PNG 100 × 100 с прозрачностью вокруг значка — для загрузки.</li><li>27 WebP 100 × 100 без потерь — альтернативный формат; не загружайте оба как разные эмодзи.</li><li>27 SVG — векторные исходники для редактирования, не формат загрузки.</li><li>Таблица привязки к обычным эмодзи и инструкция для @Stickers.</li></ul><p class="note">Набор пока не создан в Telegram: файлы загружаются через @Stickers. Использование кастомных эмодзи может зависеть от Telegram Premium и контекста отправки.</p><footer class="foot">Версия 02: единый набор 27. Исходные 24 эмодзи побайтово неизменны; добавлены Ссылка, GitHub и Информация. Аватары и предыдущие материалы не изменены.</footer></main><dialog id="zoom"><div class="bar"><span id="caption"></span><button id="close">Закрыть ✕</button></div><img id="large" alt=""></dialog><script>const d=document.getElementById("zoom"),im=document.getElementById("large");document.querySelectorAll(".open").forEach(b=>b.onclick=()=>{const a=b.querySelector("img");im.src=a.src;im.alt=a.alt;document.getElementById("caption").textContent=a.alt;d.showModal()});document.getElementById("close").onclick=()=>d.close();d.onclick=e=>{if(e.target===d)d.close()};</script></body></html>'
assets={};lookup={}
def dedup(m):
 v=m.group(1)
 if v not in assets:assets[v]='p'+str(len(assets))
 return 'data-png="'+assets[v]+'"'
s=re.sub(r'src="(data:image/png;base64,[^"]+)"',dedup,s)
lookup={k:v for v,k in assets.items()}
s=s.replace('</body>','<script>const PNGS='+json.dumps(lookup)+';document.querySelectorAll("img[data-png]").forEach(i=>i.src=PNGS[i.dataset.png]);</script></body>')
(NEW/'MOKO_Эмодзи_Просмотр.html').write_text(s)
import csv
with (NEW/'Привязка_эмодзи.csv').open('w',encoding='utf-8-sig',newline='') as fp:
 w=csv.writer(fp,delimiter=';');w.writerow(['№','Файл PNG','Название','Обычный эмодзи для привязки','Раздел'])
 for i,r in enumerate(rows,1):w.writerow([i,r['file'],r['title'],r['emoji'],r['section']])
def font(n):return ImageFont.truetype(str(ROOT/'05_Бренд_MOKO/03_Шрифты/Inter.ttf'),n)
board=Image.new('RGB',(1440,1560),'#0B1220');d=ImageDraw.Draw(board)
d.text((70,44),'MOKO / TELEGRAM · CUSTOM EMOJI · V02',font=font(24),fill='#A4B4C9')
d.text((70,99),'Общение + инженерный MOKO',font=font(45),fill='#F7F9FC')
d.text((70,167),'27 статичных эмодзи · 100 × 100 · стиль выбранных аватаров В',font=font(22),fill='#A4B4C9')
for n,r in enumerate(rows):
 x=70+n%6*218;y=244+n//6*210
 a=Image.open(io.BytesIO(cairosvg.svg2png(url=str(NEW/r['svg']),output_width=130,output_height=130))).convert('RGBA');board.paste(a,(x+33,y),a)
 d.text((x+98,y+142),r['title'],font=font(21),fill='#F7F9FC',anchor='mt')
 d.text((x+98,y+174),r['slug'][:2],font=font(13),fill='#8298B4',anchor='mt')
d.line((70,1332,1370,1332),fill='#2B3B52',width=2)
d.text((70,1360),'Примеры в строке сообщения',font=font(23),fill='#F7F9FC')
x=70;y=1420
for txt,ids in [('Новое видео ',[0,2]),('  Репозиторий ',[25,24]),('  Информация ',[26,10])]:
 d.text((x,y),txt,font=font(25),fill='#DFE6EF');x+=d.textlength(txt,font=font(25))
 for i in ids:
  a=Image.open(NEW/rows[i]['file']).convert('RGBA').resize((28,28),Image.Resampling.LANCZOS);board.paste(a,(round(x),y+2),a);x+=34
board.save(NEW/'MOKO_Эмодзи_Превью.jpg',quality=93,optimize=True)
(NEW/'README.md').write_text('''# MOKO — кастомные эмодзи для Telegram

Версия 02 · единый набор 27 статичных эмодзи · на согласование

## Состав
Прежние 24 (общение, реакции, статусы, инженерия) + добавленные по запросу: **25 Ссылка, 26 GitHub, 27 Информация**. Исходные 24 файла побайтово неизменны.

## Форматы
- `png_100/` — основной комплект для загрузки: PNG 100 × 100, RGBA, прозрачные уголки.
- `webp_100/` — те же изображения в WebP без потерь. Используйте либо PNG, либо WebP, не оба как разные эмодзи.
- `svg/` — векторные исходники; не формат прямой загрузки статичных эмодзи.
- `Привязка_эмодзи.csv` — названия и предлагаемые обычные эмодзи для привязки (у GitHub нет отдельного Unicode-эмодзи, предложен 💻).
- HTML — автономная галерея с увеличением и проверкой 22/28 px; JPG — общий обзор.
- `MOKO_24_эмодзи_v01.zip` — прежний комплект 24, сохранён как история.
- `MOKO_27_эмодзи_v02.zip` — текущий единый комплект.

## Как создать набор
1. Откройте в Telegram **@Stickers** и отправьте `/newemojipack` (статичный набор, если бот спрашивает).
2. Название, например **MOKO · Общение и инженерия**.
3. Отправляйте файлы из `png_100/` как файлы/документы, без сжатия, в порядке таблицы CSV.
4. Привяжите обычный эмодзи по CSV и опубликуйте набор подсказками бота.

Пак нами не опубликован: ссылки `t.me/addemoji/...` нет. Загрузка ботом в аккаунте не проверялась. Использование кастомных эмодзи зависит от Telegram Premium и контекста отправки.

Это графические значки, не активные ссылки: URL вставляется отдельным текстом сообщения. Знак GitHub — из Simple Icons, официальное партнёрство не подразумевается.
''')
qa={'count':27,'format':'static_custom_emoji','size':[100,100],'published':False,'files':[]}
for r in rows:
 p=NEW/r['file'];im=Image.open(p).convert('RGBA')
 assert im.size==(100,100) and im.getchannel('A').getextrema()==(0,255) and im.getpixel((0,0))[3]==0
 assert Image.open(NEW/r['webp']).size==(100,100)
 assert '<text' not in (NEW/r['svg']).read_text()
 qa['files'].append({'file':r['file'],'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(SRC/'QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
with zipfile.ZipFile(NEW/'MOKO_27_эмодзи_v02.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for folder in ('png_100','webp_100','svg'):
  for p in sorted((NEW/folder).glob('*')):z.write(p,p.relative_to(NEW))
 for name in ('MOKO_Эмодзи_Превью.jpg','MOKO_Эмодзи_Просмотр.html','Привязка_эмодзи.csv','README.md'):z.write(NEW/name,name)
with zipfile.ZipFile(NEW/'MOKO_27_эмодзи_v02.zip') as z:assert z.testzip() is None and len(z.namelist())==85
shutil.rmtree(ADDON)
print('Unified set ready: 27 emoji; v02 zip files:',85)

# ---------- MOKO Telegraph avatar ----------
TG.mkdir(parents=True,exist_ok=True)
news=(TECH/'01_Аватары_ФИНАЛ_В/svg/01_news.svg').read_text()
mark_paths=re.search(r'opacity="0.045"><path d="([^"]+)"',news).group(1)
ACCENT='#C13E7A'
glyph=('<rect x="320" y="690" width="470" height="62" rx="30" fill="'+INK+'"/>'
 '<rect x="690" y="596" width="80" height="100" rx="22" fill="'+INK+'"/>'
 '<path d="M728 630L430 556" stroke="'+INK+'" stroke-width="50" stroke-linecap="round" fill="none"/>'
 '<circle cx="412" cy="548" r="56" fill="'+INK+'"/>'
 '<rect x="452" y="606" width="46" height="88" fill="'+INK+'"/>'
 '<rect x="330" y="352" width="150" height="40" rx="20" fill="'+ACCENT+'"/>'
 '<circle cx="545" cy="372" r="22" fill="'+ACCENT+'"/>'
 '<rect x="610" y="352" width="150" height="40" rx="20" fill="'+ACCENT+'"/>')
svg=('<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">'
 '<rect width="1024" height="1024" fill="'+PAPER+'"/>'
 '<path d="M0 0H371L154 1024H0Z" fill="'+ACCENT+'"/>'
 '<path d="M371 0H405L188 1024H154Z" fill="#D4D9D7"/>'
 '<g transform="translate(584 -79) scale(2.2693726937269374)" opacity="0.045"><path d="'+mark_paths+'" fill="#17263a"/></g>'
 +glyph+'</svg>')
(TG/'MOKO_Telegraph.svg').write_text(svg)
big=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(),output_width=1024,output_height=1024))).convert('RGBA')
big.save(TG/'MOKO_Telegraph_1024.png')
mask=Image.new('L',(1024,1024),0);ImageDraw.Draw(mask).ellipse((0,0,1023,1023),fill=255)
circ=Image.new('RGBA',(1024,1024),(0,0,0,0));circ.paste(big,(0,0),mask)
board=Image.new('RGB',(1280,720),'#0B1220');d=ImageDraw.Draw(board)
d.text((60,42),'MOKO TELEGRAPH · АВАТАР ПАБЛИКА',font=font(20),fill='#A4B4C9')
d.text((60,84),'Телеграфный ключ и азбука Морзе',font=font(38),fill='#F7F9FC')
d.text((60,140),'Стиль финальных аватаров В · диагональ '+ACCENT,font=font(20),fill='#A4B4C9')
board.paste(big.resize((430,430),Image.Resampling.LANCZOS),(60,210),big.resize((430,430),Image.Resampling.LANCZOS))
c=circ.resize((430,430),Image.Resampling.LANCZOS);board.paste(c,(560,210),c)
for n,x in [(128,1050),(64,1190)]:
 c2=circ.resize((n,n),Image.Resampling.LANCZOS);board.paste(c2,(x,210+(430-n)//2),c2)
d.text((60,672),'Квадрат 1024 и круглая обрезка, как её показывает Telegram',font=font(18),fill='#A4B4C9')
board.save(TG/'MOKO_Telegraph_Превью.jpg',quality=92,optimize=True)
(TG/'README.md').write_text('''# MOKO Telegraph — аватар паблика

Новая иконка для телеграм-паблика **MOKO Telegraph** в стиле финальных аватаров В: светлая основа, диагональная полоса (новый цвет #C13E7A), бледный знак MOKO справа вверху.

Символ — телеграфный ключ и строка азбуки Морзе (тире‑точка‑тире): отсылка к названию Telegraph и инженерному характеру MOKO.

- `MOKO_Telegraph_1024.png` — файл для установки, 1024 × 1024.
- `MOKO_Telegraph.svg` — векторный исходник.
- `MOKO_Telegraph_Превью.jpg` — квадрат, круглая обрезка и малые размеры для проверки.

Композиция рассчитана на круглую обрезку Telegram: ключевые элементы внутри безопасного круга. На площадке аватар не устанавливался.
''')
assert big.size==(1024,1024)
print('Telegraph avatar ready:',sorted(p.name for p in TG.iterdir()))
