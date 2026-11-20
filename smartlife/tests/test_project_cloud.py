import sys,unittest,json,hashlib,hmac
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
from project_cloud import ProjectAPI,DirectCloud,parse_model
from portable_credentials import encrypt_config,decrypt_config
from demo import sample
CONFIG={'access_id':'test-client','access_secret':'test-secret-never-real','uid':'test-user','region':'Central Europe'}
class Response:
 status_code=200
 def __init__(self,data):self.data=data
 def raise_for_status(self):pass
 def json(self):return self.data
class Session:
 def __init__(self,data):self.data=data;self.calls=[]
 def request(self,*args,**kwargs):self.calls.append((args,kwargs));return Response(self.data)
 def close(self):pass
class FakeAPI:
 def __init__(self):self.calls=[];self.result=True
 def request(self,*args,**kwargs):self.calls.append((args,kwargs));return self.result
 def close(self):pass
class ProjectTests(unittest.TestCase):
 def direct(self):
  api=FakeAPI();d=DirectCloud(CONFIG,api);d.homes=[{'id':'demo','name':'Zuhause'}];d.rooms=[{'id':'Wohnzimmer','home':'demo','name':'Wohnzimmer'},{'id':'other','home':'demo','name':'Anderer Raum'}];d.devices=sample()['devices'];return d,api
 def test_token_signature_has_no_access_token(self):
  session=Session({'success':True,'result':{'access_token':'access','expire_time':3600}});api=ProjectAPI(CONFIG,session)
  with patch('project_cloud.time.time',return_value=1700000000):api.connect()
  args,kw=session.calls[0];self.assertTrue(args[1].endswith('/v1.0/token?grant_type=1'));self.assertNotIn('access_token',kw['headers'])
  canonical='GET\n'+hashlib.sha256(b'').hexdigest()+'\n\n/v1.0/token?grant_type=1'
  expected=hmac.new(CONFIG['access_secret'].encode(),('test-client1700000000000'+canonical).encode(),hashlib.sha256).hexdigest().upper();self.assertEqual(kw['headers']['sign'],expected)
 def test_signed_body_is_identical_to_sent_bytes(self):
  session=Session({'success':True,'result':True});api=ProjectAPI(CONFIG,session);api.token='access';api.expires=10**15
  body={'name':'Küche'}
  with patch('project_cloud.time.time',return_value=1700000000):api.request('PUT','/v1.0/devices/test',body=body)
  _,kw=session.calls[0];self.assertEqual(json.loads(kw['data']),body)
  canonical='PUT\n'+hashlib.sha256(kw['data']).hexdigest()+'\n\n/v1.0/devices/test'
  expected=hmac.new(CONFIG['access_secret'].encode(),('test-clientaccess1700000000000'+canonical).encode(),hashlib.sha256).hexdigest().upper();self.assertEqual(kw['headers']['sign'],expected)
 def test_batch_mac_signature_matches_official_tuya_parameter_rules(self):
  session=Session({'success':True,'result':[]});api=ProjectAPI(CONFIG,session);api.token='access';api.expires=10**15
  with patch('project_cloud.time.time',return_value=1700000000):api.request('GET','/v1.0/devices/factory-infos',params={'device_ids':'first-device,second-device'})
  args,kw=session.calls[0];self.assertTrue(args[1].endswith('device_ids=first-device%2Csecond-device'))
  canonical='GET\n'+hashlib.sha256(b'').hexdigest()+'\n\n/v1.0/devices/factory-infos?device_ids=first-device,second-device'
  expected=hmac.new(CONFIG['access_secret'].encode(),('test-clientaccess1700000000000'+canonical).encode(),hashlib.sha256).hexdigest().upper()
  self.assertEqual(kw['headers']['sign'],expected)
 def test_query_signature_orders_raw_values_but_escapes_transport(self):
  session=Session({'success':True,'result':[]});api=ProjectAPI(CONFIG,session);api.token='access';api.expires=10**15
  with patch('project_cloud.time.time',return_value=1700000000):api.request('GET','/test',params={'z':'Küche & Büro','a':'x+y'})
  args,kw=session.calls[0];self.assertTrue(args[1].endswith('a=x%2By&z=K%C3%BCche+%26+B%C3%BCro'))
  canonical='GET\n'+hashlib.sha256(b'').hexdigest()+'\n\n/test?a=x+y&z=Küche & Büro'
  expected=hmac.new(CONFIG['access_secret'].encode(),('test-clientaccess1700000000000'+canonical).encode(),hashlib.sha256).hexdigest().upper()
  self.assertEqual(kw['headers']['sign'],expected)
 def test_signature_error_during_query_does_not_blame_credentials(self):
  api=ProjectAPI(CONFIG,Session({'success':False,'code':1004,'msg':'sign invalid'}));api.token='access';api.expires=10**15
  with self.assertRaisesRegex(RuntimeError,'nicht automatisch falsche Zugangsdaten'):api.request('GET','/v1.0/devices/factory-infos',{'device_ids':'a,b'})
 def test_api_error_never_exposes_secret(self):
  api=ProjectAPI(CONFIG,Session({'success':False,'code':1106,'msg':CONFIG['access_secret']}))
  with self.assertRaises(RuntimeError) as caught:api.connect()
  self.assertNotIn(CONFIG['access_secret'],str(caught.exception));self.assertIn('1106',str(caught.exception))
 def test_no_mutation_retry(self):
  session=Session({'success':False,'code':1010});api=ProjectAPI(CONFIG,session);api.token='old';api.expires=10**15
  with self.assertRaises(RuntimeError):api.request('PUT','/v1.0/devices/test',body={'name':'Test'})
  self.assertEqual(len(session.calls),1)
 def test_model_read_only_not_writable(self):
  funcs,ranges=parse_model({'model':json.dumps({'services':[{'properties':[{'code':'control','accessMode':'rw','typeSpec':{'type':'enum','range':['open','close','stop']}},{'code':'percent_state','accessMode':'ro','typeSpec':{'type':'value','min':0,'max':100,'step':1}}]}]})})
  self.assertIn('control',funcs);self.assertNotIn('percent_state',funcs);self.assertIn('percent_state',ranges)
 def test_rename_only_changes_name(self):
  d,a=self.direct();d.rename_device('s','Neu');self.assertEqual(a.calls[-1],(('PUT','/v1.0/devices/s'),{'body':{'name':'Neu'}}))
 def test_delete_nonempty_room_never_deletes(self):
  d,a=self.direct();a.result=[{'id':'s'}]
  with self.assertRaises(ValueError):d.delete_room('demo','Wohnzimmer')
  self.assertEqual(len(a.calls),1);self.assertEqual(a.calls[0][0][0],'GET')
 def test_move_only_adds_selected_device(self):
  d,a=self.direct();a.result=[];d.move_device('s','other');self.assertEqual(a.calls[0],(('POST','/v1.0/homes/demo/rooms/other/devices'),{'body':{'device_ids':['s']}}));self.assertFalse(any(x[0][0]=='PUT' for x in a.calls))
 def test_cross_home_room_rejected_before_write(self):
  d,a=self.direct()
  with self.assertRaises(ValueError):d.move_device('s','room-from-elsewhere')
  self.assertEqual(a.calls,[])
 def test_stale_scene_is_not_overwritten(self):
  d,a=self.direct();a.result=[{'scene_id':'old','name':'Geändert','actions':[],'background':'x'}]
  with self.assertRaisesRegex(RuntimeError,'inzwischen'):d.save_scene('Neu','demo',[{'device':'s','code':'switch','value':True}],{'scene_id':'old','name':'Alt','actions':[],'background':'x'})
  self.assertEqual(len(a.calls),1);self.assertEqual(a.calls[0][0][0],'GET')
 def test_portable_credentials_roundtrip(self):
  blob=encrypt_config(CONFIG,'Ein-lang-es-Kennwort!');self.assertNotIn(CONFIG['access_secret'].encode(),blob);self.assertEqual(decrypt_config(blob,'Ein-lang-es-Kennwort!'),CONFIG)
 def test_portable_credentials_wrong_password_and_tamper(self):
  blob=encrypt_config(CONFIG,'Ein-lang-es-Kennwort!')
  for encrypted,password in [(blob,'falschesKennwort'),(blob[:-3]+b'AA\n','Ein-lang-es-Kennwort!')]:
   with self.assertRaises(ValueError):decrypt_config(encrypted,password)
if __name__=='__main__':unittest.main()
