from Servizi.Servizio import Servizio


class SalaBiliardo(Servizio):
    def __init__(self, costo: float, descrizione: str, nome_servizio: str, numero_tavoli: int):
        super().__init__(costo, descrizione, nome_servizio)
        self._numero_tavoli: int = -1
        self.numero_tavoli: int = numero_tavoli


    @property
    def numero_tavoli(self):
        return self._numero_tavoli

    @numero_tavoli.setter
    def numero_tavoli(self, numero_tavoli: int):
        if numero_tavoli < 0.0:
            raise ValueError("Il numero_tavoli non può essere negativo")
        self._numero_tavoli = numero_tavoli
