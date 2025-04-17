from typing import override
from Servizi.Servizio import Servizio
import uuid

class TavoloBiliardino(Servizio):
    def __init__(self, costo: float, descrizione: str, nome_servizio: str):
        super().__init__(costo, descrizione, nome_servizio)


    @override
    def __str__(self):
        return self.nome_servizio
