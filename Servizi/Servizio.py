import uuid

class Servizio:
    def __init__(self, costo: float, descrizione: str, nome_servizio: str):
        # Usa un ID univoco per un riferimento più semplice se necessario in seguito
        self._costo: float = -1.0
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
        if not isinstance(costo, (int, float)) or costo < 0.0:
            raise ValueError("Il costo deve essere un numero non negativo")
        self._costo = float(costo)

    @property
    def descrizione(self):
        return self._descrizione

    @descrizione.setter
    def descrizione(self, descrizione: str):
        if not isinstance(descrizione, str) or descrizione.strip() == "":
            raise ValueError("La descrizione non può essere vuota")
        self._descrizione = descrizione.strip()

    @property
    def nome_servizio(self):
        return self._nome_servizio

    @nome_servizio.setter
    def nome_servizio(self, nome_servizio: str):
        if not isinstance(nome_servizio, str) or nome_servizio.strip() == "":
            raise ValueError("Il nome_servizio non può essere vuoto")
        # Considera un controllo di unicità a livello di gestore se necessario
        self._nome_servizio = nome_servizio.strip()

    @property
    def stato(self):
        return self._stato

    @stato.setter
    def stato(self, value: str):
        # Validazione di base dello stato, si potrebbe usare un Enum
        stati_permissi = ["Disponibile", "Prenotato", "In Manutenzione"]
        if value not in stati_permissi:
            raise ValueError(f"Stato non valido. Stati permessi: {', '.join(stati_permissi)}")
        self._stato = value

    # Rendi gli oggetti confrontabili per ordinamento o ricerca se necessario
    def __eq__(self, other):
        if not isinstance(other, Servizio):
            return NotImplemented
        return self.id == other.id

    # Rappresentazione per debugging/logging
    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, nome='{self.nome_servizio}', costo={self.costo}, stato='{self.stato}')"
