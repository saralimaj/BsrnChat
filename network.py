"""
@file network.py
@brief TCP und UDP Netzwerkfunktionen für SLCP.
"""
import socket, toml, os, logging

def udp_send(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (ip, port))
    logging.debug(f"[UDP] an {ip}:{port}: {message}")
    sock.close()

def udp_listener(port, callback):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", port))
    while True:
        msg, addr = sock.recvfrom(1024)
        logging.debug(f"[UDP-Empf.] {addr}: {msg}")
        callback(msg.decode(), addr)

def tcp_send(ip, port, message):
    with socket.create_connection((ip, port)) as s:
        s.sendall(message.encode())
    logging.debug(f"[TCP] MSG an {ip}:{port}: {message}")

def tcp_send_image(ip, port, imagepath):
    with socket.create_connection((ip, port)) as s:
        with open(imagepath, 'rb') as f:
            s.sendfile(f)
    logging.debug(f"[TCP] Bild an {ip}:{port}: {imagepath}")

def tcp_listener(port, callback):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", port))
    sock.listen()
    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)
        callback(data, addr)
        conn.close()
        logging.debug(f"[TCP Empfang] von {addr}: {data}")

def load_config(path="config.toml"):
    try:
        with open(path, "r") as f:
            return toml.load(f)
    except:
        with open("config.example.toml", "r") as f:
            return toml.load(f)

def save_config(config, path="config.toml"):
    with open(path, "w") as f:
        toml.dump(config, f)