#!/bin/bash

# teststart.command – Starte GUI + CLI lokal zum Testen

cd "$(dirname "$0")"

echo "[INFO] Bereinige vorherige Chatlogs..."
rm -f chat_log_Sara.txt chat_log_Ilirjon.txt

# Starte GUI (Sara)
echo "[INFO] Starte Chat-GUI (Sara) auf Port 5101..."
osascript -e 'tell application "Terminal"
  do script "cd \"'"$PWD"'\" && source .venv/bin/activate && python3 main.py --handle Sara --port 5100 5101 --whoisport 4000"
end tell'

sleep 2

# Starte CLI (Ilirjon)
echo "[INFO] Starte CLI-Client (Ilirjon) auf Port 5201..."
osascript -e 'tell application "Terminal"
  do script "cd \"'"$PWD"'\" && source .venv/bin/activate && python3 main.py --cli --handle Ilirjon --port 5200 5201 --whoisport 4000"
end tell'

sleep 1

echo "[INFO] Teststart erfolgreich – Kommunikation lokal aktiv."
echo "[HINWEIS] CLI: 'msg Sara <Text>' oder 'who' eingeben."