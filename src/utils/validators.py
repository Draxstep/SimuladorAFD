"""
Módulo de utilidades para validaciones de entrada
"""

def is_valid_state_name(name):
    """Verifica si un nombre de estado es válido (no vacío y sin espacios)."""
    return name and isinstance(name, str) and ' ' not in name

def is_valid_symbol(symbol):
    """Verifica si un símbolo es válido (un solo carácter no vacío)."""
    return symbol and isinstance(symbol, str) and len(symbol) == 1

def validate_automaton_definition(data):
    """
    Valida la estructura y los datos de la definición de un autómata.
    
    :param data: Diccionario con la definición del autómata.
    :raises ValueError: Si la definición es inválida.
    """
    states = set(data.get('states', []))
    alphabet = set(data.get('alphabet', []))
    initial = data.get('initial')
    finals = set(data.get('finals', []))
    transitions = data.get('transitions', [])

    if not states:
        raise ValueError("El conjunto de estados no puede estar vacío.")
    
    if not all(is_valid_state_name(s) for s in states):
        raise ValueError("Los nombres de los estados deben ser válidos.")
    
    if not alphabet:
        raise ValueError("El alfabeto no puede estar vacío.")
    
    if not all(is_valid_symbol(s) for s in alphabet):
        raise ValueError("Los símbolos del alfabeto deben ser válidos.")
    
    if not initial:
        raise ValueError("Se debe definir un estado inicial.")
    
    if initial not in states:
        raise ValueError(f"El estado inicial '{initial}' no está en el conjunto de estados.")
        
    for final_state in finals:
        if final_state not in states:
            raise ValueError(f"El estado final '{final_state}' no está en el conjunto de estados.")

    for from_state, symbol, to_state in transitions:
        if from_state not in states:
            raise ValueError(f"Estado de origen '{from_state}' de una transición no existe.")
        if symbol not in alphabet:
            raise ValueError(f"Símbolo '{symbol}' de una transición no existe en el alfabeto.")
        if to_state not in states:
            raise ValueError(f"Estado de destino '{to_state}' de una transición no existe.")