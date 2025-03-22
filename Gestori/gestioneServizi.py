import json
from Servizi.Servizio import Servizio

class GestioneServizi:
    def __init__(self):
        self._servizi: list[Servizio] = []

    def aggiungi_servizio(self):
        raise NotImplementedError

    def rimuovi_servizio(self):
        raise NotImplementedError

    def get_servizio(self) -> Servizio:
        raise NotImplementedError

    def salva_su_file(self, nome_file: str):
        with open(nome_file, "w") as f:
            json.dump(self._servizi, f)

    def leggi_da_file(self, nome_file: str):
        with open(nome_file, "r") as f:
            self._servizi = json.load(f)