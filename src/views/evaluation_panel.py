"""Panel para evaluar cadenas"""

import tkinter as tk
from tkinter import ttk

class EvaluationPanel:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.presenter = None
        self._create_widgets()
    
    def set_presenter(self, presenter):
        self.presenter = presenter
    
    def _create_widgets(self):
        # Entrada de cadena
        ttk.Label(self.frame, text="Cadena a evaluar:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.string_entry = ttk.Entry(self.frame, width=40)
        self.string_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Button(self.frame, text="Evaluar", command=self._evaluate).grid(row=0, column=2, padx=10, pady=10)
        
        # Área de resultados
        ttk.Label(self.frame, text="Proceso paso a paso:").grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky='w')
        
        self.result_text = tk.Text(self.frame, height=20, width=70, wrap=tk.WORD)
        self.result_text.grid(row=2, column=0, columnspan=3, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.result_text.yview)
        scrollbar.grid(row=2, column=3, sticky='ns', pady=5)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        # Etiqueta de resultado
        self.result_label = ttk.Label(self.frame, text="", font=('Arial', 12, 'bold'))
        self.result_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
    
    def _evaluate(self):
        if self.presenter:
            input_string = self.string_entry.get()
            result = self.presenter.evaluate_string(input_string)
            if result:
                self.display_result(result)
    
    def display_result(self, result):
        self.result_text.delete(1.0, tk.END)
        
        accepted, path, message = result
        
        self.result_text.insert(tk.END, f"Evaluando la cadena: '{self.string_entry.get()}'\n\n")
        
        if path:
            for i, (state, symbol) in enumerate(path):
                if i == 0:
                    self.result_text.insert(tk.END, f"Estado inicial: {state}\n")
                else:
                    prev_state = path[i-1][0]
                    self.result_text.insert(tk.END, f"{i}. Desde el estado ({prev_state}) con el símbolo '{symbol}' se transita al estado ({state})\n")
        
        self.result_text.insert(tk.END, f"\n{message}\n")
        
        # Actualizar etiqueta de resultado
        if accepted:
            self.result_label.config(text="✓ CADENA ACEPTADA", foreground='green')
        else:
            self.result_label.config(text="✗ CADENA RECHAZADA", foreground='red')