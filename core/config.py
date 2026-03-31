import json
import os

class ConfigManager:
    def __init__(self, path="config.json"):
        self.path = path

    def has_servers(self) -> bool:
        """Retorna True se houver pelo menos um servidor configurado."""
        if not os.path.exists(self.path):
            return False
        
        try:
            with open(self.path, "r") as f:
                dados = json.load(f)
                # Verifica se a lista de servers não está vazia
                return len(dados.get("servers", [])) > 0
        except:
            return False

    def get_all_active(self):
        # ... sua lógica atual de retornar a lista ...
        with open(self.path, "r") as f:
            return json.load(f).get("servers", [])
        
        