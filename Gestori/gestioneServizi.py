import json
from Servizi.Servizio import Servizio
from Servizi.CampoBocce import CampoBocce
from Servizi.SalaBiliardo import SalaBiliardo
from Servizi.TavoloBiliardino import TavoloBiliardino


class GestioneServizi:
    def __init__(self):
        self._servizi: list[Servizio] = []

    def aggiungi_campo_bocce(self, costo: float, descrizione: str, nome_servizio: str, numero_campi: int, opzioni_pagamento: str):
        self._servizi.append(CampoBocce(costo, descrizione, nome_servizio, numero_campi, opzioni_pagamento))

    def aggiungi_sala_biliardo(self, costo: float, descrizione: str, nome_servizio: str, numero_tavoli: int):
        self._servizi.append(SalaBiliardo(costo, descrizione, nome_servizio, numero_tavoli))

    def aggiungi_tavolo_biliardino(self, costo: float, descrizione: str, nome_servizio: str, costo_per_partita: float):
        self._servizi.append(TavoloBiliardino(costo, descrizione, nome_servizio, costo_per_partita))

    def rimuovi_servizio(self, servizio: Servizio):
        self._servizi.remove(servizio)

    def get_servizi(self) -> list[Servizio]:
        return self._servizi

    def _get_servizio_index(self, servizio: Servizio):
        return self._servizi.index(servizio)

    def update_servizio(self, vecchio_servizio: Servizio, nuovo_servizio: Servizio):
        self._servizi[self._get_servizio_index(vecchio_servizio)] = nuovo_servizio

    def salva_su_file(self, nome_file: str):
        with open(nome_file, "w") as f:
            json.dump(self._servizi, f)

    def leggi_da_file(self, nome_file: str):
        with open(nome_file, "r") as f:
            self._servizi = json.load(f)
