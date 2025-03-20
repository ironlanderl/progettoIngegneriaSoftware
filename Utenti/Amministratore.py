from Utenti.Utente import Utente


class Amministratore(Utente):
    def __init__(self):
        super().__init__()
        self.privilegio = True