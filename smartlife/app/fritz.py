"""Local FRITZ!Box host inventory and explicitly requested hostname changes."""
import copy,ipaddress,json,re,socket
from urllib.parse import urlparse
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape
import requests
from requests.auth import HTTPDigestAuth
from core import Vault,data_dir

HOSTS='urn:dslforum-org:service:Hosts:1'
PRIVATE_NETS=tuple(ipaddress.ip_network(n) for n in ('10.0.0.0/8','172.16.0.0/12','192.168.0.0/16','169.254.0.0/16','fc00::/7','fe80::/10'))
def local_ip(value):
    try:
        address=ipaddress.ip_address(str(value).split('%')[0])
        return str(address) if any(address.version==n.version and address in n for n in PRIVATE_NETS) else ''
    except ValueError:return ''
def mac(value):
    text=re.sub('[:-]','',str(value or '')).upper()
    return ':'.join(text[i:i+2] for i in range(0,12,2)) if re.fullmatch('[0-9A-F]{12}',text) and text not in ('000000000000','FFFFFFFFFFFF') else ''
def parse_xml(raw):
    if len(raw)>2*1024*1024 or b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper():raise ValueError('Ungültige XML-Antwort der FRITZ!Box.')
    try:return ET.fromstring(raw)
    except ET.ParseError as e:raise ValueError('Die FRITZ!Box liefert keine gültige Schnittstellenantwort.') from e
def child(node,name):return next((c.text or '' for c in node if c.tag.split('}')[-1]==name),'')
def fields(node):return {c.tag.split('}')[-1]:c.text or '' for c in node}
def safe_path(path):
    p=urlparse(path)
    if not path.startswith('/') or path.startswith('//') or p.scheme or p.netloc or '\\' in path or '..' in p.path or p.fragment:raise ValueError('Ungültige lokale Schnittstellenadresse.')
    return path
def host_record(data):
    aliases=re.findall(r'(?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}|[0-9a-fA-F]{12}',data.get('X_AVM-DE_MACAddressList',data.get('NewX_AVM-DE_MACAddressList','')))
    return {'mac':mac(data.get('MACAddress',data.get('NewMACAddress',''))),'aliases':[mac(v) for v in aliases if mac(v)],
      'ip':local_ip(data.get('IPAddress',data.get('NewIPAddress',''))),'hostname':data.get('HostName',data.get('NewHostName','')),
      'active':str(data.get('Active',data.get('NewActive','0'))).lower() in ('1','true')}
class FritzFault(RuntimeError):
    def __init__(self,code):
        self.code=str(code)
        super().__init__({'606':'Die FRITZ!Box-Berechtigung für diesen Netzwerkzugriff fehlt.',
         '714':'Dieser Netzwerkeintrag ist nicht mehr in der FRITZ!Box vorhanden.',
         '401':'Diese TR-064-Aktion wird nicht unterstützt oder die Anmeldung wurde abgelehnt.'}.get(self.code,'FRITZ!Box lehnt den Auftrag ab (Fehler '+self.code+').'))
class FritzClient:
    def __init__(self,config,session=None):
        address=str(config.get('address','fritz.box')).strip();p=urlparse(address if '://' in address else 'http://'+address)
        if p.scheme not in ('http','https') or not p.hostname or p.username or p.password or p.path not in ('','/') or p.query or p.fragment:raise ValueError('Bitte eine lokale FRITZ!Box-Adresse ohne Anmeldedaten oder Pfad eingeben.')
        try:port=p.port or (49443 if p.scheme=='https' else 49000)
        except ValueError:raise ValueError('Ungültiger FRITZ!Box-Port.')
        try:resolved=socket.getaddrinfo(p.hostname,port,type=socket.SOCK_STREAM)
        except OSError as e:raise RuntimeError('FRITZ!Box-Adresse wurde im Heimnetz nicht gefunden.') from e
        resolved=[r for r in resolved if local_ip(r[4][0])]
        if not resolved:raise ValueError('Die FRITZ!Box muss eine lokale Adresse im Heimnetz haben.')
        resolved.sort(key=lambda r:':' in r[4][0])
        # Pin the checked local address so authentication never follows an external redirect.
        address_ip=resolved[0][4][0];self.root=p.scheme+'://'+('['+address_ip+']' if ':' in address_ip else address_ip)+':'+str(port)
        self.user=str(config.get('user','')).strip();password=str(config.get('password',''))
        if not self.user or not password:raise ValueError('FRITZ!Box-Benutzername und Kennwort sind erforderlich.')
        self.session=session or requests.Session();self.session.trust_env=False;self.session.auth=HTTPDigestAuth(self.user,password);self.control='';self.actions=set()
    def request(self,method,path,**kwargs):
        try:
            r=self.session.request(method,self.root+safe_path(path),timeout=10,allow_redirects=False,**kwargs)
            if r.status_code in (401,403):raise RuntimeError('FRITZ!Box-Anmeldung abgelehnt. Benutzername, Kennwort und Benutzerrechte prüfen.')
            if 300<=r.status_code<400:raise RuntimeError('Weiterleitung der FRITZ!Box wird nicht übernommen.')
            xml=parse_xml(r.content);fault=next((n for n in xml.iter() if n.tag.split('}')[-1]=='errorCode'),None)
            if fault is not None:raise FritzFault(fault.text or 'unbekannt')
            r.raise_for_status();return xml
        except requests.RequestException as e:raise RuntimeError('FRITZ!Box nicht erreichbar. Lokale Adresse, Netzwerk und Zugriff für Anwendungen (TR-064) prüfen.') from e
    def discover(self):
        doc=self.request('GET','/tr64desc.xml')
        service=next((s for s in doc.iter() if s.tag.split('}')[-1]=='service' and child(s,'serviceType')==HOSTS),None)
        if service is None:raise RuntimeError('Die FRITZ!Box bietet keine TR-064-Netzwerkgeräteliste an.')
        self.control=safe_path(child(service,'controlURL'));description=self.request('GET',safe_path(child(service,'SCPDURL')))
        self.actions={child(n,'name') for n in description.iter() if n.tag.split('}')[-1]=='action'}
    def call(self,action,params=None):
        if action not in ('X_AVM-DE_GetHostListPath','GetHostNumberOfEntries','GetGenericHostEntry','GetSpecificHostEntry','X_AVM-DE_SetHostNameByMACAddress'):raise ValueError('Dieser Router-Aufruf ist nicht freigegeben.')
        if not self.control:self.discover()
        if action not in self.actions:raise FritzFault('401')
        values=''.join('<'+k+'>'+escape(str(v))+'</'+k+'>' for k,v in (params or {}).items())
        body=('<?xml version="1.0" encoding="utf-8"?><s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:'+action+' xmlns:u="'+HOSTS+'">'+values+'</u:'+action+'></s:Body></s:Envelope>').encode()
        doc=self.request('POST',self.control,data=body,headers={'Content-Type':'text/xml; charset=utf-8','SOAPACTION':'"'+HOSTS+'#'+action+'"'})
        response=next((n for n in doc.iter() if n.tag.split('}')[-1]==action+'Response'),None)
        if response is None:raise RuntimeError('Die FRITZ!Box hat den Auftrag nicht bestätigt.')
        return fields(response)
    def hosts(self):
        if not self.control:self.discover()
        if 'X_AVM-DE_GetHostListPath' in self.actions:
            try:
                result=self.call('X_AVM-DE_GetHostListPath');path=result.get('NewX_AVM-DE_HostListPath','')
                doc=self.request('GET',safe_path(path));return [host_record(fields(n)) for n in doc.iter() if n.tag.split('}')[-1]=='Item']
            except FritzFault as e:
                if e.code not in ('401','606'):raise
        result=self.call('GetHostNumberOfEntries');count=int(result.get('NewHostNumberOfEntries',result.get('HostNumberOfEntries','0')))
        if not 0<=count<=2048:raise RuntimeError('Die FRITZ!Box meldet eine ungültige Anzahl Netzwerkgeräte.')
        return [host_record(self.call('GetGenericHostEntry',{'NewIndex':i})) for i in range(count)]
    def host(self,address):
        address=mac(address)
        if not address:raise ValueError('Ungültige MAC-Adresse.')
        result=self.call('GetSpecificHostEntry',{'NewMACAddress':address})
        returned=result.get('NewMACAddress',address)
        if mac(returned)!=address:raise RuntimeError('Der FRITZ!Box-Eintrag gehört zu einer anderen MAC-Adresse. Es wurde nichts geändert.')
        result['NewMACAddress']=address;return host_record(result)
    def set_hostname(self,address,name):
        name=hostname(name);address=mac(address)
        if not address:raise ValueError('Ungültige MAC-Adresse.')
        return self.call('X_AVM-DE_SetHostNameByMACAddress',{'NewMACAddress':address,'NewHostName':name})
    def close(self):self.session.close()
class FritzAccount:
    def __init__(self,vault=None):self.vault=vault or Vault(data_dir()/'fritzbox');self.config=None;self.client=None;self.hosts=[];self.bindings={};self.remember=False
    def connect(self,config,remember=True):
        config=copy.deepcopy(config);candidate=FritzClient(config)
        try:hosts=candidate.hosts()
        except Exception:candidate.close();raise
        if self.config and self.config.get('address')==config.get('address'):config['bindings']=copy.deepcopy(self.bindings)
        try:
            if remember:self.vault.save(config)
            else:self.vault.clear()
        except Exception:candidate.close();raise
        old=self.client;self.client=candidate;self.config=config;self.bindings=config.get('bindings',{});self.hosts=hosts;self.remember=remember
        if old:old.close()
        return len(hosts)
    def restore(self):
        cfg=self.vault.load()
        if not cfg:return False
        self.connect(cfg,True);return True
    def refresh(self):
        if not self.client:raise RuntimeError('Bitte zuerst bei der FRITZ!Box anmelden.')
        try:self.hosts=self.client.hosts()
        except Exception:self.hosts=[];raise
        return len(self.hosts)
    def match(self,device):
        if device.get('sub'):return None
        address=mac(self.bindings.get(device['id']) or device.get('mac'))
        if not address:return None
        primary=[h for h in self.hosts if h['mac']==address];matches=primary or [h for h in self.hosts if address in h.get('aliases',[])]
        if len(matches)!=1:return None
        host=matches[0];ip=host['ip'] if host['active'] else ''
        if ip and any(h['active'] and h['ip']==ip and h['mac']!=host['mac'] for h in self.hosts):ip=''
        return dict(host,ip=ip,manual=device['id'] in self.bindings)
    def refresh_device(self,device):
        old=self.match(device)
        if not self.client or not old:return False
        try:fresh=self.client.host(old['mac'])
        except Exception:
            self.hosts=[h for h in self.hosts if h['mac']!=old['mac']];raise
        self.hosts=[fresh if h['mac']==old['mac'] else h for h in self.hosts];return True
    def rename_hostname(self,device,name,expected_mac=None):
        name=hostname(name)
        if not self.client:raise RuntimeError('Bitte zuerst bei der FRITZ!Box anmelden.')
        selected=self.match(device)
        if not selected:raise ValueError('Für dieses Gerät ist kein eindeutiger FRITZ!Box-Eintrag zugeordnet.')
        address=selected['mac']
        if expected_mac and mac(expected_mac)!=address:raise RuntimeError('Die Netzwerkzuordnung hat sich geändert. Bitte den Gerätedialog erneut öffnen.')
        before=self.client.host(address)
        if mac(before.get('mac'))!=address:raise RuntimeError('Die MAC-Adresse wurde nicht bestätigt. Es wurde nichts geändert.')
        self.client.set_hostname(address,name)
        try:after=self.client.host(address)
        except Exception as e:raise RuntimeError('FRITZ!Box hat die Änderung angenommen, aber der Hostname konnte nicht zurückgelesen werden. '+str(e)) from e
        if mac(after.get('mac'))!=address:raise RuntimeError('Die Rückmeldung gehört zu einer anderen MAC-Adresse. Der neue Hostname ist nicht bestätigt.')
        self.hosts=[copy.deepcopy(after) if h['mac']==address else h for h in self.hosts]
        if after['hostname'].casefold()!=name.casefold():raise RuntimeError('FRITZ!Box hat den gewünschten Hostnamen beim Rücklesen nicht bestätigt. Der tatsächlich gemeldete Name wurde in der Liste aktualisiert.')
        return copy.deepcopy(after)
    def bind(self,did,address):
        address=mac(address)
        if not address or sum(h['mac']==address for h in self.hosts)!=1:raise ValueError('Bitte einen eindeutigen FRITZ!Box-Eintrag auswählen.')
        cfg=copy.deepcopy(self.config);bindings=dict(self.bindings);bindings[did]=address;cfg['bindings']=bindings
        if self.remember:self.vault.save(cfg)
        self.config=cfg;self.bindings=bindings;return True
    def clear(self):
        self.vault.clear()
        if self.client:self.client.close()
        self.config=None;self.client=None;self.hosts=[];self.bindings={};self.remember=False


def hostname(value):
    value=str(value).strip()
    if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?',value):raise ValueError('Hostname: 1 bis 63 Buchstaben oder Zahlen, innen auch Bindestriche. Keine Leerzeichen, Umlaute oder Punkte. Beispiel: tv-hintergrund.')
    return value
