from pathlib import Path
from PIL import Image,ImageOps
import json,base64,io,zipfile,hashlib,subprocess,re
R=Path('/home/user/moko');F=R/'final';rows=json.load(open(F/'registry_final.json'));groups=json.load(open(R/'catalog/proposed_playlists.json'))
# Verify the previously approved 18 are byte-identical to the prior release.
with zipfile.ZipFile(R/'releases/release02/MOKO_Выпуск_02_18_обложек.zip') as z:
 preserved=0
 for name in z.namelist():
  if name.startswith('thumbnails/') and name.endswith('.jpg'):
   assert z.read(name)==(R/'production'/name).read_bytes(),name;preserved+=1
assert preserved==18
items=[]
for a in rows:
 p=(F/a['file']) if a['tab']=='Shorts' else (R/'production'/a['file'])
 im=Image.open(p).convert('RGB');im.thumbnail((640,840),Image.Resampling.LANCZOS);buf=io.BytesIO();im.save(buf,format='JPEG',quality=66,optimize=True)
 items.append({'n':a['number'],'id':a['id'],'title':a['title'],'headline':a['headline'],'category':a['key'],'playlist':a['playlist'],'color':a['color'],'file':a['file'],'short':a['tab']=='Shorts','approved':a['status'].startswith('Утверждено'),'status':a['status'],'note':a['review'],'source':a['visual_source'],'url':a['url'],'resolution':a['resolution'],'preview':'data:image/jpeg;base64,'+base64.b64encode(buf.getvalue()).decode()})
css='''*{box-sizing:border-box}body{margin:0;background:#080d15;color:#f4f7fb;font:15px/1.5 system-ui,sans-serif}header,main,footer{max-width:1520px;margin:auto;padding:26px}header{padding-top:37px}.k{font-size:12px;letter-spacing:2px;color:#ed6262;font-weight:700}h1{font-size:clamp(29px,4vw,45px);line-height:1.12;margin:15px 0}p{color:#a6b2c3}.intro{max-width:970px}.stats{display:flex;gap:26px;flex-wrap:wrap;margin:25px 0}.stat strong{display:block;color:white;font-size:25px}.stat span{font-size:12px;color:#91a0b4}.controls{display:flex;gap:10px;flex-wrap:wrap}input,select,button{font:inherit}input,select{color:#f4f7fb;background:#111c2d;border:1px solid #35445a;border-radius:9px;padding:12px;min-width:0}input{flex:2 1 260px}select{flex:1 1 220px}button{color:white;background:#182538;border:1px solid #35455d;border-radius:8px;padding:8px 12px;cursor:pointer}.count{font-size:13px;margin:13px 0 0}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:27px 22px}article{min-width:0}.pic{display:block;width:100%;padding:0;border:0;overflow:hidden;border-radius:9px;background:#111c2d}.pic img{width:100%;display:block;aspect-ratio:16/9;object-fit:contain}.pic.short img{aspect-ratio:9/16;max-height:490px}h2{font-size:18px;margin:12px 0 6px;line-height:1.3}.sub{font-size:12px;margin:5px 0}.badge{font-size:11px;padding:3px 7px;border:1px solid #37485e;border-radius:5px;display:inline-block;color:#b3c1d2}.actions{margin-top:12px;display:flex;gap:8px}.actions button{font-size:13px}.fine{font-size:12px}.warn{border-left:3px solid #ed6262;background:#131d2c;padding:13px 17px;font-size:13px;color:#afbdce}.rule{border-top:1px solid #253348;margin:24px 0}dialog{width:min(1320px,96vw);max-height:95vh;background:#0b1220;color:white;border:1px solid #35455d;border-radius:13px;padding:16px}dialog::backdrop{background:#000d}.dh{display:flex;align-items:start;justify-content:space-between;gap:16px;margin-bottom:12px}.dh h2{margin:0;max-width:1120px}.close{font-size:22px;padding:5px 12px}.big{width:100%;max-height:72vh;display:block;object-fit:contain;background:#080d15}.bar{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:15px}a{color:#a7c9ff}.file{font:12px ui-monospace,monospace;overflow-wrap:anywhere;color:#a5b6ca}.empty{padding:40px;color:#a8b7cb}@media(max-width:1050px){.grid{grid-template-columns:1fr 1fr}}@media(max-width:650px){header,main,footer{padding:18px}.grid{grid-template-columns:1fr;gap:29px}.stats{gap:20px}.controls{display:block}.controls input,.controls select{width:100%;margin-bottom:9px}.dh h2{font-size:16px}dialog{padding:12px}}'''
html='''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MOKO / Полный комплект</title><style>__CSS__</style><header><div class="k">MOKO / SYSTEMS · ПОЛНЫЙ КОМПЛЕКТ</div><h1>Все обложки канала</h1><p class="intro">Полный комплект для 94 доступных роликов. Первые 18 сохранены без изменений. Новые файлы можно отфильтровать и проверить по разделам. Для реальных приборов и программ использованы исходные изображения; условные иллюстрации не выданы за точные интерфейсы.</p><div class="stats"><div class="stat"><strong>92</strong><span>обычные обложки · 1280 × 720</span></div><div class="stat"><strong>2</strong><span>вертикальных макета · 1080 × 1920</span></div><div class="stat"><strong>8</strong><span>основных плейлистов</span></div><div class="stat"><strong>18 / 76</strong><span>прежние / новые макеты</span></div></div><div class="controls"><input id="search" placeholder="Поиск: название, тема или YouTube ID" aria-label="Поиск"><select id="category" aria-label="Плейлист"><option value="all">Все плейлисты</option>__OPTIONS__</select><select id="scope" aria-label="Отбор"><option value="all">Все 94 ролика</option><option value="new">Только новые · 76</option><option value="approved">Ранее согласованные · 18</option><option value="shorts">Только Shorts · 2</option></select></div><p class="count" id="count"></p><p class="fine" id="quality">В этой галерее — облегчённые превью. Полноразмерные JPG находятся в архиве.</p></header><main><div class="grid" id="grid"></div></main><footer><div class="rule"></div><div class="warn">Два вертикальных макета Shorts — отдельные кадры/дизайны, а не обычные загружаемые пользовательские миниатюры. Применение нужно проверить в текущем интерфейсе YouTube. Оригинал и перезалив стрима №3 сохранены оба; основную версию для плейлиста выбирает владелец.</div><p class="fine">Материалы классифицированы по названиям, исходным обложкам, доступным описаниям и главам; полный просмотр всех видео не выполнялся. На части архивных снимков чёткость ограничена исходником. Ничего не загружалось в YouTube Studio.</p></footer><dialog id="dlg"><div class="dh"><h2 id="dt"></h2><button class="close" onclick="document.getElementById('dlg').close()" aria-label="Закрыть">×</button></div><img class="big" id="di"><div class="bar"><a id="yt" target="_blank" rel="noopener">Открыть видео на YouTube</a><a id="download">Скачать JPG</a><button id="prev">← Предыдущее</button><button id="next">Следующее →</button></div><p class="file" id="df"></p><p class="fine" id="ds"></p><p class="fine" id="dn"></p></dialog><script>const data=__DATA__;const embedded=__EMBEDDED__;let filtered=[],current=0;const el=(tag,cls,text)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(text)e.textContent=text;return e};function render(){let q=document.getElementById('search').value.toLowerCase().trim(),cat=document.getElementById('category').value,scope=document.getElementById('scope').value;filtered=data.map((x,i)=>i).filter(i=>{let x=data[i];return(cat==='all'||x.category===cat)&&(scope==='all'||scope==='new'&&!x.approved||scope==='approved'&&x.approved||scope==='shorts'&&x.short)&&(!q||(x.title+' '+x.headline+' '+x.id).toLowerCase().includes(q))});const grid=document.getElementById('grid');grid.innerHTML='';document.getElementById('count').textContent='Показано: '+filtered.length+' из 94';filtered.forEach(i=>{let x=data[i],card=el('article'),btn=el('button','pic'+(x.short?' short':'')),img=el('img');img.src=embedded?x.preview:x.file;img.alt=x.headline;img.loading='lazy';btn.append(img);btn.onclick=()=>open(i);card.append(btn,el('h2','',String(x.n).padStart(2,'0')+' / '+x.headline));let p=el('p','sub',x.playlist);p.style.color=x.color;card.append(p,el('span','badge',x.approved?'Согласовано ранее':x.short?'Shorts · проверить применение':'Новый вариант'),el('p','sub',x.title));let acts=el('div','actions'),b=el('button','','Открыть крупно');b.onclick=()=>open(i);acts.append(b);card.append(acts);grid.append(card)});if(!filtered.length)grid.append(el('div','empty','Ничего не найдено. Попробуй другое слово или раздел.'))}function display(i){current=i;let x=data[i];document.getElementById('dt').textContent=String(x.n).padStart(2,'0')+' / '+x.title;document.getElementById('di').src=embedded?x.preview:x.file;document.getElementById('di').alt=x.headline;document.getElementById('yt').href=x.url;let dl=document.getElementById('download');dl.hidden=embedded;dl.href=x.file;dl.download=x.id+'.jpg';document.getElementById('df').textContent=x.file+' · '+x.resolution;document.getElementById('ds').textContent=x.source;document.getElementById('dn').textContent=x.note?'Перед применением: '+x.note:''}function open(i){display(i);document.getElementById('dlg').showModal()}function move(step){let pos=filtered.indexOf(current);if(filtered.length)display(filtered[(pos+step+filtered.length)%filtered.length])}document.getElementById('prev').onclick=()=>move(-1);document.getElementById('next').onclick=()=>move(1);document.getElementById('search').addEventListener('input',render);document.getElementById('category').addEventListener('change',render);document.getElementById('scope').addEventListener('change',render);document.addEventListener('keydown',e=>{if(document.getElementById('dlg').open){if(e.key==='ArrowRight')move(1);if(e.key==='ArrowLeft')move(-1)}});if(!embedded)document.getElementById('quality').textContent='В архивной версии доступны полноразмерные изображения и скачивание отдельных JPG.';render();</script></html>'''
import html as H
options=''.join(f'<option value="{k}">{H.escape(g["name"])}</option>' for k,g in groups.items())
base=html.replace('__CSS__',css).replace('__OPTIONS__',options)
main=base.replace('__DATA__',json.dumps(items,ensure_ascii=False).replace('</','<\\/')).replace('__EMBEDDED__','true')
(F/'MOKO_Все_обложки.html').write_text(main)
localitems=[{k:v for k,v in a.items() if k!='preview'} for a in items]
local=base.replace('__DATA__',json.dumps(localitems,ensure_ascii=False).replace('</','<\\/')).replace('__EMBEDDED__','false')
(F/'index.html').write_text(local)
# JavaScript syntax validation without any CDN/network requirement.
js=re.search(r'<script>(.*)</script>',main,re.S).group(1);r=subprocess.run(['node','--check'],input=js,text=True,capture_output=True);assert r.returncode==0,r.stderr
readme='''MOKO SYSTEMS — ПОЛНЫЙ КОМПЛЕКТ, 09.09.2026

92 обложки обычных видео: thumbnails/YouTube_ID.jpg, 1280×720.
2 вертикальных макета Shorts: shorts/YouTube_ID.jpg, 1080×1920.
Все файлы JPG меньше 2 МБ.

КАК СМОТРЕТЬ
Распакуйте весь архив, затем откройте index.html в браузере.
Галерея работает без интернета, с фильтрами, поиском и полноразмерными JPG.
Не перемещайте index.html отдельно от папок thumbnails/ и shorts/.

ДОКУМЕНТЫ
В docs/: итоговая карта плейлистов Word, правила Word,
реестр Excel и CSV. Файлы названы по ID; связь с исходными
названиями и YouTube-ссылками есть в реестре.

СТАТУС
Первые 18 ранее согласованных файлов сохранены без изменения байтов.
74 новые обычные обложки и 2 вертикальных макета — для финального просмотра.
Ничего не загружалось на YouTube. Названия роликов и плейлисты в аккаунте не менялись.

SHORTS
Вертикальный JPG не равен обычной пользовательской обложке Shorts.
Проверьте доступный выбор кадра в текущем интерфейсе YouTube;
для применения нового макета может понадобиться включить его в сам ролик.

ПРОВЕРКИ
На старых фотографиях чёткость ограничена исходниками.
Оборудование и реальные интерфейсы в новых файлах не перерисовывались.
Условные иллюстрации отмечены в реестре и не выдаются за точные модели/интерфейсы.
У оригинала и перезалива стрима №3 отдельные JPG; для плейлиста выберите основную версию.
Три ID, найденных только в старых плейлистах, исключены из выпуска и перечислены в документах.

Классификация: названия, обложки, описания и главы. Полный просмотр всех видео не выполнялся.
'''
(F/'README.txt').write_text(readme)
# Full-resolution images are not duplicated into the workspace: included directly from their canonical paths.
zipfile_path=F/'MOKO_Полный_комплект_94.zip'
with zipfile.ZipFile(zipfile_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for a in rows:
  p=(F/a['file']) if a['tab']=='Shorts' else (R/'production'/a['file']);z.write(p,a['file'])
 for p in (F/'docs').iterdir():z.write(p,'docs/'+p.name)
 for name in ['index.html','README.txt','registry_final.json']:z.write(F/name,name)
 z.write(R/'brand/logo.svg','brand/logo.svg')
# Verify completeness and archive integrity.
with zipfile.ZipFile(zipfile_path) as z:
 assert z.testzip() is None;assert sum(x.startswith('thumbnails/') and x.endswith('.jpg') for x in z.namelist())==92;assert sum(x.startswith('shorts/') and x.endswith('.jpg') for x in z.namelist())==2
 for a in rows:assert hashlib.sha256(z.read(a['file'])).hexdigest()==a['sha256']
(F/'QA.json').write_text(json.dumps({'videos':94,'horizontal':92,'vertical':2,'preserved_unchanged':preserved,'new':76,'jpeg_under_2mb':True,'archive_integrity':'ok','sha256_all_match':True,'javascript_syntax':'ok','whole_video_review':False,'youtube_upload':False},indent=2))
print('Gallery bytes',len(main),'ZIP bytes',zipfile_path.stat().st_size,'Preserved',preserved)
