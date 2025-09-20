"""Manejador de archivos para guardar y cargar autómatas"""

import json

class FileHandler:
    def save(self, filename, data):
        """Guarda el autómata en formato JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load(self, filename):
        """Carga un autómata desde un archivo JSON"""
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)