"""German setup for reading the local FRITZ!Box host inventory."""
from PySide6.QtWidgets import QDialog,QVBoxLayout,QFormLayout,QHBoxLayout,QLabel,QLineEdit,QCheckBox,QPushButton,QComboBox
from fritz import mac
class FritzDialog(QDialog):
    def __init__(self,main):
        super().__init__(main);self.main=main;self.setWindowTitle('FRITZ!Box – lokales Netzwerk');self.resize(760,620);v=QVBoxLayout(self)
        text=QLabel('Liest lokale IP-Adressen und Hostnamen direkt aus deiner FRITZ!Box. Zugang für Anwendungen (TR-064) muss in den Netzwerkeinstellungen der FRITZ!Box aktiviert sein. Es werden keine Routereinstellungen geändert.');text.setWordWrap(True);v.addWidget(text)
        cfg=main.fritz.config or {};form=QFormLayout();self.address=QLineEdit(cfg.get('address','fritz.box'));self.user=QLineEdit(cfg.get('user',''));self.password=QLineEdit(cfg.get('password',''));self.password.setEchoMode(QLineEdit.Password)
        for title,field in [('FRITZ!Box-Adresse',self.address),('FRITZ!Box-Benutzer',self.user),('Kennwort',self.password)]:form.addRow(title,field)
        v.addLayout(form);self.remember=QCheckBox('Anmeldung auf diesem PC geschützt speichern');self.remember.setChecked(main.fritz.remember or not cfg);v.addWidget(self.remember)
        self.message=QLabel('');self.message.setWordWrap(True);v.addWidget(self.message)
        row=QHBoxLayout();connect=QPushButton('Anmelden und Netzwerk lesen');connect.clicked.connect(self.connect);row.addWidget(connect);refresh=QPushButton('Netzwerk aktualisieren');refresh.clicked.connect(self.refresh);row.addWidget(refresh);v.addLayout(row)
        info=QLabel('Automatische Zuordnung über die MAC-Adresse. Falls Tuya keine MAC liefert, kannst du ein Gerät einmalig dem passenden FRITZ!Box-Eintrag zuordnen.');info.setWordWrap(True);v.addWidget(info)
        self.device=QComboBox();self.host=QComboBox();v.addWidget(self.device);v.addWidget(self.host)
        bind=QPushButton('Netzwerkeintrag diesem Gerät zuordnen');bind.clicked.connect(self.bind);v.addWidget(bind)
        row=QHBoxLayout();logout=QPushButton('FRITZ!Box abmelden');logout.clicked.connect(self.logout);row.addWidget(logout);close=QPushButton('Schließen');close.clicked.connect(self.reject);row.addWidget(close);v.addLayout(row);self.fill()
    def fill(self):
        self.device.clear();self.host.clear()
        for d in self.main.data['devices']:
            if not d.get('sub'):self.device.addItem(d['name']+(' · '+d['room'] if d.get('room') else ''),d['id'])
        self.device.setCurrentIndex(-1);self.device.setPlaceholderText('Smart-Life-Gerät auswählen')
        for h in self.main.fritz.hosts:
            if h['mac']:self.host.addItem((h['hostname'] or 'Ohne Hostnamen')+' · '+(h['ip'] or 'Ohne lokale IP')+' · '+h['mac']+('' if h['active'] else ' · nicht aktiv'),h['mac'])
        self.host.setCurrentIndex(-1);self.host.setPlaceholderText('Passenden FRITZ!Box-Eintrag auswählen')
    def run(self,fn,done):
        self.message.setText('FRITZ!Box wird direkt im Heimnetz abgefragt …');self.setEnabled(False)
        def success(result):self.setEnabled(True);self.fill();done(result)
        def fail(e):self.setEnabled(True);self.message.setText(str(e))
        self.main.submit_fritz(fn,success,fail)
    def connect(self):
        cfg={'address':self.address.text().strip(),'user':self.user.text().strip(),'password':self.password.text()};remember=self.remember.isChecked()
        def done(count):self.message.setText('FRITZ!Box verbunden · '+str(count)+' Netzwerkgeräte gelesen.');self.main.fritz_connected(retry=True)
        self.run(lambda:self.main.fritz.connect(cfg,remember),done)
    def refresh(self):
        def done(count):self.message.setText(str(count)+' Netzwerkgeräte aktualisiert.');self.main.fritz_connected(retry=True)
        self.run(self.main.fritz.refresh,done)
    def bind(self):
        did=self.device.currentData();address=self.host.currentData()
        if not did or not address:self.message.setText('Bitte zuerst ein Smart-Life-Gerät und einen FRITZ!Box-Eintrag auswählen.');return
        def done(_):self.message.setText('Zuordnung gespeichert. Lokale IP-Adresse und Hostname sind in der Geräteliste aktualisiert.');self.main.render()
        self.run(lambda:self.main.fritz.bind(did,address),done)
    def logout(self):
        def done(_):self.message.setText('FRITZ!Box abgemeldet.');self.main.fritz_status.setText('FRITZ!Box · nicht verbunden');self.main.render()
        self.run(self.main.fritz.clear,done)
