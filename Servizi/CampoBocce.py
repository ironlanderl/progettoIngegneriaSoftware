from Servizi.Servizio import Servizio


class CampoBocce(Servizio):
    def __init__(self, costo: float, descrizione: str, nome_servizio: str, numero_campi: int, opzioni_pagamento: str):
        super().__init__(costo, descrizione, nome_servizio)
        self._numero_campi: float = -1
        self._opzioni_pagamento: str = ""
        self.numero_campi = numero_campi
        self.opzioni_pagamento = opzioni_pagamento


    @property
    def numero_campi(self):
        return self._numero_campi

    @numero_campi.setter
    def numero_campi(self, numero_campi: float):
        if numero_campi < 0.0:
            raise ValueError("Il numero_campi non può essere negativo")
        self._numero_campi = numero_campi


    @property
    def opzioni_pagamento(self):
        return self._opzioni_pagamento

    @opzioni_pagamento.setter
    def opzioni_pagamento(self, opzioni_pagamento: str):
        if opzioni_pagamento == "" :
            raise ValueError("È necessario inserire delle opzioni di pagamento")
        self._opzioni_pagamento = opzioni_pagamento

