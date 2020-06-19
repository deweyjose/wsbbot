import unittest

from api import app


class ApiTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def check_result(self, result, expected_status_code=200):
        self.assertEqual(result.status_code, expected_status_code)
        return result.data.decode('utf-8')

    def test_index(self):
        result = self.check_result(self.app.get('/'))

        terms = [
            "Stonks only go up",
            "Pump and dump",
            "All Time High",
            "Due Diligence",
            "It's different this time",
            "Don't fight the fed"
        ]

        self.assertIn(result, terms)


if __name__ == '__main__':
    unittest.main()
