"""Own desktop scenes. Never writes to or impersonates Smart Life cloud scenes."""
from __future__ import annotations
import copy,json,os,time,uuid
from pathlib import Path
from core import data_dir,validate,label,fmt

class SceneStore:
    def __init__(self,folder=None):self.path=(Path(folder) if folder else data_dir())/'desktop-szenen.json'
    def all(self):
        if not self.path.exists():return []
        try:
            value=json.loads(self.path.read_text('utf-8'))
            if value.get('schema')!=1 or not isinstance(value.get('scenes'),list):raise ValueError()
            return value['scenes']
        except (ValueError,OSError,TypeError) as e:raise RuntimeError('Gespeicherte Desktop-Szenen konnten nicht gelesen werden. Die Datei wurde nicht verändert.') from e
    def save(self,name,home,actions,devices,scene_id=None):
        name=name.strip()
        if not name or len(name)>120:raise ValueError('Bitte einen Szenennamen mit 1 bis 120 Zeichen eingeben.')
        if not actions:raise ValueError('Bitte mindestens eine Geräteaktion hinzufügen.')
        if len(actions)>200:raise ValueError('Eine Szene darf höchstens 200 Aktionen enthalten.')
        device_map={d['id']:d for d in devices if d['home']==home}
        for a in actions:
            d=device_map.get(a['device'])
            if not d or a['code'] not in d['functions']:raise ValueError('Ein Gerät oder eine Gerätefunktion ist nicht mehr verfügbar.')
            validate(d['functions'][a['code']],a['value'])
        scenes=self.all()
        if scene_id and not any(s['id']==scene_id for s in scenes):raise ValueError('Diese Desktop-Szene ist nicht mehr vorhanden.')
        scene={'id':scene_id or 'desktop:'+uuid.uuid4().hex,'name':name,'home':home,'actions':copy.deepcopy(actions),'enabled':True,'source':'desktop'}
        scenes=[s for s in scenes if s['id']!=scene['id']]+[scene]
        self.path.parent.mkdir(parents=True,exist_ok=True)
        temp=self.path.with_suffix('.tmp');temp.write_text(json.dumps({'schema':1,'scenes':scenes},ensure_ascii=False,indent=2),encoding='utf-8');os.replace(temp,self.path)
        return scene
    def delete(self,scene_id):
        scenes=self.all();remaining=[s for s in scenes if s['id']!=scene_id]
        self.path.parent.mkdir(parents=True,exist_ok=True);temp=self.path.with_suffix('.tmp');temp.write_text(json.dumps({'schema':1,'scenes':remaining},ensure_ascii=False,indent=2),encoding='utf-8');os.replace(temp,self.path)

def execute(scene,cloud):
    # Validate the entire plan first to avoid avoidable partial execution.
    devices={d['id']:d for d in cloud.devices}
    for a in scene['actions']:
        d=devices.get(a['device'])
        if not d or d['home']!=scene['home'] or not d['online']:raise RuntimeError('Szene wurde nicht gestartet: Mindestens ein Gerät ist nicht erreichbar.')
        if a['code'] not in d['functions']:raise RuntimeError('Szene wurde nicht gestartet: Eine Gerätefunktion ist nicht mehr verfügbar.')
        validate(d['functions'][a['code']],a['value'])
    completed=0
    for a in scene['actions']:
        try:cloud.command(a['device'],a['code'],a['value']);completed+=1
        except Exception as e:raise RuntimeError(f'Szene nach {completed} von {len(scene["actions"])} Aktionen abgebrochen. Bereits ausgeführte Aktionen bleiben wirksam. {e}') from e
    return completed

def scene_rows(scene,devices):
    """Render only actual supplied actions; unsupported actions remain visible."""
    device_map={d['id']:d for d in devices};rows=[]
    for action in scene.get('actions',[]):
        if not isinstance(action,dict):rows.append(('Weitere Aktion','Unbekannter Aktionstyp','Keine Zuordnung möglich',None));continue
        dev_id=action.get('device') or action.get('device_id') or action.get('devId') or action.get('entityId') or action.get('entity_id')
        d=device_map.get(str(dev_id));name=d['name'] if d else action.get('entityName') or action.get('name') or 'Nicht zugeordnetes Gerät'
        pairs=[]
        if 'code' in action and 'value' in action:pairs=[(str(action['code']),action['value'])]
        elif isinstance(action.get('commands'),list):pairs=[(str(x['code']),x['value']) for x in action['commands'] if isinstance(x,dict) and 'code' in x and 'value' in x]
        else:
            props=action.get('executorProperty') or action.get('executor_property') or {}
            if isinstance(props,dict):pairs=list(props.items())
        if not pairs:rows.append((str(name),'Weitere Szenenaktion','Details nicht als Gerätebefehl bereitgestellt',None));continue
        for code,value in pairs:
            spec=(d['functions'].get(code) or d['ranges'].get(code)) if d else None
            mapped={'device':d['id'],'code':code,'value':value} if d and code in d['functions'] else None
            if code.isdigit():
                # Do not guess numeric DP meaning or make an executable copy.
                title='Gerätedatenpunkt '+code
            else:title=label(code,spec)
            rows.append((str(name),title,fmt(value,spec),mapped))
    return rows
