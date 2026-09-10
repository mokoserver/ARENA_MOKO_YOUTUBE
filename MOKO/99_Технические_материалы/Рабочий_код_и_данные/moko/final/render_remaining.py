from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageFilter,ImageEnhance
import json,math,colorsys,numpy as np,cv2
R=Path('/home/user/moko');F=R/'final';P=R/'production/thumbnails';(F/'shorts').mkdir(parents=True,exist_ok=True)
exec((R/'revision2/render.py').read_text().split('# 1 Core tutorial')[0])
V=json.load(open(R/'catalog/registry.json'));by={a['number']:a for a in V};desc={a['id']:a for a in json.load(open(R/'catalog/descriptions_all.json'))}
A={
'graph':R/'revision2/assets/graph.png','driver':R/'revision2/assets/driver.png','telegram':R/'revision2/assets/telegram.png',
'report':R/'batch02/assets/report.png','tree':R/'batch02/assets/tree.png','json':R/'batch02/assets/json.png',
'run':R/'batch03/assets/run.png','dialog':R/'batch03/assets/dialog.png','exchange':R/'batch03/assets/exchange.png','project':R/'batch03/assets/project.png','folders':R/'batch03/assets/folders.png',
'clicker':F/'assets/clicker.jpg','module':F/'assets/module_tools.jpg','media':F/'assets/media.jpg','cloud':F/'assets/cloud.jpg','server':F/'assets/server.jpg'}
# Every new video gets an explicit brief: headline, topic detail, semantic image/source, badge and layout.
# Modes: a=concept art; v=concept schematic; s=unaltered real screenshot/photo in frame; d=two real source panels; b=brand.
C={
2:('ТЕСТ','ИСТОЧНИКА ПИТАНИЯ','Автоматизация с Олегом Германом','s',2,(.59,.04,.96,.84),'СТРИМ 3','R'),
3:('АВТОМАТИЗАЦИЯ','ИЗМЕРЕНИЙ','С Олегом Германом · удалённые испытания','s',3,(.772,.30,.993,.75),'СТРИМ 2','R'),
4:('РАЗГОВОР','О MOKO SE','Иван Анищенко и Олег Герман','s',4,(.08,.24,.89,.75),'СТРИМ / ИНТЕРВЬЮ','W'),
5:('ЗАПИСЬ','В ТАБЛИЦУ','LabVIEW · панель подключения к приборам','s',5,(.049,.452,.478,.894),'СТРИМ 4.2','R'),
7:('ОБНОВЛЕНИЕ','MOKO SE','Автообновление и время выполнения','v','update',None,'СТРИМ 3 / ПЕРЕЗАЛИВ','R'),
8:('ОБНОВЛЕНИЕ','MOKO SE','Автообновление и время выполнения','v','update',None,'СТРИМ 3','R'),
10:('ИНИЦИАЛИЗАЦИЯ','ДРАЙВЕРОВ','ReInit и обработка ошибок','v','settings',None,'СТРИМ 2','L'),
11:('ТЕСТИРУЕМ','IoT-УСТРОЙСТВА','Приборы, графики, протокол испытаний','s',11,(.465,.36,.873,.765),'ДЕМОНСТРАЦИЯ','R'),
12:('ДРАЙВЕР','И СКРИПТ','Начинаем измерения · Rohde & Schwarz','a','exchange',None,'СТРИМ 1','R'),
13:('AUTOIT','+ MOKO SE','Управление сторонними приложениями','v','windows',None,'АНОНС ФУНКЦИИ','R'),
14:('РЕЗКА','МЕТАЛЛА','Новый станок XT-H1530','s',14,(.415,.365,.99,.755),'ПРОИЗВОДСТВО','R'),
15:('ПОВЕРКА','МУЛЬТИМЕТРА','Fluke 5520A + Keysight 34460A','d',15,[(.085,.73,.45,.96),(.555,.71,.915,.96)],'ДЕМОПРОЕКТ','R'),
17:('ПОДКЛЮЧАЕМ','УТИЛИТУ','Тестирование из MOKO SE','a','module',None,'УРОК 2.2','L'),
18:('СОЗДАЁМ','УТИЛИТУ','Разработка и компиляция DLL','a','module',None,'УРОК 2.1','R'),
21:('СРЕДА','РАЗРАБОТКИ','LabVIEW 2018 · VIPM · библиотеки','v','library',None,'УРОК 0','R'),
22:('СНИМКИ','ЭКРАНА','MOKO Clicker · Screenshot и PNG','v','capture',None,'УРОК 13.2','L'),
23:('УПРАВЛЕНИЕ','МЫШЬЮ','MOKO Clicker · клики и курсор','a','clicker',None,'УРОК 13.1','R'),
24:('НАСТРОЙКА','ГРАФИКОВ','Масштаб, легенда и снимок графика','v','graph_legend',None,'УРОК 12.3','L'),
25:('УПРАВЛЕНИЕ','ЛИНИЯМИ','Показать, скрыть, удалить','v','graph_lines',None,'УРОК 12.2','R'),
27:('ФОРМИРУЕМ','ПРОТОКОЛ','Скрипт и шаблон Microsoft Word','a','report',None,'УРОК 11.3','R'),
28:('СКРИПТЫ','ИСПЫТАНИЙ','Дерево, таблица и ход испытаний','a','run',None,'УРОК 11.2','L'),
29:('РЕГИСТРАЦИЯ','ОБРАЗЦА','Утилита, дерево и Report','v','form',None,'УРОК 11.1','R'),
31:('УПРАВЛЯЕМ','ИЗ СКРИПТА','Функция Program в MOKO SE','a','project',None,'УРОК 9 / PROGRAM','R'),
32:('ФОРМА','ВВОДА ДАННЫХ','Функция Utility · set и get','a','dialog',None,'УРОК 8 / UTILITY','L'),
33:('РАБОТА','С ПЛАГИНАМИ','Инициализация, данные, график','a','module',None,'УРОК 7 / PLUGIN','R'),
42:('КОНТРОЛЛЕРЫ','И ТЕЛЕМЕТРИЯ','Управление, измерения, моноблоки','s',42,(.594,.235,.949,.915),'ОБЗОР СИСТЕМ','R'),
43:('ФАЙЛЫ','И ПРОГРАММА','Ассоциации файлов в Inno Setup','v','filelink',None,'РАЗРАБОТКА / WINDOWS','L'),
44:('JOHNNY','RESPECT','Проморолик','s',44,(.612,.115,.845,.455),'МЕДИА / ПРОМО','R'),
45:('MOKO SE','АВТОМАТИЗАЦИЯ','Знакомство с платформой','b','logo',None,'ПРЕЗЕНТАЦИЯ','R'),
46:('MOKO SE','В ДЕЙСТВИИ','Платформа для автоматизации','a','graph',None,'ПРОМО / MOKO SE','L'),
47:('TELEGRAM','В MOKO SE','Подключение и использование бота','a','telegram',None,'ИНТЕГРАЦИЯ','R'),
48:('ИЗОБРАЖЕНИЯ','В ОТЧЁТАХ','Message и Report','v','image_report',None,'MOKO SE / ВОЗМОЖНОСТИ','L'),
49:('СЕНСОРНЫЕ','МОНОБЛОКИ','Обзор оборудования Тесла','s',49,(.448,.10,.945,.94),'ОБЗОР ОБОРУДОВАНИЯ','R'),
50:('ЗНАКОМСТВО','С MOKO SE','Установка и первый запуск','a','run',None,'ПОЛНАЯ ПРЕЗЕНТАЦИЯ','R'),
51:('УНИКАЛЬНАЯ','КНОПКА','Рисуем собственный элемент интерфейса','s',51,(.438,.045,.968,.87),'LABVIEW / ИНТЕРФЕЙС','R'),
52:('КАТАЛОГ','ПРОДУКЦИИ','Совместно с Johnny Respect','s',52,(.447,.09,.941,.59),'МЕДИА / ПРОЦЕСС','L'),
53:('СОЗДАЁМ','PDF-ОТЧЁТЫ','Документы в MOKO SE','v','pdf',None,'MOKO SE / ОТЧЁТЫ','R'),
54:('ЗАПУСК','СКРИПТОВ','Окно Edit Execution','s',54,(.435,.09,.952,.92),'MOKO SE / ИНСТРУКЦИЯ','L'),
55:('КОНТРОЛЛЕР','ATLANT','Управление и мобильное приложение','s',55,(.439,.098,.945,.905),'ЭЛЕКТРОНИКА','R'),
56:('БЕЛЭНЕРГОКИП','ПРОМОРОЛИК','Медиапроект MOKO','s',56,(.44,.03,.978,.948),'МЕДИА / ПОРТФОЛИО','R'),
57:('МОДЕРНИЗАЦИЯ','УПАКОВКИ','Аппарат после доработки MOKO','s',57,(.444,.155,.936,.822),'ИНЖЕНЕРНЫЙ ПРОЕКТ','L'),
58:('MOKO GRAPH','ПРЕЗЕНТАЦИЯ','Графики измерений и отчёт Word','s',58,(.428,.044,.962,.913),'ПЛАГИН / MOKO SE','R'),
59:('СПЕЦСИМВОЛЫ','В MOKO SE','Вставка символов в текст','v','symbols',None,'MOKO SE / ИНСТРУКЦИЯ','R'),
60:('МЕДИАУСЛУГИ','MOKO','Проморолики и видеопроизводство','a','media',None,'МЕДИА / КОМПАНИЯ','L'),
61:('ИНЖЕНЕРИЯ','MOKO','Электроника и программное обеспечение','b','logo',None,'О КОМПАНИИ','R'),
62:('MOKO SE','ВЕРСИЯ 2','Новый интерфейс и возможности','v','version',None,'АНОНС / АРХИВ','L'),
63:('MONITOR','BALL','MALANKA · English version','s',64,(.245,.04,.73,.96),'ENGLISH VERSION','R'),
64:('MONITOR','BALL','MALANKA · инженерный проект','s',64,(.245,.04,.73,.96),'РУССКАЯ ВЕРСИЯ','L'),
65:('СВОИ','КНОПКИ','Из картинки в элемент LabVIEW','v','buttons',None,'LABVIEW / ИНТЕРФЕЙС','L'),
66:('ОБЪЕДИНЯЕМ','ОТЧЁТЫ','На примере поверки манометров','v','merge',None,'MOKO SE / ПОВЕРКА','R'),
67:('ПОДАРОК','ОТ SOFTEQ LAB','Партнёры MOKO','s',67,(.445,.028,.94,.973),'КОМПАНИЯ / ПАРТНЁРЫ','L'),
68:('ИКОНКА','ДЛЯ ПРОГРАММЫ','Создание файла ICO','v','icon',None,'ИНСТРУМЕНТЫ','R'),
69:('НАСТРОЙКА','МОДЕМА','Новый параметр в MOKO Modem','s',69,(.437,.11,.949,.884),'C# / .NET','R'),
71:('СЕРВЕР','НЕ СТАРТУЕТ','Диагностика запуска · C# / .NET','a','server',None,'РАЗБОР ОШИБКИ','L'),
72:('ПЛАГИНЫ','НА C#','Управление из MOKO SE','s',72,(.434,.126,.952,.913),'C# / .NET','R'),
73:('НЕСКОЛЬКО','GOOGLE ДИСКОВ','Разные аккаунты в Windows 10','a','cloud',None,'WINDOWS 10 / АРХИВ','R'),
74:('РАЗМЕР','ИЗОБРАЖЕНИЯ','Изменяем разрешение в MOKO SE','v','resize',None,'MOKO SE / ИНСТРУКЦИЯ','L'),
75:('ТАБЛИЦЫ','В ОТЧЁТЕ','Report TABLE · разделитель «;»','s',75,(.422,.073,.956,.916),'MOKO SE / REPORT','R'),
76:('ФОРМАТЫ','ИЗОБРАЖЕНИЙ','Загрузка картинок в MOKO SE','v','formats',None,'MOKO SE / ИНСТРУКЦИЯ','R'),
77:('PRESET','УСТРОЙСТВА','Настройка устройства в плагине','s',77,(.427,.054,.956,.908),'LABVIEW / ЧАСТЬ 2','L'),
78:('PRESET','УСТРОЙСТВА','Настройка устройства в плагине','s',78,(.427,.054,.956,.908),'LABVIEW / ЧАСТЬ 1','R'),
80:('СОЗДАЁМ','ПЛАГИН','На базе MOKO ExPlugin','s',80,(.427,.054,.956,.908),'LABVIEW / РАЗРАБОТКА','R'),
81:('НАСТРОЙКА','ИНТЕРФЕЙСА','Вид программы в LabVIEW','s',81,(.427,.054,.956,.908),'LABVIEW / ИНТЕРФЕЙС','L'),
82:('ДЕРЕВО','В MOKO SE','Возможности и работа с деревом','s',82,(.427,.054,.956,.908),'MOKO SE / ИНСТРУКЦИЯ','R'),
83:('ПОВЕРКА','СИСТЕМ НАЛИВА','Передвижная установка партнёров','s',83,(.444,.178,.944,.77),'РЕШЕНИЕ / MOKO','R'),
84:('ЛАБОРАТОРИЯ','ПОД КЛЮЧ','Модульный подход к автоматизации','s',84,(.44,.157,.945,.773),'ЛЕКЦИЯ','L'),
85:('MOKO','НА KEYSIGHT','Интервью · Москва, 2020','s',85,(.50,.089,.905,.9),'КОНФЕРЕНЦИЯ / ИНТЕРВЬЮ','R'),
86:('КУиТ-862','ТЕЛЕМЕТРИЯ','STM32F7 и мобильное приложение','s',86,(.44,.05,.958,.9),'КОНТРОЛЛЕРЫ MOKO','R'),
87:('СПЕЦИАЛЬНАЯ','ЭЛЕКТРОНИКА','Разработка и производство MOKO','s',87,(.443,.059,.94,.827),'ИНЖЕНЕРНЫЕ РЕШЕНИЯ','L'),
88:('ДАТЧИК','И ТЕЛЕМЕТРИЯ','Передача на 2API.by · packbel.by','s',88,(.444,.109,.952,.905),'WI-FI / ESP8266','R'),
89:('ПОВОРОТНАЯ','ВИДЕОСИСТЕМА','Устройство с навесной конструкцией','s',89,(.443,.116,.94,.817),'ПРОЕКТ MOKO','L'),
90:('СТЕНД','ВОДОПОДГОТОВКИ','Проект для БелГИСС','s',90,(.44,.114,.948,.836),'АВТОМАТИЗАЦИЯ','R'),
91:('ИСПЫТАНИЯ','СТИРАЛЬНЫХ МАШИН','Испытательный стенд в БелГИСС','s',91,(.446,.14,.944,.841),'ЛАБОРАТОРНЫЙ СТЕНД','L'),
92:('ПРОТОТИП','STM32F769','Инженерный проект MOKO','s',92,(.459,.23,.948,.754),'ВСТРАИВАЕМЫЕ СИСТЕМЫ','R')}

def rgb(h):return tuple(int(h.strip('#')[i:i+2],16) for i in (0,2,4))
def crop_source(n,box):
 a=by[n];im=Image.open(R/'originals'/(a['id']+'.jpg')).convert('RGB');w,h=im.size
 im=im.crop(tuple(round(v*(w if i%2==0 else h)) for i,v in enumerate(box)))
 # Trim remnants of the old coral template, without touching the real image content.
 a=np.asarray(im);red=(a[:,:,0]>165)&(a[:,:,0]-a[:,:,1].astype(float)>40)&(a[:,:,1]>55)&(a[:,:,1]<170)
 top=0;bottom=im.height;left=0;right=im.width
 while top<min(45,im.height//5) and red[top].mean()>.52:top+=1
 while bottom>im.height-min(45,im.height//5) and red[bottom-1].mean()>.52:bottom-=1
 while left<min(24,im.width//8) and red[top:bottom,left].mean()>.52:left+=1
 while right>im.width-min(24,im.width//8) and red[top:bottom,right-1].mean()>.52:right-=1
 im=im.crop((left,top,right,bottom))
 if n==14:
  arr=np.asarray(im).astype(float)/255;im=Image.fromarray(np.uint8(np.clip(arr**.57*255,0,255)));im=ImageEnhance.Contrast(im).enhance(1.12)
 return im
def subfit(im,t,x,y,maxw,size=27):
 d=ImageDraw.Draw(im)
 while d.textlength(t,font=f(size,450,True))>maxw:size-=1
 assert size>=16,(t,size)
 d.text((x,y),t,font=f(size,450,True),fill='#c6ceda')
 return size

def recolored_asset(name,color):
 im=Image.open(A[name]).convert('RGB');arr=np.asarray(im);hsv=cv2.cvtColor(arr,cv2.COLOR_RGB2HSV)
 # Recolour only the illustration's category accent, never real photographs/screenshots.
 sourceorange=name in ['driver','json','module','cloud','server'];lo,hi=(5,28) if sourceorange else (28,65)
 if name=='media':lo,hi=115,155
 target=cv2.cvtColor(np.uint8([[rgb(color)]]),cv2.COLOR_RGB2HSV)[0,0]
 mask=(hsv[:,:,0]>=lo)&(hsv[:,:,0]<=hi)&(hsv[:,:,1]>55)&(hsv[:,:,2]>65)
 hsv[:,:,0][mask]=target[0];hsv[:,:,1][mask]=np.minimum(hsv[:,:,1][mask].astype(float)*.75+target[1]*.25,255).astype(np.uint8)
 return Image.fromarray(cv2.cvtColor(hsv,cv2.COLOR_HSV2RGB))

def place_art(im,artim,box):
 x,y,w,h=box;artim=ImageOps.fit(artim,(w,h));mask=Image.new('L',(w,h),255);d=ImageDraw.Draw(mask)
 for k in range(42):d.rectangle((k,k,w-1-k,h-1-k),outline=round(k*255/42))
 im.paste(artim,(x,y),mask)

def schematic(kind,color):
 a=Image.new('RGB',(600,600),BG);d=ImageDraw.Draw(a);accent=rgb(color);dark=tuple(int(x*.21) for x in accent)
 d.ellipse((57,44,562,551),fill=dark)
 def panel(box=(76,91,533,511)):
  d.rounded_rectangle(box,radius=20,fill='#172332',outline='#48576a',width=2)
 def txt(t,xy,size=34,col=WHITE):d.text(xy,t,font=f(size,600,True),fill=col)
 def arrow(x,y,xe,ye,col=color):
  d.line((x,y,xe,ye),fill=col,width=7);ang=math.atan2(ye-y,xe-x);p=[(xe,ye),(xe-22*math.cos(ang-.55),ye-22*math.sin(ang-.55)),(xe-22*math.cos(ang+.55),ye-22*math.sin(ang+.55))];d.polygon(p,fill=col)
 if kind in ['graph_legend','graph_lines','capture']:
  panel();d.line((117,423,488,423),fill='#7e8b9b',width=2);d.line((117,187,117,423),fill='#7e8b9b',width=2)
  for j,c in enumerate([color,'#dde5ee','#7b8b9b']):
   pts=[(120+i*3.5,330-58*math.sin(i/14+j*.8)-j*14) for i in range(103)];d.line(pts,fill=c,width=5 if j==0 else 3)
  if kind=='graph_lines':
   for y,t,c in [(126,'ShowLine',color),(455,'HideLine','#a8b4c5')]:txt(t,(158,y),27,c)
  elif kind=='graph_legend':
   txt('Autoscale',(151,125),30,color)
   for j in range(3):d.line((162+j*110,460,184+j*110,460),fill=[color,'#dde5ee','#7b8b9b'][j],width=4)
  else:
   for x,y,sx,sy in [(57,74,1,1),(550,74,-1,1),(57,528,1,-1),(550,528,-1,-1)]:d.line((x+sx*40,y,x,y,x,y+sy*40),fill=color,width=9)
   txt('Screenshot',(160,125),29,color)
 elif kind in ['form','settings','buttons','windows']:
  panel();txt({'form':'Utility','settings':'ReInit','buttons':'LabVIEW','windows':'AutoIt'}[kind],(116,122),34,color)
  if kind=='buttons':
   for i in range(3):d.rounded_rectangle((130,206+i*81,477,263+i*81),radius=[8,23,5][i],fill=[color,'#334357','#273344'][i],outline=color,width=2)
   d.polygon([(285,215),(285,254),(318,234)],fill=BG)
  else:
   for i in range(3):
    d.rounded_rectangle((118,207+i*77,488,259+i*77),radius=6,fill='#263548');d.line((140,229+i*77,295,229+i*77),fill='#a5b5c7',width=4)
    if kind=='settings':d.ellipse((356+i*14,221+i*77,380+i*14,245+i*77),fill=color)
   if kind=='windows':arrow(483,314,555,314)
 elif kind in ['pdf','merge','image_report','formats','resize','filelink','icon']:
  if kind=='merge':
   for i in range(2):d.rounded_rectangle((65+i*32,111-i*30,290+i*32,441-i*30),radius=10,fill='#ccd6df',outline='#637586',width=2)
   arrow(267,467,420,467);d.rounded_rectangle((335,230,538,520),radius=12,fill='#f4f6f9');txt('Report',(355,269),27,'#273446')
  elif kind=='formats':
   for i,t in enumerate(['BMP','JPG','PNG']):
    x=56+i*163;y=135+i*37;d.rounded_rectangle((x,y,x+144,y+246),radius=11,fill='#e6ecf2');d.rectangle((x+8,y+60,x+136,y+113),fill=color);txt(t,(x+25,y+72),30,BG)
  elif kind=='icon':
   d.rounded_rectangle((141,125,468,452),radius=50,fill=color);d.rounded_rectangle((173,157,436,420),radius=37,outline='#eff5ff',width=5);txt('ICO',(200,244),73,BG)
  elif kind=='filelink':
   d.rounded_rectangle((80,115,266,407),radius=12,fill='#e6ecf2');txt('FILE',(118,207),36,BG);d.rounded_rectangle((347,221,551,452),radius=15,fill='#223247',outline=color,width=3);txt('APP',(396,302),36,color);arrow(204,476,440,476)
  else:
   d.rounded_rectangle((141,74,467,524),radius=16,fill='#e6ecf2')
   if kind=='pdf':d.rectangle((141,158,467,257),fill=color);txt('PDF',(211,174),64,BG)
   else:
    d.rounded_rectangle((179,141,431,319),radius=8,fill='#34495b');d.polygon([(193,297),(260,191),(324,278),(356,231),(418,297)],fill=color);d.ellipse((361,165,392,196),fill='#e6ecf2')
   for i in range(3):d.line((181,360+i*40,424,360+i*40),fill='#8d9ead',width=6)
   if kind=='resize':arrow(88,85,88,512);arrow(490,540,145,540)
 elif kind=='symbols':
  panel();ft=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',100)
  for t,xy in [('Ω',(112,180)),('Δ',(326,180)),('±',(113,335)),('µ',(326,335))]:d.text(xy,t,font=ft,fill=color)
 elif kind=='version':
  panel();txt('MOKO SE',(142,138),43,WHITE);txt('2.0',(148,228),136,color);txt('UI / UPDATE',(158,438),27,'#a8b4c5')
 elif kind in ['update','library']:
  panel();txt('MOKO SE' if kind=='update' else 'LabVIEW',(133,131),39,WHITE)
  if kind=='update':
   d.arc((179,215,435,465),30,324,fill=color,width=19);d.polygon([(416,236),(451,249),(425,279)],fill=color);d.line((298,276,298,356),fill=WHITE,width=10);d.polygon([(272,337),(325,337),(298,370)],fill=WHITE)
  else:
   for i,t in enumerate(['2018','VIPM','JSON / OpenG']):txt(t,(135,230+i*80),35 if i<2 else 28,color if i==0 else WHITE)
 else:raise ValueError(kind)
 return a

def sourceframe(im,sources,box,header,color,photo=False):
 x,y,w,h=box
 if len(sources)==1 and sources[0].width/sources[0].height>1.15:
  desired=max(226,min(h,round((w-28)*sources[0].height/sources[0].width)+66));y+=round((h-desired)/2);h=desired
 d=ImageDraw.Draw(im)
 shadow=Image.new('RGBA',im.size,(0,0,0,0));sd=ImageDraw.Draw(shadow);sd.rounded_rectangle((x+6,y+7,x+w+8,y+h+8),radius=18,fill=(0,0,0,125));shadow=shadow.filter(ImageFilter.GaussianBlur(7));im.paste(shadow,(0,0),shadow)
 d=ImageDraw.Draw(im);d.rounded_rectangle((x,y,x+w,y+h),radius=16,fill='#172332',outline='#455468',width=2);d.rounded_rectangle((x+7,y+7,x+w-7,y+40),radius=8,fill='#253244');d.line((x+15,y+7,x+w-15,y+7),fill=color,width=3)
 subfit(im,header,x+21,y+14,w-42,17)
 pad=14;availw=w-2*pad;availh=h-58
 for i,src in enumerate(sources):
  sh=round(availh/len(sources))-8;scaled=ImageOps.contain(src,(availw,sh),Image.Resampling.LANCZOS);px=x+pad+(availw-scaled.width)//2;py=y+49+i*(sh+8)+(sh-scaled.height)//2;im.paste(scaled,(px,py))

def drawbrand_art(color):
 im=Image.new('RGB',(600,600),BG);d=ImageDraw.Draw(im);ac=rgb(color);d.ellipse((42,41,559,558),fill=tuple(int(x*.16) for x in ac));logo=Image.open(R/'brand/logo.png').convert('RGBA');logo=ImageOps.contain(logo,(415,297),Image.Resampling.LANCZOS);im.paste(logo,((600-logo.width)//2,113),logo);d.text((143,424),'MOKO',font=f(75,500),fill=WHITE);return im

new=[]
for n,c in C.items():
 row=by[n];out=P/(row['id']+'.jpg');assert not row.get('file'),('would overwrite approved/prepared',n)
 h1,h2,subtitle,mode,content,crop,badge,layout=c;color=row['color'];tagtext={'PY':'PYTHON / MOKO SE','LV':'LABVIEW / РАЗРАБОТКА','SE':'MOKO SE / ИНСТРУКЦИИ','DEV':'РАЗРАБОТКА','TEST':'ПРАКТИКА / ИСПЫТАНИЯ','HW':'ПРАКТИКА / ЭЛЕКТРОНИКА','CO':'MOKO / СОБЫТИЯ','MEDIA':'MOKO / МЕДИА'}[row['key']]
 if n==5:tagtext='LABVIEW / РАЗРАБОТКА'
 if n in [69,71]:tagtext='C# / .NET / РАЗРАБОТКА'
 im=base();tag(im,tagtext,color)
 if mode=='a':visual=recolored_asset(content,color)
 elif mode=='v':visual=schematic(content,color)
 elif mode=='b':visual=drawbrand_art(color)
 elif mode=='s':sources=[crop_source(content,crop)]
 elif mode=='d':sources=[crop_source(content,b) for b in crop]
 if layout=='W':
  textfit(im,h1,48,120,85,WHITE,1175);textfit(im,h2,48,220,88,color,1175);subfit(im,subtitle,53,326,1170,27)
  sourceframe(im,sources,(414,383,819,288),'Кадр из стрима',color,True);pill(im,badge,48,616,color)
 else:
  tx=48 if layout=='R' else 615;maxw=653 if layout=='R' else 616
  textfit(im,h1,tx,194,111,WHITE,maxw);textfit(im,h2,tx,321,113,color,maxw);subfit(im,subtitle,tx+4,487,maxw-4,27);pill(im,badge,tx,621,color)
  if mode in ['a','v','b']:place_art(im,visual,(706,146,558,558) if layout=='R' else (6,147,583,557))
  else:
   box=(733,151,499,531) if layout=='R' else (48,151,514,531)
   isprogram=row['key'] in ['PY','LV','SE','DEV'] or n in [5,11]
   head='LabVIEW / интерфейс' if row['key']=='LV' or n==5 else 'MOKO SE / интерфейс' if isprogram else 'Проект / исходное фото'
   if n in [2,4]:head='Кадр из стрима'
   if n in [14,49,55,57,86,87,88,89,90,91,92]:head='Оборудование / фото'
   if n==15:head='Калибратор + мультиметр'
   if n==51:head='LabVIEW / схема кнопки'
   if n==69:head='MOKO Modem / исходный экран'
   if n in [44,52,56,60,67]:head='Кадр из исходного ролика'
   if n==85:head='Keysight / Москва, 2020'
   if n in [63,64]:head='MONITOR BALL / MALANKA'
   sourceframe(im,sources,box,head,color)
 brand(im);im.save(out,quality=91,optimize=True)
 note='Исходный интерфейс/фото: сохранён без генеративной перерисовки, обрезаны поля и добавлена рамка.' if mode in ['s','d'] else 'Условная иллюстрация/схема; не изображение конкретной модели или точного интерфейса.'
 if n==63:note+=' Кадр проекта из русской версии MONITOR BALL использован и для английской версии того же проекта.'
 dtext=desc.get(row['id'],{}).get('description') or ''
 substantive=dtext.split('Дополнительная информация')[0].split('🔺')[0].strip()
 sourcebasis='Название + исходная обложка + описание автора' if len(substantive)>45 else 'Название + исходная обложка; содержательное описание ограничено'
 new.append({'number':n,'id':row['id'],'headline':h1+' '+h2,'subtitle':subtitle,'badge':badge,'layout':layout,'visual_mode':mode,'source_number':content if isinstance(content,int) else None,'crop':crop,'note':note,'basis':sourcebasis,'file':'thumbnails/'+row['id']+'.jpg'})
# Two dedicated vertical frames for Shorts, not falsely advertised as conventional uploadable custom covers.
for n in [93,94]:
 row=by[n];color=row['color'];im=Image.new('RGB',(1080,1920),BG);d=ImageDraw.Draw(im)
 for x in range(0,1080,48):d.line((x,0,x,1920),fill='#101b2b')
 for y in range(0,1920,48):d.line((0,y,1080,y),fill='#101b2b')
 d.rectangle((58,79,65,110),fill=color);d.text((82,80),'MOKO / МЕДИА' if n==93 else 'LABVIEW / РОБОТОТЕХНИКА',font=f(25,550,True),fill=color)
 logo=Image.open(R/'brand/logo.png').convert('RGBA');logo=ImageOps.contain(logo,(54,40));im.paste(logo,(718,80),logo);d.text((790,79),'MOKO',font=f(32,500,True),fill=WHITE)
 if n==93:
  title1,title2='MOKO','ПРОМО';sub='Технологии в движении';src=crop_source(93,(0,.10,.982,.895));badge='SHORTS / ПРОМО'
 else:
  title1,title2='ДРАЙВЕРЫ','РОБО-РУКИ';sub='Rozum Robotics · LabVIEW';src=crop_source(94,(.441,.061,.95,.936));badge='SHORTS / ПРОЕКТ'
 textfit(im,title1,58,207,113,WHITE,952);textfit(im,title2,58,336,114,color,952);subfit(im,sub,62,496,948,31)
 sourceframe(im,[src],(87,616,875,1029),'Кадр из ролика' if n==93 else 'Rozum Robotics / исходное изображение',color)
 d.rounded_rectangle((58,1720,600,1782),radius=10,fill=color);d.text((79,1734),badge,font=f(28,600,True),fill=BG);d.text((60,1828),'MOKO / SYSTEMS',font=f(30,500,True),fill='#a3aebe')
 out=F/'shorts'/(row['id']+'.jpg');im.save(out,quality=91,optimize=True)
 new.append({'number':n,'id':row['id'],'headline':title1+' '+title2,'subtitle':sub,'badge':badge,'layout':'vertical','visual_mode':'s','source_number':n,'note':'Вертикальный макет 1080×1920. Исходное изображение сохранено. Не обычная пользовательская обложка Shorts: применение зависит от доступного выбора/монтажа кадра.','basis':'Название и исходная обложка','file':'shorts/'+row['id']+'.jpg'})
assert len(new)==76,len(new)
assert len(list(P.glob('*.jpg')))==92
(F/'briefs/new_76.json').write_text(json.dumps(new,ensure_ascii=False,indent=2))
print('New:',len(new),'Horizontal total:',len(list(P.glob('*.jpg'))),'Vertical:',len(list((F/'shorts').glob('*.jpg'))))
