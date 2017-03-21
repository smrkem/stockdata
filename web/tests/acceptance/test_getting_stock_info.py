import unittest, json
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from flask_testing import LiveServerTestCase
from stockdata import app


class NewVisitorTest(LiveServerTestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 8943
        return app

    def setUp(self):
        self.browser = wd.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def submit_stock_symbol(self, symbol):
        inputbox = self.browser.find_element_by_id("in_symbol")
        inputbox.send_keys(symbol)
        inputbox.send_keys(Keys.ENTER)

    def check_stock_info_for(self, stockinfo):
        stockinfo_table = self.browser.find_element_by_id("stock-info")
        for value in stockinfo:
            self.assertIn(value, stockinfo_table.text, "Check {} is in stock info".format(value))
        current_price = stockinfo_table.find_element_by_id("stck-curent-price").text
        year_high = stockinfo_table.find_element_by_id("stck-1yr-high").text
        self.assertRegexpMatches(current_price, r'^\d+\.\d+$')
        self.assertRegexpMatches(year_high, r'^\d+\.\d+$')

    def test_can_visit_homepage(self):
        # Jim needs to get some stock info.
        # He hears about a new app called StockData and goes to the homepage.
        self.browser.get(self.get_server_url())
        self.assertEqual("StockData", self.browser.title)
        self.assertIn("StockData", self.browser.find_element_by_tag_name('h1').text)

        # He sees an input box where he can input a stock symbol
        inputbox = self.browser.find_element_by_id("in_symbol")
        self.assertEqual(inputbox.get_attribute('placeholder'), "Enter a stock symbol")

        # Jim tries to enter some junk to see if the app breaks
        self.submit_stock_symbol("INVALID")
        errors = self.browser.find_element_by_id("errors")
        self.assertIn("Could not find any stock for symbol: 'INVALID'", errors.text)

        # He enters "AETI" and hits Enter.
        self.submit_stock_symbol("AETI")

        # He sees the stock name and stock exchange on the page.
        self.check_stock_info_for(("AETI", "American Electric Technologies", "NCM"))

    def test_can_view_stock_info(self):
        # Jim returns to the app
        self.browser.get(self.get_server_url())

        # He tries a different stock symbol and sees the new name and exchange on the page.
        self.submit_stock_symbol("CRNT")
        self.check_stock_info_for(("CRNT", "Ceragon Networks Ltd", "NMS"))

        # Along with some price-volume trend data
        pv_trend_graph = self.browser.find_element_by_id("price-volume-trend-graph")
        pv_trend_data = json.loads(pv_trend_graph.get_attribute("data-pv_data"))
        self.assertIsInstance(pv_trend_data, type(dict()))
        for key in ['max_volume', 'min_volume', 'pv_data']:
            self.assertTrue(key in pv_trend_data.keys())
        self.assertIsInstance(pv_trend_data['pv_data'], type(list()))
        self.assertGreater(len(pv_trend_data['pv_data']), 2)


if __name__ == '__main__':
    unittest.main()
