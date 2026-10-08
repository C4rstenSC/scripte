#!/usr/bin/env bash
# Standard: reine Beobachtung. --serial-test pausiert GPSD für einen exklusiven Test.
set -uo pipefail
umask 077
serial_test=false
case ${1:-} in
    '') ;;
    --serial-test) serial_test=true ;;
    *) echo 'Aufruf: sudo witty-gps-diagnose [--serial-test]' >&2; exit 2 ;;
esac
if [[ ${EUID:-$(id -u)} -ne 0 ]]; then
    echo 'Bitte starten mit: sudo /usr/local/sbin/witty-gps-diagnose' >&2
    exit 1
fi
report_dir=/var/tmp
if [[ -n ${SUDO_USER:-} && ${SUDO_USER:-} != root ]]; then
    user_home=$(getent passwd "$SUDO_USER" | cut -d: -f6)
    [[ -d $user_home ]] && report_dir=$user_home
fi
report=$(mktemp "$report_dir/Witty-GPS-Diagnose-$(date +%Y%m%d-%H%M%S).XXXXXX.txt") || exit 1
if [[ ${SUDO_UID:-} =~ ^[0-9]+$ && ${SUDO_GID:-} =~ ^[0-9]+$ ]]; then
    chown "$SUDO_UID:$SUDO_GID" "$report"
fi
exec 3>&1
exec > >(tee "$report") 2>&1
tee_pid=$!
section(){ printf '\n===== %s =====\n' "$1"; }
section 'Gerät, Uhrzeit und Versionen'
date --iso-8601=seconds
tr -d '\0' </proc/device-tree/model 2>/dev/null || true
printf '\n'
for path in /home/wurb/wittypi5-webserver/VERSION /home/pi/wittypi5-webserver/VERSION /etc/os-release /etc/witty-addon.conf /etc/default/gpsd; do
    if [[ -f $path ]]; then printf '\n%s\n' "$path"; cat "$path"; fi
done
section 'USB und serielle Anschlüsse'
command -v lsusb >/dev/null && timeout 10s lsusb
command -v lsblk >/dev/null && timeout 10s lsblk -o NAME,TYPE,TRAN,SIZE,MOUNTPOINTS
command -v arecord >/dev/null && timeout 10s arecord -l 2>&1 || true
for path in /dev/witty-gps /dev/ttyACM* /dev/ttyUSB* /dev/ttyWURB /dev/serial/by-id/*; do
    [[ -e $path || -L $path ]] || continue
    ls -l "$path"
    resolved=$(readlink -f "$path" 2>/dev/null || true)
    if [[ $resolved == /dev/ttyACM* || $resolved == /dev/ttyUSB* ]]; then
        timeout 3s udevadm info --query=property --name="$resolved" 2>/dev/null | grep -E '^(ID_VENDOR_ID|ID_MODEL_ID|ID_SERIAL|ID_USB_DRIVER|DEVLINKS|SYSTEMD_WANTS)=' || true
        command -v fuser >/dev/null && timeout 3s fuser -v "$resolved" 2>&1 || true
    fi
done
section 'Hotplug-Regeln'
for rule in /etc/udev/rules.d/*gps* /usr/lib/udev/rules.d/*gps* /lib/udev/rules.d/*gps*; do
    [[ -f $rule ]] && { printf '\n%s\n' "$rule"; cat "$rule"; }
done
section 'Dienste und effektive Konfiguration'
timeout 10s systemctl status gpsd.socket gpsd.service wurb-gps-bridge.service wurb_2026.service witty-gps-time-once.service --no-pager --full 2>&1 || true
timeout 10s systemctl list-units 'witty-gps-hotplug@*' --all --no-pager 2>&1 || true
timeout 10s systemctl cat gpsd.service gpsd.socket wurb-gps-bridge.service witty-gps-hotplug@.service wurb_2026.service 2>&1 || true
section 'WURB GPS-Auswahl und Patch-Merkmale'
for path in /home/wurb/wurb_settings/wurb_config.yaml /home/pi/wurb_settings/wurb_config.yaml; do
    [[ -f $path ]] && sed -n '/gps_device_whitelist:/,+14p' "$path"
done
for path in /home/wurb/wurb_2026/wurb_core/record/gps_reader.py /home/pi/wurb_2026/wurb_core/record/gps_reader.py; do
    [[ -f $path ]] && grep -nE 'bridge_port|bridge_fix|errno|serial.rts|gps_device_path_found|min_number_of_satellites' "$path"
done
section 'Aktuelle GPSD-Meldungen: maximal 12 Sekunden'
# Ausschließlich gpsd beobachten; den physischen GPS-Port und WURB-PTY nicht öffnen.
direct_pi4_usb=false
if grep -Eq '^RPI_MODEL=(4|4B)$' /etc/witty-addon.conf 2>/dev/null && \
   grep -Eq '^GPS_MODE=usb$' /etc/witty-addon.conf 2>/dev/null; then
    direct_pi4_usb=true
fi
if [[ $direct_pi4_usb == true ]]; then
    echo 'Pi 4 / USB: WURB liest direkt. GPSD und virtuelle Bridge werden nicht als zusätzliche Leser gestartet.'
else
if [[ $serial_test == true ]]; then
    section 'Exklusiver USB-Test: GPSD kurz pausieren, keine Befehle an die Maus'
    (
        device=$(readlink -f /dev/witty-gps 2>/dev/null || true)
        if [[ ! $device =~ ^/dev/tty(ACM|USB)[0-9]+$ || ! -c $device ]]; then
            echo 'Direkter Test übersprungen: kein eindeutiger physischer USB-GPS-Port unter /dev/witty-gps.'
            exit 0
        fi
        command -v fuser >/dev/null || { echo 'Direkter Test übersprungen: fuser fehlt; Exklusivität nicht prüfbar.'; exit 0; }
        socket_active=false; daemon_active=false
        systemctl is-active --quiet gpsd.socket && socket_active=true
        systemctl is-active --quiet gpsd.service && daemon_active=true
        restore_gpsd(){
            local failed=false
            if [[ $socket_active == true ]]; then
                timeout 20s systemctl start gpsd.socket || failed=true
            fi
            if [[ $daemon_active == true ]]; then
                timeout 20s systemctl start gpsd.service || failed=true
            fi
            if [[ $failed == true ]]; then
                echo 'FEHLER: GPSD-Wiederherstellung fehlgeschlagen. Bitte sudo systemctl restart gpsd.socket gpsd.service ausführen.'
            else
                echo 'GPSD-Dienstzustände wiederhergestellt; die laufende Bridge verbindet sich erneut.'
            fi
        }
        trap restore_gpsd EXIT
        trap 'exit 130' INT
        trap 'exit 143' TERM
        timeout 20s systemctl stop gpsd.socket || exit 1
        timeout 20s systemctl stop gpsd.service || exit 1
        if systemctl is-active --quiet gpsd.socket || systemctl is-active --quiet gpsd.service; then
            echo 'Direkter Test abgebrochen: GPSD weiterhin aktiv.'; exit 1
        fi
        timeout 3s fuser -v "$device"
        fuser_status=$?
        if [[ $fuser_status != 1 ]]; then
            echo 'Direkter Test abgebrochen: Port belegt oder Belegungsprüfung fehlgeschlagen.'; exit 1
        fi
        python3 - "$device" <<'SERIALPY'
import errno, fcntl, os, select, sys, termios, time, tty
fd = None
original = None
try:
    fd = os.open(sys.argv[1], os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
    fcntl.ioctl(fd, termios.TIOCEXCL)
    original = termios.tcgetattr(fd)
    tty.setraw(fd, termios.TCSANOW)
    settings = termios.tcgetattr(fd)
    settings[2] |= termios.CLOCAL | termios.CREAD
    # Baudrate beibehalten; der Test erzwingt keine gerätespezifische Geschwindigkeit.
    termios.tcsetattr(fd, termios.TCSANOW, settings)
    deadline = time.monotonic() + 20
    total = 0
    sample = bytearray()
    while time.monotonic() < deadline:
        ready, _, _ = select.select([fd], [], [], max(0, deadline - time.monotonic()))
        if not ready:
            break
        try:
            chunk = os.read(fd, 8192)
        except BlockingIOError:
            continue
        if not chunk:
            raise OSError('USB-GPS während des Tests getrennt')
        total += len(chunk)
        sample.extend(chunk[:max(0, 4096 - len(sample))])
    print('Physischer USB-Port:', sys.argv[1], 'Bytes in 20 Sekunden:', total)
    print('Rohdatenprobe (maximal 4096 Bytes):', repr(bytes(sample)))
    if not total:
        print('BEFUND: Auch ohne GPSD keine Bytes. USB-Ausgabe/Empfängerzustand prüfen; kein reiner WURB-Bridge-Fehler.')
    elif b'$' in sample:
        print('BEFUND: Direkter Port liefert Text/NMEA. Mit anschließender GPSD-Messung vergleichen.')
    else:
        print('BEFUND: Bytes vorhanden, möglicherweise Binärprotokoll. Rohdaten und GPSD-Version prüfen.')
except OSError as error:
    print('BEFUND: Direkter Port-Test fehlgeschlagen:', repr(error))
finally:
    if fd is not None:
        try:
            if original is not None:
                termios.tcsetattr(fd, termios.TCSANOW, original)
        finally:
            try:
                fcntl.ioctl(fd, termios.TIOCNXCL)
            finally:
                os.close(fd)
SERIALPY
    )
    section 'GPSD nach exklusivem USB-Test: maximal 12 Sekunden'
fi
python3 - <<'PY'
import socket,json,time
counts={}; devices=[]; fixes=[]; used=[]; nmea=0
try:
    deadline=time.monotonic()+12
    with socket.create_connection(('127.0.0.1',2947),timeout=3) as c:
        c.sendall(b'?WATCH={"enable":true,"json":true,"nmea":true};\n?DEVICES;\n')
        buf=b''
        while time.monotonic()<deadline:
            c.settimeout(max(.05,deadline-time.monotonic()))
            try: chunk=c.recv(16384)
            except socket.timeout: break
            if not chunk:
                print('GPSD-Verbindung beendet'); break
            buf+=chunk
            if len(buf)>1024*1024:
                print('GPSD-Antwort zu groß'); break
            while b'\n' in buf:
                line,buf=buf.split(b'\n',1)
                if line.startswith(b'$'):
                    nmea+=1
                    if nmea<=8: print(line.decode(errors='replace'))
                    continue
                try: r=json.loads(line)
                except (ValueError,UnicodeDecodeError): continue
                if not isinstance(r,dict): continue
                kind=r.get('class','unknown'); counts[kind]=counts.get(kind,0)+1
                if kind=='DEVICES': devices=r.get('devices',[]); print('DEVICES:',json.dumps(r))
                if kind=='DEVICE': print('DEVICE:',json.dumps(r))
                if kind=='ERROR': print('ERROR:',json.dumps(r))
                if kind=='SKY':
                    used.append(r.get('uSat',sum(1 for x in r.get('satellites',[]) if x.get('used'))))
                if kind=='TPV':
                    if counts[kind]<=3: print('TPV:',json.dumps(r))
                    if r.get('mode',0)>=2 and r.get('lat') is not None and r.get('lon') is not None: fixes.append(r)
    print('Meldungen:',counts,'NMEA:',nmea,'gültige Positionsmeldungen:',len(fixes),'Satelliten:',used[-5:])
    if fixes: print('BEFUND: GPSD liefert einen Positionsfix. Danach Homepage/WURB prüfen.')
    elif not counts.get('DEVICE') and not devices: print('BEFUND: Kein GPS-Gerät im beobachteten GPSD-Datenstrom gemeldet. Erkennung/Anmeldung prüfen.')
    elif not nmea and not counts.get('TPV') and not counts.get('SKY'):
        print('BEFUND: Gerät angemeldet, aber keinerlei NMEA-/TPV-/SKY-Meldungen im Messfenster. Datenstrom/Initialisierung prüfen; fehlender Fix allein erklärt das nicht.')
    else: print('BEFUND: Datenstrom vorhanden, aber kein Positionsfix im 12-Sekunden-Fenster. Kaltstart/Empfang prüfen.')
except OSError as e: print('BEFUND: GPSD nicht erreichbar:',repr(e))
PY
section 'Ausgabe des installierten GPSD-zu-NMEA-Konverters: maximal 6 Sekunden'
echo 'Eigener Konverter-Testlauf gegen GPSD; kein Lesen oder Öffnen des laufenden WURB-PTY.'
if [[ -x /usr/local/sbin/witty-gps-nmea-bridge ]]; then
    timeout 6s /usr/local/sbin/witty-gps-nmea-bridge 2>&1 | head -n 24 || true
else
    echo 'GPS-Konverter fehlt.'
fi
fi
section 'WURB-Positionsabfrage'
python3 - <<'PY'
import urllib.request
try:
    with urllib.request.urlopen('http://127.0.0.1:8080/record/get-location/', timeout=3) as r:
        print(r.read(4096).decode('utf-8', errors='replace'))
except Exception as e: print('WURB-Positionsabfrage nicht verfügbar:', str(e))
PY
section 'Prüfsummen installierter GPS-Helfer'
for helper in witty-gps-manager witty-gps-nmea-bridge witty-patch-wurb-gps witty-gps-diagnose; do
    [[ ! -f /usr/local/sbin/$helper ]] || sha256sum "/usr/local/sbin/$helper"
done
section 'GPS/WURB-Protokolle dieses Starts'
timeout 15s journalctl -b -u gpsd.service -u wurb-gps-bridge.service -u 'witty-gps-hotplug@*' -u wurb_2026.service -u witty-gps-time-once.service -n 160 --no-pager -o short-monotonic 2>&1 || true
section 'USB-Kernelmeldungen'
timeout 15s journalctl -b -k --no-pager -o short-monotonic 2>/dev/null | grep -Ei 'usb|ttyACM|ttyUSB|cdc_acm|under.?voltage' | tail -60 || true
printf '\nDiagnose gespeichert: %s\nEnthält ggf. GPS-Koordinaten. Bitte diese Ausgabe bzw. Datei zurückgeben.\n' "$report"
exec 1>&3 2>&3
wait "$tee_pid"
