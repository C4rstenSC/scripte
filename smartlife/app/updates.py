"""Pinned-channel HTTPS updater with digest, bounded extraction and rollback."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
import time
from urllib.parse import urlparse
import zipfile
import requests
from core import VERSION, RUNTIME, MANIFESTS

def version(s):
    if not re.fullmatch(r'\d+\.\d+\.\d+',str(s)): raise ValueError('Ungültige Versionsnummer.')
    return tuple(map(int,s.split('.')))

def branch_head():
    # Git's ref advertisement is revalidated by GitHub, unlike mutable raw URLs.
    r=requests.get('https://github.com/C4rstenSC/scripte.git/info/refs',params={'service':'git-upload-pack'},timeout=20,headers={'Cache-Control':'no-cache, no-store','Pragma':'no-cache'},allow_redirects=False)
    r.raise_for_status()
    if r.is_redirect:raise ValueError('Unerwartete Weiterleitung bei der Updateprüfung.')
    raw=r.content
    if len(raw)>1024*1024:raise ValueError('Die GitHub-Antwort ist zu groß.')
    position=0
    while position<len(raw):
        try:length=int(raw[position:position+4],16)
        except ValueError:raise ValueError('GitHub hat keine gültige Versionsreferenz geliefert.')
        position+=4
        if length==0:continue
        if length<4 or position+length-4>len(raw):raise ValueError('Unvollständige Versionsreferenz von GitHub.')
        line=raw[position:position+length-4].split(b'\x00',1)[0].strip();position+=length-4
        match=re.fullmatch(rb'([0-9a-f]{40}) refs/heads/main',line)
        if match:return match.group(1).decode('ascii')
    raise ValueError('Der aktuelle Updatezweig konnte nicht ermittelt werden.')

def check():
    url=MANIFESTS.get(sys.platform)
    if not url: raise RuntimeError('Für dieses Betriebssystem gibt es keinen Updatekanal.')
    commit=branch_head();url=url.replace('/main/','/'+commit+'/',1)
    r=requests.get(url,params={'_':str(time.time_ns())},timeout=20,headers={'Cache-Control':'no-cache, no-store','Pragma':'no-cache'}); r.raise_for_status(); m=r.json()
    if m.get('status')!='available':raise RuntimeError('Für dieses Betriebssystem ist noch keine Version freigegeben.')
    if m.get('platform')!=sys.platform: raise ValueError('Update ist für ein anderes Betriebssystem bestimmt.')
    validate_url(m['url']);m['url']=m['url'].replace('/main/','/'+commit+'/',1)
    return m, version(m['version'])>version(VERSION)

def validate_url(url):
    p=urlparse(url)
    if p.scheme!='https' or p.hostname!='raw.githubusercontent.com' or not p.path.startswith('/C4rstenSC/scripte/') or p.username or p.password:
        raise ValueError('Ungültige Updatequelle.')

def extract(archive,destination):
    total=0
    with zipfile.ZipFile(archive) as z:
        for i in z.infolist():
            p=PurePosixPath(i.filename)
            if p.is_absolute() or '..' in p.parts or not p.parts or p.parts[0]!='app' or '\\' in i.filename or ':' in i.filename or (i.external_attr>>16)&0o170000==0o120000:
                raise ValueError('Unzulässiger Dateipfad im Update.')
            total+=i.file_size
            if total>20*1024*1024: raise ValueError('Update überschreitet die zulässige Größe.')
        z.extractall(destination)
    if not (destination/'app'/'main.py').is_file() or not (destination/'app'/'core.py').is_file(): raise ValueError('Update ist unvollständig.')

def stage(m,root):
    if m.get('runtime')!=RUNTIME: raise RuntimeError('Dieses Update benötigt ein neues Grundpaket. Bitte die neue Vollversion installieren.')
    validate_url(m['url'])
    if not re.fullmatch('[0-9a-f]{64}',m.get('sha256','')): raise ValueError('Prüfsumme fehlt.')
    dest=Path(tempfile.mkdtemp(prefix='SmartLife-update-')); archive=dest/'update.zip'; h=hashlib.sha256(); size=0
    with requests.get(m['url'],timeout=30,stream=True,allow_redirects=False) as r:
        r.raise_for_status()
        if r.is_redirect: raise ValueError('Unerwartete Weiterleitung.')
        with archive.open('wb') as f:
            for block in r.iter_content(65536):
                size+=len(block)
                if size>10*1024*1024: raise ValueError('Update ist zu groß.')
                h.update(block); f.write(block)
    if h.hexdigest()!=m['sha256']: raise ValueError('Prüfsumme stimmt nicht. Update wurde verworfen.')
    extract(archive,dest)
    declared=re.search(r"VERSION\s*=\s*['\"]([^'\"]+)", (dest/'app'/'core.py').read_text('utf-8'))
    if not declared or declared.group(1)!=m['version']: raise ValueError('Updateversion stimmt nicht überein.')
    # Runner is outside the app folder so the old version can be moved on Windows.
    import shutil
    runner=dest/'app'/'update_runner.py'
    if not runner.is_file():raise ValueError('Update-Installationsdatei fehlt.')
    shutil.copy2(runner,dest/'runner.py')
    return str(dest)

def install(staged,root):
    runner=Path(staged)/'runner.py'
    exe=Path(root)/'runtime'/'pythonw.exe'
    if sys.platform!='win32': raise RuntimeError('Die macOS-Installation wird mit der Mac-Version freigeschaltet.')
    subprocess.Popen([str(exe),str(runner),'--pid',str(os.getpid()),'--root',str(root),'--stage',str(staged)],creationflags=0x08000000)
