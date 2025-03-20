from Utenti.Utente import Utente


class Cliente(Utente):
    def __init__(self):
        super().__init__()
        self.prenotato = True

