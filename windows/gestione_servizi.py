from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtWidgets import QInputDialog, QMessageBox
from Gestori.gestione_servizi import GestioneServizi
from Servizi.TavoloBiliardino import TavoloBiliardino
from Servizi.SalaBiliardo import SalaBiliardo
from Servizi.CampoBocce import CampoBocce

class GestioneServiziForm(QtWidgets.QDialog):
    def __init__(self, gestore_servizi: GestioneServizi):
        super().__init__()
        uic.loadUi('./windows/gestione_servizi.ui', self)
        self.gestore_servizi = gestore_servizi
        self.setup_connections()
        self.populate_lists()

    def setup_connections(self):
        self.btnModificaPrezzoBiliardino.clicked.connect(self.modifica_prezzo_biliardino)
        self.btnModificaPrezzoBiliardo.clicked.connect(self.modifica_prezzo_biliardo)
        self.btnModificaPrezzoBocce.clicked.connect(self.modifica_prezzo_bocce)
        self.btnAggiungiTavoloBiliardo.clicked.connect(self.aggiungi_tavolo_biliardo)
        self.btnEliminaTavoloBiliardo.clicked.connect(self.elimina_tavolo_biliardo)
        self.btnAggiungiTavoloBiliardino.clicked.connect(self.aggiungi_tavolo_biliardino)
        self.btnEliminaTavoloBiliardino.clicked.connect(self.elimina_tavolo_biliardino)
        self.btnAggiungiCampoBocce.clicked.connect(self.aggiungi_campo_bocce)
        self.btnEliminaCampoBocce.clicked.connect(self.elimina_campo_bocce)

    def populate_lists(self):
        self.lstTavoliBiliardo.clear()
        for servizio in self.gestore_servizi.get_servizi_by_type(SalaBiliardo):
            self.lstTavoliBiliardo.addItem(servizio.nome_servizio)
        self.lstTavoliBiliardino.clear()
        for servizio in self.gestore_servizi.get_servizi_by_type(TavoloBiliardino):
            self.lstTavoliBiliardino.addItem(servizio.nome_servizio)
        self.lstCampiBocce.clear()
        for servizio in self.gestore_servizi.get_servizi_by_type(CampoBocce):
            self.lstCampiBocce.addItem(servizio.nome_servizio)

    def modifica_prezzo_biliardino(self):
        new_price = self.dsbPrezzoBiliardino.value()
        for servizio in self.gestore_servizi.get_servizi_by_type(TavoloBiliardino):
            servizio.costo = new_price
        self.gestore_servizi.salva_su_file("servizi.pickle")
        QMessageBox.information(self, "Successo", "Prezzo dei Tavoli Biliardino aggiornato.")

    def modifica_prezzo_biliardo(self):
        new_price = self.dsbPrezzoBiliardo.value()
        for servizio in self.gestore_servizi.get_servizi_by_type(SalaBiliardo):
            servizio.costo = new_price
        self.gestore_servizi.salva_su_file("servizi.pickle")
        QMessageBox.information(self, "Successo", "Prezzo delle Sale Biliardo aggiornato.")

    def modifica_prezzo_bocce(self):
        new_price = self.dsbPrezzoBocce.value()
        for servizio in self.gestore_servizi.get_servizi_by_type(CampoBocce):
            servizio.costo = new_price
        self.gestore_servizi.salva_su_file("servizi.pickle")
        QMessageBox.information(self, "Successo", "Prezzo dei Campi Bocce aggiornato.")

    def aggiungi_tavolo_biliardo(self):
        nome, ok = QInputDialog.getText(self, "Aggiungi Sala Biliardo", "Nome sala:")
        if ok and nome:
            costo, ok = QInputDialog.getDouble(self, "Aggiungi Sala Biliardo", "Costo:", value=10.0, decimals=2)
            if ok:
                descrizione, ok = QInputDialog.getText(self, "Aggiungi Sala Biliardo", "Descrizione:")
                if ok and descrizione:
                    numero, ok = QInputDialog.getInt(self, "Aggiungi Sala Biliardo", "Numero tavoli:", value=2, min=1)
                    if ok:
                        self.gestore_servizi.aggiungi_sala_biliardo(costo, descrizione, nome, numero)
                        self.gestore_servizi.salva_su_file("servizi.pickle")
                        self.populate_lists()

    def elimina_tavolo_biliardo(self):
        current_item = self.lstTavoliBiliardo.currentItem()
        if current_item:
            nome = current_item.text()
            self.gestore_servizi.rimuovi_servizio_by_nome(nome)
            self.gestore_servizi.salva_su_file("servizi.pickle")
            self.populate_lists()
        else:
            QMessageBox.warning(self, "Errore", "Seleziona una sala biliardo da eliminare.")

    def aggiungi_tavolo_biliardino(self):
        nome, ok = QInputDialog.getText(self, "Aggiungi Tavolo Biliardino", "Nome tavolo:")
        if ok and nome:
            costo, ok = QInputDialog.getDouble(self, "Aggiungi Tavolo Biliardino", "Costo:", value=10.0, decimals=2)
            if ok:
                descrizione, ok = QInputDialog.getText(self, "Aggiungi Tavolo Biliardino", "Descrizione:")
                if ok and descrizione:
                    self.gestore_servizi.aggiungi_tavolo_biliardino(costo, descrizione, nome)
                    self.gestore_servizi.salva_su_file("servizi.pickle")
                    self.populate_lists()

    def elimina_tavolo_biliardino(self):
        current_item = self.lstTavoliBiliardino.currentItem()
        if current_item:
            nome = current_item.text()
            self.gestore_servizi.rimuovi_servizio_by_nome(nome)
            self.gestore_servizi.salva_su_file("servizi.pickle")
            self.populate_lists()
        else:
            QMessageBox.warning(self, "Errore", "Seleziona un tavolo biliardino da eliminare.")

    def aggiungi_campo_bocce(self):
        nome, ok = QInputDialog.getText(self, "Aggiungi Campo Bocce", "Nome campo:")
        if ok and nome:
            costo, ok = QInputDialog.getDouble(self, "Aggiungi Campo Bocce", "Costo:", value=10.0, decimals=2)
            if ok:
                descrizione, ok = QInputDialog.getText(self, "Aggiungi Campo Bocce", "Descrizione:")
                if ok and descrizione:
                    self.gestore_servizi.aggiungi_campo_bocce(costo, descrizione, nome)
                    self.gestore_servizi.salva_su_file("servizi.pickle")
                    self.populate_lists()

    def elimina_campo_bocce(self):
        current_item = self.lstCampiBocce.currentItem()
        if current_item:
            nome = current_item.text()
            self.gestore_servizi.rimuovi_servizio_by_nome(nome)
            self.gestore_servizi.salva_su_file("servizi.pickle")
            self.populate_lists()
        else:
            QMessageBox.warning(self, "Errore", "Seleziona un campo bocce da eliminare.")