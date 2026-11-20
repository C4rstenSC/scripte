"""Standalone transactional Windows app update. Does not touch user credentials."""
import argparse
import ctypes
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

def alive(pid):
    k=ctypes.windll.kernel32; k.OpenProcess.restype=ctypes.c_void_p
    h=k.OpenProcess(0x1000,False,pid)
    if not h: return False
    k.GetExitCodeProcess.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_ulong)]
    k.CloseHandle.argtypes=[ctypes.c_void_p]
    code=ctypes.c_ulong()
    try: return bool(k.GetExitCodeProcess(h,ctypes.byref(code))) and code.value==259
    finally: k.CloseHandle(h)

def apply(root,stage):
    old=root/'app'; backup=root/'app.rollback'
    if backup.exists(): shutil.rmtree(backup)
    old.rename(backup)
    try:
        shutil.copytree(stage/'app',old)
        proc=subprocess.Popen([str(root/'runtime'/'pythonw.exe'),str(root/'launcher.pyw')],cwd=str(root))
        # Startup must signal readiness before we discard rollback.
        for _ in range(150):
            ready=root/'startup-ready.json'
            if ready.exists():
                try:
                    if json.loads(ready.read_text())['pid']==proc.pid: break
                except (ValueError,KeyError): pass
            if proc.poll() is not None: raise RuntimeError('Neue Version konnte nicht starten.')
            time.sleep(.2)
        else:
            proc.terminate(); proc.wait(timeout=10); raise RuntimeError('Neue Version meldet sich nicht startbereit.')
        shutil.rmtree(backup)
    except Exception:
        if old.exists(): shutil.rmtree(old)
        backup.rename(old)
        subprocess.Popen([str(root/'runtime'/'pythonw.exe'),str(root/'launcher.pyw')],cwd=str(root))
        raise

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--pid',type=int,required=True); p.add_argument('--root',type=Path,required=True); p.add_argument('--stage',type=Path,required=True); a=p.parse_args()
    try:
        for _ in range(150):
            if not alive(a.pid): break
            time.sleep(.2)
        else: raise RuntimeError('Programm wurde nicht beendet. Update abgebrochen.')
        apply(a.root,a.stage)
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(None,str(e),'Smart Life – Update fehlgeschlagen',0x10)
    finally:
        shutil.rmtree(a.stage,ignore_errors=True)
