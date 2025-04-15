import pickle
from Servizi.Prenotazione import Prenotazione
from Servizi.Servizio import Servizio
from Utenti.Cliente import Cliente
import datetime

class GestioneEventi:
    def __init__(self):
        self._eventi: list[Prenotazione] = []

    def aggiungi_evento(self, servizio: Servizio, data: datetime.datetime, durata: datetime.timedelta, cliente_prenotazione: Cliente):
        prenotazione = Prenotazione(servizio, data, durata, cliente_prenotazione)
        self._eventi.append(prenotazione)

    def get_prenotazione(self, data: datetime.datetime, cliente_prenotazione: Cliente):
        for prenotazione in self._eventi:
            if prenotazione.data == data and prenotazione.cliente_prenotazione == cliente_prenotazione:
                return prenotazione

    def elimina_prenotazione(self, data: datetime.datetime, cliente_prenotazione: Cliente):
        self._eventi.remove(self.get_prenotazione(data, cliente_prenotazione))

    def salva_su_file(self, nome_file: str):
        with open(nome_file, 'wb') as f:
            pickle.dump(self._eventi, f)

    def leggi_da_file(self, nome_file: str):
        with open(nome_file, 'rb') as f:
            self._eventi = pickle.load(f)

