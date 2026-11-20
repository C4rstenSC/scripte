"""Smart Life Desktop: capability model and serialized Tuya sharing backend."""
from __future__ import annotations
import copy
import json
import math
import re
import os
from pathlib import Path
import sys
import time
from urllib.parse import urlparse

VERSION = '0.2.8'
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

LABELS.update({'bright_value':'Helligkeit','brightness_min':'Mindesthelligkeit','brightness_max':'Maximalhelligkeit',
 'relay_status':'Verhalten nach Stromausfall','countdown':'Ausschaltverzögerung','switch_mode':'Tastenereignis',
 'doorcontact_state':'Türkontakt','temper_alarm':'Manipulationsalarm','tamper_alarm':'Manipulationsalarm',
 'switch_led':'Licht','switch_usb':'USB-Anschluss','work_mode':'Betriebsmodus','control':'Rollladensteuerung',
 'mach_operate':'Rollladensteuerung','situation_set':'Gemeldete Rollladenstellung','position':'Position',
 'percent_state':'Istposition','percent_control':'Zielposition','motor_direction':'Motorrichtung',
 'control_back_mode':'Positionsrichtung','calibration':'Kalibrierung','light_mode':'Lichtmodus',
 'temp_set':'Solltemperatur','temp_unit_convert':'Temperatureinheit','filter_reset':'Filterzähler zurücksetzen',
 'filter_life':'Filterlebensdauer','pm25_value':'Feinstaub PM2,5','fault':'Störung'})
ENUMS.update({'memory':'Letzten Zustand wiederherstellen','click':'Einfacher Tastendruck',
 'double_click':'Doppelter Tastendruck','long_press':'Langer Tastendruck','hold':'Gedrückt halten',
 'release':'Losgelassen','true':'Ein','false':'Aus','forward':'Vorwärts','reverse':'Rückwärts',
 'power_on':'Einschalten','power_off':'Ausschalten','last':'Letzter Zustand','strong':'Stark',
 'soft':'Sanft','level_1':'Stufe 1','level_2':'Stufe 2','level_3':'Stufe 3','opening':'Öffnet',
 'closing':'Schließt','opened':'Geöffnet','closed':'Geschlossen','continue':'Weiterfahren',
 'wet':'Feucht','dry':'Trocken','alarm':'Alarm','normal':'Normal','cancel':'Abbrechen',
 'reset':'Zurücksetzen','start':'Starten','pause':'Pausieren','min':'Minimum','max':'Maximum'})

LABELS.update({'countdown_set':'Ausschaltzeit auswählen','countdown_left':'Verbleibende Laufzeit',
 'countdown':'Ausschaltverzögerung','countdown_1':'Ausschaltverzögerung 1','lock':'Kindersicherung',
 'light_switch':'Beleuchtung','uv':'UV-Licht','uv_switch':'UV-Licht','ionizer':'Ionisierung',
 'filter_life':'Verbleibende Filterlebensdauer','filter_status':'Filterzustand',
 'battery_low':'Batterie schwach','battery_percent':'Batteriestand','battery_voltage':'Batteriespannung'})
LABELS.update({'switch_type':'Tastenereignis','cur_current':'Stromaufnahme','cur_power':'Leistungsaufnahme',
 'add_ele':'Energieverbrauch','total_forward_energy':'Gesamtenergieverbrauch','cur_voltage':'Netzspannung',
 'power':'Leistung','voltage':'Spannung','current':'Stromaufnahme','electricity':'Energieverbrauch'})
ENUMS.update({'single_click':'Einfacher Tastendruck','single':'Einfacher Tastendruck',
 'double':'Doppelter Tastendruck','long':'Langer Tastendruck','long_click':'Langer Tastendruck',
 'press':'Gedrückt','press_up':'Losgelassen','press_down':'Gedrückt'})

LABELS.update({'temp_current_external':'Temperatur am externen Fühler','humidity':'Luftfeuchte','humidity_current':'Luftfeuchte',
 'do_not_disturb':'Nach Stromausfall ausgeschaltet bleiben',
 'hum_calibration':'Luftfeuchte-Korrektur','humidity_calibration':'Luftfeuchte-Korrektur',
 'temp_calibration':'Temperatur-Korrektur','temp_correction':'Korrektur der Fühlertemperatur',
 'temperature_calibration':'Temperatur-Korrektur','humidity_correction':'Luftfeuchte-Korrektur',
 'temp_sensitivity':'Temperatur-Meldeschwelle','hum_sensitivity':'Luftfeuchte-Meldeschwelle',
 'temp_report':'Temperatur-Meldeintervall','hum_report':'Luftfeuchte-Meldeintervall',
 'temp_max':'Obere Temperaturgrenze','temp_min':'Untere Temperaturgrenze',
 'humidity_max':'Obere Luftfeuchtegrenze','humidity_min':'Untere Luftfeuchtegrenze',
 'temp_alarm':'Temperaturalarm','humidity_alarm':'Luftfeuchtealarm',
 'temp_periodic_report':'Temperatur-Meldeintervall','humidity_periodic_report':'Luftfeuchte-Meldeintervall',
 'temp_sensitivity':'Temperatur-Meldeschwelle','humidity_sensitivity':'Luftfeuchte-Meldeschwelle',
 'temp_unit':'Temperatureinheit','bright_state':'Helligkeitszustand','temp_value':'Farbtemperatur',
 'colour_data':'Farbe','scene_data':'Lichtszene','music_data':'Musiksteuerung',
 'switch_backlight':'Hintergrundbeleuchtung','backlight':'Hintergrundbeleuchtung',
 'indicator_status':'Kontrollleuchte','led_type':'Leuchtmitteltyp','power_on_behavior':'Verhalten nach Stromausfall',
 'cur_voltage':'Netzspannung','voltage_current':'Spannung','power_current':'Leistungsaufnahme',
 'electric_current':'Stromaufnahme','rssi':'WLAN-Signalstärke','battery':'Batteriestand'})
ENUMS.update({'scene':'Lichtszene','music':'Musiksteuerung','warm':'Warmweiß','cold':'Kaltweiß',
 'reading':'Lesen','night':'Nachtlicht','working':'Arbeiten','leisure':'Freizeit',
 'small':'Niedrig','large':'Hoch','c':'Celsius','f':'Fahrenheit','centigrade':'Celsius','fahrenheit':'Fahrenheit'})

def ui_label(code,spec=None):
    if code in LABELS:return LABELS[code]
    match=re.fullmatch(r'(.+?)(?:_)?([0-9]+)',str(code))
    if match and match.group(1).rstrip('_') in LABELS:return LABELS[match.group(1).rstrip('_')]+' '+match.group(2)
    return ''

def unit_label(unit):
    text=str(unit or '')
    translated={'秒':'s','分钟':'min','小时':'h','摄氏度':'°C','华氏度':'°F','度':'°','伏':'V','安':'A','瓦':'W'}.get(text,text)
    return '' if re.search(r'[\u3400-\u9fff]',translated) else translated

def ui_control(code,spec):
    if not ui_label(code,spec):return False
    if spec.get('type','').lower()=='enum':return all(enum_label(v,code)!='Nicht zugeordnete Einstellung' for v in meta(spec).get('range',[]))
    return spec.get('type','').lower() in ('boolean','integer')

def enum_label(value,code=None):
    text=str(value)
    if code in ('mode','fan_speed','fan_speed_enum') and re.fullmatch(r'[1-9]F',text):return 'Lüfterstufe '+text[0]+' ('+text+')'
    if code in ('countdown_set','countdown') and text=='cancel':return 'Deaktiviert'
    if re.fullmatch(r'[0-9]+[hH]',text):return text[:-1]+' Stunde'+('' if text[:-1]=='1' else 'n')
    if text in ENUMS:return ENUMS[text]
    if re.fullmatch(r'[0-9. +%°-]+',text):return text
    return 'Nicht zugeordnete Einstellung'

def label(code, spec=None):
    if code in LABELS:return LABELS[code]
    # Tuya uses both switch_mode1 and switch_led_1 for numbered channels.
    match=re.fullmatch(r'(.+?)(?:_)?([0-9]+)',code)
    if match:
        base=match.group(1).rstrip('_')
        if base in LABELS:return LABELS[base]+' '+match.group(2)
    original=str((spec or {}).get('name','')).strip()
    if original and original!=code:return original+' ('+code+')'
    return 'Herstellerfunktion: '+code

def meta(spec):
    v=(spec or {}).get('values', {})
    if isinstance(v,str):
        try: v=json.loads(v)
        except (ValueError,TypeError): v={}
    return v if isinstance(v,dict) else {}

def fmt(value, spec=None):
    m=meta(spec)
    if value is None:return ''
    code=(spec or {}).get('code')
    if isinstance(value,bool) and code in ('doorcontact_state','doorcontact_state_2','doorcontact_state_3'):return 'Offen' if value else 'Geschlossen'
    if isinstance(value,bool) and code in ('tamper_alarm','temper_alarm'):return 'Alarm' if value else 'Kein Alarm'
    if code=='fault' and value==0:return 'Keine Störung'
    if isinstance(value,bool): return 'Ein' if value else 'Aus'
    if isinstance(value,(int,float)):
        scale=int(m.get('scale',0)); unit=unit_label(m.get('unit',''))
        value=value/(10**scale)
        return (f'{value:.{max(0,min(scale,6))}f}').replace('.',',')+(' '+unit if unit else '')
    if isinstance(value,(dict,list)): return 'Erweiterte Geräteeinstellung'
    return enum_label(value,(spec or {}).get('code'))

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
            keyring.set_password('SmartLifeDesktop','session:'+self.folder.name,raw.decode())
        else: raise RuntimeError('Sichere Speicherung ist hier nicht verfügbar.')
    def load(self):
        if sys.platform=='win32':
            p=self.folder/'session.dat'
            return json.loads(self._crypt(p.read_bytes(),True)) if p.exists() else None
        if sys.platform=='darwin':
            import keyring
            raw=keyring.get_password('SmartLifeDesktop','session:'+self.folder.name); return json.loads(raw) if raw else None
        return None
    def clear(self):
        if sys.platform=='darwin':
            import keyring
            try: keyring.delete_password('SmartLifeDesktop','session:'+self.folder.name)
            except keyring.errors.PasswordDeleteError: pass
        else: (self.folder/'session.dat').unlink(missing_ok=True)

class Cloud:
    """All methods called by one executor, never on the UI thread."""
    def __init__(self):
        import tuya_sharing.user as userapi
        userapi.DEFAULT_TIMEOUT=20
        from tuya_sharing import LoginControl
        self.login=LoginControl(); self.login.session.trust_env=True; self.manager=None; self.state=None; self.vault=Vault(); self.remember=True
        self.direct=None;self.direct_vault=Vault(data_dir()/'cloud-project');self.homes=[]; self.devices=[]; self.scenes=[]; self.room_warnings=0; self.room_failed=[]; self.qr_created=0
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
    def connect_direct(self,config,save=True):
        from project_cloud import DirectCloud
        candidate=DirectCloud(config)
        try:
            candidate.verify()
            if save:self.direct_vault.save(config)
        except Exception:
            candidate.close();raise
        self.stop();self.direct=candidate
        return True
    def restore(self):
        project=self.direct_vault.load()
        if project:
            self.connect_direct(project,save=False);return True
        s=self.vault.load()
        if s: self.attach(s)
        return bool(s)
    def load(self):
        if self.direct:
            data=self.direct.load();self.homes=data['homes'];self.devices=self.direct.devices;self.scenes=data['scenes'];return data
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
            self.scenes=[{'id':s.scene_id,'name':s.name,'home':str(s.home_id),'enabled':getattr(s,'enabled',True),'source':'smartlife','actions':copy.deepcopy(getattr(s,'actions',[]))} for s in m.query_scenes()]
        except Exception: scene_error=True
        return {'homes':self.homes,'devices':copy.deepcopy(devices),'scenes':self.scenes,
                'room_failed':len(room_failed),'scene_error':scene_error}
    @staticmethod
    def snapshot(d,home,room=None):
        return {'id':d.id,'name':d.name,'home':str(home),'room_id':str(room.id) if room else '',
                'room':room.name if room else '', 'room_order':getattr(room,'display_order',0) if room else 0,
                'mac':getattr(d,'mac','') or '', 'product_id':getattr(d,'product_id',''), 'product_name':getattr(d,'product_name',''), 'online':bool(d.online),'category':getattr(d,'category',''), 'ip':getattr(d,'ip','') or '', 'sub':bool(getattr(d,'sub',False)),
                'status':copy.deepcopy(d.status),'functions':{k:vars(v).copy() for k,v in d.function.items()},
                'ranges':{k:vars(v).copy() for k,v in d.status_range.items()}}
    def refresh(self,device_id=None):
        if self.direct:
            self.devices=self.direct.devices;return self.direct.refresh(device_id)
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
                        d['ip']=item.get('ip',d.get('ip','')) or ''; d['sub']=bool(item.get('sub',d.get('sub',False))); d['status']=status; d['online']=bool(item.get('online',d['online'])); d['name']=item.get('name',d['name'])
        return copy.deepcopy(self.devices)
    def probe(self,device_id):
        """Read documented API endpoints for one device; no guessed commands."""
        if self.direct:
            d=next(d for d in self.direct.devices if d['id']==device_id)
            d['status']=self.direct.read_status(d)
            report={'programmversion':VERSION,'gerät':d['name'],'produkt':d.get('product_name',''),'kategorie':d['category'],'bedienfunktionen':copy.deepcopy(d['functions']),'werte':copy.deepcopy(d['status']),'anbindung':'Direkter Cloudzugriff'}
            return {'report':report,'devices':copy.deepcopy(self.direct.devices)}
        if not self.manager:raise RuntimeError('Bitte zuerst anmelden.')
        d=next(d for d in self.devices if d['id']==device_id)
        report={'programmversion':VERSION,'gerät':d['name'],'kategorie':d.get('category',''),
                'produkt':d.get('product_name',''),'produktkennung':d.get('product_id',''),'abfragen':{}}
        api=self.manager.customer_api
        queries=[('gerätedetails','/v1.0/m/life/ha/devices/detail',{'devIds':device_id}),
                 ('funktionen',f'/v1.1/m/life/{device_id}/specifications',None),
                 ('datenpunktzuordnung',f'/v1.0/m/life/devices/{device_id}/status',None)]
        for name,path,params in queries:
            try:
                reply=api.get(path,params)
                report['abfragen'][name]=diagnostic_filter(reply)
            except Exception as e:
                report['abfragen'][name]={'fehlercode':str(getattr(e,'error_code',type(e).__name__))}
        # Re-read the complete SDK device representation in case Tuya has now supplied specs.
        try:
            fresh=self.manager.device_repository.query_devices_by_ids([device_id])
            if fresh:
                obj=fresh[0];self.manager.device_map[device_id]=obj
                d['status']=copy.deepcopy(obj.status)
                d['functions']={k:vars(v).copy() for k,v in obj.function.items()}
                d['ranges']={k:vars(v).copy() for k,v in obj.status_range.items()}
        except Exception:pass
        report['werte']=copy.deepcopy(d['status']);report['bedienfunktionen']=copy.deepcopy(d['functions'])
        return {'report':report,'devices':copy.deepcopy(self.devices)}

    def command(self,device_id,code,value):
        if getattr(self,'direct',None):return self.direct.command(device_id,code,value)
        d=next((d for d in self.devices if d['id']==device_id),None)
        if not d or not d['online']: raise RuntimeError('Gerät ist nicht online.')
        if code not in d['functions']: raise ValueError('Funktion ist für dieses Gerät nicht freigegeben.')
        validate(d['functions'][code],value)
        reply=self.manager.customer_api.post(f'/v1.1/m/thing/{device_id}/commands',None,{'commands':[{'code':code,'value':value}]})
        if not reply or not reply.get('success') or reply.get('result') is False: raise RuntimeError('Smart Life hat den Befehl nicht bestätigt.')
        return True
    def scene(self,home,scene):
        if self.direct:return self.direct.trigger(home,scene)
        reply=self.manager.customer_api.post('/v1.0/m/scene/ha/trigger',None,{'homeId':home,'sceneId':scene})
        if not reply or not reply.get('success') or reply.get('result') is False: raise RuntimeError('Szene konnte nicht gestartet werden.')
        return True
    def logout(self):
        if self.direct:
            self.direct_vault.clear();self.stop();self.state=None;self.devices=[];self.homes=[];return None
        error=None
        try:
            if self.manager:
                self.manager.user_repository.unload(self.manager.terminal_id)
        except Exception: error='Lokale Anmeldung entfernt; die Verbindung konnte bei Smart Life nicht widerrufen werden.'
        finally:
            self.vault.clear(); self.stop(); self.state=None; self.devices=[]; self.homes=[]
        return error
    def stop(self):
        if self.direct:self.direct.close();self.direct=None
        if self.manager:
            if self.manager.mq: self.manager.mq.stop()
            self.manager.customer_api.session.close()
        self.manager=None


TEMPERATURE_CODES=('va_temperature','temp_current','temperature','temp_current_f','temp_current_external')
HUMIDITY_CODES=('va_humidity','humidity_value','humidity','humidity_current')
def climate(d,codes,unit):
    parts=[]
    for code in codes:
        if code not in d['status'] or d['status'][code] is None:continue
        spec=d['ranges'].get(code) or d['functions'].get(code) or {}
        value=fmt(d['status'][code],spec)
        if not meta(spec).get('unit'):value+=' '+('°F' if code.endswith('_f') else unit)
        return value
    return ''

def is_cover(d):
    return any(word in d.get('name','').casefold() for word in ('rollladen','rolladen','jalousie','vorhang')) or d.get('category') in ('cl','clkg','jdcljqr') or any(c in d['functions'] for c in ('percent_control','control','mach_operate')) or any(c in d['status'] for c in ('percent_state','percent_state_1'))

def cover_position(d):
    # Actual position feedback only. percent_control is a target on many devices.
    for c in ('percent_state','percent_state_1','position','position_state','curtain_position'):
        v=d['status'].get(c)
        if isinstance(v,(int,float)) and not isinstance(v,bool):
            spec=d['ranges'].get(c) or d['functions'].get(c) or {};m=meta(spec)
            lo=float(m.get('min',0));hi=float(m.get('max',100))
            if hi<=lo:return None
            # Tuya cover percentage uses 0 closed, 100 open (same convention as HA).
            return max(0,min(100,round((v-lo)*100/(hi-lo))))
    return None

def cover_text(d):
    v=cover_position(d)
    if v is not None:
        return 'Geschlossen · 0 % offen' if v==0 else ('Vollständig offen · 100 % offen' if v==100 else f'{v} % offen')
    target=next((d['status'][c] for c in ('percent_control','percent_control_1') if c in d['status']),None)
    return 'Gemeldeter Sollwert: '+str(target)+' %' if target is not None else ''


def diagnostic_filter(value):
    # Allowlist only device schema/status fields. IDs, local keys, tokens, MACs and IPs are dropped.
    allowed={'success','code','msg','result','status','functions','values','value','name','type',
      'desc','dpId','dp_id','statusCode','status_code','valueConvert','statusFormat','valueDesc',
      'valueType','enumMappingMap','dpStatusRelationDTOS','supportLocal','productKey',
      'min','max','step','scale','unit','range'}
    if isinstance(value,dict):return {k:diagnostic_filter(v) for k,v in value.items() if k in allowed}
    if isinstance(value,list):return [diagnostic_filter(v) for v in value]
    return value


BATTERY_CODES=('battery_percentage','battery_percent','battery_value','battery_state','battery_low','battery_voltage')
def battery_text(d):
    status=d.get('status',{})
    for code in BATTERY_CODES:
        if code not in status or status[code] is None:continue
        value=status[code];spec=d.get('ranges',{}).get(code) or d.get('functions',{}).get(code) or {}
        if code=='battery_low' and isinstance(value,bool):return 'Schwach' if value else 'In Ordnung'
        text=fmt(value,spec)
        if code in ('battery_percentage','battery_percent') and not meta(spec).get('unit'):text+=' %'
        return text
    return ''

def probe_summary(report):
    functions=report.get('bedienfunktionen',{});values=report.get('werte',{})
    lines=['Gerät: '+str(report.get('gerät','')), 'Produkt: '+str(report.get('produkt','')),
           'Bedienfunktionen über diese Anbindung: '+str(len(functions)),
           'Gemeldete Werte: '+str(len(values))]
    if not functions:
        lines+=['','Diese Gerätefreigabe liefert keine Bedienfunktionen für dieses Modell. Darum kann das Programm das Gerät darüber nicht steuern.']
    if not values:lines+=['','Es wird auch keine aktuelle Position geliefert. Daraus folgt kein Defekt des Geräts; die Anzeige in der Smart-Life-App kann davon abweichen.']
    return '\n'.join(lines)
