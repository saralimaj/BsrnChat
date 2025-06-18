"""
@file chat_gui_client.py
@brief Grafische Benutzeroberfläche für den BSRN-Chat mit SLCP inkl. Nutzerliste, Bildversand und Autoreply.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from network import *
from cli import get_own_ip
import queue, threading, os, logging

class ChatGUI:
    def __init__(self, master):
        self.master = master
        self.queue = queue.Queue()
        self.config = load_config()
        if self.config.get("debug"):
            logging.basicConfig(level=logging.DEBUG)

        self.handle = self.config['handle']
        self.port = self.config['port'][1]
        self.broadcast_ip = self.config.get('broadcast_ip', '255.255.255.255')
        self.whoisport = self.config['whoisport']
        self.abwesend_text = self.config['autoreply']
        self.bildpfad = os.path.expanduser(self.config['imagepath'])

        master.title("BSRN Chat GUI")

        # Layout
        self.chat = scrolledtext.ScrolledText(master, state='disabled', width=60, height=20)
        self.chat.grid(row=0, column=0, columnspan=3, padx=10, pady=5)

        self.entry = tk.Entry(master)
        self.entry.grid(row=1, column=0, sticky='we', padx=10)

        self.senden_btn = ttk.Button(master, text="Senden", command=self.sende_text)
        self.senden_btn.grid(row=1, column=1, padx=5)

        self.ziel_menu = ttk.Combobox(master, values=["(niemand)"])
        self.ziel_menu.grid(row=2, column=0, padx=10, sticky='we')
        self.ziel_menu.set("(niemand)")

        self.bild_btn = ttk.Button(master, text="Bild senden", command=self.sende_bild)
        self.bild_btn.grid(row=2, column=1, padx=5)

        self.save_btn = ttk.Button(master, text="Speichern", command=self.speichere_config)
        self.save_btn.grid(row=2, column=2, padx=5)

        self.nutzer_listbox = tk.Listbox(master, height=6)
        self.nutzer_listbox.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky='we')

    def sende_text(self):
        ziel = self.ziel_menu.get()
        msg = self.entry.get()
        if ziel and ziel != "(niemand)":
            tcp_send("127.0.0.1", self.port, f"MSG {ziel} {msg}")
            self.zeige_nachricht(f"Du an {ziel}: {msg}")
        self.entry.delete(0, tk.END)

    def sende_bild(self):
        ziel = self.ziel_menu.get()
        pfad = filedialog.askopenfilename()
        if ziel and pfad:
            groesse = os.path.getsize(pfad)
            tcp_send("127.0.0.1", self.port, f"IMG {ziel} {groesse}")
            tcp_send_image("127.0.0.1", self.port, pfad)
            self.zeige_nachricht(f"Bild an {ziel} gesendet: {os.path.basename(pfad)}")

    def speichere_config(self):
        self.config['handle'] = self.handle
        self.config['port'] = [self.port - 1, self.port]
        save_config(self.config)
        messagebox.showinfo("Info", "Konfiguration gespeichert.")

    def zeige_nachricht(self, text):
        self.chat.config(state='normal')
        self.chat.insert(tk.END, text + "\n")
        self.chat.config(state='disabled')
