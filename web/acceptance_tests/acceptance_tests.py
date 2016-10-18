import unittest
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from flask_testing import LiveServerTestCase, TestCase
from stockdata import app


class ViewsUnitTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_home_view_calls_index_template(self):
        self.client.get('/')
        self.assert_template_used('index.html')

    def test_posting_symbol_returns_stock_info(self):
        response = self.client.post('/', data={'symbol': 'AETI'})
        stock = {
            "name": "American Electric Technologies Inc",
            "exchange": "NASDAQ"
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_context_variable('stock'), stock)


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

    def test_can_visit_homepage(self):
        # Jim needs to get some stock info.
        # He hears about a new app called StockData and goes to the homepage.
        self.browser.get(self.get_server_url())
        self.assertEqual("StockData", self.browser.title)
        self.assertIn("StockData", self.browser.find_element_by_tag_name('h1').text)

        # He sees an input box where he can input a stock symbol
        inputbox = self.browser.find_element_by_id("in_symbol")
        self.assertEqual(inputbox.get_attribute('placeholder'), "Enter a stock symbol")

        # He enters "AETI" and hits Enter.
        inputbox.send_keys("AETI")
        inputbox.send_keys(Keys.ENTER)

        # He sees the stock name and stock exchange on the page.
        self.assertIn("American Electric Technologies Inc",
                      self.browser.page_source)
        self.assertIn("NASDAQ",
                      self.browser.page_source)

        # He tries a different stock symbol and sees the new name and exchange on the page.
        inputbox = self.browser.find_element_by_id("in_symbol")
        inputbox.send_keys("CRNT")
        inputbox.send_keys(Keys.ENTER)

        self.assertIn("Ceragon Networks Ltd",
                      self.browser.page_source)
        self.assertIn("NASDAQ",
                      self.browser.page_source)


if __name__ == '__main__':
    unittest.main()