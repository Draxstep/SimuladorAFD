"""Ventana principal de la aplicación"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from .automaton_editor import AutomatonEditor
from .evaluation_panel import EvaluationPanel
from .generation_panel import GenerationPanel

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador AFD")
        self.root.geometry("900x700")
        self.presenter = None
        
        self._create_menu()
        self._create_notebook()
    
    def set_presenter(self, presenter):
        self.presenter = presenter
        self.editor.set_presenter(presenter)
        self.evaluator.set_presenter(presenter)
        self.generator.set_presenter(presenter)
    
    def _create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nuevo", command=self._new_automaton)
        file_menu.add_command(label="Abrir", command=self._open_file)
        file_menu.add_command(label="Guardar", command=self._save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
    
    def _create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.editor = AutomatonEditor(self.notebook)
        self.evaluator = EvaluationPanel(self.notebook)
        self.generator = GenerationPanel(self.notebook)
        
        self.notebook.add(self.editor.frame, text="Editor AFD")
        self.notebook.add(self.evaluator.frame, text="Evaluar Cadenas")
        self.notebook.add(self.generator.frame, text="Generar Cadenas")
    
    def _new_automaton(self):
        if self.presenter:
            self.presenter.new_automaton()
    
    def _open_file(self):
        if self.presenter:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                self.presenter.load_automaton(filename)
    
    def _save_file(self):
        if self.presenter:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                self.presenter.save_automaton(filename)
    
    def show_message(self, title, message, type='info'):
        if type == 'info':
            messagebox.showinfo(title, message)
        elif type == 'error':
            messagebox.showerror(title, message)
        elif type == 'warning':
            messagebox.showwarning(title, message)