"""Authenticated Tuya project API; never uses the limited sharing app identity.
Protocol references: Tuya openapi.py, User Permission Package, Smart Home APIs.
"""
from __future__ import annotations
import copy,hashlib,hmac,json,re,time,threading
from urllib.parse import quote,urlencode
import requests
from core import Vault,data_dir,validate,meta

ENDPOINTS={'Central Europe':'https://openapi.tuyaeu.com','Western Europe':'https://openapi-weaz.tuyaeu.com',
 'Western America':'https://openapi.tuyaus.com','Eastern America':'https://openapi-ueaz.tuyaus.com',
 'China':'https://openapi.tuyacn.com','India':'https://openapi.tuyain.com','Singapore':'https://openapi-sg.iotbing.com'}

def part(value):
    if not str(value):raise ValueError('Eine erforderliche Geräte-, Raum- oder Zuhause-Kennung fehlt.')
    return quote(str(value),safe='')

def items(value,*keys):
    if isinstance(value,list):return value
    if isinstance(value,dict):
        for key in keys:
            if isinstance(value.get(key),list):return value[key]
    raise ValueError('Tuya liefert eine unerwartete Listenstruktur. Die Daten wurden nicht verändert.')

class ProjectAPI:
    def __init__(self,config,session=None):
        self.client=config['access_id'].strip();self.secret=config['access_secret'].strip();self.uid=config['uid'].strip();self.region=config['region']
        if self.region not in ENDPOINTS:raise ValueError('Bitte das Datenzentrum auswählen.')
        if not self.client or not self.secret or not self.uid:raise ValueError('Access ID, Access Secret und UID sind erforderlich.')
        self.endpoint=ENDPOINTS[self.region];self.session=session or requests.Session();self.token='';self.expires=0
    def _send(self,method,path,params=None,body=None,token=True):
        params=params or {};query=urlencode(sorted(params.items()));url_path=path+('?' + query if query else '')
        raw=json.dumps(body,ensure_ascii=False,separators=(',',':')).encode('utf-8') if body is not None else b''
        stamp=str(int(time.time()*1000));access=self.token if token else ''
        canonical=method+'\n'+hashlib.sha256(raw).hexdigest()+'\n\n'+url_path
        signature=hmac.new(self.secret.encode(),(self.client+access+stamp+canonical).encode(),hashlib.sha256).hexdigest().upper()
        headers={'client_id':self.client,'sign':signature,'sign_method':'HMAC-SHA256','t':stamp,'lang':'de','Content-Type':'application/json'}
        if access:headers['access_token']=access
        try:
            r=self.session.request(method,self.endpoint+url_path,data=raw if body is not None else None,headers=headers,timeout=20,allow_redirects=False)
            if 300<=r.status_code<400:raise RuntimeError('Unerwartete Weiterleitung von Tuya. Anfrage abgebrochen.')
            r.raise_for_status();reply=r.json()
        except requests.Timeout as e:raise RuntimeError('Zeitüberschreitung bei Tuya. Bei einem Schreibvorgang bitte zuerst neu laden und den tatsächlichen Stand prüfen.') from e
        except requests.RequestException as e:raise RuntimeError('Die Tuya-Cloud ist nicht erreichbar. Bitte Internetverbindung und Datenzentrum prüfen.') from e
        if not isinstance(reply,dict) or not reply.get('success'):
            code=str(reply.get('code','unbekannt')) if isinstance(reply,dict) else 'unbekannt'
            tips={'1004':'Access ID oder Access Secret ist falsch; auch die Systemzeit prüfen.',
             '1106':'Zugriff verweigert. Kontoverknüpfung, Datenzentrum und API-Berechtigung prüfen.',
             '1010':'Die Anmeldung ist ungültig. Bitte erneut verbinden.',
             '28841105':'Der benötigte API-Dienst ist für dieses Projekt nicht freigeschaltet.',
             '60001001':'Das Tuya-Kontingent für steuerbare Geräte reicht nicht aus. Das Geräte-Kontingent im Tuya-Cloud-Projekt prüfen.'}
            message=tips.get(code,'Die Anfrage wurde von Tuya abgelehnt.')
            raise RuntimeError('Tuya-Fehler '+code+': '+message)
        return reply
    def connect(self):
        reply=self._send('GET','/v1.0/token',{'grant_type':1},token=False);result=reply.get('result',{})
        if not result.get('access_token'):raise RuntimeError('Tuya hat keinen gültigen Zugangstoken geliefert.')
        self.token=result['access_token'];self.expires=time.monotonic()+int(result.get('expire_time',result.get('expire',3600)))-60
    def request(self,method,path,params=None,body=None):
        if not self.token or time.monotonic()>=self.expires:self.connect()
        # Mutations are never retried automatically: a timeout can mean success.
        return self._send(method,path,params,body).get('result')
    def close(self):self.session.close();self.token=''

class DirectCloud:
    def __init__(self,config,api=None):
        self.config=copy.deepcopy(config);self.api=api or ProjectAPI(config);self.homes=[];self.rooms=[];self.devices=[];self.scenes=[];self.spec_cache={};self.warnings=[];self.automations=[];self.background_pause=threading.Event();self.name_checked=set();self.mac_attempted=set()
    def verify(self):
        self.api.connect();homes=items(self.api.request('GET',f'/v1.0/users/{part(self.config["uid"])}/homes'),'homes')
        if not homes:raise RuntimeError('Die Anmeldung funktioniert, aber für diese UID werden keine Zuhause geliefert. UID und App-Verknüpfung prüfen.')
        return len(homes)
    def load(self):
        homes=items(self.api.request('GET',f'/v1.0/users/{part(self.config["uid"])}/homes'),'homes')
        hs=[];rs=[];ds=[];ss=[];automations=[];automation_errors=[];warnings=[]
        for h in homes:
            hid=str(h.get('home_id',h.get('id','')));part(hid);hs.append({'id':hid,'name':h.get('name','Zuhause')})
            room_list=items(self.api.request('GET',f'/v1.0/homes/{part(hid)}/rooms'),'rooms')
            room_map={}
            for room in room_list:
                rid=str(room.get('room_id',room.get('id','')));part(rid);name=room.get('name','Raum');rs.append({'id':rid,'name':name,'home':hid})
                for d in items(self.api.request('GET',f'/v1.0/homes/{part(hid)}/rooms/{part(rid)}/devices'),'devices'):
                    room_map[str(d.get('id',d.get('device_id','')))]=(rid,name)
            for item in items(self.api.request('GET',f'/v1.0/homes/{part(hid)}/devices'),'devices'):
                did=str(item.get('id',item.get('device_id','')));part(did);rid,name=room_map.get(did,('',''))
                device={'id':did,'home':hid,'name':item.get('name','Gerät'),'room_id':rid,'room':name,'room_order':0,
                 'category':item.get('category',''),'product_id':item.get('product_id',''),'product_name':item.get('product_name',''),
                 'mac':item.get('mac','') or '', 'online':bool(item.get('online',False)),'ip':item.get('ip','') or '','sub':bool(item.get('sub',False)),
                 'status':normalize_status(item.get('status',[])),'functions':{},'ranges':{},'raw_control':False}
                if did in self.name_checked:
                    try:
                        detail=self.api.request('GET',f'/v1.0/devices/{part(did)}')
                        if not isinstance(detail,dict) or not isinstance(detail.get('name'),str):raise ValueError('Gerätename fehlt in den Gerätedetails.')
                        device['name']=detail['name']
                    except Exception as e:warnings.append(device['name']+': Name konnte nicht bestätigt werden ('+str(e)+')')
                if did not in self.spec_cache:
                    try:
                        model=self.api.request('GET',f'/v2.0/cloud/thing/{part(did)}/model');functions,ranges=parse_model(model)
                        self.spec_cache[did]=(functions,ranges,True)
                    except Exception as raw_error:
                        try:
                            spec=self.api.request('GET',f'/v1.0/devices/{part(did)}/specifications') or {}
                            functions={x['code']:x for x in spec.get('functions',[])};ranges={x['code']:x for x in spec.get('status',[])}
                            self.spec_cache[did]=(functions,ranges,False)
                        except Exception as e:warnings.append(device['name']+': Funktionsabfrage fehlgeschlagen ('+str(e)+')')
                if did in self.spec_cache:device['functions'],device['ranges'],device['raw_control']=copy.deepcopy(self.spec_cache[did])
                try:device['status']=self.read_status(device)
                except Exception as e:warnings.append(device['name']+': Status nicht aktuell ('+str(e)+')')
                ds.append(device)
            try:
                scenes=self.read_scenes(hid)
                for s in scenes:
                    sid=str(s.get('scene_id',s.get('id','')))
                    ss.append({'id':sid,'name':s.get('name','Szene'),'home':hid,'enabled':s.get('enabled',True),'source':'project',
                               'actions':copy.deepcopy(s.get('actions',[])),'original':copy.deepcopy(s)})
            except Exception as e:warnings.append('Szenen: '+str(e))
            try:
                for rule in items(self.api.request('GET',f'/v1.1/homes/{part(hid)}/automations'),'automations'):
                    aid=str(rule.get('automation_id',rule.get('id','')));part(aid)
                    try:rule=self.get_automation(hid,aid)
                    except (ValueError,RuntimeError) as e:
                        if not rule.get('conditions'):warnings.append(rule.get('name','Automation')+': '+str(e))
                    automations.append({'id':aid,'name':rule.get('name','Automation'),'home':hid,'source':'automation',
                        'enabled':rule.get('enabled'),'conditions':copy.deepcopy(rule.get('conditions',[])),
                        'actions':copy.deepcopy(rule.get('actions',[])),'match_type':rule.get('match_type'),'condition_rule':rule.get('condition_rule'),
                        'preconditions':copy.deepcopy(rule.get('preconditions',[])),'original':copy.deepcopy(rule)})
            except Exception as e:
                message='Automationen konnten nicht vollständig geladen werden: '+str(e);automation_errors.append(message);warnings.append(message)
        self.homes,self.rooms,self.devices,self.scenes,self.warnings=hs,rs,ds,ss,warnings;self.automations=automations
        return {'homes':hs,'rooms':rs,'devices':copy.deepcopy(ds),'scenes':ss,'automations':automations,'automation_errors':automation_errors,'room_failed':0,'scene_error':False,'warnings':warnings,'direct':True}
    def network_macs(self,device_ids=None):
        from fritz import mac
        allowed={d['id']:d for d in self.devices if not d.get('sub')};requested=set(device_ids) if device_ids is not None else set(allowed)
        ids=[did for did in allowed if did in requested and not mac(allowed[did].get('mac')) and did not in self.mac_attempted];warnings=[]
        for start in range(0,len(ids),20):
            batch=ids[start:start+20]
            try:
                rows=items(self.api.request('GET','/v1.0/devices/factory-infos',params={'device_ids':','.join(batch)}),'devices')
                for row in rows:
                    did=str(row.get('id',''));value=mac(row.get('mac'))
                    if did in batch and value:allowed[did]['mac']=value
                self.mac_attempted.update(batch)
            except Exception as e:warnings.append('Tuya-MAC-Adressen konnten nicht vollständig gelesen werden: '+str(e));self.mac_attempted.update(batch)
        return {'macs':{did:mac(d.get('mac')) for did,d in allowed.items() if did in requested and mac(d.get('mac'))},'warnings':warnings}
    def read_scenes(self,home):
        try:return items(self.api.request('GET',f'/v1.1/homes/{part(home)}/scenes'),'scenes')
        except RuntimeError:return items(self.api.request('GET',f'/v1.0/homes/{part(home)}/scenes'),'scenes')
    def read_status(self,d):
        if d.get('raw_control'):
            r=self.api.request('GET',f'/v2.0/cloud/thing/{part(d["id"])}/shadow/properties')
            return normalize_status(r.get('properties',r) if isinstance(r,dict) else r)
        return normalize_status(self.api.request('GET',f'/v1.0/devices/{part(d["id"])}/status'))
    def refresh(self,device_id=None):
        for d in self.devices:
            if device_id is None and self.background_pause.is_set():break
            if device_id is None or d['id']==device_id:d['status']=self.read_status(d)
        return copy.deepcopy(self.devices)
    def command(self,did,code,value):
        d=next((d for d in self.devices if d['id']==did),None)
        if not d:raise ValueError('Gerät ist nicht im geladenen Konto vorhanden.')
        if not d['online']:raise RuntimeError('Gerät wird als nicht erreichbar gemeldet.')
        if code not in d['functions']:raise ValueError('Diese Funktion ist nicht schreibbar.')
        validate(d['functions'][code],value)
        if d.get('raw_control'):
            result=self.api.request('POST',f'/v2.0/cloud/thing/{part(did)}/shadow/properties/issue',body={'properties':json.dumps({code:value},ensure_ascii=False,separators=(',',':'))})
        else:result=self.api.request('POST',f'/v1.0/devices/{part(did)}/commands',body={'commands':[{'code':code,'value':value}]})
        if result is False or result is None:raise RuntimeError('Tuya hat den Gerätebefehl nicht bestätigt. Bitte den tatsächlichen Zustand neu laden.')
        return True
    def rename_device(self,did,name):
        if not any(d['id']==did for d in self.devices):raise ValueError('Unbekanntes Gerät.')
        name=checked_name(name);self._write('PUT',f'/v1.0/devices/{part(did)}',{'name':name});return True
    def rename_and_refresh(self,did,name):
        name=checked_name(name)
        try:self.rename_device(did,name)
        except Exception as e:raise RuntimeError('Gerätename konnte nicht gespeichert werden. '+str(e)) from e
        try:return self.refresh_changed_device(did,expected_name=name)
        except Exception as e:raise RuntimeError('Tuya hat die Umbenennung angenommen, aber das Rücklesen ist fehlgeschlagen. '+str(e)) from e
    def move_and_refresh(self,did,room):
        self.move_device(did,room)
        return self.refresh_changed_device(did,target_room=room)
    def refresh_changed_device(self,did,expected_name=None,target_room=None):
        device=next((d for d in self.devices if d['id']==did),None)
        if not device:raise ValueError('Unbekanntes Gerät.')
        record=None
        for attempt in range(3):
            record=self.api.request('GET',f'/v1.0/devices/{part(did)}')
            if not isinstance(record,dict) or str(record.get('id',did))!=did:raise RuntimeError('Die Cloud hat keine passenden Gerätedetails zurückgegeben.')
            if isinstance(record.get('name'),str) and record['name'] and (expected_name is None or record['name']==expected_name):break
            if attempt<2:time.sleep(.2)
        else:raise RuntimeError('Der neue Gerätename wurde beim Rücklesen von Tuya nicht bestätigt. Die Anzeige wurde nicht als erfolgreich geändert.')
        fresh=copy.deepcopy(device);fresh['name']=record['name'];warnings=[]
        for key in ('online','ip','sub'):
            if key in record:fresh[key]=record[key]
        if target_room:
            members=items(self.api.request('GET',f'/v1.0/homes/{part(device["home"])}/rooms/{part(target_room)}/devices'),'devices')
            if not any(str(x.get('id',x.get('device_id','')))==did for x in members):raise RuntimeError('Die neue Raumzuordnung wurde beim Rücklesen nicht bestätigt.')
            room=next(r for r in self.rooms if r['id']==target_room and r['home']==device['home']);fresh['room_id']=room['id'];fresh['room']=room['name']
        elif device.get('room_id'):
            try:
                members=items(self.api.request('GET',f'/v1.0/homes/{part(device["home"])}/rooms/{part(device["room_id"])}/devices'),'devices')
                if not any(str(x.get('id',x.get('device_id','')))==did for x in members):warnings.append('Die bisherige Raumzuordnung wird von der Cloud nicht mehr bestätigt.')
            except Exception as e:warnings.append('Gerätename bestätigt; Raumzuordnung konnte nicht nachgelesen werden: '+str(e))
        try:fresh['status']=self.read_status(fresh)
        except Exception as e:warnings.append('Gerätename bestätigt; Status nicht aktuell: '+str(e))
        device.update(fresh);self.name_checked.add(did);updated=[]
        for automation in self.automations:
            if automation['home']!=device['home'] or not references_device(automation.get('original',automation),did):continue
            try:
                raw=self.get_automation(automation['home'],automation['id'])
                for key in ('name','enabled','conditions','actions','match_type','condition_rule','preconditions'):
                    if key in raw:automation[key]=copy.deepcopy(raw[key])
                automation['original']=copy.deepcopy(raw);updated.append(copy.deepcopy(automation))
            except Exception as e:warnings.append('Gerätename bestätigt; zugehörige Automation „'+automation['name']+'“ konnte nicht nachgelesen werden: '+str(e))
        return {'device':copy.deepcopy(device),'automations':updated,'warnings':warnings}
    def add_room(self,home,name):
        self._home(home);return self._write('POST',f'/v1.0/homes/{part(home)}/room',{'name':checked_name(name)})
    def rename_room(self,home,room,name):
        self._room(home,room);return self._write('PUT',f'/v1.0/homes/{part(home)}/rooms/{part(room)}',{'name':checked_name(name)})
    def delete_room(self,home,room):
        self._room(home,room)
        # Refuse nonempty rooms; avoids accidental device/group disassociation.
        current=items(self.api.request('GET',f'/v1.0/homes/{part(home)}/rooms/{part(room)}/devices'),'devices')
        if current:raise ValueError('Dieser Raum enthält noch Geräte. Bitte die Geräte zuerst in andere Räume verschieben.')
        return self._write('DELETE',f'/v1.0/homes/{part(home)}/rooms/{part(room)}')
    def move_device(self,did,room):
        d=next((d for d in self.devices if d['id']==did),None)
        if not d:raise ValueError('Unbekanntes Gerät.')
        self._room(d['home'],room)
        # Add the one device, never replace the room's whole device list.
        self._write('POST',f'/v1.0/homes/{part(d["home"])}/rooms/{part(room)}/devices',{'device_ids':[did]})
        old=d.get('room_id')
        if old and old!=room:
            members=items(self.api.request('GET',f'/v1.0/homes/{part(d["home"])}/rooms/{part(old)}/devices'),'devices')
            if any(str(x.get('id',x.get('device_id','')))==did for x in members):
                try:self._write('DELETE',f'/v1.0/homes/{part(d["home"])}/rooms/{part(old)}/devices',{'device_ids':[did]})
                except Exception as e:raise RuntimeError('Die Zielzuordnung wurde gespeichert; die bisherige Zuordnung konnte nicht entfernt werden. Bitte neu laden. '+str(e)) from e
        return True
    def _home(self,home):
        if not any(h['id']==home for h in self.homes):raise ValueError('Unbekanntes Zuhause.')
    def _room(self,home,room):
        self._home(home)
        if not any(r['id']==room and r['home']==home for r in self.rooms):raise ValueError('Raum gehört nicht zum ausgewählten Zuhause.')
    def _write(self,method,path,body=None):
        result=self.api.request(method,path,body=body)
        if result is False or result is None:raise RuntimeError('Tuya hat die Änderung nicht bestätigt. Bitte neu laden und den tatsächlichen Stand prüfen.')
        return result
    def trigger(self,home,sid):self._home(home);return self._write('POST',f'/v1.0/homes/{part(home)}/scenes/{part(sid)}/trigger',{})
    def save_scene(self,name,home,actions,original=None):
        self._home(home);name=checked_name(name)
        if original and not isinstance(original.get('actions'),list):raise ValueError('Die vollständigen Originalaktionen wurden nicht geliefert. Die Szene wird nicht überschrieben.')
        if not actions:raise ValueError('Mindestens eine Aktion ist erforderlich.')
        device_map={d['id']:d for d in self.devices if d['home']==home};cloud_actions=[]
        if original:
            sid=str(original.get('scene_id',original.get('id','')))
            latest=next((x for x in self.read_scenes(home) if str(x.get('scene_id',x.get('id','')))==sid),None)
            if not latest or any(latest.get(k)!=original.get(k) for k in ('name','actions','background')):raise RuntimeError('Die Szene wurde inzwischen geändert oder entfernt. Bitte neu laden, bevor du Änderungen speicherst.')
        for a in actions:
            if '_raw' in a:
                if not original or a['_raw'] not in original.get('actions',[]):raise ValueError('Eine unveränderte Originalaktion konnte nicht zugeordnet werden.')
                cloud_actions.append(copy.deepcopy(a['_raw']));continue
            d=device_map.get(a['device'])
            if not d or a['code'] not in d['functions']:raise ValueError('Eine Geräteaktion ist nicht mehr verfügbar.')
            validate(d['functions'][a['code']],a['value'])
            cloud_actions.append({'entity_id':a['device'],'action_executor':'dpIssue','executor_property':{a['code']:a['value']}})
        background=(original or {}).get('background')
        if not background:
            pictures=self.api.request('GET','/v1.0/scenes/default-pictures')
            pool=pictures.get('pictures',[]) if isinstance(pictures,dict) else pictures
            if isinstance(pool,list) and pool:
                first=pool[0];background=first if isinstance(first,str) else first.get('url',first.get('background'))
        if not background:raise RuntimeError('Tuya hat kein erforderliches Szenenhintergrundbild geliefert. Es wurde nichts gespeichert.')
        body={'name':name,'background':background,'actions':cloud_actions}
        if original:
            sid=str(original.get('scene_id',original.get('id','')));part(sid)
            result=self._write('PUT',f'/v1.0/homes/{part(home)}/scenes/{part(sid)}',body)
        else:
            sid=str(self._write('POST',f'/v1.0/homes/{part(home)}/scenes',body))
        return {'id':sid,'home':home,'name':name,'enabled':True,'source':'project','actions':cloud_actions,'original':dict(body,scene_id=sid)}
    def get_automation(self,home,aid):
        result=self.api.request('GET',f'/v1.0/homes/{part(home)}/automations/{part(aid)}')
        if isinstance(result,list):result=next((r for r in result if str(r.get('automation_id',r.get('id','')))==str(aid)),None)
        if not isinstance(result,dict):raise ValueError('Die Cloud hat keine vollständigen Automationsdetails geliefert.')
        returned=result.get('automation_id',result.get('id'))
        if returned is not None and str(returned)!=str(aid):raise ValueError('Die Cloudantwort gehört zu einer anderen Automation.')
        result=copy.deepcopy(result)
        for key in ('conditions','actions','preconditions'):
            if isinstance(result.get(key),str):
                try:result[key]=json.loads(result[key])
                except ValueError:raise ValueError('Die Cloud liefert unlesbare '+key+'.')
        if not isinstance(result.get('conditions'),list) or not result['conditions'] or not isinstance(result.get('actions'),list):
            raise ValueError('Die Cloudantwort enthält keine vollständigen Auslöser und Aktionen. Die bestehende Regel wird nicht überschrieben.')
        result['automation_id']=str(aid)
        return result
    def encode_actions(self,home,actions,original=None):
        if not actions:raise ValueError('Mindestens eine Geräteaktion ist erforderlich.')
        device_map={d['id']:d for d in self.devices if d['home']==home};out=[]
        for a in actions:
            if '_raw' in a:
                if not original or a['_raw'] not in original.get('actions',[]):raise ValueError('Eine Originalaktion ist nicht mehr zugeordnet.')
                out.append(copy.deepcopy(a['_raw']));continue
            d=device_map.get(a.get('device'));code=a.get('code')
            if not d or code not in d['functions']:raise ValueError('Eine Geräteaktion ist nicht mehr verfügbar.')
            validate(d['functions'][code],a['value'])
            out.append({'entity_id':d['id'],'action_executor':'dpIssue','executor_property':{code:a['value']}})
        return out
    def save_automation(self,home,name,conditions,actions,match_type,original=None,condition_rule=''):
        self._home(home);name=checked_name(name)
        if not conditions:raise ValueError('Mindestens eine Auslösebedingung ist erforderlich.')
        if match_type not in (1,2,3):raise ValueError('Ungültige Bedingungsverknüpfung.')
        if original:
            aid=str(original['automation_id']);latest=self.get_automation(home,aid)
            fields=('name','conditions','actions','match_type','condition_rule','preconditions','background','enabled')
            if any(latest.get(k)!=original.get(k) for k in fields):raise RuntimeError('Diese Automation wurde inzwischen geändert. Bitte neu laden; es wurde nichts überschrieben.')
        numbers=[];devices={d['id']:d for d in self.devices if d['home']==home}
        for c in conditions:
            number=c.get('order_num')
            if not isinstance(number,int) or number<1 or number in numbers:raise ValueError('Bedingungsnummern müssen eindeutig sein.')
            numbers.append(number)
            if original and c in original.get('conditions',[]):continue
            if c.get('entity_type')!=1:raise ValueError('Neue Bedingungen müssen eine gemeldete Gerätefunktion verwenden.')
            d=devices.get(str(c.get('entity_id')));display=c.get('display',{});code=display.get('code')
            spec=({**d['functions'],**d.get('ranges',{})}).get(code) if d else None
            if not spec:raise ValueError('Eine Bedingung verweist auf eine unbekannte Gerätefunktion.')
            validate(spec,display.get('value'))
            allowed=('==','>','<') if spec.get('type','').lower()=='integer' else ('==',)
            if display.get('operator') not in allowed:raise ValueError('Dieser Vergleich ist für die Gerätefunktion nicht zulässig.')
        if match_type==3:validate_condition_expression(condition_rule,numbers)
        encoded=self.encode_actions(home,actions,original)
        background=(original or {}).get('background')
        if not background:
            pictures=self.api.request('GET','/v1.0/scenes/default-pictures');pool=pictures.get('pictures',[]) if isinstance(pictures,dict) else pictures
            if isinstance(pool,list) and pool:
                first=pool[0];background=first if isinstance(first,str) else first.get('url',first.get('background'))
        if not background:raise RuntimeError('Die Cloud hat kein erforderliches Szenenbild geliefert. Es wurde nichts gespeichert.')
        body={'name':name,'background':background,'conditions':copy.deepcopy(conditions),'actions':encoded,'match_type':match_type}
        if original:
            for key in ('preconditions','timezone_id'):
                if key in original:body[key]=copy.deepcopy(original[key])
        if match_type==3:body['condition_rule']=condition_rule
        if original:self._write('PUT',f'/v1.0/homes/{part(home)}/automations/{part(aid)}',body)
        else:
            result=self._write('POST',f'/v1.0/homes/{part(home)}/automations',body)
            aid=str(result.get('automation_id',result.get('id',''))) if isinstance(result,dict) else str(result)
            part(aid)
        return {'id':aid,'home':home,'name':name,'source':'automation','conditions':conditions,'actions':encoded,'match_type':match_type}
    def close(self):self.api.close()

def checked_name(name):
    name=str(name).strip()
    if not name or len(name)>120 or any(ord(c)<32 for c in name):raise ValueError('Bitte einen Namen mit 1 bis 120 Zeichen eingeben.')
    return name

def normalize_status(raw):
    if isinstance(raw,dict):return copy.deepcopy(raw)
    if isinstance(raw,list):return {str(x['code']):x['value'] for x in raw if isinstance(x,dict) and 'code' in x and 'value' in x}
    raise ValueError('Tuya liefert keine auswertbaren Gerätewerte.')

def parse_model(result):
    model=result.get('model',result) if isinstance(result,dict) else result
    if isinstance(model,str):model=json.loads(model)
    if not isinstance(model,dict):raise ValueError('Ungültiges Gerätemodell.')
    ranges={};functions={}
    for service in model.get('services',[]):
        for p in service.get('properties',[]):
            code=p.get('code');spec=p.get('typeSpec',{})
            if not code or not isinstance(spec,dict):continue
            typ={'bool':'Boolean','value':'Integer','enum':'Enum','string':'String','json':'Json'}.get(spec.get('type'))
            if not typ:continue
            obj={'code':code,'name':p.get('name',code),'type':typ,'values':{k:v for k,v in spec.items() if k!='type'}}
            if p.get('abilityId',p.get('dpId',p.get('id'))) is not None:obj['dp_id']=p.get('abilityId',p.get('dpId',p.get('id')))
            ranges[code]=obj
            if p.get('accessMode') in ('rw','wr','write','readWrite'):functions[code]=copy.deepcopy(obj)
    if not ranges:raise ValueError('Tuya liefert keine Eigenschaften im Gerätemodell.')
    return functions,ranges


def validate_condition_expression(expression,numbers):
    tokens=re.findall(r'\d+|&&|\|\||[()]',expression)
    if ''.join(tokens)!=re.sub(r'\s+','',expression) or not tokens:raise ValueError('Die eigene Verknüpfung enthält ungültige Zeichen.')
    position=0
    def term():
        nonlocal position
        if position>=len(tokens):raise ValueError('Die Bedingungsverknüpfung ist unvollständig.')
        token=tokens[position];position+=1
        if token=='(':
            chain()
            if position>=len(tokens) or tokens[position]!=')':raise ValueError('Eine schließende Klammer fehlt.')
            position+=1
        elif not token.isdigit() or int(token) not in numbers:raise ValueError('Die Verknüpfung verweist auf eine nicht vorhandene Bedingung.')
    def chain():
        nonlocal position
        term()
        while position<len(tokens) and tokens[position] in ('&&','||'):position+=1;term()
    chain()
    if position!=len(tokens):raise ValueError('Die Bedingungsverknüpfung ist ungültig.')


def references_device(value,did):
    if isinstance(value,dict):return any(references_device(v,did) for v in value.values())
    if isinstance(value,list):return any(references_device(v,did) for v in value)
    if isinstance(value,str):
        if value==did:return True
        if value.startswith(('{','[')):
            try:return references_device(json.loads(value),did)
            except ValueError:pass
    return False
