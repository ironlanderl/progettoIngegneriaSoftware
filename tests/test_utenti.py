import os
import tempfile
import unittest
import pickle

from Utenti.Utente import Utente
from Gestori.gestione_utenti import GestioneUtenti

class TestUtente(unittest.TestCase):
    """
    Classe di test per la classe Utente.
    """
    def test_creazione_utente(self):
        """Verifica la creazione base di un utente."""
        utente = Utente("Mario", "Rossi", "mario.rossi", "password")
        self.assertEqual(utente.nome, "Mario")
        self.assertEqual(utente.cognome, "Rossi")
        self.assertEqual(utente.username, "mario.rossi")
        self.assertEqual(utente.password, "password")
    
    def test_nome_vuoto_raises(self):
        """Verifica che la creazione fallisca con nome vuoto."""
        with self.assertRaises(ValueError):
            Utente("", "Rossi", "mario.rossi", "password")
    
    def test_cognome_vuoto_raises(self):
        """Verifica che la creazione fallisca con cognome vuoto."""
        with self.assertRaises(ValueError):
            Utente("Mario", "", "mario.rossi", "password")
    
    def test_username_vuoto_raises(self):
        """Verifica che la creazione fallisca con username vuoto."""
        with self.assertRaises(ValueError):
            Utente("Mario", "Rossi", "", "password")
    
    def test_password_vuota_raises(self):
        """Verifica che la creazione fallisca con password vuota."""
        with self.assertRaises(ValueError):
            Utente("Mario", "Rossi", "mario.rossi", "")
    
    def test_modifiche_username_not_allowed(self):
        """Verifica che non sia possibile modificare lo username dopo la creazione."""
        utente = Utente("Mario", "Rossi", "mario.rossi", "password")
        with self.assertRaises(ValueError):
            utente.username = "nuovo_username"
    
    def test_modifica_password(self):
        """Verifica la modifica della password."""
        utente = Utente("Mario", "Rossi", "mario.rossi", "password")
        utente.password = "nuova_password"
        self.assertEqual(utente.password, "nuova_password")
        # Questo test verifica se si solleva eccezione se si imposta la stessa password.
        with self.assertRaises(ValueError):
            utente.password = "nuova_password"

class TestGestioneUtenti(unittest.TestCase):
    """
    Classe di test per la classe GestioneUtenti.
    """
    def setUp(self):
        """Configurazione prima di ogni test."""
        # Utilizza un file temporaneo per i test
        self.temp_dir = tempfile.gettempdir()
        self.temp_file = os.path.join(self.temp_dir, "test_utenti.pickle")
        self.default_file = "utenti.pickle" # File usato dalla gestione di default

        # Rimuove eventuali file esistenti per non avere interferenze tra i test
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        # Rimuove il file di default se esiste, per garantire un gestore pulito
        if os.path.exists(self.default_file):
            os.remove(self.default_file)

        
        # Inizializza il gestore. Ora caricherà dal file dummy creato.
        self.gestore = GestioneUtenti()
        # Pulisce la lista utenti caricata dal file dummy per avere un punto di partenza vuoto per la maggior parte dei test.
        self.gestore._utenti = []
    
    def tearDown(self):
        """Pulizia dopo ogni test."""
        # Rimuove il file temporaneo se esiste
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        # Rimuove il file di default se esiste
        if os.path.exists(self.default_file):
            os.remove(self.default_file)
    
    def test_aggiungi_utente(self):
        """Verifica l'aggiunta di un utente."""
        utente = self.gestore.aggiungi_utente("Mario", "Rossi", "mario.rossi", "password")
        self.assertEqual(len(self.gestore._utenti), 1)
        self.assertEqual(self.gestore._utenti[0].username, "mario.rossi")
        self.assertEqual(utente.username, "mario.rossi") # Verifica anche il valore ritornato
    
    def test_aggiungi_utente_duplicato_raises(self):
        """Verifica che l'aggiunta di un utente con username duplicato fallisca."""
        self.gestore.aggiungi_utente("Mario", "Rossi", "mario.rossi", "password")
        with self.assertRaises(ValueError):
            self.gestore.aggiungi_utente("Luigi", "Verdi", "mario.rossi", "password2") # Stesso username

    def test_rimuovi_utente(self):
        """Verifica la rimozione di un utente esistente."""
        self.gestore.aggiungi_utente("Mario", "Rossi", "mario.rossi", "password")
        self.assertEqual(len(self.gestore._utenti), 1)
        self.gestore.rimuovi_utente("mario.rossi")
        self.assertEqual(len(self.gestore._utenti), 0)

    def test_rimuovi_utente_inesistente_raises(self):
        """Verifica che la rimozione di un utente inesistente fallisca."""
        # Assicurati che non ci siano utenti
        self.gestore._utenti.clear()
        with self.assertRaises(ValueError):
            self.gestore.rimuovi_utente("utente_inesistente")
    
    def test_get_utente_valid(self):
        """Verifica il recupero di un utente esistente."""
        self.gestore.aggiungi_utente("Mario", "Rossi", "mario.rossi", "password")
        utente = self.gestore.get_utente("mario.rossi")
        self.assertIsNotNone(utente)
        self.assertEqual(utente.nome, "Mario")
        self.assertEqual(utente.username, "mario.rossi")
    
    def test_get_utente_invalid(self):
        """Verifica che il recupero di un utente inesistente fallisca."""
        with self.assertRaises(ValueError):
            self.gestore.get_utente("utente_inesistente")
    
    def test_get_utenti(self):
        """Verifica il recupero della lista completa degli utenti."""
        self.gestore.aggiungi_utente("Mario", "Rossi", "mario.rossi", "password")
        self.gestore.aggiungi_utente("Luigi", "Verdi", "luigi.verdi", "password2")
        utenti = self.gestore.get_utenti()
        self.assertEqual(len(utenti), 2)
        self.assertIn("mario.rossi", [u.username for u in utenti])
        self.assertIn("luigi.verdi", [u.username for u in utenti])

    def test_check_credenziali_success(self):
        """Verifica la validazione di credenziali corrette."""
        self.gestore.aggiungi_utente("Mario", "Rossi", "mario.rossi", "password")
        result, utente = self.gestore.check_credenziali("mario.rossi", "password")
        self.assertTrue(result)
        self.assertIsNotNone(utente)
        self.assertEqual(utente.username, "mario.rossi")
    
    def test_check_credenziali_failure(self):
        """Verifica la validazione di credenziali errate."""
        self.gestore.aggiungi_utente("Mario", "Rossi", "mario.rossi", "password")
        result, utente = self.gestore.check_credenziali("mario.rossi", "wrongpassword")
        self.assertFalse(result)
        self.assertIsNone(utente)

    def test_check_credenziali_user_not_exist(self):
        """Verifica la validazione con username non esistente."""
        self.gestore.aggiungi_utente("Mario", "Rossi", "mario.rossi", "password")
        result, utente = self.gestore.check_credenziali("utente_inesistente", "password")
        self.assertFalse(result)
        self.assertIsNone(utente)
    
    def test_salva_leggi_file(self):
        """Verifica il salvataggio e caricamento degli utenti su file."""
        self.gestore.aggiungi_utente("Mario", "Rossi", "mario.rossi", "password")
        self.gestore.aggiungi_utente("Luigi", "Verdi", "luigi.verdi", "password2")

        # Salva il gestore su file temporaneo
        self.gestore.salva_su_file(self.temp_file)
        
        # Crea un nuovo gestore pulito e carica dal file salvato
        # Rimuove il file di default per assicurarsi che il nuovo gestore carichi dal temp_file
        if os.path.exists(self.default_file):
            os.remove(self.default_file)
        
        new_gestore = GestioneUtenti()
        # Assicura che il nuovo gestore inizi vuoto prima di leggere
        new_gestore._utenti = [] 
        new_gestore.leggi_da_file(self.temp_file)
        
        self.assertEqual(len(new_gestore._utenti), 2)
        user_loaded = new_gestore.get_utente("mario.rossi")
        self.assertIsNotNone(user_loaded)
        self.assertEqual(user_loaded.nome, "Mario")
        user_loaded2 = new_gestore.get_utente("luigi.verdi")
        self.assertIsNotNone(user_loaded2)
        self.assertEqual(user_loaded2.cognome, "Verdi")


if __name__ == "__main__":
    unittest.main(verbosity=2)