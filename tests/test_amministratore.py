import unittest
from Utenti.Amministratore import Amministratore


class MyTestCase(unittest.TestCase):
    def test_something(self):
        amm = Amministratore()
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
