from pathlib import Path
import json,base64,hashlib
import cairosvg
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];B=R/'telegram_avatars/alternatives04';PREV=R/'telegram_avatars/concept03'
for d in ['png','svg','source']:(B/d).mkdir(parents=True,exist_ok=True)
W='#F7F9FC';G='#B93636'
news={
 'megaphone':f'<g fill="{W}"><rect x="205" y="349" width="106" height="145" rx="26"/><path d="M290 350L594 234V603L290 492Z"/><rect x="575" y="219" width="44" height="397" rx="21"/><path d="M325 495L423 530L391 686L307 655Z"/></g><g fill="none" stroke="{W}" stroke-width="34" stroke-linecap="round"><path d="M687 416H823M672 305L772 242M672 528L772 591"/></g>',
 'broadcast':f'<g fill="none" stroke="{W}" stroke-width="36" stroke-linecap="round" stroke-linejoin="round"><path d="M316 213C194 332 194 457 316 579M708 213C830 332 830 457 708 579M406 290C343 346 343 432 406 491M618 290C681 346 681 432 618 491M512 442V663M414 678H610"/></g><circle cx="512" cy="388" r="61" fill="{W}"/>',
 'lightning':f'<path d="M588 181L282 487H462L402 717L744 363H550L588 181Z" fill="{W}" stroke="{W}" stroke-width="10" stroke-linejoin="round"/>'}
group={
 'network':f'<g stroke="{W}" stroke-width="39" stroke-linecap="round"><path d="M328 272L708 637M708 272L328 637"/></g><g fill="{W}"><circle cx="512" cy="455" r="85"/><circle cx="328" cy="272" r="65"/><circle cx="708" cy="272" r="65"/><circle cx="328" cy="637" r="65"/><circle cx="708" cy="637" r="65"/></g>',
 'sections':f'<path d="M512 322V446H286V542M512 446V542M512 446H738V542" fill="none" stroke="{W}" stroke-width="35" stroke-linecap="round" stroke-linejoin="round"/><g fill="{W}"><rect x="422" y="200" width="180" height="122" rx="25"/><rect x="218" y="542" width="136" height="136" rx="26"/><rect x="444" y="542" width="136" height="136" rx="26"/><rect x="670" y="542" width="136" height="136" rx="26"/></g>',
 'team':f'<g fill="{W}"><circle cx="307" cy="375" r="61"/><circle cx="717" cy="375" r="61"/><path d="M195 649V551Q195 466 307 466Q419 466 419 551V649Z"/><path d="M605 649V551Q605 466 717 466Q829 466 829 551V649Z"/></g><path d="M370 681V520Q370 410 512 410Q654 410 654 520V681Z" fill="{W}" stroke="{G}" stroke-width="24" stroke-linejoin="round"/><circle cx="512" cy="288" r="78" fill="{W}"/>'}
items=[('N1','Н1','news_01_megaphone','Новости · Мегафон','Обновления и объявления','news','megaphone',True),('N2','Н2','news_02_broadcast','Новости · Вещание','Публикации и трансляция новостей','news','broadcast',False),('N3','Н3','news_03_lightning','Новости · Молния','Быстрые и важные обновления','news','lightning',False),('G1','Г1','group_01_network','Группа · Связанные узлы','Взаимодействие участников','group','network',False),('G2','Г2','group_02_sections','Группа · Дерево разделов','Одна группа — несколько тем','group','sections',True),('G3','Г3','group_03_team','Группа · Команда','Люди и общение','group','team',False)]
records=[]
for code,label,slug,title,desc,kind,icon,recommended in items:
 old=(PREV/'svg'/('01_news.svg' if kind=='news' else '03_moko_systems.svg')).read_text()
 start=old.index('<rect x="238"' if kind=='news' else '<rect x="264"')
 end=old.index('<path d="M0 750')
 prefix,suffix=old[:start],old[end:]
 s=prefix+(news[icon] if kind=='news' else group[icon])+suffix
 assert s[:start]==prefix and s.endswith(suffix)
 (B/'svg'/f'{slug}.svg').write_text(s);cairosvg.svg2png(bytestring=s.encode(),write_to=str(B/'png'/f'{slug}.png'))
 records.append(dict(code=code,label=label,slug=slug,title=title,description=desc,kind=kind,recommended=recommended,png=f'png/{slug}.png',svg=f'svg/{slug}.svg'))
def circle(path,n):
 im=Image.open(path).convert('RGBA').resize((n,n),Image.Resampling.LANCZOS);mask=Image.new('L',(n*3,n*3));ImageDraw.Draw(mask).ellipse((0,0,n*3-1,n*3-1),fill=255);im.putalpha(mask.resize((n,n),Image.Resampling.LANCZOS));return im
f=lambda n:ImageFont.truetype(str(R/'brand/Inter.ttf'),n)
board=Image.new('RGB',(1440,1510),'#0B1220');d=ImageDraw.Draw(board)
d.text((70,46),'MOKO / TELEGRAM · ВЫБИРАЕМ ДВА СИМВОЛА',font=f(24),fill='#A4B4C9')
d.text((70,99),'Альтернативы для новостей и группы',font=f(42),fill=W)
d.text((70,166),'Фактура, цвета и подпись MOKO — без изменений',font=f(23),fill='#A4B4C9')
d.text((70,221),'НОВОСТИ',font=f(21),fill='#55C9FF');d.text((70,801),'ГРУППА MOKO SYSTEMS',font=f(21),fill='#ED6262')
for n,r in enumerate(records):
 x=72+n%3*442;y=265+n//3*580;a=circle(B/r['png'],310);board.paste(a,(x+44,y),a)
 name=r['label']+' · '+r['title'].split(' · ')[1]
 d.text((x+199,y+329),name,font=f(25),fill=W,anchor='mt');d.text((x+199,y+371),r['description'],font=f(16),fill='#A4B4C9',anchor='mt')
 a=circle(B/r['png'],48);board.paste(a,(x+65,y+423),a)
 d.text((x+129,y+435),'48 px',font=f(17),fill='#A4B4C9')
 if r['recommended']:d.text((x+213,y+438),'РЕКОМЕНДУЮ',font=f(13),fill='#B8EB55')
d.line((70,764,1370,764),fill='#293C55',width=2);d.line((70,1380,1370,1380),fill='#293C55',width=2)
d.text((70,1418),'Мой выбор: Н1 — мегафон  +  Г2 — дерево разделов',font=f(25),fill=W)
board.save(B/'MOKO_Новости_и_группа_Альтернативы.jpg',quality=93,optimize=True)
def uri(r):return 'data:image/svg+xml;base64,'+base64.b64encode((B/r['svg']).read_bytes()).decode()
css='''*{box-sizing:border-box}body{margin:0;background:#0b1220;color:#f7f9fc;font:16px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}main{max-width:1100px;margin:auto;padding:30px 20px 55px}.eyebrow{font-size:11px;color:#a4b4c9;letter-spacing:.13em}h1{font-size:clamp(30px,4vw,44px);line-height:1.1;margin:18px 0}h2{font-size:25px;margin:36px 0 10px}p{color:#a4b4c9}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.card{background:#142137;border:1px solid #30415a;padding:20px 13px;border-radius:16px;text-align:center}.visual{border:0;border-radius:50%;background:none;padding:0;max-width:100%;cursor:zoom-in}.visual img{width:236px;max-width:100%;border-radius:50%;display:block}h3{font-size:18px;margin:15px 0 6px}.card p{font-size:13px;margin:5px 0 16px}.mini{display:flex;align-items:center;justify-content:center;gap:13px;color:#a4b4c9;font-size:12px}.mini img{width:48px;height:48px;border-radius:50%}.tag{font-size:11px;color:#b8eb55;margin-top:13px}.note{border-left:3px solid #b8eb55;padding:12px 16px;background:#142137}.foot{border-top:1px solid #30415a;margin-top:32px;padding-top:17px;font-size:12px;color:#91a5bf}dialog{max-width:95vw;max-height:95vh;padding:12px;background:#0b1220;color:white;border:1px solid #536880;border-radius:16px}dialog::backdrop{background:#000d}dialog img{display:block;width:auto;height:auto;max-width:86vw;max-height:76vh;margin:12px auto;border-radius:50%}.bar{display:flex;align-items:center;justify-content:space-between;gap:14px}#close{padding:10px 13px;background:#1d304b;color:white;border:1px solid #536880;border-radius:8px;cursor:pointer}@media(max-width:650px){.grid{grid-template-columns:1fr}.card{display:grid;grid-template-columns:140px 1fr;gap:10px;align-items:center;text-align:left;padding:16px 12px}.visual img{width:140px}h3{font-size:17px;margin-top:0}.mini{justify-content:flex-start}.mini img{width:40px;height:40px}.card p{font-size:12px;margin-bottom:10px}main{padding:25px 16px}.tag{font-size:10px}}'''
s='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MOKO — альтернативы для новостей и группы</title><style>'+css+'</style></head><body><main><div class="eyebrow">MOKO / TELEGRAM · ВЫБИРАЕМ ДВА СИМВОЛА</div><h1>Новости и группа.<br>По три альтернативы.</h1><p>Меняется только крупный символ. Фактура, цвета и нижняя подпись из концепта 03 сохранены. Остальные четыре аватара не менялись.</p><p class="note">Мой выбор — <b>Н1: мегафон</b> для новостей и <b>Г2: дерево разделов</b> для группы. Нажмите на любой аватар, чтобы рассмотреть его крупно.</p>'
for kind,title in [('news','Новости · выбрать один'),('group','Группа MOKO Systems · выбрать один')]:
 s+='<section><h2>'+title+'</h2><div class="grid">'
 for r in records:
  if r['kind']!=kind:continue
  s+=f'<article class="card"><button class="visual" aria-label="Увеличить {r["label"]}"><img src="{uri(r)}" alt="{r["label"]}: {r["title"]}"></button><div><h3>{r["label"]} · {r["title"].split(" · ")[1]}</h3><p>{r["description"]}</p><div class="mini"><img src="{uri(r)}" alt="Малый размер"><span>В списке чатов</span></div>'+('<div class="tag">РЕКОМЕНДУЮ</div>' if r['recommended'] else '')+'</div></article>'
 s+='</div></section>'
s+='<p class="note">Мегафон — объявления и новые публикации. Дерево — одна группа, внутри которой несколько разделов. У молнии возможна ассоциация с электротехникой, поэтому для новостей я предпочитаю мегафон.</p><footer class="foot">Варианты на выбор, не новая утверждённая сборка. Предыдущие файлы сохранены. В Telegram ничего не установлено.</footer></main><dialog id="zoom"><div class="bar"><span id="caption"></span><button id="close">Закрыть ✕</button></div><img id="large" alt=""></dialog><script>const d=document.getElementById("zoom"),im=document.getElementById("large");document.querySelectorAll(".visual").forEach(b=>b.onclick=()=>{const a=b.querySelector("img");im.src=a.src;im.alt=a.alt;document.getElementById("caption").textContent=a.alt;d.showModal()});document.getElementById("close").onclick=()=>d.close();d.onclick=e=>{if(e.target===d)d.close()};</script></body></html>'
(B/'MOKO_Выбор_символов.html').write_text(s)
(B/'source/manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
q={'status':'alternatives_awaiting_selection','background_and_footer_preserved':True,'other_four_avatars_changed':False,'files':[]}
for r in records:
 p=B/r['png'];im=Image.open(p);assert im.size==(1024,1024);im.verify()
 q['files'].append({'file':r['png'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(B/'source/QA.json').write_text(json.dumps(q,indent=2))
print('Six alternatives ready')
