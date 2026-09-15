#!/usr/bin/env bash
set -Eeuo pipefail

# Allgemeiner Installationsstarter fuer Raspberry Pi OS. Er laedt bei jedem
# Aufruf das aktuelle GitHub-Paket; installer_addon.sh verarbeitet danach die
# interaktiven Eingaben oder die Parameter des Windows-Programms.
readonly ADDON_URL="https://raw.githubusercontent.com/C4rstenSC/scripte/main/RaspberryPI_Addons/Witty%20PI%20Addon/witty_addon.zip"

log() { printf '[Witty-Launcher] %s\n' "$*"; }
die() { printf '[Witty-Launcher] FEHLER: %s\n' "$*" >&2; exit 1; }

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
log "Lade die aktuelle witty_addon.zip von GitHub ..."
curl --fail --location --show-error --silent --connect-timeout 15 --max-time 180 \
    --retry 5 --retry-delay 2 --retry-all-errors \
    --output "$archive" "${ADDON_URL}?download=$(date +%s)" || \
    die "GitHub-Download fehlgeschlagen."

unzip -tq "$archive" >/dev/null || die "Das GitHub-ZIP ist beschaedigt."
if unzip -Z1 "$archive" | grep -Eq '(^/|(^|/)\.\.(/|$))'; then
    die "Unsichere Dateipfade im ZIP-Archiv."
fi

unzip -q "$archive" -d "$work_dir/extracted"
runner="$work_dir/extracted/witty_addon/installer_addon.sh"
[[ -f "$runner" ]] || die "installer_addon.sh fehlt im GitHub-ZIP."
chmod 0755 "$runner"

printf '[WITTY-CONTROL] event=install_started source=github\n'
runner_rc=0
bash "$runner" "$@" || runner_rc=$?
if (( runner_rc != 0 )); then
    printf '[WITTY-CONTROL] event=install_finished result=error exit_code=%s\n' "$runner_rc"
    exit "$runner_rc"
fi
printf '[WITTY-CONTROL] event=install_finished result=success\n'
