import unittest
import datetime
import os
import tempfile
import shutil

from Servizi.Prenotazione import Prenotazione
from Servizi.CampoBocce import CampoBocce
from Servizi.SalaBiliardo import SalaBiliardo
from Gestori.gestione_prenotazioni import GestionePrenotazioni

class TestPrenotazione(unittest.TestCase):
    """
    Classe di test per le classi Prenotazione e GestionePrenotazioni.
    """
    def setUp(self):
        """Configurazione prima di ogni test."""
        # Rimuove i file di default per garantire un ambiente pulito
        self.prenotazioni_file = "prenotazioni.pickle"
        self.orari_file = "orari.json"
        if os.path.exists(self.prenotazioni_file):
            os.remove(self.prenotazioni_file)
        if os.path.exists(self.orari_file):
            os.remove(self.orari_file)

        # Inizializza il gestore. Ora caricherà dai file dummy creati.
        self.gestione = GestionePrenotazioni()
        # Pulisco le liste caricate dai file dummy per avere un punto di partenza vuoto per la maggior parte dei test.
        self.gestione._prenotazioni.clear()

        self.utente_username1 = "mario"
        self.utente_username2 = "luigi"

        self.servizio1 = CampoBocce(15.0, "Campo da bocce", "Campo Bocce 1")
        self.servizio2 = SalaBiliardo(20.0, "Sala biliardo", "Sala Biliardo 1", numero_tavoli=3)

        # Date e durate per i test
        self.data1 = datetime.datetime(2025, 4, 20, 14, 0)
        self.data2 = datetime.datetime(2025, 4, 21, 16, 0)
        self.durata1 = datetime.timedelta(hours=2)  # Durata di 2 ore
        self.durata2 = datetime.timedelta(hours=3)  # Durata di 3 ore

        # Date/orari per test di disponibilità specifici
        self.data_lunedimattina = datetime.datetime(2025, 5, 5, 10, 0) # Lunedì 5 Maggio 2025, 10:00 (dentro orari)
        self.data_lunedisera = datetime.datetime(2025, 5, 5, 22, 0) # Lunedì 5 Maggio 2025, 22:00 (vicino chiusura)
        self.durata_lunga = datetime.timedelta(hours=2) # Durata che potrebbe sforare


    def tearDown(self):
        """Pulizia dopo ogni test."""
        # Rimuove i file creati o usati durante i test
        if os.path.exists(self.prenotazioni_file):
            os.remove(self.prenotazioni_file)
        if os.path.exists(self.orari_file):
            os.remove(self.orari_file)

    def test_creazione_prenotazione(self):
        """Verifica la creazione corretta di una prenotazione."""
        prenotazione = Prenotazione(self.servizio1, self.data1, self.durata1, self.utente_username1)
        self.assertEqual(prenotazione.servizio, self.servizio1)
        self.assertEqual(prenotazione.data, self.data1)
        self.assertEqual(prenotazione.durata, self.durata1)
        self.assertEqual(prenotazione.utente_prenotazione, self.utente_username1)
        expected_cost_timedelta = self.servizio1.costo * self.durata1
        self.assertEqual(prenotazione.costo_totale, expected_cost_timedelta)


    def test_prenotazione_attributi(self):
        """Verifica che la prenotazione possieda gli attributi richiesti."""
        prenotazione = Prenotazione(self.servizio1, self.data1, self.durata1, self.utente_username1)
        self.assertTrue(hasattr(prenotazione, 'servizio'))
        self.assertTrue(hasattr(prenotazione, 'data'))
        self.assertTrue(hasattr(prenotazione, 'durata'))
        self.assertTrue(hasattr(prenotazione, 'utente_prenotazione'))
        self.assertTrue(hasattr(prenotazione, 'data_fine'))
        self.assertTrue(hasattr(prenotazione, 'costo_totale'))


    def test_modifica_prenotazione(self):
        """Verifica la possibilità di modificare data e durata di una prenotazione tramite i setter."""
        prenotazione = Prenotazione(self.servizio1, self.data1, self.durata1, self.utente_username1)
        nuova_data = datetime.datetime(2025, 4, 21, 16, 0)  # 21 Aprile 2025, ore 16:00
        nuova_durata = datetime.timedelta(hours=3)  # Durata di 3 ore
        
        try:
            prenotazione.data = nuova_data
            prenotazione.durata = nuova_durata
            self.assertEqual(prenotazione.data, nuova_data)
            self.assertEqual(prenotazione.durata, nuova_durata)
            # Verifica che data_fine e costo_totale si aggiornino
            self.assertEqual(prenotazione.data_fine, nuova_data + nuova_durata)
            expected_cost_timedelta = self.servizio1.costo * nuova_durata
            self.assertEqual(prenotazione.costo_totale, expected_cost_timedelta)

        except AttributeError:
            # Questo test passa se i setter esistono e funzionano.
            # Se AttributeError fosse sollevato, il test fallirebbe.
            self.fail("Impossibile modificare gli attributi della prenotazione tramite setter.")

    def test_prenotazione_setter_validation(self):
        """Verifica la validazione dei setter nella classe Prenotazione."""
        prenotazione = Prenotazione(self.servizio1, self.data1, self.durata1, self.utente_username1)

        # Test setter data
        with self.assertRaises(TypeError):
            prenotazione.data = "data non valida" # Deve essere datetime
        
        # Test setter durata
        with self.assertRaises(ValueError):
            prenotazione.durata = "durata non valida" # Non è un timedelta, ma il controllo <=0 fallisce prima
        with self.assertRaises(ValueError):
            prenotazione.durata = datetime.timedelta(hours=-1) # Deve essere positivo
            
        # Test setter servizio
        with self.assertRaises(ValueError):
            prenotazione.id_servizio = None # Non può essere None
        with self.assertRaises(ValueError):
            prenotazione.id_servizio = "non un servizio" # Non deve essere istanza di Servizio

        # Test setter utente_prenotazione
        with self.assertRaises(ValueError):
             prenotazione.utente_prenotazione = "" # Non può essere vuoto


class TestGestionePrenotazioni(unittest.TestCase):
    """
    Classe di test per la classe GestionePrenotazioni.
    """
    def setUp(self):
        """Configurazione prima di ogni test."""
        # Rimuove i file di default per garantire un ambiente pulito
        self.prenotazioni_file = "prenotazioni.pickle"
        self.orari_file = "orari.json"
        if os.path.exists(self.prenotazioni_file):
            os.remove(self.prenotazioni_file)
        if os.path.exists(self.orari_file):
            os.remove(self.orari_file)

        # Inizializza il gestore. Ora caricherà dai file dummy creati.
        self.gestione = GestionePrenotazioni()
        # Pulisco le liste caricate dai file dummy per avere un punto di partenza vuoto per la maggior parte dei test.
        self.gestione._prenotazioni.clear()

        self.utente_username1 = "mario"
        self.utente_username2 = "luigi"

        self.servizio1 = CampoBocce(15.0, "Campo da bocce", "Campo Bocce 1") # CampoBocce prende 3 argomenti + self
        self.servizio2 = SalaBiliardo(20.0, "Sala biliardo", "Sala Biliardo 1", numero_tavoli=3) # SalaBiliardo prende 4 argomenti + self

        # Date e durate per i test
        self.data1 = datetime.datetime(2025, 4, 20, 14, 0)
        self.data2 = datetime.datetime(2025, 4, 21, 16, 0)
        self.durata1 = datetime.timedelta(hours=2)  # Durata di 2 ore
        self.durata2 = datetime.timedelta(hours=3)  # Durata di 3 ore

        # Date/orari per test di disponibilità specifici
        self.data_lunedimattina = datetime.datetime(2025, 5, 5, 10, 0) # Lunedì 5 Maggio 2025, 10:00 (dentro orari)
        self.data_lunedisera = datetime.datetime(2025, 5, 5, 22, 0) # Lunedì 5 Maggio 2025, 22:00 (vicino chiusura)
        self.durata_lunga = datetime.timedelta(hours=2) # Durata che potrebbe sforare


    def tearDown(self):
        """Pulizia dopo ogni test."""
        # Rimuove i file creati o usati durante i test
        if os.path.exists(self.prenotazioni_file):
            os.remove(self.prenotazioni_file)
        if os.path.exists(self.orari_file):
            os.remove(self.orari_file)

    def test_aggiungi_prenotazione(self):
        """Verifica l'aggiunta di una prenotazione valida."""
        prenotazione = self.gestione.aggiungi_prenotazione(self.servizio1, self.data1, self.durata1, self.utente_username1)
        self.assertEqual(len(self.gestione._prenotazioni), 1)
        self.assertEqual(prenotazione.servizio, self.servizio1)
        self.assertEqual(prenotazione.utente_prenotazione, self.utente_username1)
        self.assertIsNotNone(self.gestione.get_prenotazione(self.data1, self.utente_username1)) # Verifica che sia recuperabile

    def test_aggiungi_prenotazione_non_disponibile_raises(self):
        """Verifica che l'aggiunta di una prenotazione non disponibile sollevi un'eccezione."""
        # Aggiunge una prenotazione che occupa il servizio
        self.gestione.aggiungi_prenotazione(self.servizio1, self.data1, self.durata1, self.utente_username1) # 14:00 - 16:00

        # Tenta di aggiungere una prenotazione sovrapposta per lo stesso servizio
        overlapping_data = self.data1 + datetime.timedelta(hours=1) # 15:00
        overlapping_durata = datetime.timedelta(hours=1) # 15:00 - 16:00
        with self.assertRaises(Exception): # La classe solleva Exception generica
             self.gestione.aggiungi_prenotazione(self.servizio1, overlapping_data, overlapping_durata, self.utente_username2)

    def test_get_prenotazione(self):
        """Verifica il recupero di una prenotazione esistente e None se inesistente."""
        self.gestione.aggiungi_prenotazione(self.servizio1, self.data1, self.durata1, self.utente_username1)
        self.gestione.aggiungi_prenotazione(self.servizio2, self.data2, self.durata2, self.utente_username2)

        prenotazione1 = self.gestione.get_prenotazione(self.data1, self.utente_username1)
        self.assertIsNotNone(prenotazione1)
        self.assertEqual(prenotazione1.servizio, self.servizio1)
        self.assertEqual(prenotazione1.data, self.data1)
        self.assertEqual(prenotazione1.durata, self.durata1)
        self.assertEqual(prenotazione1.utente_prenotazione, self.utente_username1) # Corretto

        prenotazione2 = self.gestione.get_prenotazione(self.data2, self.utente_username2)
        self.assertIsNotNone(prenotazione2)
        self.assertEqual(prenotazione2.servizio, self.servizio2)
        self.assertEqual(prenotazione2.data, self.data2)
        self.assertEqual(prenotazione2.durata, self.durata2)
        self.assertEqual(prenotazione2.utente_prenotazione, self.utente_username2) # Corretto

        # Prenotazione inesistente (data corretta, utente sbagliato)
        prenotazione_none_user = self.gestione.get_prenotazione(self.data1, "utente_inesistente")
        self.assertIsNone(prenotazione_none_user)

        # Prenotazione inesistente (data sbagliata, utente corretto)
        prenotazione_none_data = self.gestione.get_prenotazione(datetime.datetime(2025, 4, 22, 14, 0), self.utente_username1)
        self.assertIsNone(prenotazione_none_data)

        # Prenotazione inesistente (data e utente sbagliati)
        prenotazione_none_both = self.gestione.get_prenotazione(datetime.datetime(2025, 4, 22, 14, 0), "utente_inesistente")
        self.assertIsNone(prenotazione_none_both)


    def test_elimina_prenotazione(self):
        """Verifica l'eliminazione di una prenotazione esistente."""
        self.gestione.aggiungi_prenotazione(self.servizio1, self.data1, self.durata1, self.utente_username1)
        self.gestione.aggiungi_prenotazione(self.servizio2, self.data2, self.durata2, self.utente_username2)
        self.assertEqual(len(self.gestione._prenotazioni), 2)

        self.gestione.elimina_prenotazione(self.data1, self.utente_username1)
        self.assertEqual(len(self.gestione._prenotazioni), 1)
        self.assertIsNone(self.gestione.get_prenotazione(self.data1, self.utente_username1))
        self.assertIsNotNone(self.gestione.get_prenotazione(self.data2, self.utente_username2))

    def test_elimina_prenotazione_inesistente_raises(self):
        """Verifica che l'eliminazione di una prenotazione inesistente fallisca."""
        # Assicurati che non ci siano prenotazioni
        self.gestione._prenotazioni.clear()
        with self.assertRaises(ValueError):
            self.gestione.elimina_prenotazione(self.data1, self.utente_username1)


    def test_salva_leggi_file(self):
        """Verifica il salvataggio e il caricamento delle prenotazioni su file."""
        self.gestione.aggiungi_prenotazione(self.servizio1, self.data1, self.durata1, self.utente_username1)
        self.gestione.aggiungi_prenotazione(self.servizio2, self.data2, self.durata2, self.utente_username2)
        
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, "test_prenotazioni.pkl")
        
        try:
            self.gestione.salva_su_file(temp_file)

            # Crea un nuovo gestore e carica dal file salvato
            # Rimuove i file di default per assicurarsi che il nuovo gestore non li carichi per errore
            if os.path.exists(self.prenotazioni_file):
                 os.remove(self.prenotazioni_file)
            if os.path.exists(self.orari_file):
                 os.remove(self.orari_file)

            # Rimuove il gestore creato in setUp per testare l'inizializzazione da zero
            del self.gestione

            # Sposta il file temporaneo nella directory corrente per farlo trovare da __init__
            self.assertTrue(os.path.exists(temp_file))
            shutil.move(temp_file, self.prenotazioni_file)
            self.assertTrue(os.path.exists(self.prenotazioni_file)) # Verifica che lo spostamento sia avvenuto

            nuovo_gestore = GestionePrenotazioni()
            # __init__ dovrebbe aver caricato i dati dal file prenotazioni rinominato

            self.assertEqual(len(nuovo_gestore._prenotazioni), 2)

            # Verifica che le prenotazioni caricate siano corrette
            prenotazione1 = nuovo_gestore.get_prenotazione(self.data1, self.utente_username1)
            self.assertIsNotNone(prenotazione1)
            self.assertEqual(prenotazione1.servizio.nome_servizio, self.servizio1.nome_servizio)
            self.assertEqual(prenotazione1.data, self.data1)
            self.assertEqual(prenotazione1.utente_prenotazione, self.utente_username1) # Corretto

            prenotazione2 = nuovo_gestore.get_prenotazione(self.data2, self.utente_username2)
            self.assertIsNotNone(prenotazione2)
            self.assertEqual(prenotazione2.servizio.nome_servizio, self.servizio2.nome_servizio)
            self.assertEqual(prenotazione2.data, self.data2)
            self.assertEqual(prenotazione2.utente_prenotazione, self.utente_username2) # Corretto

        finally:
            # Pulisce i file temporanei e di default
            if os.path.exists(temp_file): # Potrebbe non esistere se rinominato
                os.remove(temp_file)
            if os.path.exists(self.prenotazioni_file): # Rimuove il file rinominato
                 os.remove(self.prenotazioni_file)
            if os.path.exists(self.orari_file):
                 os.remove(self.orari_file)


    def test_controlla_disponibilita_overlapping_bookings(self):
        """Verifica il controllo di disponibilità con prenotazioni sovrapposte."""
        # Prenotazione esistente: Campo Bocce 1, 2025-04-20 14:00 - 16:00
        self.gestione.aggiungi_prenotazione(self.servizio1, self.data1, self.durata1, self.utente_username1)

        # Test prenotazione che inizia durante quella esistente
        overlapping_start = self.data1 + datetime.timedelta(hours=1) # 15:00
        self.assertFalse(self.gestione.controlla_disponibilita(self.servizio1, overlapping_start, datetime.timedelta(hours=1))) # 15:00 - 16:00

        # Test prenotazione che finisce durante quella esistente
        overlapping_end_data = self.data1 - datetime.timedelta(hours=1) # 13:00
        overlapping_end_durata = datetime.timedelta(hours=2) # 13:00 - 15:00
        self.assertFalse(self.gestione.controlla_disponibilita(self.servizio1, overlapping_end_data, overlapping_end_durata))

        # Test prenotazione che contiene quella esistente
        containing_data = self.data1 - datetime.timedelta(hours=1) # 13:00
        containing_durata = datetime.timedelta(hours=3) # 13:00 - 16:00
        self.assertFalse(self.gestione.controlla_disponibilita(self.servizio1, containing_data, containing_durata))

        # Test prenotazione contenuta in quella esistente
        contained_data = self.data1 + datetime.timedelta(minutes=30) # 14:30
        contained_durata = datetime.timedelta(hours=1) # 14:30 - 15:30
        self.assertFalse(self.gestione.controlla_disponibilita(self.servizio1, contained_data, contained_durata))

        # Test prenotazione che inizia esattamente alla fine di quella esistente (dovrebbe essere disponibile)
        exact_end_start = self.data1 + self.durata1 # 16:00
        self.assertTrue(self.gestione.controlla_disponibilita(self.servizio1, exact_end_start, datetime.timedelta(hours=1))) # 16:00 - 17:00

        # Test prenotazione che finisce esattamente all'inizio di quella esistente (dovrebbe essere disponibile)
        exact_start_end_data = self.data1 - datetime.timedelta(hours=1) # 13:00
        exact_start_end_durata = datetime.timedelta(hours=1) # 13:00 - 14:00
        self.assertTrue(self.gestione.controlla_disponibilita(self.servizio1, exact_start_end_data, exact_start_end_durata))

        # Test prenotazione per un altro servizio nello stesso orario (dovrebbe essere disponibile)
        self.assertTrue(self.gestione.controlla_disponibilita(self.servizio2, self.data1, self.durata1))


    def test_controlla_disponibilita_opening_hours(self):
        """Verifica il controllo di disponibilità basato sugli orari di apertura."""
        # Giorno: Lunedì. Orari: 09:00 - 23:00 (impostati in setUp per tutti i giorni tramite file dummy)

        # Test prenotazione interamente dentro l'orario
        data_ok = datetime.datetime(2025, 5, 5, 10, 0) # Lunedì 10:00
        durata_ok = datetime.timedelta(hours=1) # 11:00 fine
        self.assertTrue(self.gestione.controlla_disponibilita(self.servizio1, data_ok, durata_ok))

        # Test prenotazione che inizia prima dell'apertura
        data_early = datetime.datetime(2025, 5, 5, 8, 59) # Lunedì 08:59
        durata_short = datetime.timedelta(minutes=30)
        self.assertFalse(self.gestione.controlla_disponibilita(self.servizio1, data_early, durata_short))

        # Test prenotazione che finisce dopo la chiusura
        data_late_start = datetime.datetime(2025, 5, 5, 22, 30) # Lunedì 22:30
        durata_long = datetime.timedelta(hours=1) # 23:30 fine
        self.assertFalse(self.gestione.controlla_disponibilita(self.servizio1, data_late_start, durata_long))

        # Test prenotazione che inizia esattamente all'apertura
        data_at_open = datetime.datetime(2025, 5, 5, 9, 0) # Lunedì 09:00
        durata_short = datetime.timedelta(hours=1) # 10:00 fine
        self.assertTrue(self.gestione.controlla_disponibilita(self.servizio1, data_at_open, durata_short))

        # Test prenotazione che finisce esattamente alla chiusura
        data_ends_at_close = datetime.datetime(2025, 5, 5, 22, 0) # Lunedì 22:00
        durata_exact = datetime.timedelta(hours=1) # 23:00 fine
        self.assertTrue(self.gestione.controlla_disponibilita(self.servizio1, data_ends_at_close, durata_exact))

        # Test prenotazione che finisce un minuto dopo la chiusura
        data_ends_after_close = datetime.datetime(2025, 5, 5, 22, 0) # Lunedì 22:00
        durata_over = datetime.timedelta(hours=1, minutes=1) # 23:01 fine
        self.assertFalse(self.gestione.controlla_disponibilita(self.servizio1, data_ends_after_close, durata_over))

        # Test prenotazione che è esattamente l'intero orario di apertura (esempio: 09:00-23:00 = 14 ore)
        full_day_duration = datetime.timedelta(hours=14)
        self.assertTrue(self.gestione.controlla_disponibilita(self.servizio1, data_at_open, full_day_duration))

        # Test prenotazione che supera di un minuto l'intero orario
        full_day_duration_over = datetime.timedelta(hours=14, minutes=1)
        self.assertFalse(self.gestione.controlla_disponibilita(self.servizio1, data_at_open, full_day_duration_over))


    def test_salva_leggi_orari(self):
        """Verifica il salvataggio e caricamento degli orari su file JSON."""
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, "test_orari.json")

        # Modifica gli orari (caricati dal file dummy in setUp)
        self.gestione.set_orario_apertura("Monday", "08:00")
        self.gestione.set_orario_chiusura("Sunday", "20:00")

        # Salva su file temporaneo
        self.gestione.salva_orari_su_file(temp_file)

        # Crea un nuovo gestore e carica gli orari dal file temporaneo
        # Rimuove i file di default per assicurarsi che il nuovo gestore non li carichi per errore
        if os.path.exists(self.prenotazioni_file):
                 os.remove(self.prenotazioni_file)
        if os.path.exists(self.orari_file):
                 os.remove(self.orari_file)

        # Rimuove il gestore creato in setUp per testare l'inizializzazione da zero
        del self.gestione

        # Sposta il file temporaneo nella directory corrente per farlo trovare da __init__
        self.assertTrue(os.path.exists(temp_file))
        shutil.move(temp_file, self.orari_file)
        self.assertTrue(os.path.exists(self.orari_file)) # Verifica che lo spostamento sia avvenuto


        nuovo_gestore = GestionePrenotazioni()
        # __init__ dovrebbe aver caricato i dati dal file orari rinominato

        # Verifica che gli orari caricati siano corretti
        self.assertEqual(nuovo_gestore.get_orario_apertura("Monday"), "08:00")
        self.assertEqual(nuovo_gestore.get_orario_chiusura("Sunday"), "20:00")
        # Verifica che gli altri orari siano stati caricati (se presenti nel file salvato)
        # La classe GestionePrenotazioni salva l'intero dizionario, quindi dovrebbero esserci tutti i giorni.
        self.assertEqual(nuovo_gestore.get_orario_apertura("Tuesday"), "09:00") # Presumendo che fosse 09:00 di default

        # Pulizia
        if os.path.exists(temp_file): # Potrebbe non esistere se rinominato
            os.remove(temp_file)
        if os.path.exists(self.prenotazioni_file):
                 os.remove(self.prenotazioni_file)
        if os.path.exists(self.orari_file): # Rimuove il file rinominato
                 os.remove(self.orari_file)


if __name__ == '__main__':
    unittest.main(verbosity=2)