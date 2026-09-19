"""Автоматическая публикация наборов кастомных эмодзи MOKO в Telegram.

Использует официальный Bot API: createNewStickerSet со sticker_type=custom_emoji
(доступно с Bot API 6.2). Набор создаётся в собственность указанного пользователя,
бот получает право редактировать набор. Скрипт сам подбирает эмодзи-привязки из
манифестов, загружает PNG и печатает ссылку t.me/addemoji/...

Что нужно:
1. Создать бота у @BotFather и взять токен.
2. Узнать свой числовой Telegram ID (например, у @userinfobot).
3. Запустить: python publish_telegram_pack.py --token <ТОКЕН> --user-id <ID> --set group_v03

Без сети/токена можно посмотреть план: добавьте --dry-run.
Загрузка идёт как multipart-файлы; привязки берутся из manifest.json наборов.
Использование кастомных эмодзи в чатах может требовать Telegram Premium по правилам Telegram.
"""
import argparse, json, sys
from pathlib import Path
import requests

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
API = 'https://api.telegram.org/bot{token}/{method}'

SETS = {
 'channel27': dict(
  manifest=ROOT/'99_Технические_материалы/Рабочий_код_и_данные/emoji_set_v02/manifest.json',
  folder=ROOT/'02_Telegram/02_Эмодзи_27', title='MOKO · Общение и инженерия', short='moko_channel_27'),
 'group_v02': dict(
  manifest=ROOT/'99_Технические_материалы/Рабочий_код_и_данные/emoji_group_v02/manifest.json',
  folder=ROOT/'02_Telegram/04_Эмодзи_Главная_группа', title='MOKO · Главная группа', short='moko_group_18'),
 'group_v03': dict(
  manifest=ROOT/'99_Технические_материалы/Рабочий_код_и_данные/emoji_group_v03/manifest.json',
  folder=ROOT/'02_Telegram/04_Эмодзи_Главная_группа', title='MOKO · Главная группа v03', short='moko_group_flat'),
}

def call(token, method, **kw):
 r = requests.post(API.format(token=token, method=method), timeout=60, **kw)
 data = r.json()
 if not data.get('ok'):
  raise SystemExit(f'Telegram API error in {method}: {data.get("description")}')
 return data['result']

def main():
 ap = argparse.ArgumentParser(description='Публикация набора эмодзи MOKO в Telegram')
 ap.add_argument('--token', default='', help='Токен бота (или переменная TELEGRAM_BOT_TOKEN)')
 ap.add_argument('--user-id', type=int, default=0, help='Ваш числовой Telegram ID — владелец набора')
 ap.add_argument('--set', choices=sorted(SETS), default='group_v03', help='Какой набор публиковать')
 ap.add_argument('--dry-run', action='store_true', help='Показать план без обращения к сети')
 args = ap.parse_args()
 token = args.token or __import__('os').environ.get('TELEGRAM_BOT_TOKEN', '')
 cfg = SETS[args.set]
 rows = json.loads(cfg['manifest'].read_text())
 stickers = []
 files = {}
 for i, r in enumerate(rows):
  png = cfg['folder']/r['file']
  assert png.is_file(), f'Не найден файл {png}'
  stickers.append({'sticker': f'attach://s{i}', 'format': 'static', 'emoji_list': [r['emoji']]})
  files[f's{i}'] = (png.name, png.read_bytes(), 'image/png')
 print(f'Набор: {args.set} · {len(rows)} эмодзи · привязки подобраны из манифеста:')
 for r in rows: print(f"  {r['slug']}  ->  {r['emoji']}")
 if args.dry_run:
  print('\n[dry-run] Будет вызван createNewStickerSet: user_id=<ваш ID>, '
        'name=<short>_by_<имя_бота>, sticker_type=custom_emoji, stickers=<файлы выше>.')
  return
 if not token or not args.user_id:
  sys.exit('Нужны --token и --user-id (или TELEGRAM_BOT_TOKEN). Для плана используйте --dry-run.')
 me = call(token, 'getMe')
 bot = me['username']
 name = f"{cfg['short']}_by_{bot}".lower()
 assert name.endswith(f'_by_{bot}'.lower()) and len(name) <= 64
 data = {'user_id': args.user_id, 'name': name, 'title': cfg['title'],
         'stickers': json.dumps(stickers, ensure_ascii=False), 'sticker_type': 'custom_emoji'}
 call(token, 'createNewStickerSet', data=data, files=files)
 print(f'\nГотово! Набор опубликован: https://t.me/addemoji/{name}')
 print('Проверьте в Telegram: настройки → стикеры и эмодзи → ваши наборы.')

if __name__ == '__main__':
 main()
