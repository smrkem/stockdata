import unittest
from selenium import webdriver as wd
from flask_testing import LiveServerTestCase, TestCase
from stockdata import app


class ViewsUnitTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_home_view_calls_index_template(self):
        response = self.client.get('/')
        self.assert_template_used('index.html')


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
        self.browser.get(self.get_server_url())

        self.assertEqual("StockData", self.browser.title)
        self.assertEqual("Hello, Karl", self.browser.find_element_by_tag_name('h1').text)


if __name__ == '__main__':
    unittest.main()