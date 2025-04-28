import unittest
import tempfile
import os
import shutil

from Servizi.Servizio import Servizio
from Servizi.CampoBocce import CampoBocce
from Servizi.SalaBiliardo import SalaBiliardo
from Servizi.TavoloBiliardino import TavoloBiliardino
from Gestori.gestione_servizi import GestioneServizi


class TestServizi(unittest.TestCase):
    """
    Classe di test per le classi Servizio e le sue sottoclassi, e per GestioneServizi.
    """
    def setUp(self):
        """Configurazione prima di ogni test."""
        # Utilizza un file temporaneo per i test
        self.temp_dir = tempfile.gettempdir()
        self.temp_file = os.path.join(self.temp_dir, "test_servizi.pkl")
        self.default_file = "servizi.pickle" # File usato dalla gestione di default

        # Rimuove eventuali file esistenti per non avere interferenze tra i test
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        # Rimuove il file di default se esiste, per garantire un gestore pulito
        if os.path.exists(self.default_file):
            os.remove(self.default_file)

        # Inizializza il gestore. Ora caricherà dal file dummy creato.
        self.gestore = GestioneServizi()
        # Pulisce la lista servizi caricata dal file dummy per avere un punto di partenza vuoto per la maggior parte dei test.
        self.gestore._servizi.clear()


    def tearDown(self):
        """Pulizia dopo ogni test."""
        # Rimuove i file temporanei e di default usati nel test
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        if os.path.exists(self.default_file):
             os.remove(self.default_file)


    def test_creazione_servizio(self):
        """Verifica la creazione base di un Servizio."""
        servizio = Servizio(10.0, "Descrizione test", "Servizio test")
        self.assertEqual(servizio.costo, 10.0)
        self.assertEqual(servizio.descrizione, "Descrizione test")
        self.assertEqual(servizio.nome_servizio, "Servizio test")

    def test_campo_bocce(self):
        """Verifica la creazione e validazione di CampoBocce."""
        campo = CampoBocce(15.0, "Campo da bocce", "Campo Bocce 1")
        self.assertEqual(campo.costo, 15.0)
        self.assertEqual(campo.descrizione, "Campo da bocce")
        self.assertEqual(campo.nome_servizio, "Campo Bocce 1")


    def test_sala_biliardo(self):
        """Verifica la creazione e validazione di SalaBiliardo."""
        sala = SalaBiliardo(20.0, "Sala biliardo", "Sala Biliardo 1", numero_tavoli=3)
        self.assertEqual(sala.costo, 20.0)
        self.assertEqual(sala.descrizione, "Sala biliardo")
        self.assertEqual(sala.nome_servizio, "Sala Biliardo 1")
        self.assertEqual(sala.numero_tavoli, 3)
        with self.assertRaises(ValueError): # La classe solleva ValueError anche per tipo errato
            sala.numero_tavoli = -2
        with self.assertRaises(ValueError): # La classe solleva ValueError anche per tipo errato
             sala.numero_tavoli = "quattro"


    def test_tavolo_biliardino(self):
        """Verifica la creazione di TavoloBiliardino."""
        tavolo = TavoloBiliardino(5.0, "Tavolo da biliardino", "Biliardino 1")
        self.assertEqual(tavolo.costo, 5.0)
        self.assertEqual(tavolo.descrizione, "Tavolo da biliardino")
        self.assertEqual(tavolo.nome_servizio, "Biliardino 1")

    def test_aggiungi_campo_bocce(self):
        """Verifica l'aggiunta di un CampoBocce tramite GestioneServizi."""
        gestore = GestioneServizi()
        # Pulisce i servizi di default per isolare il test
        gestore._servizi.clear()
        gestore.aggiungi_campo_bocce(15.0, "Campo da bocce", "Campo Bocce 1")
        self.assertEqual(len(gestore._servizi), 1)
        servizio = gestore.get_servizio("Campo Bocce 1")
        self.assertIsNotNone(servizio)
        self.assertIsInstance(servizio, CampoBocce)

    def test_aggiungi_sala_biliardo(self):
        """Verifica l'aggiunta di una SalaBiliardo tramite GestioneServizi."""
        gestore = GestioneServizi()
        gestore._servizi.clear()
        gestore.aggiungi_sala_biliardo(20.0, "Sala biliardo", "Sala Biliardo 1", numero_tavoli=3)
        self.assertEqual(len(gestore._servizi), 1)
        servizio = gestore.get_servizio("Sala Biliardo 1")
        self.assertIsNotNone(servizio)
        self.assertIsInstance(servizio, SalaBiliardo)
        self.assertEqual(servizio.numero_tavoli, 3)

    def test_aggiungi_tavolo_biliardino(self):
        """Verifica l'aggiunta di un TavoloBiliardino tramite GestioneServizi."""
        gestore = GestioneServizi()
        gestore._servizi.clear()
        gestore.aggiungi_tavolo_biliardino(5.0, "Tavolo da biliardino", "Biliardino 1")
        self.assertEqual(len(gestore._servizi), 1)
        servizio = gestore.get_servizio("Biliardino 1")
        self.assertIsNotNone(servizio)
        self.assertIsInstance(servizio, TavoloBiliardino)

    def test_rimuovi_servizio(self):
        """Verifica la rimozione di un servizio tramite GestioneServizi."""
        gestore = GestioneServizi()
        gestore._servizi.clear()
        gestore.aggiungi_campo_bocce(15.0, "Campo da bocce", "Campo Bocce 1")
        servizio = gestore.get_servizio("Campo Bocce 1")
        self.assertIsNotNone(servizio)
        gestore.rimuovi_servizio(servizio)
        self.assertEqual(len(gestore._servizi), 0)
        self.assertIsNone(gestore.get_servizio("Campo Bocce 1"))

    def test_rimuovi_servizio_inesistente_raises(self):
        """Verifica che la rimozione di un servizio inesistente fallisca."""
        gestore = GestioneServizi()
        gestore._servizi.clear()
        dummy_servizio = Servizio(1, "d", "dummy")
        with self.assertRaises(ValueError):
             gestore.rimuovi_servizio(dummy_servizio)

    def test_rimuovi_servizio_by_nome(self):
         """Verifica la rimozione di un servizio per nome tramite GestioneServizi."""
         gestore = GestioneServizi()
         gestore._servizi.clear()
         gestore.aggiungi_campo_bocce(15.0, "Campo da bocce", "Campo Bocce 1")
         gestore.aggiungi_sala_biliardo(20.0, "Sala biliardo", "Sala Biliardo 1", numero_tavoli=3)
         self.assertEqual(len(gestore._servizi), 2)

         gestore.rimuovi_servizio_by_nome("Campo Bocce 1")
         self.assertEqual(len(gestore._servizi), 1)
         self.assertIsNone(gestore.get_servizio("Campo Bocce 1"))
         self.assertIsNotNone(gestore.get_servizio("Sala Biliardo 1"))

    def test_rimuovi_servizio_by_nome_inesistente_raises(self):
         """Verifica che la rimozione per nome di un servizio inesistente fallisca."""
         gestore = GestioneServizi()
         gestore._servizi.clear()
         with self.assertRaises(ValueError):
              gestore.rimuovi_servizio_by_nome("Servizio Inesistente")


    def test_get_servizio(self):
        """Verifica il recupero di un servizio per nome tramite GestioneServizi."""
        gestore = GestioneServizi()
        gestore._servizi.clear()
        gestore.aggiungi_campo_bocce(15.0, "Campo A", "Campo Bocce 1")
        servizio = gestore.get_servizio("Campo Bocce 1")
        self.assertIsNotNone(servizio)
        self.assertEqual(servizio.nome_servizio, "Campo Bocce 1")
        self.assertEqual(servizio.costo, 15.0)
        self.assertIsInstance(servizio, CampoBocce)

        # Verifica recupero servizio inesistente
        servizio_inesistente = gestore.get_servizio("Servizio Inesistente")
        self.assertIsNone(servizio_inesistente)

    def test_get_servizi_by_type(self):
        """Verifica il recupero di servizi filtrati per tipo."""
        gestore = GestioneServizi()
        gestore._servizi.clear()

        gestore.aggiungi_campo_bocce(15.0, "Campo A", "Campo Bocce 1")
        gestore.aggiungi_campo_bocce(16.0, "Campo B", "Campo Bocce 2")
        gestore.aggiungi_sala_biliardo(20.0, "Sala A", "Sala Biliardo 1", numero_tavoli=3)
        gestore.aggiungi_tavolo_biliardino(5.0, "Biliardino A", "Biliardino 1")

        campi_bocce = gestore.get_servizi_by_type(CampoBocce)
        self.assertEqual(len(campi_bocce), 2)
        for s in campi_bocce:
            self.assertIsInstance(s, CampoBocce)
        self.assertIn("Campo Bocce 1", [s.nome_servizio for s in campi_bocce])
        self.assertIn("Campo Bocce 2", [s.nome_servizio for s in campi_bocce])

        sale_biliardo = gestore.get_servizi_by_type(SalaBiliardo)
        self.assertEqual(len(sale_biliardo), 1)
        self.assertIsInstance(sale_biliardo[0], SalaBiliardo)
        self.assertEqual(sale_biliardo[0].nome_servizio, "Sala Biliardo 1")

        tavoli_biliardino = gestore.get_servizi_by_type(TavoloBiliardino)
        self.assertEqual(len(tavoli_biliardino), 1)
        self.assertIsInstance(tavoli_biliardino[0], TavoloBiliardino)
        self.assertEqual(tavoli_biliardino[0].nome_servizio, "Biliardino 1")

        servizi_generici = gestore.get_servizi_by_type(Servizio)
        self.assertEqual(len(servizi_generici), 4)
        for s in servizi_generici:
            self.assertIsInstance(s, Servizio)


    def test_scrittura_lettura(self):
        """Verifica il salvataggio e il caricamento dei servizi su file."""
        gestore = GestioneServizi()
        gestore._servizi.clear()

        gestore.aggiungi_campo_bocce(15.0, "Campo da bocce", "Campo Bocce 1")
        gestore.aggiungi_sala_biliardo(20.0, "Sala biliardo", "Sala Biliardo 1", numero_tavoli=3)
        gestore.aggiungi_tavolo_biliardino(5.0, "Tavolo da biliardino", "Biliardino 1")

        self.assertEqual(len(gestore._servizi), 3)

        # Usa un file temporaneo per il test di serializzazione
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, "test_servizi.pkl")
        default_file = "servizi.pickle" # File usato dalla gestione di default

        try:
            # Salva il gestore su file temporaneo
            gestore.salva_su_file(temp_file)

            # Crea un nuovo gestore e carica dal file salvato
            # Rimuove il file di default per assicurarsi che il nuovo gestore non lo carichi per errore
            if os.path.exists(default_file):
                 os.remove(default_file)

            # Rimuove il gestore creato in setUp per testare l'inizializzazione da zero
            del self.gestore

            # Sposta il file temporaneo nella directory corrente per farlo trovare da __init__
            self.assertTrue(os.path.exists(temp_file))
            shutil.move(temp_file, default_file)
            self.assertTrue(os.path.exists(default_file)) # Verifica che lo spostamento sia avvenuto

            nuovo_gestore = GestioneServizi()
            # __init__ dovrebbe aver caricato i dati dal file rinominato

            self.assertEqual(len(nuovo_gestore._servizi), 3)

            # Verifica che i servizi caricati siano corretti usando get_servizio e controllando i tipi
            campo = nuovo_gestore.get_servizio("Campo Bocce 1")
            self.assertIsNotNone(campo)
            self.assertIsInstance(campo, CampoBocce)
            self.assertEqual(campo.costo, 15.0)

            sala = nuovo_gestore.get_servizio("Sala Biliardo 1")
            self.assertIsNotNone(sala)
            self.assertIsInstance(sala, SalaBiliardo)
            self.assertEqual(sala.costo, 20.0)
            self.assertEqual(sala.numero_tavoli, 3)

            biliardino = nuovo_gestore.get_servizio("Biliardino 1")
            self.assertIsNotNone(biliardino)
            self.assertIsInstance(biliardino, TavoloBiliardino)
            self.assertEqual(biliardino.costo, 5.0)

        finally:
            # Pulisce i file temporanei e di default usati nel test
            # Il file temporaneo potrebbe essere stato rinominato, quindi rimuoviamo il file di default
            if os.path.exists(temp_file):
                os.remove(temp_file)
            if os.path.exists(default_file):
                 os.remove(default_file)


if __name__ == "__main__":
    unittest.main(verbosity=2)