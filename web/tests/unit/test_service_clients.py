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

    def setUp(self):
        self.sample_price_history = [
            {'Close': '1.69', 'Volume': '792600', 'Low': '1.61', 'Symbol': 'TST', 'Open': '1.82', 'High': '1.88', 'Adj_Close': '1.69', 'Date': '2016-11-17'},
            {'Close': '1.67', 'Volume': '756800', 'Low': '1.50', 'Symbol': 'TST', 'Open': '1.50', 'High': '1.73', 'Adj_Close': '1.67', 'Date': '2016-11-16'},
            {'Close': '1.48', 'Volume': '625600', 'Low': '1.34', 'Symbol': 'TST', 'Open': '1.34', 'High': '1.48', 'Adj_Close': '1.48', 'Date': '2016-11-15'}
        ]
        self.sample_source_stockinfo = {
            "name": "Test Company Name",
            "exchange": "TST",
            "current_price": 2.32,
            "year_high": 6.66,
            "price_history": self.sample_price_history
        }
        self.expected_pv_trend_data = {
            "max_volume": 792600,
            "min_volume": 625600,
            "volume_p75": 774700,
            "pv_data": [
                {
                    "Volume": 792600,
                    "pct_change": -7.1,
                    "Date": "2016-11-17"
                },
                {
                    "Volume": 756800,
                    "pct_change": 11.3,
                    "Date": "2016-11-16"
                },
                {
                    "Volume": 625600,
                    "pct_change": 10.4,
                    "Date": "2016-11-15"
                }
            ]
        }

    @patch('stockdata.controllers.stockinfo.YahooFinanceClient')
    def test_init_calls_source_get_stock_info(self, mock_source):
        mock_source.return_value.get_stock_info.return_value = self.sample_source_stockinfo
        stock = StockData("SYMB")
        mock_source.return_value.get_stock_info.assert_called_with("SYMB")

    @patch('stockdata.services.yahoo_finance_client.Share')
    def test_get_stock_info_returns_none_for_no_results(self, mock_share):
        mock_share.return_value.get_name.return_value = None
        stock = StockData("INVLD")
        actual_stock = stock.get_stock_info()
        self.assertIsNone(actual_stock)


    @patch('stockdata.controllers.stockinfo.YahooFinanceClient')
    def test_get_stock_info_returns_formatted_stock(self, mock_source):
        mock_source.return_value.get_stock_info.return_value = self.sample_source_stockinfo

        stock = StockData("SYMB")
        actual_stock = stock.get_stock_info()

        expected_stock = {
            "symbol": "SYMB",
            "name": "Test Company Name",
            "exchange": "TST",
            "current_price": 2.32,
            "year_high": 6.66
        }
        self.assertEqual(actual_stock, expected_stock)

    @patch('stockdata.controllers.stockinfo.YahooFinanceClient')
    def test_get_pv_trenddata_returns_formatted_data(self, mock_source):
        mock_source.return_value.get_stock_info.return_value = {
            "stock": "data",
            "price_history": self.sample_price_history
        }
        stock = StockData("SYMB")
        actual_pv_trend_data = stock.get_pv_trend_data()
        for key in self.expected_pv_trend_data.keys():
            self.assertTrue(key in actual_pv_trend_data.keys(), "key: {} was not in actual_pv_trend_data".format(key))
        self.assertEqual(actual_pv_trend_data, self.expected_pv_trend_data)

    @patch('stockdata.controllers.stockinfo.YahooFinanceClient')
    def test_get_pv_trenddata_gets_max_volume(self, mock_source):
        mock_source.return_value.get_stock_info.return_value = {
            "stock": "data",
            "price_history": self.sample_price_history
        }
        stock = StockData("SYMB")
        actual_pv_trend_data = stock.get_pv_trend_data()
        self.assertEqual(actual_pv_trend_data['max_volume'], 792600)

    @patch('stockdata.controllers.stockinfo.YahooFinanceClient')
    def test_get_pv_trenddata_gets_min_volume(self, mock_source):
        mock_source.return_value.get_stock_info.return_value = {
            "stock": "data",
            "price_history": self.sample_price_history
        }
        stock = StockData("SYMB")
        actual_pv_trend_data = stock.get_pv_trend_data()
        self.assertEqual(actual_pv_trend_data['min_volume'], 625600)

    @patch('stockdata.controllers.stockinfo.YahooFinanceClient')
    def test_get_pv_trenddata_gets_pv_data(self, mock_source):
        mock_source.return_value.get_stock_info.return_value = {
            "stock": "data",
            "price_history": self.sample_price_history
        }
        stock = StockData("SYMB")
        actual_pv_trend_data = stock.get_pv_trend_data()
        self.assertEqual(actual_pv_trend_data['pv_data'], self.expected_pv_trend_data['pv_data'])


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
