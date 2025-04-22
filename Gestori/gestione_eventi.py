import pickle
from Eventi.Torneo import Torneo

class GestioneEventi:
    def __init__(self):
        self._eventi: list[Torneo] = []

    def aggiungi_evento(self, data: str):
        self._eventi.append(Torneo(data))

    def rimuovi_evento(self, data: str):
        self._eventi.remove(self.get_evento(data))

    def get_evento(self, data: str) -> Torneo:
        for evento in self._eventi:
            if evento.data.strftime("%Y-%m-%d %H:%M:%S") == data:
                return evento
        raise ValueError("Evento non trovato")

    def salva_su_file(self, nome_file: str):
        with open(nome_file, 'wb') as f:
            pickle.dump(self._eventi, f)

    def leggi_da_file(self, nome_file: str):
        with open(nome_file, 'rb') as f:
            self._eventi = pickle.load(f)
