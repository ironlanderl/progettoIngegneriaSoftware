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
        data_prenotazione = self.dteDataPrenotazione.date().toPyDate()
        ora_prenotazione = self.tmeDurata.time().toPyTime()
        data_ora_prenotazione = datetime.datetime.combine(data_prenotazione, datetime.datetime.min.time())
        data_ora_prenotazione = data_ora_prenotazione.replace(hour=ora_prenotazione.hour, minute=ora_prenotazione.minute)

        # Aggiungi la prenotazione tramite il gestore prenotazioni
        try:
            self.gestore_prenotazioni.aggiungi_prenotazione(tavolo_selezionato, data_ora_prenotazione, durata_delta, self.utente.username)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Errore", str(e))
            return
        
        self.accept()
