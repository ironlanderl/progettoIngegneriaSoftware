from PyQt6 import QtWidgets, uic
from datetime import datetime
from Utenti.Feedback import Feedback
from Utenti.Utente import Utente

class FeedbackForm(QtWidgets.QDialog):
    def __init__(self, utente: Utente):
        super().__init__()
        uic.loadUi('./windows/feedback.ui', self)

        self.utente = utente
        
        self.buttonBox.accepted.connect(self.invia_feedback)
        self.buttonBox.rejected.connect(self.reject)
        
    def invia_feedback(self):
        contenuto = self.txtFeedback.toPlainText().strip()
        if not contenuto:
            QtWidgets.QMessageBox.warning(self, "Errore", "Il feedback non può essere vuoto.")
            return
        
        feedback = Feedback(contenuto, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        self.utente.aggiungi_feedback(feedback)
        self.accept()