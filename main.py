from typing import override
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QComboBox, QPlainTextEdit, QPushButton
import sys

from Gestori import gestione_servizi
from windows.login import LoginRegistrazioneForm
from windows.campo_bocce import CampoBocceForm

from Utenti.Utente import Utente

from Servizi.CampoBocce import CampoBocce

from Gestori.gestione_utenti import GestioneUtenti
from Gestori.gestione_servizi import GestioneServizi
from Gestori.gestione_prenotazioni import GestionePrenotazioni

class Ui(QtWidgets.QMainWindow):
    def __init__(self, gestore_utenti: GestioneUtenti, gestore_servizi: GestioneServizi, gestore_prenotazioni: GestionePrenotazioni):
        super(Ui, self).__init__()
        uic.loadUi('./windows/main.ui', self)

        self.gestore_utenti = gestore_utenti
        self.gestore_servizi = gestore_servizi
        self.gestore_prenotazioni = gestore_prenotazioni

        self.utente_loggato = None # Inizialmente nessun utente loggato
        self.login_dialog = None # Instance of LoginRegistrazioneForm
        self.campo_bocce_form = None

        self.aggiorna_elementi()

        # Connetti i segnali clicked() dei bottoni (servizi)
        self.btnCampiBoccie.clicked.connect(self.apri_campi_boccie)
        self.btnBiliardino.clicked.connect(self.apri_biliardino)
        self.btnTorneoBurraco.clicked.connect(self.apri_torneo_burraco)
        self.btnSalaBiliardo.clicked.connect(self.apri_sala_biliardo)
        self.btnFeedback.clicked.connect(self.apri_feedback)
        self.btnAmministratore.clicked.connect(self.apri_amministratore)

        # Connetti il bottone Login/Logout
        self.btnLoginLogout.clicked.connect(self.gestisci_login_logout)

    def aggiorna_elementi(self):
        self.btnAmministratore.setEnabled(False)
        if self.utente_loggato:
            self.lblUtenteLoggato.setText(f"Utente loggato: {self.utente_loggato}")
            self.btnLoginLogout.setText("Logout")
            if self.utente_loggato.amministratore:
                self.btnAmministratore.setEnabled(True)
        else:
            self.lblUtenteLoggato.setText("Utente non loggato")
            self.btnLoginLogout.setText("Login")


    def gestisci_login_logout(self):
        if self.utente_loggato:
            self.esegui_logout()
        else:
            self.esegui_login_dialog() # Apri finestra di login

    def esegui_login_dialog(self):
        if not self.login_dialog:
            self.login_dialog = LoginRegistrazioneForm(self)

            self.login_dialog.gestore_utenti = self.gestore_utenti

            # Connetti il segnale login_successful_signal
            self.login_dialog.login_successful_signal.connect(self.on_login_success)

        result = self.login_dialog.exec() # Show Login Form as modal

        self.login_dialog = None


    def on_login_success(self, username: Utente):
        self.utente_loggato = username
        self.aggiorna_elementi()
        print(f"Login effettuato con successo per l'utente: {username}")


    def esegui_logout(self):
        self.utente_loggato = None
        self.aggiorna_elementi()
        print("Logout effettuato.")

    def apri_campi_boccie(self):
        if self.campo_bocce_form is None:
            self.campo_bocce_form = CampoBocceForm(self.gestore_servizi.get_servizi_by_tipe(CampoBocce), self.gestore_prenotazioni, self.utente_loggato)
            self.campo_bocce_form.exec()
            self.campo_bocce_form = None

    def apri_biliardino(self):
        print("Bottone 'Biliardino' cliccato!")

    def apri_torneo_burraco(self):
        print("Bottone 'Torneo Burraco' cliccato!")

    def apri_sala_biliardo(self):
        print("Bottone 'Sala da Biliardo' cliccato!")

    def apri_feedback(self):
        print("Bottone 'Feedback' cliccato!")

    def apri_amministratore(self):
        print("Bottone 'Amministratore' cliccato!")

if __name__ == "__main__":
    # Inizializzazione dei gestori
    gestore_utenti = GestioneUtenti()
    gestore_servizi = GestioneServizi()
    gestore_prenotazioni = GestionePrenotazioni()

    app = QtWidgets.QApplication(sys.argv)
    window = Ui(gestore_utenti, gestore_servizi, gestore_prenotazioni)
    window.show()
    app.exec()
