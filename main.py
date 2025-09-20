#!/usr/bin/env python3
"""Punto de entrada principal del simulador AFD"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.views.main_window import MainWindow
from src.presenters.main_presenter import MainPresenter
from src.models.automaton import Automaton
import tkinter as tk

def main():
    root = tk.Tk()
    model = Automaton()
    view = MainWindow(root)
    presenter = MainPresenter(model, view)
    view.set_presenter(presenter)
    root.mainloop()

if __name__ == "__main__":
    main()