import sys,unittest,threading,copy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch,Mock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
from PySide6.QtWidgets import QApplication,QDialog
from main import Main,STYLE
from scene_editor import SceneEditor
from automation_ui import AutomationEditor
from cloud_ui import RoomAdminDialog
from project_cloud import DirectCloud
from demo import sample
class LoadingTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.app=QApplication.instance() or QApplication([]);cls.app.setStyleSheet(STYLE)
 def setUp(self):
  self.w=Main(True);self.w.pending=True;self.w.poll.start();self.direct=SimpleNamespace(background_pause=threading.Event(),rooms=[],devices=self.w.data['devices']);self.w.cloud.direct=self.direct
 def tearDown(self):self.w.close();self.app.processEvents()
 def assert_paused(self,dialog=None):self.assertTrue(self.direct.background_pause.is_set());self.assertFalse(self.w.poll.isActive());return QDialog.Rejected
 def test_scene_editor_opens_while_loading_and_restores_poll(self):
  with patch.object(SceneEditor,'exec',self.assert_paused),patch('main.QMessageBox.information') as message:self.w.edit_scene();message.assert_not_called()
  self.assertFalse(self.direct.background_pause.is_set());self.assertTrue(self.w.poll.isActive())
 def test_automation_editor_opens_while_loading(self):
  with patch.object(AutomationEditor,'exec',self.assert_paused),patch('main.QMessageBox.information') as message:self.w.edit_automation();message.assert_not_called()
  self.assertFalse(self.direct.background_pause.is_set())
 def test_room_editor_opens_while_loading(self):
  with patch.object(RoomAdminDialog,'exec',self.assert_paused),patch('main.QMessageBox.information') as message:self.w.manage_rooms();message.assert_not_called()
 def test_automation_read_error_restores_pause_state(self):
  self.direct.get_automation=Mock(side_effect=RuntimeError('Cloudfehler'))
  def submit(fn,success,error):
   try:result=fn()
   except Exception as e:error(e);return
   success(result)
  self.w.submit=submit
  with patch.object(self.w,'error') as error:self.w.edit_automation({'id':'rule'});error.assert_called_once()
  self.assertFalse(self.direct.background_pause.is_set());self.assertTrue(self.w.poll.isActive())
 def test_device_table_replaces_public_ip_with_verified_lan_host(self):
  self.w.data['devices'][1]['mac']='AA:BB:CC:DD:EE:FF';self.w.data['devices'][1]['ip']='84.171.255.146'
  self.w.fritz.hosts=[{'mac':'AA:BB:CC:DD:EE:FF','aliases':[],'hostname':'TV-Steckdose','ip':'192.168.178.20','active':True}];self.w.navigate('Geräte')
  headers=[self.w.tree.headerItem().text(i) for i in range(self.w.tree.columnCount())];self.assertIn('FRITZ!Box-Hostname',headers);self.assertNotIn('IP-Adresse (Tuya)',headers)
  rows=[[self.w.tree.topLevelItem(i).text(c) for c in range(self.w.tree.columnCount())] for i in range(self.w.tree.topLevelItemCount())]
  self.assertTrue(any(r[2:4]==['192.168.178.20','TV-Steckdose'] for r in rows));self.assertNotIn('84.171.255.146',str(rows))
class RenameStageTests(unittest.TestCase):
 def cloud(self,api):
  cloud=DirectCloud({},api);cloud.devices=sample()['devices'];return cloud
 def test_write_rejection_has_specific_phase_and_no_read(self):
  api=Mock();api.request.side_effect=RuntimeError('Tuya-Fehler 60001001')
  with self.assertRaisesRegex(RuntimeError,'nicht gespeichert'):self.cloud(api).rename_and_refresh('s','Neuer Name')
  self.assertEqual(api.request.call_count,1);self.assertEqual(api.request.call_args.args[0],'PUT')
 def test_read_rejection_is_distinguished_from_write_rejection(self):
  api=Mock();api.request.side_effect=[True,RuntimeError('Lesen verweigert')]
  with self.assertRaisesRegex(RuntimeError,'angenommen, aber das Rücklesen'):self.cloud(api).rename_and_refresh('s','Neuer Name')
  self.assertEqual(api.request.call_count,2)
if __name__=='__main__':unittest.main()
