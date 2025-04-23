from PyQt6 import QtWidgets, uic
from Eventi.Torneo import Torneo

class GestioneMembriSquadraForm(QtWidgets.QDialog):
    def __init__(self, torneo, nome_squadra: str):
        super().__init__()
        uic.loadUi('./windows/gestione_membri_squadra.ui', self)
        
        self.torneo = torneo
        self.nome_squadra = nome_squadra

        self.setWindowTitle(f"Gestione Membri Squadra - {self.nome_squadra}")
        self.lblNomeSquadra.setText(f"Squadra: {self.nome_squadra}")

        self.aggiorna_lista_membri()

        self.btnAggiungiMembro.clicked.connect(self.aggiungi_membro)
        self.btnRimuoviMembro.clicked.connect(self.rimuovi_membro)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def aggiorna_lista_membri(self):
        self.lstMembriSquadra.clear()
        membri = self.torneo.squadre.get(self.nome_squadra, [])
        for membro in membri:
            self.lstSquadreItem = QtWidgets.QListWidgetItem(membro)
            self.lstMembriSquadra.addItem(self.lstSquadreItem)

    def aggiungi_membro(self):
        nuovo_membro = self.txtNuovoMembro.text().strip()
        if nuovo_membro:
            # Aggiunge il nuovo membro nella squadra all'interno del torneo
            self.torneo.squadre.setdefault(self.nome_squadra, []).append(nuovo_membro)
            self.aggiorna_lista_membri()
            self.txtNuovoMembro.clear()
        else:
            QtWidgets.QMessageBox.warning(self, "Errore", "Inserisci un nome per il nuovo membro.")

    def rimuovi_membro(self):
        current_item = self.lstMembriSquadra.currentItem()
        if current_item:
            membro = current_item.text()
            try:
                self.torneo.squadre[self.nome_squadra].remove(membro)
                self.aggiorna_lista_membri()
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Errore", "Impossibile rimuovere il membro.")
        else:
            QtWidgets.QMessageBox.warning(self, "Errore", "Seleziona un membro da rimuovere.")