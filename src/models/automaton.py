"""Modelo principal del Autómata Finito Determinista"""

class Automaton:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.initial_state = None
        self.final_states = set()
        self.transitions = {}  # {(state, symbol): next_state}
    
    def add_state(self, state):
        self.states.add(state)
    
    def add_symbol(self, symbol):
        self.alphabet.add(symbol)
    
    def set_initial(self, state):
        if state in self.states:
            self.initial_state = state
            return True
        return False
    
    def add_final_state(self, state):
        if state in self.states:
            self.final_states.add(state)
            return True
        return False
    
    def add_transition(self, from_state, symbol, to_state):
        if from_state in self.states and to_state in self.states and symbol in self.alphabet:
            self.transitions[(from_state, symbol)] = to_state
            return True
        return False
    
    def evaluate(self, input_string):
        if not self.is_valid():
            return False, []
        
        current = self.initial_state
        path = [(current, None)]
        
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False, path
            
            key = (current, symbol)
            if key not in self.transitions:
                return False, path
            
            current = self.transitions[key]
            path.append((current, symbol))
        
        return current in self.final_states, path
    
    def is_valid(self):
        return (self.states and self.alphabet and 
                self.initial_state and self.initial_state in self.states)
    
    def to_dict(self):
        return {
            'states': list(self.states),
            'alphabet': list(self.alphabet),
            'initial_state': self.initial_state,
            'final_states': list(self.final_states),
            'transitions': {f"{k[0]},{k[1]}": v for k, v in self.transitions.items()}
        }
    
    def from_dict(self, data):
        self.states = set(data.get('states', []))
        self.alphabet = set(data.get('alphabet', []))
        self.initial_state = data.get('initial_state')
        self.final_states = set(data.get('final_states', []))
        self.transitions = {}
        for key, value in data.get('transitions', {}).items():
            state, symbol = key.split(',')
            self.transitions[(state, symbol)] = value