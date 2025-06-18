#!/bin/bash

# Starte CLI und GUI Clients für lokalen Test

cd "$(dirname "$0")"

echo "[INFO] Bereinige vorherige Chatlogs..."
rm -f chat_log_Sara.txt chat_log_Ilirjon.txt

echo "[INFO] Starte Chat-GUI (Sara) auf Port 5101..."
osascript -e 'tell application "Terminal"
    do script "cd \"'"$PWD"'\" && python3 main.py --handle Sara --port 5100 5101 --whoisport 4000"
end tell'

sleep 2

echo "[INFO] Starte CLI-Client (Ilirjon) auf Port 5201..."
osascript -e 'tell application "Terminal"
    do script "cd \"'"$PWD"'\" && python3 main.py --cli --handle Ilirjon --port 5200 5201 --whoisport 4000"
end tell'

sleep 1

echo "[INFO] Starte Test erfolgreich. Kommunikation über UDP und TCP aktiv."
echo "Tipp: In CLI 'msg Sara <Text>' eingeben oder 'who' abfragen."

