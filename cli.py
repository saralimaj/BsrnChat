# @file cli.py
# @brief Kommandozeilen-Client für das BSRN-Chatprogramm

import socket, threading
from network import udp_send, tcp_send, load_config
from discovery import discovery_send

def get_own_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def run(args):
    config = load_config()
    handle = args.handle or config.get("handle", "User")
    port = args.port[1] if args.port else config.get("port", [5000, 5001])[1]
    whoisport = args.whoisport or config.get("whoisport", 4000)
    broadcast_ip = config.get("broadcast_ip", "255.255.255.255")

    print(f"[CLI] Starte Chat als {handle} auf Port {port}")
    udp_send(broadcast_ip, whoisport, f"JOIN {handle} {port}")

    def listener():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("", port))
        sock.listen()
        while True:
            conn, addr = sock.accept()
            data = conn.recv(1024).decode()
            print(f"[TCP] Von {addr}: {data}")
            conn.close()

    threading.Thread(target=listener, daemon=True).start()

    try:
        while True:
            cmd = input("> ").strip()
            if cmd == "exit":
                udp_send(broadcast_ip, whoisport, f"LEAVE {handle}")
                print("[CLI] Chat verlassen.")
                break
            elif cmd == "who":
                udp_send(broadcast_ip, whoisport, "WHO")
            elif cmd.startswith("msg "):
                _, ziel, *text = cmd.split()
                msg = " ".join(text)
                tcp_send("127.0.0.1", port, f"MSG {ziel} {msg}")
            else:
                print("[CLI] Befehle: msg <Name> <Text> | who | exit")
    except KeyboardInterrupt:
        udp_send(broadcast_ip, whoisport, f"LEAVE {handle}")
        print("[CLI] Abgebrochen durch Benutzer")