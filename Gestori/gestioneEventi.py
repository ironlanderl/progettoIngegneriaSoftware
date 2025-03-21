import json
from Eventi.Tornei import Tornei

class GestioneEventi:
    def __init__(self):
        self._eventi: list[Tornei] = []

    def aggiungi_evento(self):
        raise NotImplementedError

    def rimuovi_evento(self):
        raise NotImplementedError

    def visualizza_eventi(self):
        raise NotImplementedError

    def salva_su_file(self, nome_file: str):
        with open(nome_file, 'w') as f:
            json.dump(self._eventi, f)

    def leggi_da_file(self, nome_file: str):
        with open(nome_file, 'r') as f:
            self._eventi = json.load(f)