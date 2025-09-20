"""Panel para generar cadenas del lenguaje"""

import tkinter as tk
from tkinter import ttk

class GenerationPanel:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.presenter = None
        self._create_widgets()
    
    def set_presenter(self, presenter):
        self.presenter = presenter
    
    def _create_widgets(self):
        # Título y descripción
        ttk.Label(self.frame, text="Generador de Cadenas del Lenguaje", 
                 font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=10)
        
        ttk.Label(self.frame, text="Genera las 10 cadenas más cortas aceptadas por el autómata").grid(row=1, column=0, pady=5)
        
        # Botón de generar
        ttk.Button(self.frame, text="Generar Cadenas", command=self._generate, 
                  style='Accent.TButton').grid(row=2, column=0, pady=20)
        
        # Lista de cadenas generadas
        ttk.Label(self.frame, text="Cadenas generadas:").grid(row=3, column=0, sticky='w', padx=10, pady=5)
        
        self.strings_listbox = tk.Listbox(self.frame, height=15, width=50)
        self.strings_listbox.grid(row=4, column=0, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.strings_listbox.yview)
        scrollbar.grid(row=4, column=1, sticky='ns', pady=5)
        self.strings_listbox.config(yscrollcommand=scrollbar.set)
        
        # Información adicional
        self.info_label = ttk.Label(self.frame, text="")
        self.info_label.grid(row=5, column=0, pady=10)
    
    def _generate(self):
        if self.presenter:
            strings = self.presenter.generate_strings()
            if strings is not None:
                self.display_strings(strings)
    
    def display_strings(self, strings):
        self.strings_listbox.delete(0, tk.END)
        
        if not strings:
            self.strings_listbox.insert(tk.END, "No se encontraron cadenas aceptadas")
            self.info_label.config(text="El autómata no acepta ninguna cadena o no está definido correctamente")
        else:
            for i, string in enumerate(strings, 1):
                if string == "":
                    display_str = "ε (cadena vacía)"
                else:
                    display_str = string
                self.strings_listbox.insert(tk.END, f"{i}. {display_str} (longitud: {len(string)})")
            
            self.info_label.config(text=f"Se generaron {len(strings)} cadenas")