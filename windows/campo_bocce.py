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
        data_e_ora_prenotazione = self.dteDataOraPrenotazione.dateTime().toPyDateTime()
        try:
            self.gestore_prenotazioni.aggiungi_prenotazione(campo_selezionato, data_e_ora_prenotazione ,durata_delta, self.utente.username)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Errore", str(e))
            return
        self.accept()


    def on_item_selection_changed(self):
        selected_items = self.lstCampi.selectedItems()
        if selected_items:
            print("Elementi selezionati:")
            for item in selected_items:
                print(item.text())
                self.calculate_total_cost()
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
