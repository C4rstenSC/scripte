import sys,unittest,copy,socket
from pathlib import Path
from unittest.mock import Mock,patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
from fritz import FritzClient,FritzAccount,FritzFault,mac,local_ip,parse_xml,safe_path,host_record
from project_cloud import DirectCloud
from requests.auth import HTTPDigestAuth
CONFIG={'address':'fritz.box','user':'local-user','password':'test-password-never-real'}
RESOLVED=[(socket.AF_INET,socket.SOCK_STREAM,6,'',('192.168.178.1',49000))]
SERVICE=b'<root><device><serviceList><service><serviceType>urn:dslforum-org:service:Hosts:1</serviceType><controlURL>/upnp/control/hosts</controlURL><SCPDURL>/hostsSCPD.xml</SCPDURL></service></serviceList></device></root>'
HOSTS=b'<List><Item><IPAddress>192.168.178.20</IPAddress><MACAddress>AA:BB:CC:DD:EE:FF</MACAddress><HostName>TV-Steckdose</HostName><Active>1</Active></Item></List>'
def soap(action,values):return ('<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><u:'+action+'Response xmlns:u="urn:dslforum-org:service:Hosts:1">'+values+'</u:'+action+'Response></s:Body></s:Envelope>').encode()
class Response:
 def __init__(self,content,status=200):self.content=content;self.status_code=status
 def raise_for_status(self):
  if self.status_code>=400:
   import requests;raise requests.HTTPError()
class Session:
 def __init__(self,replies):self.replies=list(replies);self.calls=[];self.closed=False
 def request(self,*args,**kwargs):self.calls.append((args,kwargs));return self.replies.pop(0)
 def close(self):self.closed=True
class FritzTests(unittest.TestCase):
 def client(self,replies):
  session=Session(replies)
  with patch('fritz.socket.getaddrinfo',return_value=RESOLVED):client=FritzClient(CONFIG,session)
  return client,session
 def test_documented_host_list_protocol_digest_and_local_only(self):
  actions=b'<scpd><actionList><action><name>X_AVM-DE_GetHostListPath</name></action></actionList></scpd>'
  replies=[Response(SERVICE),Response(actions),Response(soap('X_AVM-DE_GetHostListPath','<NewX_AVM-DE_HostListPath>/hosts.lua?sid=test-session</NewX_AVM-DE_HostListPath>')),Response(HOSTS)]
  client,session=self.client(replies);hosts=client.hosts();self.assertEqual(hosts[0]['hostname'],'TV-Steckdose');self.assertEqual(hosts[0]['ip'],'192.168.178.20')
  self.assertIsInstance(session.auth,HTTPDigestAuth);self.assertFalse(session.trust_env)
  self.assertTrue(all(args[1].startswith('http://192.168.178.1:49000/') and not kwargs['allow_redirects'] for args,kwargs in session.calls))
  post=session.calls[2];self.assertEqual(post[0][0],'POST');self.assertIn('#X_AVM-DE_GetHostListPath',post[1]['headers']['SOAPACTION']);self.assertNotIn(CONFIG['password'].encode(),post[1]['data'])
 def test_public_router_address_is_rejected(self):
  with patch('fritz.socket.getaddrinfo',return_value=[(socket.AF_INET,socket.SOCK_STREAM,6,'',('8.8.8.8',49000))]),self.assertRaises(ValueError):FritzClient(CONFIG,Session([]))
 def test_redirect_does_not_forward_authentication(self):
  client,session=self.client([Response(b'',302)])
  with self.assertRaisesRegex(RuntimeError,'Weiterleitung'):client.request('GET','/tr64desc.xml')
  self.assertEqual(len(session.calls),1)
 def test_wrong_credentials_have_german_error(self):
  client,_=self.client([Response(b'',401)])
  with self.assertRaisesRegex(RuntimeError,'Anmeldung abgelehnt'):client.request('GET','/tr64desc.xml')
 def test_xml_entities_are_rejected(self):
  with self.assertRaises(ValueError):parse_xml(b'<!DOCTYPE x [<!ENTITY secret "text">]><x>&secret;</x>')
 def test_external_hostlist_url_is_rejected(self):
  for path in ('http://evil.example/x','//evil.example/x','/../x','/\\evil'):
   with self.subTest(path=path),self.assertRaises(ValueError):safe_path(path)
 def test_only_getter_actions_are_allowed(self):
  client,session=self.client([])
  with self.assertRaises(ValueError):client.call('X_AVM-DE_SetHostNameByMACAddress',{'NewHostName':'bad'})
  self.assertEqual(session.calls,[])
 def test_fallback_reads_generic_host_entries(self):
  actions=b'<scpd><action><name>GetHostNumberOfEntries</name></action><action><name>GetGenericHostEntry</name></action></scpd>'
  client,_=self.client([Response(SERVICE),Response(actions),Response(soap('GetHostNumberOfEntries','<NewHostNumberOfEntries>1</NewHostNumberOfEntries>')),Response(soap('GetGenericHostEntry','<NewMACAddress>AA:BB:CC:DD:EE:FF</NewMACAddress><NewIPAddress>192.168.178.20</NewIPAddress><NewHostName>TV</NewHostName><NewActive>1</NewActive>'))])
  self.assertEqual(client.hosts()[0]['hostname'],'TV')
 def account(self):
  account=FritzAccount(Mock());account.hosts=[{'mac':'AA:BB:CC:DD:EE:FF','aliases':[],'ip':'192.168.178.20','hostname':'TV','active':True}];return account
 def test_exact_mac_matches_even_with_different_names(self):
  account=self.account();host=account.match({'id':'device','name':'Anderer Name','mac':'aabbccddeeff'});self.assertEqual(host['ip'],'192.168.178.20')
 def test_shared_public_ip_is_never_used_for_matching(self):
  account=self.account();self.assertIsNone(account.match({'id':'a','name':'TV','ip':'84.171.255.146'}));self.assertEqual(local_ip('84.171.255.146'),'')
 def test_subdevices_never_inherit_gateway_address(self):
  account=self.account();self.assertIsNone(account.match({'id':'sensor','mac':'AA:BB:CC:DD:EE:FF','sub':True}))
 def test_ambiguous_mac_is_not_guessed(self):
  account=self.account();account.hosts.append(dict(account.hosts[0],hostname='Anderer Eintrag'));self.assertIsNone(account.match({'id':'a','mac':'AA:BB:CC:DD:EE:FF'}))
 def test_inactive_entry_has_no_current_ip(self):
  account=self.account();account.hosts[0]['active']=False;self.assertEqual(account.match({'id':'a','mac':'AA:BB:CC:DD:EE:FF'})['ip'],'')
 def test_manual_association_is_saved_only_to_protected_vault(self):
  vault=Mock();account=self.account();account.vault=vault;account.remember=True;account.config=copy.deepcopy(CONFIG);account.bind('tuya-device','AA:BB:CC:DD:EE:FF')
  self.assertEqual(vault.save.call_args.args[0]['bindings']['tuya-device'],'AA:BB:CC:DD:EE:FF');self.assertTrue(account.match({'id':'tuya-device'})['manual'])
 def test_factory_mac_lookup_requests_only_known_devices_and_excludes_subdevices(self):
  api=Mock();api.request.return_value=[{'id':'d','mac':'aabbccddeeff','local_key':'not-for-ui'}];cloud=DirectCloud({},api);cloud.devices=[{'id':'d','sub':False,'mac':''},{'id':'sub','sub':True,'mac':''}]
  result=cloud.network_macs();self.assertEqual(result['macs'],{'d':'AA:BB:CC:DD:EE:FF'});self.assertNotIn('not-for-ui',str(result));api.request.assert_called_once_with('GET','/v1.0/devices/factory-infos',params={'device_ids':'d'})
if __name__=='__main__':unittest.main()
