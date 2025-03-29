import pickle
from Utenti.Utente import Utente

class GestioneUtenti:
    def __init__(self):
        self._utenti: list[Utente] = []

    def aggiungi_utente(self, nome: str, cognome: str, username: str, password: str):
        self._utenti.append(Utente(nome, cognome, username, password))

    def rimuovi_utente(self, username: str):
        self._utenti.remove(self.get_utente(username))

    def get_utente(self, username: str) -> Utente:
        for utente in self._utenti:
            if utente.username == username:
                return utente
        raise ValueError("L'utente cercato non esiste")

    def salva_su_file(self, nome_file: str):
        with open(nome_file, "wb") as f:
            pickle.dump(self._utenti, f)

    def leggi_da_file(self, nome_file: str):
        with open(nome_file, "rb") as f:
            self._utenti = pickle.load(f)
