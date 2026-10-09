#!/usr/bin/env bash
set -Eeuo pipefail

# Allgemeiner Installationsstarter fuer Raspberry Pi OS. Das Windows-Programm
# lädt das verschlüsselte GitHub-Paket, entschlüsselt und prüft es und überträgt
# anschließend diese Klartext-ZIP nur zum Raspberry.
readonly ADDON_ENCRYPTED_URL="https://raw.githubusercontent.com/C4rstenSC/scripte/main/RaspberryPI_Addons/Witty%20PI%20Addon/witty_addon.zip.enc"

log() { printf '[Witty-Launcher] %s\n' "$*"; }
die() { printf '[Witty-Launcher] FEHLER: %s\n' "$*" >&2; exit 1; }

console_install_blocked() {
    cat >&2 <<'EOF'
[Witty-Launcher] INSTALLATION GESPERRT.
[Witty-Launcher] Diese installer.sh darf nicht manuell über SSH oder eine andere Konsole gestartet werden.
[Witty-Launcher] Bitte Raspi-Scripte für Windows öffnen und dort „Basis Installation“ verwenden.
EOF
    exit 23
}

# Eine Basisinstallation verändert Hardware-, Dienst- und GPS-Einstellungen.
# Deshalb akzeptiert der Starter ausschließlich die einmalige, vom verbundenen
# Windows-Programm erzeugte Freigabe. Die Datei wird vor allen Änderungen
# verbraucht; ein kopierter Konsolenbefehl lässt sich danach nicht wiederholen.
launcher_user="${SUDO_USER:-}"
[[ -n "$launcher_user" && "$launcher_user" != root ]] || console_install_blocked
id "$launcher_user" >/dev/null 2>&1 || console_install_blocked
launcher_home="$(getent passwd "$launcher_user" 2>/dev/null | cut -d: -f6)"
ticket_file="$launcher_home/.raspi-scripte-install.ticket"
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

[[ "${EUID:-$(id -u)}" -eq 0 ]] || die "Bitte mit sudo starten: sudo ./installer.sh"

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
work_dir="$(mktemp -d "$temp_base/witty-install-github.XXXXXX")"
cleanup() { rm -rf -- "$work_dir"; }
trap cleanup EXIT

archive="$work_dir/witty_addon.zip"
if [[ -n "${WITTY_ADDON_LOCAL_ZIP:-}" ]]; then
    [[ -f "$WITTY_ADDON_LOCAL_ZIP" ]] || die "Das übergebene lokale Witty-Paket fehlt: $WITTY_ADDON_LOCAL_ZIP"
    log "Verwende die vom Windows-Programm übertragene witty_addon.zip ..."
    cp -- "$WITTY_ADDON_LOCAL_ZIP" "$archive"
else
    launcher_user="${SUDO_USER:-$(id -un)}"
    launcher_home="$(getent passwd "$launcher_user" 2>/dev/null | cut -d: -f6)"
    prepared_zip="${launcher_home:-/home/$launcher_user}/witty_addon.zip"
    if [[ -f "$prepared_zip" && -r "$prepared_zip" ]]; then
        log "Verwende die von Raspi-Scripte vorbereitete witty_addon.zip aus $prepared_zip ..."
        cp -- "$prepared_zip" "$archive"
    elif [[ -x /usr/local/sbin/witty-package-decrypt ]]; then
        encrypted_archive="$work_dir/witty_addon.zip.enc"
        log "Lade das verschlüsselte Witty-Paket von GitHub ..."
        curl --fail --location --show-error --silent --connect-timeout 15 --max-time 180 \
            --retry 5 --retry-delay 2 --retry-all-errors \
            --output "$encrypted_archive" "${ADDON_ENCRYPTED_URL}?download=$(date +%s)" || \
            die "GitHub-Download des verschlüsselten Pakets fehlgeschlagen."
        /usr/local/sbin/witty-package-decrypt "$encrypted_archive" "$archive" || \
            die "Das GitHub-Paket konnte auf dem Raspberry nicht entschlüsselt werden."
    else
        die "Erstinstallation benötigt Raspi-Scripte 0.6; danach kann der Raspberry verschlüsselte Updates selbst verarbeiten."
    fi
fi

unzip -tq "$archive" >/dev/null || die "Das GitHub-ZIP ist beschaedigt."
if unzip -Z1 "$archive" | grep -Eq '(^/|(^|/)\.\.(/|$))'; then
    die "Unsichere Dateipfade im ZIP-Archiv."
fi

unzip -q "$archive" -d "$work_dir/extracted"
runner="$work_dir/extracted/witty_addon/installer_addon.sh"
[[ -f "$runner" ]] || die "installer_addon.sh fehlt im GitHub-ZIP."
chmod 0755 "$runner"

# Mit jeder Basisinstallation auch den Update-Starter im Home des aufrufenden
# SSH-Benutzers erneuern. So bleibt keine ältere update.sh neben dem neuen
# Add-on liegen.
update_launcher="$work_dir/extracted/witty_addon/launchers/update.sh"
[[ -f "$update_launcher" ]] || die "launchers/update.sh fehlt im GitHub-ZIP."
if [[ -n "$launcher_user" && "$launcher_user" != root ]] && id "$launcher_user" >/dev/null 2>&1; then
    launcher_home="$(getent passwd "$launcher_user" | cut -d: -f6)"
    launcher_group="$(id -gn "$launcher_user")"
    if [[ -n "$launcher_home" && -d "$launcher_home" ]]; then
        install -o "$launcher_user" -g "$launcher_group" -m 0755 \
            "$update_launcher" "$launcher_home/update.sh"
        log "update.sh im Benutzer-Home aktualisiert: $launcher_home/update.sh"
    fi
fi

printf '[WITTY-CONTROL] event=install_started source=windows-upload\n'
runner_rc=0
bash "$runner" "$@" || runner_rc=$?
if (( runner_rc != 0 )); then
    printf '[WITTY-CONTROL] event=install_finished result=error exit_code=%s\n' "$runner_rc"
    exit "$runner_rc"
fi
printf '[WITTY-CONTROL] event=install_finished result=success\n'
