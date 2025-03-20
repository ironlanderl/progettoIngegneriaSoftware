from Utenti.Feedback import Feedback
import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        feed = Feedback()
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
