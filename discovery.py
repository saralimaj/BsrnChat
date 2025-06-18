"""
@file discovery.py
@brief Discovery-Dienst zur Verwaltung von JOIN, LEAVE, WHO und KNOWNUSERS Nachrichten.
"""
import socket, threading, logging
bekannte_nutzer = {}

def discovery_listener(port, callback):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", port))
    while True:
        msg, addr = sock.recvfrom(1024)
        logging.debug(f"[UDP-Empfang] {addr}: {msg}")
        callback(msg.decode(), addr)

def discovery_send(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(message.encode(), (ip, port))
    logging.debug(f"[UDP-Sendung] an {ip}:{port} => {message}")
    sock.close()