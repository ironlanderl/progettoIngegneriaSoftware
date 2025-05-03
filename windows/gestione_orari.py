from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QTime
from Gestori.gestione_prenotazioni import GestionePrenotazioni

class GestioneOrariForm(QtWidgets.QDialog):
    def __init__(self, gestore_prenotazioni: GestionePrenotazioni):
        super().__init__()
        uic.loadUi('./windows/gestione_orari.ui', self)
        self.gestore_prenotazioni = gestore_prenotazioni

        # Connessione con il bottone
        self.buttonBox.accepted.connect(self.invia_orari)

        # Popola i campi con gli orari attuali
        self.populate_orari()

    def populate_orari(self):
        # Lista dei giorni in italiano, corrispondenti alle chiavi usate in gestione prenotazioni
        giorni = ["Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi", "Sabato", "Domenica"]

        giorni_italian_to_english = {
            "Lunedi": "Monday",
            "Martedi": "Tuesday",
            "Mercoledi": "Wednesday",
            "Giovedi": "Thursday",
            "Venerdi": "Friday",
            "Sabato": "Saturday",
            "Domenica": "Sunday"
        }

        for giorno in giorni:
            # Recupera i widget dinamicamente in base al giorno
            timeEditApertura = self.findChild(QtWidgets.QTimeEdit, f"timeEdit{giorno}Apertura")
            timeEditChiusura = self.findChild(QtWidgets.QTimeEdit, f"timeEdit{giorno}Chiusura")

            orario_apertura = self.gestore_prenotazioni.get_orario_apertura(giorni_italian_to_english[giorno])
            orario_chiusura = self.gestore_prenotazioni.get_orario_chiusura(giorni_italian_to_english[giorno])

            # Converte la stringa "HH:mm" in QTime e imposta i campi
            qt_time_apertura = QTime.fromString(orario_apertura, "HH:mm")
            qt_time_chiusura = QTime.fromString(orario_chiusura, "HH:mm")
            timeEditApertura.setTime(qt_time_apertura)
            timeEditChiusura.setTime(qt_time_chiusura)

    def invia_orari(self):
        giorni = ["Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi", "Sabato", "Domenica"]

        giorni_italian_to_english = {
            "Lunedi": "Monday",
            "Martedi": "Tuesday",
            "Mercoledi": "Wednesday",
            "Giovedi": "Thursday",
            "Venerdi": "Friday",
            "Sabato": "Saturday",
            "Domenica": "Sunday"
        }

        try:
            for giorno in giorni:
                timeEditApertura = self.findChild(QtWidgets.QTimeEdit, f"timeEdit{giorno}Apertura")
                timeEditChiusura = self.findChild(QtWidgets.QTimeEdit, f"timeEdit{giorno}Chiusura")
                # Ottieni gli orari in formato stringa "HH:mm"
                nuovo_apertura = timeEditApertura.time().toString("HH:mm")
                nuovo_chiusura = timeEditChiusura.time().toString("HH:mm")

                self.gestore_prenotazioni.set_orario_apertura(giorni_italian_to_english[giorno], nuovo_apertura)
                self.gestore_prenotazioni.set_orario_chiusura(giorni_italian_to_english[giorno], nuovo_chiusura)

            self.gestore_prenotazioni.salva_orari_su_file("orari.json")
            self.accept()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Errore", f"Si è verificato un errore: {e}")