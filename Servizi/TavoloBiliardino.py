from Servizi.Servizio import Servizio


class TavoloBiliardino(Servizio):
    def __init__(self, costo: float, descrizione: str, nome_servizio: str, costo_per_partita: float):
        super().__init__(costo, descrizione, nome_servizio)
        self._costo_per_partita: float = -1
        self.costo_per_partita: float = costo_per_partita


    @property
    def costo_per_partita(self):
        return self._costo_per_partita

    @costo_per_partita.setter
    def costo_per_partita(self, costo_per_partita: float):
        if costo_per_partita < 0.0:
            raise ValueError("Il costo_per_partita non può essere negativo")
        self._costo_per_partita = costo_per_partita
