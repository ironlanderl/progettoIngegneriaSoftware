from typing import override
from Servizi.Servizio import Servizio
import uuid # Import uuid if not already imported in Servizio

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
        if not isinstance(numero_tavoli, int) or numero_tavoli <= 0:
            raise ValueError("Il numero_tavoli deve essere un intero positivo")
        self._numero_tavoli = numero_tavoli

    @override
    def __repr__(self):
        # Extend base representation
        base_repr = super().__repr__()
        return f"{base_repr[:-1]}, tavoli={self.numero_tavoli})"
