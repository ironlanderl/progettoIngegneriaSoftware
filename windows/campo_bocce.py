from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate

from Servizi.CampoBocce import CampoBocce
from Gestori.gestione_prenotazioni import GestionePrenotazioni
from Utenti.Utente import Utente

import datetime

class CampoBocceForm(QtWidgets.QDialog):
    def __init__(self, campi: list[CampoBocce], gestore_prenotazioni: GestionePrenotazioni, utente: Utente):
        super().__init__()
        uic.loadUi('./windows/campo_bocce.ui', self) # Carica il file .ui

        self.campi = campi
        self.gestore_prenotazioni = gestore_prenotazioni
        self.utente = utente

        for campo in self.campi:
            self.lstCampi.addItem(str(campo))

        self.lstCampi.itemSelectionChanged.connect(self.on_item_selection_changed)

        self.buttonBox.accepted.connect(self.aggiungi_prenotazione)
        self.buttonBox.rejected.connect(self.reject)
        self.tmeDurata.timeChanged.connect(self.calculate_total_cost)

    def aggiungi_prenotazione(self):
        if not self.lstCampi.currentItem():
            return
        campo_selezionato = self.campi[self.lstCampi.currentRow()]
        durata = self.tmeDurata.time().toPyTime()
        durata_delta = datetime.timedelta(hours=durata.hour, minutes=durata.minute, seconds=durata.second, microseconds=durata.microsecond)
        data_prenotazione = self.dteDataPrenotazione.date().toPyDate()
        ora_prenotazione = self.tmeDurata.time().toPyTime()
        data_e_ora_prenotazione = datetime.datetime(data_prenotazione.year, data_prenotazione.month, data_prenotazione.day, ora_prenotazione.hour, ora_prenotazione.minute, ora_prenotazione.second)
        prenotazione = self.gestore_prenotazioni.aggiungi_prenotazione(campo_selezionato, data_e_ora_prenotazione ,durata_delta, self.utente.username)
        self.accept()


    def on_item_selection_changed(self):
        selected_items = self.lstCampi.selectedItems()
        if selected_items:
            print("Elementi selezionati:")
            for item in selected_items:
                print(item.text())
        else:
            print("Nessun elemento selezionato.")

    def calculate_total_cost(self):
        if not self.lstCampi.currentItem():
            return
        campo_selezionato = self.campi[self.lstCampi.currentRow()]
        durata = self.tmeDurata.time().toPyTime()
        durata_delta = datetime.timedelta(hours=durata.hour, minutes=durata.minute, seconds=durata.second, microseconds=durata.microsecond)
        costo_totale = campo_selezionato.calcola_costo(durata_delta)
        self.lblCostoTotale.setText(f"Costo totale: {costo_totale}€")
