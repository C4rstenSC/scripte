import sys,unittest,tempfile,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
from core import fmt,validate,safe_endpoint,Cloud,cover_position,cover_text,climate,TEMPERATURE_CODES,label,diagnostic_filter
from updates import extract,version,validate_url
from demo import sample
class CoreTests(unittest.TestCase):
 def test_cover_actual_position(self):
  d=sample()['devices'][3];self.assertEqual(cover_position(d),75)
  d['status']={'percent_control':25};self.assertIsNone(cover_position(d));self.assertIn('Sollwert',cover_text(d))
  d['status']={'percent_state':0};self.assertIn('Geschlossen',cover_text(d))
  d['status']={'percent_state':100};self.assertIn('Vollständig offen',cover_text(d))
 def test_german_numbered_labels(self):
  self.assertEqual(label('bright_value_1'),'Helligkeit 1')
  self.assertEqual(label('switch_led_1'),'Licht 1')
  self.assertEqual(label('brightness_min_1'),'Mindesthelligkeit 1')
  self.assertEqual(fmt('memory'),'Letzten Zustand wiederherstellen')
 def test_climate_single_temperature(self):
  d=sample()['devices'][0];d['status']['temp_current']=224
  self.assertEqual(climate(d,TEMPERATURE_CODES,'°C'),'22,3 °C')
 def test_diagnostics_exclude_credentials(self):
  self.assertEqual(diagnostic_filter({'local_key':'secret','ip':'1.2.3.4','access_token':'secret','result':{'status':[],'localKey':'secret'}}),{'result':{'status':[]}})
 def test_scaled_temperature(self):self.assertEqual(fmt(223,{'values':{'scale':1,'unit':'°C'}}),'22,3 °C')
 def test_negative(self):self.assertEqual(fmt(-42,{'values':'{"scale":1}'}),'-4,2')
 def test_false(self):self.assertEqual(fmt(False),'Aus')
 def test_enum(self):self.assertEqual(fmt('auto'),'Automatisch')
 def test_bounds(self):
  s={'type':'Integer','values':{'min':10,'max':1000,'step':10}}
  self.assertEqual(validate(s,650),650)
  for v in (0,1001,655,True,1.2):
   with self.subTest(v=v),self.assertRaises(ValueError):validate(s,v)
 def test_enum_rejected(self):
  with self.assertRaises(ValueError):validate({'type':'Enum','values':{'range':['open','close','stop']}},'reverse')
 def test_boolean_str_rejected(self):
  with self.assertRaises(ValueError):validate({'type':'Boolean'},'true')
 def test_endpoints(self):
  self.assertTrue(safe_endpoint('https://apigw.tuyaeu.com'))
  for s in ['http://apigw.tuyaeu.com','https://evil.tuya.com.evil.org','https://evil.org','https://user:pass@apigw.tuyaeu.com']:
   self.assertFalse(safe_endpoint(s))
 def test_version(self):self.assertTrue(version('0.10.0')>version('0.9.9'))
 def test_bad_version(self):
  with self.assertRaises(ValueError):version('0.1.evil')
 def test_update_source(self):
  validate_url('https://raw.githubusercontent.com/C4rstenSC/scripte/main/smartlife/a.zip')
  with self.assertRaises(ValueError):validate_url('https://evil.org/a.zip')
 def test_zip_slip(self):
  for path in ['../evil','/tmp/evil','app/../../evil','app\\evil','other/evil','app/C:evil']:
   with tempfile.TemporaryDirectory() as td:
    p=Path(td);z=p/'a.zip'
    with zipfile.ZipFile(z,'w') as f:f.writestr(path,'bad')
    with self.subTest(path=path),self.assertRaises(ValueError):extract(z,p/'dest')
 def test_valid_package(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);z=p/'a.zip'
   with zipfile.ZipFile(z,'w') as f:f.writestr('app/main.py','pass');f.writestr('app/core.py','pass')
   extract(z,p/'dest');self.assertTrue((p/'dest/app/main.py').exists())
 def test_commands_require_online_and_function(self):
  c=object.__new__(Cloud);d=sample()['devices'][1];c.devices=[d];d['online']=False
  with self.assertRaises(RuntimeError):c.command(d['id'],'switch',True)
  d['online']=True
  with self.assertRaises(ValueError):c.command(d['id'],'factory_reset',True)
 def test_no_false_ack(self):
  from types import SimpleNamespace
  c=object.__new__(Cloud);c.devices=[sample()['devices'][1]]
  for reply in [None,{'success':False},{'success':True,'result':False}]:
   c.manager=SimpleNamespace(customer_api=SimpleNamespace(post=lambda *a:reply))
   with self.assertRaises(RuntimeError):c.command('s','switch',True)
if __name__=='__main__':unittest.main()
