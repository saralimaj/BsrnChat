#!/bin/bash

# lan_setup.command – LAN-Teststart mit zwei GUI-Clients
# Erzeugt config.toml für GUI1 und GUI2 mit Broadcast-IP und startet beide

cd "$(dirname "$0")"

# === Einstellungen ===
DEFAULT_WHOISPORT=4000
GUI1_PORT=(5100 5101)
GUI2_PORT=(5200 5201)
BROADCAST_IP="10.129.170.255"  # ← Hier ggf. anpassen

read -p "Handle für GUI 1: " GUI1_HANDLE
read -p "Handle für GUI 2: " GUI2_HANDLE

# === GUI 1 config.toml ===
cat > config_gui1.toml <<EOF
handle = "$GUI1_HANDLE"
port = [${GUI1_PORT[0]}, ${GUI1_PORT[1]}]
whoisport = $DEFAULT_WHOISPORT
autoreply = "Bin im LAN-Test (GUI1)"
imagepath = "~/chat_images"
broadcast_ip = "$BROADCAST_IP"
debug = true
EOF

# === GUI 2 config_gui2.toml ===
cat > config_gui2.toml <<EOF
handle = "$GUI2_HANDLE"
port = [${GUI2_PORT[0]}, ${GUI2_PORT[1]}]
whoisport = $DEFAULT_WHOISPORT
autoreply = "Bin im LAN-Test (GUI2)"
imagepath = "~/chat_images"
broadcast_ip = "$BROADCAST_IP"
debug = true
EOF

# === Starte GUI 1 ===
echo "[INFO] Starte GUI 1 ($GUI1_HANDLE)..."
osascript -e 'tell application "Terminal"
  do script "cd \"'"$PWD"'\" && source .venv/bin/activate && cp config_gui1.toml config.toml && python3 main.py --handle '"$GUI1_HANDLE"' --port '${GUI1_PORT[0]}' '${GUI1_PORT[1]}' --whoisport '$DEFAULT_WHOISPORT'"
end tell'

sleep 2

# === Starte GUI 2 ===
echo "[INFO] Starte GUI 2 ($GUI2_HANDLE)..."
osascript -e 'tell application "Terminal"
  do script "cd \"'"$PWD"'\" && source .venv/bin/activate && cp config_gui2.toml config.toml && python3 main.py --handle '"$GUI2_HANDLE"' --port '${GUI2_PORT[0]}' '${GUI2_PORT[1]}' --whoisport '$DEFAULT_WHOISPORT'"
end tell'

sleep 1
echo "[FERTIG] Beide GUIs aktiv: $GUI1_HANDLE & $GUI2_HANDLE"
echo "[TIPP] Kommunikation über Broadcast ($BROADCAST_IP)"