from pathlib import Path
import io,json,base64,csv,zipfile,hashlib
from PIL import Image,ImageDraw,ImageFont
import cairosvg
R=Path(__file__).resolve().parents[2];B=R/'emoji'
for d in ['png_100','webp_100','svg','source']:(B/d).mkdir(parents=True,exist_ok=True)
u={};exec((R/'branding/source/build.py').read_text().split('files=[]')[0],u)
text,mark=u['text'],u['mark'];INK='#17263A';PAPER='#F2F0E8'
rows=[]
def add(slug,title,fallback,section,col,body):rows.append(dict(slug=slug,title=title,emoji=fallback,section=section,color=col,body=body))
def strokes(d,w=4.8,c=INK):return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
add('01_youtube','YouTube','▶️','Общение','#D64545','<rect x="25" y="30" width="65" height="46" rx="12" fill="#D64545"/><path d="M51 40L73 53L51 66Z" fill="#FFFFFF"/>')
add('02_telegram','Telegram','✈️','Общение','#2587B3','<path d="M26 45L88 23L71 80L54 64L43 74L45 56Z" fill="#2587B3"/>'+strokes('M45 56L76 34L54 64',2.8,PAPER))
thumb='<rect x="24" y="49" width="12" height="33" rx="3" fill="#2587B3"/><path d="M38 50L48 37L50 23Q51 17 57 21Q65 26 60 43H79Q87 43 85 51L80 76Q79 82 70 82H48L38 77Z" fill="'+INK+'"/>'+strokes('M64 54H78',2.8,PAPER)
add('03_like','Лайк','👍','Реакции','#2587B3',thumb)
add('04_dislike','Дизлайк','👎','Реакции','#B93636','<g transform="translate(0 101) scale(1 -1)">'+thumb.replace('#2587B3','#B93636')+'</g>')
add('05_heart','Сердце','❤️','Реакции','#D64545','<path d="M57 82L32 57C18 43 24 27 39 27Q50 26 57 36Q65 25 76 27C92 29 96 43 82 58Z" fill="#D64545"/>')
add('06_fire','Огонь','🔥','Реакции','#C7772D','<path d="M57 19C67 37 49 37 62 49Q72 43 71 34C91 53 87 82 60 84C33 87 22 65 37 47Q36 61 45 58C40 41 52 37 57 19Z" fill="#C7772D"/><path d="M58 49C65 60 73 67 68 75C62 85 47 79 46 71Q46 63 58 49Z" fill="#F3CF6A"/>')
add('07_smile','Улыбка','🙂','Реакции','#C6A54C','<circle cx="40" cy="43" r="3.8" fill="'+INK+'"/><circle cx="73" cy="43" r="3.8" fill="'+INK+'"/>'+strokes('M37 60Q57 82 78 60',5))
add('08_laugh','Смех','😂','Реакции','#C6A54C',strokes('M32 41Q39 32 46 41M65 41Q72 32 79 41',4.3)+'<path d="M35 54H79Q77 82 57 82Q38 82 35 54Z" fill="'+INK+'"/><path d="M39 56H75L73 63H41Z" fill="'+PAPER+'"/><ellipse cx="57" cy="75" rx="10" ry="4" fill="#D96C63"/><path d="M27 46Q19 57 23 63Q31 68 33 59Z" fill="#2587B3"/><path d="M84 46Q93 57 89 63Q81 68 79 59Z" fill="#2587B3"/>')
add('09_wink','Подмигивание','😉','Реакции','#C6A54C','<circle cx="41" cy="43" r="3.8" fill="'+INK+'"/>'+strokes('M65 42Q72 48 79 42M40 61Q63 81 79 58',4.8))
add('10_thanks','Спасибо','🙏','Реакции','#C6A54C','<path d="M56 28Q48 22 46 35L41 50L30 67L44 80L57 62Z" fill="#E5B885" stroke="'+INK+'" stroke-width="3.2" stroke-linejoin="round"/><path d="M59 28Q67 22 69 35L74 50L86 67L72 80L58 62Z" fill="#E5B885" stroke="'+INK+'" stroke-width="3.2" stroke-linejoin="round"/><path d="M29 66L45 80L39 87L23 74Z" fill="#2587B3"/><path d="M86 66L70 80L76 87L92 74Z" fill="#2587B3"/>'+strokes('M57 31V63',2.6))
add('11_done','Готово','✅','Статусы','#23886B',strokes('M31 53L49 72L83 33',9,'#23886B'))
add('12_error','Ошибка','❌','Статусы','#D64545',strokes('M37 32L80 75M80 32L37 75',8.3,'#D64545'))
add('13_question','Вопрос','❓','Статусы','#8C64B2',text('?',58,80,65,INK,'Inter',750,anchor='middle'))
add('14_attention','Внимание','⚠️','Статусы','#C59D32','<path d="M58 24L87 77H29Z" fill="#E6BC4E" stroke="#E6BC4E" stroke-width="6" stroke-linejoin="round"/>'+strokes('M58 42V56',5.5)+'<circle cx="58" cy="66" r="3" fill="'+INK+'"/>')
add('15_wait','Ожидание','⏳','Статусы','#C59D32',strokes('M37 24H79M37 83H79M41 28Q42 42 58 53Q74 65 75 78H41Q42 64 58 53Q73 41 75 28',4.4)+'<path d="M46 32H70L58 44Z" fill="#C59D32"/><path d="M46 75L58 63L70 75Z" fill="#C59D32"/>')
add('16_idea','Идея','💡','Статусы','#C59D32','<path d="M46 65C45 57 36 57 36 43C36 17 79 17 79 43C79 57 70 58 69 65Z" fill="#E8CA78" stroke="'+INK+'" stroke-width="3.5" stroke-linejoin="round"/>'+strokes('M47 71H68M50 78H65M58 10V16M29 20L34 25M82 20L78 25',4))
add('17_code','Код','💻','Инженерия','#2587B3',strokes('M45 35L29 52L45 68M70 35L86 52L70 68M63 28L53 76',5.7))
add('18_python','Python','🐍','Инженерия','#91B943',text('Py',58,70,45,INK,'Inter',750,anchor='middle')+'<rect x="37" y="78" width="42" height="4" rx="2" fill="#91B943"/>')
add('19_labview','LabVIEW','🧩','Инженерия','#C7772D',strokes('M43 36H58V57H75M58 57V74H47',3.6)+'<rect x="27" y="25" width="22" height="23" rx="4" fill="#C7772D"/><rect x="70" y="46" width="21" height="23" rx="4" fill="#C7772D"/><rect x="30" y="67" width="23" height="18" rx="4" fill="#C7772D"/>')
add('20_measurement','Измерения','📈','Инженерия','#2587B3','<rect x="25" y="26" width="65" height="49" rx="7" fill="none" stroke="'+INK+'" stroke-width="4"/>'+strokes('M31 52H42L48 37L56 64L66 43L73 53H84',3.8,'#2587B3')+strokes('M58 76V84M45 84H71',4))
chip='<rect x="36" y="31" width="44" height="45" rx="5" fill="'+INK+'"/><rect x="48" y="43" width="20" height="21" rx="2" fill="'+PAPER+'"/>'
for a in [43,58,73]:chip+=strokes(f'M{a} 23V30M{a} 77V84',4)
for a in [38,53,68]:chip+=strokes(f'M28 {a}H35M81 {a}H88',4)
add('21_hardware','Оборудование','⚙️','Инженерия','#2587B3',chip)
add('22_moko_se','MOKO SE','🤖','Инженерия','#238F83',strokes('M58 28V38',3.5)+'<circle cx="58" cy="24" r="4.5" fill="'+INK+'"/><rect x="29" y="38" width="59" height="39" rx="8" fill="'+INK+'"/><rect x="21" y="48" width="6" height="19" rx="2" fill="'+INK+'"/><rect x="90" y="48" width="6" height="19" rx="2" fill="'+INK+'"/>'+text('SE',58.5,67,26,PAPER,'Inter',750,anchor='middle'))
add('23_launch','Запуск','🚀','Инженерия','#238F83','<path d="M41 64C37 43 51 27 80 20C83 47 67 64 48 69Z" fill="'+INK+'"/><path d="M41 47L29 52L27 68L44 64ZM58 64L54 81L69 78L73 64Z" fill="'+INK+'"/><circle cx="64" cy="39" r="7" fill="'+PAPER+'"/><path d="M38 68L27 83L45 78Z" fill="#C7772D"/>')
add('24_moko','MOKO','🔺','Инженерия','#D64545',mark(26,28,63))
assert len(rows)==24
for r in rows:
 # A transparent outer canvas, simplified circular light base and the diagonal of concept В.
 s='<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><defs><clipPath id="badge"><circle cx="50" cy="50" r="46"/></clipPath></defs>'
 s+='<g clip-path="url(#badge)"><rect width="100" height="100" fill="'+PAPER+'"/><path d="M0 0H33L13 100H0Z" fill="'+r['color']+'"/><path d="M33 0H36L16 100H13Z" fill="#D4D9D7"/>'+mark(67,-8,51,mono=INK,opacity=.035)+'</g><circle cx="50" cy="50" r="46" fill="none" stroke="#D6DBD8" stroke-width="1.4"/>'+r['body']+'</svg>'
 (B/'svg'/f'{r["slug"]}.svg').write_text(s)
 raw=cairosvg.svg2png(bytestring=s.encode(),output_width=400,output_height=400)
 im=Image.open(io.BytesIO(raw)).convert('RGBA').resize((100,100),Image.Resampling.LANCZOS)
 im.save(B/'png_100'/f'{r["slug"]}.png',optimize=True)
 im.save(B/'webp_100'/f'{r["slug"]}.webp',lossless=True,method=6)
 r['file']=f'png_100/{r["slug"]}.png';r['svg']=f'svg/{r["slug"]}.svg';r['webp']=f'webp_100/{r["slug"]}.webp'

def rgba(path,n):
 return Image.open(path).convert('RGBA').resize((n,n),Image.Resampling.LANCZOS)
f=lambda n:ImageFont.truetype(str(R/'brand/Inter.ttf'),n)
board=Image.new('RGB',(1440,1320),'#0B1220');d=ImageDraw.Draw(board)
d.text((70,44),'MOKO / TELEGRAM · CUSTOM EMOJI · V01',font=f(24),fill='#A4B4C9')
d.text((70,99),'Общение + инженерный MOKO',font=f(45),fill='#F7F9FC')
d.text((70,167),'24 статичных эмодзи · 100 × 100 · стиль выбранных аватаров В',font=f(22),fill='#A4B4C9')
for n,r in enumerate(rows):
 x=70+n%6*218;y=244+n//6*210
 # Render vector at presentation size, not a blurry upscale of the 100px upload file.
 a=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=(B/r['svg']).read_bytes(),output_width=130,output_height=130))).convert('RGBA');board.paste(a,(x+33,y),a)
 d.text((x+98,y+142),r['title'],font=f(21),fill='#F7F9FC',anchor='mt')
 d.text((x+98,y+174),r['slug'][:2],font=f(13),fill='#8298B4',anchor='mt')
d.line((70,1092,1370,1092),fill='#2B3B52',width=2)
d.text((70,1120),'Примеры в строке сообщения',font=f(23),fill='#F7F9FC')
x=70;y=1180
for txt,ids in [('Новое видео ',[0,2]),('  Код работает ',[16,10]),('  Запускаем тест ',[19,22])]:
 d.text((x,y),txt,font=f(25),fill='#DFE6EF');x+=d.textlength(txt,font=f(25))
 for i in ids:
  a=rgba(B/rows[i]['file'],28);board.paste(a,(round(x),y+2),a);x+=34
board.save(B/'MOKO_Эмодзи_Превью.jpg',quality=93,optimize=True)

# Lightweight self-contained viewer. Real 22/28px tests use the actual upload PNGs.
def data(path):
 p=B/path;mime='image/svg+xml' if p.suffix=='.svg' else 'image/png';return 'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
css='''*{box-sizing:border-box}body{margin:0;background:#0b1220;color:#f7f9fc;font:16px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}main{max-width:1100px;margin:auto;padding:30px 22px 55px}.eyebrow{color:#a4b4c9;font-size:11px;letter-spacing:.13em}h1{font-size:clamp(31px,5vw,46px);line-height:1.1;margin:18px 0}h2{font-size:25px;margin-top:35px}p{color:#a4b4c9}.grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;margin:26px 0}.card{background:#152238;border:1px solid #30445d;padding:13px 8px;border-radius:14px;text-align:center}.open{padding:0;border:0;background:none;cursor:zoom-in;max-width:100%}.open img{display:block;width:110px;max-width:100%;height:auto}.card strong{display:block;font-size:13px;margin-top:8px}.card small{font-size:10px;color:#93A9C4}.tests{display:grid;grid-template-columns:1fr 1fr;gap:16px}.test{padding:20px;border-radius:14px;background:#182B41;color:#f2f5fa}.test.light{background:#F7F7F4;color:#17263A}.test p{color:inherit;margin:15px 0;font-size:17px}.inline{display:inline-block;width:22px;height:22px;vertical-align:-5px;margin:0 2px}.bigline .inline{width:28px;height:28px;vertical-align:-7px}.strip{display:flex;gap:7px;flex-wrap:wrap;margin:15px 0}.strip img{width:22px;height:22px}.note{padding:12px 16px;border-left:3px solid #B8EB55;background:#142137;font-size:14px}li{margin:8px 0;color:#a4b4c9}.foot{border-top:1px solid #30445d;margin-top:32px;padding-top:18px;font-size:12px;color:#8b9fb9}dialog{max-width:94vw;max-height:94vh;padding:15px;background:#142137;color:white;border:1px solid #516781;border-radius:16px}dialog::backdrop{background:#000d}dialog img{display:block;width:300px;max-width:80vw;height:auto;margin:18px auto}.bar{display:flex;justify-content:space-between;align-items:center;gap:14px}#close{padding:10px 12px;color:white;background:#1b2c45;border:1px solid #516781;border-radius:8px;cursor:pointer}@media(max-width:650px){main{padding:25px 16px}.grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:9px}.card{padding:10px 5px}.card strong{font-size:12px}.open img{width:90px}.tests{grid-template-columns:1fr}}'''
s='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MOKO — эмодзи для общения и инженерии</title><style>'+css+'</style></head><body><main><div class="eyebrow">MOKO / TELEGRAM · CUSTOM EMOJI · V01</div><h1>Общение +<br>инженерный MOKO.</h1><p>24 статичных кастомных эмодзи в стиле выбранного варианта В. Светлая основа, цветная диагональ, тёмная графика. Мелкие подписи и сложная фактура убраны ради читаемости в строке сообщения.</p><p class="note">Это файлы для собственного набора эмодзи, не стикеры и не уже опубликованный Telegram-пак. Нажмите на значок, чтобы рассмотреть его.</p><div class="grid">'
for r in rows:s+=f'<article class="card"><button class="open" aria-label="Увеличить: {r["title"]}"><img src="{data(r["svg"])}" alt="{r["title"]}"></button><strong>{r["title"]}</strong><small>{r["slug"][:2]} · {r["section"]}</small></article>'
s+='</div><h2>Проверка в сообщениях</h2><p>Условные примеры на светлом и тёмном фоне. Здесь используются реальные PNG 100 × 100, показанные в размере 22 и 28 пикселей.</p><div class="tests">'
def inline(i):return f'<img class="inline" src="{data(rows[i]["file"])}" alt="{rows[i]["title"]}">'
for theme in ['', 'light']:
 s+=f'<div class="test {theme}"><b>{"Светлая тема" if theme else "Тёмная тема"}</b><p>Новое видео {inline(0)} {inline(2)}</p><p>Код работает {inline(16)} {inline(10)}</p><p>Есть идея {inline(15)} Обсудим? {inline(12)}</p><p>Проверим измерения {inline(19)} {inline(14)}</p><p class="bigline">Спасибо! {inline(9)} {inline(4)}</p><div class="strip">'+''.join(f'<img src="{data(r["file"])}" alt="{r["title"]}">' for r in rows)+'</div></div>'
s+='</div><h2>Что подготовлено</h2><ul><li>24 PNG 100 × 100 с прозрачностью вокруг значка — для загрузки.</li><li>24 WebP 100 × 100 без потерь — альтернативный формат.</li><li>24 SVG с графикой в векторе — для редактирования и масштабирования, не для прямой загрузки как статичных эмодзи.</li><li>Таблица привязки к обычным эмодзи и инструкция для @Stickers.</li></ul><p class="note">Набор пока не создан в Telegram. Его нужно загрузить через @Stickers. Использование кастомных эмодзи может зависеть от Telegram Premium и контекста отправки.</p><footer class="foot">Первая версия на согласование. YouTube и Telegram представлены стилизованными значками площадок, без заявления об официальном партнёрстве. Аватары и предыдущие материалы не изменены.</footer></main><dialog id="zoom"><div class="bar"><span id="caption"></span><button id="close">Закрыть ✕</button></div><img id="large" alt=""></dialog><script>const d=document.getElementById("zoom"),im=document.getElementById("large");document.querySelectorAll(".open").forEach(b=>b.onclick=()=>{const a=b.querySelector("img");im.src=a.src;im.alt=a.alt;document.getElementById("caption").textContent=a.alt;d.showModal()});document.getElementById("close").onclick=()=>d.close();d.onclick=e=>{if(e.target===d)d.close()};</script></body></html>'
# Store each upload PNG only once; the same real pixels are used in every inline test.
import re
assets={}
def dedup(match):
 value=match.group(1)
 if value not in assets:assets[value]='p'+str(len(assets))
 return 'data-png="'+assets[value]+'"'
s=re.sub(r'src="(data:image/png;base64,[^"]+)"',dedup,s)
lookup={key:value for value,key in assets.items()}
loader='<script>const PNGS='+json.dumps(lookup)+';document.querySelectorAll("img[data-png]").forEach(i=>i.src=PNGS[i.dataset.png]);</script>'
s=s.replace('</body>',loader+'</body>')
(B/'MOKO_Эмодзи_Просмотр.html').write_text(s)
with (B/'Привязка_эмодзи.csv').open('w',encoding='utf-8-sig',newline='') as fp:
 w=csv.writer(fp,delimiter=';');w.writerow(['№','Файл PNG','Название','Обычный эмодзи для привязки','Раздел'])
 for i,r in enumerate(rows,1):w.writerow([i,r['file'],r['title'],r['emoji'],r['section']])
readme='''# MOKO — кастомные эмодзи для Telegram

Версия 01 · 24 статичных эмодзи · На согласование

## Форматы
- `png_100/` — основной комплект для загрузки: PNG 100 × 100, RGBA. Уголки и пространство вокруг значка прозрачные; светлая подложка внутри значка — часть выбранного дизайна.
- `webp_100/` — те же изображения 100 × 100 в WebP без потерь. Используйте либо PNG, либо WebP: не загружайте обе копии как разные эмодзи.
- `svg/` — векторные исходники. Текст Py, SE и знак вопроса переведены в контуры. SVG не является файлом для прямой загрузки статичных эмодзи в этом наборе.
- `Привязка_эмодзи.csv` — названия файлов и предлагаемые обычные эмодзи для привязки.
- HTML — автономная галерея с увеличением и проверкой 22/28 px на двух фонах. JPG — общий обзор.

## Как создать набор
1. Откройте в Telegram **@Stickers**.
2. Отправьте `/newemojipack`, затем выберите статичный набор (Static), если бот предлагает выбор.
3. Укажите название, например **MOKO · Общение и инженерия**.
4. Отправляйте файлы из `png_100/` **как файлы/документы, без сжатия в фотографии**. Размер 100 × 100 и порядок загрузки соответствуют практической инструкции. [5](https://blog.invitemember.com/custom-emojis-in-telegram-step-by-step-guide/)
5. Для каждого файла укажите обычный эмодзи по таблице CSV или выберите свой.
6. После добавления всего набора следуйте подсказкам бота для публикации. Название и короткий адрес набора выбираете вы; свободность адреса не проверялась.

Пак пока не опубликован: действующей ссылки `t.me/addemoji/...` ещё нет. Приём файлов самим ботом в аккаунте не проверялся. Размеры, формат и прозрачность проверены локально.

Доступность использования кастомных эмодзи зависит от Telegram Premium и контекста отправки; создание файлов само по себе не снимает эти ограничения. [5](https://blog.invitemember.com/custom-emojis-in-telegram-step-by-step-guide/)

## Состав и стиль
YouTube, Telegram, лайк, дизлайк, сердце, огонь, улыбка, смех, подмигивание, спасибо, готово, ошибка, вопрос, внимание, ожидание, идея, код, Python, LabVIEW, измерения, оборудование, MOKO SE, запуск, MOKO.

Сохранены светлая основа, диагональная полоса и палитра аватаров варианта В. Мелкая надпись MOKO намеренно не добавлена на каждый значок: в строке она мешала бы читаемости. Отдельный эмодзи MOKO содержит исходный фирменный знак. Python и LabVIEW различаются зелёным и оранжевым акцентами; их пиктограммы — собственные обозначения тем, не официальные логотипы продуктов. Статичные изображения не имеют анимации. Гарнитура/канальные аватары в этот набор не переносились целиком.
'''
(B/'README.md').write_text(readme)
manifest=[{k:v for k,v in r.items() if k!='body'} for r in rows];(B/'source/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
qa={'count':24,'format':'static_custom_emoji','size':[100,100],'published':False,'telegram_bot_acceptance_tested':False,'files':[]}
for r in rows:
 p=B/r['file'];im=Image.open(p);assert im.size==(100,100) and im.mode=='RGBA';a=im.getchannel('A');assert a.getextrema()==(0,255);assert a.getpixel((0,0))==0;assert p.stat().st_size<64000
 assert Image.open(B/r['webp']).size==(100,100)
 assert '<text' not in (B/r['svg']).read_text()
 qa['files'].append({'file':r['file'],'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(B/'source/QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
with zipfile.ZipFile(B/'MOKO_24_эмодзи_v01.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for folder in ['png_100','webp_100','svg']:
  for p in sorted((B/folder).glob('*')):z.write(p,p.relative_to(B))
 for filename in ['MOKO_Эмодзи_Превью.jpg','MOKO_Эмодзи_Просмотр.html','Привязка_эмодзи.csv','README.md']:z.write(B/filename,filename)
with zipfile.ZipFile(B/'MOKO_24_эмодзи_v01.zip') as z:assert z.testzip() is None
print('24 emoji ready; maximum PNG bytes:',max(x['bytes'] for x in qa['files']),'ZIP bytes:',(B/'MOKO_24_эмодзи_v01.zip').stat().st_size)
