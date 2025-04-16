import pickle
import os
from Utenti.Utente import Utente

class GestioneUtenti:
    def __init__(self):
        self._utenti: list[Utente] = []
        # Caricamento automatico
        if os.path.exists("utenti.pickle"):
            self.leggi_da_file("utenti.pickle")

    def aggiungi_utente(self, nome: str, cognome: str, username: str, password: str) -> Utente:
        utente: Utente = Utente(nome, cognome, username, password)
        self._utenti.append(utente)
        self.salva_su_file("utenti.pickle")
        return utente

    def rimuovi_utente(self, username: str):
        self._utenti.remove(self.get_utente(username))
        self.salva_su_file("utenti.pickle")

    def get_utente(self, username: str) -> Utente:
        for utente in self._utenti:
            if utente.username == username:
                return utente
        raise ValueError("L'utente cercato non esiste")

    def check_credenziali(self, username: str, password: str) -> tuple[bool, Utente | None]:
        for utente in self._utenti:
            if utente.username == username and utente.password == password:
                return True, utente
        return False, None

    def salva_su_file(self, nome_file: str):
        with open(nome_file, "wb") as f:
            pickle.dump(self._utenti, f)

    def leggi_da_file(self, nome_file: str):
        with open(nome_file, "rb") as f:
            self._utenti = pickle.load(f)
