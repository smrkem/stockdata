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
        response = self.client.get('/')
        self.assert_template_used('index.html')

    def test_posting_symbol_returns_stock_name(self):
        response = self.client.post('/', data={'symbol': 'AETI'})
        self.assertEqual(response.status_code, 200)
        self.assertIn("American Electric Technologies Inc", response.data.decode('utf8'))


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

        self.assertIn("American Electric Technologies Inc",
                      self.browser.page_source)




if __name__ == '__main__':
    unittest.main()