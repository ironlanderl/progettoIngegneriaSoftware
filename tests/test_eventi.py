import os
import unittest
import tempfile
from datetime import datetime, timedelta
import shutil

from Eventi.Torneo import Torneo
from Gestori.gestione_eventi import GestioneEventi



class TestEventi(unittest.TestCase):
    """
    Classe di test per le classi Torneo e GestioneEventi.
    """
    def setUp(self):
        """Configurazione prima di ogni test."""
        # Usa un file temporaneo per i test di GestioneEventi
        self.temp_dir = tempfile.gettempdir()
        self.temp_file = os.path.join(self.temp_dir, "test_eventi.pickle")
        self.default_file = "eventi.pickle" # File usato dalla gestione di default

        # Rimuove eventuali file esistenti per non avere interferenze tra i test
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        # Rimuove il file di default se esiste, per garantire un gestore pulito
        if os.path.exists(self.default_file):
            os.remove(self.default_file)

        # Inizializza il gestore. Ora caricherà dal file dummy creato.
        self.gestore = GestioneEventi()
        # Pulisce gli eventi caricati dal file dummy per avere un punto di partenza vuoto per la maggior parte dei test.
        self.gestore._eventi.clear()


    def tearDown(self):
        """Pulizia dopo ogni test."""
        # Rimuove i file temporanei e di default usati nel test
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        if os.path.exists(self.default_file):
            os.remove(self.default_file)

    def test_aggiunta_evento(self):
        """Verifica che un evento venga aggiunto correttamente."""
        # Crea una data futura
        data_futura = datetime.now() + timedelta(days=10)
        # Formatta la data come stringa per il metodo aggiungi_evento di GestioneEventi
        data_stringa = data_futura.strftime("%Y-%m-%d %H:%M:%S")
        
        self.gestore.aggiungi_evento(data_stringa)
        
        self.assertEqual(len(self.gestore._eventi), 1)
        evento = self.gestore._eventi[0]
        # Confronta gli oggetti datetime
        self.assertEqual(evento.data, data_futura.replace(microsecond=0))

    def test_aggiunta_evento_data_passata_raises(self):
        """Verifica che l'aggiunta di un evento con data passata fallisca."""
        # Crea una data passata
        data_passata = datetime.now() - timedelta(days=10)
        # Formatta la data come stringa
        data_stringa = data_passata.strftime("%Y-%m-%d %H:%M:%S")

        # aggiungi_evento chiama il setter di Torneo, che solleva ValueError
        with self.assertRaises(ValueError):
             self.gestore.aggiungi_evento(data_stringa)

    def test_aggiunta_evento_formato_data_errato_raises(self):
         """Verifica che l'aggiunta di un evento con formato data errato fallisca."""
         # aggiungi_evento parsa la stringa, sollevando ValueError se il formato è sbagliato
         with self.assertRaises(ValueError):
              self.gestore.aggiungi_evento("data non valida")
    
    def test_rimozione_evento(self):
        """Verifica che un evento venga rimosso correttamente."""
        data_futura = datetime.now() + timedelta(days=10)
        data_stringa = data_futura.strftime("%Y-%m-%d %H:%M:%S")
        
        self.gestore.aggiungi_evento(data_stringa)
        self.assertEqual(len(self.gestore._eventi), 1)
        
        self.gestore.rimuovi_evento(data_stringa)
        self.assertEqual(len(self.gestore._eventi), 0)

    def test_rimozione_evento_inesistente_raises(self):
        """Verifica che la rimozione di un evento inesistente fallisca."""
        # Assicurati che non ci siano eventi
        self.gestore._eventi.clear()
        data_inesistente_stringa = (datetime.now() + timedelta(days=20)).strftime("%Y-%m-%d %H:%M:%S")

        # rimuovi_evento chiama get_evento, che solleva ValueError se non trova l'evento
        with self.assertRaises(ValueError):
             self.gestore.rimuovi_evento(data_inesistente_stringa)

    
    def test_salva_leggi_file_gestore(self):
        """Verifica il salvataggio e il caricamento degli eventi da file tramite GestioneEventi."""
        data_futura = datetime.now() + timedelta(days=10)
        data_stringa = data_futura.strftime("%Y-%m-%d %H:%M:%S")
        
        self.gestore.aggiungi_evento(data_stringa)
        self.gestore.aggiungi_partecipante(data_stringa, "Team Alpha", "UtenteA")
        self.gestore.aggiungi_partecipante(data_stringa, "Team Beta", "UtenteB")

        # Salva il gestore su file temporaneo
        self.gestore.salva_su_file(self.temp_file)

        # Crea un nuovo gestore e carica dal file salvato
        # Rimuove il file di default per assicurarsi che il nuovo gestore non lo carichi per errore
        if os.path.exists(self.default_file):
             os.remove(self.default_file)

        # Rimuove il gestore creato in setUp per testare l'inizializzazione da zero
        del self.gestore

        # Sposta il file temporaneo nella directory corrente per farlo trovare da __init__
        self.assertTrue(os.path.exists(self.temp_file))
        shutil.move(self.temp_file, self.default_file) # Usa shutil.move
        self.assertTrue(os.path.exists(self.default_file)) # Verifica che lo spostamento sia avvenuto

        gestore_caricato = GestioneEventi()
        
        self.assertEqual(len(gestore_caricato._eventi), 1)
        
        # Verifica che l'evento caricato abbia la data corretta e le squadre/partecipanti
        evento_caricato = gestore_caricato._eventi[0]
        self.assertEqual(evento_caricato.data, data_futura.replace(microsecond=0))
        self.assertIn("Team Alpha", evento_caricato.squadre)
        self.assertIn("Team Beta", evento_caricato.squadre)
        self.assertIn("UtenteA", evento_caricato.squadre["Team Alpha"])
        self.assertIn("UtenteB", evento_caricato.squadre["Team Beta"])
        self.assertEqual(len(evento_caricato.squadre["Team Alpha"]), 1) # Solo UtenteA
        self.assertEqual(len(evento_caricato.squadre["Team Beta"]), 1) # Solo UtenteB

    
    def test_creazione_torneo(self):
        """Verifica l'inizializzazione corretta di un Torneo."""
        data_futura = datetime.now() + timedelta(days=10)
        torneo = Torneo(data_futura)
        
        # I valori di default o iniziali devono essere coerenti
        self.assertEqual(torneo.data.replace(microsecond=0), data_futura.replace(microsecond=0))
        # Verifica che il dizionario squadre sia inizializzato come vuoto
        self.assertEqual(torneo.squadre, {})
    
    def test_torneo_setter_data_passata_raises(self):
        """Verifica che impostare una data passata sul Torneo sollevi ValueError."""
        data_futura = datetime.now() + timedelta(days=10)
        torneo = Torneo(data_futura)
        data_passata = datetime.now() - timedelta(days=1)
        with self.assertRaises(ValueError):
            torneo.data = data_passata
            
    def test_torneo_setter_data_wrong_type_raises(self):
         """Verifica che impostare una data non datetime sul Torneo sollevi TypeError."""
         data_futura = datetime.now() + timedelta(days=10)
         torneo = Torneo(data_futura)
         with self.assertRaises(TypeError):
             torneo.data = "data non valida"

    def test_torneo_aggiungi_squadra(self):
        """Verifica l'aggiunta di una squadra a un torneo."""
        data_futura = datetime.now() + timedelta(days=10)
        torneo = Torneo(data_futura)
        torneo.aggiungi_squadra("Squadra Rossa")
        self.assertIn("Squadra Rossa", torneo.squadre)
        self.assertEqual(torneo.squadre["Squadra Rossa"], [])
        self.assertEqual(len(torneo.squadre), 1)

    def test_torneo_aggiungi_squadra_duplicata_raises(self):
        """Verifica che l'aggiunta di una squadra duplicata fallisca."""
        data_futura = datetime.now() + timedelta(days=10)
        torneo = Torneo(data_futura)
        torneo.aggiungi_squadra("Squadra Rossa")
        with self.assertRaises(ValueError):
             torneo.aggiungi_squadra("Squadra Rossa")

    def test_torneo_aggiungi_utente_a_squadra(self):
        """Verifica l'aggiunta di un utente a una squadra esistente."""
        data_futura = datetime.now() + timedelta(days=10)
        torneo = Torneo(data_futura)
        torneo.aggiungi_squadra("Squadra Blu")
        torneo.aggiungi_utente_a_squadra("Squadra Blu", "Utente A")
        self.assertIn("Utente A", torneo.squadre["Squadra Blu"])
        self.assertEqual(len(torneo.squadre["Squadra Blu"]), 1)

    def test_torneo_aggiungi_utente_a_squadra_inesistente_raises(self):
        """Verifica che l'aggiunta di un utente a una squadra inesistente fallisca."""
        data_futura = datetime.now() + timedelta(days=10)
        torneo = Torneo(data_futura)
        with self.assertRaises(ValueError):
             torneo.aggiungi_utente_a_squadra("Squadra Inesistente", "Utente A")

    def test_torneo_aggiungi_utente_duplicato_raises(self):
        """Verifica che l'aggiunta di un utente duplicato nella stessa squadra fallisca."""
        data_futura = datetime.now() + timedelta(days=10)
        torneo = Torneo(data_futura)
        torneo.aggiungi_squadra("Squadra Verde")
        torneo.aggiungi_utente_a_squadra("Squadra Verde", "Utente B")
        with self.assertRaises(ValueError):
             torneo.aggiungi_utente_a_squadra("Squadra Verde", "Utente B")

    def test_torneo_rimuovi_utente_da_squadra(self):
        """Verifica la rimozione di un utente da una squadra."""
        data_futura = datetime.now() + timedelta(days=10)
        torneo = Torneo(data_futura)
        torneo.aggiungi_squadra("Squadra Gialla")
        torneo.aggiungi_utente_a_squadra("Squadra Gialla", "Utente C")
        torneo.aggiungi_utente_a_squadra("Squadra Gialla", "Utente D")
        self.assertEqual(len(torneo.squadre["Squadra Gialla"]), 2)

        torneo.rimuovi_utente_da_squadra("Squadra Gialla", "Utente C")
        self.assertNotIn("Utente C", torneo.squadre["Squadra Gialla"])
        self.assertEqual(len(torneo.squadre["Squadra Gialla"]), 1)
        self.assertIn("Utente D", torneo.squadre["Squadra Gialla"])

    def test_torneo_rimuovi_utente_inesistente_raises(self):
        """Verifica che la rimozione di un utente inesistente da una squadra fallisca."""
        data_futura = datetime.now() + timedelta(days=10)
        torneo = Torneo(data_futura)
        torneo.aggiungi_squadra("Squadra Viola")
        torneo.aggiungi_utente_a_squadra("Squadra Viola", "Utente E")
        with self.assertRaises(ValueError):
             torneo.rimuovi_utente_da_squadra("Squadra Viola", "Utente Inesistente")

    def test_torneo_rimuovi_utente_da_squadra_inesistente_raises(self):
        """Verifica che la rimozione di un utente da una squadra inesistente fallisca."""
        data_futura = datetime.now() + timedelta(days=10)
        torneo = Torneo(data_futura)
        with self.assertRaises(ValueError):
             torneo.rimuovi_utente_da_squadra("Squadra Inesistente", "Utente F")

    def test_torneo_rimuovi_squadra(self):
        """Verifica la rimozione di una squadra da un torneo."""
        data_futura = datetime.now() + timedelta(days=10)
        torneo = Torneo(data_futura)
        torneo.aggiungi_squadra("Squadra Nera")
        torneo.aggiungi_squadra("Squadra Bianca")
        self.assertEqual(len(torneo.squadre), 2)

        torneo.rimuovi_squadra("Squadra Nera")
        self.assertNotIn("Squadra Nera", torneo.squadre)
        self.assertEqual(len(torneo.squadre), 1)
        self.assertIn("Squadra Bianca", torneo.squadre)

    def test_torneo_rimuovi_squadra_inesistente_raises(self):
        """Verifica che la rimozione di una squadra inesistente fallisca."""
        data_futura = datetime.now() + timedelta(days=10)
        torneo = Torneo(data_futura)
        with self.assertRaises(ValueError):
             torneo.rimuovi_squadra("Squadra Inesistente")


    def test_get_evento(self):
        """Verifica il recupero di un evento tramite GestioneEventi."""
        data_futura = datetime.now() + timedelta(days=10)
        data_stringa = data_futura.strftime("%Y-%m-%d %H:%M:%S")
        data_futura_no_micros = data_futura.replace(microsecond=0)

        self.gestore.aggiungi_evento(data_stringa)
        
        # Recupera l'evento usando la stringa data
        evento = self.gestore.get_evento(data_stringa)
        self.assertIsNotNone(evento)
        # Verifica che l'evento recuperato abbia la data corretta
        self.assertEqual(evento.data, data_futura_no_micros)
    
        # Test per evento inesistente
        data_inesistente_stringa = (datetime.now() + timedelta(days=20)).strftime("%Y-%m-%d %H:%M:%S")
        with self.assertRaises(ValueError):
            self.gestore.get_evento(data_inesistente_stringa)

        # Test con formato data errato nella ricerca (GestioneEventi.get_evento parsa la stringa)
        with self.assertRaises(ValueError):
             self.gestore.get_evento("data non valida per ricerca")

if __name__ == "__main__":
    unittest.main(verbosity=2)