import copy
import os
from Eventi.Torneo import Torneo
from Gestori.gestione_eventi import GestioneEventi
import unittest
import tempfile
from datetime import datetime, timedelta


class TestEventi(unittest.TestCase):

    def test_aggiunta_evento(self):
        gestore = GestioneEventi()
        # Crea una data futura
        data_futura = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
        gestore.aggiungi_evento(data_futura, 16, "Scacchi")
        self.assertEqual(len(gestore._eventi), 1)

    def test_rimozione_evento(self):
        gestore = GestioneEventi()
        # Crea una data futura
        data_futura = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
        gestore.aggiungi_evento(data_futura, 16, "Scacchi")
        gestore.rimuovi_evento(data_futura)
        self.assertEqual(len(gestore._eventi), 0)

    def test_scrittura_lettura(self):
        # Creo un gestore e aggiungo un evento
        gestore = GestioneEventi()
        # Crea una data futura
        data_futura = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
        gestore.aggiungi_evento(data_futura, 16, "Scacchi")

        # Uso un file temporaneo per il test
        temp_file = os.path.join(tempfile.gettempdir(), "test_eventi.pickle")

        try:
            # Salvo il gestore su file
            gestore.salva_su_file(temp_file)

            # Ricreo un gestore e leggo da file
            new_gestore = GestioneEventi()
            new_gestore.leggi_da_file(temp_file)

            # Verifico che l'evento sia stato caricato correttamente
            self.assertEqual(len(new_gestore._eventi), 1)

        finally:
            # Pulizia: rimuovo il file temporaneo
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_creazione_torneo(self):
        # Crea una data futura
        data_futura = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
        torneo = Torneo(data_futura, 16, "Scacchi")
        self.assertEqual(torneo._numero_partecipanti, 16)
        self.assertEqual(torneo._tipo, "Scacchi")
        self.assertEqual(torneo._data.strftime("%Y-%m-%d %H:%M:%S"), data_futura)

    def test_modifica_data(self):
        # Crea una data futura iniziale
        data_futura_iniziale = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
        torneo = Torneo(data_futura_iniziale, 16, "Scacchi")
        
        # Prova a modificare con una nuova data futura
        data_futura_nuova = (datetime.now() + timedelta(days=20)).strftime("%Y-%m-%d %H:%M:%S")
        torneo.data = data_futura_nuova
        self.assertEqual(torneo._data.strftime("%Y-%m-%d %H:%M:%S"), data_futura_nuova)
        
        # Prova a modificare con una data passata (deve generare un'eccezione)
        data_passata = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
        with self.assertRaises(ValueError):
            torneo.data = data_passata

    def test_modifica_partecipanti(self):
        # Crea una data futura
        data_futura = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
        torneo = Torneo(data_futura, 16, "Scacchi")
        
        # Prova a modificare il numero di partecipanti a un valore valido
        torneo.numero_partecipanti = 32
        self.assertEqual(torneo._numero_partecipanti, 32)
        
        # Prova a modificare il numero di partecipanti a un valore non valido
        with self.assertRaises(ValueError):
            torneo.numero_partecipanti = 0

    def test_modifica_tipo(self):
        # Crea una data futura
        data_futura = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
        torneo = Torneo(data_futura, 16, "Scacchi")
        
        # Prova a modificare il tipo a un valore valido
        torneo.tipo = "Dama"
        self.assertEqual(torneo._tipo, "Dama")
        
        # Prova a modificare il tipo a un valore non valido
        with self.assertRaises(ValueError):
            torneo.tipo = ""

    def test_get_evento(self):
        gestore = GestioneEventi()
        # Crea una data futura
        data_futura = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
        gestore.aggiungi_evento(data_futura, 16, "Scacchi")
        
        # Prova a recuperare un evento esistente
        evento = gestore.get_evento(data_futura)
        self.assertIsNotNone(evento)
        self.assertEqual(evento._tipo, "Scacchi")
        
        # Prova a recuperare un evento non esistente
        data_inesistente = (datetime.now() + timedelta(days=20)).strftime("%Y-%m-%d %H:%M:%S")
        with self.assertRaises(ValueError):
            gestore.get_evento(data_inesistente)

    def test_creazione_torneo_regression(self):
        # Crea una data futura
        data_futura = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
        
        # Test con data in formato errato
        with self.assertRaises(ValueError):
            _ = Torneo("data non valida", 16, "Scacchi")
        
        # Test con numero di partecipanti non valido
        with self.assertRaises(ValueError):
            _ = Torneo(data_futura, 0, "Scacchi")
        
        # Test con tipo non valido
        with self.assertRaises(ValueError):
            _ = Torneo(data_futura, 16, "")


if __name__ == "__main__":
    _ = unittest.main()
