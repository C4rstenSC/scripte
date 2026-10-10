#!/usr/bin/env bash
set -Eeuo pipefail

# Allgemeiner Update-Starter. Das öffentliche GitHub-Paket ist verschlüsselt.
# Raspi-Scripte 0.7.2 lädt und entschlüsselt es vorab und legt die geprüfte ZIP
# im Benutzer-Home ab. Dadurch liegt das Paket auf GitHub nicht im Klartext.
readonly ADDON_ENCRYPTED_URL="https://raw.githubusercontent.com/C4rstenSC/scripte/main/RaspberryPI_Addons/Witty%20PI%20Addon/witty_addon.zip.enc"

log() { printf '[Witty-Launcher] %s\n' "$*"; }
die() { printf '[Witty-Launcher] FEHLER: %s\n' "$*" >&2; exit 1; }

console_install_blocked() {
    cat >&2 <<'EOF'
[Witty-Launcher] UPDATE GESPERRT.
[Witty-Launcher] Diese update.sh darf nicht manuell über SSH oder eine andere Konsole gestartet werden.
[Witty-Launcher] Bitte Raspi-Scripte für Windows öffnen und dort „Witty Software update“ verwenden.
EOF
    exit 23
}

# Eine Das Update verändert Dienste und Einstellungen.
# Deshalb akzeptiert der Starter ausschließlich die einmalige, vom verbundenen
# Windows-Programm erzeugte Freigabe. Die Datei wird vor allen Änderungen
# verbraucht; ein kopierter Konsolenbefehl lässt sich danach nicht wiederholen.
launcher_user="${SUDO_USER:-}"
[[ -n "$launcher_user" && "$launcher_user" != root ]] || console_install_blocked
id "$launcher_user" >/dev/null 2>&1 || console_install_blocked
launcher_home="$(getent passwd "$launcher_user" 2>/dev/null | cut -d: -f6)"
ticket_file="$launcher_home/.raspi-scripte-update.ticket"
session_token="${WITTY_WINDOWS_SESSION:-}"
[[ "$session_token" =~ ^[0-9A-Fa-f]{64}$ ]] || console_install_blocked
[[ -f "$ticket_file" && ! -L "$ticket_file" ]] || console_install_blocked
[[ "$(stat -c '%U' "$ticket_file" 2>/dev/null || true)" == "$launcher_user" ]] || console_install_blocked
ticket_mode="$(stat -c '%a' "$ticket_file" 2>/dev/null || true)"
[[ "$ticket_mode" == 600 || "$ticket_mode" == 400 ]] || console_install_blocked
IFS= read -r ticket_token < "$ticket_file" || console_install_blocked
[[ "$ticket_token" == "$session_token" ]] || console_install_blocked
rm -f -- "$ticket_file"
unset ticket_token session_token WITTY_WINDOWS_SESSION
export WITTY_WINDOWS_AUTHORIZED=1

[[ "${EUID:-$(id -u)}" -eq 0 ]] || die "Bitte mit sudo starten: sudo ./update.sh"

missing=false
for command_name in curl unzip; do
    command -v "$command_name" >/dev/null 2>&1 || missing=true
done
if [[ "$missing" == true ]]; then
    if ! DEBIAN_FRONTEND=noninteractive dpkg --force-confold --configure -a; then
        DEBIAN_FRONTEND=noninteractive apt-get -o DPkg::Lock::Timeout=120 \
            -o Dpkg::Options::=--force-confold --fix-broken install -y || \
            die "Die unterbrochene Debian-Paketinstallation konnte nicht repariert werden."
        DEBIAN_FRONTEND=noninteractive dpkg --force-confold --configure -a || \
            die "Die Debian-Pakete konnten nicht vollstaendig konfiguriert werden."
    fi
    apt-get -o DPkg::Lock::Timeout=120 -o Dpkg::Options::=--force-confold update
    DEBIAN_FRONTEND=noninteractive apt-get -o DPkg::Lock::Timeout=120 \
        -o Dpkg::Options::=--force-confold install -y curl unzip ca-certificates
fi

temp_base="${TMPDIR:-/var/tmp}"
[[ -d "$temp_base" ]] || temp_base=/tmp
work_dir="$(mktemp -d "$temp_base/witty-update-github.XXXXXX")"
cleanup() { rm -rf -- "$work_dir"; }
trap cleanup EXIT

archive="$work_dir/witty_addon.zip"
update_source=windows-upload
if [[ -n "${WITTY_ADDON_LOCAL_ZIP:-}" ]]; then
    [[ -f "$WITTY_ADDON_LOCAL_ZIP" && -r "$WITTY_ADDON_LOCAL_ZIP" ]] || \
        die "Das vorbereitete Witty-Paket ist nicht lesbar: $WITTY_ADDON_LOCAL_ZIP"
    log "Verwende die vom Windows-Programm vorbereitete witty_addon.zip ..."
    cp -- "$WITTY_ADDON_LOCAL_ZIP" "$archive"
    update_source=windows-upload
else
    launcher_user="${SUDO_USER:-$(id -un)}"
    launcher_home="$(getent passwd "$launcher_user" 2>/dev/null | cut -d: -f6)"
    prepared_zip="${launcher_home:-/home/$launcher_user}/witty_addon.zip"
    if [[ -x /usr/local/sbin/witty-package-decrypt ]]; then
        encrypted_archive="$work_dir/witty_addon.zip.enc"
        log "Lade das verschlüsselte Witty-Paket von GitHub ..."
        curl --fail --location --show-error --silent --connect-timeout 15 --max-time 180 \
            --retry 5 --retry-delay 2 --retry-all-errors \
            --output "$encrypted_archive" "${ADDON_ENCRYPTED_URL}?download=$(date +%s)" || \
            die "GitHub-Download des verschlüsselten Pakets fehlgeschlagen."
        /usr/local/sbin/witty-package-decrypt "$encrypted_archive" "$archive" || \
            die "Das GitHub-Paket konnte auf dem Raspberry nicht entschlüsselt werden."
        update_source=raspberry-decrypt
    elif [[ -f "$prepared_zip" && -r "$prepared_zip" ]]; then
        log "Verwende die von Raspi-Scripte vorbereitete witty_addon.zip aus $prepared_zip ..."
        cp -- "$prepared_zip" "$archive"
    else
        die "Kein entschlüsseltes Witty-Paket und kein lokaler Entschlüsseler vorhanden. Bitte zuerst über Raspi-Scripte 0.7.2 installieren."
    fi
fi

unzip -tq "$archive" >/dev/null || die "Das GitHub-ZIP ist beschaedigt."
if unzip -Z1 "$archive" | grep -Eq '(^/|(^|/)\.\.(/|$))'; then
    die "Unsichere Dateipfade im ZIP-Archiv."
fi

unzip -q "$archive" -d "$work_dir/extracted"
runner="$work_dir/extracted/witty_addon/update_addon.sh"
[[ -f "$runner" ]] || die "update_addon.sh fehlt im GitHub-ZIP."
chmod 0755 "$runner"
package_version="$(tr -d '\r\n' < "$work_dir/extracted/witty_addon/VERSION")"
[[ "$package_version" =~ ^[0-9]+([.][0-9]+)+$ ]] || die "Ungültige Paketversion."
log "Geprüfte Witty-Paketversion: $package_version"


printf '[WITTY-CONTROL] event=update_started source=%s\n' "$update_source"
runner_rc=0
bash "$runner" "$@" || runner_rc=$?
if (( runner_rc != 0 )); then
    result=error
    (( runner_rc == 130 )) && result=cancelled
    printf '[WITTY-CONTROL] event=update_finished result=%s exit_code=%s\n' "$result" "$runner_rc"
    exit "$runner_rc"
fi
printf '[WITTY-CONTROL] event=update_finished result=success\n'
