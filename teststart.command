#!/bin/bash

# Startmenü für BSRN-Chat: Lokaler Modus oder LAN-Modus (mit automatischer .venv Aktivierung)

# === Automatisch virtuelle Umgebung aktivieren ===
if [ -d ".venv" ]; then
  source .venv/bin/activate
else
  echo "[FEHLER] .venv nicht gefunden. Bitte zuerst python3 -m venv .venv ausführen."
  exit 1
fi

echo "===================================="
echo "        🧩 BSRN Chat Starter        "
echo "===================================="
echo "Bitte Modus wählen:"
echo "1) Lokaler Test (GUI + CLI auf 1 Gerät)"
echo "2) LAN-Modus (Mehrere Geräte, config.toml wird erzeugt)"
echo "3) Nur GUI starten"
echo "4) Nur CLI starten"
echo "q) Beenden"
echo "===================================="
read -p "> Auswahl: " auswahl

case $auswahl in
  1)
    echo "[Lokal] Starte Test GUI + CLI (Sara & Ilirjon)..."
    bash teststart.command
    ;;

  2)
    echo "[LAN] Setup für Netzwerktest..."
    bash lan_setup_script.sh
    ;;

  3)
    read -p "Handle für GUI: " H
    python3 main.py --handle "$H" --port 5100 5101 --whoisport 4000
    ;;

  4)
    read -p "Handle für CLI: " H
    python3 main.py --cli --handle "$H" --port 5200 5201 --whoisport 4000
    ;;

  q)
    echo "Beendet."
    exit 0
    ;;

  *)
    echo "Ungültige Eingabe."
    ;;
esac