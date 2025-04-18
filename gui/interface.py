# gui/interface.py

import tkinter as tk
from tkinter import ttk
from utils.logger import setup_logger


class TradingInterface:
    def __init__(self, root):
        self.logger = setup_logger("GUI")
        self.root = root
        self.root.title("PerceptraderAI")
        self.create_widgets()
        self.running = False  # Track trading state

    def create_widgets(self):
        # Symbol input
        ttk.Label(self.root, text="نماد:").grid(row=0, column=0, padx=5, pady=5)
        self.symbol = ttk.Entry(self.root)
        self.symbol.grid(row=0, column=1, padx=5, pady=5)

        # Control buttons
        self.start_btn = ttk.Button(self.root, text="شروع", command=self.start)
        self.stop_btn = ttk.Button(self.root, text="توقف", command=self.stop, state=tk.DISABLED)

        self.start_btn.grid(row=1, column=0, padx=5, pady=5)
        self.stop_btn.grid(row=1, column=1, padx=5, pady=5)

    def start(self):
        if not self.running:
            sym = self.symbol.get()
            if sym:  # Validate input
                self.running = True
                self.logger.info(f"Start trading {sym}")
                self.start_btn.config(state=tk.DISABLED)
                self.stop_btn.config(state=tk.NORMAL)
                self.symbol.config(state=tk.DISABLED)
            else:
                self.logger.warning("Please enter a symbol")

    def stop(self):
        if self.running:
            self.running = False
            self.logger.info("Stop trading")
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.symbol.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = TradingInterface(root)
    root.mainloop()  # Don't forget the main loop!
