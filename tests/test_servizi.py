import unittest
import tempfile
import copy
import os

from Servizi.Servizio import Servizio
from Servizi.CampoBocce import CampoBocce
from Servizi.SalaBiliardo import SalaBiliardo
from Servizi.TavoloBiliardino import TavoloBiliardino
from Gestori.gestioneServizi import GestioneServizi


class TestServizi(unittest.TestCase):

    def test_creazione_servizio(self):
        servizio = Servizio(10.0, "Descrizione test", "Servizio test")
        self.assertEqual(servizio.costo, 10.0)
        self.assertEqual(servizio.descrizione, "Descrizione test")
        self.assertEqual(servizio.nome_servizio, "Servizio test")

    def test_campo_bocce(self):
        campo = CampoBocce(15.0, "Campo da bocce", "Campo Bocce 1", 2, "Contanti/Carta")
        self.assertEqual(campo.costo, 15.0)
        self.assertEqual(campo.descrizione, "Campo da bocce")
        self.assertEqual(campo.nome_servizio, "Campo Bocce 1")
        self.assertEqual(campo.numero_campi, 2)
        self.assertEqual(campo.opzioni_pagamento, "Contanti/Carta")

        with self.assertRaises(ValueError):
            campo.numero_campi = -1
        with self.assertRaises(ValueError):
            campo.opzioni_pagamento = ""

    def test_sala_biliardo(self):
        sala = SalaBiliardo(20.0, "Sala biliardo", "Sala Biliardo 1", 3)
        self.assertEqual(sala.costo, 20.0)
        self.assertEqual(sala.descrizione, "Sala biliardo")
        self.assertEqual(sala.nome_servizio, "Sala Biliardo 1")
        self.assertEqual(sala.numero_tavoli, 3)

        with self.assertRaises(ValueError):
            sala.numero_tavoli = -2

    def test_tavolo_biliardino(self):
        tavolo = TavoloBiliardino(5.0, "Tavolo da biliardino", "Biliardino 1", 2.5)
        self.assertEqual(tavolo.costo, 5.0)
        self.assertEqual(tavolo.descrizione, "Tavolo da biliardino")
        self.assertEqual(tavolo.nome_servizio, "Biliardino 1")
        self.assertEqual(tavolo.costo_per_partita, 2.5)

        with self.assertRaises(ValueError):
            tavolo.costo_per_partita = -1.0

    def test_aggiungi_campo_bocce(self):
        gestore = GestioneServizi()
        # Modifico la chiamata secondo la firma del metodo nel file gestioneServizi.py
        gestore.aggiungi_campo_bocce(15.0, "Campo da bocce", "Campo Bocce 1", 2, "Contanti/Carta")
        self.assertEqual(len(gestore._servizi), 1)

    def test_aggiungi_sala_biliardo(self):
        gestore = GestioneServizi()
        gestore.aggiungi_sala_biliardino(20.0, "Sala biliardo", "Sala Biliardo 1", 3)
        self.assertEqual(len(gestore._servizi), 1)

    def test_aggiungi_tavolo_biliardino(self):
        gestore = GestioneServizi()
        gestore.aggiungi_tavolo_biliardino(5.0, "Tavolo da biliardino", "Biliardino 1", 2.5)
        self.assertEqual(len(gestore._servizi), 1)

    def test_rimuovi_servizio(self):
        gestore = GestioneServizi()
        gestore.aggiungi_campo_bocce(15.0, "Campo da bocce", "Campo Bocce 1", 2, "Contanti/Carta")
        gestore.rimuovi_servizio("Campo Bocce 1")
        self.assertEqual(len(gestore._servizi), 0)

    def test_get_servizio(self):
        gestore = GestioneServizi()
        gestore.aggiungi_campo_bocce(15.0, "Campo da bocce", "Campo Bocce 1", 2, "Contanti/Carta")
        servizio = gestore.get_servizio("Campo Bocce 1")
        self.assertEqual(servizio.nome_servizio, "Campo Bocce 1")
        self.assertEqual(servizio.costo, 15.0)

    def test_scrittura_lettura(self):
        # Creo un gestore e aggiungo servizi
        gestore = GestioneServizi()
        gestore.aggiungi_campo_bocce(15.0, "Campo da bocce", "Campo Bocce 1", 2, "Contanti/Carta")
        gestore.aggiungi_sala_biliardino(20.0, "Sala biliardo", "Sala Biliardo 1", 3)
        gestore.aggiungi_tavolo_biliardino(5.0, "Tavolo da biliardino", "Biliardino 1", 2.5)

        # Uso un file temporaneo per il test
        temp_file = os.path.join(tempfile.gettempdir(), "test_servizi.json")

        try:
            # Salvo il gestore su file
            gestore.salva_su_file(temp_file)

            # Ricreo un gestore e leggo da file
            new_gestore = GestioneServizi()
            new_gestore.leggi_da_file(temp_file)

            # Verifico che i servizi siano stati caricati correttamente
            self.assertEqual(len(new_gestore._servizi), 3)

        finally:
            # Pulizia: rimuovo il file temporaneo
            if os.path.exists(temp_file):
                os.remove(temp_file)


if __name__ == "__main__":
    _ = unittest.main()