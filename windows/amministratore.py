from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QComboBox, QLabel, QListWidget
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Gestori.gestione_utenti import GestioneUtenti
from Utenti.Statistiche import Statistiche
from Gestori.gestione_prenotazioni import GestionePrenotazioni

from windows.visualizza_feedback import VisualizzaFeedbackForm

class AmministratoreForm(QtWidgets.QDialog):
    def __init__(self, gestore_utenti: GestioneUtenti, gestore_prenotazioni: GestionePrenotazioni):
        super().__init__()
        uic.loadUi('./windows/amministratore.ui', self)

        self.gestore_utenti = gestore_utenti
        self.gestore_prenotazioni = gestore_prenotazioni
        self.replace_label_with_graph()

        self.populate_accounts()

        self.btnAggiungiAmministratore.clicked.connect(self.aggiungi_amministratore)
        self.btnEliminaAmministratore.clicked.connect(self.rimuovi_amministratore)

        self.btnVisualizzaFeedback.clicked.connect(self.visualizza_feedback)

        self.visualizzaFeedbackForm = None

    def replace_label_with_graph(self):
        # Trova la label nel layout
        if self.lblGraficoStatistiche:
            parent = self.lblGraficoStatistiche.parentWidget()
            layout = parent.layout()
            
            # Rimuove la label dal layout
            index = layout.indexOf(self.lblGraficoStatistiche)
            layout.removeWidget(self.lblGraficoStatistiche)
            self.lblGraficoStatistiche.text = ""
            self.lblGraficoStatistiche.deleteLater()
            
            stats = Statistiche()
            stats.aggiornaDatiDaPrenotazioni(self.gestore_prenotazioni)
            fig = stats.generaFigura()
            
            canvas = FigureCanvas(fig)
            # Inserisce il canvas nel layout nello stesso posto della label
            layout.insertWidget(index, canvas)

    def populate_accounts(self):
        self.cmbUtentiNonAdmin.clear()
        for utente in self.gestore_utenti._utenti:
            if not utente.amministratore:
                self.cmbUtentiNonAdmin.addItem(utente.username)

        self.lstAmministratori.clear()
        for utente in self.gestore_utenti._utenti:
            if utente.amministratore:
                self.lstAmministratori.addItem(utente.username)

    def aggiungi_amministratore(self):
        username = self.cmbUtentiNonAdmin.currentText()
        if username:
            utente = self.gestore_utenti.get_utente(username)
            utente.amministratore = True
            self.gestore_utenti.salva_su_file()
            self.populate_accounts()
            QtWidgets.QMessageBox.information(self, "Aggiungi Admin", f"L'utente {username} è stato promosso ad amministratore.")
        else:
            QtWidgets.QMessageBox.warning(self, "Aggiungi Admin", "Seleziona un utente da promuovere.")

    def rimuovi_amministratore(self):
        selected_items = self.lstAmministratori.selectedItems()
        if selected_items:
            username = selected_items[0].text()
            utente = self.gestore_utenti.get_utente(username)
            if utente.username == "admin":
                 QtWidgets.QMessageBox.warning(self, "Rimuovi Admin", "Non puoi rimuovere l'amministratore di default.")
                 return
            utente.amministratore = False
            self.gestore_utenti.salva_su_file()
            self.populate_accounts()
            QtWidgets.QMessageBox.information(self, "Rimuovi Admin", f"L'utente {username} è stato rimosso dagli amministratori.")
        else:
            QtWidgets.QMessageBox.warning(self, "Rimuovi Admin", "Seleziona un utente da rimuovere dagli amministratori.")

    def visualizza_feedback(self):
        if self.visualizzaFeedbackForm is None:
            self.visualizzaFeedbackForm = VisualizzaFeedbackForm(self.gestore_utenti)
            self.visualizzaFeedbackForm.exec()
            self.visualizzaFeedbackForm = None
