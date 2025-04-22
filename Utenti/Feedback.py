from datetime import datetime

class Feedback:
    def __init__(self, contenuto: str, data: str):
        self._contenuto: str = ""
        self._data: datetime = None
        self.contenuto: str = contenuto
        self.data: str = data

    @property
    def contenuto(self):
        return self._contenuto

    @contenuto.setter
    def contenuto(self, value: str):
        if value == "":
            raise ValueError("Il contenuto del feedback non può essere vuoto")
        self._contenuto = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value: str):
        try:
            parsed_date: datetime = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError("La data è in un formato errato")
        self._data = parsed_date

    def __str__(self):
        return f"Feedback(contenuto='{self.contenuto}', data='{self.data.strftime('%Y-%m-%d %H:%M:%S')}')"
