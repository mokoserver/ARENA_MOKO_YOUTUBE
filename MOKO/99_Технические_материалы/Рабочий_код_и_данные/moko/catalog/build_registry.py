from pathlib import Path
import json,re,collections
R=Path('/home/user/moko');V=json.load(open(R/'catalog/all_videos.json'))
G={
'PY':dict(name='Python — автоматизация в MOKO SE',visual='Уроки Python',color='#B8EB55',tag='PYTHON / MOKO SE',order=1,nums=[16]+list(range(22,42)),description='Последовательный курс Python для MOKO SE: установка, проекты, команды, отчёты, плагины, графики и Telegram.',sorting='По номеру урока: 0, 0.1, 1, 2 … 14. Не по дате публикации.'),
'LV':dict(name='LabVIEW — драйверы, утилиты и плагины',visual='Разработка · LabVIEW',color='#FF9A48',tag='LABVIEW / РАЗРАБОТКА',order=2,nums=list(range(17,22))+[51,65,70,77,78,79,80,81],description='Разработка драйверов, утилит, плагинов и интерфейсов на LabVIEW для экосистемы MOKO.',sorting='Сначала курс 0 → 1.1 → 1.2 → 2.1 → 2.2; затем интерфейсы, State Machine, библиотеки, плагины и PRESET 1 → 2.'),
'SE':dict(name='MOKO SE — возможности и инструкции',visual='MOKO SE · Инструкции',color='#55D6C2',tag='MOKO SE / ИНСТРУКЦИИ',order=3,nums=[13,45,46,47,48,50,53,54,58,59,62,72,74,75,76,82],description='Обзор платформы, запуск, отчёты, изображения, интеграции и отдельные функции MOKO SE вне последовательного курса.',sorting='Полная презентация и первый запуск → базовые функции → отчёты/изображения → плагины и интеграции → анонсы. Отмечать устаревшие версии.'),
'TEST':dict(name='Автоматизация измерений — стенды, испытания и поверка',visual='Практика · Испытания',color='#55C9FF',tag='ПРАКТИКА / ИСПЫТАНИЯ',order=4,nums=[2,3,9,11,15,66,83,84,90,91],description='Реальные измерительные задачи, автоматизированные испытания, лаборатории, стенды и поверка приборов.',sorting='Обзор лаборатории → демонстрации решений → частные испытания; стримы по теме добавлять после соответствующего кейса.'),
'HW':dict(name='Электроника и оборудование — проекты MOKO',visual='Практика · Электроника',color='#55C9FF',tag='ПРАКТИКА / ЭЛЕКТРОНИКА',order=5,nums=[14,42,49,55,57,63,64,86,87,88,89,92,94],description='Контроллеры, телеметрия, электронные устройства, оборудование и инженерные проекты MOKO.',sorting='По продуктовым сериям; внутри серии — от общего обзора к деталям. Английскую версию MONITOR BALL поставить рядом с русской и пометить EN.'),
'DEV':dict(name='Разработка ПО — практика, инструменты и стримы',visual='Разработка · Практика',color='#FF9A48',tag='РАЗРАБОТКА',order=6,nums=[5,6,7,8,10,12,43,68,69,71,73],description='Практическая разработка, C#/.NET, настройка инструментов, работа с драйверами и разборы задач в прямом эфире.',sorting='Связанные стримы — по номеру; самостоятельные инструкции — тематическими блоками. Не приписывать язык программирования, если он не подтверждён.'),
'CO':dict(name='MOKO — компания, выставки и интервью',visual='Компания · События',color='#ED6262',tag='MOKO / СОБЫТИЯ',order=7,nums=[1,4,61,67,85],description='Новости MOKO, выставки, партнёрства, интервью и знакомство с компанией.',sorting='Свежие события сначала; обзор компании можно закрепить первым. Год выставки сохранять.'),
'MEDIA':dict(name='Медиапроекты MOKO — промо и съёмки',visual='Медиа · Портфолио',color='#B69AFF',tag='MOKO / МЕДИА',order=8,nums=[44,52,56,60,93],description='Проморолики, медиапроизводство и примеры творческих работ MOKO.',sorting='Описание медиауслуг → примеры готовых работ → процесс создания. Не смешивать с техническими уроками.')}
# One primary playlist per item, with optional secondary playlists/format collection.
idx={}
for k,g in G.items():
 for n in g['nums']:
  assert n not in idx,(n,k);idx[n]=k
assert set(idx)==set(range(1,95))
heads=['MOKO SE → RF-SE','Тест источника питания','Автоматизация измерений','Разговор о MOKO SE','Запись в таблицу','Пишем плагин','Обновление MOKO SE','Обновление MOKO SE','Тест LED-фары','Инициализация драйверов','Тестируем IoT','Основа драйвера','AutoIt + MOKO SE','Новый станок XT-H1530','Поверка мультиметра','Дерево данных','Подключаем утилиту','Создаём утилиту','Подключаем драйвер','Создаём драйвер','Среда разработки','Снимки экрана','Управление мышью','Настройка графиков','Управление линиями','Графики в MOKO SE','Формируем протокол','Скрипты испытаний','Регистрация образца','Telegram + MOKO SE','Управление из скрипта','Форма ввода данных','Работа с плагинами','Обмен с приборами','Создаём отчёты','Сообщения в MOKO SE','Этапы программы','Запускаем проект','Структура папок','Создаём проект','Первый запуск','Контроллеры и телеметрия','Открываем файл программой','Johnny Respect / промо','Платформа автоматизации','MOKO SE в действии','Подключаем Telegram','Изображения в отчётах','Сенсорные моноблоки','Знакомство с MOKO SE','Кнопка в LabVIEW','Создаём каталог MOKO','Создаём PDF','Запуск скриптов','Контроллер ATLANT','БелЭнергоКип / промо','Модернизация упаковки','Знакомство с MOKO Graph','Спецсимволы в MOKO SE','Медиауслуги MOKO','Инженерия MOKO','MOKO SE / версия 2','MONITOR BALL / EN','MONITOR BALL','Свои кнопки','Объединяем отчёты','Подарок от SOFTEQ','Иконка для программы','Настройка модема','State Machine','C# / сервер не запускается','Плагины на C#','Несколько Google Дисков','Размер изображений','Таблицы в отчёте','Форматы изображений','PRESET / часть 2','PRESET / часть 1','Обновляем библиотеку','Создаём плагин','Настройка интерфейса','Дерево в MOKO SE','Поверка систем налива','Лаборатория под ключ','MOKO на Keysight','КУиТ-862 / телеметрия','Разработка спецоборудования','Датчик → 2API.by','Поворотная видеосистема','Стенд водоподготовки','Испытания стиральных машин','Прототип STM32F769','MOKO / короткое промо','Драйверы роботизированной руки']
assert len(heads)==94
rows=[]
for n,a in enumerate(V,1):
 key=idx[n];g=G[key];title=a['title'];isstream='стрим' in title.lower();language='Python' if key=='PY' else 'LabVIEW' if key=='LV' or n==94 else 'C# / .NET' if n in [69,71,72] else 'Не подтверждён / не применимо'
 lesson=re.search(r'Урок\s*№\s*([\d.]+)',title,re.I);lesson=lesson.group(1).rstrip('.') if lesson else ''
 fmt='Shorts' if a['source_tab']=='Shorts' else 'Стрим / интервью' if n==4 else 'Стрим' if isstream else 'Урок' if key in ['PY','LV'] else 'Промо' if key=='MEDIA' else 'Видео'
 notes=[];review=[]
 if n in [7,8]:notes.append('Оригинал / перезалив одного стрима. Сверить содержание и выбрать основную версию для плейлиста.');review.append('Дубликат: требуется решение')
 if n in [63,64]:notes.append('Русская и английская версии одного проекта; обе сохраняются, английская с меткой EN.')
 if n in [13,45,46,50,54,62,66,72,74,75,76,82]:notes.append('Проверить версию программы и актуальность интерфейса перед финальной обложкой.')
 if n==73:notes.append('Windows 10 и инструкция по Google Дискам могут быть устаревшими; проверить актуальность.');review.append('Актуальность')
 if a['source_tab']=='Shorts':notes.append('Нужен отдельный вертикальный макет; способ применения проверить в текущем интерфейсе YouTube.');review.append('Вертикальный формат')
 if n in [5,6,7,8,10,12]:notes.append('Не ставить Python/LabVIEW на обложке без подтверждения языка по содержанию.')
 if key not in ['PY','LV']:review.append('Тематика по метаданным; содержание не просмотрено полностью')
 extra=[]
 if isstream:extra.append('Стримы MOKO — разработка и измерения')
 if n in [17,18,19,20,21,51,65,70,77,78,79,80,81,94]:extra.append(G['DEV']['name'])
 if n in [47,58,72]:extra.append(G['DEV']['name'])
 if n in [2,3,9,11,15,66]:extra.append(G['SE']['name'])
 status='Готово · утверждённый образец' if n in [1,6,9,20,26,30] else 'Готово · новая партия 02, проверить' if (R/'production/thumbnails'/(a['id']+'.jpg')).exists() else 'Ожидает вертикального макета' if a['source_tab']=='Shorts' else 'В очереди'
 rows.append(dict(number=n,id=a['id'],title=title,url=a['url'],tab=a['source_tab'],existing='; '.join(a['existing_playlists']),key=key,playlist=g['name'],extra='; '.join(dict.fromkeys(extra)),visual=g['visual'],color=g['color'],language=language,format=fmt,lesson=lesson,headline=heads[n-1],status=status,review='; '.join(review),notes=' '.join(notes),file=('thumbnails/'+a['id']+'.jpg') if (R/'production/thumbnails'/(a['id']+'.jpg')).exists() else '',basis='Текущий плейлист Python + исходная обложка' if key=='PY' else 'Название LabVIEW или логотип LabVIEW на исходной обложке' if key=='LV' else 'Название, текущие плейлисты и исходная обложка'))
(R/'catalog/registry.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));(R/'catalog/proposed_playlists.json').write_text(json.dumps(G,ensure_ascii=False,indent=2))
for k,g in G.items():print(k,len(g['nums']),g['name'])
print(collections.Counter(a['status'] for a in rows))
