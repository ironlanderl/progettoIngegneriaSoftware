from PyQt6 import QtWidgets, uic
from Gestori.gestione_prenotazioni import GestionePrenotazioni
import datetime

class VisualizzazionePrenotazioniForm(QtWidgets.QDialog):
    def __init__(self, gestore_prenotazioni: GestionePrenotazioni):
        super().__init__()
        uic.loadUi('./windows/visualizzazione_prenotazioni.ui', self)
        self.gestore_prenotazioni = gestore_prenotazioni

        # Connetti il bottone di ricerca
        self.btnCercaPrenotazioni.clicked.connect(self.cerca_prenotazioni)

        # Popola inizialmente la lista con tutte le prenotazioni
        self.popola_lista_prenotazioni()

    def popola_lista_prenotazioni(self, prenotazioni=None):
        self.lstPrenotazioni.clear()
        if prenotazioni is None:
            prenotazioni = self.gestore_prenotazioni._prenotazioni
        # Ordina le prenotazioni per data
        prenotazioni_sorted = sorted(prenotazioni, key=lambda p: p.data)
        for prenotazione in prenotazioni_sorted:
            testo = (
                f"{prenotazione.servizio.nome_servizio} - "
                f"{prenotazione.data.strftime('%d/%m/%Y %H:%M')} - "
                f"Durata: {prenotazione.durata} - "
                f"Utente: {prenotazione.utente_prenotazione} - "
                f"Costo Totale: {round(prenotazione.costo_totale, 2)} €"
            )
            self.lstPrenotazioni.addItem(testo)

    def cerca_prenotazioni(self):
        start_date = self.dateTimeEditDataInizio.dateTime().toPyDateTime()
        end_date = self.dateTimeEditDataFine.dateTime().toPyDateTime()
        prenotazioni_filtrate = [
            p for p in self.gestore_prenotazioni._prenotazioni
            if start_date <= p.data <= end_date
        ]
        self.popola_lista_prenotazioni(prenotazioni_filtrate)