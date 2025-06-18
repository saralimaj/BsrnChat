import argparse
from network import load_config
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--handle', type=str)
    parser.add_argument('--port', nargs=2, type=int)
    parser.add_argument('--whoisport', type=int)
    parser.add_argument('--autoreply', type=str)
    parser.add_argument('--cli', action='store_true')
    args = parser.parse_args()

    config = load_config()
    if config.get("debug"):
        import logging
        logging.basicConfig(level=logging.DEBUG)

    if args.cli:
        import cli
        cli.run(args)
    else:
        import tkinter as tk
        from chat_gui_client import ChatGUI
        root = tk.Tk()
        app = ChatGUI(root)
        root.mainloop()