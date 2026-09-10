"""Check sorted files or build a disposable copy of the old project layout.
Original sorted files are never modified. Cache directories are not deliverables.
"""
from pathlib import Path
import argparse,json,hashlib,shutil,zipfile
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--check',action='store_true',help='Verify all relocated original files (default).')
parser.add_argument('--restore',action='store_true',help='Rebuild the original layout in a disposable working directory.')
parser.add_argument('--destination',default='/home/user/.cache/MOKO_workbench')
parser.add_argument('--hydrate-archived',action='store_true',help='Also recreate earlier archived PNG intermediates from their ZIP or SVG sources.')
args=parser.parse_args()
plan=json.loads((HERE/'Карта_переноса.json').read_text())
for row in plan['files']:
 source=PROJECT/row['new']
 assert source.is_file(),str(source)
 assert source.stat().st_size==row['size'],str(source)
 assert hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256'],str(source)
print('Verified',len(plan['files']),'unchanged original files.')
if not args.restore:raise SystemExit(0)
dest=Path(args.destination).resolve()
assert dest.is_relative_to(Path('/home/user')), 'Destination must stay inside the workspace.'
assert not dest.is_relative_to(PROJECT), 'Do not restore into the sorted deliverable folder.'
if dest.exists() and any(dest.iterdir()):raise SystemExit('Destination is not empty. Choose another cache directory.')
dest.mkdir(parents=True,exist_ok=True)
for row in plan['files']:
 src=PROJECT/row['new'];dst=dest/row['old'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 # Only the disposable working copy is patched. Archived source files remain byte-identical.
 if dst.suffix.lower() in ['.py','.json','.md','.txt','.csv']:
  try:
   content=dst.read_text(encoding='utf-8')
   updated=content.replace('/home/user/moko',str(dest/'moko')).replace('/home/user/uploads',str(dest/'uploads'))
   if content!=updated:dst.write_text(updated,encoding='utf-8')
  except UnicodeError:pass
if args.hydrate_archived:
 t=dest/'moko/telegram_avatars';manifest=t/'source/archived_raster_locations.json'
 if manifest.exists():
  rows=json.loads(manifest.read_text())
  for item in rows:
   p=t/item['file']
   if p.exists():continue
   p.parent.mkdir(parents=True,exist_ok=True)
   if item.get('archive'):
    with zipfile.ZipFile(t/item['archive']) as z:p.write_bytes(z.read(item['member']))
   elif item.get('vector_source'):
    import cairosvg
    cairosvg.svg2png(bytestring=(t/item['vector_source']).read_bytes(),write_to=str(p))
print('Disposable working tree:',dest)
print('Historical scripts may still depend on inputs removed before the organization step; inspect their notes before running them.')
