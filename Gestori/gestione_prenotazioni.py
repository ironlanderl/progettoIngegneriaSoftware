import pickle
from Servizi.Prenotazione import Prenotazione
from Servizi.Servizio import Servizio
from Utenti.Utente import Utente
import datetime
import os

class GestionePrenotazioni:
    def __init__(self):
        self._prenotazioni: list[Prenotazione] = []
        if os.path.exists("prenotazioni.pickle"):
            self.leggi_da_file("prenotazioni.pickle")


    def aggiungi_prenotazione(self, servizio: Servizio, data: datetime.datetime, durata: datetime.timedelta, utente_prenotazione: str):
        prenotazione = Prenotazione(servizio, data, durata, utente_prenotazione)
        self._prenotazioni.append(prenotazione)
        self.salva_su_file("prenotazioni.pickle")
        return prenotazione

    def get_prenotazione(self, data: datetime.datetime, utente_prenotazione: str):
        for prenotazione in self._prenotazioni:
            if prenotazione.data == data and prenotazione.utente_prenotazione == utente_prenotazione:
                return prenotazione

    def elimina_prenotazione(self, data: datetime.datetime, utente_prenotazione: str):
        self._prenotazioni.remove(self.get_prenotazione(data, utente_prenotazione))
        self.salva_su_file("prenotazioni.pickle")

    def salva_su_file(self, nome_file: str):
        with open(nome_file, 'wb') as f:
            pickle.dump(self._prenotazioni, f)

    def leggi_da_file(self, nome_file: str):
        with open(nome_file, 'rb') as f:
            self._prenotazioni = pickle.load(f)

