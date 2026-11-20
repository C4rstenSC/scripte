import os,sys,unittest,time,threading
from unittest.mock import patch
from pathlib import Path
os.environ['QT_QPA_PLATFORM']='offscreen'
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
from PySide6.QtWidgets import QApplication,QPushButton
from main import Main,STYLE
class UiTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.app=QApplication.instance() or QApplication([]);cls.app.setStyleSheet(STYLE)
 def setUp(self):self.w=Main(True)
 def tearDown(self):self.w.close();self.app.processEvents()
 def test_rooms(self):
  self.w.navigate('Räume');self.assertEqual(self.w.tree.topLevelItemCount(),6)
  self.w.room.setCurrentIndex(self.w.room.findData('Wohnzimmer'));self.assertEqual(self.w.tree.topLevelItemCount(),3)
 def test_search(self):self.w.navigate('Geräte');self.w.search.setText('reiniger');self.assertEqual(self.w.tree.topLevelItemCount(),1)
 def test_device_controls(self):
  self.w.navigate('Geräte')
  for i in range(self.w.tree.topLevelItemCount()):
   self.w.tree.setCurrentItem(self.w.tree.topLevelItem(i));self.app.processEvents()
  self.assertIsNotNone(self.w.detail_id)
 def test_overview_only_climate(self):
  self.assertEqual(self.w.climate_tree.columnCount(),5)
  self.assertFalse(self.w.room_tabs.isVisible())
  self.assertEqual(self.w.climate_tree.topLevelItemCount(),1)
 def test_move_room_tabs_keeps_room_identity(self):
  self.w.settings.remove('room-order/demo');self.w.change_home();self.w.navigate('Räume')
  index=next(i for i in range(self.w.room_tabs.count()) if self.w.room_tabs.tabData(i)=='Wohnzimmer')
  self.w.room_tabs.moveTab(index,1);self.w.room_tabs.setCurrentIndex(1)
  self.assertEqual(self.w.room.currentData(),'Wohnzimmer');self.assertEqual(self.w.tree.topLevelItemCount(),3)
  self.w.change_home();self.assertEqual(self.w.room_tabs.tabData(1),'Wohnzimmer');self.w.settings.remove('room-order/demo')
 def test_update_interval_is_one_minute(self):self.assertEqual(self.w.update_timer.interval(),60000)
 def test_update_check_not_blocked_by_devices(self):
  gate=threading.Event();blocked=self.w.pool.submit(lambda:gate.wait(2));self.w.demo=False
  try:
   with patch('main.updates.check',return_value=({'version':'9.9.9'},True)):
    self.w.check_update(False)
    end=time.monotonic()+1
    while getattr(self.w,'update_checking',False) and time.monotonic()<end:self.app.processEvents();time.sleep(.005)
    self.assertIn('9.9.9',self.w.update_note.text());self.assertFalse(blocked.done())
  finally:gate.set();blocked.result(timeout=2)
 def test_click_during_check_is_not_lost(self):
  self.w.demo=False;self.w.update_checking=True;self.w.check_update(True)
  self.assertTrue(self.w.update_interactive);self.assertIn('läuft',self.w.update_note.text())
 def test_ip_column(self):
  self.w.navigate('Geräte');self.assertEqual(self.w.tree.headerItem().text(2),'IP-Adresse (Tuya)')
 def test_scenes(self):self.w.navigate('Szenen');self.assertEqual(self.w.tree.topLevelItemCount(),1)
 def test_navigation(self):
  self.w.navigate('Räume');self.assertTrue(self.w.buttons['Räume'].isChecked());self.assertFalse(self.w.buttons['Geräte'].isChecked())
if __name__=='__main__':unittest.main()
