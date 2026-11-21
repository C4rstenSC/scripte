import sys,unittest,copy
from pathlib import Path
from unittest.mock import Mock,patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
from end_user import EndUserAPI
from project_cloud import DirectCloud
from demo import sample
KEY='sk-EUexampletestkey'
class Response:
 status_code=200
 def __init__(self,value):self.value=value
 def raise_for_status(self):pass
 def json(self):return self.value
class Session:
 def __init__(self,replies):self.replies=list(replies);self.calls=[]
 def request(self,*args,**kwargs):self.calls.append((args,kwargs));return Response(self.replies.pop(0))
 def close(self):pass
def ok(data):return {'success':True,'result':data}
class EndUserTests(unittest.TestCase):
 def test_documented_endpoint_bearer_and_verified_readback(self):
  session=Session([ok({'device_id':'a','name':'Alt'}),ok({}),ok({'device_id':'a','name':'Neu'})]);api=EndUserAPI(KEY,session)
  self.assertEqual(api.rename('a','Neu')['name'],'Neu')
  self.assertEqual([a[0][0] for a in session.calls],['GET','POST','GET'])
  args,kw=session.calls[1];self.assertEqual(args[1],'https://openapi.tuyaeu.com/v1.0/end-user/devices/a/attribute');self.assertEqual(kw['json'],{'name':'Neu'});self.assertEqual(kw['headers']['Authorization'],'Bearer '+KEY);self.assertFalse(kw['allow_redirects'])
 def test_wrong_account_target_never_writes(self):
  session=Session([ok({'device_id':'other','name':'Alt'})]);api=EndUserAPI(KEY,session)
  with self.assertRaises(RuntimeError):api.rename('a','Neu')
  self.assertEqual(len(session.calls),1)
 def test_failed_write_is_not_retried_or_reported_success(self):
  session=Session([ok({'device_id':'a','name':'Alt'}),{'success':False,'code':1010,'msg':KEY}]);api=EndUserAPI(KEY,session)
  with self.assertRaises(RuntimeError) as err:api.rename('a','Neu')
  self.assertNotIn(KEY,str(err.exception));self.assertEqual(len(session.calls),2)
 def test_stale_readback_never_reports_success(self):
  session=Session([ok({'device_id':'a','name':'Alt'}),ok({})]+[ok({'device_id':'a','name':'Alt'})]*3);api=EndUserAPI(KEY,session)
  with patch('end_user.time.sleep'):
   with self.assertRaisesRegex(RuntimeError,'nicht bestätigt'):api.rename('a','Neu')
  self.assertEqual(sum(args[0]=='POST' for args,kw in session.calls),1)
 def test_rejects_project_id_and_arbitrary_hosts(self):
  for key in ('old-client-id','sk-ZZinvalid','https://evil.test','sk-EUtest\r\nHost: evil'):
   with self.assertRaises(ValueError):EndUserAPI(key)
 def test_explicit_redirect_does_not_forward_key(self):
  reply=Response({});reply.status_code=302;session=Mock();session.request.return_value=reply
  with self.assertRaisesRegex(RuntimeError,'Weiterleitung'):EndUserAPI(KEY,session).devices()
  self.assertEqual(session.request.call_count,1)
 def test_direct_cloud_routes_rename_only_to_end_user_and_refreshes_target(self):
  project=Mock();cloud=DirectCloud({'access_id':'test','access_secret':'fake','uid':'test','region':'Central Europe'},project)
  cloud.devices=sample()['devices'];cloud.rooms=[];device=next(d for d in cloud.devices if d['id']=='s');device['room_id']='';cloud.end_user=Mock();cloud.end_user.rename.return_value={'id':'s','name':'Neu'};cloud.read_status=Mock(return_value={})
  result=cloud.rename_and_refresh('s','Neu');self.assertEqual(result['device']['name'],'Neu');cloud.end_user.rename.assert_called_once_with('s','Neu');project.request.assert_not_called()
 def test_read_only_key_check_never_mutates(self):
  session=Session([ok({'devices':[{'device_id':'a'}]})]);rows=EndUserAPI(KEY,session).devices();self.assertEqual(rows[0]['device_id'],'a');self.assertEqual(session.calls[0][0][0],'GET')

class EndUserControlTests(unittest.TestCase):
 def cloud(self):
  project=Mock();cloud=DirectCloud({'access_id':'test','access_secret':'fake','uid':'test','region':'Central Europe'},project);cloud.devices=sample()['devices'];cloud.end_user=Mock();return cloud,project
 def test_command_uses_documented_double_serialized_properties(self):
  import json
  session=Session([ok({'device_id':'a'}),ok({})]);api=EndUserAPI(KEY,session)
  self.assertTrue(api.command('a','switch_1',False));args,kw=session.calls[-1]
  self.assertEqual(args,('POST','https://openapi.tuyaeu.com/v1.0/end-user/devices/a/shadow/properties/issue'))
  self.assertIsInstance(kw['json']['properties'],str);self.assertEqual(json.loads(kw['json']['properties']),{'switch_1':False})
 def test_bad_ack_is_not_retried(self):
  session=Session([ok({'device_id':'a'}),ok(False)])
  with self.assertRaisesRegex(RuntimeError,'nicht bestätigt'):EndUserAPI(KEY,session).command('a','switch_1',True)
  self.assertEqual(len(session.calls),2)
 def test_no_device_identity_no_control_write(self):
  session=Session([ok({'device_id':'other'})])
  with self.assertRaises(RuntimeError):EndUserAPI(KEY,session).command('a','switch_1',True)
  self.assertEqual(len(session.calls),1)
 def test_switch_and_raw_device_never_write_to_project(self):
  for raw in (False,True):
   cloud,project=self.cloud();device=next(d for d in cloud.devices if d['id']=='s');device.update(raw_control=raw,online=True)
   self.assertTrue(cloud.command('s','switch',False));cloud.end_user.command.assert_called_once_with('s','switch',False);project.request.assert_not_called()
 def test_failed_end_user_control_never_falls_back_to_project(self):
  cloud,project=self.cloud();cloud.end_user.command.side_effect=RuntimeError('abgelehnt')
  with self.assertRaisesRegex(RuntimeError,'abgelehnt'):cloud.command('s','switch',False)
  project.request.assert_not_called()
 def test_invalid_function_never_sends(self):
  cloud,project=self.cloud()
  with self.assertRaises(ValueError):cloud.command('s','unbekannt',True)
  cloud.end_user.command.assert_not_called();project.request.assert_not_called()
 def test_actual_status_uses_end_user_and_keeps_zero_and_false(self):
  cloud,project=self.cloud();device=next(d for d in cloud.devices if d['id']=='s');cloud.end_user.properties.return_value={'device_id':'s','online':False,'properties':{'switch':False,'cur_power':0}}
  self.assertEqual(cloud.read_status(device),{'switch':False,'cur_power':0});self.assertFalse(device['online']);project.request.assert_not_called()
 def test_absent_properties_does_not_become_empty_success(self):
  with self.assertRaisesRegex(RuntimeError,'keine auswertbaren'):EndUserAPI(KEY,Session([ok({'device_id':'a'})])).properties('a')
 def test_supported_inventory_reads_use_end_user_routes(self):
  cloud,project=self.cloud()
  for old,new in [('/v1.0/users/test/homes','/v1.0/end-user/homes/all'),('/v1.0/homes/h/rooms','/v1.0/end-user/homes/h/rooms'),('/v1.0/homes/h/rooms/r/devices','/v1.0/end-user/homes/room/r/devices'),('/v1.0/homes/h/devices','/v1.0/end-user/homes/h/devices'),('/v2.0/cloud/thing/s/model','/v1.0/end-user/devices/s/model')]:
   cloud._read(old);cloud.end_user.request.assert_called_with('GET',new)
  project.request.assert_not_called()
 def test_scene_api_not_guessed_for_end_user(self):
  cloud,project=self.cloud();cloud._read('/v1.1/homes/h/scenes');project.request.assert_called_once_with('GET','/v1.1/homes/h/scenes');cloud.end_user.request.assert_not_called()

 def test_inventory_reload_keeps_confirmed_mac_and_gateway_identity(self):
  cloud,project=self.cloud();old=next(d for d in cloud.devices if d['id']=='s');old.update(mac='AA:BB:CC:DD:EE:FF',sub=True)
  project.request.return_value=[]
  def read(method,path):
   if path.endswith('/homes/all'):return {'homes':[{'home_id':'demo','name':'Zuhause'}]}
   if path.endswith('/homes/demo/rooms'):return {'rooms':[]}
   if path.endswith('/homes/demo/devices'):return {'devices':[{'device_id':'s','name':'Steckdose','online':True}]}
   if path.endswith('/devices/s/model'):return {'model':{'services':[]}}
   raise AssertionError(path)
  cloud.end_user.request.side_effect=read;cloud.end_user.properties.return_value={'device_id':'s','properties':{'switch':True},'online':True}
  result=cloud.load();device=next(d for d in result['devices'] if d['id']=='s')
  self.assertEqual(device['mac'],'AA:BB:CC:DD:EE:FF');self.assertTrue(device['sub'])
