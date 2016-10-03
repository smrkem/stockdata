import unittest
from selenium import webdriver as wd

LIVE_SERVER_URL = 'http://localhost:8000/'


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = wd.Firefox()
        self.browser.implicitly_wait(3)
        pass

    def tearDown(self):
        self.browser.quit()
        pass

    def test_test_is_running(self):
        self.browser.get(LIVE_SERVER_URL)
        self.assertRegex(self.browser.page_source, r'^<html(.*)</html>$')


if __name__ == '__main__':
    unittest.main()
