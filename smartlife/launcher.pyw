"""Stable entry point outside app so app can be replaced transactionally."""
from pathlib import Path
import os
import sys
import traceback
root=Path(__file__).resolve().parent
os.chdir(root)
sys.path.insert(0,str(root/'app'))
try:
 from main import run
 sys.exit(run())
except Exception:
 import ctypes
 message=traceback.format_exc()
 folder=Path(os.environ.get('LOCALAPPDATA',str(Path.home())))/'SmartLifeDesktop';folder.mkdir(parents=True,exist_ok=True)
 (folder/'Startfehler.txt').write_text(message,encoding='utf-8')
 ctypes.windll.user32.MessageBoxW(None,'Smart Life konnte nicht starten. Details: '+str(folder/'Startfehler.txt'),'Smart Life Desktop',0x10)
