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
        for nome_tavolo in tavoli_disponibili:
            self.lstTavoli.addItem(str(nome_tavolo))

        # Esempio: Connetti un'azione quando si preme "Accetta" per leggere i valori
        self.buttonBox.accepted.connect(self.on_accept)

    def on_accept(self):
        if not self.lstTavoli.currentItem():
            return
        tavolo_selezionato = self.tavoli_disponibili[self.lstTavoli.currentRow()]
        durata = self.tmeDurata.time().toPyTime()
        durata = self.tmeDurata.time().toPyTime()
        durata_delta = datetime.timedelta(hours=durata.hour, minutes=durata.minute, seconds=durata.second, microseconds=durata.microsecond)
        data_prenotazione = self.dteDataPrenotazione.date().toPyDate()
        data_ora_prenotazione = datetime.datetime.combine(data_prenotazione, durata)
        self.gestore_prenotazioni.aggiungi_prenotazione(tavolo_selezionato, data_ora_prenotazione, durata_delta, self.utente.username)
        self.accept()
