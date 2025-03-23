import copy

from Utenti.Utente import Utente
from Gestori.gestioneUtenti import GestioneUtenti
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
        # Clono il gestore
        gestore_clone = copy.deepcopy(gestore)
        with tempfile.gettempdir() as temp_dir:
            # Salvo il gestore su file, ricreo un gestore e leggo da file
            gestore.salva_su_file(f"{temp_dir}/test.json")
            gestore = GestioneUtenti()
            gestore.leggi_da_file(f"{temp_dir}/test.json")
            self.assertEqual(gestore, gestore_clone)

    
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
