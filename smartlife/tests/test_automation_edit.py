import sys,unittest,copy
from pathlib import Path
from unittest.mock import patch,Mock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
from project_cloud import DirectCloud,validate_condition_expression
from demo import sample
import updates
class AutomationTests(unittest.TestCase):
 def setUp(self):
  self.original={'automation_id':'rule','name':'TV-Licht','background':'picture','enabled':True,'match_type':1,'conditions':[{'entity_type':1,'entity_id':'s','order_num':1,'display':{'code':'switch','operator':'==','value':True}}],'actions':[{'entity_id':'s','action_executor':'dpIssue','executor_property':{'switch':False}}],'preconditions':[{'cond_type':'timeCheck','display':{'start':'10:00','end':'20:00','loops':'1111111','timezone_id':'Europe/Berlin'}}]}
  self.calls=[];outer=self
  class Api:
   def request(self,method,path,body=None):
    outer.calls.append((method,path,copy.deepcopy(body)))
    if method=='GET':return copy.deepcopy(outer.latest)
    return True
  self.latest=copy.deepcopy(self.original);self.cloud=DirectCloud({},Api());self.cloud.homes=[{'id':'demo'}];self.cloud.devices=sample()['devices'];self.actions=[{'device':'s','code':'switch','value':True}]
 def save(self,conditions=None,actions=None):return self.cloud.save_automation('demo','TV neu',conditions or self.original['conditions'],actions or self.actions,1,self.original)
 def test_saved_action_retains_conditions_preconditions_and_no_trigger(self):
  self.save();method,path,body=self.calls[-1]
  self.assertEqual((method,path),('PUT','/v1.0/homes/demo/automations/rule'))
  self.assertEqual(body['conditions'],self.original['conditions']);self.assertEqual(body['preconditions'],self.original['preconditions'])
  self.assertEqual(body['actions'][0]['executor_property'],{'switch':True});self.assertNotIn('trigger',path)
 def test_changed_device_condition_is_saved(self):
  conditions=copy.deepcopy(self.original['conditions']);conditions[0]['display']['value']=False
  self.save(conditions);self.assertFalse(self.calls[-1][2]['conditions'][0]['display']['value'])
 def test_stale_rule_is_not_overwritten(self):
  self.latest['conditions'][0]['display']['value']=False
  with self.assertRaisesRegex(RuntimeError,'inzwischen'):self.save()
  self.assertTrue(all(method=='GET' for method,_,_ in self.calls))
 def test_missing_triggers_never_overwrites_existing_rule(self):
  self.latest['conditions']=[]
  with self.assertRaisesRegex(ValueError,'vollständigen'):self.save()
  self.assertTrue(all(method=='GET' for method,_,_ in self.calls))
 def test_invalid_condition_does_not_write(self):
  conditions=copy.deepcopy(self.original['conditions']);conditions[0]['display']['operator']='>'
  with self.assertRaisesRegex(ValueError,'Vergleich'):self.save(conditions)
  self.assertTrue(all(method=='GET' for method,_,_ in self.calls))
 def test_unmodified_special_action_is_preserved(self):
  self.original['actions']=[{'action_executor':'lightBase','executor_property':{'unknown':'keep'}}];self.latest=copy.deepcopy(self.original)
  self.save(actions=[{'_raw':copy.deepcopy(self.original['actions'][0])}]);self.assertEqual(self.calls[-1][2]['actions'],self.original['actions'])
 def test_forged_original_action_cannot_be_written(self):
  with self.assertRaises(ValueError):self.save(actions=[{'_raw':{'action_executor':'lightBase','unknown':'new'}}])
  self.assertTrue(all(method=='GET' for method,_,_ in self.calls))
 def test_original_weather_condition_is_preserved(self):
  self.original['conditions']=[{'entity_type':3,'entity_id':'city','order_num':1,'display':{'code':'wind','operator':'>','value':25}}];self.latest=copy.deepcopy(self.original)
  self.save();self.assertEqual(self.calls[-1][2]['conditions'],self.original['conditions'])
 def test_custom_expression_references_only_existing_conditions(self):
  validate_condition_expression('(1&&2)||3',[1,2,3])
  for expr in ('1&&4','1&&','1); import os','(1||2','1 2'):
   with self.subTest(expr=expr),self.assertRaises(ValueError):validate_condition_expression(expr,[1,2,3])
class UpdateRefTests(unittest.TestCase):
 def packet(self,body):return ('%04x'%(len(body)+4)).encode()+body
 def test_uses_main_ref_not_default_head(self):
  raw=self.packet(b'# service=git-upload-pack\n')+b'0000'+self.packet(b'a'*40+b' HEAD\x00capabilities\n')+self.packet(b'b'*40+b' refs/heads/main\n')+b'0000'
  response=Mock(content=raw,is_redirect=False)
  with patch('updates.requests.get',return_value=response) as get:
   self.assertEqual(updates.branch_head(),'b'*40);self.assertEqual(get.call_args.kwargs['params'],{'service':'git-upload-pack'})
 def test_invalid_reference_never_reports_current(self):
  with patch('updates.requests.get',return_value=Mock(content=b'not a git reply',is_redirect=False)):
   with self.assertRaises(ValueError):updates.branch_head()
 def test_manifest_and_package_use_same_commit(self):
  sha='a'*40;manifest={'status':'available','platform':'win32','version':'9.9.9','url':'https://raw.githubusercontent.com/C4rstenSC/scripte/main/smartlife/updates/windows/test.zip'}
  response=Mock();response.json.return_value=manifest
  with patch('updates.branch_head',return_value=sha),patch('updates.sys.platform','win32'),patch('updates.requests.get',return_value=response) as get:
   m,newer=updates.check();self.assertTrue(newer);self.assertIn('/'+sha+'/',get.call_args.args[0]);self.assertIn('/'+sha+'/',m['url']);self.assertNotIn('/main/',m['url'])
if __name__=='__main__':unittest.main()
