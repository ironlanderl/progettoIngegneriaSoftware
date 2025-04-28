import os
import pickle
from datetime import datetime
from Eventi.Torneo import Torneo

class GestioneEventi:
    def __init__(self):
        self._eventi: list[Torneo] = []
        if os.path.exists("eventi.pickle"):
            self.leggi_da_file()

    def aggiungi_evento(self, data: str):
        # Convertire la stringa in un oggetto datetime
        data_datetime = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
        self._eventi.append(Torneo(data_datetime))
        self.salva_su_file()

    def rimuovi_evento(self, data: str):
        evento = self.get_evento(data)
        self._eventi.remove(evento)
        self.salva_su_file()

    def aggiungi_partecipante(self, data: str, nome_squadra: str, nome_utente: str):
        evento = self.get_evento(data)
        self.aggiungi_squadra(evento, nome_squadra)
        evento.aggiungi_utente_a_squadra(nome_squadra, nome_utente)
        self.salva_su_file()

    def rimuovi_partecipante(self, data: str, nome_squadra: str, nome_utente: str):
        evento = self.get_evento(data)
        evento.rimuovi_utente_da_squadra(nome_squadra, nome_utente)
        self.salva_su_file()

    def aggiungi_squadra(self, evento: Torneo, nome_squadra: str):
        if nome_squadra not in evento.squadre:
            evento.aggiungi_squadra(nome_squadra)

    def get_evento(self, data: str) -> Torneo:
        # Convertire la stringa in un oggetto datetime per il confronto
        data_datetime = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
        for evento in self._eventi:
            if evento.data == data_datetime:
                return evento
        raise ValueError("Evento non trovato")

    def salva_su_file(self, nome_file: str = "eventi.pickle"):
        with open(nome_file, 'wb') as f:
            pickle.dump(self._eventi, f)

    def leggi_da_file(self, nome_file: str = "eventi.pickle"):
        with open(nome_file, 'rb') as f:
            self._eventi = pickle.load(f)
