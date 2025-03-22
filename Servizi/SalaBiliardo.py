from Servizi.Servizio import Servizio


class SalaBiliardo(Servizio):
    def __init__(self):
        super().__init__()
        self.numero_tavoli: int = -1