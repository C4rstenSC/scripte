#!/bin/bash

set -euo pipefail

# ------------------------------------------------------------
# Witty Pi 5 Schedule Copier / Date Editor / Activator
# Raspberry Pi OS 64-bit / Trixie
# ------------------------------------------------------------

WP5_CMD="wp5"

# Check whether wp5 is available
if ! command -v "$WP5_CMD" >/dev/null 2>&1; then
    echo "ERROR: wp5 could not be found."
    exit 1
fi

# expect is required for menu automation
if ! command -v expect >/dev/null 2>&1; then
    echo "ERROR: 'expect' is not installed."
    echo
    echo "Please install it with:"
    echo "  sudo apt update"
    echo "  sudo apt install expect"
    exit 1
fi

# Temporary working directory
WORKDIR="$(mktemp -d /tmp/wittypi_schedule_XXXXXX)"

cleanup() {
    rm -rf "$WORKDIR"
}

trap cleanup EXIT

cd "$WORKDIR"

echo
echo "=========================================="
echo " Witty Pi 5 Schedule Assistant"
echo "=========================================="
echo

read -r -p "Name of the existing script on the Witty Pi (for example: basis.wpi): " SOURCE_SCRIPT

if [[ -z "$SOURCE_SCRIPT" ]]; then
    echo "No filename was entered."
    exit 1
fi

# Safety check: only allow schedule file extensions
case "$SOURCE_SCRIPT" in
    *.wpi|*.act|*.skd)
        ;;
    *)
        echo "ERROR: The file must use .wpi, .act or .skd."
        exit 1
        ;;
esac

echo
echo "Downloading '$SOURCE_SCRIPT' from the Witty Pi..."
echo

expect <<EOF
set timeout 30

spawn $WP5_CMD

expect {
    -re "Manage schedule scripts" {
        # Already in the correct menu
    }

    -re "Please input.*:" {
        send "6\r"

        expect {
            -re "Manage schedule scripts" {}
            timeout {
                puts "ERROR: Could not reach the schedule management menu."
                exit 10
            }
        }
    }
}

expect -re "Please input.*:"
send "3\r"

expect {
    -re "filename.*:" {
        send "$SOURCE_SCRIPT\r"
    }

    -re "choose a number.*:" {
        send "$SOURCE_SCRIPT\r"
    }

    -re "Input a filename.*:" {
        send "$SOURCE_SCRIPT\r"
    }

    timeout {
        puts "ERROR: Could not find the download selection."
        exit 11
    }
}

expect {
    -re "Downloaded.*" {}
    -re "downloaded.*" {}
    -re "Download.*success" {}
    -re "Manage schedule scripts" {}
    timeout {}
}

send "\003"
expect eof
EOF

# Check whether the file was actually downloaded
if [[ ! -f "$SOURCE_SCRIPT" ]]; then
    echo
    echo "ERROR: '$SOURCE_SCRIPT' was not found in the working directory."
    echo
    echo "Working directory:"
    echo "  $WORKDIR"
    echo
    echo "The menu structure in your wp5 version may be different."
    exit 1
fi

echo
echo "Download completed successfully."
echo

# ------------------------------------------------------------
# Find BEGIN / END
# ------------------------------------------------------------

BEGIN_LINE="$(grep -E '^[[:space:]]*BEGIN[[:space:]]+[0-9]{4}-[0-9]{2}-[0-9]{2}' "$SOURCE_SCRIPT" | head -n1 || true)"
END_LINE="$(grep -E '^[[:space:]]*END[[:space:]]+[0-9]{4}-[0-9]{2}-[0-9]{2}' "$SOURCE_SCRIPT" | head -n1 || true)"

if [[ -z "$BEGIN_LINE" ]]; then
    echo "ERROR: No BEGIN line was found."
    exit 1
fi

if [[ -z "$END_LINE" ]]; then
    echo "ERROR: No END line was found."
    exit 1
fi

OLD_BEGIN_DATE="$(echo "$BEGIN_LINE" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -n1)"
OLD_END_DATE="$(echo "$END_LINE" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | head -n1)"

echo "Found:"
echo
echo "  $BEGIN_LINE"
echo "  $END_LINE"
echo

# ------------------------------------------------------------
# Validate dates
# ------------------------------------------------------------

valid_date() {
    local input="$1"

    [[ "$input" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || return 1

    local normalised
    normalised="$(date -d "$input" '+%Y-%m-%d' 2>/dev/null)" || return 1

    [[ "$normalised" == "$input" ]]
}

while true; do
    read -r -p "New START date [YYYY-MM-DD]: " NEW_BEGIN_DATE

    if valid_date "$NEW_BEGIN_DATE"; then
        break
    fi

    echo "Invalid date. Example: 2026-09-20"
done

while true; do
    read -r -p "New END date   [YYYY-MM-DD]: " NEW_END_DATE

    if ! valid_date "$NEW_END_DATE"; then
        echo "Invalid date. Example: 2026-09-25"
        continue
    fi

    if [[ "$NEW_END_DATE" < "$NEW_BEGIN_DATE" ]]; then
        echo "The END date must not be earlier than the START date."
        continue
    fi

    break
done

# ------------------------------------------------------------
# Create the new schedule file
# ------------------------------------------------------------

EXTENSION="${SOURCE_SCRIPT##*.}"
NEW_SCRIPT="${NEW_BEGIN_DATE}.${EXTENSION}"

cp "$SOURCE_SCRIPT" "$NEW_SCRIPT"

# Replace only the date and keep the existing time unchanged
sed -i -E \
    "0,/^([[:space:]]*BEGIN[[:space:]]+)[0-9]{4}-[0-9]{2}-[0-9]{2}/s//\1${NEW_BEGIN_DATE}/" \
    "$NEW_SCRIPT"

sed -i -E \
    "0,/^([[:space:]]*END[[:space:]]+)[0-9]{4}-[0-9]{2}-[0-9]{2}/s//\1${NEW_END_DATE}/" \
    "$NEW_SCRIPT"

echo
echo "New schedule:"
echo "------------------------------------------"
grep -E '^[[:space:]]*(BEGIN|END)[[:space:]]+' "$NEW_SCRIPT"
echo "------------------------------------------"
echo
echo "Filename:"
echo "  $NEW_SCRIPT"
echo

read -r -p "Upload and activate this schedule? [Y/n]: " ANSWER

case "${ANSWER:-Y}" in
    y|Y)
        ;;
    *)
        echo "Cancelled."
        exit 0
        ;;
esac

# ------------------------------------------------------------
# Upload and activate
# ------------------------------------------------------------

echo
echo "Uploading '$NEW_SCRIPT' and activating it..."
echo

expect <<EOF
set timeout 30

spawn $WP5_CMD

expect {
    -re "Manage schedule scripts" {
        # Already in the correct menu
    }

    -re "Please input.*:" {
        send "6\r"

        expect {
            -re "Manage schedule scripts" {}
            timeout {
                puts "ERROR: Could not reach the schedule management menu."
                exit 20
            }
        }
    }
}

expect -re "Please input.*:"
send "1\r"

expect {
    -re "Input a filename.*:" {
        send "$NEW_SCRIPT\r"
    }

    -re "filename.*:" {
        send "$NEW_SCRIPT\r"
    }

    timeout {
        puts "ERROR: Could not find the upload filename prompt."
        exit 21
    }
}

expect {
    -re "Uploaded.*" {}
    -re "uploaded.*" {}
    -re "Manage schedule scripts" {}
    timeout {}
}

expect -re "Please input.*:"
send "2\r"

expect {
    -re "Input a filename.*:" {
        send "$NEW_SCRIPT\r"
    }

    -re "filename.*:" {
        send "$NEW_SCRIPT\r"
    }

    timeout {
        puts "ERROR: Could not find the activation filename prompt."
        exit 22
    }
}

expect {
    -re "Activated.*" {}
    -re "activated.*" {}
    -re "Activation.*" {}
    -re "Manage schedule scripts" {}
    timeout {}
}

send "\003"
expect eof
EOF

echo
echo "=========================================="
echo " Done"
echo "=========================================="
echo
echo "Original schedule:"
echo "  $SOURCE_SCRIPT"
echo
echo "Changed:"
echo "  BEGIN: $OLD_BEGIN_DATE -> $NEW_BEGIN_DATE"
echo "  END:   $OLD_END_DATE -> $NEW_END_DATE"
echo
echo "Activated:"
echo "  $NEW_SCRIPT"
echo
echo "The temporary working directory will now be removed."
