from pathlib import Path
import io,json,base64,hashlib,zipfile
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];T=R/'telegram_avatars';B=T/'final_graphic'
for f in ['png','svg']:(B/f).mkdir(parents=True,exist_ok=True)
u={'__file__':str(T/'source/build_bold_concepts.py')};exec((T/'source/build_bold_concepts.py').read_text().split('styles=[')[0],u)
records=u['records'];mark,text,tw=u['mark'],u['text'],u['tw']
qa={'final_direction':'В — Графический знак (исходный)','not_variants':['В1','В2'],'news_symbol':'Мегафон','group_symbol':'Крупный знак MOKO','published':False,'files':[]}
for r,m in zip(records,u['masks']):
 im=u['graphic'](r,m)
 # Verify that the lossless final PNG comes from exactly the approved concept render.
 trial=io.BytesIO();im.save(trial,'JPEG',quality=95,subsampling=0,optimize=True)
 assert trial.getvalue()==(T/'bold_concepts/jpg'/f'c_{r["slug"]}.jpg').read_bytes()
 p=B/'png'/f'{r["slug"]}.png';im.save(p,optimize=True)
 # Fully vector counterpart: the same original role paths, with a luminance mask for cutouts.
 source=(T/r['source_svg']).read_text();start=source.index('r="460"');start=source.index('/>',start)+2;end=source.index('<path d="M0 750')
 g=source[start:end].replace(r['color'],'#000000').replace('#F7F9FC','#FFFFFF').replace('#F0D48C','#FFFFFF')
 col=r['color'] if r['slug']!='06_johnny_respect' else '#CCA955';ink='#17263A' if r['slug']!='06_johnny_respect' else '#695126'
 s='<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024"><defs><mask id="role" x="0" y="0" width="1024" height="1024" maskUnits="userSpaceOnUse" style="mask-type:luminance"><rect width="1024" height="1024" fill="black"/>'+g+'</mask></defs>'
 s+='<rect width="1024" height="1024" fill="#F2F0E8"/>'+f'<path d="M0 0H371L154 1024H0Z" fill="{col}"/><path d="M371 0H405L188 1024H154Z" fill="#D4D9D7"/>'
 s+=mark(584,-79,615,mono='#17263a',opacity=.045)+mark(-165,680,490,mono='#ffffff',opacity=.14)
 scale=922/1024
 s+=f'<g transform="translate(119 25) scale({scale})" opacity=".4"><rect width="1024" height="1024" fill="#B1B8B8" mask="url(#role)"/></g><g transform="translate(111 13) scale({scale})"><rect width="1024" height="1024" fill="{ink}" mask="url(#role)"/></g>'
 s+=f'<path d="M324 771H854" stroke="#17263A" stroke-width="5"/><rect x="324" y="771" width="147" height="10" fill="{col}"/>'
 total=116+24+tw('MOKO',93,'Jost',500);x=(1024-total)/2
 s+=mark(x,892-116*193/271,116)+text('MOKO',x+140,892,93,'#17263A','Jost',500)+'</svg>'
 (B/'svg'/f'{r["slug"]}.svg').write_text(s)
 qa['files'].append({'file':str(p.relative_to(B)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':p.stat().st_size,'approved_render_match':True})

def circle(p,n):
 im=Image.open(p).convert('RGBA').resize((n,n),Image.Resampling.LANCZOS);mask=Image.new('L',(n*3,n*3));ImageDraw.Draw(mask).ellipse((0,0,n*3-1,n*3-1),fill=255);im.putalpha(mask.resize((n,n),Image.Resampling.LANCZOS));return im
f=lambda n:ImageFont.truetype(str(R/'brand/Inter.ttf'),n)
board=Image.new('RGB',(1440,1450),'#0B1220');d=ImageDraw.Draw(board)
d.text((70,48),'MOKO / TELEGRAM · ФИНАЛЬНЫЙ ВАРИАНТ В',font=f(25),fill='#A4B4C9');d.text((70,103),'Графический знак. Итоговый комплект.',font=f(42),fill='#F7F9FC');d.text((70,170),'Светлая основа · цветная диагональ · выбранные символы',font=f(24),fill='#A4B4C9')
for n,r in enumerate(records):
 x=72+n%3*442;y=250+n//3*470;a=circle(B/'png'/f'{r["slug"]}.png',322);board.paste(a,(x+38,y),a)
 d.text((x+199,y+345),r['title'],font=f(28),fill='#F7F9FC',anchor='mt');d.text((x+199,y+389),r['description'],font=f(17),fill='#A4B4C9',anchor='mt')
d.line((70,1210,1370,1210),fill='#2B3B52',width=2);d.text((70,1243),'Проверка в малом размере',font=f(24),fill='#F7F9FC')
for n,r in enumerate(records):
 a=circle(B/'png'/f'{r["slug"]}.png',64);board.paste(a,(70+n*133,1310),a)
d.text((912,1308),'6 PNG 1024 × 1024 + SVG\nТолько выбранный вариант В.',font=f(21),fill='#A4B4C9',spacing=10)
board.save(B/'MOKO_Telegram_Финал_В.jpg',quality=93,optimize=True)

def uri(path):
 im=Image.open(path).convert('RGB');im.thumbnail((640,640));o=io.BytesIO();im.save(o,'WEBP',quality=90,method=6);return 'data:image/webp;base64,'+base64.b64encode(o.getvalue()).decode()
css='''*{box-sizing:border-box}body{margin:0;background:#0b1220;color:#f7f9fc;font:16px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}main{max-width:1080px;margin:auto;padding:32px 20px 55px}.eyebrow{color:#a4b4c9;font-size:11px;letter-spacing:.15em}h1{font-size:clamp(32px,5vw,48px);line-height:1.08;margin:18px 0}p{color:#a4b4c9}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin:28px 0}.card{background:#152238;border:1px solid #30445d;border-radius:16px;padding:20px 12px;text-align:center}.open{border:0;background:none;padding:0;border-radius:50%;max-width:100%;cursor:zoom-in}.open img{width:242px;max-width:100%;border-radius:50%;display:block}h2{font-size:18px;margin:14px 0 5px}.card p{font-size:13px;min-height:40px}.card code{font-size:11px;color:#9eacc1;overflow-wrap:anywhere}.note{padding:12px 16px;border-left:3px solid #b8eb55;background:#142137;font-size:14px}.mini{display:flex;gap:18px;flex-wrap:wrap;margin:22px 0}.mini img{width:48px;height:48px;border-radius:50%}.foot{margin-top:32px;padding-top:20px;border-top:1px solid #30445d;font-size:12px;color:#8b9fb9}dialog{max-width:95vw;max-height:95vh;background:#0b1220;color:white;padding:12px;border:1px solid #516781;border-radius:16px}dialog::backdrop{background:#000d}dialog img{display:block;width:auto;height:auto;max-width:87vw;max-height:76vh;margin:12px auto;border-radius:50%}.bar{display:flex;align-items:center;justify-content:space-between;gap:12px}#close{padding:10px 14px;background:#1b2c45;color:white;border:1px solid #516781;border-radius:8px;cursor:pointer}@media(max-width:650px){main{padding:27px 16px}.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.card{padding:14px 8px}.open img{width:160px}h2{font-size:15px}.card p{font-size:12px;min-height:53px}.card code{font-size:9px}}'''
s='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MOKO Telegram — финальный вариант В</title><style>'+css+'</style></head><body><main><div class="eyebrow">MOKO / TELEGRAM · ФИНАЛЬНЫЙ ВАРИАНТ В</div><h1>Графический знак.<br>Выбранный финал.</h1><p>Именно исходный вариант В: светлая основа, цветная диагональ слева и тёмный крупный символ. Не В1 и не В2. Для новостей — мегафон, для группы — крупный знак MOKO.</p><p class="note">Нажмите на аватар, чтобы увеличить. В ZIP только шесть финальных аватаров: PNG 1024 × 1024 для установки и SVG-исходники.</p><div class="grid">'
for n,r in enumerate(records):s+=f'<article class="card"><button class="open"><img id="i{n}" src="{uri(B/"png"/(r["slug"]+".png"))}" alt="{r["title"]}"></button><h2>{r["title"]}</h2><p>{r["description"]}</p><code>{r["slug"]}.png</code></article>'
s+='</div><h2>В малом размере</h2><div class="mini">'+''.join(f'<img data-ref="i{n}" alt="{r["title"]}">' for n,r in enumerate(records))+'</div><h2>Как установить</h2><p>Выберите нужный PNG в папке png. Устанавливайте квадрат целиком, без дополнительного приближения: круг формируется при отображении в Telegram. Названия в презентации помогают выбрать файл; переименовывать паблики необязательно.</p><p>SVG содержит векторные формы, маски и текст в контурах. Для загрузки в Telegram используйте PNG. Векторная и растровая версии могут немного различаться сглаживанием краёв.</p><footer class="foot">Остальные концепты — в архиве, в этот комплект не входят. Файлы подготовлены; в Telegram ничего не установлено.</footer></main><dialog id="zoom"><div class="bar"><span id="caption"></span><button id="close">Закрыть ✕</button></div><img id="large" alt=""></dialog><script>document.querySelectorAll("img[data-ref]").forEach(i=>i.src=document.getElementById(i.dataset.ref).src);const d=document.getElementById("zoom"),im=document.getElementById("large");document.querySelectorAll(".open").forEach(b=>b.onclick=()=>{const a=b.querySelector("img");im.src=a.src;im.alt=a.alt;document.getElementById("caption").textContent=a.alt;d.showModal()});document.getElementById("close").onclick=()=>d.close();d.onclick=e=>{if(e.target===d)d.close()};</script></body></html>'
(B/'MOKO_Telegram_Финал_В.html').write_text(s)
readme='MOKO / TELEGRAM — ФИНАЛЬНЫЙ ВАРИАНТ В\n\nВыбран исходный В «Графический знак»: светлый фон, диагональное цветовое поле слева и тёмные символы. Это НЕ В1 и НЕ В2.\n\n'
for r in records:readme+=f'png/{r["slug"]}.png — {r["title"]}; {r["description"]}.\n'
readme+='\nPNG: 1024 × 1024, основной формат для установки. Они получены без потерь из того же рендера, который дал выбранные JPG-превью варианта В; соответствие исходному рендеру проверено.\nSVG: векторная версия с масками яркости и текстом в контурах; установка шрифтов не требуется. При импорте в редакторы проверяйте поддержку масок. Сглаживание краёв может немного отличаться от PNG.\nHTML: автономная презентация. JPG: общий обзор, не файл для установки.\n\nДля Telegram устанавливайте квадратный PNG целиком, без дополнительного приближения. Круг формируется при отображении. Символ гарнитуры обозначает связь с командой, а не наличие звонков.\n\nВ комплекте нет альтернатив. Остальные концепты перенесены в архивные сравнения. На площадках ничего не опубликовано.\n'
(B/'README.txt').write_text(readme)
(B/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2));(B/'QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
print('Six canonical PNG and vector SVG files ready')
