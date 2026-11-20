"""Offline UI preview only, never mixed with account data."""
def sample():
 def spec(code,typ,values):return {'code':code,'type':typ,'values':values}
 def dev(i,name,room,status,functions,ranges=None,online=True):return {'id':i,'name':name,'home':'demo','room_id':room,'room':room,'room_order':0,'category':'','online':online,'status':status,'functions':functions,'ranges':ranges or functions}
 b=spec('switch','Boolean',{})
 temp={'va_temperature':spec('va_temperature','Integer',{'scale':1,'unit':'°C'}),'va_humidity':spec('va_humidity','Integer',{'scale':0,'unit':'%'}),'battery_percentage':spec('battery_percentage','Integer',{'scale':0,'unit':'%'})}
 return {'homes':[{'id':'demo','name':'Mein Zuhause'}],'scenes':[{'id':'s1','name':'Abendbeleuchtung','home':'demo','enabled':True}], 'devices':[
 dev('t','Temperatursensor','Wohnzimmer',{'va_temperature':223,'va_humidity':48,'battery_percentage':86},{},temp),
 dev('s','Steckdose Stehlampe','Wohnzimmer',{'switch':True},{'switch':b}),
 dev('d','Dimmer Deckenlicht','Wohnzimmer',{'switch_led':True,'bright_value_v2':650},{'switch_led':spec('switch_led','Boolean',{}),'bright_value_v2':spec('bright_value_v2','Integer',{'min':10,'max':1000,'step':1,'scale':0})}),
 dev('r','Rollladen','Schlafzimmer',{'control':'stop','percent_state':75},{'control':spec('control','Enum',{'range':['open','stop','close']}),'percent_control':spec('percent_control','Integer',{'min':0,'max':100,'step':1,'unit':'%'})}),
 dev('a','Luftreiniger','Schlafzimmer',{'switch':True,'mode':'auto','pm25':12},{'switch':b,'mode':spec('mode','Enum',{'range':['auto','sleep','manual']}),'fan_speed_enum':spec('fan_speed_enum','Enum',{'range':['low','middle','high']})}),
 dev('o','Schalter Garten','Garten',{'switch':False},{'switch':b},online=False)]}
