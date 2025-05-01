# src/perceptrader/gui/tk_dashboard.py

import threading
import time
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Dict

import tkinter as tk
from tkinter import ttk

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from perceptrader.config.settings import settings
from perceptrader.utils.logger import setup_logger


class TkDashboard:
    """Tkinter dashboard for real-time monitoring of PerceptraderAI."""

    REFRESH_MS = 5000  # refresh interval in milliseconds
    MAX_POINTS = 100  # max points to keep in rolling chart

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("PerceptraderAI Dashboard")

        # Logger for internal events
        self.logger = setup_logger("dashboard")

        # Shared data structures
        # e.g. {'EURUSD_M1': 123.45, 'USDJPY_M5': -67.89}
        self.pnl_data: Dict[str, float] = {f"{s}_{tf}": 0.0
                                           for s in settings.SYMBOLS
                                           for tf in settings.TIMEFRAMES}
        self.time_series = deque(maxlen=self.MAX_POINTS)
        self.pnl_series = deque(maxlen=self.MAX_POINTS)

        # Top‐level frames
        self._build_status_frame()
        self._build_pnl_frame()
        self._build_chart_frame()
        self._build_todo_frame()

        # Start periodic update
        self._schedule_refresh()

    def _build_status_frame(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Workflow Status")
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.status_var = tk.StringVar(value="Initializing…")
        ttk.Label(frame, textvariable=self.status_var).pack(anchor="w", padx=5, pady=5)

    def _build_pnl_frame(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Live PnL per Symbol")
        frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        cols = ("symbol", "pnl")
        self.pnl_table = ttk.Treeview(frame, columns=cols, show="headings", height=5)
        for c in cols:
            self.pnl_table.heading(c, text=c.upper())
            self.pnl_table.column(c, width=100, anchor="center")
        for sym in self.pnl_data:
            self.pnl_table.insert("", "end", iid=sym, values=(sym, f"{0.0:.2f}"))
        self.pnl_table.pack(fill="both", expand=True)

    def _build_chart_frame(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Total PnL Over Time")
        frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)
        self.fig = Figure(figsize=(5, 3))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Total PnL")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("PnL")
        self.line, = self.ax.plot([], [], linewidth=2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _build_todo_frame(self) -> None:
        frame = ttk.LabelFrame(self.root, text="To-Do / Next Tasks")
        frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.todo_var = tk.StringVar(value="Loading next tasks…")
        ttk.Label(frame, textvariable=self.todo_var, justify="left").pack(anchor="w", padx=5, pady=5)

    def _schedule_refresh(self) -> None:
        self.root.after(self.REFRESH_MS, self._refresh)

    def _refresh(self) -> None:
        """Fetch latest metrics and update all widgets."""
        try:
            # 1) Update status (stub: rotate stages)
            now = datetime.utcnow().strftime("%H:%M:%S")
            stage = f"Last refresh at {now}"
            self.status_var.set(stage)

            # 2) Update PnL table (stub: simulate random walk or read from a metrics store)
            total = 0.0
            for sym in self.pnl_data:
                # In real use: fetch from a shared memory, queue, or log parsing
                delta = (0.5 - time.time() % 1) * 0.1  # dummy variation
                self.pnl_data[sym] += delta
                total += self.pnl_data[sym]
                self.pnl_table.set(sym, column="pnl", value=f"{self.pnl_data[sym]:.2f}")

            # 3) Update rolling chart
            self.time_series.append(datetime.now())
            self.pnl_series.append(total)
            xs = list(self.time_series)
            ys = list(self.pnl_series)
            self.line.set_data(xs, ys)
            self.ax.relim()
            self.ax.autoscale_view()
            self.canvas.draw()

            # 4) Update to-do list (stub)
            next_run = (datetime.now().timestamp() + settings.PAPER_DURATION)
            nxt = datetime.fromtimestamp(next_run).strftime("%Y-%m-%d %H:%M:%S")
            self.todo_var.set(f"Next paper-test at ~ {nxt}")

            self.logger.info("Dashboard refreshed")
        except Exception as e:
            self.logger.exception("Error during dashboard refresh: %s", e)

        # Schedule next update
        self._schedule_refresh()

    def run(self) -> None:
        """Start the Tkinter mainloop (blocking)."""
        self.root.mainloop()


def start_dashboard_in_thread() -> threading.Thread:
    """
    Helper to start the dashboard without blocking
    the main orchestrator flow.
    """
    thread = threading.Thread(target=TkDashboard().run, daemon=True)
    thread.start()
    return thread
