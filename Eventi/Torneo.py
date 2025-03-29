from datetime import datetime


class Torneo:
    def __init__(self, data: str, numero_partecipanti: int, tipo: str):
        self._numero_partecipanti: int = -1
        self._data: datetime = datetime.fromtimestamp(0)
        self._tipo: str = ""
        self.data: datetime = data
        self.numero_partecipanti: int = numero_partecipanti
        self.tipo: str = tipo

    @property
    def data(self) -> datetime:
        return self._data

    @data.setter
    def data(self, data: str):
        # Primo controllo: la data deve essere nel formato specificato (TODO: Controllare se esiste un widget di QT e quale formato usa)
        try:
            tmp: datetime = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
        except:
            raise ValueError("La data è in un forato errato")

        # Secondo controllo: Il torneo deve essere pianificato dopo di adesso
        if datetime.now() > tmp:
            raise ValueError("Non è possibile pianificare un torneo nel passato")

        self._data = tmp

    @property
    def numero_partecipanti(self):
        """The numero_partecipanti property."""
        return self._numero_partecipanti

    @numero_partecipanti.setter
    def numero_partecipanti(self, value: int):
        if value < 1:
            raise ValueError("Non è possibile avere tornei senza partecipanti")
        self._numero_partecipanti = value

    @property
    def tipo(self):
        """The tipo property."""
        return self._tipo

    @tipo.setter
    def tipo(self, value: str):
        if value == "":
            raise ValueError("Il tipo non può essere vuoto")
        self._tipo = value
