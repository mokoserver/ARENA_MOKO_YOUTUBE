from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageFont
import numpy as np,cv2
R=Path('/home/user/moko');D=R/'revision12'
base=Image.open(R/'selected/thumbs/06_expo.jpg').convert('RGB')
a=np.asarray(Image.open(D/'expo_portrait_edit.png').convert('RGB')).copy()
# Remove a small accessory introduced by the generative treatment, absent from the request.
m=np.zeros(a.shape[:2],np.uint8);cv2.ellipse(m,(1261,456),(9,15),0,0,360,255,-1);a=cv2.inpaint(a,m,4,cv2.INPAINT_TELEA)
edit=Image.fromarray(a).resize(base.size,Image.Resampling.LANCZOS)
mask=Image.new('L',base.size,0);d=ImageDraw.Draw(mask);d.polygon([(749,145),(1279,145),(1279,719),(711,719),(711,652),(749,635)],fill=255);mask=mask.filter(ImageFilter.GaussianBlur(5))
out=Image.composite(edit,base,mask)
# Keep all approved lettering and the product mark as-is.
out.paste(base.crop((0,0,735,643)),(0,0));out.paste(base.crop((0,0,1280,115)),(0,0))
out.save(D/'06_expo_stylized.png');out.save(D/'06_expo_stylized.jpg',quality=97)
assert np.array_equal(np.asarray(out)[:643,:735],np.asarray(base)[:643,:735])
def f(n,w=500):
 q=ImageFont.truetype(str(R/'brand/Inter.ttf'),n);q.set_variation_by_axes([14,w]);return q
sheet=Image.new('RGB',(1648,609),'#080d15');s=ImageDraw.Draw(sheet)
s.text((32,25),'MOKO / SYSTEMS · ОБРАБОТКА ПОРТРЕТА',font=f(29,650),fill='white')
s.text((32,83),'БЫЛО',font=f(20,550),fill='#a3aebe');s.text((848,83),'НОВАЯ ОБРАБОТКА',font=f(20,550),fill='#ed6262')
for x,im in [(32,base),(848,out)]:sheet.paste(im.resize((768,432),Image.Resampling.LANCZOS),(x,129))
s.text((32,579),'Изменён только портрет и его окружение. Текст и обозначение продукта сохранены.',font=f(16),fill='#a3aebe')
sheet.save(D/'expo_comparison.jpg',quality=96)
