import sys,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
from desktop_scenes import SceneStore,scene_rows,execute
from demo import sample
class SceneTests(unittest.TestCase):
 def setUp(self):self.temp=tempfile.TemporaryDirectory();self.store=SceneStore(self.temp.name);self.ds=sample()['devices'];self.action={'device':'s','code':'switch','value':True}
 def tearDown(self):self.temp.cleanup()
 def test_create_edit_reload(self):
  s=self.store.save('Abends','demo',[self.action],self.ds)
  edited=self.store.save('Abends neu','demo',[dict(self.action,value=False)],self.ds,s['id'])
  self.assertEqual(SceneStore(self.temp.name).all(),[edited]);self.assertEqual(s['id'],edited['id'])
 def test_invalid_function_not_saved(self):
  with self.assertRaises(ValueError):self.store.save('Falsch','demo',[dict(self.action,code='reset')],self.ds)
  self.assertFalse(self.store.path.exists())
 def test_save_never_executes(self):
  self.store.save('Licht','demo',[self.action],self.ds);self.assertEqual(len(self.store.all()),1)
 def test_preflight_no_partial_execution_if_offline(self):
  calls=[];ds=sample()['devices'];ds[1]['online']=False;cloud=SimpleNamespace(devices=ds,command=lambda *a:calls.append(a))
  with self.assertRaises(RuntimeError):execute({'home':'demo','actions':[self.action]},cloud)
  self.assertEqual(calls,[])
 def test_partial_failure_is_reported(self):
  calls=[]
  def send(*a):
   calls.append(a)
   if len(calls)==2:raise RuntimeError('Nicht erreichbar')
  cloud=SimpleNamespace(devices=self.ds,command=send)
  with self.assertRaisesRegex(RuntimeError,'nach 1 von 2'):execute({'home':'demo','actions':[self.action,dict(self.action,value=False)]},cloud)
 def test_cloud_action_view(self):
  rows=scene_rows({'actions':[{'entityId':'s','executorProperty':{'switch':True}}]},self.ds)
  self.assertEqual(rows[0][:3],('Steckdose Stehlampe','Ein/Aus','Ein'));self.assertEqual(rows[0][3],self.action)
 def test_unknown_actions_remain_visible_and_not_copied(self):
  rows=scene_rows({'actions':[{'entityId':'s','executorProperty':{'99':12}}]},self.ds)
  self.assertEqual(len(rows),1);self.assertIsNone(rows[0][3])
 def test_delete_preserves_other_scene(self):
  a=self.store.save('A','demo',[self.action],self.ds);b=self.store.save('B','demo',[self.action],self.ds);self.store.delete(a['id']);self.assertEqual(self.store.all(),[b])
if __name__=='__main__':unittest.main()
