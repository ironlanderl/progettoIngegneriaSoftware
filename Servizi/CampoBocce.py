from typing import override
from Servizi.Servizio import Servizio

class CampoBocce(Servizio):
    def __init__(self, costo: float, descrizione: str, nome_servizio: str):
        super().__init__(costo, descrizione, nome_servizio)
        self._numero_campi: int = -1 # Should be integer
        self._opzioni_pagamento: str = ""

    @override
    def __str__(self) -> str:
        return self.nome_servizio
