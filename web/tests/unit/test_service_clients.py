import unittest
from unittest.mock import patch
from flask_testing import TestCase
from stockdata import app
from stockdata.services.StockData import StockData
from stockdata.services.sources.YahooFinanceClient import YahooFinanceClient


class StockDataTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    @patch('stockdata.services.StockData.YahooFinanceClient')
    def test_get_stock_info_calls_source_get_stock_info(self, mock_source):
        mock_source.return_value.get_stock_info.return_value = {"stock":"data"}
        stock = StockData()
        stockdata = stock.get_stock_info("SYMB")
        mock_source.return_value.get_stock_info.assert_called_with("SYMB")
        self.assertEqual(stockdata, {"stock":"data"})



class YahooFinanceClientTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app


    @patch('stockdata.services.sources.YahooFinanceClient.Share')
    def test_get_stock_info_gets_share_for_symbol(self, mock_share):
        YahooFinanceClient().get_stock_info("SYMB")
        mock_share.assert_called_with("SYMB")

    @patch('stockdata.services.sources.YahooFinanceClient.Share')
    def test_get_stock_info_fetches_name(self, mock_share):
        YahooFinanceClient().get_stock_info("SYMB")
        mock_share.return_value.get_name.assert_called_with()

    @patch('stockdata.services.sources.YahooFinanceClient.Share')
    def test_get_stock_info_fetches_exchange(self, mock_share):
        YahooFinanceClient().get_stock_info("SYMB")
        mock_share.return_value.get_stock_exchange.assert_called_with()

    @patch('stockdata.services.sources.YahooFinanceClient.Share')
    def test_get_stock_info_returns_stock(self, mock_share):
        mock_share.return_value.get_stock_exchange.return_value = "TST"
        mock_share.return_value.get_name.return_value = "Test Company Name"

        expected_stock = {
            "symbol": "SYMB",
            "name": "Test Company Name",
            "exchange": "TST"
        }
        actual_stock = YahooFinanceClient().get_stock_info("SYMB")

        self.assertEqual(actual_stock, expected_stock)



if __name__ == '__main__':
    unittest.main()
