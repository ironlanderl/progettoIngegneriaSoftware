from Utenti.Utente import Utente
import unittest


class TestUtenti(unittest.TestCase):
    
    def test_creazione(self):
        utente = Utente()
        self.assertEqual(True, False)  # add assertion here

if __name__ == "__main__":
    _ = unittest.main()
