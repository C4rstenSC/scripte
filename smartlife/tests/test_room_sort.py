import os,sys,unittest
from pathlib import Path
os.environ['QT_QPA_PLATFORM']='offscreen'
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
from PySide6.QtWidgets import QApplication,QTreeWidget
from PySide6.QtCore import Qt
from ui_widgets import DeviceItem
from main import Main
class RoomSortTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.app=QApplication.instance() or QApplication([])
 def test_both_room_directions_keep_names_ascending(self):
  tree=QTreeWidget();tree.setColumnCount(2);tree.setSortingEnabled(True)
  for name,room in [('Zulu','Büro'),('Beta','Bad'),('alpha','Büro'),('Anton','Bad')]:tree.addTopLevelItem(DeviceItem([name,room]))
  for order,expected in [(Qt.AscendingOrder,['Anton','Beta','alpha','Zulu']),(Qt.DescendingOrder,['alpha','Zulu','Anton','Beta'])]:
   tree.sortItems(1,order)
   self.assertEqual([tree.topLevelItem(i).text(0) for i in range(4)],expected)
 def test_render_and_page_switch_keep_room_sort(self):
  window=Main(True)
  try:
   window.navigate('Geräte');window.tree.sortItems(1,Qt.DescendingOrder)
   def rows():return [(window.tree.topLevelItem(i).text(1),window.tree.topLevelItem(i).text(0)) for i in range(window.tree.topLevelItemCount())]
   before=rows();window.render();self.assertEqual(rows(),before)
   window.navigate('Szenen');window.navigate('Geräte');self.assertEqual(rows(),before)
   self.assertEqual(window.tree.sortColumn(),1);self.assertEqual(window.tree.header().sortIndicatorOrder(),Qt.DescendingOrder)
  finally:window.close()
