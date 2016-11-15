import unittest
from unittest.mock import patch
from flask_testing import TestCase
from stockdata import app
from stockdata.services import StockData


class StockDataTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    @patch('stockdata.services.YahooFinanceClient')
    def test_get_stock_info_calls_source_get_stock_info(self, mock_source):
        mock_source.return_value.get_stock_info.return_value = {"stock":"data"}
        stock = StockData()
        stockdata = stock.get_stock_info("SYMB")
        mock_source.return_value.get_stock_info.assert_called_with("SYMB")
        self.assertEqual(stockdata, {"stock":"data"})

if __name__ == '__main__':
    unittest.main()
