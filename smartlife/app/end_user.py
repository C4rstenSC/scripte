"""Tuya Smart Control end-user REST API, documented at tuya.ai/developer/docs.
Only user-initiated renames are written; never retries mutations.
"""
import re,time
from urllib.parse import quote
import requests
HOSTS={'EU':'openapi.tuyaeu.com','WE':'openapi-weaz.tuyaeu.com','AY':'openapi.tuyacn.com',
       'AZ':'openapi.tuyaus.com','UE':'openapi-ueaz.tuyaus.com','IN':'openapi.tuyain.com','SG':'openapi-sg.iotbing.com'}
class EndUserAPI:
    def __init__(self,key,session=None):
        self.key=str(key).strip()
        if not re.fullmatch(r'sk-(?:EU|WE|AY|AZ|UE|IN|SG)[A-Za-z0-9]+',self.key):
            raise ValueError('Bitte einen Endnutzer-API-Schlüssel von tuya.ai eingeben (sk-…). Access ID und Access Secret sind andere Zugangsdaten.')
        self.origin='https://'+HOSTS[self.key[3:5]];self.session=session or requests.Session()
    def request(self,method,path,body=None):
        try:
            reply=self.session.request(method,self.origin+path,headers={'Authorization':'Bearer '+self.key,'Content-Type':'application/json'},json=body,timeout=20,allow_redirects=False)
            if 300<=reply.status_code<400:raise RuntimeError('Unerwartete Weiterleitung. Endnutzer-Anfrage abgebrochen.')
            reply.raise_for_status();data=reply.json()
        except requests.RequestException as e:raise RuntimeError('Endnutzer-Zugang nicht erreichbar oder abgelehnt. Bei Zeitüberschreitung einer Änderung zuerst den tatsächlichen Namen prüfen.') from None
        except ValueError:raise RuntimeError('Endnutzer-Zugang hat keine lesbare Antwort geliefert.') from None
        if not isinstance(data,dict) or data.get('success') is not True:
            code=str(data.get('code','unbekannt')) if isinstance(data,dict) else 'unbekannt'
            if not re.fullmatch(r'[0-9]{1,16}',code):code='unbekannt'
            raise RuntimeError('Endnutzer-Zugang: Anfrage abgelehnt (Fehler '+code+'). Schlüssel, Kontoverknüpfung und verfügbare Aufrufe prüfen.')
        return data.get('result')
    def devices(self):
        data=self.request('GET','/v1.0/end-user/devices/all')
        rows=data.get('devices') if isinstance(data,dict) else None
        if not isinstance(rows,list):raise RuntimeError('Endnutzer-Zugang liefert keine Geräteliste.')
        return rows
    def detail(self,did):
        data=self.request('GET','/v1.0/end-user/devices/'+quote(str(did),safe='')+'/detail')
        if not isinstance(data,dict) or str(data.get('device_id',''))!=str(did):raise RuntimeError('Dieses Gerät wurde im Endnutzer-Konto nicht eindeutig bestätigt. Es wird nichts als erfolgreich geändert angezeigt.')
        return data
    def rename(self,did,name):
        # Confirm the exact target in this account before writing anything.
        self.detail(did)
        result=self.request('POST','/v1.0/end-user/devices/'+quote(str(did),safe='')+'/attribute',{'name':name})
        if result is False:raise RuntimeError('Endnutzer-Zugang hat die Änderung nicht bestätigt.')
        for attempt in range(3):
            try:data=self.detail(did)
            except Exception as e:raise RuntimeError('Die Namensänderung wurde angenommen, konnte anschließend aber nicht zurückgelesen werden. '+str(e)) from None
            if data.get('name')==name:return {'id':str(did),'name':name,**({'online':data['online']} if isinstance(data.get('online'),bool) else {})}
            if attempt<2:time.sleep(.2)
        raise RuntimeError('Der gewünschte Gerätename wurde nach dem Speichern nicht bestätigt. Bitte vor einem erneuten Versuch den tatsächlichen Namen prüfen.')
    def close(self):self.session.close()
