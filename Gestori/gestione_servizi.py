import os
import pickle
from Servizi.Servizio import Servizio
from Servizi.CampoBocce import CampoBocce
from Servizi.SalaBiliardo import SalaBiliardo
from Servizi.TavoloBiliardino import TavoloBiliardino


class GestioneServizi:
    def __init__(self):
        self._servizi: list[Servizio] = []
        self._orario_apertura = {
            "Lunedi": "09:00",
            "Martedi": "09:00",
            "Mercoledi": "09:00",
            "Giovedi": "09:00",
            "Venerdi": "09:00",
            "Sabato": "09:00",
            "Domenica": "09:00"
        }
        self._orario_chiusura = {
            "Lunedi": "23:00",
            "Martedi": "23:00",
            "Mercoledi": "23:00",
            "Giovedi": "23:00",
            "Venerdi": "23:00",
            "Sabato": "23:00",
            "Domenica": "23:00"
        }

        if os.path.exists("servizi.pickle"):
            self.leggi_da_file("servizi.pickle")
        else:
            # Creazione default
            self.aggiungi_campo_bocce(nome_servizio="Campo da bocce 1", costo=10.0, descrizione="Campo da bocce 1")
            self.aggiungi_campo_bocce(nome_servizio="Campo da bocce 2", costo=10.0, descrizione="Campo da bocce 2")
            self.aggiungi_campo_bocce(nome_servizio="Campo da bocce 3", costo=10.0, descrizione="Campo da bocce 3")
            self.aggiungi_campo_bocce(nome_servizio="Campo da bocce 4", costo=10.0, descrizione="Campo da bocce 4")
            self.aggiungi_campo_bocce(nome_servizio="Campo da bocce 5", costo=10.0, descrizione="Campo da bocce 5")
            self.aggiungi_campo_bocce(nome_servizio="Campo da bocce 6", costo=10.0, descrizione="Campo da bocce 6")

            self.aggiungi_tavolo_biliardino(nome_servizio="Tavolo Biliardino 1", costo=10.0, descrizione="Tavolo Biliardino 1")
            self.aggiungi_tavolo_biliardino(nome_servizio="Tavolo Biliardino 2", costo=10.0, descrizione="Tavolo Biliardino 2")

            self.aggiungi_sala_biliardo(nome_servizio="Sala Biliardo 1", costo=10.0, descrizione="Sala Biliardo 1", numero_tavoli=2)
            self.aggiungi_sala_biliardo(nome_servizio="Sala Biliardo 2", costo=10.0, descrizione="Sala Biliardo 2", numero_tavoli=3)

            self.salva_su_file("servizi.pickle")

    def aggiungi_campo_bocce(self, costo: float, descrizione: str, nome_servizio: str):
        self._servizi.append(CampoBocce(costo, descrizione, nome_servizio))

    def aggiungi_sala_biliardo(self, costo: float, descrizione: str, nome_servizio: str, numero_tavoli: int):
        self._servizi.append(SalaBiliardo(costo, descrizione, nome_servizio, numero_tavoli))

    def aggiungi_tavolo_biliardino(self, costo: float, descrizione: str, nome_servizio: str):
        self._servizi.append(TavoloBiliardino(costo, descrizione, nome_servizio))

    def rimuovi_servizio(self, servizio: Servizio):
        self._servizi.remove(servizio)

    def get_servizi(self) -> list[Servizio]:
        return self._servizi

    def _get_servizio_index(self, servizio: Servizio):
        return self._servizi.index(servizio)

    def update_servizio(self, vecchio_servizio: Servizio, nuovo_servizio: Servizio):
        self._servizi[self._get_servizio_index(vecchio_servizio)] = nuovo_servizio

    def get_servizio(self, name: str):
        for servizio in self._servizi:
            if servizio.nome_servizio == name:
                return servizio

    def get_servizi_by_type(self, tipe: type):
        return [servizio for servizio in self._servizi if isinstance(servizio, tipe)]

    def rimuovi_servizio_by_nome(self, name: str):
        self._servizi.remove(self.get_servizio(name))

    def salva_su_file(self, nome_file: str):
        with open(nome_file, "wb") as f:
            pickle.dump(self._servizi, f)

    def leggi_da_file(self, nome_file: str):
        with open(nome_file, "rb") as f:
            self._servizi = pickle.load(f)

    def get_orario_apertura(self, giorno):
        return self._orario_apertura[giorno]

    def set_orario_apertura(self, giorno, orario_apertura):
        self._orario_apertura[giorno] = orario_apertura

    def get_orario_chiusura(self, giorno):
        return self._orario_chiusura[giorno]

    def set_orario_chiusura(self, giorno, orario_chiusura):
        self._orario_chiusura[giorno] = orario_chiusura
