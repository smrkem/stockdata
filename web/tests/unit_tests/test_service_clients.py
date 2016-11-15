import unittest
from unittest import mock
from flask_testing import TestCase
from stockdata import app
from stockdata.services import StockData


class StockDataTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_has_source(self):
        '''
        Ultimately I'm gonna want to be able to get info from a list of sources,
        maybe depending on what's asked for in the query. For now, the minimal thing is for
        get_stock_info to call the YahooFinanceClient's get_stock_info.
        :return:
        '''
    def test_has_a_list_of_sources(self):
        stock = StockData()
        self.assertIsInstance(stock.sources, type(list()))

    def test_get_stockinfo_calls_source_get_stockinfo(self):
        stock = StockData()
        mock_source = mock.MagicMock()
        stock.sources.append(mock_source)
        stock.get_stock_info("SYMB")
        mock_source.get_stock_info.assert_called_with("SYMB")



if __name__ == '__main__':
    unittest.main()