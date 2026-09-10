from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np
R=Path('/home/user/moko');O=R/'revision4'
# Recreate the approved composition without its old screenshot frame.
exec((R/'revision3/render.py').read_text().split('# Actual source screenshot')[0])
# Shadow is outside the screenshot. The screenshot itself stays pixel-for-pixel intact in the PNG master.
shadow=Image.new('RGBA',im.size,(0,0,0,0));sh=ImageDraw.Draw(shadow)
sh.rounded_rectangle((555,366,1241,719),radius=20,fill=(0,0,0,165))
shadow=shadow.filter(ImageFilter.GaussianBlur(12));im=Image.alpha_composite(im.convert('RGBA'),shadow).convert('RGB');d=ImageDraw.Draw(im)
# Layered matte frame, distinct decorative title strip and controlled rubric accent.
d.rounded_rectangle((552,357,1233,710),radius=17,fill='#101925',outline='#4e5b6b',width=2)
d.rounded_rectangle((556,361,1229,706),radius=14,fill='#182332')
d.rounded_rectangle((560,362,1225,396),radius=10,fill='#253244')
d.rectangle((560,386,1225,396),fill='#253244')
d.line((567,362,1218,362),fill='#ff9a48',width=3)
d.rounded_rectangle((576,372,594,386),radius=3,outline='#ff9a48',width=2)
d.line((581,390,589,390),fill='#ff9a48',width=2)
d.text((606,370),'MOKO ExPlugin',font=f(18,550,True),fill='#e9eef6')
for x in [1165,1183,1201]:d.ellipse((x,376,x+5,381),fill='#6c7a8e')
# Recessed surround: no altered UI, fake controls or perspective applied to the source screenshot.
d.rectangle((586,399,1189,694),fill='#080e17',outline='#4f5d6e',width=1)
screen=Image.open(R/'revision3/assets/plugin_screenshot.png').convert('RGB')
assert screen.size==(598,290)
im.paste(screen,(589,402))
pill(im,'● СТРИМ 4.1',48,646,ORANGE)
d.text((564,333),'СКОРОСТНОЙ СБОР ДАННЫХ',font=f(19,600,True),fill='#c6ceda')
brand(im)
im.save(O/'05_stream_framed.png')
im.save(O/'05_stream_framed.jpg',quality=97)
assert np.array_equal(np.asarray(im.crop((589,402,1187,692))),np.asarray(screen))
# Comparison kept separate from the usable thumbnail.
sheet=Image.new('RGB',(1648,609),'#080d15');s=ImageDraw.Draw(sheet)
s.text((32,25),'MOKO / SYSTEMS · ОФОРМЛЕНИЕ ИНТЕРФЕЙСА',font=f(29,600),fill=WHITE)
s.text((32,83),'БЫЛО',font=f(20,550,True),fill='#a3aebe');s.text((848,83),'НОВАЯ РАМКА · ТОТ ЖЕ СКРИНШОТ',font=f(20,550,True),fill=ORANGE)
for x,p in [(32,R/'revision3/thumbs/05_stream.jpg'),(848,O/'05_stream_framed.png')]:
 a=Image.open(p).convert('RGB').resize((768,432),Image.Resampling.LANCZOS);sheet.paste(a,(x,129))
s.text((32,579),'Интерфейс не перерисован. Изменено только внешнее оформление.',font=f(17,450,True),fill='#a3aebe')
sheet.save(O/'frame_comparison.jpg',quality=96)
print('PNG screenshot verified: exact original crop, no resampling or pixel edits.')
