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
        if self.controlla_disponibilita(servizio, data, durata):
            prenotazione = Prenotazione(servizio, data, durata, utente_prenotazione)
            self._prenotazioni.append(prenotazione)
            self.salva_su_file("prenotazioni.pickle")
            return prenotazione
        else:
            raise Exception("Servizio non disponibile in questa data e ora")

    def get_prenotazione(self, data: datetime.datetime, utente_prenotazione: str):
        for prenotazione in self._prenotazioni:
            if prenotazione.data == data and prenotazione.utente_prenotazione == utente_prenotazione:
                return prenotazione

    def controlla_disponibilita(self, servizio: Servizio, data: datetime.datetime, durata: datetime.timedelta) -> bool:
        nuova_fine = data + durata
        for prenotazione in self._prenotazioni:
            if prenotazione.servizio == servizio:
                prenotazione_inizio = prenotazione.data
                prenotazione_fine = prenotazione.data + prenotazione.durata
                # Gli intervalli si sovrappongono se l'inizio della nuova prenotazione è precedente alla fine della prenotazione esistente
                # e l'inizio della prenotazione esistente è precedente alla fine della nuova prenotazione
                if data < prenotazione_fine and prenotazione_inizio < nuova_fine:
                    return False
        return True

    def elimina_prenotazione(self, data: datetime.datetime, utente_prenotazione: str):
        self._prenotazioni.remove(self.get_prenotazione(data, utente_prenotazione))
        self.salva_su_file("prenotazioni.pickle")

    def salva_su_file(self, nome_file: str):
        with open(nome_file, 'wb') as f:
            pickle.dump(self._prenotazioni, f)

    def leggi_da_file(self, nome_file: str):
        with open(nome_file, 'rb') as f:
            self._prenotazioni = pickle.load(f)

