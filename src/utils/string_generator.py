"""
Lógica para generar cadenas que pertenecen al lenguaje de un AFD.
Utiliza un enfoque de búsqueda en anchura para encontrar las cadenas
más cortas primero.
"""

from collections import deque

class StringGenerator:
    def generate(self, automaton, limit=10):
        """
        Genera las primeras 'limit' cadenas aceptadas por el autómata.
        
        :param automaton: La instancia del autómata a utilizar.
        :param limit: El número máximo de cadenas a generar.
        :return: Una lista de cadenas aceptadas, ordenadas por longitud.
        """
        if not automaton.is_valid():
            return []

        # Usamos una cola para la búsqueda en anchura
        # Los elementos de la cola son tuplas: (estado_actual, cadena_construida)
        queue = deque([(automaton.initial_state, "")])
        
        # Guardamos las cadenas ya visitadas para evitar ciclos y repeticiones
        visited = set([(automaton.initial_state, "")])
        
        accepted_strings = []

        while queue and len(accepted_strings) < limit:
            current_state, current_string = queue.popleft()

            # Si el estado actual es un estado de aceptación y la cadena no ha sido agregada
            if current_state in automaton.final_states:
                # La verificación de unicidad no es tan crítica en BFS para cadenas,
                # pero ayuda a ser robusto.
                if current_string not in accepted_strings:
                    accepted_strings.append(current_string)
                    # Si ya alcanzamos el límite, no continuamos
                    if len(accepted_strings) == limit:
                        break

            # Explorar transiciones para cada símbolo del alfabeto
            for symbol in sorted(list(automaton.alphabet)):
                next_state = automaton.transitions.get((current_state, symbol))
                
                if next_state:
                    next_string = current_string + symbol
                    state_string_pair = (next_state, next_string)
                    
                    if state_string_pair not in visited:
                        visited.add(state_string_pair)
                        queue.append(state_string_pair)
        
        return accepted_strings