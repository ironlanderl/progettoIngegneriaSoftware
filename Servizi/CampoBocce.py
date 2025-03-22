from Servizi.Servizio import Servizio


class CampoBocce(Servizio):
    def __init__(self):
        super().__init__()
        self.numero_campi: int = -1

