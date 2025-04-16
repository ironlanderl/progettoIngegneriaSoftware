from PyQt6 import QtWidgets, uic, QtCore
from Gestori.gestione_utenti import GestioneUtenti
from Utenti.Utente import Utente

class LoginRegistrazioneForm(QtWidgets.QDialog):
    login_successful_signal = QtCore.pyqtSignal(Utente)

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('./windows/login.ui', self)

        # Connetti i segnali clicked() dei bottoni alle funzioni
        self.btnLogin.clicked.connect(self.esegui_login)
        self.btnRegistrazione.clicked.connect(self.esegui_registrazione)

    def esegui_login(self):
        username = self.txtUsernameLogin.text()
        password = self.txtPasswordLogin.text()
        res, user = self.gestore_utenti.check_credenziali(username, password)
        if res:
            self.lblMessaggio.setText("Login effettuato con successo!")
            self.login_successful_signal.emit(user) # Emit signal with username (user object)
            self.accept() # Chiude la finestra di login con risultato accettato (QDialog.Accepted)
        else:
            self.lblMessaggio.setText("Credenziali di login errate.")

    def esegui_registrazione(self):
        nome = self.txtNomeRegistrazione.text()
        cognome = self.txtCognomeRegistrazione.text()
        username = self.txtUsernameRegistrazione.text()
        password = self.txtPasswordRegistrazione.text()
        conferma_password = self.txtConfermaPasswordRegistrazione.text()
        if password == conferma_password and len(password) > 5:
            user = self.gestore_utenti.aggiungi_utente(nome, cognome, username, password)
            if user:
                self.lblMessaggio.setText("Registrazione effettuata con successo!")
                self.login_successful_signal.emit(user)
                self.accept()
            else:
                self.lblMessaggio.setText("Errore nella registrazione (utente non creato).") # Handle case where user creation fails.
        else:
            self.lblMessaggio.setText("Errore nella registrazione. Controlla i campi.")
