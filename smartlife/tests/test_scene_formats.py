import sys,json,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
from desktop_scenes import scene_rows,condition_rows,precondition_rows,scene_report
from core import label,enum_label
from project_cloud import DirectCloud
from demo import sample
class SceneFormatTests(unittest.TestCase):
 def setUp(self):self.devices=sample()['devices']
 def test_reported_button_names_are_german(self):
  self.assertEqual(label('switch_type_1',{'name':'开关1'}),'Tastenereignis 1')
  self.assertEqual(label('switch_type_2',{'name':'开关2'}),'Tastenereignis 2')
  self.assertEqual(enum_label('single_click'),'Einfacher Tastendruck')
 def test_json_properties_resolve_device_and_value(self):
  rows=scene_rows({'actions':[{'entity_id':'s','action_executor':'dpIssue','executor_property':json.dumps({'switch':False})}]},self.devices)
  self.assertEqual(rows[0][:3],('Steckdose Stehlampe','Ein/Aus','Aus'));self.assertEqual(rows[0][3]['value'],False)
 def test_numeric_dp_uses_only_device_model(self):
  self.devices[1]['functions']['switch']['dp_id']=1
  rows=scene_rows({'actions':[{'entity_id':'s','action_executor':'dpIssue','executor_property':{'1':True}}]},self.devices)
  self.assertEqual(rows[0][3],{'device':'s','code':'switch','value':True})
 def test_unknown_executor_is_not_converted_into_device_command(self):
  rows=scene_rows({'actions':[{'entity_id':'s','action_executor':'lightBase','executor_property':{'switch':True}}]},self.devices)
  self.assertIsNone(rows[0][3])
 def test_wrapped_original_keeps_meaningful_columns(self):
  raw={'entity_id':'s','action_executor':'dpIssue','executor_property':{'switch':True}}
  rows=scene_rows({'actions':[{'_raw':raw}]},self.devices)
  self.assertEqual(rows[0][:3],('Steckdose Stehlampe','Ein/Aus','Ein'));self.assertIsNone(rows[0][3])
 def test_power_condition_preserves_scale_comparison_and_action(self):
  d=self.devices[1];d['ranges']['cur_power']={'code':'cur_power','values':{'scale':1,'unit':'W'}}
  rule={'conditions':[{'entity_id':'s','entity_type':1,'display':{'code':'cur_power','operator':'>','value':100}}]}
  rows=condition_rows(rule,self.devices)
  self.assertEqual(rows,[('Steckdose Stehlampe','Leistungsaufnahme','ist größer als 10,0 W')])
 def test_delay_is_not_displayed_as_device(self):
  rows=scene_rows({'actions':[{'action_executor':'delay','executor_property':{'seconds':'5'}}]},self.devices)
  self.assertEqual(rows[0][:3],('Wartezeit','Verzögerung','5 Sekunden'))
 def test_preconditions_are_readable(self):
  rows=precondition_rows({'preconditions':[{'cond_type':'timeCheck','display':{'start':'10:00','end':'20:00','loops':'0111110'}}]})
  self.assertIn('Montag',rows[0]);self.assertNotIn('Sonntag',rows[0])
 def test_report_does_not_export_credentials(self):
  r=scene_report({'id':'test','home':'demo','actions':[{'secret':'bad','executor_property':'{"access_token":"bad","switch":true}'}]},self.devices)
  text=json.dumps(r);self.assertNotIn('bad',text);self.assertNotIn('local_key',text)
 def test_new_scene_api_with_legacy_fallback(self):
  calls=[]
  class Api:
   def request(self,method,path):
    calls.append(path)
    if '/v1.1/' in path:raise RuntimeError('Nicht freigeschaltet')
    return []
  d=DirectCloud({},Api());self.assertEqual(d.read_scenes('home'),[])
  self.assertEqual(calls,['/v1.1/homes/home/scenes','/v1.0/homes/home/scenes'])
 def test_load_automation_retains_condition_and_action(self):
  rule={'automation_id':'tv','name':'TV-Licht','enabled':True,'match_type':1,'conditions':[{'entity_id':'s','display':{'code':'cur_power','operator':'>','value':100}}],'actions':[{'entity_id':'light','action_executor':'dpIssue','executor_property':{'switch_led':True}}]}
  class Api:
   def request(self,method,path):
    if path=='/v1.0/users/user/homes':return [{'home_id':'demo','name':'Haus'}]
    if path=='/v1.1/homes/demo/automations':return [rule]
    return []
  direct=DirectCloud({'uid':'user'},Api());result=direct.load();loaded=result['automations'][0]
  self.assertEqual(loaded['conditions'],rule['conditions']);self.assertEqual(loaded['actions'],rule['actions']);self.assertEqual(result['automation_errors'],[])
if __name__=='__main__':unittest.main()
