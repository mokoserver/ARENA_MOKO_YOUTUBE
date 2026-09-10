from pathlib import Path
import numpy as np,cv2
from PIL import Image,ImageDraw,ImageFilter,ImageEnhance
R=Path('/home/user/moko');O=R/'revision7'
old=Image.open(R/'revision6/05_stream_corrected.png').convert('RGB')
src=Image.open(R/'revision3/assets/plugin_cutout.png').convert('RGBA')
# Real photograph pixels only. Geometric alignment, colour correction and alpha compositing.
source=np.float32([[202,157],[437,177],[299,54]])
destination=np.float32([[148,269],[409,270],[275,150]])
M=cv2.getAffineTransform(source,destination)
a=np.asarray(src).copy()
# Neutralize webcam colour cast. Match original forehead tone to the graded portrait.
rgb=np.asarray(ImageEnhance.Color(src.convert('RGB')).enhance(.70)).astype(float)
sample=rgb[115:142,285:340].mean(axis=(0,1))
target=np.asarray(old)[228:250,255:312].mean(axis=(0,1))
gain=np.clip(target/sample,.8,1.3)
rgb=np.clip(rgb*gain,0,255).astype('uint8')
print('Photographic colour match gains:',gain)
a[:,:,:3]=rgb
# Keep the real scalp and forehead; feather out well above the eyes.
y=np.arange(src.height)[:,None]
fade=np.clip((202-y)/36,0,1)
a[:,:,3]=(a[:,:,3].astype(float)*fade).astype('uint8')
warped=cv2.warpAffine(a,M,old.size,flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT)
# Restore original background behind the hair, removing the generated buzzcut silhouette.
ns={};exec((R/'revision2/render.py').read_text().split('# 1 Core tutorial')[0],ns)
bg=ns['base']();d=ImageDraw.Draw(bg);d.ellipse((45,199,526,680),fill='#192331')
erase=Image.new('L',old.size,0);ed=ImageDraw.Draw(erase)
ed.rounded_rectangle((126,109,436,257),radius=26,fill=255)
erase=erase.filter(ImageFilter.GaussianBlur(5))
base=Image.composite(bg,old,erase)
layer=Image.fromarray(warped,'RGBA');base.paste(layer,(0,0),layer)
# Preserve everything outside the local hair/upper-forehead area.
assert np.array_equal(np.asarray(base)[:,500:],np.asarray(old)[:,500:])
base.save(O/'05_stream_real_hair.png');base.save(O/'05_stream_real_hair.jpg',quality=97)
# A close-up comparison for visual checking.
sheet=Image.new('RGB',(1000,650),'#0b1220')
orig=src.crop((160,20,470,320));orig.thumbnail((440,550));sheet.paste(orig,(20,60),orig)
res=base.crop((115,108,445,435)).resize((500,495));sheet.paste(res,(490,60))
ImageDraw.Draw(sheet).text((30,15),'ORIGINAL PHOTO',fill='white');ImageDraw.Draw(sheet).text((500,15),'RESTORED REAL HAIR',fill='white')
sheet.save(O/'hair_check.jpg')
