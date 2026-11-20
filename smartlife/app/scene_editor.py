"""German editor for own scenes and read-only cloud action inspector."""
from copy import deepcopy
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QDialog,QVBoxLayout,QHBoxLayout,QLabel,QLineEdit,QComboBox,
 QPushButton,QTreeWidget,QTreeWidgetItem,QDoubleSpinBox,QWidget,QMessageBox)
from core import label,meta,fmt,enum_label,validate
from desktop_scenes import scene_rows
from ui_widgets import CleanSelectionDelegate

class SceneEditor(QDialog):
    def __init__(self,parent,store,home,devices,scene=None,cloud=False,save_handler=None,draft=False):
        super().__init__(parent);self.cloud=cloud;self.save_handler=save_handler;self.setWindowTitle('Desktop-Szene bearbeiten' if scene and scene.get('source')=='desktop' else 'Neue Desktop-Szene');self.resize(930,720)
        if cloud:self.setWindowTitle('Smart-Life-Szene bearbeiten' if scene else 'Neue Smart-Life-Szene')
        self.store=store;self.home=home;self.devices=[d for d in devices if d['home']==home];self.scene=scene;self.actions=deepcopy(scene.get('actions',[])) if scene else [];self.result_scene=None
        v=QVBoxLayout(self);note=QLabel('Diese Szene wird auf diesem PC gespeichert. Sie verändert keine vorhandene Smart-Life-Szene. Beim Ausführen werden die Geräte über Smart Life gesteuert.');note.setWordWrap(True)
        if cloud:note.setText('Die Szene wird direkt in deinem Smart-Life-Konto gespeichert und erscheint auch in der App. Speichern führt die Szene nicht aus.')
        if draft:note.setText('Geräteaktionen für die Automation bearbeiten. Erst „Automation speichern“ im Hauptfenster des Editors überträgt die Änderungen.')
        v.addWidget(note)
        self.name=QLineEdit(scene['name'] if scene else '');self.name.setPlaceholderText('Name der Szene');v.addWidget(self.name)
        self.tree=QTreeWidget();self.tree.setItemDelegate(CleanSelectionDelegate(self.tree));self.tree.setHeaderLabels(['Gerät','Funktion','Einstellung']);self.tree.setRootIsDecorated(False);self.tree.itemSelectionChanged.connect(self.select_action);v.addWidget(self.tree,1)
        selectors=QHBoxLayout();self.device=QComboBox();self.function=QComboBox();selectors.addWidget(self.device,1);selectors.addWidget(self.function,1);v.addLayout(selectors)
        for d in self.devices:
            if any(s.get('type','').lower() in ('boolean','enum','integer') for s in d['functions'].values()):self.device.addItem(d['name'],d['id'])
        self.value_area=QWidget();self.value_layout=QHBoxLayout(self.value_area);self.value_layout.setContentsMargins(0,0,0,0);v.addWidget(self.value_area)
        actions=QHBoxLayout();self.add=QPushButton('Aktion hinzufügen');self.add.clicked.connect(self.add_action);actions.addWidget(self.add)
        self.replace=QPushButton('Ausgewählte Aktion ändern');self.replace.clicked.connect(lambda:self.add_action(True));actions.addWidget(self.replace)
        remove=QPushButton('Aktion entfernen');remove.clicked.connect(self.remove_action);actions.addWidget(remove);v.addLayout(actions)
        order=QHBoxLayout()
        for title,delta in [('Nach oben',-1),('Nach unten',1)]:
            b=QPushButton(title);b.clicked.connect(lambda checked=False,d=delta:self.move_action(d));order.addWidget(b)
        order.addStretch();v.addLayout(order)
        bottom=QHBoxLayout();bottom.addStretch();save=QPushButton('Aktionen übernehmen' if draft else 'Szene speichern');save.clicked.connect(self.save);bottom.addWidget(save);cancel=QPushButton('Abbrechen');cancel.clicked.connect(self.reject);bottom.addWidget(cancel);v.addLayout(bottom)
        self.device.currentIndexChanged.connect(self.choose_device);self.function.currentIndexChanged.connect(self.choose_function);self.choose_device();self.render()
        if self.actions:self.tree.setCurrentItem(self.tree.topLevelItem(0))
    def selected_device(self):return next((d for d in self.devices if d['id']==self.device.currentData()),None)
    def choose_device(self):
        self.function.blockSignals(True);self.function.clear();d=self.selected_device()
        if d:
            for code,spec in d['functions'].items():
                if spec.get('type','').lower() in ('boolean','integer','enum'):self.function.addItem(label(code,spec),code)
        self.function.blockSignals(False);self.choose_function()
    def choose_function(self):
        while self.value_layout.count():
            item=self.value_layout.takeAt(0)
            if item.widget():item.widget().hide();item.widget().deleteLater()
        d=self.selected_device();code=self.function.currentData();self.value=None
        self.add.setEnabled(bool(d and code))
        if not d or not code:return
        spec=d['functions'][code];m=meta(spec);typ=spec['type'].lower()
        if typ in ('boolean','enum'):
            self.value=QComboBox()
            for value in ([True,False] if typ=='boolean' else m.get('range',[])):self.value.addItem(fmt(value,spec),value)
        else:
            self.value=QDoubleSpinBox();sc=max(0,min(6,int(m.get('scale',0))));self.value.setDecimals(sc);self.value.setRange(m.get('min',0)/10**sc,m.get('max',100)/10**sc);self.value.setSingleStep(max(1,m.get('step',1))/10**sc);self.value.setSuffix(' '+str(m.get('unit','')))
        self.value_layout.addWidget(QLabel('Gewünschte Einstellung:'));self.value_layout.addWidget(self.value,1)
    def value_to_raw(self):
        d=self.selected_device();spec=d['functions'][self.function.currentData()]
        if isinstance(self.value,QComboBox):return self.value.currentData()
        m=meta(spec);lo=int(m.get('min',0));st=max(1,int(m.get('step',1)));sc=int(m.get('scale',0));raw=lo+round((self.value.value()*10**sc-lo)/st)*st
        return validate(spec,raw)
    def add_action(self,replace=False):
        if self.value is None:return
        try:
            a={'device':self.device.currentData(),'code':self.function.currentData(),'value':self.value_to_raw()}
            if replace:
                i=self.tree.indexOfTopLevelItem(self.tree.currentItem())
                if i<0:raise ValueError('Bitte zuerst eine Aktion auswählen.')
                self.actions[i]=a
            else:self.actions.append(a)
            self.render()
        except (ValueError,KeyError) as e:QMessageBox.warning(self,'Szene',str(e))
    def render(self):
        self.tree.blockSignals(True);self.tree.clear()
        for name,code,value,_ in scene_rows({'actions':self.actions},self.devices):self.tree.addTopLevelItem(QTreeWidgetItem([name,code,value]))
        for c in range(3):self.tree.resizeColumnToContents(c)
        self.tree.blockSignals(False)
    def select_action(self):
        i=self.tree.indexOfTopLevelItem(self.tree.currentItem())
        if not 0<=i<len(self.actions):return
        a=self.actions[i]
        if '_raw' in a:
            self.replace.setEnabled(False);self.device.setCurrentIndex(-1);self.device.setPlaceholderText('Gerät für eine neue Aktion auswählen');return
        self.replace.setEnabled(True);self.device.setCurrentIndex(self.device.findData(a['device']));self.function.setCurrentIndex(self.function.findData(a['code']))
        if isinstance(self.value,QComboBox):self.value.setCurrentIndex(self.value.findData(a['value']))
        elif self.value is not None:
            spec=self.selected_device()['functions'][a['code']];self.value.setValue(a['value']/10**int(meta(spec).get('scale',0)))
    def remove_action(self):
        i=self.tree.indexOfTopLevelItem(self.tree.currentItem())
        if i>=0:self.actions.pop(i);self.render()
    def move_action(self,delta):
        i=self.tree.indexOfTopLevelItem(self.tree.currentItem());j=i+delta
        if i>=0 and 0<=j<len(self.actions):self.actions[i],self.actions[j]=self.actions[j],self.actions[i];self.render();self.tree.setCurrentItem(self.tree.topLevelItem(j))
    def save(self):
        name=self.name.text();home=self.home;actions=deepcopy(self.actions);sid=self.scene['id'] if self.scene and self.scene.get('source')=='desktop' else None
        def action():return self.store.save(name,home,actions,self.devices,sid)
        def done(result):self.result_scene=result;self.setEnabled(True);self.accept()
        def failed(e):self.setEnabled(True);QMessageBox.warning(self,'Szene speichern',str(e))
        if self.save_handler:
            self.setEnabled(False);self.save_handler(action,done,failed)
        else:
            try:done(action())
            except (ValueError,RuntimeError,OSError) as e:failed(e)

def question_de(parent,title,text):
    m=QMessageBox(parent);m.setWindowTitle(title);m.setText(text);m.setIcon(QMessageBox.Question);m.setStandardButtons(QMessageBox.Yes|QMessageBox.No);m.button(QMessageBox.Yes).setText('Ja');m.button(QMessageBox.No).setText('Nein');return m.exec()
