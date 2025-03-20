from Utenti.Cliente import Cliente
import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        cliente = Cliente()
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
