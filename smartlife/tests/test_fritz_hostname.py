import sys,unittest,copy,threading
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock,patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
from fritz import FritzAccount,FritzClient,hostname,FritzFault
from test_fritz import Response,Session,RESOLVED,soap
from PySide6.QtWidgets import QApplication
from cloud_ui import DeviceAdminDialog
from main import Main,STYLE
class HostnameTests(unittest.TestCase):
 def account(self):
  account=FritzAccount(Mock());account.hosts=[{'mac':'AA:BB:CC:DD:EE:FF','aliases':[],'ip':'192.168.178.20','hostname':'old-name','active':True},{'mac':'11:22:33:44:55:66','aliases':[],'ip':'192.168.178.21','hostname':'other-host','active':True}]
  account.client=Mock();account.client.host.side_effect=[copy.deepcopy(account.hosts[0]),dict(account.hosts[0],hostname='tv-hintergrund')]
  return account
 def test_rename_checks_mac_then_writes_once_and_reads_same_host(self):
  account=self.account();device={'id':'tv','mac':'AA:BB:CC:DD:EE:FF'};other=copy.deepcopy(account.hosts[1]);result=account.rename_hostname(device,'TV-Hintergrund','AA:BB:CC:DD:EE:FF')
  self.assertEqual(result['hostname'],'tv-hintergrund');self.assertEqual(account.hosts[1],other)
  account.client.set_hostname.assert_called_once_with('AA:BB:CC:DD:EE:FF','TV-Hintergrund')
  self.assertEqual([call.args for call in account.client.host.call_args_list],[('AA:BB:CC:DD:EE:FF',),('AA:BB:CC:DD:EE:FF',)])
  account.client.hosts.assert_not_called()
 def test_changed_association_does_not_write(self):
  account=self.account()
  with self.assertRaisesRegex(RuntimeError,'Netzwerkzuordnung'):account.rename_hostname({'id':'tv','mac':'AA:BB:CC:DD:EE:FF'},'new-name','11:22:33:44:55:66')
  account.client.set_hostname.assert_not_called()
 def test_fresh_identity_mismatch_does_not_write(self):
  account=self.account();account.client.host.side_effect=[dict(account.hosts[0],mac='11:22:33:44:55:66')]
  with self.assertRaisesRegex(RuntimeError,'MAC-Adresse'):account.rename_hostname({'id':'tv','mac':'AA:BB:CC:DD:EE:FF'},'new-name')
  account.client.set_hostname.assert_not_called()
 def test_unchanged_readback_is_not_success(self):
  account=self.account();account.client.host.side_effect=[copy.deepcopy(account.hosts[0]),copy.deepcopy(account.hosts[0])]
  with self.assertRaisesRegex(RuntimeError,'nicht bestätigt'):account.rename_hostname({'id':'tv','mac':'AA:BB:CC:DD:EE:FF'},'new-name')
  self.assertEqual(account.hosts[0]['hostname'],'old-name');account.client.set_hostname.assert_called_once()
 def test_invalid_hostnames_never_write(self):
  for name in ('','tv licht','gerät','-tv','tv-','tv.fritz.box','a'*64):
   account=self.account()
   with self.subTest(name=name),self.assertRaises(ValueError):account.rename_hostname({'id':'tv','mac':'AA:BB:CC:DD:EE:FF'},name)
   account.client.set_hostname.assert_not_called()
 def test_documented_soap_setter_uses_mac_and_hostname(self):
  session=Session([Response(soap('X_AVM-DE_SetHostNameByMACAddress',''))])
  with patch('fritz.socket.getaddrinfo',return_value=RESOLVED):client=FritzClient({'address':'fritz.box','user':'user','password':'fake'},session)
  client.control='/upnp/control/hosts';client.actions={'X_AVM-DE_SetHostNameByMACAddress'};client.set_hostname('aabbccddeeff','tv-hintergrund')
  args,kwargs=session.calls[0];self.assertEqual(args[0],'POST');self.assertIn(b'<NewMACAddress>AA:BB:CC:DD:EE:FF</NewMACAddress>',kwargs['data']);self.assertIn(b'<NewHostName>tv-hintergrund</NewHostName>',kwargs['data'])
 def test_unsupported_setter_never_posts(self):
  session=Session([])
  with patch('fritz.socket.getaddrinfo',return_value=RESOLVED):client=FritzClient({'address':'fritz.box','user':'user','password':'fake'},session)
  client.control='/upnp/control/hosts';client.actions={'GetSpecificHostEntry'}
  with self.assertRaises(FritzFault):client.set_hostname('aabbccddeeff','tv-hintergrund')
  self.assertEqual(session.calls,[])
class HostnameDialogTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.app=QApplication.instance() or QApplication([]);cls.app.setStyleSheet(STYLE)
 def test_hostname_button_updates_fritz_column_without_tuya_or_full_reload(self):
  w=Main(True);w.navigate('Geräte');device=next(d for d in w.data['devices'] if d['id']=='s');device['mac']='AA:BB:CC:DD:EE:FF'
  w.cloud.direct=SimpleNamespace(rooms=[],background_pause=threading.Event());w.fritz=HostnameTests().account();w.submit=Mock();w.submit_fritz=lambda fn,done,fail:done(fn())
  with patch.object(w,'load') as load:
   dialog=DeviceAdminDialog(w,device);self.assertTrue(dialog.hostname_button.isEnabled());dialog.hostname.setText('tv-hintergrund');dialog.hostname_button.click();self.app.processEvents()
   self.assertIn('bestätigt',dialog.message.text());self.assertEqual(dialog.hostname.text(),'tv-hintergrund');w.submit.assert_not_called();load.assert_not_called()
   self.assertTrue(any(w.tree.topLevelItem(i).text(3)=='tv-hintergrund' for i in range(w.tree.topLevelItemCount())));dialog.close()
  w.close();self.app.processEvents()
if __name__=='__main__':unittest.main()
