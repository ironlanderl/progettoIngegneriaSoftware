from datetime import datetime


class Torneo:
    def __init__(self, data: datetime):
        self._squadre: dict = {}
        self._data: datetime = datetime.fromtimestamp(0)
        self.data: datetime = data

    @property
    def data(self) -> datetime:
        return self._data

    @data.setter
    def data(self, data: datetime):
        if not isinstance(data, datetime):
            raise TypeError("La data deve essere un oggetto datetime")
        
        if datetime.now() > data:
            raise ValueError("Non è possibile pianificare un torneo nel passato")
        

        self._data = data

    @property
    def squadre(self):
        """The squadre property."""
        return self._squadre

    def aggiungi_squadra(self, nome_squadra: str):
        if nome_squadra in self._squadre:
            raise ValueError("La squadra è già presente nel torneo")
        self._squadre[nome_squadra] = []

    def aggiungi_utente_a_squadra(self, nome_squadra: str, utente: str):
        if nome_squadra not in self._squadre:
            raise ValueError("La squadra non esiste nel torneo")
        if utente in self._squadre[nome_squadra]:
            raise ValueError("L'utente è già presente nella squadra")
        self._squadre[nome_squadra].append(utente)

    def visualizza_squadre(self):
        return self._squadre

    def rimuovi_utente_da_squadra(self, nome_squadra: str, utente: str):
        if nome_squadra not in self._squadre:
            raise ValueError("La squadra non esiste nel torneo")
        if utente not in self._squadre[nome_squadra]:
            raise ValueError("L'utente non è presente nella squadra")
        self._squadre[nome_squadra].remove(utente)

    def rimuovi_squadra(self, nome_squadra: str):
        if nome_squadra not in self._squadre:
            raise ValueError("La squadra non esiste nel torneo")
        del self._squadre[nome_squadra]
