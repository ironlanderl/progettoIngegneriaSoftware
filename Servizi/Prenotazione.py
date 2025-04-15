import datetime
from enum import Enum
from Servizi.Servizio import Servizio
from Utenti.Cliente import Cliente

class Prenotazione:
    def __init__(self, servizio: Servizio, data: datetime.datetime, durata: datetime.timedelta, cliente_prenotazione: Cliente):
        self._servizio: Servizio|None = None
        self._data: datetime.datetime = datetime.datetime(1970, 1, 1, 0, 0)
        self._durata: datetime.timedelta = datetime.timedelta(hours=0, minutes=0)
        self._cliente_prenotazione: Cliente|None = None

        # Use setters for validation
        self.id_servizio = servizio
        self.data = data
        self.durata = durata
        self.cliente_prenotazione = cliente_prenotazione


    @property
    def servizio(self):
        return self._servizio

    @servizio.setter
    def id_servizio(self, value: Servizio):
         if not isinstance(value, Servizio) or not value:
             raise ValueError("Il servizio deve essere un'istanza di Servizio.")
         self._servizio = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value: datetime.datetime):
        if not isinstance(value, datetime.datetime):
            raise TypeError("La data deve essere un oggetto datetime.")
        # Optional: Add check if date is in the past? Depends on requirements.
        # if value < datetime.datetime.now():
        #     raise ValueError("Non è possibile prenotare nel passato.")
        self._data = value

    @property
    def data_fine(self) -> datetime.datetime:
        """Calculated end time of the booking."""
        return self.data + self.durata

    @property
    def durata(self):
        return self._durata

    @durata.setter
    def durata(self, value: datetime.timedelta):
        if not isinstance(value, datetime.timedelta) or value <= datetime.timedelta(0):
            raise ValueError("La durata deve essere un timedelta positivo.")
        self._durata = value

    @property
    def costo_totale(self):
        """Calulated total cost"""
        return self._servizio.costo * self.durata

    @property
    def cliente_prenotazione(self):
        return self._cliente_prenotazione

    @cliente_prenotazione.setter
    def cliente_prenotazione(self, value: Cliente):
        if not isinstance(value, Cliente) or not value:
            raise ValueError("Il cliente deve essere un'istanza di Cliente.")
        self._cliente_prenotazione = value
