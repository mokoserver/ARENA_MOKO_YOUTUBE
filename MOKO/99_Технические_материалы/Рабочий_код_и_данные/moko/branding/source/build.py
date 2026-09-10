from pathlib import Path
import math,io,re,json
import xml.etree.ElementTree as ET
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
import cairosvg
from PIL import Image,ImageDraw,ImageFont,ImageOps
R=Path('/home/user/moko');B=R/'branding'
BG='#0b1220';WHITE='#f4f7fb';MUTED='#9eacbf';RED='#d64545'
COLORS=['#b8eb55','#ff9a48','#55d6c2','#55c9ff','#ed6262','#b69aff']
fonts={}
def getfont(kind='Inter',weight=500):
 key=(kind,weight)
 if key not in fonts:
  f=TTFont(R/'brand'/(kind+'.ttf'));axes={a.axisTag:a.defaultValue for a in f['fvar'].axes};axes['wght']=weight
  if 'opsz' in axes:axes['opsz']=14
  f=instantiateVariableFont(f,axes,inplace=False);fonts[key]=(f,f.getGlyphSet(),f.getBestCmap(),f['head'].unitsPerEm)
 return fonts[key]
def tw(txt,size,kind='Inter',weight=500,spacing=0):
 f,g,c,u=getfont(kind,weight);return sum(g[c.get(ord(ch),'space')].width for ch in txt)*size/u+max(0,len(txt)-1)*spacing
def text(txt,x,y,size=32,color=WHITE,kind='Inter',weight=500,anchor='start',spacing=0,opacity=1):
 f,g,c,u=getfont(kind,weight);scale=size/u;w=tw(txt,size,kind,weight,spacing)
 if anchor=='middle':x-=w/2
 elif anchor=='end':x-=w
 parts=[]
 for ch in txt:
  glyph=g[c.get(ord(ch),'space')];pen=SVGPathPen(g);glyph.draw(pen);path=pen.getCommands()
  if path:parts.append(f'<path d="{path}" transform="translate({x:.3f} {y:.3f}) scale({scale:.6f} {-scale:.6f})"/>')
  x+=glyph.width*scale+spacing
 return f'<g fill="{color}" opacity="{opacity}">'+''.join(parts)+'</g>'
root=ET.fromstring((R/'brand/logo.svg').read_text());LOGO=[(p.attrib['d'],p.attrib['fill']) for p in root if p.tag.endswith('path')]
def mark(x,y,w,mono=None,opacity=1):
 geometry=(f'<path d="{" ".join(d for d,c in LOGO)}" fill="{mono}"/>' if mono else ''.join(f'<path d="{d}" fill="{c}"/>' for d,c in LOGO))
 return f'<g transform="translate({x} {y}) scale({w/271})" opacity="{opacity}">'+geometry+'</g>'
def defs():
 return '''<defs><pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse"><path d="M48 0H0V48" fill="none" stroke="#23334a" stroke-width="1" opacity=".38"/></pattern><pattern id="dots" width="192" height="192" patternUnits="userSpaceOnUse"><circle cx="0" cy="0" r="2" fill="#334760" opacity=".4"/></pattern></defs>'''
def start(w,h):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'+defs()
def bg(w,h,quiet=False):
 p=f'<rect width="{w}" height="{h}" fill="{BG}"/><rect width="{w}" height="{h}" fill="url(#grid)" opacity="{.48 if quiet else .82}"/>'
 if not quiet:p+=f'<rect width="{w}" height="{h}" fill="url(#dots)"/>'
 return p

def waves(w,h):
 # Peripheral graphical details carry no essential information and may be cropped.
 s='';sy=h/2
 for i,c in enumerate(['#55c9ff','#b8eb55','#ff9a48']):
  y=sy-95+i*90
  s+=f'<path d="M-80 {y+140} C{w*.10} {y+140} {w*.12} {y-100} {w*.20} {y-90} S{w*.25} {y+45} {w*.28} {y+45}" fill="none" stroke="{c}" stroke-width="2" opacity=".17"/>'
  s+=f'<path d="M{w*.75} {y+90}H{w*.83}V{y-30}H{w+70}" fill="none" stroke="{c}" stroke-width="2" opacity=".14"/>'
  s+=f'<circle cx="{w*.83}" cy="{y-30}" r="5" fill="{c}" opacity=".27"/>'
 return s

def rail(x,y,w,h=4):
 s='';gap=10;seg=(w-gap*5)/6
 for i,c in enumerate(COLORS):s+=f'<rect x="{x+i*(seg+gap)}" y="{y}" width="{seg}" height="{h}" rx="{h/2}" fill="{c}"/>'
 return s

def wordmark(x,y,size=80,fg=WHITE):
 s='';pos=x
 for t,c in [('MOKO ',fg),('/ ',RED),('SYSTEMS',fg)]:
  s+=text(t,pos,y,size,c,'Jost',500);pos+=tw(t,size,'Jost',500)
 return s,pos-x

def lockup(cx,baseline,size=92,icon=206,gap=42,tagline=True,web=False):
 ww=tw('MOKO / SYSTEMS',size,'Jost',500);total=icon+gap+ww;x=cx-total/2
 s=mark(x,baseline-icon*193/271+9,icon)
 s+=wordmark(x+icon+gap,baseline,size)[0]
 if tagline:s+=text('Разработка · Измерения · Автоматизация',x+icon+gap,baseline+69,round(min(33,size*.38)),MUTED,'Inter',400)
 s+=rail(x+icon+gap,baseline+106,min(ww,785),4)
 if web:s+=text('moko.by',cx,baseline+176,25,MUTED,'Inter',450,anchor='middle')
 return s,(x,baseline-icon*193/271+9,x+total,baseline+112)
files=[]
def emit(rel,svg,w,h,also_jpg=False,save_svg=False):
 path=B/rel;path.parent.mkdir(parents=True,exist_ok=True)
 if save_svg:(path.with_suffix('.svg')).write_text(svg)
 cairosvg.svg2png(bytestring=svg.encode(),write_to=str(path),output_width=w,output_height=h)
 files.append({'file':str(path.relative_to(B)),'width':w,'height':h})
 if also_jpg:
  im=Image.open(path).convert('RGB');im.save(path.with_suffix('.jpg'),quality=95,optimize=True)
 return path
# Exact original symbol and transparent logo lockups, paths only: no installed fonts required.
(B/'logo/moko_symbol_original.svg').write_text((R/'brand/logo.svg').read_text())
for variant,fg,mono in [('on_dark',WHITE,None),('on_light','#162132',None),('white','#ffffff','#ffffff')]:
 size=104;icon=200;gap=36;ww=tw('MOKO / SYSTEMS',size,'Jost',500);w=math.ceil(icon+gap+ww+60);h=220
 s=start(w,h)+mark(24,31,icon,mono)
 if mono:s+=text('MOKO / SYSTEMS',24+icon+gap,147,size,fg,'Jost',500)
 else:s+=wordmark(24+icon+gap,147,size,fg)[0]
 s+='</svg>';emit('logo/moko_lockup_'+variant+'.png',s,w,h,save_svg=True)
# Stacked compact logo, transparent.
s=start(800,680)+mark(155,55,490)+text('MOKO / SYSTEMS',400,554,72,WHITE,'Jost',500,anchor='middle')+rail(176,602,448,4)+'</svg>'
emit('logo/moko_compact_on_dark.png',s,800,680,save_svg=True)
# Avatar: two useful circle-safe adaptations, not a replacement corporate symbol.
for name,with_name in [('avatar_primary',False),('avatar_with_name',True)]:
 s=start(1024,1024)+bg(1024,1024,True)
 s+='<circle cx="512" cy="512" r="436" fill="none" stroke="#263449" stroke-width="2" opacity=".7"/>'
 if with_name:s+=mark(222,180,580)+text('MOKO',512,785,118,WHITE,'Jost',500,anchor='middle')
 else:s+=mark(172,248,680)
 s+='</svg>';emit('avatars/'+name+'.png',s,1024,1024,save_svg=True)
# YouTube banner. All meaningful content inside a conservative central 1400×340 region.
s=start(2560,1440)+bg(2560,1440)+waves(2560,1440)
s+=mark(-110,60,820,mono='#162435',opacity=.18)+mark(2140,986,560,mono='#162435',opacity=.18)
lock,bounds=lockup(1280,706,92,206,42,True,False);s+=lock
s+=text('PYTHON  /  LABVIEW  /  MOKO SE',1280,870,22,MUTED,'Inter',500,anchor='middle',spacing=1.5)
s+='</svg>';emit('youtube/channel_banner.png',s,2560,1440,also_jpg=True,save_svg=True)
# Actual simplified visible crops for reviewing, never substitutes for the upload file.
im=Image.open(B/'youtube/channel_banner.png');im.crop((512,512,2048,928)).save(B/'guides/youtube_mobile_crop.png');im.crop((0,512,2560,928)).save(B/'guides/youtube_desktop_crop.png')
guide=im.convert('RGB');d=ImageDraw.Draw(guide);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',28)
d.rectangle((512,512,2048,928),outline='#b8eb55',width=4);d.rectangle((580,550,1980,890),outline='#ff9a48',width=3);d.text((530,467),'Консервативная зона обрезки · 1536 × 416',font=font,fill='#b8eb55');d.text((604,946),'Служебная схема. НЕ загружать вместо баннера.',font=font,fill='white');guide.save(B/'guides/youtube_safe_area.jpg',quality=92)
# Small transparent watermarks.
for name,mono in [('watermark_color',None),('watermark_white','#ffffff')]:
 s=start(150,150)+mark(14,30,122,mono)+'</svg>';emit('youtube/'+name+'.png',s,150,150,save_svg=True)
# VK community desktop cover.
s=start(1920,768)+bg(1920,768)+waves(1920,768);s+=lockup(960,362,77,167,34,True,False)[0];s+=text('moko.by',960,578,26,MUTED,'Inter',450,anchor='middle');s+='</svg>';emit('vk/community_cover.png',s,1920,768,also_jpg=True,save_svg=True)
# Vertical mobile/static cover and universal story composition. Critical content is in the central region.
s=start(1080,1920)+bg(1080,1920)+waves(1080,1920)
s+=mark(326,425,428)+text('MOKO / SYSTEMS',540,871,75,WHITE,'Jost',500,anchor='middle')
s+=text('Разработка · Измерения',540,969,37,MUTED,'Inter',400,anchor='middle')+text('Автоматизация',540,1030,37,MUTED,'Inter',400,anchor='middle')+rail(244,1093,592,5)+text('moko.by',540,1182,31,WHITE,'Inter',450,anchor='middle')
s+='</svg>';emit('vk/mobile_cover_static.png',s,1080,1920,also_jpg=True,save_svg=True)
# Telegram: a real post/pinned-message graphic, not a fictitious uploadable profile-header slot.
s=start(1280,720)+bg(1280,720)+waves(1280,720)
s+=text('УРОКИ · ПРОЕКТЫ · ИНЖЕНЕРНАЯ ПРАКТИКА',640,130,21,MUTED,'Inter',500,anchor='middle',spacing=1)
s+=lockup(640,343,59,133,28,True,False)[0]
s+=text('PYTHON',317,597,22,COLORS[0],'Inter',550,anchor='middle')+text('LABVIEW',640,597,22,COLORS[1],'Inter',550,anchor='middle')+text('MOKO SE',963,597,22,COLORS[2],'Inter',550,anchor='middle')
s+='</svg>';emit('telegram/pinned_post_banner.png',s,1280,720,also_jpg=True,save_svg=True)
# Quiet wallpaper: actual availability in Telegram depends on channel appearance settings.
s=start(1080,1920)+bg(1080,1920,True);s+=mark(-160,190,650,mono='#243146',opacity=.2)+mark(668,1400,550,mono='#243146',opacity=.2);s+='</svg>';emit('telegram/channel_wallpaper_optional.png',s,1080,1920,also_jpg=True,save_svg=True)
# Small navigation tiles, no fake links; the owner assigns destinations in VK.
menu=[('01_python','PYTHON','#b8eb55','code'),('02_labview','LABVIEW','#ff9a48','nodes'),('03_mokose','MOKO SE','#55d6c2','logo'),('04_testing','ИСПЫТАНИЯ','#55c9ff','graph'),('05_projects','ПРОЕКТЫ','#55c9ff','nodes'),('06_development','РАЗРАБОТКА','#ff9a48','code'),('07_company','О КОМПАНИИ','#ed6262','logo'),('08_media','МЕДИА','#b69aff','play')]
for name,label,c,icon in menu:
 s=start(376,256)+bg(376,256,True)+f'<rect x="30" y="220" width="316" height="3" fill="{c}"/>'
 if icon=='logo':s+=mark(145,32,86)
 elif icon=='code':s+=text('</>',188,117,66,c,'Inter',500,anchor='middle')
 elif icon=='play':s+=f'<rect x="137" y="46" width="103" height="80" rx="12" fill="none" stroke="{c}" stroke-width="3"/><path d="M178 63L208 86L178 109Z" fill="{c}"/>'
 elif icon=='graph':s+=f'<path d="M125 132V43M125 132H258M136 113L160 98L178 107L198 71L221 89L249 55" fill="none" stroke="{c}" stroke-width="3"/>'
 else:s+=f'<path d="M188 63V87H133V113M188 87H243V113" stroke="{c}" stroke-width="3" fill="none"/><rect x="171" y="33" width="34" height="32" rx="4" fill="{c}"/><rect x="116" y="111" width="34" height="30" rx="4" fill="{c}"/><rect x="226" y="111" width="34" height="30" rx="4" fill="{c}"/>'
 s+=text(label,188,188,27,c,'Inter',600,anchor='middle')+'</svg>';emit('vk/menu/'+name+'.png',s,376,256,save_svg=True)
# End-screen background: the native video/subscription elements are added separately in YouTube Studio.
s=start(1920,1080)+bg(1920,1080)+waves(1920,1080)
s+=mark(78,59,64)+wordmark(163,102,35)[0]
s+=text('СМОТРИТЕ ДАЛЬШЕ',100,250,65,WHITE,'Jost',650)
s+='<circle cx="275" cy="589" r="124" fill="#111d2e" stroke="#314158" stroke-width="2"/>'
s+='<rect x="543" y="410" width="588" height="331" rx="12" fill="#111d2e" stroke="#314158" stroke-width="2"/><rect x="1210" y="410" width="588" height="331" rx="12" fill="#111d2e" stroke="#314158" stroke-width="2"/>'
s+=text('ПОДПИСАТЬСЯ',275,812,25,MUTED,'Inter',550,anchor='middle')+text('СЛЕДУЮЩЕЕ ВИДЕО',837,812,25,MUTED,'Inter',550,anchor='middle')+text('ЕЩЁ ПО ТЕМЕ',1504,812,25,MUTED,'Inter',550,anchor='middle')+rail(100,945,1700,4)
s+='</svg>';emit('youtube/end_screen_background.png',s,1920,1080,also_jpg=True,save_svg=True)
# Three still scenes for the channel's existing stream format.
for name,h1,h2 in [('stream_start','ЭФИР СКОРО','НАЧНЁТСЯ'),('stream_pause','СКОРО','ВЕРНЁМСЯ'),('stream_end','СПАСИБО','ЗА ПРОСМОТР')]:
 s=start(1920,1080)+bg(1920,1080)+waves(1920,1080);s+=mark(108,88,85)+wordmark(220,150,46)[0]
 s+=text(h1,960,465,94,WHITE,'Jost',650,anchor='middle')+text(h2,960,594,94,RED,'Jost',650,anchor='middle');s+=rail(645,686,630,5)+text('MOKO / SYSTEMS',960,810,29,MUTED,'Inter',450,anchor='middle')
 s+='</svg>';emit('streams/'+name+'.png',s,1920,1080,also_jpg=True,save_svg=True)
(B/'source/manifest.json').write_text(json.dumps({'files':files,'youtube_essential_bounds':bounds,'palette':COLORS},ensure_ascii=False,indent=2))
print('PNG deliverables',len(files),'YT essential bounds',bounds)
