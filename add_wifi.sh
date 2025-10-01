#!/bin/bash
# Usage: ./add_wifi.sh "SSID_NAME" "WIFI_PASSWORD"

# On the latest Raspberry Pi OS (Bookworm, 2023+), network management 
# is handled by NetworkManager (instead of dhcpcd used in older releases).

SSID_NAME="$1"
WIFI_PASSWORD="$2"

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 \"SSID_NAME\" \"WIFI_PASSWORD\""
    echo "For classroom router setup, use:"
    echo "$0 \"meWIFI-Classroom\" \"analysis-SUNRISE-grecian\""
    exit 1
fi

SSID_NAME="$1"
WIFI_PASSWORD="$2"

echo "Adding Wi-Fi profile for SSID: $SSID_NAME"

sudo nmcli connection add type wifi ifname wlan0 \
    con-name "$SSID_NAME" ssid "$SSID_NAME" \
    wifi-sec.key-mgmt wpa-psk wifi-sec.psk "$WIFI_PASSWORD" \
    connection.autoconnect yes

echo "Done. The profile will connect automatically when in range."
