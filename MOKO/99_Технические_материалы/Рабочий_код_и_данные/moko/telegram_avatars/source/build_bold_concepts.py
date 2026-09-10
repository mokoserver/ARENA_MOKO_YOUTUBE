from pathlib import Path
import io,json,base64,hashlib,math
import numpy as np
from PIL import Image,ImageDraw,ImageFilter,ImageChops,ImageFont
import cairosvg
R=Path(__file__).resolve().parents[2];T=R/'telegram_avatars';B=T/'bold_concepts'
for f in ['jpg','source']:(B/f).mkdir(parents=True,exist_ok=True)
ns={};exec((R/'branding/source/build.py').read_text().split('files=[]')[0],ns)
mark,text,tw=ns['mark'],ns['text'],ns['tw']
records=json.loads((T/'selected/manifest.json').read_text())
N=1024; yy,xx=np.mgrid[0:N,0:N];X=(xx-512)/512;Y=(yy-512)/512;rad=np.sqrt(X*X+Y*Y)
def rgb(h):return np.array([int(h[i:i+2],16) for i in [1,3,5]],float)
def image(a):return Image.fromarray(np.clip(a,0,255).astype('uint8'),'RGB')
def grad(top,bottom):return image(np.broadcast_to(rgb(top)[None,None,:]*(1-yy[:,:,None]/1023)+rgb(bottom)[None,None,:]*(yy[:,:,None]/1023),(N,N,3)))
def alpha(im,color,mask,opacity=1):
 if opacity!=1:mask=mask.point(lambda x:round(x*opacity))
 layer=Image.new('RGB',im.size,color) if isinstance(color,str) else color
 im.paste(layer,(0,0),mask)
def svgim(body):return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=('<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024">'+body+'</svg>').encode()))).convert('RGBA')
def mask_for(r):
 s=(T/r['source_svg']).read_text();start=s.index('r="460"');start=s.index('/>',start)+2;end=s.index('<path d="M0 750');g=s[start:end]
 g=g.replace(r['color'],'#000000').replace('#F7F9FC','#FFFFFF').replace('#F0D48C','#FFFFFF')
 return svgim('<rect width="1024" height="1024" fill="black"/>'+g).convert('L')
def ellipse(box):
 a=Image.new('L',(N,N));ImageDraw.Draw(a).ellipse(box,fill=255);return a

def brand(im,baseline=876,size=86,icon=108,fg='#F7F9FC'):
 total=icon+24+tw('MOKO',size,'Jost',500);x=(1024-total)/2
 layer=svgim(mark(x,baseline-icon*193/271,icon)+text('MOKO',x+icon+24,baseline,size,fg,'Jost',500));im.paste(layer,(0,0),layer)
# Geometrically exact role masks; these remain the same across all concepts.
masks=[mask_for(r) for r in records]
for n,m in enumerate(masks):assert m.getbbox() is not None

# A. Machined medallion, recessed enamel surface and raised ceramic symbols.
def enamel(r,m):
 im=Image.new('RGB',(N,N),'#0a1220')
 light=np.clip(.60-.30*X-.34*Y,0,1)
 metal=75+150*light+30*np.sin((rad-.9)*100)
 arr=np.stack([metal*.93,metal*.98,metal*1.06],axis=2);alpha(im,image(arr),ellipse((26,26,998,998)))
 d=ImageDraw.Draw(im);d.ellipse((36,36,988,988),outline='#9dafbe',width=3);d.ellipse((63,63,961,961),outline='#202d3c',width=14)
 col=rgb(r['color']);shade=np.clip(.78-.25*X-.35*Y,.38,1.15)
 paint=col[None,None,:]*shade[:,:,None]+18*np.exp(-((X+.32)**2+(Y+.45)**2)/.5)[:,:,None]
 # Low-frequency linear grain adds a brushed finish without noisy pixels.
 brush=1.7*np.sin(yy*.40)+1.1*np.sin(yy*.11)
 paint+=brush[:,:,None]
 alpha(im,image(paint),ellipse((83,83,941,941)))
 etch=svgim(mark(71,108,260,mono='#ffffff',opacity=.055)+mark(685,270,260,mono='#ffffff',opacity=.045)+mark(200,569,255,mono='#ffffff',opacity=.04));im.paste(etch,(0,0),etch)
 # Small metallic fasteners, outside the pictogram.
 d=ImageDraw.Draw(im)
 for ang in [45,135,225,315]:
  a=math.radians(ang);cx=512+460*math.cos(a);cy=512+460*math.sin(a)
  d.ellipse((cx-10,cy-10,cx+10,cy+10),fill='#354253',outline='#bbc7d2',width=2);d.line((cx-5,cy-4,cx+5,cy+4),fill='#0e1927',width=3)
 alpha(im,'#000000',ImageChops.offset(m,15,22).filter(ImageFilter.GaussianBlur(13)),.56)
 for off in range(17,0,-1):alpha(im,'#8b723e' if r['slug']=='06_johnny_respect' else '#687a8f',ImageChops.offset(m,off//2,off))
 alpha(im,grad('#FFF0B5','#B99549') if r['slug']=='06_johnny_respect' else grad('#ffffff','#aebed1'),m)
 hi=ImageChops.subtract(m,ImageChops.offset(m,3,4));lo=ImageChops.subtract(m,ImageChops.offset(m,-3,-4))
 alpha(im,'#ffffff',hi,.9);alpha(im,'#65778f',lo,.65)
 # Recessed brand cartouche replaces the old footer strip.
 d=ImageDraw.Draw(im);d.rounded_rectangle((273,777,751,909),radius=33,fill='#0c1727',outline='#899bab',width=3)
 d.line((307,783,717,783),fill='#050e19',width=6);brand(im,869,79,98)
 return im

# B. Luminous technical panel: saturated symbols, circuit traces, dark common base.
def module(r,m):
 col=rgb('#D4B764' if r['slug']=='06_johnny_respect' else r['color']);light=np.exp(-((X-.08)**2+(Y+.30)**2)/.8)
 arr=np.zeros((N,N,3));arr[:]=rgb('#08121F');arr+=light[:,:,None]*col[None,None,:]*.19
 im=image(arr);d=ImageDraw.Draw(im)
 trace=tuple(np.clip(col*.58+15,0,255).astype(int));bright=tuple(np.clip(col*1.10+48,0,255).astype(int))
 for x in range(96,980,64):
  for y in range(96,980,64):
   if (x-512)**2+(y-512)**2<450**2:d.ellipse((x-1,y-1,x+1,y+1),fill='#26384e')
 paths=[[(51,256),(182,256),(238,200),(238,111),(402,111)],[(60,534),(130,534),(199,603),(199,718),(287,718)],[(964,288),(852,288),(809,245),(809,173),(665,173)],[(970,568),(906,568),(843,632),(843,743),(734,743)],[(342,957),(342,930),(182,930),(117,865)],[(682,957),(682,930),(843,930),(908,865)]]
 for path in paths:
  d.line(path,fill=trace,width=5,joint='curve')
  for cx,cy in [path[0],path[-1]]:d.ellipse((cx-7,cy-7,cx+7,cy+7),outline=bright,width=3)
 for a,b in [(15,72),(105,163),(195,253),(285,343)]:d.arc((39,39,985,985),a,b,fill=bright,width=9)
 d.ellipse((62,62,962,962),outline='#2a3c52',width=2)
 ghost=svgim(mark(192,230,640,mono='#ffffff',opacity=.028));im.paste(ghost,(0,0),ghost)
 alpha(im,bright,m.filter(ImageFilter.GaussianBlur(21)),.36)
 alpha(im,bright,m.filter(ImageFilter.GaussianBlur(7)),.32)
 alpha(im,'#020913',ImageChops.offset(m,7,10),.8)
 top=np.minimum(col*1.12+88,255);bottom=np.minimum(col*.95+23,255)
 layer=image(top[None,None,:]*(1-yy[:,:,None]/1023)+bottom[None,None,:]*yy[:,:,None]/1023)
 alpha(im,layer,m)
 alpha(im,'#F7FCFF',ImageChops.subtract(m,ImageChops.offset(m,2,3)),.65)
 d=ImageDraw.Draw(im);d.line((261,782,763,782),fill=trace,width=3);d.line((397,917,627,917),fill=bright,width=4)
 brand(im,877,83,106)
 return im

# C. Bold editorial geometry: light ground, diagonal color field, offset symbol.
def graphic(r,m):
 im=Image.new('RGB',(N,N),'#F2F0E8');d=ImageDraw.Draw(im);col=r['color'] if r['slug']!='06_johnny_respect' else '#CCA955'
 d.polygon([(0,0),(371,0),(154,1024),(0,1024)],fill=col)
 d.polygon([(371,0),(405,0),(188,1024),(154,1024)],fill='#d4d9d7')
 # Deliberate broad facets, drawn from the source logo, not decorative noise.
 etch=svgim(mark(584,-79,615,mono='#17263a',opacity=.045)+mark(-165,680,490,mono='#ffffff',opacity=.14));im.paste(etch,(0,0),etch)
 moved=Image.new('L',(N,N));sm=m.resize((922,922),Image.Resampling.LANCZOS);moved.paste(sm,(111,13))
 alpha(im,'#b1b8b8',ImageChops.offset(moved,8,12),.40)
 alpha(im,'#17263A' if r['slug']!='06_johnny_respect' else '#695126',moved)
 d=ImageDraw.Draw(im);d.line((324,771,854,771),fill='#17263A',width=5)
 # A short role-colored rail ties the main symbol to the colored edge.
 d.rectangle((324,771,470,780),fill=col)
 brand(im,892,93,116,fg='#17263A')
 return im

styles=[{'id':'a','code':'А','name':'Литой жетон','description':'Металлический обод, цветная эмаль и рельефные светлые символы.','render':enamel},{'id':'b','code':'Б','name':'Инженерный модуль','description':'Тёмная панель, светящиеся дорожки и крупные цветные символы.','render':module},{'id':'c','code':'В','name':'Графический знак','description':'Светлая основа, диагональное цветовое поле и контрастная графика.','render':graphic}]
output=[]
for st in styles:
 for r,m in zip(records,masks):
  im=st['render'](r,m);path=B/'jpg'/f'{st["id"]}_{r["slug"]}.jpg';im.save(path,quality=95,subsampling=0,optimize=True)
  output.append({'style':st['id'],'slug':r['slug'],'title':r['title'],'file':str(path.relative_to(B)),'width':1024,'height':1024,'source_symbol':r['source_svg']})

def circle(im,n):
 im=im.convert('RGBA').resize((n,n),Image.Resampling.LANCZOS);mask=Image.new('L',(n*3,n*3));ImageDraw.Draw(mask).ellipse((0,0,n*3-1,n*3-1),fill=255);im.putalpha(mask.resize((n,n),Image.Resampling.LANCZOS));return im
f=lambda n:ImageFont.truetype(str(R/'brand/Inter.ttf'),n)
board=Image.new('RGB',(1680,1910),'#0B1220');d=ImageDraw.Draw(board)
d.text((70,42),'MOKO / TELEGRAM · СМЕЛЫЕ КОНЦЕПТЫ',font=f(25),fill='#A5B5C9');d.text((70,93),'Три новых направления + текущий вариант',font=f(45),fill='#F7F9FC');d.text((70,166),'Символы сохранены. Меняем материал, свет, фон и компоновку.',font=f(24),fill='#A5B5C9')
rows=[('0','Текущий вариант','Фирменная фактура и тёмная нижняя полоса.')]+[(s['id'],s['code']+' / '+s['name'],s['description']) for s in styles]
short=['Новости','Чат новостей','MOKO Systems','MOKO SE Bot','Связь с MOKO','Johnny Respect']
for i,(sid,title,desc) in enumerate(rows):
 y=240+i*397;d.text((70,y),title,font=f(29),fill='#F7F9FC');d.text((70,y+45),desc,font=f(19),fill='#A5B5C9')
 for n,r in enumerate(records):
  p=T/r['source_png'] if sid=='0' else B/'jpg'/f'{sid}_{r["slug"]}.jpg';a=circle(Image.open(p),206);x=70+n*259;board.paste(a,(x+14,y+91),a);d.text((x+117,y+315),short[n],font=f(17),fill='#F7F9FC',anchor='mt')
 if i<3:d.line((70,y+369,1610,y+369),fill='#293d56',width=2)
d.text((70,1848),'Это варианты для сравнения. Текущий комплект не изменён.',font=f(22),fill='#A5B5C9');board.save(B/'MOKO_Сравнение_концептов.jpg',quality=93,optimize=True)

# Embed compact preview JPEGs once per avatar; modal and small-size references reuse them.
def preview_uri(path):
 im=Image.open(path).convert('RGB');im.thumbnail((640,640));o=io.BytesIO();im.save(o,'JPEG',quality=88,subsampling=0,optimize=True);return 'data:image/jpeg;base64,'+base64.b64encode(o.getvalue()).decode()
css='''*{box-sizing:border-box}body{margin:0;background:#0b1220;color:#f7f9fc;font:16px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}main{max-width:1140px;margin:auto;padding:30px 22px 60px}.eyebrow{font-size:11px;letter-spacing:.17em;color:#a5b5c9}h1{font-size:clamp(31px,5vw,50px);line-height:1.07;margin:18px 0}h2{font-size:27px;margin:0}p{color:#a5b5c9}.intro{max-width:760px}.tabs{display:flex;gap:8px;flex-wrap:wrap;margin:25px 0}.tabs button{border:1px solid #40516b;color:#dae5f2;border-radius:24px;padding:9px 14px;background:#142137;cursor:pointer}.tabs button[aria-pressed=true]{color:#0b1220;background:#b8eb55;border-color:#b8eb55}.section{padding-top:20px;margin-top:25px;border-top:1px solid #2c3f58}.section[hidden]{display:none}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin:22px 0}.card{background:#152238;border:1px solid #30445d;border-radius:16px;text-align:center;padding:18px 12px}.open{border:0;border-radius:50%;padding:0;background:none;cursor:zoom-in;max-width:100%}.open img{display:block;width:245px;max-width:100%;border-radius:50%}h3{font-size:16px;margin:13px 0 4px}.card small{font-size:11px;color:#9cafc6}.sizecheck{display:flex;gap:18px;align-items:center;flex-wrap:wrap;background:#111e31;border-radius:13px;padding:16px}.sizecheck img{width:48px;height:48px;border-radius:50%}.sizecheck span{color:#a5b5c9;font-size:12px}.note{border-left:3px solid #b8eb55;padding:12px 16px;background:#142137;font-size:14px}.foot{border-top:1px solid #30445d;margin-top:40px;padding-top:20px;color:#8b9fb9;font-size:12px}dialog{max-width:96vw;max-height:96vh;padding:12px;border:1px solid #516781;background:#0b1220;color:white;border-radius:16px}dialog::backdrop{background:#000d}dialog img{display:block;width:auto;height:auto;max-width:88vw;max-height:76vh;border-radius:50%;margin:12px auto}.bar{display:flex;align-items:center;justify-content:space-between;gap:12px}#close{padding:10px 14px;border:1px solid #516781;border-radius:8px;background:#1b2c45;color:white;cursor:pointer}@media(max-width:650px){main{padding:26px 16px 45px}.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.card{padding:14px 8px}h3{font-size:14px}.open img{width:160px}.sizecheck{gap:13px}.sizecheck img{width:40px;height:40px}.sizecheck span{flex-basis:100%}.tabs button{padding:8px 11px;font-size:12px}}'''
s='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MOKO — три смелых концепта</title><style>'+css+'</style></head><body><main><div class="eyebrow">MOKO / TELEGRAM · ВЫБОР ФИНАЛЬНОГО НАПРАВЛЕНИЯ</div><h1>Знакомые символы.<br>Совсем разный характер.</h1><p class="intro">Три новых направления, по шесть аватаров в каждом. Мегафон, крупный знак MOKO, диалоги, робот SE, гарнитура и JR сохранены. Меняются отделка, свет, фон и компоновка, а не смысл символов.</p><p class="note">Для сравнения добавлен текущий комплект. Переключайте направления и нажимайте на аватары для увеличения. В конце каждого раздела — проверка малого размера.</p><div class="tabs" role="group" aria-label="Выбор концепта">'
for sid,label in [('all','Все концепты'),('a','А · Жетон'),('b','Б · Модуль'),('c','В · Графика'),('0','Текущий')]:s+=f'<button data-filter="{sid}" aria-pressed="{str(sid=="all").lower()}">{label}</button>'
s+='</div>'
for sid,title,desc in [(st['id'],st['code']+' / '+st['name'],st['description']) for st in styles]+[rows[0]]:
 s+=f'<section class="section" data-style="{sid}"><h2>{title}</h2><p>{desc}</p><div class="grid">'
 for n,r in enumerate(records):
  p=T/r['source_png'] if sid=='0' else B/'jpg'/f'{sid}_{r["slug"]}.jpg';key=f'{sid}_{n}';u=preview_uri(p)
  s+=f'<article class="card"><button class="open"><img id="img_{key}" src="{u}" alt="{title} — {r["title"]}"></button><h3>{r["title"]}</h3><small>{"Текущий комплект" if sid=="0" else "Концепт · 1024 × 1024"}</small></article>'
 s+='</div><div class="sizecheck"><span>Проверка в списке чатов</span>'+''.join(f'<img data-ref="img_{sid}_{n}" alt="{r["title"]}">' for n,r in enumerate(records))+'</div></section>'
s+='<p class="note">А — визуализация металла и эмали; Б — цифровая подсветка и инженерная графика; В — плоская контрастная компоновка. Это дизайнерские изображения, а не фотографии физических изделий.</p><footer class="foot">18 новых вариантов + 6 текущих для сравнения. Новое направление ещё не выбрано. Текущий комплект и выбранные символы не изменены. Ничего не установлено в Telegram.</footer></main><dialog id="zoom"><div class="bar"><span id="caption"></span><button id="close">Закрыть ✕</button></div><img id="large" alt=""></dialog><script>document.querySelectorAll("img[data-ref]").forEach(i=>i.src=document.getElementById(i.dataset.ref).src);document.querySelectorAll("[data-filter]").forEach(b=>b.onclick=()=>{document.querySelectorAll("[data-filter]").forEach(x=>x.setAttribute("aria-pressed",String(x===b)));document.querySelectorAll(".section").forEach(x=>x.hidden=b.dataset.filter!=="all"&&x.dataset.style!==b.dataset.filter)});const d=document.getElementById("zoom"),im=document.getElementById("large");document.querySelectorAll(".open").forEach(b=>b.onclick=()=>{const a=b.querySelector("img");im.src=a.src;im.alt=a.alt;document.getElementById("caption").textContent=a.alt;d.showModal()});document.getElementById("close").onclick=()=>d.close();d.onclick=e=>{if(e.target===d)d.close()};</script></body></html>'
(B/'MOKO_Новые_концепты.html').write_text(s)
q={'new_concepts':3,'new_avatars':18,'baseline_changed':False,'final_direction_selected':False,'files':[]}
for r in output:
 p=B/r['file'];im=Image.open(p);assert im.size==(1024,1024);im.verify();q['files'].append({'file':r['file'],'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(B/'source/manifest.json').write_text(json.dumps(output,ensure_ascii=False,indent=2));(B/'source/QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2))
print('18 concepts rendered; HTML bytes:',(B/'MOKO_Новые_концепты.html').stat().st_size)
