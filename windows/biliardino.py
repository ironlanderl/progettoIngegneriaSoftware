from PyQt6 import QtWidgets, uic

from Servizi.TavoloBiliardino import TavoloBiliardino
from Gestori.gestione_prenotazioni import GestionePrenotazioni
from Utenti.Utente import Utente

import datetime

class PrenotazioneBiliardinoForm(QtWidgets.QDialog):
    def __init__(self, tavoli_disponibili: list[TavoloBiliardino], gestore_prenotazioni: GestionePrenotazioni, utente: Utente):
        super().__init__()
        uic.loadUi('./windows/biliardino.ui', self)

        self.tavoli_disponibili = tavoli_disponibili
        self.gestore_prenotazioni = gestore_prenotazioni
        self.utente = utente

        # Popola la lista dei tavoli a runtime
        for tavolo in tavoli_disponibili:
            self.lstTavoli.addItem(str(tavolo))

        # Connetti un'azione quando si preme "Accetta" per leggere i valori
        self.buttonBox.accepted.connect(self.on_accept)

        self.lstTavoli.itemSelectionChanged.connect(self.on_item_selection_changed)
        self.tmeDurata.timeChanged.connect(self.calculate_total_cost)

    def on_accept(self):
        if not self.lstTavoli.currentItem():
            return
        tavolo_selezionato = self.tavoli_disponibili[self.lstTavoli.currentRow()]
        
        # Calcola la durata come timedelta dalla QTimeEdit (widget "tmeDurata")
        durata_time = self.tmeDurata.time().toPyTime()
        durata_delta = datetime.timedelta(
            hours=durata_time.hour, 
            minutes=durata_time.minute, 
            seconds=durata_time.second
        )
        
        # Ottieni la data e ora della prenotazione dal QDateTimeEdit (widget "dateTimeEditData")
        data_e_ora_prenotazione = self.dteDataPrenotazione.dateTime().toPyDateTime()

        # Aggiungi la prenotazione tramite il gestore prenotazioni
        try:
            self.gestore_prenotazioni.aggiungi_prenotazione(tavolo_selezionato, data_e_ora_prenotazione, durata_delta, self.utente.username)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Errore", str(e))
            return
        
        self.accept()

    def on_item_selection_changed(self):
        selected_items = self.lstTavoli.selectedItems()
        if selected_items:
            print("Elementi selezionati:")
            for item in selected_items:
                print(item.text())
                self.calculate_total_cost()
        else:
            print("Nessun elemento selezionato.")

    def calculate_total_cost(self):
        if not self.lstTavoli.currentItem():
            return
        campo_selezionato = self.tavoli_disponibili[self.lstTavoli.currentRow()]
        durata = self.tmeDurata.time().toPyTime()
        durata_delta = datetime.timedelta(hours=durata.hour, minutes=durata.minute, seconds=durata.second, microseconds=durata.microsecond)
        costo_totale = campo_selezionato.calcola_costo(durata_delta)
        self.lblCostoTotale.setText(f"Costo totale: {costo_totale}€")
