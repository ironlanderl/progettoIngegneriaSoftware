import json
from Utenti.Utente import Utente

class GestioneUtenti:
    def __init__(self):
        self._utenti: list[Utente] = []

    def aggiungi_utente(self):
        raise NotImplementedError

    def rimuovi_utente(self):
        raise NotImplementedError

    def get_utente(self) -> Utente:
        raise NotImplementedError

    def salva_su_file(self, nome_file: str):
        with open(nome_file, "w") as f:
            json.dump(self._utenti, f)

    def leggi_da_file(self, nome_file: str):
        with open(nome_file, "r") as f:
            self._utenti = json.load(f)