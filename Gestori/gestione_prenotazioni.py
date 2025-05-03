import pickle
from Servizi.Prenotazione import Prenotazione
from Servizi.Servizio import Servizio
from Utenti.Utente import Utente
import datetime
import os
import json

class GestionePrenotazioni:
    def __init__(self):
        self._prenotazioni: list[Prenotazione] = []
        self._orario_apertura = {
            "Monday": "09:00",
            "Tuesday": "09:00",
            "Wednesday": "09:00",
            "Thursday": "09:00",
            "Friday": "09:00",
            "Saturday": "09:00",
            "Sunday": "09:00"
        }
        self._orario_chiusura = {
            "Monday": "23:00",
            "Tuesday": "23:00",
            "Wednesday": "23:00",
            "Thursday": "23:00",
            "Friday": "23:00",
            "Saturday": "23:00",
            "Sunday": "23:00"
        }
        if os.path.exists("prenotazioni.pickle"):
            self.leggi_da_file("prenotazioni.pickle")
        if os.path.exists("orari.json"):
            self.leggi_orari_da_file("orari.json")
        else:
            self.salva_orari_su_file("orari.json")

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
        # Converti da giorno a indice (0=Monday, 6=Sunday)
        giorno_settimana = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][data.weekday()]
        orario_apertura_str = self.get_orario_apertura(giorno_settimana)
        orario_chiusura_str = self.get_orario_chiusura(giorno_settimana)
        orario_apertura = datetime.datetime.strptime(orario_apertura_str, "%H:%M").time()
        orario_chiusura = datetime.datetime.strptime(orario_chiusura_str, "%H:%M").time()
        data_e_ora_apertura = data.replace(hour=orario_apertura.hour, minute=orario_apertura.minute, second=0, microsecond=0)
        data_e_ora_chiusura = data.replace(hour=orario_chiusura.hour, minute=orario_chiusura.minute, second=0, microsecond=0)
        if data < data_e_ora_apertura or (data + durata) > data_e_ora_chiusura:
            return False
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

    def get_orario_apertura(self, giorno):
        return self._orario_apertura[giorno]

    def set_orario_apertura(self, giorno, orario_apertura):
        self._orario_apertura[giorno] = orario_apertura

    def get_orario_chiusura(self, giorno):
        return self._orario_chiusura[giorno]

    def set_orario_chiusura(self, giorno, orario_chiusura):
        self._orario_chiusura[giorno] = orario_chiusura

    def salva_orari_su_file(self, nome_file: str = "orari.json"):
        with open(nome_file, 'w') as f:
            json.dump({"apertura": self._orario_apertura, "chiusura": self._orario_chiusura}, f)
    
    def leggi_orari_da_file(self, nome_file: str = "orari.json"):
        with open(nome_file, 'r') as f:
            data = json.load(f)
            self._orario_apertura = data["apertura"]
            self._orario_chiusura = data["chiusura"]