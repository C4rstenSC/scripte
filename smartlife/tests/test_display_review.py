import sys,os,unittest
from pathlib import Path
from types import SimpleNamespace
os.environ['QT_QPA_PLATFORM']='offscreen'
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
from PySide6.QtWidgets import QApplication,QLabel,QTreeWidget,QTreeWidgetItem
from PySide6.QtCore import Qt
from main import Main,STYLE
from core import ui_label,fmt,ui_control
from ui_widgets import fit_columns
from cloud_ui import RoomAdminDialog
class DisplayReviewTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.app=QApplication.instance() or QApplication([]);cls.app.setStyleSheet(STYLE)
 def test_screenshot_function_names_are_german(self):
  self.assertEqual(ui_label('do_not_disturb',{'name':'勿扰模式'}),'Nach Stromausfall ausgeschaltet bleiben')
  self.assertEqual(ui_label('hum_calibration',{'name':'环境湿度校准'}),'Luftfeuchte-Korrektur')
  self.assertEqual(ui_label('temp_calibration',{'name':'环境温度校准'}),'Temperatur-Korrektur')
  self.assertEqual(ui_label('temp_correction',{'name':'探头温度校准'}),'Korrektur der Fühlertemperatur')
 def test_untranslated_vendor_strings_do_not_leak(self):
  self.assertEqual(ui_label('vendor_unknown',{'name':'特殊功能'}),'')
  self.assertFalse(ui_control('vendor_unknown',{'name':'特殊功能','type':'Boolean'}))
  self.assertNotIn('模式',fmt('厂家模式'))
 def test_unknown_enum_choices_are_not_presented_as_equivalent(self):
  self.assertFalse(ui_control('mode',{'type':'Enum','values':{'range':['auto','unknown_vendor_mode']}}))
 def test_full_device_view_has_no_vendor_chinese(self):
  w=Main(True);d=w.data['devices'][0]
  d['functions'].update({'do_not_disturb':{'name':'勿扰模式','type':'Boolean'},'hum_calibration':{'name':'环境湿度校准','type':'Integer','values':{'min':-10,'max':10}},'vendor_unknown':{'name':'特殊功能','type':'Boolean'}})
  d['status'].update({'do_not_disturb':False,'hum_calibration':0,'vendor_unknown':True});w.navigate('Geräte')
  item=next(w.tree.topLevelItem(i) for i in range(w.tree.topLevelItemCount()) if w.tree.topLevelItem(i).data(0,Qt.UserRole)['id']==d['id']);w.tree.setCurrentItem(item);self.app.processEvents()
  text='\n'.join(label.text() for label in w.detail.findChildren(QLabel))
  self.assertIn('Luftfeuchte-Korrektur',text);self.assertIn('Nach Stromausfall',text);self.assertNotRegex(text,r'[\u3400-\u9fff]');w.close();self.app.processEvents()
 def test_columns_include_header_and_longest_cell_plus_centimetre(self):
  tree=QTreeWidget();tree.setHeaderLabels(['Raum','Ein sehr langer Spaltenkopf']);tree.addTopLevelItem(QTreeWidgetItem(['Hauswirtschaftsraum mit langem Namen','2']))
  tree.show();self.app.processEvents();fit_columns(tree);first=[tree.columnWidth(i) for i in range(2)]
  for i in range(2):
   tree.resizeColumnToContents(i);self.assertGreaterEqual(first[i]-tree.columnWidth(i),round(tree.logicalDpiX()/2.54))
  fit_columns(tree);self.assertEqual(first,[tree.columnWidth(i) for i in range(2)]);tree.close()
 def test_room_dialog_columns_fit_actual_room_names(self):
  w=Main(True);w.cloud.direct=SimpleNamespace(rooms=[{'id':'r','name':'Hauswirtschaftsraum','home':'demo'}],devices=[])
  dialog=RoomAdminDialog(w,'demo');width=dialog.tree.columnWidth(0);dialog.tree.resizeColumnToContents(0)
  self.assertGreaterEqual(width-dialog.tree.columnWidth(0),round(dialog.tree.logicalDpiX()/2.54));dialog.close();w.close();self.app.processEvents()
if __name__=='__main__':unittest.main()
