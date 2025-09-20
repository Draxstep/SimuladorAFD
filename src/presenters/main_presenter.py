"""Presenter principal que coordina la aplicación"""

from src.utils.file_handler import FileHandler
from src.utils.string_generator import StringGenerator
from src.utils.validators import validate_automaton_definition

class MainPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.file_handler = FileHandler()
        self.generator = StringGenerator()
    
    def new_automaton(self):
        self.model.__init__()
        self.view.show_message("Nuevo", "Autómata reiniciado")
    
    def build_automaton(self, data):
        try:
            validate_automaton_definition(data)
            
            self.model.__init__()
            
            for state in data['states']:
                self.model.add_state(state)
            
            for symbol in data['alphabet']:
                self.model.add_symbol(symbol)
            
            self.model.set_initial(data['initial'])
            
            for state in data['finals']:
                self.model.add_final_state(state)
            
            for from_state, symbol, to_state in data['transitions']:
                self.model.add_transition(from_state, symbol, to_state)
            
            if not self.model.is_valid():
                raise ValueError("El autómata no está completo")
            
            self.view.show_message("Éxito", "Autómata construido correctamente")
            
        except Exception as e:
            self.view.show_message("Error", str(e), 'error')
    
    def evaluate_string(self, input_string):
        try:
            if not self.model.is_valid():
                self.view.show_message("Error", "Primero debe construir un autómata válido", 'error')
                return None
            
            accepted, path = self.model.evaluate(input_string)
            automaton_data = self.model.to_dict()
            
            if path:
                final_state = path[-1][0]
                if accepted:
                    message = f"Proceso finalizado. El estado final es ({final_state}).\nResultado: La cadena '{input_string}' es ACEPTADA."
                else:
                    # Texto modificado para el caso de rechazo
                    message = f"La cadena finaliza en el estado ({final_state}), que NO es un estado de aceptación.\nResultado: La cadena '{input_string}' es RECHAZADA."
            else:
                message = "No se pudo evaluar la cadena. Verifique que todos los símbolos pertenezcan al alfabeto."
            
            return accepted, path, message, automaton_data
            
        except Exception as e:
            self.view.show_message("Error", str(e), 'error')
            return None
    
    def generate_strings(self):
        try:
            if not self.model.is_valid():
                self.view.show_message("Error", "Primero debe construir un autómata válido", 'error')
                return None
            
            # El software debe generar las primeras 10 cadenas aceptadas por el autómata en orden de longitud, de la más corta a la más larga[cite: 11, 36, 37].
            strings = self.generator.generate(self.model, limit=10)
            return strings
            
        except Exception as e:
            self.view.show_message("Error", str(e), 'error')
            return None
    
    def save_automaton(self, filename):
        try:
            if not self.model.is_valid():
                self.view.show_message("Error", "No hay un autómata válido para guardar", 'error')
                return
            
            data = self.model.to_dict()
            self.file_handler.save(filename, data)
            self.view.show_message("Éxito", f"Autómata guardado en {filename}")
            
        except Exception as e:
            self.view.show_message("Error", f"Error al guardar: {str(e)}", 'error')
    
    def load_automaton(self, filename):
        try:
            data = self.file_handler.load(filename)
            self.model.from_dict(data)
            
            self.view.editor.update_display(data)
            self.view.show_message("Éxito", f"Autómata cargado desde {filename}")
            
        except Exception as e:
            self.view.show_message("Error", f"Error al cargar: {str(e)}", 'error')