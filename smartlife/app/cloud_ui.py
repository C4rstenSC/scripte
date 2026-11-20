"""German setup and management dialogs. All network tasks use the main worker."""
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QDialog,QVBoxLayout,QHBoxLayout,QFormLayout,QLabel,QLineEdit,QComboBox,QPushButton,
 QCheckBox,QMessageBox,QFileDialog,QTreeWidget,QTreeWidgetItem)
from project_cloud import ENDPOINTS
from portable_credentials import encrypt_config,decrypt_config
from scene_editor import question_de
from ui_widgets import CleanSelectionDelegate,fit_columns

REGION_NAMES={'Central Europe':'Mitteleuropa – Central Europe','Western Europe':'Westeuropa – Western Europe',
 'Western America':'Amerika West','Eastern America':'Amerika Ost','China':'China','India':'Indien','Singapore':'Singapur'}

class PasswordDialog(QDialog):
    def __init__(self,parent,confirm=False):
        super().__init__(parent);self.setWindowTitle('Entschlüsselungskennwort');v=QVBoxLayout(self)
        label=QLabel('Dieses Kennwort wird nicht in die Datei oder nach GitHub gespeichert. Es wird später zum Entsperren auf dem Mac benötigt.' if confirm else 'Kennwort der verschlüsselten Zugangsdatei eingeben.');label.setWordWrap(True);v.addWidget(label)
        self.password=QLineEdit();self.password.setEchoMode(QLineEdit.Password);v.addWidget(self.password);self.confirm=None
        if confirm:self.confirm=QLineEdit();self.confirm.setEchoMode(QLineEdit.Password);self.confirm.setPlaceholderText('Kennwort wiederholen');v.addWidget(self.confirm)
        row=QHBoxLayout();ok=QPushButton('Bestätigen');ok.clicked.connect(self.check);row.addWidget(ok);cancel=QPushButton('Abbrechen');cancel.clicked.connect(self.reject);row.addWidget(cancel);v.addLayout(row)
    def check(self):
        if self.confirm and (len(self.password.text())<12 or self.password.text()!=self.confirm.text()):QMessageBox.warning(self,'Kennwort','Mindestens 12 Zeichen verwenden und beide Felder identisch ausfüllen.');return
        self.accept()

class CloudSetupDialog(QDialog):
    def __init__(self,main):
        super().__init__(main);self.main=main;self.setWindowTitle('Direkten Tuya-Cloudzugriff einrichten');self.resize(720,540);v=QVBoxLayout(self)
        text=QLabel('Die Angaben stammen aus deinem verknüpften Tuya-Cloud-Projekt. Der Verbindungstest liest nur Daten und verändert keine Geräte, Räume oder Szenen.');text.setWordWrap(True);v.addWidget(text)
        form=QFormLayout();self.client=QLineEdit();self.secret=QLineEdit();self.secret.setEchoMode(QLineEdit.Password);self.uid=QLineEdit();self.region=QComboBox()
        for key in ENDPOINTS:self.region.addItem(REGION_NAMES[key],key)
        for title,w in [('Access ID / Client ID',self.client),('Access Secret / Client Secret',self.secret),('UID des Smart-Life-Kontos',self.uid),('Datenzentrum',self.region)]:form.addRow(title,w)
        v.addLayout(form);self.remember=QCheckBox('Zugang auf diesem PC geschützt speichern');self.remember.setChecked(True);v.addWidget(self.remember)
        current=getattr(main.cloud,'direct',None)
        if current:
            cfg=current.config;self.client.setText(cfg['access_id']);self.secret.setText(cfg['access_secret']);self.uid.setText(cfg['uid']);self.region.setCurrentIndex(self.region.findData(cfg['region']))
        self.result_label=QLabel('Noch nicht geprüft. Die Berechtigungen werden mit deinem Konto geprüft.');self.result_label.setWordWrap(True);v.addWidget(self.result_label)
        self.connect_btn=QPushButton('Prüfen und verbinden');self.connect_btn.clicked.connect(self.connect);v.addWidget(self.connect_btn)
        row=QHBoxLayout();export=QPushButton('Zugang verschlüsselt sichern');export.clicked.connect(self.export);row.addWidget(export);imp=QPushButton('Verschlüsselten Zugang laden');imp.clicked.connect(self.load_file);row.addWidget(imp);v.addLayout(row)
        close=QPushButton('Schließen');close.clicked.connect(self.reject);v.addWidget(close)
    def connect(self):
        config={'access_id':self.client.text().strip(),'access_secret':self.secret.text().strip(),'uid':self.uid.text().strip(),'region':self.region.currentData()}
        remember=self.remember.isChecked();self.setEnabled(False);self.result_label.setText('Anmeldung und Zugriff auf dein Zuhause werden geprüft …')
        def done(_):self.setEnabled(True);self.accept()
        def failed(e):self.setEnabled(True);self.result_label.setText(str(e))
        self.main.submit(lambda:self.main.cloud.connect_direct(config,remember),done,failed)
    def export(self):
        direct=getattr(self.main.cloud,'direct',None)
        if not direct:QMessageBox.information(self,'Zugang sichern','Bitte zuerst erfolgreich prüfen und verbinden.');return
        password=PasswordDialog(self,True)
        if password.exec()!=QDialog.Accepted:return
        filename,_=QFileDialog.getSaveFileName(self,'Verschlüsselten Zugang speichern','SmartLife-Zugang.enc','Verschlüsselte Datei (*.enc)')
        if not filename:return
        try:
            blob=encrypt_config(direct.config,password.password.text());Path(filename).write_bytes(blob)
            QMessageBox.information(self,'Zugang gesichert','Die verschlüsselte Datei ist gespeichert. Das Kennwort separat aufbewahren. Nur die verschlüsselte Datei darf nach GitHub übertragen werden.')
        except (OSError,ValueError) as e:QMessageBox.warning(self,'Zugang sichern',str(e))
    def load_file(self):
        filename,_=QFileDialog.getOpenFileName(self,'Verschlüsselten Zugang laden','','Verschlüsselte Datei (*.enc)')
        if not filename:return
        password=PasswordDialog(self)
        if password.exec()!=QDialog.Accepted:return
        try:
            cfg=decrypt_config(Path(filename).read_bytes(),password.password.text())
            self.client.setText(cfg['access_id']);self.secret.setText(cfg['access_secret']);self.uid.setText(cfg['uid']);self.region.setCurrentIndex(self.region.findData(cfg['region']));self.result_label.setText('Datei entschlüsselt. Bitte jetzt prüfen und verbinden.')
        except (OSError,ValueError) as e:QMessageBox.warning(self,'Zugang laden',str(e))

class DeviceAdminDialog(QDialog):
    def __init__(self,main,device):
        super().__init__(main);self.main=main;self.device=device;self.setWindowTitle('Gerät und FRITZ!Box-Hostname bearbeiten');self.resize(700,570);v=QVBoxLayout(self)
        self.device_title=QLabel(device['name']);v.addWidget(self.device_title)
        note=QLabel('Gerätename und Raum werden in Smart Life gespeichert. Der FRITZ!Box-Hostname wird separat direkt in deinem Router geändert.');note.setWordWrap(True);v.addWidget(note);v.addWidget(QLabel('Gerätename (Smart Life)'))
        self.name=QLineEdit(device['name']);v.addWidget(self.name);rename=QPushButton('Gerätenamen speichern');rename.clicked.connect(self.rename);v.addWidget(rename)
        self.room=QComboBox()
        for r in main.cloud.direct.rooms:
            if r['home']==device['home']:self.room.addItem(r['name'],r['id'])
        self.room.setCurrentIndex(self.room.findData(device['room_id']));v.addWidget(self.room)
        move=QPushButton('Gerät diesem Raum zuordnen');move.clicked.connect(self.move);v.addWidget(move)
        v.addWidget(QLabel('FRITZ!Box-Hostname'))
        network=main.fritz.match(device);self.fritz_mac=network['mac'] if network else ''
        self.hostname=QLineEdit(network['hostname'] if network else '');self.hostname.setPlaceholderText('Zum Beispiel: tv-hintergrund');v.addWidget(self.hostname)
        self.hostname_button=QPushButton('FRITZ!Box-Hostnamen speichern');self.hostname_button.clicked.connect(self.rename_hostname);v.addWidget(self.hostname_button)
        available=bool(network and main.fritz.client);self.hostname.setEnabled(available);self.hostname_button.setEnabled(available)
        if not available:
            info=QLabel('Für die Hostnamenänderung zuerst bei der FRITZ!Box anmelden und dieses Gerät eindeutig zuordnen.');info.setWordWrap(True);v.addWidget(info)
        self.message=QLabel('');self.message.setWordWrap(True);v.addWidget(self.message);close=QPushButton('Schließen');close.clicked.connect(self.reject);v.addWidget(close)
    def rename_hostname(self):
        device=dict(self.device);value=self.hostname.text();address=self.fritz_mac
        self.message.setText('FRITZ!Box-Hostname wird gespeichert und für dieses Gerät zurückgelesen …');self.setEnabled(False)
        def done(host):
            self.setEnabled(True);self.hostname.setText(host['hostname']);self.main.render();self.message.setText('FRITZ!Box-Hostname gespeichert und bestätigt: '+host['hostname'])
        def failed(e):self.setEnabled(True);self.main.render();self.message.setText(str(e))
        self.main.submit_fritz(lambda:self.main.fritz.rename_hostname(device,value,address),done,failed)
    def run(self,action):
        self.message.setText('Änderung wird gespeichert und gezielt aus der Cloud zurückgelesen …');self.setEnabled(False)
        def done(result):
            self.setEnabled(True);self.device=result['device'];self.name.setText(self.device['name']);self.device_title.setText(self.device['name']);self.room.setCurrentIndex(self.room.findData(self.device['room_id']))
            self.main.apply_device_update(result)
            self.message.setText('Änderung von Tuya bestätigt. Gerät und zugehörige Ansichten aktualisiert.'+('\n'+'\n'.join(result['warnings']) if result.get('warnings') else ''))
        def fail(e):self.setEnabled(True);self.message.setText(str(e))
        self.main.submit(action,done,fail)
    def rename(self):
        name=self.name.text();self.run(lambda:self.main.cloud.direct.rename_and_refresh(self.device['id'],name))
    def move(self):
        room=self.room.currentData()
        if not room:QMessageBox.warning(self,'Raumzuordnung','Bitte einen Raum auswählen.');return
        self.run(lambda:self.main.cloud.direct.move_and_refresh(self.device['id'],room))

class RoomAdminDialog(QDialog):
    def __init__(self,main,home):
        super().__init__(main);self.main=main;self.home=home;self.setWindowTitle('Räume in Smart Life verwalten');self.resize(730,540);v=QVBoxLayout(self)
        note=QLabel('Änderungen betreffen dein Smart-Life-Konto. Räume mit Geräten müssen vor dem Löschen geleert werden.');note.setWordWrap(True);v.addWidget(note)
        self.tree=QTreeWidget();self.tree.setItemDelegate(CleanSelectionDelegate(self.tree));self.tree.setHeaderLabels(['Raum','Geräte']);self.tree.setRootIsDecorated(False);self.tree.itemSelectionChanged.connect(self.selected);v.addWidget(self.tree)
        self.name=QLineEdit();self.name.setPlaceholderText('Name des Raums');v.addWidget(self.name);row=QHBoxLayout()
        for text,action in [('Raum erstellen',self.add),('Raum umbenennen',self.rename),('Raum löschen',self.delete)]:b=QPushButton(text);b.clicked.connect(action);row.addWidget(b)
        v.addLayout(row);self.message=QLabel('');self.message.setWordWrap(True);v.addWidget(self.message);close=QPushButton('Schließen');close.clicked.connect(self.reject);v.addWidget(close);self.render()
    def render(self):
        self.tree.clear()
        for r in self.main.cloud.direct.rooms:
            if r['home']==self.home:
                count=sum(d['home']==self.home and d['room_id']==r['id'] for d in self.main.cloud.direct.devices);item=QTreeWidgetItem([r['name'],str(count)]);item.setData(0,Qt.UserRole,r);self.tree.addTopLevelItem(item)
        fit_columns(self.tree)
    def selected(self):
        item=self.tree.currentItem()
        if item:self.name.setText(item.data(0,Qt.UserRole)['name'])
    def run(self,action):
        self.setEnabled(False)
        def worker():action();return self.main.cloud.load()
        def done(data):self.main.data=data;self.setEnabled(True);self.main.populate_homes();self.render();self.message.setText('Änderung bei Smart Life gespeichert.')
        def fail(e):self.setEnabled(True);self.message.setText(str(e))
        self.main.submit(worker,done,fail)
    def add(self):
        name=self.name.text();self.run(lambda:self.main.cloud.direct.add_room(self.home,name))
    def rename(self):
        item=self.tree.currentItem()
        if not item:return
        rid=item.data(0,Qt.UserRole)['id'];name=self.name.text();self.run(lambda:self.main.cloud.direct.rename_room(self.home,rid,name))
    def delete(self):
        item=self.tree.currentItem()
        if not item:return
        room=item.data(0,Qt.UserRole)
        if question_de(self,'Raum löschen','Soll der Raum „'+room['name']+'“ in Smart Life gelöscht werden?')!=QMessageBox.Yes:return
        self.run(lambda:self.main.cloud.direct.delete_room(self.home,room['id']))

class CloudSceneStore:
    def __init__(self,direct,original=None):self.direct=direct;self.original=original
    def save(self,name,home,actions,devices,scene_id=None):return self.direct.save_scene(name,home,actions,self.original)
