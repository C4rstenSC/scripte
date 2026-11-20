from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from io import BytesIO
import json
import math
import os
from pathlib import Path
import sys
import time
from PySide6.QtCore import Qt, Signal, QObject, QTimer, QSettings
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import (QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLabel,
 QPushButton,QComboBox,QLineEdit,QTreeWidget,QTreeWidgetItem,QSplitter,QScrollArea,QFormLayout,
 QDoubleSpinBox,QSpinBox,QDialog,QCheckBox,QMessageBox,QFrame,QSizePolicy,QTabBar,QHeaderView,QPlainTextEdit,QFileDialog)
from core import VERSION, Cloud, ui_label as label,ui_control,unit_label, fmt, meta, ENUMS, validate, climate, TEMPERATURE_CODES, HUMIDITY_CODES, is_cover, cover_position, cover_text, enum_label, BATTERY_CODES, battery_text, probe_summary
import updates
from fritz import FritzAccount
from fritz_ui import FritzDialog
from ui_widgets import CleanSelectionDelegate,fit_columns,DeviceItem
from automation_ui import AutomationEditor
from desktop_scenes import SceneStore,execute as execute_desktop_scene,scene_rows,condition_rows,precondition_rows,scene_report
from scene_editor import SceneEditor,question_de
from cloud_ui import CloudSetupDialog,DeviceAdminDialog,RoomAdminDialog,CloudSceneStore

STYLE='''
QScrollBar:vertical {background:#e8edf2;width:20px;border:1px solid #aab3bd;margin:18px 0;}
QScrollBar:horizontal {background:#e8edf2;height:20px;border:1px solid #aab3bd;margin:0 18px;}
QScrollBar::handle {background:#657588;border:1px solid #405065;border-radius:5px;}
QScrollBar::handle:vertical {min-height:40px;}
QScrollBar::handle:horizontal {min-width:40px;}
QScrollBar::handle:hover {background:#3375ae;}
QScrollBar::handle:pressed {background:#215683;}
QScrollBar::add-page,QScrollBar::sub-page {background:#e8edf2;}
QScrollBar::add-line,QScrollBar::sub-line {background:#b8c4d1;border:1px solid #7b8b9c;}
QScrollBar::sub-line:vertical {height:18px;subcontrol-position:top;subcontrol-origin:margin;}
QScrollBar::add-line:vertical {height:18px;subcontrol-position:bottom;subcontrol-origin:margin;}
QScrollBar::sub-line:horizontal {width:18px;subcontrol-position:left;subcontrol-origin:margin;}
QScrollBar::add-line:horizontal {width:18px;subcontrol-position:right;subcontrol-origin:margin;}
QTabBar QToolButton {background:#d3dde7;color:#203447;border:1px solid #708399;min-width:22px;}

QWidget {font-family: "Segoe UI", "Arial"; font-size: 12pt; color:#24272d;}
QMainWindow,QDialog {background:#c8cbcf;}
QFrame#nav {background:#373a3f;} QFrame#nav QLabel {color:#f5f5f5;}
QPushButton {background:#e2e4e7;border:1px solid #9a9fa6;border-radius:5px;padding:9px 13px;min-height:20px;}
QPushButton:hover {background:#ccd1d7;} QPushButton:pressed {background:#858d98;}
QPushButton:checked {background:#555f6c;color:white;font-weight:bold;border-color:#788391;}
QPushButton[active="true"] {background:#198360;color:white;font-weight:bold;}
QPushButton:disabled {color:#8c9198;background:#d1d4d8;}
QLineEdit,QComboBox,QSpinBox,QDoubleSpinBox {background:#f3f4f5;border:1px solid #9a9fa6;border-radius:4px;padding:7px;min-height:22px;}
QPlainTextEdit,QTextEdit {background:#f3f4f5;color:#24272d;selection-background-color:#505b69;selection-color:#ffffff;border:1px solid #9a9fa6;padding:10px;}
QTreeWidget {background:#edf0f2;border:0;alternate-background-color:#e0e4e8;}
QHeaderView::section {background:#505358;color:white;padding:10px;border:0;font-weight:bold;}
QTreeWidget::item {padding:9px 5px;} QTreeWidget::item:selected {background:#bdcfe0;color:#1d2e3d;}
QFrame#detail {background:#e1e4e7;border-radius:8px;}
QTabBar::tab {background:#e2e4e7;color:#24272d;padding:12px 18px;border:1px solid #9a9fa6;margin-right:4px;}
QTabBar::tab:selected {background:#505b69;color:white;font-weight:bold;}
QComboBox QAbstractItemView {background:#f3f4f5;color:#24272d;selection-background-color:#505b69;selection-color:white;}
QLabel#title {font-size:22pt;font-weight:bold;} QLabel#subtitle {color:#626971;}
'''

class Bridge(QObject):
    done=Signal(object,object,object)

class Main(QMainWindow):
    def __init__(self,demo=False):
        super().__init__(); self.setWindowTitle('Smart Life Desktop · '+VERSION); self.resize(1390,900); self.setMinimumSize(1020,680)
        self.pool=ThreadPoolExecutor(max_workers=1); self.bridge=Bridge(); self.bridge.done.connect(self.complete)
        self.update_pool=ThreadPoolExecutor(max_workers=1);self.update_bridge=Bridge();self.update_bridge.done.connect(self.complete_update)
        self.fritz=FritzAccount();self.fritz_pool=ThreadPoolExecutor(max_workers=1);self.fritz_bridge=Bridge();self.fritz_bridge.done.connect(self.complete_fritz);self.fritz_matching=False;self.fritz_reading=False
        self.settings=QSettings('C4rstenSC','SmartLifeDesktop');self.cloud=Cloud(); self.demo=demo; self.closing=False; self.jobs=0; self.ready=False
        self.scene_store=SceneStore();self.data={'homes':[],'devices':[],'scenes':[]}; self.page='Übersicht'; self.pending=False; self.detail_id=None; self.login_dialog=None
        root=QWidget(); self.setCentralWidget(root); layout=QHBoxLayout(root); layout.setContentsMargins(0,0,0,0); layout.setSpacing(0)
        nav=QFrame(); nav.setObjectName('nav'); nav.setFixedWidth(205); nl=QVBoxLayout(nav); nl.setContentsMargins(18,26,18,20)
        brand=QLabel('Smart Life\nDesktop'); brand.setStyleSheet('font-size:23pt;font-weight:bold;'); nl.addWidget(brand)
        nl.addWidget(QLabel('Dein Zuhause im Blick')); nl.addSpacing(30); self.buttons={}
        for name in ['Übersicht','Räume','Geräte','Szenen','Automationen']:
            b=QPushButton(name); b.setCheckable(True); b.clicked.connect(lambda checked=False,n=name:self.navigate(n)); nl.addWidget(b); self.buttons[name]=b
        nl.addStretch(); login=QPushButton('Konto / Anmeldung'); login.clicked.connect(self.login); nl.addWidget(login)
        direct_button=QPushButton('Direkter Cloudzugriff');direct_button.clicked.connect(self.setup_direct);nl.addWidget(direct_button)
        self.fritz_button=QPushButton('FRITZ!Box anmelden');self.fritz_button.clicked.connect(self.fritz_login);nl.addWidget(self.fritz_button)
        self.fritz_status=QLabel('FRITZ!Box · nicht verbunden');self.fritz_status.setWordWrap(True);nl.addWidget(self.fritz_status)
        self.update_btn=QPushButton('Update'); self.update_btn.clicked.connect(lambda:self.check_update(True)); nl.addWidget(self.update_btn)
        self.update_note=QLabel(''); self.update_note.setWordWrap(True);self.update_note.setMinimumHeight(50);self.update_note.setStyleSheet('color:#e2e4e7;'); nl.addWidget(self.update_note); nl.addWidget(QLabel('Version '+VERSION)); layout.addWidget(nav)
        nav.setFixedWidth(max(260,direct_button.sizeHint().width()+36,login.sizeHint().width()+36))
        body=QWidget(); bl=QVBoxLayout(body); bl.setContentsMargins(24,22,24,18); bl.setSpacing(16); layout.addWidget(body,1)
        top=QHBoxLayout(); self.title=QLabel('Dein Zuhause'); self.title.setObjectName('title'); top.addWidget(self.title); top.addStretch(); self.account=QLabel('Smart Life · nicht verbunden'); top.addWidget(self.account); bl.addLayout(top)
        self.status=QLabel('Bitte mit dem Benutzercode aus deiner Smart-Life-App anmelden.'); self.status.setWordWrap(True); bl.addWidget(self.status)
        self.home=QComboBox();self.home.hide();self.home.currentIndexChanged.connect(self.change_home)
        self.room=QComboBox();self.room.hide();self.room.currentIndexChanged.connect(self.render)
        self.search=QLineEdit();self.search.hide();self.search.textChanged.connect(self.render)
        self.new_scene_btn=QPushButton('Neue Szene erstellen');self.new_scene_btn.clicked.connect(lambda:self.edit_automation() if self.page=='Automationen' else self.edit_scene());self.new_scene_btn.hide();top.addWidget(self.new_scene_btn)
        self.manage_rooms_btn=QPushButton('Räume verwalten');self.manage_rooms_btn.clicked.connect(self.manage_rooms);self.manage_rooms_btn.hide();top.addWidget(self.manage_rooms_btn)
        self.reload=QPushButton('Neu laden');self.reload.clicked.connect(self.load);top.addWidget(self.reload)
        self.home_tabs=QTabBar();self.home_tabs.setExpanding(False);self.home_tabs.currentChanged.connect(self.select_home_tab);bl.addWidget(self.home_tabs)
        self.room_tabs=QTabBar();self.room_tabs.setMovable(True);self.room_tabs.tabMoved.connect(self.save_room_tab_order);self.room_tabs.setExpanding(False);self.room_tabs.setUsesScrollButtons(True);self.room_tabs.currentChanged.connect(self.select_room_tab);bl.addWidget(self.room_tabs)
        self.climate_tree=QTreeWidget();self.climate_tree.setHeaderLabels(['Raum','Sensor','Temperatur','Luftfeuchte','Verbindung']);self.climate_tree.setRootIsDecorated(False);self.climate_tree.setAlternatingRowColors(True);self.climate_tree.setSortingEnabled(True);self.climate_tree.setStyleSheet('QTreeWidget::item {padding:14px 10px;}');self.climate_tree.header().setSectionResizeMode(QHeaderView.ResizeToContents);self.climate_tree.header().setStretchLastSection(True);bl.addWidget(self.climate_tree,1)
        self.summary=QLabel(''); bl.addWidget(self.summary)
        self.split=QSplitter(); bl.addWidget(self.split,1)
        self.tree=QTreeWidget(); self.tree.setAlternatingRowColors(True); self.tree.setRootIsDecorated(False); self.tree.setSortingEnabled(True)
        self.tree.setItemDelegate(CleanSelectionDelegate(self.tree));self.climate_tree.setItemDelegate(CleanSelectionDelegate(self.climate_tree))
        self.tree.itemSelectionChanged.connect(self.selected); self.split.addWidget(self.tree)
        self.detail=QFrame(); self.detail.setObjectName('detail'); self.dl=QVBoxLayout(self.detail); self.dl.setContentsMargins(18,18,18,18)
        scroll=QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.NoFrame); scroll.setWidget(self.detail); scroll.setMinimumWidth(300); self.split.addWidget(scroll); self.split.setSizes([740,380])
        self.clock=QLabel(''); self.clock.setAlignment(Qt.AlignRight); bl.addWidget(self.clock)
        self.tick=QTimer(self); self.tick.timeout.connect(lambda:self.clock.setText(datetime.now().strftime('%H:%M:%S   %d.%m.%Y'))); self.tick.start(1000)
        self.poll=QTimer(self); self.poll.setInterval(30000); self.poll.timeout.connect(self.refresh)
        self.fritz_timer=QTimer(self);self.fritz_timer.setInterval(60000);self.fritz_timer.timeout.connect(self.refresh_fritz)
        self.update_timer=QTimer(self); self.update_timer.timeout.connect(lambda:self.check_update(False)); self.update_timer.start(60000)
        self.navigate('Übersicht'); self.empty_detail()
        if demo: self.demo_data()
        else: QTimer.singleShot(250,self.restore); QTimer.singleShot(1500,lambda:self.check_update(False));QTimer.singleShot(500,self.restore_fritz)
    def submit_fritz(self,fn,success,failure):
        if self.closing:return
        future=self.fritz_pool.submit(fn)
        def finish(f):
            try:value,error=f.result(),None
            except Exception as e:value,error=None,e
            if not self.closing:self.fritz_bridge.done.emit(value,error,(success,failure))
        future.add_done_callback(finish)
    def complete_fritz(self,value,error,callbacks):
        if self.closing:return
        success,failure=callbacks
        if error:failure(error)
        else:success(value)
    def fritz_login(self):
        self.begin_edit()
        try:FritzDialog(self).exec()
        finally:self.end_edit()
    def restore_fritz(self):
        def done(ok):
            if ok:self.fritz_connected()
        self.submit_fritz(self.fritz.restore,done,lambda e:self.fritz_status.setText('FRITZ!Box · '+str(e)))
    def fritz_connected(self,retry=False):
        self.fritz_status.setText('FRITZ!Box · verbunden');self.fritz_timer.start();self.render();self.read_network_macs(retry)
    def refresh_fritz(self):
        if not self.fritz.client or self.fritz_reading:return
        self.fritz_reading=True
        def done(_):self.fritz_reading=False;self.render()
        def failed(e):self.fritz_reading=False;self.fritz_status.setText('FRITZ!Box · '+str(e));self.render()
        self.submit_fritz(self.fritz.refresh,done,failed)
    def read_network_macs(self,retry=False):
        if not self.fritz.client or not self.cloud.direct or not self.data['devices'] or self.fritz_matching:return
        self.fritz_matching=True;direct=self.cloud.direct
        def done(result):
            self.fritz_matching=False
            for device in self.data['devices']:
                if device['id'] in result['macs']:device['mac']=result['macs'][device['id']]
            matched=sum(bool(self.fritz.match(d)) for d in self.data['devices']);self.fritz_status.setText('FRITZ!Box · '+str(matched)+' Geräte zugeordnet'+(' · '+result['warnings'][0] if result.get('warnings') else ''));self.render()
        def failed(e):self.fritz_matching=False;self.fritz_status.setText('FRITZ!Box · Zuordnung fehlgeschlagen: '+str(e))
        def worker():
            if retry:direct.mac_attempted.clear()
            return direct.network_macs()
        self.submit(worker,done,failed)
    def refresh_fritz_device(self,device):
        if not self.fritz.client:return
        self.submit_fritz(lambda:self.fritz.refresh_device(device),lambda _:self.render(),lambda e:self.fritz_status.setText('FRITZ!Box · '+str(e)))
    def submit(self,fn,callback=None,error=None):
        if self.closing: return
        self.jobs+=1
        f=self.pool.submit(fn)
        def finish(f):
            try: result,exc=f.result(),None
            except Exception as e: result,exc=None,e
            if not self.closing:
                self.bridge.done.emit(result,exc,(callback,error))
        f.add_done_callback(finish)
    def complete(self,value,exc,callbacks):
        self.jobs=max(0,self.jobs-1)
        if self.closing:return
        success,error=callbacks
        if exc:
            if error:error(exc)
            else:self.error(exc)
        elif success: success(value)
    def error(self,e):
        self.status.setText('Fehler: '+str(e)); QMessageBox.warning(self,'Smart Life Desktop',str(e))
    def restore(self):
        self.submit(self.cloud.restore,lambda ok:self.connected() if ok else self.login(),lambda e:(self.status.setText('Gespeicherte Anmeldung konnte nicht geladen werden.'),self.login()))
    def connected(self):
        self.account.setText('Smart Life · direkter Cloudzugriff' if self.cloud.direct else 'Smart Life · QR-Verbindung'); self.ready=True; self.load(); self.poll.start()
    def load(self):
        if self.demo:return
        if not self.ready:self.login();return
        if self.pending:return
        self.pending=True; self.reload.setEnabled(False); self.status.setText('Zuhause, Räume und Geräte werden geladen …')
        def done(data):
            self.pending=False; self.reload.setEnabled(True); self.data=data; self.populate_homes();self.read_network_macs()
            notes=[]
            if data.get('room_failed'):notes.append(f"Raumzuordnung für {data['room_failed']} Gerät(e) konnte nicht gelesen werden; bitte erneut laden.")
            if data.get('scene_error'):notes.append('Szenen konnten nicht gelesen werden.')
            if data.get('warnings'):notes.extend(data['warnings'][:3])
            self.status.setText('Verbunden · Stand '+datetime.now().strftime('%H:%M:%S')+(' · '+' '.join(notes) if notes else ''))
        def failed(e):self.pending=False;self.reload.setEnabled(True);self.error(e)
        self.submit(self.cloud.load,done,failed)
    def refresh(self):
        if not self.ready or self.pending or self.jobs or self.demo or getattr(self,'device_editing',False):return
        self.pending=True
        def done(ds):
            self.pending=False; self.data['devices']=ds; self.render(); self.status.setText('Verbunden · Datenstand '+datetime.now().strftime('%H:%M:%S'))
        def failed(e):self.pending=False;self.status.setText('Status nicht aktuell: '+str(e))
        self.submit(self.cloud.refresh,done,failed)
    def refresh_device(self,device_id):
        if not self.ready or self.pending or self.jobs or self.demo or getattr(self,'device_editing',False):return
        def done(devices):
            self.data['devices']=devices;self.render();self.status.setText('Gerätestatus aktualisiert · '+datetime.now().strftime('%H:%M:%S'))
        self.submit(lambda:self.cloud.refresh(device_id),done,lambda e:self.status.setText(str(e)))
    def populate_homes(self):
        prior=self.home.currentData(); self.home.blockSignals(True);self.home.clear()
        for h in self.data['homes']:self.home.addItem(h['name'],h['id'])
        ix=self.home.findData(prior);self.home.setCurrentIndex(max(0,ix));self.home.blockSignals(False)
        self.home_tabs.blockSignals(True)
        while self.home_tabs.count():self.home_tabs.removeTab(0)
        for h in self.data['homes']:self.home_tabs.addTab(h['name'])
        self.home_tabs.setCurrentIndex(self.home.currentIndex());self.home_tabs.setVisible(len(self.data['homes'])>1);self.home_tabs.blockSignals(False);self.change_home()
    def change_home(self):
        self.title.setText(self.home.currentText() or 'Dein Zuhause'); prior=self.room.currentData();self.room.blockSignals(True);self.room.clear();self.room.addItem('Alle Räume',None)
        rooms={}
        for d in self.data['devices']:
            if d['home']==self.home.currentData() and d['room_id']:rooms[d['room_id']]=(d['room'],d.get('room_order',0))
        for r in self.data.get('rooms',[]):
            if r['home']==self.home.currentData():rooms.setdefault(r['id'],(r['name'],0))
        for rid,(name,order) in sorted(rooms.items(),key=lambda p:(p[1][1],p[1][0].casefold())):self.room.addItem(name,rid)
        self.room.addItem('Ohne Raumzuordnung',''); ix=self.room.findData(prior);self.room.setCurrentIndex(max(0,ix));self.room.blockSignals(False)
        self.room_tabs.blockSignals(True)
        while self.room_tabs.count():self.room_tabs.removeTab(0)
        try:order=json.loads(self.settings.value('room-order/'+str(self.home.currentData()),'[]'))
        except (ValueError,TypeError):order=[]
        indices=list(range(self.room.count()));indices.sort(key=lambda i:order.index(self.room.itemData(i)) if self.room.itemData(i) in order else len(order)+i)
        for i in indices:
            tab=self.room_tabs.addTab(self.room.itemText(i));self.room_tabs.setTabData(tab,self.room.itemData(i))
        selected=next((i for i in range(self.room_tabs.count()) if self.room_tabs.tabData(i)==self.room.currentData()),0)
        self.room_tabs.setCurrentIndex(selected);self.room_tabs.blockSignals(False);self.render();self.selected() if self.tree.selectedItems() and self.page!='Übersicht' else self.empty_detail()
    def select_home_tab(self,index):
        if index>=0:self.home.setCurrentIndex(index)
    def select_room_tab(self,index):
        if index>=0:self.room.setCurrentIndex(self.room.findData(self.room_tabs.tabData(index)))
    def save_room_tab_order(self,*_):
        order=[self.room_tabs.tabData(i) for i in range(self.room_tabs.count())]
        self.settings.setValue('room-order/'+str(self.home.currentData()),json.dumps(order));self.settings.sync()
    def navigate(self,page):
        if not hasattr(self,"page_sorts"):self.page_sorts={}
        self.page_sorts[self.page]=(self.tree.sortColumn(),self.tree.header().sortIndicatorOrder())
        self.page=page
        column,order=self.page_sorts.get(page,(1 if page=="Räume" else 0,Qt.AscendingOrder))
        self.tree.header().setSortIndicator(column,order)
        for n,b in self.buttons.items():b.setChecked(n==page)
        self.manage_rooms_btn.setVisible(page=='Räume');self.new_scene_btn.setVisible(page in ('Szenen','Automationen'));self.new_scene_btn.setText('Neue Automation erstellen' if page=='Automationen' else 'Neue Szene erstellen');self.room_tabs.setVisible(page=='Räume'); self.render();self.selected() if self.tree.selectedItems() and self.page!='Übersicht' else self.empty_detail()
    def visible_devices(self):
        home=self.home.currentData(); room=self.room.currentData() if self.page=='Räume' else None; search=self.search.text().casefold()
        return [d for d in self.data['devices'] if d['home']==home and (room is None or d['room_id']==room) and search in (d['name']+' '+d['room']).casefold()]
    def render(self,*_):
        overview=self.page=='Übersicht';self.climate_tree.setVisible(overview);self.split.setVisible(not overview)
        if overview:
            self.render_climate();return
        selected=self.detail_id; self.tree.blockSignals(True);self.tree.clear()
        if self.page in ('Szenen','Automationen'):
            automation=self.page=='Automationen'
            self.tree.setColumnCount(3);self.tree.setHeaderLabels(['Automation' if automation else 'Szene','Speicherort','Status'])
            try:local=self.scene_store.all()
            except RuntimeError as e:local=[];self.status.setText(str(e))
            for s in (self.data.get('automations',[]) if automation else self.data['scenes']+local):
                if s['home']==self.home.currentData() and self.search.text().casefold() in s['name'].casefold():
                    state=('Aktiviert' if s['enabled'] is True else 'Deaktiviert' if s['enabled'] is False else '') if automation else ('Verfügbar' if s['enabled'] else 'Deaktiviert')
                    it=QTreeWidgetItem([s['name'],'Dieser PC' if s.get('source')=='desktop' else 'Smart Life',state]);it.setData(0,Qt.UserRole,s);self.tree.addTopLevelItem(it)
                    if s['id']==selected:it.setSelected(True)
            self.summary.setText(f'{self.tree.topLevelItemCount()} '+('Automationen' if automation else 'Szenen'))
            if automation and not self.cloud.direct and not self.demo:self.summary.setText('Automationen erfordern den direkten Cloudzugriff.')
            elif automation and self.data.get('automation_errors'):self.summary.setText(' · '.join(self.data['automation_errors']))
        else:
            self.tree.setColumnCount(7);self.tree.setHeaderLabels(['Gerät','Raum','Lokale IP-Adresse','FRITZ!Box-Hostname','Verbindung','Batteriestatus','Werte / Zustand'])
            ds=self.visible_devices()
            for d in ds:
                summary=' · '.join(label(k,d['ranges'].get(k))+': '+fmt(v,d['ranges'].get(k)) for k,v in d['status'].items() if k in LABEL_SUMMARY and k not in BATTERY_CODES and label(k,d['ranges'].get(k)))
                if not summary:summary=' · '.join(label(k,d['ranges'].get(k))+': '+fmt(v,d['ranges'].get(k)) for k,v in [(k,v) for k,v in d['status'].items() if k not in BATTERY_CODES and label(k,d['ranges'].get(k))][:3])
                if is_cover(d) and (cover_position(d) is not None or any(c in d['status'] for c in ('percent_control','percent_control_1'))):summary=cover_text(d)
                network=self.fritz.match(d);ip=network['ip'] if network else '';hostname=network['hostname'] if network else ''
                it=DeviceItem([d['name'],d['room'] or 'Ohne Raumzuordnung',ip,hostname,'Online' if d['online'] else 'Offline',battery_text(d),summary]);it.setData(0,Qt.UserRole,d);self.tree.addTopLevelItem(it)
                if network:
                    if network.get('last_known'):
                        it.setText(2,ip+' (zuletzt bekannt)');it.setToolTip(2,'In der FRITZ!Box gespeicherte IP-Adresse. Das Gerät wird dort derzeit als inaktiv gemeldet; die aktuelle Erreichbarkeit ist damit nicht bestätigt.')
                    elif network.get('ip_conflict'):it.setToolTip(2,'Die gespeicherte IP-Adresse ist laut FRITZ!Box derzeit einem anderen aktiven Gerät zugeordnet und wird deshalb nicht als Geräteadresse angezeigt.')
                    elif not ip:it.setToolTip(2,'Für diesen Netzwerkeintrag meldet die FRITZ!Box keine lokale IP-Adresse.')
                if d['id']==selected:it.setSelected(True)
            self.summary.setText(f'{len(ds)} Geräte · {sum(d["online"] for d in ds)} online · {len(ds)-sum(d["online"] for d in ds)} offline')
        fit_columns(self.tree)
        self.tree.blockSignals(False)
        if self.tree.selectedItems() and self.page not in ('Szenen','Automationen') and hasattr(self,'values_widget'):
            d=self.tree.selectedItems()[0].data(0,Qt.UserRole)
            if is_cover(d) and hasattr(self,'cover_label'):
                try:self.cover_label.setText(cover_text(d))
                except RuntimeError:pass
            try:
                reported='\n'.join(label(c,d['ranges'].get(c))+': '+fmt(v,d['ranges'].get(c)) for c,v in d['status'].items() if v is not None and not isinstance(v,(dict,list)) and c!='filter_reset' and label(c,d['ranges'].get(c)))
                self.values_widget.setText(reported);self.values_widget.setVisible(bool(reported));self.values_heading.setVisible(bool(reported))
            except RuntimeError:pass
            for b,c,v in getattr(self,'live_buttons',[]):
                try:
                    b.setProperty('active',d['status'].get(c)==v);b.style().unpolish(b);b.style().polish(b)
                except RuntimeError:pass
        if not self.tree.selectedItems():self.empty_detail()
    def render_climate(self):
        self.climate_tree.clear();ds=self.visible_devices();count=0
        rooms={}
        for d in ds:rooms.setdefault(d['room'] or 'Ohne Raumzuordnung',[]).append(d)
        for room,devices in sorted(rooms.items(),key=lambda x:x[0].casefold()):
            sensors=[d for d in devices if any(c in d['status'] for c in TEMPERATURE_CODES+HUMIDITY_CODES)]
            if not sensors:continue
            for d in sensors:
                self.climate_tree.addTopLevelItem(QTreeWidgetItem([room,d['name'],climate(d,TEMPERATURE_CODES,'°C'),climate(d,HUMIDITY_CODES,'%'),'Online' if d['online'] else 'Offline · letzter gemeldeter Wert']))
                count+=1
        self.climate_tree.sortItems(0,Qt.AscendingOrder);fit_columns(self.climate_tree);self.summary.setText(f'Temperatur und Luftfeuchte · {count} Sensoren')
    def clear_detail(self):
        while self.dl.count():
            item=self.dl.takeAt(0)
            if item.widget():item.widget().hide();item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    c=item.layout().takeAt(0)
                    if c.widget():c.widget().hide();c.widget().deleteLater()
    def empty_detail(self):
        self.detail_id=None; self.clear_detail();l=QLabel('Gerät oder Szene auswählen');l.setWordWrap(True);self.dl.addWidget(l);self.dl.addStretch()
    def selected(self):
        rows=self.tree.selectedItems()
        if not rows:return
        d=rows[0].data(0,Qt.UserRole);self.clear_detail()
        title=QLabel(d['name']);title.setStyleSheet('font-size:16pt;font-weight:bold;');title.setWordWrap(True);self.dl.addWidget(title)
        if self.page in ('Szenen','Automationen'):
            self.detail_id=d['id'];self.show_scene_details(d);return
        self.detail_id=d['id'];self.live_buttons=[];
        if is_cover(d) and (cover_position(d) is not None or any(c in d['status'] for c in ('percent_control','percent_control_1'))):
            position=QLabel(cover_text(d));position.setWordWrap(True);position.setStyleSheet('font-size:16pt;font-weight:bold;padding:8px 0;');self.dl.addWidget(position);self.cover_label=position
        self.dl.addWidget(QLabel((d['room'] or 'Ohne Raumzuordnung')+' · '+('Online' if d['online'] else 'Offline')))
        probe=QPushButton('Gerätedaten prüfen');probe.setEnabled(not self.demo);probe.clicked.connect(lambda:self.probe_device(d,probe));self.dl.addWidget(probe)
        edit_device=QPushButton('Gerätename und Raum bearbeiten');edit_device.clicked.connect(lambda:self.edit_device(d));self.dl.addWidget(edit_device)
        for code,spec in d['functions'].items():
            typ=spec.get('type','').lower();m=meta(spec);current=d['status'].get(code)
            if not ui_control(code,spec):continue
            frame=QWidget();fl=QVBoxLayout(frame);fl.setContentsMargins(0,8,0,4)
            function_title=QLabel('Zielposition (% offen)' if is_cover(d) and code in ('percent_control','percent_control_1','position') else label(code,spec));function_title.setWordWrap(True);fl.addWidget(function_title)
            if typ=='boolean' and code=='filter_reset':
                b=QPushButton('Filterzähler zurücksetzen')
                def reset_filter(checked=False,c=code,w=frame):
                    if question_de(self,'Filterzähler zurücksetzen','Wurde der Filter gewechselt und soll der Zähler zurückgesetzt werden?')==QMessageBox.Yes:self.command(d,c,True,w)
                b.clicked.connect(reset_filter);fl.addWidget(b)
            elif typ=='boolean':
                row=QHBoxLayout()
                for value,title in [(True,'Ein'),(False,'Aus')]:
                    b=QPushButton(title);b.setProperty('active',current is value);self.live_buttons.append((b,code,value));b.clicked.connect(lambda checked=False,c=code,v=value,w=frame:self.command(d,c,v,w));row.addWidget(b)
                fl.addLayout(row)
            elif typ=='enum':
                choices=m.get('range',[])
                if set(choices).issubset({'open','close','stop'}) and choices:
                    row=QHBoxLayout()
                    for v in choices:
                        b=QPushButton(enum_label(v,code));b.setProperty('active',current==v);self.live_buttons.append((b,code,v));b.clicked.connect(lambda checked=False,c=code,v=v,w=frame:self.command(d,c,v,w));row.addWidget(b)
                    fl.addLayout(row)
                else:
                    box=QComboBox()
                    for v in choices:box.addItem(enum_label(v,code),v)
                    box.setCurrentIndex(max(0,box.findData(current)));fl.addWidget(box);b=QPushButton('Übernehmen');b.clicked.connect(lambda checked=False,c=code,w=frame,box=box:self.command(d,c,box.currentData(),w));fl.addWidget(b)
            else:
                lo=int(m.get('min',0));hi=int(m.get('max',100));step=max(1,int(m.get('step',1)));scale=max(0,min(6,int(m.get('scale',0))))
                box=QDoubleSpinBox();box.setDecimals(scale);box.setRange(lo/10**scale,hi/10**scale);box.setSingleStep(step/10**scale);box.setSuffix(' '+unit_label(m.get('unit','')))
                if current is not None:
                    try:box.setValue(float(current)/10**scale)
                    except (ValueError,TypeError):pass
                fl.addWidget(box);b=QPushButton('Übernehmen');b.clicked.connect(lambda checked=False,c=code,w=frame,box=box,sc=scale,lo=lo,st=step:self.command(d,c,lo+round((box.value()*10**sc-lo)/st)*st,w));fl.addWidget(b)
            frame.setEnabled(d['online'] and not self.demo);self.dl.addWidget(frame)
        reported='\n'.join(label(c,d['ranges'].get(c))+': '+fmt(v,d['ranges'].get(c)) for c,v in d['status'].items() if v is not None and not isinstance(v,(dict,list)) and c!='filter_reset' and label(c,d['ranges'].get(c)))
        self.values_heading=QLabel('Gemeldete Werte');self.values_heading.setVisible(bool(reported));self.dl.addWidget(self.values_heading)
        self.values_widget=QLabel(reported);self.values_widget.setVisible(bool(reported));self.values_widget.setWordWrap(True);self.values_widget.setTextInteractionFlags(Qt.TextSelectableByMouse);self.dl.addWidget(self.values_widget);self.dl.addStretch()
    def show_scene_details(self,s):
        if s.get('source')=='automation':
            self.dl.addWidget(QLabel('Wenn – Auslöser und Bedingungen'))
            self.dl.addWidget(QLabel('Alle Bedingungen müssen zutreffen' if s.get('match_type') in (2,'2','and') else 'Mindestens eine Bedingung muss zutreffen' if s.get('match_type') in (1,'1','or') else ''))
            if s.get('match_type') in (3,'3'):
                rule=QLabel('Eigene Bedingungsverknüpfung: '+str(s.get('condition_rule') or 'noch nicht geliefert'));rule.setWordWrap(True);self.dl.addWidget(rule)
            for name,function,value in condition_rows(s,self.data['devices']):
                row=QLabel(name+'\n'+function+': '+value);row.setWordWrap(True);self.dl.addWidget(row)
            for text in precondition_rows(s):
                pre=QLabel(text);pre.setWordWrap(True);self.dl.addWidget(pre)
            self.dl.addWidget(QLabel('Dann – Geräteaktionen'))
            for name,function,value,_ in scene_rows(s,self.data['devices']):
                row=QLabel(name+'\n'+function+': '+value);row.setWordWrap(True);self.dl.addWidget(row)
            edit=QPushButton('Automation bearbeiten');edit.clicked.connect(lambda:self.edit_automation(s));self.dl.addWidget(edit)
            self.add_scene_report_button(s);self.dl.addStretch();return
        own=s.get('source')=='desktop'
        note=QLabel('Desktop-Szene · auf diesem PC gespeichert' if own else ('Smart-Life-Szene · direkt im Konto bearbeitbar' if s.get('source')=='project' else 'Smart-Life-Szene · über die QR-Anbindung schreibgeschützt'));note.setWordWrap(True);self.dl.addWidget(note)
        rows=scene_rows(s,self.data['devices'])
        if not rows:
            info=QLabel('Keine Geräteaktionen von Smart Life bereitgestellt.' if not own else 'Keine Geräteaktionen gespeichert.');info.setWordWrap(True);self.dl.addWidget(info)
        for name,function,value,_ in rows:
            detail=QLabel(name+'\n'+function+': '+value);detail.setWordWrap(True);detail.setStyleSheet('padding:10px 0;border-bottom:1px solid #abb0b7;');self.dl.addWidget(detail)
        run=QPushButton('Szene ausführen');run.setEnabled(s['enabled'] and not self.demo);run.clicked.connect(lambda:self.scene(s,run));self.dl.addWidget(run)
        edit=QPushButton('Szene bearbeiten' if own or s.get('source')=='project' else 'Cloudzugriff für Bearbeitung einrichten');edit.setEnabled(True);edit.clicked.connect(lambda:self.edit_scene(s));self.dl.addWidget(edit)
        if not own:self.add_scene_report_button(s)
        if not own and s.get('source')!='project':
            why=QLabel('Änderungen an dieser Smart-Life-Szene erfolgen in der Smart-Life-App. Eine bearbeitbare Desktop-Kopie ist möglich, wenn alle Geräteaktionen eindeutig zugeordnet werden können.');why.setWordWrap(True);self.dl.addWidget(why)
        elif own:
            remove=QPushButton('Desktop-Szene löschen');remove.clicked.connect(lambda:self.delete_scene(s));self.dl.addWidget(remove)
        self.dl.addStretch()
    def add_scene_report_button(self,s):
        button=QPushButton('Szenenbericht speichern');button.clicked.connect(lambda:self.export_scene_report(s));self.dl.addWidget(button)
    def export_scene_report(self,s):
        filename,_=QFileDialog.getSaveFileName(self,'Szenenbericht speichern','SmartLife-Szenenbericht.json','JSON-Datei (*.json)')
        if not filename:return
        try:Path(filename).write_text(json.dumps(scene_report(s,self.data['devices']),ensure_ascii=False,indent=2),encoding='utf-8')
        except OSError as e:self.error(e)
    def setup_direct(self):
        if self.login_dialog:self.login_dialog.reject()
        dlg=CloudSetupDialog(self)
        if dlg.exec()==QDialog.Accepted:self.connected()
    def require_direct(self,allow_background=False):
        if not self.cloud.direct:
            self.setup_direct();return False
        return True
    def begin_edit(self):
        depth=getattr(self,'edit_depth',0);self.edit_depth=depth+1
        if depth:return
        self.edit_poll_active=self.poll.isActive();self.poll.stop();self.device_editing=True
        self.edit_fritz_active=self.fritz_timer.isActive();self.fritz_timer.stop()
        if self.cloud.direct:self.cloud.direct.background_pause.set()
    def end_edit(self):
        self.edit_depth=max(0,getattr(self,'edit_depth',1)-1)
        if self.edit_depth:return
        self.device_editing=False
        if self.cloud.direct:self.cloud.direct.background_pause.clear()
        if getattr(self,'edit_poll_active',False):self.poll.start()
        if getattr(self,'edit_fritz_active',False):self.fritz_timer.start()
    def edit_device(self,d):
        if not self.require_direct(allow_background=True):return
        self.begin_edit()
        try:DeviceAdminDialog(self,d).exec()
        finally:self.end_edit()
    def apply_device_update(self,result):
        changed=result['device']
        for device in self.data['devices']:
            if device['id']==changed['id']:device.update(changed);break
        by_id={rule['id']:rule for rule in result.get('automations',[])}
        for rule in self.data.get('automations',[]):
            if rule['id'] in by_id:rule.update(by_id[rule['id']])
        self.detail_id=changed['id'];self.render()
        if self.tree.selectedItems():self.selected()
        self.refresh_fritz_device(changed)
        self.status.setText('Änderung bestätigt · '+changed['name']+' gezielt aktualisiert'+(' · '+' · '.join(result['warnings']) if result.get('warnings') else ''))
    def manage_rooms(self):
        if not self.require_direct():return
        if not self.home.currentData():return
        self.begin_edit()
        try:RoomAdminDialog(self,self.home.currentData()).exec()
        finally:self.end_edit()
    def edit_automation(self,s=None):
        if not self.require_direct():return
        home=self.home.currentData()
        if not home:return
        self.begin_edit()
        def open_editor(original):
            try:
                dialog=AutomationEditor(self,home,original)
                if dialog.exec()==QDialog.Accepted:self.detail_id=dialog.result_rule['id'];self.load()
            finally:self.end_edit()
        def failed(e):self.end_edit();self.error(e)
        if s:self.submit(lambda:self.cloud.direct.get_automation(home,s['id']),open_editor,failed)
        else:open_editor(None)
    def edit_scene(self,s=None):
        if not self.home.currentData():self.error(ValueError('Bitte zuerst ein Zuhause laden.'));return
        own=s and s.get('source')=='desktop'
        if not own:
            if not self.require_direct():return
            if s and s.get('source')!='project':
                self.load();return
        original=None
        if s and not own:
            rows=scene_rows(s,self.data['devices'])
            original=s.get('original');editable=[]
            for raw in s.get('actions',[]):
                converted=scene_rows({'actions':[raw]},self.data['devices'])
                if converted and all(row[3] is not None for row in converted):editable.extend(row[3] for row in converted)
                else:editable.append({'_raw':raw})
            s=dict(s,actions=editable)
        store=self.scene_store if own else CloudSceneStore(self.cloud.direct,original)
        dialog=SceneEditor(self,store,self.home.currentData(),self.data['devices'],s,cloud=not own,save_handler=self.submit if not own else None)
        self.begin_edit()
        try:
            if dialog.exec()==QDialog.Accepted:
                self.detail_id=dialog.result_scene['id']
                if own:self.render();self.selected()
                else:self.load()
                self.status.setText('Szene gespeichert. Es wurden noch keine Geräte geschaltet.')
        finally:self.end_edit()
    def delete_scene(self,s):
        if question_de(self,'Desktop-Szene löschen','Soll diese auf dem PC gespeicherte Szene gelöscht werden?')!=QMessageBox.Yes:return
        try:self.scene_store.delete(s['id']);self.render()
        except (RuntimeError,OSError) as e:self.error(e)
    def probe_device(self,d,button):
        button.setEnabled(False);self.status.setText('Gerätedaten werden gezielt geprüft …')
        def done(result):
            try:button.setEnabled(True)
            except RuntimeError:pass
            self.data['devices']=result['devices'];self.render();self.selected()
            text=json.dumps(result['report'],ensure_ascii=False,indent=2)
            dlg=QDialog(self);dlg.setWindowTitle('Geräteprüfung – '+d['name']);dlg.resize(780,420);v=QVBoxLayout(dlg)
            explanation=QLabel('Diese Prüfung zeigt, welche Funktionen und Werte Tuya für dieses Modell freigibt. Zugangsschlüssel, Kontotoken und Netzwerkadressen werden nicht exportiert.');explanation.setWordWrap(True);v.addWidget(explanation)
            summary=QLabel(probe_summary(result['report']));summary.setWordWrap(True);summary.setTextInteractionFlags(Qt.TextSelectableByMouse);summary.setStyleSheet('background:#f3f4f5;color:#24272d;padding:14px;font-size:12pt;');v.addWidget(summary)
            toggle=QPushButton('Technische Details anzeigen');toggle.setCheckable(True);v.addWidget(toggle)
            view=QPlainTextEdit();view.setReadOnly(True);view.setPlainText(text);view.setMinimumHeight(230);v.addWidget(view);view.hide()
            def details(show):
                view.setVisible(show);toggle.setText('Technische Details ausblenden' if show else 'Technische Details anzeigen')
            toggle.toggled.connect(details)
            save=QPushButton('Gerätebericht speichern');v.addWidget(save)
            def export():
                filename,_=QFileDialog.getSaveFileName(dlg,'Gerätebericht speichern','SmartLife-Geraetepruefung.json','JSON-Datei (*.json)')
                if filename:
                    try:Path(filename).write_text(text,encoding='utf-8')
                    except OSError as e:self.error(e)
            save.clicked.connect(export);dlg.exec()
        def fail(e):
            try:button.setEnabled(True)
            except RuntimeError:pass
            self.error(e)
        self.submit(lambda:self.cloud.probe(d['id']),done,fail)
    def command(self,d,code,value,widget):
        widget.setEnabled(False);self.status.setText('Befehl wird gesendet …')
        def done(_):
            try:widget.setEnabled(True)
            except RuntimeError:pass
            self.status.setText('Befehl von Smart Life angenommen · Gerätestatus wird neu gelesen.');QTimer.singleShot(1200,lambda:self.refresh_device(d['id']))
            if is_cover(d):
                for delay in (4000,8000,15000,25000):QTimer.singleShot(delay,lambda:self.refresh_device(d['id']))
        def failed(e):
            try:widget.setEnabled(True)
            except RuntimeError:pass
            self.error(e)
        self.submit(lambda:self.cloud.command(d['id'],code,value),done,failed)
    def scene(self,s,b):
        if self.demo:return
        b.setEnabled(False)
        def done(_):
            try:b.setEnabled(True)
            except RuntimeError:pass
            self.status.setText('Desktop-Szene ausgeführt.' if s.get('source')=='desktop' else 'Szene von Smart Life angenommen.');QTimer.singleShot(1200,self.refresh)
        def fail(e):
            try:b.setEnabled(True)
            except RuntimeError:pass
            self.error(e)
        self.submit(lambda:execute_desktop_scene(s,self.cloud) if s.get('source')=='desktop' else self.cloud.scene(s['home'],s['id']),done,fail)
    def login(self):
        if self.cloud.direct:self.setup_direct();return
        if self.login_dialog:self.login_dialog.raise_();return
        dlg=QDialog(self);self.login_dialog=dlg;dlg.setWindowTitle('Mit Smart Life verbinden');dlg.resize(590,700);v=QVBoxLayout(dlg)
        text=QLabel('Auf deinem iPhone: Smart Life → Profil / Ich → Einstellungen → Konto und Sicherheit → Benutzercode.');text.setWordWrap(True);v.addWidget(text)
        direct=QPushButton('Statt QR: Direkten Cloudzugriff einrichten');direct.clicked.connect(self.setup_direct);v.addWidget(direct)
        code=QLineEdit();code.setPlaceholderText('Benutzercode');v.addWidget(code)
        remember=QCheckBox('Angemeldet bleiben (Windows schützt die Anmeldung)');remember.setChecked(True);v.addWidget(remember)
        create=QPushButton('QR-Code anzeigen');v.addWidget(create);qr=QLabel();qr.setAlignment(Qt.AlignCenter);qr.setMinimumHeight(300);v.addWidget(qr)
        state=QLabel('Den QR-Code anschließend in Smart Life über + → Scannen öffnen und bestätigen.');state.setWordWrap(True);v.addWidget(state)
        attribution=QLabel('Die Freigabe kann in Smart Life als „Home Assistant“ erscheinen. Verwendet wird die öffentliche Tuya-Gerätefreigabe dieser Integration.');attribution.setWordWrap(True);attribution.setStyleSheet('color:#626971;font-size:9pt');v.addWidget(attribution)
        check=QPushButton('Anmeldung bestätigt – verbinden');check.setEnabled(False);v.addWidget(check)
        timer=QTimer(dlg);timer.setInterval(3000);polling=[False];generation=[0]
        def failed(e):
            if self.login_dialog is not dlg:return
            create.setEnabled(True);check.setEnabled(False);timer.stop();state.setText(str(e))
        def request():
            generation[0]+=1;gen=generation[0];timer.stop();create.setEnabled(False);check.setEnabled(False);state.setText('QR-Code wird angefordert …');self.cloud.remember=remember.isChecked()
            def ready(data):
                if self.login_dialog is not dlg or gen!=generation[0]:return
                import qrcode
                b=BytesIO();qrcode.make(data).save(b,format='PNG');im=QImage.fromData(b.getvalue());qr.setPixmap(QPixmap.fromImage(im).scaled(300,300,Qt.KeepAspectRatio,Qt.FastTransformation));check.setEnabled(True);create.setEnabled(True);state.setText('Mit Smart Life scannen und Anmeldung auf dem iPhone bestätigen.');timer.start()
            usercode=code.text()
            self.submit(lambda:self.cloud.qr(usercode),ready,failed)
        def poll():
            if polling[0] or self.jobs:return
            polling[0]=True
            def result(ok):
                polling[0]=False
                if self.login_dialog is not dlg:return
                if ok:timer.stop();dlg.accept();self.connected()
            def fail(e):polling[0]=False;failed(e)
            self.submit(self.cloud.poll_login,result,fail)
        create.clicked.connect(request);code.returnPressed.connect(request);check.clicked.connect(poll);timer.timeout.connect(poll)
        if self.ready:
            logout=QPushButton('Abmelden und gespeicherte Anmeldung entfernen');v.addWidget(logout)
            def out():
                self.poll.stop();self.ready=False
                def done(warning):
                    dlg.reject();self.data={'homes':[],'devices':[],'scenes':[]};self.populate_homes();self.account.setText('Smart Life · nicht verbunden');self.status.setText(warning or 'Abgemeldet.')
                self.submit(self.cloud.logout,done)
            logout.clicked.connect(out)
        dlg.finished.connect(lambda _:(timer.stop(),setattr(self,'login_dialog',None)))
        dlg.setAttribute(Qt.WA_DeleteOnClose);dlg.open()
    def set_update_note(self,text,newer=False):
        self.update_note.setText(text)
        self.update_note.setStyleSheet('color:#ffb4a9;font-weight:bold;' if newer else 'color:#e2e4e7;')
    def submit_update(self,fn,success,failure):
        if self.closing:return
        future=self.update_pool.submit(fn)
        def finish(f):
            try:value,error=f.result(),None
            except Exception as e:value,error=None,e
            if not self.closing:self.update_bridge.done.emit(value,error,(success,failure))
        future.add_done_callback(finish)
    def complete_update(self,value,error,callbacks):
        if self.closing:return
        success,failure=callbacks
        try:
            if error:failure(error)
            else:success(value)
        except Exception as e:
            self.update_btn.setEnabled(True);self.update_installing=False;self.error(e)
    def check_update(self,interactive=False):
        if self.demo or getattr(self,'update_installing',False):return
        self.update_interactive=getattr(self,'update_interactive',False) or interactive
        if getattr(self,'update_checking',False):
            self.set_update_note('Updateprüfung läuft …');return
        self.update_checking=True;self.set_update_note('Updateprüfung läuft …')
        def done(result):
            self.update_checking=False;m,newer=result;show=self.update_interactive;self.update_interactive=False
            self.set_update_note('Update verfügbar: '+m['version'] if newer else '',newer)
            self.update_btn.setText('Update · '+m['version'] if newer else 'Update')
            if not show:return
            if not newer:QMessageBox.information(self,'Updates','Installiert: '+VERSION+'\nDeine Version ist aktuell.');return
            if question_de(self,'Update',f"Installiert: {VERSION}\nVerfügbar: {m['version']}\n\n{m.get('notes','')}\n\nJetzt herunterladen und installieren?")!=QMessageBox.Yes:return
            self.update_installing=True;self.update_btn.setEnabled(False);self.set_update_note('Update wird geladen und geprüft …')
            def staged(path):
                try:updates.install(path,Path(__file__).resolve().parent.parent)
                except Exception as e:fail(e);return
                self.close()
            def fail(e):
                self.update_installing=False;self.update_btn.setEnabled(True);self.set_update_note('Update fehlgeschlagen – erneut versuchen');self.error(e)
            self.submit_update(lambda:updates.stage(m,Path(__file__).resolve().parent.parent),staged,fail)
        def failed(e):
            self.update_checking=False;show=self.update_interactive;self.update_interactive=False;self.set_update_note('Updateprüfung fehlgeschlagen')
            if show:self.error(e)
        self.submit_update(updates.check,done,failed)
    def closeEvent(self,event):
        self.closing=True;self.fritz_timer.stop();self.poll.stop();self.update_timer.stop();self.update_pool.shutdown(wait=False,cancel_futures=True);self.fritz_pool.shutdown(wait=False,cancel_futures=True);self.pool.shutdown(wait=False,cancel_futures=True);event.accept()
    def demo_data(self):
        from demo import sample
        self.data=sample();self.populate_homes();self.status.setText('Vorschau mit Beispieldaten · keine Verbindung zu deinem Zuhause');self.account.setText('Smart Life · Vorschau')

LABEL_SUMMARY={'temp_current','va_temperature','humidity_value','va_humidity','switch','switch_1','switch_led','bright_value','bright_value_v2','percent_state','pm25','pm25_value','mode'}

def run():
    app=QApplication(sys.argv);app.setApplicationName('Smart Life Desktop');app.setStyle('Fusion');app.setStyleSheet(STYLE)
    w=Main('--demo' in sys.argv);w.showMaximized()
    root=Path(__file__).resolve().parent.parent
    try:(root/'startup-ready.json').write_text(json.dumps({'pid':os.getpid(),'version':VERSION}))
    except OSError:pass
    return app.exec()

if __name__=='__main__':sys.exit(run())
