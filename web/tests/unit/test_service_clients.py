import unittest
from unittest.mock import patch
from flask_testing import TestCase
from stockdata import app
from stockdata.controllers.stockinfo import StockData
from stockdata.services.yahoo_finance_client import YahooFinanceClient


class StockDataTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    @patch('stockdata.controllers.stockinfo.YahooFinanceClient')
    def test_get_stock_info_calls_source_get_stock_info(self, mock_source):
        stock = StockData()
        stockdata = stock.get_stock_info("SYMB")
        mock_source.return_value.get_stock_info.assert_called_with("SYMB")

    @patch('stockdata.services.yahoo_finance_client.Share')
    def test_get_stock_info_returns_none_for_no_results(self, mock_share):
        stock = StockData()
        mock_share.return_value.get_name.return_value = None

        actual_stock = stock.get_stock_info("INVLD")

        self.assertIsNone(actual_stock)


    @patch('stockdata.services.yahoo_finance_client.Share')
    def test_get_stock_info_returns_formatted_stock(self, mock_share):
        stock = StockData()
        mock_share.return_value.get_stock_exchange.return_value = "TST"
        mock_share.return_value.get_name.return_value = "Test Company Name"
        mock_share.return_value.get_price.return_value = 2.32
        mock_share.return_value.get_year_high.return_value = 6.66
        price_history = [{'Close': '1.69', 'Volume': '792600', 'Low': '1.61', 'Symbol': 'TST', 'Open': '1.82', 'High': '1.88', 'Adj_Close': '1.69', 'Date': '2016-11-17'},
                   {'Close': '1.67', 'Volume': '756800', 'Low': '1.50', 'Symbol': 'TST', 'Open': '1.50', 'High': '1.73', 'Adj_Close': '1.67', 'Date': '2016-11-16'},
                   {'Close': '1.48', 'Volume': '625600', 'Low': '1.34', 'Symbol': 'TST', 'Open': '1.34', 'High': '1.48', 'Adj_Close': '1.48', 'Date': '2016-11-15'}
                   ]
        mock_share.return_value.get_historical.return_value = price_history

        expected_pv_trend_data = {
            "max_volume": 792600,
            "min_volume": 625600,
            "pv_data": [
                {
                    "volume": 792600,
                    "pct_change": -7.1,
                    "date": "2016-11-17"
                },
                {
                    "volume": 756800,
                    "pct_change": 11.3,
                    "date": "2016-11-16"
                },
                {
                    "volume": 625600,
                    "pct_change": 10.4,
                    "date": "2016-11-15"
                }
            ]
        }
        expected_stock = {
            "symbol": "SYMB",
            "name": "Test Company Name",
            "exchange": "TST",
            "current_price": 2.32,
            "year_high": 6.66,
            "pv_trend_data": expected_pv_trend_data
        }
        actual_stock = stock.get_stock_info("SYMB")

        self.assertEqual(actual_stock, expected_stock)


class YahooFinanceClientTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    @patch('stockdata.services.yahoo_finance_client.Share')
    def test_get_stock_info_gets_share_for_symbol(self, mock_share):
        YahooFinanceClient().get_stock_info("SYMB")
        mock_share.assert_called_with("SYMB")

    @patch('stockdata.services.yahoo_finance_client.Share')
    def test_get_stock_info_fetches_name(self, mock_share):
        YahooFinanceClient().get_stock_info("SYMB")
        mock_share.return_value.get_name.assert_called_with()

    @patch('stockdata.services.yahoo_finance_client.Share')
    def test_get_stock_info_fetches_exchange(self, mock_share):
        YahooFinanceClient().get_stock_info("SYMB")
        mock_share.return_value.get_stock_exchange.assert_called_with()

    @patch('stockdata.services.yahoo_finance_client.Share')
    def test_get_stock_info_fetches_year_high(self, mock_share):
        YahooFinanceClient().get_stock_info("SYMB")
        mock_share.return_value.get_year_high.assert_called_with()

    @patch('stockdata.services.yahoo_finance_client.Share')
    def test_get_stock_info_fetches_current_price(self, mock_share):
        YahooFinanceClient().get_stock_info("SYMB")
        mock_share.return_value.get_price.assert_called_with()

    @patch('stockdata.services.yahoo_finance_client.Share')
    def test_get_stock_info_fetches_historical_prices(self, mock_share):
        YahooFinanceClient().get_stock_info("SYMB")
        self.assertTrue(mock_share.return_value.get_historical.called)

if __name__ == '__main__':
    unittest.main()
