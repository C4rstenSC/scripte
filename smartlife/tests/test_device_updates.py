import sys,copy,unittest,os,threading
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace
os.environ['QT_QPA_PLATFORM']='offscreen'
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
from project_cloud import DirectCloud,references_device
from demo import sample
from PySide6.QtWidgets import QApplication,QPushButton
from PySide6.QtCore import Qt
from main import Main,STYLE
from cloud_ui import DeviceAdminDialog
class DeviceUpdateTests(unittest.TestCase):
 def setUp(self):
  self.calls=[];self.saved_name='Steckdose Stehlampe';self.return_old_name=False;outer=self
  self.raw={'automation_id':'related','name':'TV-Licht','conditions':[{'entity_id':'s','display':{'code':'switch','operator':'==','value':True}}],'actions':[{'entity_id':'s','action_executor':'dpIssue','executor_property':{'switch':False}}],'match_type':1}
  class Api:
   def request(self,method,path,params=None,body=None):
    outer.calls.append((method,path,copy.deepcopy(body)))
    if method=='PUT':outer.saved_name=body['name'];return True
    if method in ('POST','DELETE'):return True
    if path=='/v1.0/devices/s':return {'id':'s','name':'Alter Name' if outer.return_old_name else outer.saved_name,'local_key':'not-for-ui','online':True}
    if path=='/v1.0/devices/s/status':return [{'code':'switch','value':True}]
    if path.endswith('/rooms/Wohnzimmer/devices'):return [] if any(c[0]=='POST' for c in outer.calls) else [{'id':'s'}]
    if path.endswith('/rooms/other/devices'):return [{'id':'s'}]
    if path.endswith('/automations/related'):return copy.deepcopy(outer.raw)
    raise AssertionError('Unzulässige zusätzliche Abfrage: '+path)
  self.direct=DirectCloud({},Api());self.direct.devices=sample()['devices'];self.direct.homes=[{'id':'demo'}];self.direct.rooms=[{'id':'Wohnzimmer','home':'demo','name':'Wohnzimmer'},{'id':'other','home':'demo','name':'Büro'}]
  self.direct.automations=[{'id':'related','home':'demo','name':'TV-Licht','original':copy.deepcopy(self.raw)},{'id':'unrelated','home':'demo','name':'Andere Regel','original':{'conditions':[{'entity_id':'other-device'}]}}]
 def test_rename_reads_back_only_changed_device_and_dependencies(self):
  before=copy.deepcopy(self.direct.devices[0]);result=self.direct.rename_and_refresh('s','Fernseher Steckdose')
  self.assertEqual(result['device']['name'],'Fernseher Steckdose');self.assertEqual(self.direct.devices[0],before)
  self.assertEqual([a['id'] for a in result['automations']],['related'])
  self.assertNotIn('not-for-ui',str(result));self.assertEqual(self.calls[0],('PUT','/v1.0/devices/s',{'name':'Fernseher Steckdose'}))
  self.assertTrue(all('/devices/s' in path or '/rooms/Wohnzimmer/devices' in path or '/automations/related' in path for _,path,_ in self.calls))
 def test_rename_preserves_related_rule_exactly_without_fetching_details(self):
  before=copy.deepcopy(self.direct.automations)
  result=self.direct.rename_and_refresh('s','Fernseher neu')
  self.assertEqual(result['warnings'],[]);self.assertEqual(self.direct.automations,before)
  self.assertEqual(result['automations'],[before[0]])
  self.assertFalse(any('/automations/' in path for method,path,body in self.calls))
 def test_rename_refreshes_display_from_device_id_with_partial_original_rule(self):
  from desktop_scenes import scene_rows,condition_rows
  self.direct.automations[0]['original']={'actions':[{'entity_id':'s','action_executor':'dpIssue','executor_property':{'switch':False}}]}
  result=self.direct.rename_and_refresh('s','Fernseher neu')
  self.assertEqual(result['warnings'],[])
  rows=scene_rows(result['automations'][0]['original'],self.direct.devices)
  self.assertEqual(rows[0][0],'Fernseher neu')
  self.assertFalse(any('/automations/' in path for method,path,body in self.calls))
 def test_full_validation_is_retained_when_editing_incomplete_rule(self):
  self.raw={'automation_id':'related','actions':[{'entity_id':'s'}]}
  with self.assertRaisesRegex(ValueError,'vollständigen Auslöser'):self.direct.get_automation('demo','related')
 def test_unconfirmed_rename_never_changes_display_snapshot(self):
  self.return_old_name=True;old=copy.deepcopy(self.direct.devices)
  with patch('project_cloud.time.sleep'),self.assertRaisesRegex(RuntimeError,'nicht bestätigt'):self.direct.rename_and_refresh('s','Neuer Name')
  self.assertEqual(self.direct.devices,old);self.assertEqual(sum(method=='PUT' for method,_,_ in self.calls),1)
 def test_move_updates_only_target_and_affected_room_memberships(self):
  result=self.direct.move_and_refresh('s','other');self.assertEqual(result['device']['room'],'Büro');self.assertEqual(result['device']['room_id'],'other')
  self.assertFalse(any(path.endswith('/homes/demo/devices') or path.endswith('/homes/demo/rooms') or path.endswith('/homes/demo/automations') for _,path,_ in self.calls))
 def test_background_refresh_yields_for_editor(self):
  self.direct.background_pause.set();self.direct.refresh();self.assertEqual(self.calls,[])
 def test_embedded_dependency_is_detected(self):
  self.assertTrue(references_device({'executor_property':'{"device_id":"s"}'},'s'));self.assertFalse(references_device({'device_id':'ss'},'s'))
class DeviceDialogTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.app=QApplication.instance() or QApplication([]);cls.app.setStyleSheet(STYLE)
 def test_actual_save_button_updates_list_and_details_without_full_reload(self):
  w=Main(True);w.navigate('Geräte');device=next(d for d in w.data['devices'] if d['id']=='s');target=copy.deepcopy(device);target['name']='Fernseher neu';calls=[]
  def rename(did,name):calls.append((did,name));return {'device':dict(target,name=name),'automations':[],'warnings':[]}
  w.cloud.direct=SimpleNamespace(rooms=[{'id':device['room_id'],'home':'demo','name':device['room']}],rename_and_refresh=rename)
  w.submit=lambda fn,done,error:done(fn())
  with patch.object(w,'load') as load:
   dialog=DeviceAdminDialog(w,device);dialog.name.setText('Fernseher neu');button=next(b for b in dialog.findChildren(QPushButton) if b.text()=='Gerätenamen speichern');button.click();self.app.processEvents()
   self.assertEqual(calls,[('s','Fernseher neu')]);self.assertEqual(device['name'],'Fernseher neu');self.assertIn('bestätigt',dialog.message.text());load.assert_not_called()
   self.assertTrue(any(w.tree.topLevelItem(i).text(0)=='Fernseher neu' for i in range(w.tree.topLevelItemCount())));dialog.close()
  w.close();self.app.processEvents()
 def test_device_editor_is_allowed_during_background_read(self):
  w=Main(True);w.pending=True;w.cloud.direct=SimpleNamespace()
  self.assertTrue(w.require_direct(allow_background=True));w.close();self.app.processEvents()
if __name__=='__main__':unittest.main()
