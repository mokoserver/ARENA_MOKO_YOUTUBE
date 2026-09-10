from pathlib import Path
import json,base64,hashlib
import cairosvg
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];B=R/'telegram_avatars/group05';prev=R/'telegram_avatars/concept03'
for f in ['png','svg','source']:(B/f).mkdir(parents=True,exist_ok=True)
ns={};exec((R/'branding/source/build.py').read_text().split('files=[]')[0],ns)
mark,text,tw=ns['mark'],ns['text'],ns['tw'];W='#F7F9FC'
old=(prev/'svg/03_moko_systems.svg').read_text();a=old.index('<rect x="264"');z=old.index('<path d="M0 750');prefix,suffix=old[:a],old[z:]
width=tw('MOKO',244,'Jost',500);tracking=(width-tw('SYSTEMS',122,'Jost',500))/6
variants=[('Г4','group_04_symbol','Фирменный знак','Основная группа обозначена самим MOKO',mark(207,212,610,mono=W)),('Г5','group_05_wordmark','MOKO / SYSTEMS','Название компании вместо пиктограммы',text('MOKO',512,438,244,W,'Jost',500,anchor='middle')+text('SYSTEMS',512,610,122,W,'Jost',500,anchor='middle',spacing=tracking)),('Г6','group_06_symbol_systems','Знак + SYSTEMS','Фирменный знак и явное название направления',mark(309.5,205,405,mono=W)+text('SYSTEMS',512,650,123,W,'Jost',550,anchor='middle'))]
records=[]
for code,slug,title,desc,graphic in variants:
 s=prefix+graphic+suffix;assert s.startswith(prefix) and s.endswith(suffix)
 (B/'svg'/f'{slug}.svg').write_text(s);cairosvg.svg2png(bytestring=s.encode(),write_to=str(B/'png'/f'{slug}.png'))
 records.append(dict(code=code,slug=slug,title=title,description=desc,png=f'png/{slug}.png',svg=f'svg/{slug}.svg'))
def circle(p,n):
 im=Image.open(p).convert('RGBA').resize((n,n),Image.Resampling.LANCZOS);m=Image.new('L',(n*3,n*3));ImageDraw.Draw(m).ellipse((0,0,n*3-1,n*3-1),fill=255);im.putalpha(m.resize((n,n),Image.Resampling.LANCZOS));return im
f=lambda n:ImageFont.truetype(str(R/'brand/Inter.ttf'),n)
board=Image.new('RGB',(1440,1120),'#0B1220');d=ImageDraw.Draw(board)
d.text((70,45),'MOKO / TELEGRAM · НОВЫЕ ВАРИАНТЫ ДЛЯ ГРУППЫ',font=f(24),fill='#A4B4C9')
d.text((70,100),'Основная группа — это MOKO Systems.',font=f(42),fill=W)
d.text((70,166),'Не значок «группы», а фирменный знак или название компании',font=f(23),fill='#A4B4C9')
for n,r in enumerate(records):
 x=72+n*442;y=251;im=circle(B/r['png'],322);board.paste(im,(x+38,y),im)
 d.text((x+199,603),r['code']+' · '+r['title'],font=f(25),fill=W,anchor='mt');d.text((x+199,646),r['description'],font=f(15),fill='#A4B4C9',anchor='mt')
 im=circle(B/r['png'],48);board.paste(im,(x+80,705),im);d.text((x+145,721),'48 px',font=f(17),fill='#A4B4C9')
 if r['code']=='Г6':d.text((x+233,724),'РЕКОМЕНДУЮ',font=f(12),fill='#B8EB55')
d.line((70,805,1370,805),fill='#293C55',width=2)
news=R/'telegram_avatars/alternatives04/png/news_01_megaphone.png';im=circle(news,140);board.paste(im,(80,859),im)
d.text((255,881),'Для новостей выбран мегафон',font=f(28),fill=W)
d.text((255,930),'Остальные четыре аватара и оформление фона не меняем.',font=f(21),fill='#A4B4C9')
d.text((70,1045),'Мой выбор для группы — Г6: знак MOKO + SYSTEMS.',font=f(25),fill=W)
board.save(B/'MOKO_Группа_Новые_варианты.jpg',quality=93,optimize=True)
def uri(p):return 'data:image/svg+xml;base64,'+base64.b64encode(p.read_bytes()).decode()
css='''*{box-sizing:border-box}body{margin:0;background:#0b1220;color:#f7f9fc;font:16px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}main{max-width:1050px;margin:auto;padding:28px 20px 50px}.eyebrow{font-size:11px;letter-spacing:.15em;color:#9fb2ca}h1{font-size:clamp(30px,5vw,44px);line-height:1.1;margin:18px 0}p{color:#a4b4c9}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin:30px 0}.card{border:1px solid #30415a;border-radius:16px;background:#142137;padding:20px 15px;text-align:center}.open{border:0;background:none;padding:0;border-radius:50%;max-width:100%;cursor:zoom-in}.open img{display:block;width:240px;max-width:100%;border-radius:50%}h2{font-size:19px;margin:16px 0 7px}.card p{font-size:13px;min-height:40px}.mini{display:flex;align-items:center;justify-content:center;gap:14px;color:#9fb2ca;font-size:12px}.mini img{width:48px;height:48px;border-radius:50%}.tag{color:#b8eb55;font-size:11px;margin-top:14px}.selected{display:flex;gap:18px;align-items:center;border:1px solid #30415a;background:#142137;border-radius:16px;padding:18px}.selected img{width:88px;height:88px;border-radius:50%}.selected p{margin:4px 0;font-size:14px}.note{border-left:3px solid #b8eb55;background:#142137;padding:12px 16px}.foot{border-top:1px solid #30415a;padding-top:20px;margin-top:32px;color:#91a5bf;font-size:12px}dialog{max-width:95vw;max-height:95vh;background:#0b1220;color:white;padding:12px;border:1px solid #536880;border-radius:15px}dialog::backdrop{background:#000d}dialog img{display:block;width:auto;height:auto;max-width:86vw;max-height:76vh;border-radius:50%;margin:12px auto}.bar{display:flex;align-items:center;justify-content:space-between;gap:14px}#close{padding:10px 13px;background:#1d304b;color:white;border:1px solid #536880;border-radius:8px;cursor:pointer}@media(max-width:650px){.grid{grid-template-columns:1fr}.card{padding:20px}.open img{width:235px}.card p{min-height:0}main{padding:25px 16px}.selected img{width:66px;height:66px}.selected{gap:12px}.selected p{font-size:12px}}'''
s='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MOKO — новые варианты для группы</title><style>'+css+'</style></head><body><main><div class="eyebrow">MOKO / TELEGRAM · ВАРИАНТЫ ДЛЯ ГРУППЫ</div><h1>Основная группа —<br>это MOKO Systems.</h1><p>Отказываемся от абстрактных узлов, схем и человечков. Пусть основную группу представляет сам бренд: знак, название или их сочетание. Фактуру, цвет и нижнюю подпись сохраняем.</p><p class="note">Рекомендую Г6 — крупный знак MOKO и надпись SYSTEMS. Это отличается от остальных аватаров по главному элементу, но остаётся в общей фирменной семье.</p><div class="grid">'
for r in records:
 u=uri(B/r['svg']);s+=f'<article class="card"><button class="open" aria-label="Увеличить {r["code"]}"><img src="{u}" alt="{r["code"]} · {r["title"]}"></button><h2>{r["code"]} · {r["title"]}</h2><p>{r["description"]}</p><div class="mini"><img src="{u}" alt="Малый размер"><span>48 px</span></div>'+('<div class="tag">РЕКОМЕНДУЮ</div>' if r['code']=='Г6' else '')+'</article>'
s+='</div><div class="selected"><img src="'+uri(R/'telegram_avatars/alternatives04/svg/news_01_megaphone.svg')+'" alt="Мегафон для новостей"><div><strong>Новости: мегафон выбран</strong><p>Остальные четыре аватара не менялись.</p></div></div><p>В Г5 слово SYSTEMS растянуто по ширине MOKO. В Г4 и Г6 использована геометрия исходного фирменного знака в белой версии; нижняя подпись остаётся с красным знаком.</p><footer class="foot">Три варианта на выбор. Финальная сборка ожидает выбора аватара группы. В Telegram ничего не установлено.</footer></main><dialog id="zoom"><div class="bar"><span id="caption"></span><button id="close">Закрыть ✕</button></div><img id="large" alt=""></dialog><script>const d=document.getElementById("zoom"),im=document.getElementById("large");document.querySelectorAll(".open").forEach(b=>b.onclick=()=>{const a=b.querySelector("img");im.src=a.src;im.alt=a.alt;document.getElementById("caption").textContent=a.alt;d.showModal()});document.getElementById("close").onclick=()=>d.close();d.onclick=e=>{if(e.target===d)d.close()};</script></body></html>'
(B/'MOKO_Группа_Выбор.html').write_text(s)
q={'status':'group_selection_pending','news_selected':'Н1 — Мегафон','other_four_unchanged':True,'background_and_footer_unchanged':True,'files':[]}
for r in records:
 p=B/r['png'];im=Image.open(p);assert im.size==(1024,1024);im.verify();q['files'].append({'file':r['png'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
assert abs(tw('SYSTEMS',122,'Jost',500,tracking)-width)<.01
q['stacked_systems_width_matches_moko']=True
(B/'source/QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2));(B/'source/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
print('Three group alternatives ready')
