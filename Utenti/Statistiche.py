import matplotlib.pyplot as plt
import datetime
from Gestori.gestione_prenotazioni import GestionePrenotazioni

class Statistiche:
    def __init__(self):
        self.report: str = ""
        self.tabella_mesi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
        self.tabella_numero_clienti = [0] * 12

    def aggiornaDatiDaPrenotazioni(self, gestore_prenotazioni: GestionePrenotazioni, anno: int = datetime.datetime.now().year):
        """
        Aggiorna la statistica conteggiando il numero di prenotazioni per mese
        basandosi sull'attributo 'data' di ciascuna prenotazione.
        """
        # Resetta i conteggi
        self.tabella_numero_clienti = [0] * 12

        for prenotazione in gestore_prenotazioni._prenotazioni:
            # Assicurati che la prenotazione abbia un attributo data di tipo datetime.datetime
            if isinstance(prenotazione.data, datetime.datetime):
                # Filtra per anno
                if prenotazione.data.year == anno:
                    mese = prenotazione.data.month  # mese in formato 1-12
                    self.tabella_numero_clienti[mese - 1] += 1

    def generaFigura(self):
        """
        Crea e ritorna una figura matplotlib basata sui dati aggiornati.
        """
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.bar(self.tabella_mesi, self.tabella_numero_clienti, color="skyblue")
        ax.set_title("Numero di clienti per mese")
        ax.set_xlabel("Mesi")
        ax.set_ylabel("Numero di clienti")
        plt.tight_layout()
        return fig

    def mostraGrafico(self):
        """
        Crea e mostra un grafico a barre basato sui dati aggiornati.
        """
        fig = self.generaFigura()
        plt.show()
