import datetime


class Tornei:
    def __init__(self, data: str, numero_partecipanti: int, tipo: str):
        self.data: datetime.datetime = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
        self.numero_partecipanti: int = 0
        self.tipo: str = ""
