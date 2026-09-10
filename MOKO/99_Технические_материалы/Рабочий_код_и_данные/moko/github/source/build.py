from pathlib import Path
import io,json,hashlib,zipfile
from PIL import Image,ImageDraw,ImageFont
import cairosvg
R=Path(__file__).resolve().parents[2];B=R/'github';B.mkdir(parents=True,exist_ok=True)
u={};exec((R/'branding/source/build.py').read_text().split('files=[]')[0],u)
mark,text,tw=u['mark'],u['text'],u['tw']
ink='#17263A';paper='#F2F0E8';red='#B93636'
def brackets(color):return f'<path d="M332 305L292 423L332 541M852 305L892 423L852 541" fill="none" stroke="{color}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>'
s='<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024"><rect width="1024" height="1024" fill="'+paper+'"/><path d="M0 0H371L154 1024H0Z" fill="'+red+'"/><path d="M371 0H405L188 1024H154Z" fill="#D4D9D7"/>'
s+=mark(584,-79,615,mono='#17263a',opacity=.045)+mark(-165,680,490,mono='#ffffff',opacity=.14)
s+='<g transform="translate(8 12)" opacity=".4">'+mark(337,235,500,mono='#B1B8B8')+brackets('#B1B8B8')+'</g>'
s+=mark(337,235,500,mono=ink)+brackets(ink)
s+='<path d="M324 771H854" stroke="'+ink+'" stroke-width="5"/><rect x="324" y="771" width="147" height="10" fill="'+red+'"/>'
total=116+24+tw('MOKO',93,'Jost',500);x=(1024-total)/2
s+=mark(x,892-116*193/271,116)+text('MOKO',x+140,892,93,ink,'Jost',500)+'</svg>'
(B/'MOKO_GitHub.svg').write_text(s)
raw=cairosvg.svg2png(bytestring=s.encode(),output_width=2048,output_height=2048)
im=Image.open(io.BytesIO(raw)).convert('RGB')
for size in [512,1024]:im.resize((size,size),Image.Resampling.LANCZOS).save(B/f'MOKO_GitHub_{size}.png',optimize=True)

def circle(n):
 a=im.convert('RGBA').resize((n,n),Image.Resampling.LANCZOS);m=Image.new('L',(n*3,n*3));ImageDraw.Draw(m).ellipse((0,0,n*3-1,n*3-1),fill=255);a.putalpha(m.resize((n,n),Image.Resampling.LANCZOS));return a
f=lambda n:ImageFont.truetype(str(R/'brand/Inter.ttf'),n)
board=Image.new('RGB',(1200,910),'#0B1220');d=ImageDraw.Draw(board)
d.text((60,38),'MOKO / GITHUB',font=f(25),fill='#A4B4C9');d.text((60,93),'Аватар организации MOKO',font=f(42),fill='#F7F9FC')
d.text((60,159),'Светлый стиль В · крупный знак · акцент на разработке',font=f(22),fill='#A4B4C9')
a=circle(420);board.paste(a,(60,237),a)
board.paste(im.resize((350,350),Image.Resampling.LANCZOS),(703,262))
d.text((270,683),'Круглая обрезка',font=f(23),fill='#F7F9FC',anchor='mt');d.text((878,646),'Квадратный файл для загрузки',font=f(19),fill='#A4B4C9',anchor='mt')
d.line((60,752,1140,752),fill='#2B3B52',width=2)
x=62
for size in [32,48,64]:
 a=circle(size);board.paste(a,(x,794+(64-size)//2),a);d.text((x+size+12,815),str(size)+' px',font=f(16),fill='#A4B4C9');x+=190
d.text((704,807),'PNG 512 / 1024 + SVG',font=f(23),fill='#F7F9FC');board.save(B/'MOKO_GitHub_Превью.jpg',quality=93,optimize=True)
(B/'README.txt').write_text('MOKO / GitHub — аватар организации\n\nMOKO_GitHub_512.png — основной файл для загрузки, 512 × 512.\nMOKO_GitHub_1024.png — версия 1024 × 1024.\nMOKO_GitHub.svg — векторный исходник, текст в контурах.\nMOKO_GitHub_Превью.jpg — пример круглой обрезки и малых размеров, не файл для установки.\n\nСветлое оформление основано на выбранном варианте В. Исходная геометрия знака MOKO сохранена; скобки кода обозначают разработку. Загрузите PNG целиком, без дополнительного приближения; проверьте обрезку в настройках аккаунта организации. В GitHub ничего не установлено.\n')
q={'purpose':'MOKO GitHub organization avatar','style':'В — Графический знак','published':False,'files':[]}
for size in [512,1024]:
 p=B/f'MOKO_GitHub_{size}.png';a=Image.open(p);assert a.size==(size,size);a.verify();assert p.stat().st_size<1024*1024
 q['files'].append({'file':p.name,'size':p.stat().st_size,'dimensions':[size,size],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
assert '<text' not in s and 'href=' not in s
with zipfile.ZipFile(B/'MOKO_GitHub_Аватар.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name in ['MOKO_GitHub_512.png','MOKO_GitHub_1024.png','MOKO_GitHub.svg','MOKO_GitHub_Превью.jpg','README.txt']:z.write(B/name,name)
with zipfile.ZipFile(B/'MOKO_GitHub_Аватар.zip') as z:assert z.testzip() is None
(B/'source/QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2))
print('GitHub avatar ready:',q['files'])
