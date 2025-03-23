class Servizio:
    def __init__(self, costo: float, descrizione: str, nome_servizio: str):
        self._costo: float = -1
        self._descrizione: str = ""
        self._nome_servizio: str = ""


        self.costo: float = costo
        self.nome_servizio: str = nome_servizio
        self.descrizione: str = descrizione

    @property
    def costo(self):
        return self._costo

    @costo.setter
    def costo(self, costo: float):
        if costo < 0.0:
            raise ValueError("Il costo non può essere negativo")
        self._costo = costo

    @property
    def descrizione(self):
        return self._descrizione

    @descrizione.setter
    def descrizione(self, descrizione: str):
        if descrizione == "":
            raise ValueError("La descrizione non può essere vuota")
        self._descrizione = descrizione

    @property
    def nome_servizio(self):
        return self._nome_servizio

    @nome_servizio.setter
    def nome_servizio(self, nome_servizio: str):
        if nome_servizio == "":
            raise ValueError("Il nome_servizio non può essere vuoto")
        self._nome_servizio = nome_servizio
