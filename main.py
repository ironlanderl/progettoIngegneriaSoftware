from typing import override
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QComboBox, QPlainTextEdit, QPushButton
import sys
import random
import pprint

class Test():
    def __init__(self, number: int):
        self.number = number

    @override
    def __str__(self) -> str:
        return f"Test: {self.number}"


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('./windows/testing.ui', self)

        self.test1 = Test(10)
        self.test2 = Test(20)
        self.test3 = Test(30)


        # Azioni Pulsanti
        self.btnCopyText.clicked.connect(self.copyButtonPressed)
        self.btnCopyCombo.clicked.connect(self.cmbButtonPressed)

        # Popolamento combobox
        self.populate_combobox()
    

        self.show()

    def copyButtonPressed(self):
        self.txtCopyOutput.insertPlainText(str(random.randint(0, 100)))

    def cmbButtonPressed(self):
        self.txtComboOutput.setText(self.cmbInput.currentText())
        print("Current combo index: ", self.cmbInput.currentIndex())

    def populate_combobox(self):
        self.cmbInput.clear()
        self.cmbInput.addItems([str(self.test1), str(self.test2), str(self.test3)])

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec()
