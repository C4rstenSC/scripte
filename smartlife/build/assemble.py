"""Reproducible packaging from pinned official Python and PyPI wheels."""
import hashlib,json,shutil,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def extract_runtime(lock,cache,dest):
 dest.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(cache/lock['python']['file']) as z:z.extractall(dest)
 site=dest/'Lib/site-packages';site.mkdir(parents=True,exist_ok=True)
 for item in lock['wheels']:
  with zipfile.ZipFile(cache/item['file']) as z:
   for name in z.namelist():
    if name.startswith('PySide6/'):
     p=Path(name);base=p.name
     keep=(name.count('/')==1 and (base in ['__init__.py','_config.py','_git_pyside_version.py','QtCore.pyd','QtGui.pyd','QtWidgets.pyd','Qt6Core.dll','Qt6Gui.dll','Qt6Widgets.dll','pyside6.abi3.dll'] or base.startswith(('msvcp','vcruntime','concrt')))) or name.startswith(('PySide6/plugins/platforms/qwindows.','PySide6/plugins/styles/','PySide6/licenses/'))
     if not keep:continue
    z.extract(name,site)
 (dest/'python313._pth').write_text('python313.zip\n.\nLib/site-packages\nimport site\n')

def main():
 import argparse,urllib.request
 p=argparse.ArgumentParser();p.add_argument('--cache',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 lock=json.loads((ROOT/'runtime-lock.json').read_text())
 for i in [lock['python'],*lock['wheels']]:
  f=a.cache/i['file']
  if not f.exists():urllib.request.urlretrieve(i['url'],f)
  if hashlib.sha256(f.read_bytes()).hexdigest()!=i['sha256']:raise RuntimeError('Hash mismatch: '+f.name)
 a.output.mkdir(parents=True,exist_ok=True)
 for n in ['app','launcher.pyw','Starten.vbs','Installieren.cmd','Installieren.ps1','Anleitung.txt','README.md','runtime-lock.json','build']:
  src=ROOT/n;dst=a.output/n
  if src.is_dir():shutil.copytree(src,dst,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
  else:shutil.copy2(src,dst)
 extract_runtime(lock,a.cache,a.output/'runtime')
if __name__=='__main__':main()
