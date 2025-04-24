from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from Gestori.gestione_utenti import GestioneUtenti
from Utenti.Utente import Utente
from Utenti.Feedback import Feedback

class VisualizzaFeedbackForm(QtWidgets.QDialog):
    def __init__(self, gestore_utenti: GestioneUtenti):
        super().__init__()
        uic.loadUi('./windows/visualizza_feedback.ui', self)
        self.gestore_utenti = gestore_utenti
        # Ora memorizziamo tuple di (utente, feedback) per permettere l'eliminazione e la visualizzazione
        self.all_feedback: list[tuple[Utente, Feedback]] = []

        self.btnEliminaFeedback.clicked.connect(self.elimina_feedback)
        self.populate_feedback()
        self.lstFeedback.itemSelectionChanged.connect(self.visualizza_feedback)

    def populate_feedback(self):
        self.lstFeedback.clear()
        self.all_feedback.clear()
        for utente in self.gestore_utenti._utenti:
            for feedback in utente.feedback:
                self.all_feedback.append((utente, feedback))
                self.lstFeedback.addItem(str(feedback))
        
        if self.lstFeedback.count() > 0:
            self.lstFeedback.setCurrentRow(0)
            self.visualizza_feedback()

    def elimina_feedback(self):
        index = self.lstFeedback.currentRow()
        if index == -1:
            QMessageBox.warning(self, "Elimina Feedback", "Nessun feedback selezionato.")
            return

        utente, feedback = self.all_feedback[index]
        # Usa il metodo rimuovi_feedback definito in Utente.py
        utente.rimuovi_feedback(feedback)
        self.populate_feedback()
        self.gestore_utenti.salva_su_file()

    def visualizza_feedback(self):
        index = self.lstFeedback.currentRow()
        if index == -1:
            QMessageBox.warning(self, "Visualizza Feedback", "Nessun feedback selezionato.")
            return

        utente, feedback = self.all_feedback[index]
        self.lblUsernameFeedback.setText(f"Utente: {utente.username}")
        self.lblDataFeedback.setText(feedback.data.strftime("%d/%m/%Y %H:%M:%S"))
