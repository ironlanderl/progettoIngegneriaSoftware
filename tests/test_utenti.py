import copy
import os
from Utenti.Utente import Utente
from Gestori.gestione_utenti import GestioneUtenti
import unittest
import tempfile


class TestUtenti(unittest.TestCase):

    def test_aggiunta_utente(self):
        gestore = GestioneUtenti()
        gestore.aggiungi_utente("Mario", "Rossi", "mario.rossi", "password")
        self.assertEqual(len(gestore._utenti), 1)

    def test_rimozione_utente(self):
        gestore = GestioneUtenti()
        gestore.aggiungi_utente("Mario", "Rossi", "mario.rossi", "password")
        gestore.rimuovi_utente("mario.rossi")
        self.assertEqual(len(gestore._utenti), 0)

    def test_scrittura_lettura(self):
        # Creo un gestore e aggiungo un utente
        gestore = GestioneUtenti()
        gestore.aggiungi_utente("Mario", "Rossi", "mario.rossi", "password")

        # Uso un file temporaneo per il test
        temp_file = os.path.join(tempfile.gettempdir(), "test_utenti.pickle")

        try:
            # Salvo il gestore su file
            gestore.salva_su_file(temp_file)

            # Ricreo un gestore e leggo da file
            new_gestore = GestioneUtenti()
            new_gestore.leggi_da_file(temp_file)

            # Verifico che l'utente sia stato caricato correttamente
            self.assertEqual(len(new_gestore._utenti), 1)

        finally:
            # Pulizia: rimuovo il file temporaneo
            if os.path.exists(temp_file):
                os.remove(temp_file)

    
    def test_creazione_utente(self):
        utente = Utente("Mario", "Rossi", "mario.rossi", "password")
        self.assertEqual(utente._nome, "Mario")
        self.assertEqual(utente._cognome, "Rossi")
        self.assertEqual(utente._username, "mario.rossi")
        self.assertEqual(utente._password, "password")

    def test_cambio_password(self):
        utente = Utente("Mario", "Rossi", "mario.rossi", "password")
        utente.password = "nuova_password"
        self.assertEqual(utente._password, "nuova_password")
        with self.assertRaises(ValueError):
            utente.password = "nuova_password"

    def test_cambio_username(self):
        utente = Utente("Mario", "Rossi", "mario.rossi", "password")
        with self.assertRaises(ValueError):
            utente.username = "nuovo_username"
            self.assertNotEqual(utente._username, "nuovo_username")

    def test_creazione_utente_regression(self):
        with self.assertRaises(ValueError):
            _ = Utente("", "Rossi", "mario.rossi", "password")
        with self.assertRaises(ValueError):
            _ = Utente("Mario", "", "mario.rossi", "password")
        with self.assertRaises(ValueError):
            _ = Utente("Mario", "Rossi", "", "password")
        with self.assertRaises(ValueError):
            _ = Utente("Mario", "Rossi", "mario.rossi", "")


if __name__ == "__main__":
    _ = unittest.main()
