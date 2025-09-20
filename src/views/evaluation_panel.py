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
        # ... (código existente para la entrada y el área de texto) ...
        ttk.Label(self.frame, text="Cadena a evaluar:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.string_entry = ttk.Entry(self.frame, width=40)
        self.string_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Button(self.frame, text="Evaluar", command=self._evaluate).grid(row=0, column=2, padx=10, pady=10)
        
        ttk.Label(self.frame, text="Proceso paso a paso:").grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky='w')
        
        self.result_text = tk.Text(self.frame, height=10, width=70, wrap=tk.WORD)
        self.result_text.grid(row=2, column=0, columnspan=3, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.result_text.yview)
        scrollbar.grid(row=2, column=3, sticky='ns', pady=5)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        self.result_label = ttk.Label(self.frame, text="", font=('Arial', 12, 'bold'))
        self.result_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        
        # Nueva sección de visualización
        ttk.Label(self.frame, text="Visualización del Proceso:").grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky='w')
        self.canvas = tk.Canvas(self.frame, width=600, height=100, bg='white', borderwidth=2, relief="solid")
        self.canvas.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    def _evaluate(self):
        if self.presenter:
            input_string = self.string_entry.get()
            result = self.presenter.evaluate_string(input_string)
            if result:
                self.display_result(result)
    
    def display_result(self, result):
        self.result_text.delete(1.0, tk.END)
        self.canvas.delete("all")  # Limpiar el canvas antes de dibujar
        
        accepted, path, message, automaton_data = result
        
        self.result_text.insert(tk.END, f"Evaluando la cadena: '{self.string_entry.get()}'\n\n")
        
        # Mostrar el camino en el cuadro de texto
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

        # --- DIBUJAR LA VISUALIZACIÓN EN EL CANVAS ---
        self._draw_path_visual(path, automaton_data)

    def _draw_path_visual(self, path, automaton_data):
        if not path:
            return

        x_start = 50
        y_center = 50
        step_x = 100

        # Dibujar cada estado en el camino
        for i, (state, symbol) in enumerate(path):
            x, y = x_start + i * step_x, y_center
            
            # Determinar si el estado es final
            is_final = state in automaton_data.get('final_states', [])
            
            # Dibujar el estado
            self._draw_state(x, y, state, is_final)
            
            # Dibujar el inicio (flecha de entrada) si es el primer estado
            if i == 0:
                # Modificación aquí para mover la flecha y el texto
                start_x = x - 22
                self.canvas.create_text(start_x, y - 5, text="Start", anchor=tk.E, font=('Arial', 8, 'italic'))

            # Dibujar la transición si no es el primer estado
            if i > 0:
                prev_x = x_start + (i - 1) * step_x
                self._draw_transition(prev_x, y, x, y, symbol)

    def _draw_state(self, x, y, state_name, is_final):
        """Dibuja un círculo para representar un estado."""
        # Círculo para el estado
        self.canvas.create_oval(x-20, y-20, x+20, y+20, fill='white', outline='black', width=2)
        
        # Círculo doble si es un estado final
        if is_final:
            self.canvas.create_oval(x-16, y-16, x+16, y+16, outline='black', width=1)
        
        # Nombre del estado
        self.canvas.create_text(x, y, text=state_name, font=('Arial', 10, 'bold'))

    def _draw_transition(self, x1, y1, x2, y2, symbol):
        """Dibuja una flecha entre dos estados con el símbolo."""
        # Flecha entre estados
        self.canvas.create_line(x1+20, y1, x2-20, y2, arrow=tk.LAST, width=1)
        # Símbolo de la transición
        self.canvas.create_text((x1+x2)/2, (y1+y2)/2 - 15, text=symbol, font=('Arial', 8, 'italic'))