from PyQt6 import QtWidgets, uic
from Gestori.gestione_prenotazioni import GestionePrenotazioni
from Servizi.SalaBiliardo import SalaBiliardo
from Utenti.Utente import Utente
import datetime

class SalaBiliardoForm(QtWidgets.QDialog):
    def __init__(self, sale: list[SalaBiliardo], gestore_prenotazioni: GestionePrenotazioni, utente: Utente):
        super().__init__()
        uic.loadUi('./windows/sala_biliardo.ui', self)
        
        self.sale = sale
        self.gestore_prenotazioni = gestore_prenotazioni
        self.utente = utente

        # Popola la lista dei servizi disponibili (la QListWidget presente nella UI si chiama "lstTavoliBiliardino")
        for sala in self.sale:
            self.lstTavoliBiliardino.addItem(str(sala))
        
        # Connetti i segnali
        self.buttonBox.accepted.connect(self.aggiungi_prenotazione)
        self.buttonBox.rejected.connect(self.reject)
        self.timeEditDurata.timeChanged.connect(self.calculate_total_cost)
        self.lstTavoliBiliardino.itemSelectionChanged.connect(self.on_item_selection_changed)
    
    def aggiungi_prenotazione(self):
        if not self.lstTavoliBiliardino.currentItem():
            return
        
        sala_selezionata = self.sale[self.lstTavoliBiliardino.currentRow()]
        
        # Calcola la durata come timedelta dalla QTimeEdit (widget "timeEditDurata")
        durata_time = self.timeEditDurata.time().toPyTime()
        durata_delta = datetime.timedelta(
            hours=durata_time.hour, 
            minutes=durata_time.minute, 
            seconds=durata_time.second
        )
        
        # Ottieni la data e ora della prenotazione dal QDateTimeEdit (widget "dateTimeEditData")
        data_ora_prenotazione = self.dateTimeEditData.dateTime().toPyDateTime()

        # Aggiungi la prenotazione tramite il gestore prenotazioni
        try:
            self.gestore_prenotazioni.aggiungi_prenotazione(sala_selezionata, data_ora_prenotazione, durata_delta, self.utente.username)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Errore", str(e))
            return
        self.accept()
    
    def calculate_total_cost(self):
        if not self.lstTavoliBiliardino.currentItem():
            self.lblCostoTotale.setText("Costo Totale: 0€")
            return
        
        sala_selezionata = self.sale[self.lstTavoliBiliardino.currentRow()]
        durata_time = self.timeEditDurata.time().toPyTime()
        durata_delta = datetime.timedelta(
            hours=durata_time.hour, 
            minutes=durata_time.minute, 
            seconds=durata_time.second
        )
        costo_totale = sala_selezionata.calcola_costo(durata_delta)
        self.lblCostoTotale.setText(f"Costo Totale: {costo_totale}€")
    
    def on_item_selection_changed(self):
        selected_items = self.lstTavoliBiliardino.selectedItems()
        if selected_items:
            for item in selected_items:
                print("Selezionato:", item.text())
        else:
            print("Nessun elemento selezionato.")