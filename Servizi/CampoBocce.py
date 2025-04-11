from typing import override
from Servizi.Servizio import Servizio
import uuid

class CampoBocce(Servizio):
    def __init__(self, costo: float, descrizione: str, nome_servizio: str, numero_campi: int, opzioni_pagamento: str):
        super().__init__(costo, descrizione, nome_servizio)
        self._numero_campi: int = -1 # Should be integer
        self._opzioni_pagamento: str = ""
        self.numero_campi = numero_campi
        self.opzioni_pagamento = opzioni_pagamento


    @property
    def numero_campi(self):
        return self._numero_campi

    @numero_campi.setter
    def numero_campi(self, numero_campi: int):
        if not isinstance(numero_campi, int) or numero_campi <= 0:
            raise ValueError("Il numero_campi deve essere un intero positivo")
        self._numero_campi = numero_campi


    @property
    def opzioni_pagamento(self):
        return self._opzioni_pagamento

    @opzioni_pagamento.setter
    def opzioni_pagamento(self, opzioni_pagamento: str):
        if not isinstance(opzioni_pagamento, str) or opzioni_pagamento.strip() == "" :
            raise ValueError("È necessario inserire delle opzioni di pagamento")
        self._opzioni_pagamento = opzioni_pagamento.strip()

    @override
    def __repr__(self):
        base_repr = super().__repr__()
        return f"{base_repr[:-1]}, campi={self.numero_campi})" # Assumes base ends with ')'
