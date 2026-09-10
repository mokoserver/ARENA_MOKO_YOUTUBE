from PIL import Image,ImageDraw,ImageFont,ImageOps
from pathlib import Path
root=Path('/home/user/moko')
def font(name,size,weight=400):
 f=ImageFont.truetype(str(root/'brand'/name),size)
 try:f.set_variation_by_axes([weight] if name=='Jost.ttf' else [14,weight])
 except Exception:pass
 return f
im=ImageOps.fit(Image.open(root/'branded/graph_art.png').convert('RGB'),(1280,720))
d=ImageDraw.Draw(im)
# Guarantee clean typography area and a uniformly dark brand header/footer.
d.rectangle((0,0,705,720),fill='#050505');d.rectangle((0,0,1280,137),fill='#050505');d.rectangle((0,620,1280,720),fill='#050505')
d.rectangle((64,64,70,88),fill='#d64545')
d.text((86,60),'MOKO SE / ОБУЧЕНИЕ',font=font('Inter.ttf',21,600),fill='#d64545')
logo=Image.open(root/'brand/logo.png').convert('RGBA')
logo.thumbnail((78,57),Image.Resampling.LANCZOS)
im.paste(logo,(920,65),logo)
d.text((1013,58),'MOKO',font=font('Jost.ttf',36,500),fill='white')
d.text((1016,103),'S Y S T E M S',font=font('Inter.ttf',11,400),fill='#a3a3a3')
d.text((60,214),'ГРАФИКИ',font=font('Jost.ttf',106,700),fill='white',stroke_width=0)
d.text((60,330),'В MOKO SE',font=font('Jost.ttf',91,700),fill='#d64545')
d.text((65,470),'Добавление и настройка',font=font('Inter.ttf',27,400),fill='#a3a3a3')
d.line((64,598,1216,598),fill='#262626',width=1)
d.rectangle((64,631,193,674),fill='#111111',outline='#383838',width=1)
mono=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',18)
d.text((79,641),'УРОК 12.1',font=mono,fill='white')
d.text((214,642),'MOKO GRAPH',font=font('Inter.ttf',18,500),fill='#a3a3a3')
im.save(root/'branded/01_graph_brand.jpg',quality=96)
# side by side comparison
sheet=Image.new('RGB',(1600,606),'#111111');sd=ImageDraw.Draw(sheet)
f=font('Inter.ttf',24,600)
sd.text((32,27),'01 / ПЕРВЫЙ КОНЦЕПТ',font=f,fill='white');sd.text((816,27),'02 / ФИРМЕННЫЙ MOKO',font=f,fill='white')
for x,p in [(32,root/'concepts/01_graph_1280x720.jpg'),(816,root/'branded/01_graph_brand.jpg')]:
 sheet.paste(ImageOps.fit(Image.open(p).convert('RGB'),(752,423)),(x,85))
sd.text((32,536),'Цветовое разделение учебных серий',font=font('Inter.ttf',19),fill='#a3a3a3')
sd.text((816,536),'Палитра сайта · Jost / Inter · строгая композиция',font=font('Inter.ttf',19),fill='#a3a3a3')
sheet.save(root/'branded/style_comparison.jpg',quality=95)
