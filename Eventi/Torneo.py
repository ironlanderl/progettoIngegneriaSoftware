from datetime import datetime


class Torneo:
    def __init__(self, data: str):
        self._utenti: list = []
        self._data: datetime = datetime.fromtimestamp(0)
        self.data: datetime = data

    @property
    def data(self) -> datetime:
        return self._data

    @data.setter
    def data(self, data: str):
        try:
            tmp: datetime = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
        except:
            raise ValueError("La data è in un formato errato")

        if datetime.now() > tmp:
            raise ValueError("Non è possibile pianificare un torneo nel passato")

        self._data = tmp

    @property
    def utenti(self):
        """The utenti property."""
        return self._utenti

    def aggiungi_utente(self, utente):
        if utente in self._utenti:
            raise ValueError("L'utente è già presente nel torneo")
        self._utenti.append(utente)

    def visualizza_utenti(self):
        return self._utenti

    def rimuovi_utente(self, utente):
        if utente not in self._utenti:
            raise ValueError("L'utente non è presente nel torneo")
        self._utenti.remove(utente)
