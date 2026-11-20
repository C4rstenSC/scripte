"""Smart Life Desktop: capability model and serialized Tuya sharing backend."""
from __future__ import annotations
import copy
import json
import math
import os
from pathlib import Path
import sys
import time
from urllib.parse import urlparse

VERSION = '0.1.0'
RUNTIME = 'win64-py313-qt683-v1'
# Public Tuya device-sharing registration also used by Home Assistant.
CLIENT_ID = 'HA_3y9q4ak7g4ephrvke'
SCHEMA = 'haauthorize'
MANIFESTS = {
 'win32': 'https://raw.githubusercontent.com/C4rstenSC/scripte/main/smartlife/updates/windows.json',
 'darwin': 'https://raw.githubusercontent.com/C4rstenSC/scripte/main/smartlife/updates/macos.json',
}
LABELS = {
 'temp_current':'Temperatur', 'va_temperature':'Temperatur', 'temperature':'Temperatur',
 'temp_current_f':'Temperatur (°F)', 'humidity_value':'Luftfeuchte', 'va_humidity':'Luftfeuchte',
 'battery_percentage':'Batterie', 'battery_state':'Batteriestatus', 'battery_value':'Batterie',
 'switch':'Ein/Aus', 'switch_1':'Schalter 1', 'switch_2':'Schalter 2', 'switch_3':'Schalter 3',
 'switch_led':'Licht', 'bright_value':'Helligkeit', 'bright_value_v2':'Helligkeit',
 'control':'Rollladen', 'percent_control':'Zielposition', 'percent_state':'Position',
 'fan_speed':'Lüfterstufe', 'fan_speed_enum':'Lüfterstufe', 'speed':'Geschwindigkeit',
 'mode':'Betriebsmodus', 'pm25':'Feinstaub PM2,5', 'pm25_value':'Feinstaub PM2,5',
 'filter':'Filter', 'filter_life':'Filterlebensdauer', 'filter_life_percent':'Filterlebensdauer',
 'child_lock':'Kindersicherung', 'anion':'Ionisierung', 'sleep':'Schlafmodus',
 'light':'Beleuchtung', 'fault':'Störung', 'air_quality':'Luftqualität',
 'cur_power':'Leistung', 'cur_voltage':'Spannung', 'cur_current':'Strom', 'countdown_1':'Countdown',
}
ENUMS = {'open':'Öffnen','close':'Schließen','stop':'Stoppen','on':'Ein','off':'Aus',
 'auto':'Automatisch','manual':'Manuell','sleep':'Schlafmodus','low':'Niedrig',
 'middle':'Mittel','medium':'Mittel','high':'Hoch','normal':'Normal','good':'Gut',
 'excellent':'Sehr gut','poor':'Schlecht','bright':'Hell','white':'Weiß','colour':'Farbe'}

def label(code, spec=None):
    return LABELS.get(code) or (spec or {}).get('name') or code.replace('_',' ').capitalize()

def meta(spec):
    v=(spec or {}).get('values', {})
    if isinstance(v,str):
        try: v=json.loads(v)
        except (ValueError,TypeError): v={}
    return v if isinstance(v,dict) else {}

def fmt(value, spec=None):
    m=meta(spec)
    if isinstance(value,bool): return 'Ein' if value else 'Aus'
    if isinstance(value,(int,float)):
        scale=int(m.get('scale',0)); unit=str(m.get('unit',''))
        value=value/(10**scale)
        return (f'{value:.{max(0,min(scale,6))}f}').replace('.',',')+(' '+unit if unit else '')
    if isinstance(value,(dict,list)): return json.dumps(value,ensure_ascii=False)
    return ENUMS.get(str(value), str(value))

def validate(spec, value):
    typ=spec.get('type','').lower(); m=meta(spec)
    if typ=='boolean':
        if not isinstance(value,bool): raise ValueError('Ein/Aus-Wert erforderlich.')
    elif typ=='enum':
        if value not in m.get('range',[]): raise ValueError('Unbekannter Betriebsmodus.')
    elif typ=='integer':
        if isinstance(value,bool) or not isinstance(value,int): raise ValueError('Ganzzahliger Wert erforderlich.')
        lo,hi,step=m.get('min',0),m.get('max',100),max(1,m.get('step',1))
        if not lo<=value<=hi or (value-lo)%step: raise ValueError('Wert außerhalb des zulässigen Bereichs.')
    else: raise ValueError('Diese Funktion kann hier nur angezeigt werden.')
    return value

def safe_endpoint(endpoint):
    p=urlparse(endpoint)
    return p.scheme=='https' and not p.username and not p.password and (p.hostname or '').endswith(('.tuya.com','.iotbing.com','.tuyaeu.com','.tuyaus.com','.tuyacn.com')) and not p.query and not p.fragment

def data_dir():
    if sys.platform=='win32': return Path(os.environ.get('LOCALAPPDATA',str(Path.home())))/'SmartLifeDesktop'
    if sys.platform=='darwin': return Path.home()/'Library'/'Application Support'/'SmartLifeDesktop'
    return Path.home()/'.local'/'share'/'SmartLifeDesktop'

class Vault:
    """Windows current-user DPAPI; macOS Keychain. Never plaintext credentials."""
    def __init__(self, folder=None): self.folder=Path(folder) if folder else data_dir()
    def _crypt(self, raw, decrypt=False):
        import ctypes
        from ctypes import wintypes
        class Blob(ctypes.Structure): _fields_=[('cbData',wintypes.DWORD),('pbData',ctypes.POINTER(ctypes.c_char))]
        buf=ctypes.create_string_buffer(raw); src=Blob(len(raw),ctypes.cast(buf,ctypes.POINTER(ctypes.c_char))); dst=Blob()
        dll=ctypes.windll.crypt32
        if decrypt: ok=dll.CryptUnprotectData(ctypes.byref(src),None,None,None,None,1,ctypes.byref(dst))
        else: ok=dll.CryptProtectData(ctypes.byref(src),ctypes.c_wchar_p('Smart Life Desktop'),None,None,None,1,ctypes.byref(dst))
        if not ok: raise OSError('Windows konnte die Anmeldung nicht schützen.')
        try: return ctypes.string_at(dst.pbData,dst.cbData)
        finally: ctypes.windll.kernel32.LocalFree(dst.pbData)
    def save(self,value):
        raw=json.dumps(value).encode()
        if sys.platform=='win32':
            self.folder.mkdir(parents=True,exist_ok=True)
            target=self.folder/'session.dat'; tmp=target.with_suffix('.tmp'); tmp.write_bytes(self._crypt(raw)); tmp.replace(target)
        elif sys.platform=='darwin':
            import keyring
            keyring.set_password('SmartLifeDesktop','session',raw.decode())
        else: raise RuntimeError('Sichere Speicherung ist hier nicht verfügbar.')
    def load(self):
        if sys.platform=='win32':
            p=self.folder/'session.dat'
            return json.loads(self._crypt(p.read_bytes(),True)) if p.exists() else None
        if sys.platform=='darwin':
            import keyring
            raw=keyring.get_password('SmartLifeDesktop','session'); return json.loads(raw) if raw else None
        return None
    def clear(self):
        if sys.platform=='darwin':
            import keyring
            try: keyring.delete_password('SmartLifeDesktop','session')
            except keyring.errors.PasswordDeleteError: pass
        else: (self.folder/'session.dat').unlink(missing_ok=True)

class Cloud:
    """All methods called by one executor, never on the UI thread."""
    def __init__(self):
        import tuya_sharing.user as userapi
        userapi.DEFAULT_TIMEOUT=20
        from tuya_sharing import LoginControl
        self.login=LoginControl(); self.login.session.trust_env=True; self.manager=None; self.state=None; self.vault=Vault(); self.remember=True
        self.homes=[]; self.devices=[]; self.scenes=[]; self.room_warnings=0; self.room_failed=[]; self.qr_created=0
    def qr(self,code):
        code=code.strip()
        if not code: raise ValueError('Bitte deinen Benutzercode aus Smart Life eingeben.')
        result=self.login.qr_code(CLIENT_ID,SCHEMA,code)
        if not result.get('success'): raise RuntimeError('Smart Life: '+str(result.get('msg','QR-Code konnte nicht erstellt werden.')))
        self.code=code; self.qr_token=result['result']['qrcode']; self.qr_created=time.time()
        return 'tuyaSmart--qrLogin?token='+self.qr_token
    def poll_login(self):
        if time.time()-self.qr_created>180: raise RuntimeError('QR-Code abgelaufen. Bitte einen neuen erzeugen.')
        ok,info=self.login.login_result(self.qr_token,CLIENT_ID,self.code)
        if not ok: return False
        self.attach({'user_code':self.code,'info':info},save=True)
        return True
    def attach(self,state,save=False):
        from tuya_sharing import Manager
        self.stop()
        import tuya_sharing.customerapi as customerapi
        customerapi.DEFAULT_TIMEOUT=20
        info=state['info']
        if not safe_endpoint(info['endpoint']): raise RuntimeError('Ungültige Smart-Life-Serveradresse.')
        self.state=copy.deepcopy(state)
        class Tokens:
            def __init__(self,owner): self.owner=owner
            def update_token(self,token):
                self.owner.state['info'].update(token)
                if self.owner.remember: self.owner.vault.save(self.owner.state)
        self.manager=Manager(CLIENT_ID,state['user_code'],info['terminal_id'],info['endpoint'],info,Tokens(self))
        if save and self.remember: self.vault.save(self.state)
    def restore(self):
        s=self.vault.load()
        if s: self.attach(s)
        return bool(s)
    def load(self):
        if not self.manager: raise RuntimeError('Bitte zuerst mit Smart Life verbinden.')
        m=self.manager
        homes=m.home_repository.query_homes()
        devices=[]; room_failed=[]
        # Keep home association even if a device belongs to multiple shared homes.
        for h in homes:
            for d in m.device_repository.query_devices_by_home(h.id):
                try: r=m.query_room_by_device(d.id)
                except Exception: r=None; room_failed.append(d.id)
                devices.append(self.snapshot(d,h.id,r))
                m.device_map[d.id]=d
        self.homes=[{'id':h.id,'name':h.name} for h in homes]; m.user_homes=homes
        self.devices=devices; self.room_failed=room_failed
        self.scenes=[]
        scene_error=False
        try:
            self.scenes=[{'id':s.scene_id,'name':s.name,'home':str(s.home_id),'enabled':getattr(s,'enabled',True)} for s in m.query_scenes()]
        except Exception: scene_error=True
        return {'homes':self.homes,'devices':copy.deepcopy(devices),'scenes':self.scenes,
                'room_failed':len(room_failed),'scene_error':scene_error}
    @staticmethod
    def snapshot(d,home,room=None):
        return {'id':d.id,'name':d.name,'home':str(home),'room_id':str(room.id) if room else '',
                'room':room.name if room else '', 'room_order':getattr(room,'display_order',0) if room else 0,
                'online':bool(d.online),'category':getattr(d,'category',''),
                'status':copy.deepcopy(d.status),'functions':{k:vars(v).copy() for k,v in d.function.items()},
                'ranges':{k:vars(v).copy() for k,v in d.status_range.items()}}
    def refresh(self):
        # Read status without repeatedly fetching specifications, rooms or strategies.
        ids=list(dict.fromkeys(d['id'] for d in self.devices))
        for start in range(0,len(ids),20):
            reply=self.manager.customer_api.get('/v1.0/m/life/ha/devices/detail',{'devIds':','.join(ids[start:start+20])})
            if not reply or not reply.get('success'): raise RuntimeError('Gerätestatus konnte nicht geladen werden.')
            for item in reply.get('result',[]):
                status=item.get('status',[])
                if isinstance(status,list): status={x['code']:x['value'] for x in status if 'code' in x and 'value' in x}
                for d in self.devices:
                    if d['id']==item['id']:
                        d['status']=status; d['online']=bool(item.get('online',d['online'])); d['name']=item.get('name',d['name'])
        return copy.deepcopy(self.devices)
    def command(self,device_id,code,value):
        d=next((d for d in self.devices if d['id']==device_id),None)
        if not d or not d['online']: raise RuntimeError('Gerät ist nicht online.')
        if code not in d['functions']: raise ValueError('Funktion ist für dieses Gerät nicht freigegeben.')
        validate(d['functions'][code],value)
        reply=self.manager.customer_api.post(f'/v1.1/m/thing/{device_id}/commands',None,{'commands':[{'code':code,'value':value}]})
        if not reply or not reply.get('success') or reply.get('result') is False: raise RuntimeError('Smart Life hat den Befehl nicht bestätigt.')
        return True
    def scene(self,home,scene):
        reply=self.manager.customer_api.post('/v1.0/m/scene/ha/trigger',None,{'homeId':home,'sceneId':scene})
        if not reply or not reply.get('success') or reply.get('result') is False: raise RuntimeError('Szene konnte nicht gestartet werden.')
        return True
    def logout(self):
        error=None
        try:
            if self.manager:
                self.manager.user_repository.unload(self.manager.terminal_id)
        except Exception: error='Lokale Anmeldung entfernt; die Verbindung konnte bei Smart Life nicht widerrufen werden.'
        finally:
            self.vault.clear(); self.stop(); self.state=None; self.devices=[]; self.homes=[]
        return error
    def stop(self):
        if self.manager:
            if self.manager.mq: self.manager.mq.stop()
            self.manager.customer_api.session.close()
        self.manager=None
