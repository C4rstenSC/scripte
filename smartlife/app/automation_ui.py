"""Edit existing cloud automations while retaining unsupported original fields."""
from copy import deepcopy
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QDialog,QVBoxLayout,QHBoxLayout,QLabel,QLineEdit,QComboBox,
 QPushButton,QTreeWidget,QTreeWidgetItem,QDoubleSpinBox,QMessageBox,QFormLayout)
from core import label,meta,fmt,validate
from desktop_scenes import scene_rows,condition_rows,precondition_rows
from scene_editor import SceneEditor
from ui_widgets import CleanSelectionDelegate

class ConditionDialog(QDialog):
    def __init__(self,parent,devices,condition=None):
        super().__init__(parent);self.setWindowTitle('Auslösebedingung bearbeiten' if condition else 'Auslösebedingung hinzufügen');self.resize(680,330)
        self.devices=devices;self.original=deepcopy(condition);self.result_condition=None
        v=QVBoxLayout(self);form=QFormLayout();v.addLayout(form)
        self.device=QComboBox();self.function=QComboBox();self.operator=QComboBox();self.value_combo=QComboBox();self.value_number=QDoubleSpinBox()
        form.addRow('Gerät',self.device);form.addRow('Gemeldeter Wert',self.function);form.addRow('Vergleich',self.operator);form.addRow('Einstellung',self.value_combo);form.addRow('Grenzwert',self.value_number)
        for d in devices:
            if any(s.get('type','').lower() in ('integer','enum','boolean') for s in self.specs(d).values()):self.device.addItem(d['name'],d['id'])
        self.device.currentIndexChanged.connect(self.choose_device);self.function.currentIndexChanged.connect(self.choose_function);self.choose_device()
        row=QHBoxLayout();save=QPushButton('Bedingung übernehmen');save.clicked.connect(self.save);row.addWidget(save);cancel=QPushButton('Abbrechen');cancel.clicked.connect(self.reject);row.addWidget(cancel);v.addLayout(row)
        if condition:
            self.device.setCurrentIndex(self.device.findData(str(condition.get('entity_id'))));display=condition.get('display',{})
            self.function.setCurrentIndex(self.function.findData(display.get('code')));self.operator.setCurrentIndex(self.operator.findData(display.get('operator')))
            if self.spec():
                if self.spec()['type'].lower()=='integer':self.value_number.setValue(float(display['value'])/10**int(meta(self.spec()).get('scale',0)))
                else:self.value_combo.setCurrentIndex(self.value_combo.findData(display.get('value')))
    @staticmethod
    def specs(d):return {**d['functions'],**d.get('ranges',{})}
    def selected_device(self):return next((d for d in self.devices if d['id']==self.device.currentData()),None)
    def spec(self):
        d=self.selected_device();return self.specs(d).get(self.function.currentData()) if d else None
    def choose_device(self):
        self.function.blockSignals(True);self.function.clear();d=self.selected_device()
        if d:
            for code,spec in self.specs(d).items():
                if spec.get('type','').lower() in ('integer','boolean','enum'):self.function.addItem(label(code,spec),code)
        self.function.blockSignals(False);self.choose_function()
    def choose_function(self):
        self.operator.clear();self.value_combo.clear();spec=self.spec();typ=(spec or {}).get('type','').lower();numeric=typ=='integer'
        self.value_number.setVisible(numeric);self.value_combo.setVisible(not numeric)
        for text,value in ([('ist gleich','=='),('ist größer als','>'),('ist kleiner als','<')] if numeric else [('ist gleich','==')]):self.operator.addItem(text,value)
        if not spec:return
        m=meta(spec)
        if numeric:
            scale=int(m.get('scale',0));self.value_number.setDecimals(scale);self.value_number.setRange(m.get('min',0)/10**scale,m.get('max',100)/10**scale);self.value_number.setSingleStep(max(1,m.get('step',1))/10**scale);self.value_number.setSuffix(' '+str(m.get('unit','')))
        else:
            for value in ([True,False] if typ=='boolean' else m.get('range',[])):self.value_combo.addItem(fmt(value,spec),value)
    def save(self):
        try:
            spec=self.spec()
            if not spec:raise ValueError('Bitte ein Gerät und eine gemeldete Funktion auswählen.')
            if spec['type'].lower()=='integer':
                m=meta(spec);lo=int(m.get('min',0));step=max(1,int(m.get('step',1)));value=lo+round((self.value_number.value()*10**int(m.get('scale',0))-lo)/step)*step
            else:value=self.value_combo.currentData()
            validate(spec,value)
            c=deepcopy(self.original) if self.original else {'entity_type':1}
            c.update(entity_id=self.device.currentData(),entity_type=1,display={'code':self.function.currentData(),'operator':self.operator.currentData(),'value':value})
            self.result_condition=c;self.accept()
        except (ValueError,TypeError,KeyError) as e:QMessageBox.warning(self,'Bedingung',str(e))

class DraftActions:
    def save(self,name,home,actions,devices,scene_id=None):return {'actions':deepcopy(actions)}

class AutomationEditor(QDialog):
    def __init__(self,main,home,original=None):
        super().__init__(main);self.main=main;self.home=home;self.original=deepcopy(original);self.devices=[d for d in main.data['devices'] if d['home']==home]
        self.conditions=deepcopy((original or {}).get('conditions',[]));self.actions=[];self.result_rule=None
        for action in (original or {}).get('actions',[]):
            rows=scene_rows({'actions':[action]},self.devices)
            if rows and all(r[3] is not None for r in rows):self.actions.extend(r[3] for r in rows)
            else:self.actions.append({'_raw':deepcopy(action)})
        self.setWindowTitle('Automation bearbeiten' if original else 'Neue Automation');self.resize(1000,760);v=QVBoxLayout(self)
        note=QLabel('Änderungen werden in deinem Smart-Life-Konto gespeichert. Die Automation läuft dort anschließend entsprechend ihren Bedingungen weiter.');note.setWordWrap(True);v.addWidget(note)
        self.name=QLineEdit((original or {}).get('name',''));self.name.setPlaceholderText('Name der Automation');v.addWidget(self.name)
        self.match=QComboBox()
        for text,value in [('Mindestens eine Bedingung muss zutreffen',1),('Alle Bedingungen müssen zutreffen',2),('Eigene Bedingungsverknüpfung',3)]:self.match.addItem(text,value)
        self.match.setCurrentIndex(self.match.findData((original or {}).get('match_type',1)));v.addWidget(self.match)
        self.expression=QLineEdit((original or {}).get('condition_rule') or '');self.expression.setPlaceholderText('Zum Beispiel: 1&&2 oder 1||2 (Nummern aus der Bedingungsliste)');v.addWidget(self.expression);self.match.currentIndexChanged.connect(lambda:self.expression.setVisible(self.match.currentData()==3));self.expression.setVisible(self.match.currentData()==3)
        v.addWidget(QLabel('Wenn – Auslöser und Bedingungen'))
        self.condition_tree=QTreeWidget();self.condition_tree.setHeaderLabels(['Nr.','Gerät / Auslöser','Funktion','Vergleich / Einstellung']);self.condition_tree.setRootIsDecorated(False);self.condition_tree.setItemDelegate(CleanSelectionDelegate(self.condition_tree));v.addWidget(self.condition_tree,1)
        row=QHBoxLayout()
        for text,handler in [('Bedingung hinzufügen',lambda:self.edit_condition(False)),('Bedingung bearbeiten',lambda:self.edit_condition(True)),('Bedingung entfernen',self.remove_condition)]:
            b=QPushButton(text);b.clicked.connect(handler);row.addWidget(b)
        v.addLayout(row);v.addWidget(QLabel('Dann – Geräteaktionen'))
        self.action_tree=QTreeWidget();self.action_tree.setHeaderLabels(['Gerät','Funktion','Einstellung']);self.action_tree.setRootIsDecorated(False);self.action_tree.setItemDelegate(CleanSelectionDelegate(self.action_tree));v.addWidget(self.action_tree,1)
        edit=QPushButton('Geräteaktionen bearbeiten');edit.clicked.connect(self.edit_actions);v.addWidget(edit)
        for text in precondition_rows(original or {}):
            item=QLabel(text+' · bleibt erhalten');item.setWordWrap(True);v.addWidget(item)
        row=QHBoxLayout();row.addStretch();self.save_button=QPushButton('Automation speichern');self.save_button.clicked.connect(self.save);row.addWidget(self.save_button);cancel=QPushButton('Abbrechen');cancel.clicked.connect(self.reject);row.addWidget(cancel);v.addLayout(row);self.render()
    def render(self):
        self.condition_tree.clear();self.action_tree.clear()
        for c in self.conditions:
            rows=condition_rows({'conditions':[c]},self.devices)
            for name,function,value in rows:self.condition_tree.addTopLevelItem(QTreeWidgetItem([str(c.get('order_num','')),name,function,value]))
        for name,function,value,_ in scene_rows({'actions':self.actions},self.devices):self.action_tree.addTopLevelItem(QTreeWidgetItem([name,function,value]))
        for tree in (self.condition_tree,self.action_tree):
            for col in range(tree.columnCount()-1):tree.resizeColumnToContents(col)
    def edit_condition(self,existing):
        i=self.condition_tree.indexOfTopLevelItem(self.condition_tree.currentItem())
        c=self.conditions[i] if existing and 0<=i<len(self.conditions) else None
        if existing and c is None:return
        if c and (c.get('entity_type') not in (1,'1') or not isinstance(c.get('display'),dict)):
            QMessageBox.information(self,'Bedingung','Diese besondere Originalbedingung bleibt erhalten. Gerätebedingungen können ergänzt und bearbeitet werden.');return
        dialog=ConditionDialog(self,self.devices,c)
        if dialog.exec()!=QDialog.Accepted:return
        result=dialog.result_condition
        if existing:self.conditions[i]=result
        else:result['order_num']=max((c.get('order_num',0) for c in self.conditions),default=0)+1;self.conditions.append(result)
        self.render()
    def remove_condition(self):
        i=self.condition_tree.indexOfTopLevelItem(self.condition_tree.currentItem())
        if 0<=i<len(self.conditions):self.conditions.pop(i);self.render()
    def edit_actions(self):
        draft={'name':self.name.text(),'actions':self.actions,'source':'project'}
        dialog=SceneEditor(self,DraftActions(),self.home,self.devices,draft,cloud=True,draft=True)
        if dialog.exec()==QDialog.Accepted:self.actions=dialog.result_scene['actions'];self.render()
    def save(self):
        name=self.name.text();conditions=deepcopy(self.conditions);actions=deepcopy(self.actions);match=self.match.currentData();expression=self.expression.text();self.setEnabled(False)
        def done(result):self.result_rule=result;self.setEnabled(True);self.accept()
        def failed(e):self.setEnabled(True);QMessageBox.warning(self,'Automation speichern',str(e))
        self.main.submit(lambda:self.main.cloud.direct.save_automation(self.home,name,conditions,actions,match,self.original,expression),done,failed)
