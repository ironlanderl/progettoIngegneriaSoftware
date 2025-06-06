import datetime
from enum import Enum
from Servizi.Servizio import Servizio

class Prenotazione:
    def __init__(self, servizio: Servizio, data: datetime.datetime, durata: datetime.timedelta, utente_prenotazione: str):
        self._servizio: Servizio|None = None
        self._data: datetime.datetime = datetime.datetime(1970, 1, 1, 0, 0)
        self._durata: datetime.timedelta = datetime.timedelta(hours=0, minutes=0)
        self._utente_prenotazione: str|None = None

        # Use setters for validation
        self.id_servizio = servizio
        self.data = data
        self.durata = durata
        self.utente_prenotazione = utente_prenotazione


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
        return self._servizio.costo * (self.durata.total_seconds() / 3600)

    @property
    def utente_prenotazione(self):
        return self._utente_prenotazione

    @utente_prenotazione.setter
    def utente_prenotazione(self, value: str):
        if not isinstance(value, str) or not value:
            raise ValueError("L'utente di prenotazione deve essere una stringa non vuota.")
        self._utente_prenotazione = value
