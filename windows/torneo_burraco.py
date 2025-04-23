from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDateTime

from Eventi.Torneo import Torneo
from Gestori.gestione_eventi import GestioneEventi
from Utenti.Utente import Utente
from Gestori.gestione_utenti import GestioneUtenti

from windows.gestione_membri_squadra import GestioneMembriSquadraForm


class TorneoBurracoForm(QtWidgets.QDialog):
    def __init__(self, gestore_eventi: GestioneEventi, gestore_utenti: GestioneUtenti):
        super().__init__()
        uic.loadUi('./windows/torneo_burraco.ui', self)

        self.gestore_eventi = gestore_eventi
        self.gestore_utenti = gestore_utenti
        self.torneo = None
        self.gestione_membri_form = None

        self.btnNuovaSquadra.clicked.connect(self.aggiungi_squadra)
        self.btnEliminaSquadra.clicked.connect(self.elimina_squadra)
        self.btnApri.clicked.connect(self.aggiungi_membri)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.dateTimeEditTorneo.dateTimeChanged.connect(self.aggiorna_lista_squadre)
        self.aggiorna_lista_squadre()

    def aggiungi_squadra(self):
        nome_squadra = self.txtInputSquadra.text()
        if nome_squadra:
            try:
                data_torneo = self.dateTimeEditTorneo.dateTime().toString("yyyy-MM-dd HH:mm:ss")
                if not self.torneo:
                    self.gestore_eventi.aggiungi_evento(data_torneo)
                    self.torneo = self.gestore_eventi.get_evento(data_torneo)
                    print("Torneo creato con successo.")
                self.gestore_eventi.aggiungi_squadra(self.torneo, nome_squadra)
                self.aggiorna_lista_squadre()
            except ValueError as e:
                QtWidgets.QMessageBox.warning(self, "Errore", str(e))

    def elimina_squadra(self):
        selected_item = self.lstSquadre.currentItem()
        if selected_item:
            nome_squadra = selected_item.text()
            try:
                data_torneo = self.dateTimeEditTorneo.dateTime().toString("yyyy-MM-dd HH:mm:ss")
                evento = self.gestore_eventi.get_evento(data_torneo)

                for utente in list(evento.squadre[nome_squadra]):
                    self.gestore_eventi.rimuovi_partecipante(data_torneo, nome_squadra, utente)

                evento.rimuovi_squadra(nome_squadra)
                self.aggiorna_lista_squadre()
            except ValueError as e:
                QtWidgets.QMessageBox.warning(self, "Errore", str(e))
        else:
            QtWidgets.QMessageBox.warning(self, "Errore", "Seleziona una squadra da eliminare.")

    def aggiorna_lista_squadre(self):
        data_torneo = self.dateTimeEditTorneo.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        try:
            self.lstSquadre.clear()
            self.torneo = self.gestore_eventi.get_evento(data_torneo)
            if self.torneo:
                squadre = self.torneo.visualizza_squadre()
                for squadra in squadre:
                    self.lstSquadre.addItem(squadra)
        except ValueError:
            print("Nessun torneo trovato per la data e l'ora selezionate.")
            self.torneo = None

    def aggiungi_membri(self):
        selected_item = self.lstSquadre.currentItem()
        if selected_item:
            nome_squadra = selected_item.text()
            if not self.gestione_membri_form:
                self.gestione_membri_form = GestioneMembriSquadraForm(self.torneo, nome_squadra)
            self.gestione_membri_form.exec()
            self.gestore_eventi.salva_su_file()
        else:
            QtWidgets.QMessageBox.warning(self, "Errore", "Seleziona una squadra per gestire i membri.")