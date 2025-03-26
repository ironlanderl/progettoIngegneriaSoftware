from Utenti.Utente import Utente


class Cliente(Utente):
    def __init__(self, nome: str, cognome: str, username: str, password: str, prenotato: bool):
        super().__init__(nome, cognome, username, password)
        self._prenotato: bool = False
        self.prenotato: bool = prenotato

    @property
    def prenotato(self):
        """The prenotato property."""
        return self._prenotato

    @prenotato.setter
    def prenotato(self, value):
        self._prenotato = value
