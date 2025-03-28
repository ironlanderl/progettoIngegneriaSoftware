from datetime import datetime

class Feedback:
    def __init__(self, contenuto: str, data: datetime):
        self._contenuto: str = ""
        self._data: datetime.datetime = datetime.datetime(1970,1,1,0,0)

    @property
    def contenuto(self):
        """The contenuto property."""
        return self._contenuto

    @contenuto.setter
    def contenuto(self, value):
        if value == "":
            raise ValueException("Il contenuto del feedback non può essere vuoto")
        self._contenuto = value

    @property
    def data(self):
        """The data property."""
        return self._data

    @data.setter
    def data(self, value):
        # Primo controllo: la data deve essere nel formato specificato
        try:
            tmp: datetime = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except:
            raise ValueError("La data è in un forato errato")

        self._data = tmp

