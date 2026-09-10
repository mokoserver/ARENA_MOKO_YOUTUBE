from pathlib import Path
import io,json,base64,hashlib,math
import numpy as np
import cv2
from PIL import Image,ImageDraw,ImageFilter,ImageChops,ImageFont
R=Path(__file__).resolve().parents[2];T=R/'telegram_avatars';B=T/'bc_variants'
for f in ['jpg','source']:(B/f).mkdir(parents=True,exist_ok=True)
u={'__file__':str(T/'source/build_bold_concepts.py')};exec((T/'source/build_bold_concepts.py').read_text().split('styles=[')[0],u)
records=u['records'];masks=u['masks'];alpha=u['alpha'];brand=u['brand'];svgim=u['svgim'];mark=u['mark'];rgb=u['rgb'];image=u['image'];N=1024
Y,X=np.mgrid[0:N,0:N];XX=(X-512)/512;YY=(Y-512)/512
accents=['#59CDFF','#BB91FF','#FF777F','#53E3C9','#FFAB63','#ECD084']
def accent(r):return accents[[v['slug'] for v in records].index(r['slug'])]
def body_gradient(col):
 c=rgb(col);shade=np.exp(-((XX-.05)**2+(YY+.2)**2)/.72);a=np.empty((N,N,3));a[:]=rgb('#08131F');a+=shade[:,:,None]*c[None,None,:]*.10;return image(a)
def halo(im,col,m,opacity=.35):
 alpha(im,col,m.filter(ImageFilter.GaussianBlur(19)),opacity);alpha(im,col,m.filter(ImageFilter.GaussianBlur(6)),opacity*.65)
def circuit(im,col,light=False):
 d=ImageDraw.Draw(im);c=rgb(col);ink=tuple((c*.28+(255*.72 if light else 12)).clip(0,255).astype(int))
 paths=[[(71,244),(181,244),(224,202),(224,118),(415,118)],[(950,271),(838,271),(800,232),(800,155),(653,155)],[(63,584),(130,584),(200,654),(200,728),(300,728)],[(960,605),(892,605),(839,658),(839,739),(726,739)]]
 for p in paths:
  d.line(p,fill=ink,width=4,joint='curve');x,y=p[-1];d.ellipse((x-6,y-6,x+6,y+6),outline=ink,width=3)

def neon(r,m):
 col=accent(r);im=body_gradient(col);circuit(im,col);d=ImageDraw.Draw(im)
 for a,b in [(12,65),(112,163),(195,253),(291,343)]:d.arc((36,36,988,988),a,b,fill=col,width=12)
 d.ellipse((62,62,962,962),outline='#294057',width=2)
 ghost=svgim(mark(203,230,619,mono=col,opacity=.025));im.paste(ghost,(0,0),ghost)
 er=Image.fromarray(cv2.erode(np.array(m),np.ones((49,49),np.uint8)))
 edge=ImageChops.subtract(m,er)
 alpha(im,col,m,.12);halo(im,col,edge,.52);alpha(im,col,edge)
 inner=ImageChops.subtract(m,Image.fromarray(cv2.erode(np.array(m),np.ones((7,7),np.uint8))))
 alpha(im,'#F8FCFF',inner,.45)
 d=ImageDraw.Draw(im);d.line((295,783,729,783),fill=tuple((rgb(col)*.5).astype(int)),width=3)
 brand(im,877,85,108);d.line((407,924,617,924),fill=col,width=5)
 return im

def display(r,m):
 col=accent(r);im=body_gradient(col);d=ImageDraw.Draw(im)
 # Broad colored brackets carry category color even at small sizes.
 d.arc((33,33,991,991),117,245,fill=col,width=38);d.arc((33,33,991,991),297,65,fill=col,width=12)
 d.ellipse((73,73,951,951),outline='#304A61',width=2)
 panel=[(226,139),(787,139),(864,216),(864,735),(160,735),(160,205)]
 d.polygon(panel,fill='#102135');d.line(panel+[panel[0]],fill='#344A61',width=3)
 d.line((247,142,770,142),fill=col,width=8)
 for x in [240,268,296]:d.rectangle((x,167,x+12,173),fill=col)
 # Restrained watermark keeps the face uncluttered.
 ghost=svgim(mark(246,288,532,mono=col,opacity=.035));im.paste(ghost,(0,0),ghost)
 alpha(im,'#000610',ImageChops.offset(m,6,9),.6)
 alpha(im,'#FFF0B6' if r['slug']=='06_johnny_respect' else '#F6F8FC',m)
 d=ImageDraw.Draw(im);d.line((160,754,864,754),fill=col,width=7)
 d.rounded_rectangle((280,788,744,916),radius=20,fill='#091321',outline='#344A61',width=2)
 brand(im,877,85,108)
 return im

def light_scheme(r,m):
 col=r['color'] if r['slug']!='06_johnny_respect' else '#98722C'
 im=Image.new('RGB',(N,N),'#F0F3EF');d=ImageDraw.Draw(im)
 for x in range(0,N,64):d.line((x,0,x,N),fill='#E2E7E3',width=1)
 for y in range(0,N,64):d.line((0,y,N,y),fill='#E2E7E3',width=1)
 circuit(im,col,True)
 d.polygon([(0,0),(414,0),(0,257)],fill=col);d.polygon([(1024,758),(620,1024),(1024,1024)],fill=col)
 etch=svgim(mark(372,257,663,mono='#132C44',opacity=.035));im.paste(etch,(0,0),etch)
 if r['slug']=='03_moko_systems':
  g=svgim(mark(207,212,610));im.paste(g,(0,0),g)
 else:alpha(im,col,m)
 d=ImageDraw.Draw(im);d.line((295,774,795,774),fill=col,width=5)
 brand(im,891,94,116,fg='#142A42')
 return im

def diagonal(r,m):
 col=r['color'] if r['slug']!='06_johnny_respect' else '#A27927'
 im=Image.new('RGB',(N,N),'#F6F1E8');d=ImageDraw.Draw(im)
 d.polygon([(0,0),(538,0),(221,1024),(0,1024)],fill=col)
 d.polygon([(538,0),(568,0),(251,1024),(221,1024)],fill='#14273D')
 # White logos are etched into the colored side only.
 etch=svgim(mark(-125,146,430,mono='#FFFFFF',opacity=.08)+mark(-94,668,380,mono='#FFFFFF',opacity=.09));im.paste(etch,(0,0),etch)
 moved=Image.new('L',(N,N));moved.paste(m.resize((942,942),Image.Resampling.LANCZOS),(105,0))
 # Continuous silhouette, two inks: inversion precisely follows the diagonal field.
 region=Image.new('L',(N,N));ImageDraw.Draw(region).polygon([(0,0),(568,0),(251,1024),(0,1024)],fill=255)
 alpha(im,'#14273D',moved);alpha(im,'#FFFFFF',ImageChops.multiply(moved,region))
 d=ImageDraw.Draw(im);d.line((329,781,850,781),fill='#14273D',width=7)
 d.line((329,781,485,781),fill=col,width=10)
 brand(im,894,92,112,fg='#14273D')
 return im
styles=[{'id':'b1','label':'Б1','name':'Неоновый контур','desc':'Тёмная плата, светящиеся контуры и полупрозрачная заливка символов.','render':neon},{'id':'b2','label':'Б2','name':'Контрастный дисплей','desc':'Светлые символы, широкие цветные акценты и более спокойный фон.','render':display},{'id':'c1','label':'В1','name':'Светлая схема','desc':'Светлая основа, цветные символы и тонкие инженерные линии.','render':light_scheme},{'id':'c2','label':'В2','name':'Диагональ 2.0','desc':'Крупное цветовое поле и двухцветный символ на границе диагонали.','render':diagonal}]
files=[]
for st in styles:
 for r,m in zip(records,masks):
  p=B/'jpg'/f'{st["id"]}_{r["slug"]}.jpg';st['render'](r,m).save(p,quality=92,subsampling=0,optimize=True)
  files.append({'style':st['id'],'slug':r['slug'],'title':r['title'],'file':str(p.relative_to(B)),'source_symbol':r['source_svg']})
rows=[('b','Б / Инженерный модуль','Исходное понравившееся направление.',T/'bold_concepts/jpg'),('b1','Б1 / Неоновый контур',styles[0]['desc'],B/'jpg'),('b2','Б2 / Контрастный дисплей',styles[1]['desc'],B/'jpg'),('c','В / Графический знак','Исходное понравившееся направление.',T/'bold_concepts/jpg'),('c1','В1 / Светлая схема',styles[2]['desc'],B/'jpg'),('c2','В2 / Диагональ 2.0',styles[3]['desc'],B/'jpg')]
def circle(im,n):
 im=im.convert('RGBA').resize((n,n),Image.Resampling.LANCZOS);mask=Image.new('L',(n*3,n*3));ImageDraw.Draw(mask).ellipse((0,0,n*3-1,n*3-1),fill=255);im.putalpha(mask.resize((n,n),Image.Resampling.LANCZOS));return im
f=lambda n:ImageFont.truetype(str(R/'brand/Inter.ttf'),n)
board=Image.new('RGB',(1680,2560),'#0B1220');d=ImageDraw.Draw(board)
d.text((70,42),'MOKO / TELEGRAM · РАЗВИВАЕМ Б И В',font=f(25),fill='#A5B5C9');d.text((70,95),'Четыре новых варианта на выбранной основе',font=f(43),fill='#F7F9FC');d.text((70,164),'24 новых аватара. Б и В оставлены рядом для сравнения.',font=f(24),fill='#A5B5C9')
short=['Новости','Чат новостей','MOKO Systems','MOKO SE Bot','Связь с MOKO','Johnny Respect']
for i,(sid,title,desc,folder) in enumerate(rows):
 y=230+i*372;d.text((70,y),title,font=f(29),fill='#F7F9FC');d.text((70,y+44),desc,font=f(18),fill='#A5B5C9')
 for n,r in enumerate(records):
  a=circle(Image.open(folder/f'{sid}_{r["slug"]}.jpg'),195);x=70+n*259;board.paste(a,(x+20,y+88),a);d.text((x+117,y+300),short[n],font=f(17),fill='#F7F9FC',anchor='mt')
 if i<5:d.line((70,y+346,1610,y+346),fill='#293d56',width=2)
d.text((70,2480),'А и прежний вариант — в архиве. Выбранные символы не меняем.',font=f(22),fill='#A5B5C9');board.save(B/'MOKO_Б_и_В_Сравнение.jpg',quality=90,optimize=True)

def uri(p):
 im=Image.open(p).convert('RGB');im.thumbnail((560,560));o=io.BytesIO();im.save(o,'WEBP',quality=86,method=6);return 'data:image/webp;base64,'+base64.b64encode(o.getvalue()).decode()
# Reuse tested layout and interactions, with filters extended to the six active directions.
old=(T/'bold_concepts/MOKO_Новые_концепты.html').read_text();css=old.split('<style>')[1].split('</style>')[0]
s='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MOKO — новые варианты Б и В</title><style>'+css+'</style></head><body><main><div class="eyebrow">MOKO / TELEGRAM · РАЗВИВАЕМ ВЫБРАННЫЕ НАПРАВЛЕНИЯ</div><h1>Б и В.<br>Ещё четыре варианта.</h1><p class="intro">По два продолжения каждого понравившегося направления. Мегафон, пирамиды, диалоги, робот SE, гарнитура и JR остаются. Меняем способ подачи, но не назначение аватаров.</p><p class="note">А и прежняя версия убраны в архив. Здесь только Б, В и их новые варианты. Выберите направление кнопками; на любой аватар можно нажать для увеличения.</p><div class="tabs" role="group" aria-label="Направления">'
for key,title in [('all','Все'),('new','Только новые'),('b','Б · Основа'),('b1','Б1 · Контур'),('b2','Б2 · Дисплей'),('c','В · Основа'),('c1','В1 · Схема'),('c2','В2 · Диагональ')]:s+=f'<button data-filter="{key}" aria-pressed="{str(key=="new").lower()}">{title}</button>'
s+='</div>'
for sid,title,desc,folder in rows:
 hidden=' hidden' if sid in ['b','c'] else ''
 s+=f'<section class="section" data-style="{sid}"{hidden}><h2>{title}</h2><p>{desc}</p><div class="grid">'
 for n,r in enumerate(records):
  p=folder/f'{sid}_{r["slug"]}.jpg';s+=f'<article class="card"><button class="open"><img id="img_{sid}_{n}" src="{uri(p)}" alt="{title} — {r["title"]}"></button><h3>{r["title"]}</h3><small>{"Понравившаяся основа" if sid in ["b","c"] else "Новый вариант · 1024 × 1024"}</small></article>'
 s+='</div><div class="sizecheck"><span>Проверка в списке чатов</span>'+''.join(f'<img data-ref="img_{sid}_{n}" alt="{r["title"]}">' for n,r in enumerate(records))+'</div></section>'
s+='<p class="note">Б1 — акцент на контуре. Б2 — на контрасте символа. В1 — на светлом инженерном оформлении. В2 — на крупной диагонали и двухцветной графике. Можно выбрать одно направление целиком или назвать удачные детали для следующей доработки.</p><footer class="foot">24 новых аватара + 12 из направлений Б и В для сравнения. Финальный вариант ещё не выбран. На площадках ничего не установлено.</footer></main><dialog id="zoom"><div class="bar"><span id="caption"></span><button id="close">Закрыть ✕</button></div><img id="large" alt=""></dialog><script>document.querySelectorAll("img[data-ref]").forEach(i=>i.src=document.getElementById(i.dataset.ref).src);document.querySelectorAll("[data-filter]").forEach(b=>b.onclick=()=>{document.querySelectorAll("[data-filter]").forEach(x=>x.setAttribute("aria-pressed",String(x===b)));document.querySelectorAll(".section").forEach(x=>{const k=b.dataset.filter;x.hidden=k==="new"?["b","c"].includes(x.dataset.style):k!=="all"&&x.dataset.style!==k})});const d=document.getElementById("zoom"),im=document.getElementById("large");document.querySelectorAll(".open").forEach(b=>b.onclick=()=>{const a=b.querySelector("img");im.src=a.src;im.alt=a.alt;document.getElementById("caption").textContent=a.alt;d.showModal()});document.getElementById("close").onclick=()=>d.close();d.onclick=e=>{if(e.target===d)d.close()};</script></body></html>'
(B/'MOKO_Б_и_В_Новые_варианты.html').write_text(s)
q={'new_directions':4,'new_avatars':24,'parent_directions':['Б','В'],'archived_directions':['А','previous'],'final_choice':None,'files':[]}
for r in files:
 p=B/r['file'];im=Image.open(p);assert im.size==(1024,1024);im.verify();q['files'].append({'file':r['file'],'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(B/'source/manifest.json').write_text(json.dumps(files,ensure_ascii=False,indent=2));(B/'source/QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2))
print('24 variants ready; HTML bytes:',(B/'MOKO_Б_и_В_Новые_варианты.html').stat().st_size)
