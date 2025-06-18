# @file chat_gui_client.py
# @brief Finalisierte GUI mit Dark Mode, Auto-Scroll, Button-Hover-Animation und Scrollverlauf-Speicherung.

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from network import *
from cli import get_own_ip
import queue, threading, os, logging, datetime

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
        self.chatlog_path = f"chat_log_{self.handle}.txt"

        master.title("BSRN Chat GUI")
        master.configure(bg="#2b2b2b")

        # === Dark Mode Stil ===
        style = ttk.Style(master)
        style.theme_use('clam')
        style.configure('.', background='#2b2b2b', foreground='#f0f0f0', fieldbackground='#3c3f41')
        style.configure('TButton', background='#4a4a4a', foreground='#ffffff')
        style.map('TButton', background=[('active', '#5a5a5a')])

        # Layout
        self.chat = scrolledtext.ScrolledText(master, state='disabled', width=60, height=20, bg='#2b2b2b', fg='#f0f0f0', insertbackground='white')
        self.chat.grid(row=0, column=0, columnspan=3, padx=10, pady=5)

        self.entry = tk.Entry(master, bg='#3c3f41', fg='white', insertbackground='white')
        self.entry.grid(row=1, column=0, sticky='we', padx=10)

        self.senden_btn = ttk.Button(master, text="🕊️ Senden", command=self.sende_text)
        self.senden_btn.grid(row=1, column=1, padx=5)

        self.ziel_menu = ttk.Combobox(master, values=["(niemand)"])
        self.ziel_menu.grid(row=2, column=0, padx=10, sticky='we')
        self.ziel_menu.set("(niemand)")

        self.bild_btn = ttk.Button(master, text="📷 Bild senden", command=self.sende_bild)
        self.bild_btn.grid(row=2, column=1, padx=5)

        self.save_btn = ttk.Button(master, text="💾 Speichern", command=self.speichere_config)
        self.save_btn.grid(row=2, column=2, padx=5)

        self.nutzer_listbox = tk.Listbox(master, height=6, bg='#3c3f41', fg='white')
        self.nutzer_listbox.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky='we')

        self.lade_chatverlauf()

    def sende_text(self):
        ziel = self.ziel_menu.get()
        msg = self.entry.get()
        if ziel and ziel != "(niemand)":
            tcp_send("127.0.0.1", self.port, f"MSG {ziel} {msg}")
            self.zeige_nachricht(f"Du an {ziel}: {msg}")
            self.speichere_chatverlauf(f"Du an {ziel}: {msg}")
        self.entry.delete(0, tk.END)

    def sende_bild(self):
        ziel = self.ziel_menu.get()
        pfad = filedialog.askopenfilename()
        if ziel and pfad:
            groesse = os.path.getsize(pfad)
            tcp_send("127.0.0.1", self.port, f"IMG {ziel} {groesse}")
            tcp_send_image("127.0.0.1", self.port, pfad)
            info = f"Bild an {ziel} gesendet: {os.path.basename(pfad)}"
            self.zeige_nachricht(info)
            self.speichere_chatverlauf(info)

    def speichere_config(self):
        self.config['handle'] = self.handle
        self.config['port'] = [self.port - 1, self.port]
        save_config(self.config)
        messagebox.showinfo("Info", "Konfiguration gespeichert.")

    def zeige_nachricht(self, text):
        self.chat.config(state='normal')
        self.chat.insert(tk.END, text + "\n")
        self.chat.see(tk.END)  # Auto-Scroll
        self.chat.config(state='disabled')

    def speichere_chatverlauf(self, text):
        with open(self.chatlog_path, "a") as f:
            zeit = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            f.write(f"{zeit} {text}\n")

    def lade_chatverlauf(self):
        if os.path.exists(self.chatlog_path):
            with open(self.chatlog_path, "r") as f:
                self.chat.config(state='normal')
                self.chat.insert(tk.END, f.read())
                self.chat.see(tk.END)
                self.chat.config(state='disabled')