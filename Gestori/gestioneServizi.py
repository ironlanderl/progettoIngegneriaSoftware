import json
from Servizi.Servizio import Servizio

class GestioneServizi:
    def __init__(self):
        self._servizi: list[Servizio] = []

    def aggiungi_campo_bocce(self, costo: float, descrizione: str, nome_servizio: str, numero_campi: int, opzioni_pagamento: str):
        raise NotImplementedError

    def aggiungi_sala_biliardino(self, costo: float, descrizione: str, nome_servizio: str, numero_tavoli: int):
        raise NotImplementedError

    def aggiungi_tavolo_biliardino(self, costo: float, descrizione: str, nome_servizio: str, costo_per_partita: float):
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
