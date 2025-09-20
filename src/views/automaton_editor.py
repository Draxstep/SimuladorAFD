"""Panel para crear y editar el autómata"""

import tkinter as tk
from tkinter import ttk, messagebox

class AutomatonEditor:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.presenter = None
        self._create_widgets()
    
    def set_presenter(self, presenter):
        self.presenter = presenter
    
    def _create_widgets(self):
        # Estados
        ttk.Label(self.frame, text="Estados (separados por coma):").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.states_entry = ttk.Entry(self.frame, width=50)
        self.states_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Alfabeto
        ttk.Label(self.frame, text="Alfabeto (separados por coma):").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.alphabet_entry = ttk.Entry(self.frame, width=50)
        self.alphabet_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Estado inicial
        ttk.Label(self.frame, text="Estado Inicial:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.initial_entry = ttk.Entry(self.frame, width=50)
        self.initial_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Estados finales
        ttk.Label(self.frame, text="Estados Finales (separados por coma):").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.finals_entry = ttk.Entry(self.frame, width=50)
        self.finals_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Frame para transiciones
        trans_frame = ttk.LabelFrame(self.frame, text="Transiciones")
        trans_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky='ew')
        
        # Entrada de transiciones
        ttk.Label(trans_frame, text="Estado Actual:").grid(row=0, column=0, padx=5, pady=5)
        self.from_state = ttk.Entry(trans_frame, width=15)
        self.from_state.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(trans_frame, text="Símbolo:").grid(row=0, column=2, padx=5, pady=5)
        self.symbol = ttk.Entry(trans_frame, width=10)
        self.symbol.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(trans_frame, text="Estado Siguiente:").grid(row=0, column=4, padx=5, pady=5)
        self.to_state = ttk.Entry(trans_frame, width=15)
        self.to_state.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Button(trans_frame, text="Agregar", command=self._add_transition).grid(row=0, column=6, padx=5, pady=5)
        
        # Lista de transiciones
        self.trans_listbox = tk.Listbox(trans_frame, height=10, width=60)
        self.trans_listbox.grid(row=1, column=0, columnspan=7, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(trans_frame, orient='vertical', command=self.trans_listbox.yview)
        scrollbar.grid(row=1, column=7, sticky='ns', pady=5)
        self.trans_listbox.config(yscrollcommand=scrollbar.set)
        
        ttk.Button(trans_frame, text="Eliminar Seleccionada", command=self._remove_transition).grid(row=2, column=0, columnspan=7, pady=5)
        
        # Botón de construir
        ttk.Button(self.frame, text="Construir Autómata", command=self._build_automaton, style='Accent.TButton').grid(row=5, column=0, columnspan=2, pady=20)
    
    def _add_transition(self):
        from_s = self.from_state.get().strip()
        sym = self.symbol.get().strip()
        to_s = self.to_state.get().strip()
        
        if from_s and sym and to_s:
            self.trans_listbox.insert(tk.END, f"δ({from_s}, {sym}) = {to_s}")
            self.from_state.delete(0, tk.END)
            self.symbol.delete(0, tk.END)
            self.to_state.delete(0, tk.END)
    
    def _remove_transition(self):
        selection = self.trans_listbox.curselection()
        if selection:
            self.trans_listbox.delete(selection[0])
    
    def _build_automaton(self):
        if not self.presenter:
            return
        
        data = {
            'states': [s.strip() for s in self.states_entry.get().split(',') if s.strip()],
            'alphabet': [s.strip() for s in self.alphabet_entry.get().split(',') if s.strip()],
            'initial': self.initial_entry.get().strip(),
            'finals': [s.strip() for s in self.finals_entry.get().split(',') if s.strip()],
            'transitions': []
        }
        
        for i in range(self.trans_listbox.size()):
            trans = self.trans_listbox.get(i)
            # Parse: δ(q0, a) = q1
            parts = trans.replace('δ(', '').replace(')', '').replace(' ', '').split('=')
            if len(parts) == 2:
                from_sym = parts[0].split(',')
                if len(from_sym) == 2:
                    data['transitions'].append((from_sym[0], from_sym[1], parts[1]))
        
        self.presenter.build_automaton(data)
    
    def update_display(self, automaton_data):
        self.states_entry.delete(0, tk.END)
        self.states_entry.insert(0, ','.join(automaton_data.get('states', [])))
        
        self.alphabet_entry.delete(0, tk.END)
        self.alphabet_entry.insert(0, ','.join(automaton_data.get('alphabet', [])))
        
        self.initial_entry.delete(0, tk.END)
        self.initial_entry.insert(0, automaton_data.get('initial_state', ''))
        
        self.finals_entry.delete(0, tk.END)
        self.finals_entry.insert(0, ','.join(automaton_data.get('final_states', [])))
        
        self.trans_listbox.delete(0, tk.END)
        for key, value in automaton_data.get('transitions', {}).items():
            state, symbol = key.split(',')
            self.trans_listbox.insert(tk.END, f"δ({state}, {symbol}) = {value}")