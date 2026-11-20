import os,sys,unittest
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
  self.assertEqual(self.w.climate_tree.topLevelItemCount(),3)
 def test_ip_column(self):
  self.w.navigate('Geräte');self.assertEqual(self.w.tree.headerItem().text(2),'IP-Adresse (Tuya)')
 def test_scenes(self):self.w.navigate('Szenen');self.assertEqual(self.w.tree.topLevelItemCount(),1)
 def test_navigation(self):
  self.w.navigate('Räume');self.assertTrue(self.w.buttons['Räume'].isChecked());self.assertFalse(self.w.buttons['Geräte'].isChecked())
if __name__=='__main__':unittest.main()
