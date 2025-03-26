from Utenti.Utente import Utente


class Amministratore(Utente):

    def __init__(self, nome: str, cognome: str, username: str, password: str, privilegio: bool):
        super().__init__(nome, cognome, username, password)
        # TODO: Considerare un enum con diversi livelli di privilegi. Altrimenti muovere il privilegio all'interno di Utente
        self._privilegio: bool = False
        self.privilegio: bool = privilegio

    @property
    def privilegio(self):
        """The privilegio property."""
        return self._privilegio

    @privilegio.setter
    def privilegio(self, value):
        self._privilegio = value
