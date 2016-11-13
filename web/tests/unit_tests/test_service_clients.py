import unittest
from unittest.mock import patch
from flask_testing import TestCase
from stockdata import app
from stockdata.services import StockData


class StockDataTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_has_a_list_of_sources(self):
        stock = StockData()
        self.assertIsInstance(stock.sources, type(list()))

    def test_stockdata_format(self):
        stock = StockData()
        self.assertIsInstance(stock.stockdata, type(dict()))
        self.assertEqual(stock.stockdata.keys(), [
            'Name', 'Exchange', 'Symbol'
        ])


if __name__ == '__main__':
    unittest.main()