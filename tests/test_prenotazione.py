import unittest
import datetime
from Utenti.Cliente import Cliente
from Servizi.Servizio import Servizio
from Servizi.Prenotazione import Prenotazione
from Servizi.CampoBocce import CampoBocce
from Servizi.SalaBiliardo import SalaBiliardo
from Gestori.gestione_prenotazioni import GestioneEventi
import os
import tempfile
import pickle


class TestPrenotazione(unittest.TestCase):
    def setUp(self):
        # Creo istanze da utilizzare nei test
        self.cliente = Cliente("Mario", "Rossi", "mario", "password123", False)
        self.servizio = CampoBocce(15.0, "Campo da bocce", "Campo Bocce 1", 2, "Contanti/Carta")
        self.data = datetime.datetime(2025, 4, 20, 14, 0)  # 20 Aprile 2025, ore 14:00
        self.durata = datetime.timedelta(hours=2)  # Durata di 2 ore
    
    def test_creazione_prenotazione(self):
        """Test per verificare la creazione corretta di una prenotazione"""
        prenotazione = Prenotazione(self.servizio, self.data, self.durata, self.cliente)
        
        self.assertEqual(prenotazione.servizio, self.servizio)
        self.assertEqual(prenotazione.data, self.data)
        self.assertEqual(prenotazione.durata, self.durata)
        self.assertEqual(prenotazione.cliente_prenotazione, self.cliente)
        
    def test_prenotazione_attributi(self):
        """Test per verificare la correttezza degli attributi di una prenotazione"""
        prenotazione = Prenotazione(self.servizio, self.data, self.durata, self.cliente)
        
        # Verifica che la prenotazione abbia gli attributi corretti
        self.assertTrue(hasattr(prenotazione, 'servizio'))
        self.assertTrue(hasattr(prenotazione, 'data'))
        self.assertTrue(hasattr(prenotazione, 'durata'))
        self.assertTrue(hasattr(prenotazione, 'cliente_prenotazione'))
    
    def test_modifica_prenotazione(self):
        """Test per verificare la modifica dei dati di una prenotazione"""
        prenotazione = Prenotazione(self.servizio, self.data, self.durata, self.cliente)
        
        # Modifica la data e la durata
        nuova_data = datetime.datetime(2025, 4, 21, 16, 0)  # 21 Aprile 2025, ore 16:00
        nuova_durata = datetime.timedelta(hours=3)  # Durata di 3 ore
        
        # Verifica che si possano modificare gli attributi
        try:
            prenotazione.data = nuova_data
            prenotazione.durata = nuova_durata
            self.assertEqual(prenotazione.data, nuova_data)
            self.assertEqual(prenotazione.durata, nuova_durata)
        except AttributeError:
            self.fail("Non è possibile modificare gli attributi della prenotazione")


class TestGestioneEventi(unittest.TestCase):
    def setUp(self):
        self.gestore_eventi = GestioneEventi()
        self.cliente1 = Cliente("Mario", "Rossi", "mario", "password123", False)
        self.cliente2 = Cliente("Luigi", "Verdi", "luigi", "password456", False)
        self.servizio1 = CampoBocce(15.0, "Campo da bocce", "Campo Bocce 1", 2, "Contanti/Carta")
        self.servizio2 = SalaBiliardo(20.0, "Sala biliardo", "Sala Biliardo 1", 3)
        self.data1 = datetime.datetime(2025, 4, 20, 14, 0)
        self.data2 = datetime.datetime(2025, 4, 21, 16, 0)
        self.durata1 = datetime.timedelta(hours=2)
        self.durata2 = datetime.timedelta(hours=3)
    
    def test_aggiungi_evento(self):
        """Test per verificare l'aggiunta di un evento alla gestione eventi"""
        self.gestore_eventi.aggiungi_evento(self.servizio1, self.data1, self.durata1, self.cliente1)
        
        # Verifica che ci sia un evento nel gestore
        self.assertEqual(len(self.gestore_eventi._eventi), 1)
        
        # Aggiungi un altro evento
        self.gestore_eventi.aggiungi_evento(self.servizio2, self.data2, self.durata2, self.cliente2)
        self.assertEqual(len(self.gestore_eventi._eventi), 2)
    
    def test_get_prenotazione(self):
        """Test per verificare il recupero di una prenotazione"""
        self.gestore_eventi.aggiungi_evento(self.servizio1, self.data1, self.durata1, self.cliente1)
        self.gestore_eventi.aggiungi_evento(self.servizio2, self.data2, self.durata2, self.cliente2)
        
        # Recupera la prenotazione del cliente1
        prenotazione = self.gestore_eventi.get_prenotazione(self.data1, self.cliente1)
        self.assertIsNotNone(prenotazione)
        self.assertEqual(prenotazione.servizio, self.servizio1)
        self.assertEqual(prenotazione.data, self.data1)
        self.assertEqual(prenotazione.durata, self.durata1)
        self.assertEqual(prenotazione.cliente_prenotazione, self.cliente1)
        
        # Recupera la prenotazione del cliente2
        prenotazione = self.gestore_eventi.get_prenotazione(self.data2, self.cliente2)
        self.assertIsNotNone(prenotazione)
        self.assertEqual(prenotazione.servizio, self.servizio2)
        self.assertEqual(prenotazione.data, self.data2)
        self.assertEqual(prenotazione.durata, self.durata2)
        self.assertEqual(prenotazione.cliente_prenotazione, self.cliente2)
        
        # Prova a recuperare una prenotazione inesistente
        prenotazione = self.gestore_eventi.get_prenotazione(datetime.datetime(2025, 4, 22, 14, 0), self.cliente1)
        self.assertIsNone(prenotazione)
    
    def test_elimina_prenotazione(self):
        """Test per verificare l'eliminazione di una prenotazione"""
        # Aggiungi due prenotazioni
        self.gestore_eventi.aggiungi_evento(self.servizio1, self.data1, self.durata1, self.cliente1)
        self.gestore_eventi.aggiungi_evento(self.servizio2, self.data2, self.durata2, self.cliente2)
        self.assertEqual(len(self.gestore_eventi._eventi), 2)
        
        # Elimina una prenotazione
        self.gestore_eventi.elimina_prenotazione(self.data1, self.cliente1)
        self.assertEqual(len(self.gestore_eventi._eventi), 1)
        
        # Verifica che la prenotazione corretta sia stata eliminata
        prenotazione = self.gestore_eventi.get_prenotazione(self.data1, self.cliente1)
        self.assertIsNone(prenotazione)
        
        prenotazione = self.gestore_eventi.get_prenotazione(self.data2, self.cliente2)
        self.assertIsNotNone(prenotazione)
    
    def test_salva_leggi_file(self):
        """Test per verificare il salvataggio e la lettura da file"""
        # Crea e aggiungi alcune prenotazioni
        self.gestore_eventi.aggiungi_evento(self.servizio1, self.data1, self.durata1, self.cliente1)
        self.gestore_eventi.aggiungi_evento(self.servizio2, self.data2, self.durata2, self.cliente2)
        
        # Crea un file temporaneo per il test
        temp_file = os.path.join(tempfile.gettempdir(), "test_prenotazioni.pkl")
        
        try:
            # Salva su file
            self.gestore_eventi.salva_su_file(temp_file)
            
            # Crea un nuovo gestore e carica dal file
            nuovo_gestore = GestioneEventi()
            nuovo_gestore.leggi_da_file(temp_file)
            
            # Verifica che ci siano le stesse prenotazioni
            self.assertEqual(len(nuovo_gestore._eventi), 2)
            
            # Verifica che le prenotazioni siano corrette
            prenotazione1 = nuovo_gestore.get_prenotazione(self.data1, self.cliente1)
            self.assertIsNotNone(prenotazione1)
            self.assertEqual(prenotazione1.servizio.nome_servizio, self.servizio1.nome_servizio)
            self.assertEqual(prenotazione1.data, self.data1)
            
            prenotazione2 = nuovo_gestore.get_prenotazione(self.data2, self.cliente2)
            self.assertIsNotNone(prenotazione2)
            self.assertEqual(prenotazione2.servizio.nome_servizio, self.servizio2.nome_servizio)
            self.assertEqual(prenotazione2.data, self.data2)
            
        finally:
            # Pulizia: rimuovi il file temporaneo
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_errore_elimina_prenotazione_inesistente(self):
        """Test per verificare il comportamento quando si elimina una prenotazione inesistente"""
        # Non aggiungi prenotazioni
        
        # Prova a eliminare una prenotazione inesistente
        with self.assertRaises(ValueError):
            self.gestore_eventi.elimina_prenotazione(self.data1, self.cliente1)


if __name__ == '__main__':
    unittest.main()
