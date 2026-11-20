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
